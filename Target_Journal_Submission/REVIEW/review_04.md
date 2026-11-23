# Review 04 — Machine-learning reviewer

**Recommendation:** Major revision. The ML arm, as built, cannot support any general statement about machine-learning detectors.

## Summary

D8 (LightGBM) and D9 (GRU) are trained on very few labelled eyes, selected on a tiny validation set, and thresholded on the same set. They never see null-like data. On GRAPE, D8 is applied across a perimeter dB-scale shift using absolute-level features. The paper's main ML message is that "a threshold at 95% specificity on labelled stable eyes does not control false alarms". That point is reasonable, but it concerns threshold calibration, not machine learning. The obvious fair comparator, an ML score calibrated against the same shuffle or conformal null as D5, is missing. Several sentences generalise from these two weak models to ML detectors in general.

## Issues

### 1. MAJOR — The training and validation sets are tiny, and this is not reported
**Location:** "D8 machine learning, tabular: gradient-boosted trees on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set stable eyes".
**Evidence:** Applying the reference definition (≥ 8 tests; progressor if the MTD slope is < −0.3 dB/yr with p < 0.01; stable if p > 0.5) to the locked split, as `run_all.py` does, gives **93 progressors and 99 stable eyes for training** and **31 progressors and 39 stable eyes for validation**. The 221 + 75 intermediate eyes are discarded. In `detectors.py`, model selection (best AUC over 12 configurations) **and** the 95% threshold (`np.quantile(sv[yv == 0], 0.95)`) both use the same 70 validation eyes. The threshold is then fixed by the top 2 of 39 stable-eye scores. That is extremely unstable, as the seed SDs of D8 false alarms show (5.1 pp at k = 3), and it is optimistically biased because the same data are used for selection and calibration.
**Fix:** Report n for training, validation and threshold-setting per k. Use separate data for model selection and threshold calibration (nested CV, or a split of the validation set). Report the bootstrap variability of the threshold itself.

### 2. MAJOR — The ML models were set up without the calibration given to the competing statistical detectors
**Location:** "Thresholds chosen on labelled stable eyes are a natural choice for machine-learning detectors of progression [15–17], but our results show that they should also be checked on true no-change data." "The machine-learning result has a simple explanation."
**Problem:** D5 and D6 get a null distribution built from 20 shuffles of every training eye (thousands of null samples, stratified by level). D8 and D9 get 39 stable eyes whose full-series slope is *positive* (see Review 01, Issue 1). These eyes are easy negatives and do not resemble the noise of a short series. The ML models are therefore calibrated against the wrong null, while the statistical detectors are calibrated against the right one. That alone explains the false-alarm excess and makes the ML-vs-statistics contrast unfair. The protocol presents this as "common ML practice" (RQ4), which is a legitimate question, but the paper's broader statements ("Methods that found more worsening, including two machine-learning methods, also gave many more false alarms"; KSP: "a machine-learning model thresholded at 95% specificity reached 27.7%") are read as a verdict on ML.
**Fix:** Add D8-conformal and D9-conformal variants: the same trained score, with the threshold set at the 95th percentile of scores on shuffled training series (exactly as D5), or on a pooled-detrended null. Report them in Table 2. Only then can the authors separate "ML is weak" from "ML was thresholded naively". Restrict claims to "ML detectors thresholded on labelled stable eyes".

### 3. MAJOR — The GRAPE transfer of D8 is confounded by a perimeter dB-scale shift in level features
**Location:** "D8 was transferred unchanged from UWHVF"; Discussion: "Our external results point the same way: the model transferred from UWHVF to GRAPE lost specificity, while a simple test calibrated on the external clinic's own data did not." Abstract: "Externally, gradient-boosted trees had a specificity of 61.2%, compared with 95.3% for the trend test."
**Evidence:** `tab_features` includes absolute levels (`md[-1]`, `md.mean()`, plus `Y.std(0).mean()` and `t[-1]-t[0]`). The protocol (A2) acknowledges that the GRAPE "dB scale differs from Humphrey". A tree model trained on HFA levels and applied to a shifted scale is out of distribution by construction. "Grid-agnostic" is not "scale-agnostic". In addition, the Discussion compares the unrecalibrated D8 with "a simple test calibrated on the external clinic's own data", i.e. D5. D1 was not recalibrated either, but D1 is scale-invariant. So the contrast is between recalibrated or invariant statistics and a non-recalibrated, scale-sensitive model. It does not show that ML transfers poorly in general.
**Fix:** Either (a) recalibrate D8's threshold on GRAPE by the same 5-fold cross-fitting used for D5 and D7 (shuffled GRAPE series, no labels needed), or (b) drop the level features, or standardise them within device, and re-run. Then rewrite the abstract sentence. As it stands, the 61.2% figure should not appear in the abstract without the caveat.

