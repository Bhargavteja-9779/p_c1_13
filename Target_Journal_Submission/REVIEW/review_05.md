# Review 05 — Machine-learning reviewer

## Summary
The paper concludes that supervised ML detectors (LightGBM D8, GRU D9), thresholded at 95% specificity on validation reference-stable eyes, have inflated false-alarm rates on true no-change data (RQ4). It also concludes, more broadly, that "apparent early-detection gains of ... machine-learning detectors came with false alarms". I read `detectors.py` and `run_all.py`. The ML baselines are small, trained on very few labels, and thresholded on a tiny, unrepresentative set. Their features also include shortcut variables, which could explain the false alarms without any reference to the "usual threshold rule". The paper draws general conclusions about ML from what amounts to a weak baseline.

**Recommendation: Major revision.**

## Issues

1. **MAJOR — Training and threshold sets are tiny (Methods D8/D9; not reported).**
   - Re-running the reference definition gives 93 progressors and 99 stable training eyes, and 31/39 validation eyes.
   - D8 and D9 are trained on about 190 labelled series. The model is selected by validation AUC over 12 configurations and then thresholded at the 95th percentile of **39** validation stable scores (`np.quantile(sv[yv == 0], 0.95)`), which is roughly the 2nd-highest score.
   - Model selection and thresholding use the same 70 validation eyes (double use).
   - A threshold estimated from 39 values has very large sampling error. That alone could produce 4–28% false-alarm rates elsewhere. D8's seed SD on the true-null arm is 5.1 pp at k = 3.

   *Fix:* report the training and validation label counts. Use cross-validated thresholds or a separate calibration split. Report the variability of the threshold. Consider unlabelled or weakly labelled pre-training on the 2,643 training eyes.

2. **MAJOR — Shortcut features probably drive the false alarms, not the threshold rule (Methods D8: "14 summary features"; Results RQ4).**
   - `tab_features` includes the follow-up span `t[-1] - t[0]` and level features (`md[-1]`, `md.mean()`).
   - In the reference cohort, progressors had shorter spans: the median span of the first 3 tests was 2.08 years vs 2.37 for stable eyes, and at 6 tests 5.9 vs 7.2 years. They also had lower mean sensitivity (25.7 vs 27.8 dB at k = 3).
   - Artes windows receive donor spans from all UWHVF test eyes (median 2.19 years at k = 3, closer to progressors). The Artes mean sensitivity (median 26.9 dB) lies between the two groups.
   - A model that has learnt "tested more often and worse" will flag Artes windows without any trend. The RQ4 interpretation ("this threshold rule gives too many false alarms") is therefore confounded with covariate shift and shortcut learning.

   *Fix:* ablate the span and level features; train on change-only features. Report feature importance or SHAP values. Report the true-null false-alarm rate when Artes donor spans are drawn from reference-stable eyes only.

3. **MAJOR — Tuning budget and architecture are not a fair test of "ML" (Methods D9; Limitations "Seventh").**
   - The GRU takes the raw k × 52 field plus intervals. It has 16–64 hidden units, up to 40 epochs, no early stopping, no augmentation, and is trained on about 190 sequences.
   - D10's self-supervised network trained on all training eyes, but its representation is not used by D8 or D9.
   - "Same 12 configurations" is equal in number but not in effective search. LightGBM's grid covers trees, learning rate and leaves; the GRU's covers size, learning rate and epochs.

   *Fix:* either label D8/D9 as "simple reference ML baselines" and restrict claims to them, or add a stronger, literature-standard model (e.g., a re-implementation of a published VF progression model) with a larger budget. Remove generalisations about "machine-learning detectors" from the Abstract and Conclusions.

4. **MAJOR — "As is common in machine-learning studies" is uncited (Methods D8; Results RQ4 sentence 1).** The claim that 95% specificity on reference-stable eyes is the usual rule has no citation. Refs 17–22 are cited only generally. I cannot verify how each of them set thresholds. *Fix:* cite specific studies and quote their threshold rule, or drop the claim.

5. **MAJOR — D8 is "valid" and the most sensitive detector at k = 6, which contradicts the narrative (Table 1; Table 3; Abstract Conclusion).** At k = 6, D8 has a 3.6% true-null rate and 70.8% sensitivity; it flags 78% of progressors by test 6 vs 69% for D1. With 26 eyes this is not significant, but it is the opposite of "explained by false alarms". *Fix:* state this result in the Abstract and Discussion. Discuss why false alarms are non-monotone in k (27.7%, 9.4%, 18.8%, 3.6%). This pattern itself suggests unstable per-k models and thresholds (separate models per k).

6. **MODERATE — The GRAPE transfer of D8 is not a fair test (Methods E4; Results RQ5; Abstract "33.5 percentage points more false positives").**
   - D8 is applied unchanged to a different perimeter, with a different dB scale (Octopus per the code docstring; I cannot verify this independently), a different point count, and much shorter intervals (GRAPE follow-up spans up to 4.8 years).
   - Level and span features are out of distribution, and a 33.5-pp increase in false positives is the expected outcome of dataset shift.
   - The Abstract presents this as evidence about ML detectors in general.

   *Fix:* present it explicitly as a no-recalibration transfer failure. Add a version recalibrated on GRAPE with the same 5-fold cross-fitting as D5/D7, which is the fair comparison. Remove it from the Abstract or qualify it there.

7. **MODERATE — The model is selected per k, separately (`self.models[k]`).** Each k has its own model and threshold from the same tiny validation set. This explains the erratic k-pattern. *Fix:* train a single model across k with k as a feature, or report the selected configuration per k and per seed.

8. **MODERATE — Leakage check of the label definition.** The reference label uses the full series, including the first k tests that the model sees. That is "partial verification" or incorporation. The model is trained to predict a label that partly depends on its own inputs, which inflates sensitivity on E1 (it does not affect E2). *Fix:* define training and evaluation labels on tests k+1..end only, or at least report results with that definition.

9. **MINOR — Class weighting.** The GRU uses `pos_weight`; LightGBM uses none. *Fix:* harmonise, or justify the difference.

10. **MINOR — D10 is described as "a PoPLR-type permutation statistic [33]".** Ref. 33 is a classification permutation test in observational studies. The citation supports the general idea, not this use. *Fix:* soften "[33]" to "inspired by".
