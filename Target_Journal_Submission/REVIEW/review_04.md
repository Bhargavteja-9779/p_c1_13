# Review 04: Machine-learning methods reviewer

## Summary
The paper's ML claims (RQ4: "thresholding at 95% specificity, as is common practice, gives too many false alarms") rest on two baselines, LightGBM (D8) and a GRU (D9). I read `detectors.py` and recomputed the label counts. Neither baseline gives a fair test of "ML" or of "common practice":

- They are trained on very few labelled eyes.
- Model selection and threshold setting use the same small validation set.
- D8 is transferred across perimeters using absolute-level features.

The negative findings about ML are therefore findings about these particular implementations.

## Recommendation
**Major revision.**

## Issues

1. **MAJOR – Tiny labelled training and threshold sets.**
   - *Location:* Detectors D8/D9 ("trained to predict the reference label; threshold set at 95% specificity on validation-set stable eyes").
   - *Problem:* Labels exist only for eyes with ≥8 tests and a determinate reference. Using the code's `reference()`, I find 192 labelled training eyes (93 progressors / 99 stable) and 70 validation eyes (31 / 39). The 95th percentile of scores in 39 stable eyes lies between the two highest scores. This threshold is extremely noisy, which explains the erratic false-alarm pattern of D8 (27.7 → 9.4 → 18.8 → 3.6% at k = 3–6) and the seed SD of D9 sensitivity of up to 13.2 pp. Most of the 2,643 training eyes are unused.
   - *Fix:*
     - Report the n of labelled train and validation eyes per k.
     - Use cross-validated out-of-fold scores to set the threshold, or use the shuffle/no-change null to calibrate the threshold.
     - Consider semi-supervised use of unlabelled eyes, or a forward-looking label with a shorter horizon to enlarge the training set.

2. **MAJOR – Model selection and threshold use the same data.**
   - *Location:* `MLTabular.fit` (`a = roc_auc_score(yv, …)` then `thr = quantile(sv[yv == 0], .95)`); likewise `MLSequence.fit`.
   - *Problem:* The configuration with the best validation AUC is chosen, and its threshold is then set on the same validation scores. Both steps are optimistically biased on 70 eyes.
   - *Fix:* Use a three-way split or nested CV: tune on inner folds, set the threshold on held-out folds.

3. **MAJOR – The "common practice" claim is a straw man.**
   - *Location:* Methods D8 ("as is common in machine-learning studies"); Discussion ("This matters for machine-learning studies, which usually set the threshold at a fixed specificity in reference-stable eyes [15, 16, 23]").
   - *Problem:* The cited studies used different labels (Saeedi [15]: consensus of 6 algorithms; Dixit [16]: VFI/MD/PLR labels) and far larger training sets. Whether they set thresholds on reference-stable eyes is not verified in the paper. The present models are small re-implementations, not the published models.
   - *Fix:* Either evaluate a published model or weights, or limit the claim to "in our re-implementation". Quote the threshold procedure of each cited study, or remove the attribution.

4. **MAJOR – The D8 transfer to GRAPE is invalid by design.**
   - *Location:* E4 ("D8 was transferred unchanged from UWHVF"); Results External clinic; Abstract ("Externally, higher sensitivity again came with more false positives").
   - *Problem:* `tab_features` includes absolute levels (`md[-1]`, `md.mean()`), ranges and spreads in dB. GRAPE was measured on a different perimeter with a different dB scale (A2). The model's 61.2% specificity at k = 3 reflects covariate shift, not a property of ML detectors. Calling the features "grid-agnostic" is true for dimensionality, but not for scale.
   - *Fix:* Re-fit D8 on GRAPE by cross-fitting, as was done for D5 and D7, or restrict it to scale-invariant features (z-scores, p-value summaries). Otherwise remove D8 from the GRAPE conclusions.

5. **MODERATE – The features differ from the protocol.**
   - *Location:* Protocol D8 ("MD level/slope/z, PLR counts, PoPLR S, worst region slope, range, SD") vs `tab_features`.
   - *Problem:* The code uses the mean −log p (not the PoPLR S statistic or its permutation p) and the mean of the worst decile of pointwise slopes (not a regional slope). It also includes k (constant within a model) and the time span t[-1] − t[0]. On Artes, the time span is a donor-assigned quantity (A1), so the model sees a feature whose distribution is set by the donor draw.
   - *Fix:* List all 14 features in a supplementary table and record the protocol deviation.

6. **MODERATE – D9 is under-specified and possibly under-trained.**
   - *Location:* D9; `MLSequence`.
   - *Problem:*
     - 20 or 40 fixed epochs, no early stopping, inputs scaled by /35;
     - positive-class weighting on a nearly balanced set;
     - a GRU on 52 × k inputs trained on 192 sequences.

     High seed variance (Table S1) shows the model is unstable. It is not a credible "sequence model" baseline.
   - *Fix:* Report learning curves and validation AUC per k. Consider a simpler pooled model with spatial pre-processing, or pretraining on all unlabelled UWHVF series.

7. **MODERATE – Calibration and score distributions are not reported.**
   - *Location:* Results RQ4.
   - *Problem:* The reader cannot tell whether false alarms arise from a shift between UW validation eyes and Artes windows, for example in severity: Artes median mean sensitivity 26.9 dB vs 28.1 dB in UW reference eyes (my computation).
   - *Fix:* Show score histograms for validation-stable, test-stable, Artes and shuffled series, with the threshold marked.

8. **MODERATE – Leakage audit: the threshold "95% specificity" is not 95% on the test set.**
   - *Location:* RQ4 ("specificity in test-set stable eyes was at least 91.5%").
   - *Problem:* This is correct, but those stable eyes are improving eyes (full-series slope > 0, see Review 06), so specificity is near 100% by construction.
   - *Fix:* Add the incorporation and selection issue to the leakage audit and to the Limitations.

9. **MINOR – D10 description.**
   - *Location:* D10 [29].
   - *Problem:* The order network is trained on train eyes including progressors. Under the null its statistic is exchangeable only if within-eye permutation is used, which it is (`pvalue_within`). Good. However, the reference [29] (classification permutation test) is about covariate balance; the conceptual link should be explained in one sentence.
   - *Fix:* Add that sentence.
