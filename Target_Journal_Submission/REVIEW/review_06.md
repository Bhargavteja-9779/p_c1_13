# Review 06: Reference-standard and circularity skeptic

## Summary
The paper's main argument is that "specificity against a conventional reference did not reveal" false alarms that a true no-change arm did reveal. That argument depends on how the reference was built. In UWHVF and GRAPE, the reference labels are derived from the same data the detectors see (incorporation bias), from the same quantity (mean deviation) that D1 and D2 use, and, for "stable" eyes, from a selection that guarantees near-perfect specificity. The Discussion gives a speculative mechanism that my own check on the data contradicts.

## Recommendation
**Major revision**, bordering on reject unless E1 and E4 are re-designed.

## Issues

1. **FATAL – The "stable" reference eyes are selected on a positive slope over the very tests being evaluated.**
   - *Location:* Methods, Reference standard; Results ("specificity against the future reference hardly separated valid from invalid detectors"); Discussion paragraph 2.
   - *Problem:* Stable means full-series one-sided p > 0.5, i.e. slope > 0. The full series includes tests 1–k. Eyes whose early tests drift downward by chance are less likely to be labelled stable. Specificity of 92–100% for every detector is therefore largely built in. The paper's key contrast ("specificity looked fine, true no-change did not") is partly a design artefact, not an empirical discovery about reference-based evaluation in general.
   - *Fix:*
     - Define the reference from tests k+1…end only (a genuinely future reference), or from tests ≥ k + 2.
     - Define stable eyes by an equivalence criterion (|slope| < 0.2 dB/yr with a CI), not by the sign of the slope.
     - Repeat E1 and show whether the specificity–validity gap persists.

2. **MAJOR – The mechanism offered in the Discussion is contradicted by the data.**
   - *Location:* Discussion paragraph 2 ("Such eyes are likely to have low test–retest variability … True no-change data from patients with typical glaucoma and typical variability are a harder test").
   - *Problem:* I computed the median residual SD of mean sensitivity about the full-series linear trend in the 26 UW reference-stable eyes: about 1.03 dB (this includes any non-linearity and long-term fluctuation). For the Artes patients, the median SD of mean sensitivity over 12 weeks is about 0.48 dB. Artes is the *low*-variability set, not the harder one. The likelier explanations are:
     - selection on a positive slope (issue 1);
     - detector-specific features of the Artes windows: the donor time labels, severity, and the fact that D6's detrending fails with 1 residual df whatever the variability.
   - *Fix:* Remove the speculation, or test it by reporting the variability of the reference-stable eyes, the Artes eyes and the UW test eyes side by side.

3. **MAJOR – The reference and the comparator use the same quantity, so the reference favours D1.**
   - *Location:* Limitations ("the PoPLR-based secondary reference gave the same conclusions").
   - *Problem:* The primary reference is an MTD trend with p < 0.01 over the full series, and D1 is a mean-sensitivity trend with p < 0.05 over the first k tests. Because the full series contains the first k tests, D1 is partly predicting its own input. The Limitations mention "favours mean-deviation detectors" but never mention the overlap of tests (incorporation). The leakage audit says this overlap is "stated as a limitation", but it is not stated in the manuscript.
   - *Fix:* Add the incorporation bias to the Limitations, and run a future-only reference sensitivity analysis.

4. **MAJOR – The secondary reference does not "give the same ordering".**
   - *Location:* Results ("The secondary reference … gave the same ordering (Supplementary Table S1)").
   - *Problem:* Under the PoPLR reference at 6 tests, D1 (37.9%) ranks below D6 (43.1%), D10 (43.1%), D8 (42.1%) and D7 (39.7%). At 3 tests, D2 (24.1%) and D8 (24.1%) exceed D1 (10.3%). No specificity (17 stable eyes) and no paired tests are reported for this reference. The claim is not supported.
   - *Fix:* Report sensitivity, specificity and paired tests for the PoPLR reference, and rewrite the sentence to describe the actual pattern: D1's advantage is reference-dependent.

5. **MAJOR – The GRAPE "clinician labels" are computed from the same short series.**
   - *Location:* Data sources, GRAPE; E4; Table 2; Abstract ("Externally …").
   - *Problem:* The GRAPE labels come from three criteria (MD, PLR2, PLR3) applied to each eye's whole follow-up. By my count, 100/263 GRAPE eyes have exactly 3 visits and 75 have exactly 4, and 9/27 MD-progressors have only 3 visits. At k = 3 and k = 4, the detector therefore often sees the *entire* series from which the label was computed. E4 measures agreement between two rules applied to the same data, not early detection. D1 and D2 (MD trend) are naturally closest to an MD-trend label.
   - *Fix:*
     - Restrict E4 to eyes with ≥ k + 2 visits, so the label uses data the detector did not see.
     - Describe the labels as criterion-based, not "clinician-labelled".
     - Report results for PLR2/PLR3 labels as well (protocol secondary).

6. **MODERATE – Partial verification and spectrum.**
   - *Location:* Results, Study sample (80 of 132 eyes excluded as indeterminate).
   - *Problem:* Sensitivity and specificity are computed on the extremes only. Detectors that do well on borderline eyes are not credited, and detectors that over-flag borderline eyes are not penalised.
   - *Fix:* Report flag rates among the 80 indeterminate eyes and a three-category analysis.

7. **MODERATE – The reference threshold is not justified.**
   - *Location:* Reference standard.
   - *Problem:* The rule "−0.3 dB/yr with p < 0.01" is not referenced, and no sensitivity analysis is given (e.g. −0.5 dB/yr, or p < 0.05).
   - *Fix:* Cite a source or add a sensitivity analysis.
