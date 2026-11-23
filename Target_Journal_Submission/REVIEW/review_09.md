# Review 09: Sceptic of the main claim

**Claim under review:** "A plain trend test of mean sensitivity remained as good as any valid alternative" (Abstract Conclusion). Also Conclusions: "In three independent data sources, a plain trend test … was as good as any detector that kept false alarms at the nominal level".

## Summary

The data show something narrower: with 26 progressors, no detector that passed a post-hoc validity rule beat D1 by enough to clear Holm-corrected exact McNemar tests. They do not show equivalence. The design could only detect gains of about 35 percentage points. The reference standard is built from the same statistic as D1. "Validity" rests on 30 early-glaucoma eyes. The one non-significant gain larger than the pre-set 10-pp margin (D8 at six tests) is left out of the Abstract. The negative result is useful. The wording turns absence of evidence into evidence of absence.

## Issues

**1. FATAL — H2 could essentially not be falsified with n = 26, so "supports our main hypothesis" and "as good as" are unjustified.**
- Locations:
  - Discussion: "This result supports our main hypothesis."
  - Abstract: "remained as good as any valid alternative".
  - Results: "The hypothesis … was therefore not rejected".
- Evidence:
  - H2 is falsified only by a gain of at least 10 pp *and* Holm-adjusted exact McNemar p < 0.05.
  - With 26 pairs and 9 comparisons, the most significant comparison needs p < 0.0056. Discordance of 8:0 gives p = 0.0078 and fails; 9:0 gives p = 0.0039; 11:1 gives p = 0.0063 and fails; 12:1 gives p = 0.0034.
  - So the smallest possible falsifying gain is 9/26 = **34.6 pp**. Any clinically plausible gain of 10–25 pp could never have falsified H2. Only the 10:0 result for D6 (+38.5 pp) passed.
  - The upper confidence limits for valid detectors' gains include large benefits: D2 k = 3 up to +42.3 pp; D8 k = 6 up to +30.8; D7 k = 5 up to +26.9; D10 k = 5 up to +23.1 (Table S2).
- Fix:
  - Replace "as good as" and "supports" with "we found no evidence that any valid detector was more sensitive. The study could exclude only gains above about 35 percentage points."
  - Report the minimum detectable difference.
  - If equivalence is the claim, pre-specify a non-inferiority or equivalence margin and test it. That would need a much larger reference set, for example all UWHVF test eyes with a later-test reference.

**2. MAJOR — The reference standard is circular in D1's favour, and the secondary reference does not remove the problem.**
- Locations:
  - Methods: "An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01."
  - Limitations: "Against a secondary reference based on PoPLR, the pattern was the same".
- Evidence:
  - The reference is a one-sided OLS t-test on the mean-TD slope over the full series, which includes tests 1…k. D1 is a one-sided OLS t-test on the mean-sensitivity slope over tests 1…k: the same statistic, computed on part of the same data. D5 uses the same statistic again.
  - Any detector that measures a different construct (localised loss: D3, D4, D7, D10) is penalised by design.
  - The secondary reference is not independent of the primary. All 26 primary progressors are among its 58 progressors (my cross-tabulation of `raw_results.csv`).
  - Under the secondary reference the pattern is **not** the same at later k (Table S1, "Sens, PoPLR ref"):
    - k = 5: valid D7 has 31.0% against D1's 27.6%.
    - k = 6: valid D10 has 43.1% and valid D8 has 42.1%, against D1's 37.9%.
  - No paired tests or specificities were run for the secondary reference.
- Fix:
  - Run the paired analysis and specificity against the secondary reference.
  - Add a reference built only from tests after k.
  - Delete "the pattern was the same", or limit it to k = 3.

**3. MAJOR — D1's "validity" depends on a lenient post-hoc rule and on early-glaucoma retest data.**
- Locations: "It was valid at every number of tests"; Conclusions: "kept false alarms at the nominal level".
- Evidence:
  - D1's false-alarm CIs are 2.8–6.3%, 1.9–6.2%, 2.2–7.5% and 2.5–8.1%. Under the protocol's wording ("FPR CI upper bound vs 5%"), D1 is not shown to be at the nominal level at any k. It counts as valid only under the post-hoc 10% ceiling (Review 07, item 2).
  - Over four sequential reviews (k = 3–6), D1 flags about 12.6% of Artes windows at least once (my computation from `raw_results.csv`).
  - Artes eyes have median mean sensitivity 26.9 dB, which is early disease. In more damaged eyes, residual variance and D1's false alarms are unknown.
- Fix: replace "kept false alarms at the nominal level" with "had false-alarm rates of 3.8–5.1% per review in early glaucoma (upper 95% limits up to 8.1%)". Report the cumulative rate.

**4. MAJOR — The machine-learning conclusion follows from how the labels and threshold were built, not from "common practice".**
- Locations: "D8 and D9 were thresholded at 95% specificity on validation-set stable eyes, as is common practice"; Discussion: "The machine-learning result has a simple explanation."
- Evidence:
  - The "stable" eyes used for training and thresholding all have a **positive** long-term slope, because one-sided p > 0.5 means b > 0 (`deferral.ols`).
  - The threshold is the 95th percentile of scores from only **39** validation stable eyes (my count), which is roughly the second-highest score. A threshold calibrated on improving eyes will be anti-conservative on flat true-null series.
  - Training used 93 progressors and 99 improving eyes, with 12 configurations and no calibration step.
  - This is a weak version of ML practice. It cannot support the general Discussion statement that ML thresholds "should also be checked on true no-change data" as an empirical finding about ML.
  - When D8 *was* valid (k = 6), it had the highest sensitivity of any detector: 70.8% against 57.7%, +11.5 pp, which is above the pre-set 10-pp margin (p = 1.00 after Holm, n = 26).
  - The Abstract omits this and reports only D8's invalid cells.
