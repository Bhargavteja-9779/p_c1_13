# Review 02 — Machine-learning methods reviewer

**Focus:** fairness of the ML baselines, tuning budget, threshold choice, leakage, and whether the ML criticism is a strawman.

## Summary

The paper uses two supervised detectors (D8 LightGBM on 14 summary features; D9 GRU on raw fields) and one self-supervised order network (D10) to argue that ML detectors "flagged more progressors only with excess false alarms". It also argues that "a model's flag rate on true no-change data should be reported before any claim of earlier detection". I read `code/src/models/detectors.py`, `run_all.py`, `summarise.py` and the leakage audit. I also ran read-only checks on the data: training-set sizes, per-seed rates, and how D8's false alarms relate to severity.

I found no test-set leakage. The split is patient-level, and thresholds and model selection use only training and validation data. But the ML detectors are built in a way that makes poor false-alarm behaviour very likely. The evaluation also asks D8/D9 to do something different from what they were trained to do. Together, these make the ML criticism look largely like a strawman. The abstract and Discussion generalise it to ML "increasingly proposed for this task".

## Issues

### 1. FATAL — D8/D9 are trained to answer a prognostic question but scored as change detectors; their "false alarms" partly reflect risk prediction
*Location:* Methods D8: "gradient-boosted trees on 14 summary features of the first k tests, trained to predict the reference label". Discussion: "In our data the true false-alarm rate of the tabular model ranged from 3.6% to 27.7%".

*Problem:* The training label is whether the full series of ~11 fields over ~13 years has a significant MD slope. A model that minimises loss for this label will learn level and severity features that predict future decline. These features are in the feature set: `md[-1]`, `md.mean()`, `Y.std(0).mean()`, range and duration. Then the model is asked to stay silent on Artes eyes, which are glaucomatous eyes with real risk. I checked the raw results. D8's Artes false-alarm rate at k = 3 correlates strongly with the patient's mean sensitivity (Spearman ρ = −0.71). By tertile of mean sensitivity, flag rates are 41%, 26% and 16%. The shuffle audit confirms the same: D8 flags 17.3% of shuffled series (k = 3), so most flags do not depend on test order at all. The flags are severity-driven risk predictions, not false progression calls produced by noise in the trend. The paper's conclusion that "the threshold does not control false alarms in a new eye with short follow-up" may still hold. But the mechanism is a mismatch between the training label and the target estimand. The paper presents it as a generic property of ML detectors.

*Fix:* Train ML detectors on a label that encodes change within the observed window, or make the features order-dependent only. Examples: use differences or slopes only, with no level features; or use contrastive training on true versus shuffled order, as in D10. Report an ablation without level features. Discuss the prognosis-versus-detection distinction explicitly, and reword the Discussion and abstract to say that "a model trained to predict future progression risk is not a progression detector and flags high-risk stable eyes".

### 2. MAJOR — Training data are tiny and the large unlabelled cohort is left unused; the baselines are under-powered by construction
*Location:* Methods D8/D9; Results, Table 2.

*Problem:* Only eyes with ≥ 8 tests and a determinate label are used. I re-derived the counts: training has 93 progressors and 99 stable eyes (192 eyes), and validation has 31 + 39 eyes, out of 2,643 training eyes. LightGBM is tuned over up to 400 trees with 31 leaves and min_child_samples = 10 on 192 rows. A GRU with 64 hidden units over 53-dimensional inputs is trained for up to 40 epochs on the same 192 sequences. There is no early stopping, no augmentation, and no use of the 2,000+ unlabelled training eyes for pre-training. No published ML progression model would be trained like this. Dixit 2021 [16] and Wang 2019 [17] used thousands of eyes or other labelling. The results are what one would expect from these settings: seed SD up to 13.2 points in sensitivity (GRU, k = 6), and FPR varying from 21.9% to 33.2% across seeds at k = 3.