### 4. MAJOR — The PLS and Results say both ML methods "found more worsening", but D9 was less sensitive than D1
**Location:** PLS: "Methods that found more worsening, including two machine-learning methods, also gave many more false alarms."
**Evidence:** D9 sensitivity vs D1 (`metrics.json`): k = 3: 12.3 vs 19.2; k = 4: 11.5 vs 30.8; k = 5: 40.8 vs 42.3; k = 6: 37.7 vs 57.7. D9 never found more worsening. The GRU is in fact the weakest non-trivial detector, with seed SD up to 13.2 pp at k = 6, which suggests under-training rather than an inherent limitation.
**Fix:** Correct the PLS ("one machine-learning method"). Report D9 training diagnostics (learning curves, validation AUC per k) and acknowledge that it is probably under-fitted with about 190 training sequences.

### 5. MODERATE — The tuning budget is "equal" but not adequate, and the search is not described
**Location:** "D9 machine learning, sequence: a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8." Limitations: "our machine-learning detectors had a fixed and modest tuning budget".
**Problem:** Equal configuration counts do not mean equal effort: 12 LightGBM configurations is reasonable, while 12 GRU configurations with no early stopping, no augmentation and 20–40 epochs on about 190 sequences is minimal. There is no input normalisation beyond /35, no use of the 296 unlabelled long eyes or the thousands of short-series training eyes (for example self-supervised pre-training, which D10 shows is feasible), and no class weighting for LightGBM.
**Fix:** List the grids in the Supplement (they are in `detectors.py`). Report the validation AUC of each model per k. Consider a semi-supervised or pre-trained variant, or state clearly that the ML arm represents a "minimal-effort common practice" baseline.

### 6. MODERATE — The feature set deviates from the protocol
**Location:** "14 summary features of the first k tests".
**Evidence:** The protocol lists "MD level/slope/z, PLR counts, PoPLR S, worst region slope, range, SD". The code uses the mean of −log p (a proxy for PoPLR S), the worst-decile pointwise slope (not a regional slope) and includes `k`, which is constant within each per-k model and therefore useless.
**Fix:** List the 14 features in the Supplement and report the deviations from the protocol.

### 7. MODERATE — A leakage-like design issue: the Artes data were used in development, and the test-set eyes supply the donor dates
**Location:** "Sixth, the Artes data were used once during development, to check false alarms of a candidate method".
**Problem:** There is no leakage into the ML models; their fitting uses train and validation only, which I verified in `run_all.py`. However, the true no-change arm was used to select which statistical variant to put in the benchmark (D6; see Review 02, Issue 3), and E2 windows take their time stamps from test-set eyes. The paper should describe the role of every dataset at every stage in one table.
**Fix:** Add a data-use matrix (dataset × stage: development, protocol design, final evaluation).

### 8. MODERATE — The threshold choice is not explored
**Location:** "threshold set at 95% specificity on validation-set stable eyes".
**Problem:** The paper reports a single operating point. A curve of sensitivity vs true no-change false alarms as the threshold varies (for D8, D9 and the conformal p-value detectors) would show whether D8 dominates D1 at matched false alarms. That is the actual question for ML. At k = 6, D8 has 70.8% sensitivity with 3.6% false alarms vs D1's 57.7% and 5.1%, a hint that a properly calibrated D8 might be better.
**Fix:** Add operating curves, or report sensitivity at a false-alarm rate matched to D1 on the Artes data. The latter is a post hoc analysis, so label it as such.

### 9. MINOR — Seed handling for ML
**Location:** "Results varied across seeds: the seed standard deviation of D8 sensitivity was 5.0 percentage points at three tests."
**Fix:** Report the seed SD of D8 and D9 at every k in the main text or Table 2 (it reaches 8.9 pp at k = 5 and 13.2 pp at k = 6 for D9). Note that the paired tests use a 5-seed majority ensemble, which is a different model from what is described.

### 10. MINOR — D10 is described as an "ML" detector, but it is a permutation test with a learned statistic
**Location:** "D10 self-supervised order network".
**Fix:** Group D10 with the permutation methods in the Results and figures (it is valid by construction), so that "ML" in the paper's message refers only to D8 and D9.