- Fix:
  - Add D8 k = 6 to the Abstract.
  - Describe the threshold sample size and the "improving eyes" definition.
  - Add an ML variant thresholded on shuffled or true-null-like training data, or on a flat-slope stable group. Without that, limit the ML claim to "ML thresholded on a small, extreme stable group".

**5. MAJOR — The external result is confounded by perimeter scale and does not support "three independent data sources".**
- Locations: Conclusions: "In three independent data sources, a plain trend test …"; Discussion: "the model transferred from UWHVF to GRAPE lost specificity, while a simple test calibrated on the external clinic's own data did not".
- Evidence:
  - Only UWHVF has a sensitivity comparison with validity. Artes has no progressors. GRAPE has no true-null arm, so validity cannot be judged there.
  - D8's features include absolute dB levels (`md[-1]`, `md.mean()`). Amendment A2 itself says the GRAPE "dB scale differs from Humphrey". Feeding a different dB scale into a model trained on Humphrey levels is expected to shift scores; it is not evidence about the thresholding practice.
  - In GRAPE, D2 had a higher point sensitivity than D1 (59.3% against 44.4%, p = 0.78 after Holm) at lower specificity. Labels are an MD criterion on the full 3–5-visit series, which favours D1.
- Fix:
  - Remove "three independent data sources". Say instead "in one development data set with a true-null arm, with supportive concordance in one external data set".
  - Present the D8 GRAPE result as a transfer failure with a known scale mismatch.

**6. MAJOR — The Conclusions contain untested claims.**
- Location: Conclusions: "Faster confirmation of progression will more likely come from better-timed testing than from more aggressive analysis."
- Evidence: test timing was not studied. The only scheduling analysis (S1, round 2) was an abandoned pilot of test *deferral*, and it was negative.
- Location: Conclusions: "Detectors that appeared to find progression earlier did so largely by raising false alarms."
- Evidence: this is true for D6 at k = 3 and for D8 at k = 3–5. It is not shown for D2 (k = 3, +19.2 pp, false alarms 2.6%), D7 (k = 5, +7.7 pp, 1.2%) or D8 (k = 6, +11.5 pp, 3.6%). Those detectors had higher point sensitivity with low false alarms.
- Fix: delete the timing sentence or mark it as speculation, and change "largely" to "in two of the detectors".

**7. MAJOR — The Plain Language Summary misstates the results.**
- Location: PLS: "Methods that found more worsening, including two machine-learning methods, also gave many more false alarms."
- Evidence: D9 (GRU) never found more worsening than D1: 12.3% against 19.2% at k = 3, and 37.7% against 57.7% at k = 6.
- Location: PLS: "This check gave a fair estimate of the false-alarm rate."
- Evidence: the pre-specified accuracy target was not met (ρ = 0.65 < 0.70), and errors reached 10.4 pp.
- Fix: change the first to "including one machine-learning method", and the second to "gave a rough estimate".

**8. MODERATE — D6 is a straw man that makes the headline contrast close to automatic.**
- Evidence: D6 was known from development to be anti-conservative at k = 3 on the same Artes data (S1, round 5). Its significant sensitivity gain occurs only at k = 3. At k = 4–6 it was valid or near-valid, and it was *less* sensitive than D1.
- The headline "the only detector significantly more sensitive … had a false-alarm rate of 22.4%" therefore describes a known-defective construction, not a real competitor class.
- Fix: say this in the Abstract or Discussion. Present D6 as a demonstration of how detrended pooled calibration fails with one residual degree of freedom.

**9. MODERATE — "Early" detection here means years, and lead time was not measured.**
- Location: Title, "How Early Can … Be Detected".
- Evidence:
  - In UWHVF, k = 3 is a median 2.3 years and k = 6 a median 6.3 years after the first test.
  - The protocol's "number of tests to first detection" was computed (`mean_first_k_detected`: D1 4.39, D7 4.73, D8 4.20) but not reported.
  - No time-to-detection comparison with D1 among shared detections is given.
- Fix: report time to first detection with paired comparisons, or retitle the paper around false-alarm validity.

**10. MODERATE — The shuffle-audit recommendation outruns the evidence.**
- Locations: Abstract: "New detectors should report false alarms on true no-change data, or at least a shuffle audit". KSP: "Clinics and developers can check false alarms with a shuffle audit".
- Evidence:
  - H3 failed.
  - The largest error, 10.4 pp, was an underestimate for an invalid detector (D8, k = 3).
  - The audit missed D6 at k = 6 and D9 at k = 3, and wrongly implicated D2 at k = 3 and D7 at k = 6.
  - The audit includes identity orders and true progressors (Review 06, item 4).
- Fix: present the audit as a "screening check with errors of up to 10 pp in both directions" in the Abstract and KSP.

**11. MINOR — Some validity verdicts are knife-edge.**
- Evidence: D9 at k = 6 is "not valid" because its upper CI is 10.0002%. D6 at k = 4 is "valid" at 5.1% (3.4–7.2%), while D6 at k = 6 is invalid at 7.6% (4.5–11.1%). These borderline categorisations feed the narrative.
- Fix: label borderline cells as indeterminate.