*Fix:* Re-implement at least one published ML detector faithfully (e.g. the archetype/AA approach of Wang et al. [17], or Yousefi's GEM [20]). Alternatively, enlarge the label set, e.g. label eyes with ≥ 6 tests using a future-window reference, or use self-supervised pre-training. Report learning curves showing whether the ML results are limited by data. Add a strong but simple ML baseline such as penalised logistic regression on slope features.

### 3. MAJOR — The threshold rule estimates a 95th percentile from about 39 stable validation eyes on the same set used for model selection
*Location:* Methods D8: "threshold set at 95% specificity on validation-set reference-stable eyes."

*Problem:* `self.thr[k] = np.quantile(sv[yv == 0], 0.95)` on 39 stable validation eyes is about the second-largest score. Its sampling variance is huge, and it explains the erratic FPR across k (27.7%, 9.4%, 18.8%, 3.6%) that the paper attributes to ML in general. The same validation set also picks the best of 12 configurations by AUC, which introduces optimistic selection bias into the threshold. The resulting test-stable specificity of 99–100% at k ≥ 4 shows the threshold is not even calibrated to its nominal 95%.

*Fix:* Use nested or cross-fitted thresholds (e.g. 5-fold cross-fitting over train ∪ val), smoothed quantiles, or a conformal threshold with a finite-sample correction. Report the threshold's bootstrap variability. Better still, add an ML detector calibrated against shuffled-order nulls, the obvious fix the paper itself proposes, to show whether ML plus a proper null closes the gap.

### 4. MAJOR — The external D8 result is a foreseeable failure from a known unit mismatch, presented as evidence of label non-transfer
*Location:* Abstract: "Externally, the machine-learning detector had specificity 61% versus 95% for the trend test." Discussion: "in GRAPE, the transferred model lost 33 percentage points of specificity relative to the trend test". Amendment A2: "dB scale differs from Humphrey … D8 is the UWHVF-trained model applied unchanged".

*Problem:* The authors state that the Octopus dB scale differs from the Humphrey scale. They recalibrate D5 and D7 on GRAPE, but they feed D8 raw Octopus dB into level-dependent features. GRAPE median baseline mean sensitivity is 22.8 dB versus 27.9 dB in UWHVF reference eyes. The point grid is also not constant: from the loader, 86 of 263 GRAPE eyes have fewer than 59 analysable points (minimum 10). This changes the PLR-fraction and SD features. The D8 specificity drop is therefore a covariate-shift artefact that the design guarantees. It is not a finding about ML transfer, and citing [23] ("Labeling matters") for it is misleading.

*Fix:* Either recalibrate D8 on GRAPE with the same 5-fold cross-fitting given to D5 and D7, or at least centre and scale the level features. Present the unchanged-transfer result as a negative-control illustration, not as an abstract-level finding. Remove it from the abstract or qualify it there.

### 5. MAJOR — Asymmetric tuning: development effort went to the non-ML methods; the ML methods got a fixed 12-point grid
*Location:* Methods D9: "with the same labels, threshold rule and tuning budget (12 configurations) as D8".

*Problem:* D5, D6 and D10 are the authors' own ideas. Each went through several development rounds (Supplementary Note S1, rounds 0, 1, 3, 5). D8/D9 were added at protocol time without any pilot. "Same budget for D8 and D9" is not the relevant fairness criterion. The relevant one is comparable effort between ML and non-ML methods.

*Fix:* Describe the development effort spent on each detector family. Either give the ML detectors a comparable development phase on train and validation, or state clearly that they are naïve baselines and restrict the claims accordingly.

### 6. MAJOR — Generalising from a strawman to "machine learning … increasingly proposed"
*Location:* Introduction: "most new detectors are judged by how many eyes they flag". Discussion: "The machine-learning results deserve attention because supervised models are increasingly proposed for this task [15–20]". Key Summary Points.

*Problem:* None of refs [15–20] is reproduced or evaluated. [18] and [19] are forecasting models and [20] is unsupervised. The claim that the "usual practice" is thresholding at 95% specificity on stable eyes (protocol RQ4) is not supported by a citation. No evidence is given that published ML detectors share D8's failure mode.

*Fix:* Cite specific papers that used this thresholding practice, or drop "usual practice". Limit the conclusion to "two simple supervised baselines trained on a future-progression label".

### 7. MODERATE — D10's failure at k = 3 is structural but reported as an observation
*Location:* Results: "The self-supervised order network (D10) also flagged no eye with three fields."

*Problem:* D10 uses `pvalue_within` with exact enumeration, so it has the same 1/6 floor as PoPLR. The sentence implies an empirical finding.

*Fix:* Say that D10 shares PoPLR's structural floor. Also note that D10 was trained on windows of 3–8 tests, which mixes k values.

### 8. MODERATE — The feature set deviates from the protocol
*Location:* Protocol D8: "(MD level/slope/z, PLR counts, PoPLR S, worst region slope, range, SD)". The code (`tab_features`) has no worst-region slope; it uses the worst 10% of pointwise slopes and the mean −log p instead of PoPLR S.

*Fix:* Declare this as a deviation, or align the code with the protocol.

### 9. MODERATE — The time-scale borrowing (A1) creates out-of-distribution inputs for D8/D9
*Location:* Methods E2: "each window was given the test dates of a randomly chosen UWHVF test-set eye".

*Problem:* D8 uses `t[-1]-t[0]` and D9 uses Δt as inputs. Artes windows combine weekly noise structure (no long-term fluctuation) with multi-year timestamps. This joint distribution never occurs in training, so neither model was trained on such inputs.

*Fix:* Discuss this. Add a sensitivity analysis using the true Artes timestamps, and another using UW stable eyes' own shuffled series, which is already available as E3.

### 10. MINOR — Leakage audit
I verified that ML thresholds and model selection never touch the test set. The donor timestamps for A1 come from the test split, which is harmless because they carry no labels, but it should be stated. The leakage audit says the reference overlap is "stated as a limitation", but the manuscript does not state it (see Review 01, issue 6).

### 11. MINOR — Reproducibility details
Report LightGBM/PyTorch versions, the chosen configuration per k and seed, and the validation AUCs. Without these, the reader cannot tell whether the selected models are even reasonable discriminators.

## Recommendation

**Major revision.** The ML part is the paper's most visible claim, in the abstract, Key Summary Points and Discussion, and it is its weakest. As implemented, D8/D9 answer a prognostic question with too little training data, a noisy threshold and, in GRAPE, unscaled out-of-distribution inputs. Either the ML baselines must be made credible, or the ML claims must be reduced to what was tested.
