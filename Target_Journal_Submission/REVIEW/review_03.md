# Review 03 — Perimetry / visual-field methods expert (PoPLR, GPA, noise)

## Summary
The benchmark re-implements classical trend, pointwise, permutation and event methods and compares them against pooled-null and ML detectors. Using a weekly retest set as a true null is sound in principle; it follows Artes et al. (2014). Several perimetric implementation choices, however, make some detectors either straw men or not comparable with their clinical namesakes. The time-relabelling of the Artes data (amendment A1) has consequences that are not discussed. I checked the code in `code/src/models/detectors.py` and `code/src/models/conformal_vf.py`.

**Recommendation: Major revision.**

## Issues

1. **MAJOR — The "GPA-like" event analysis (D7) is not GPA (Methods, Detectors, D7; Discussion "Sixth").**
   - The code uses raw sensitivities. GPA uses pattern deviation, which removes diffuse loss such as cataract.
   - The change limits come from consecutive clinic test pairs with an interval ≤ 0.5 years (`EventAnalysis.fit`). These pairs are binned by the sensitivity of the *first* test of the pair. The limits are then applied to the change from the *mean of two* baseline tests.
   - That mismatch has two effects. The variance of single-minus-single is larger than single-minus-mean-of-two, which makes D7 conservative. Binning on one noisy test induces regression to the mean.
   - In routine care, short-interval repeats are often ordered because a field looked unreliable or worse. That inflates the limits further.
   - The result is D7's very low true-null rates (0–1.9%) and its large shuffle over-estimate (11.7% at k = 6).

   *Fix:* derive limits from (test − mean of two baselines) in short-interval triplets, or from the Artes retest data with leave-one-patient-out. Use pattern deviation, or explicitly call the method "sensitivity-based event analysis". Report how many pairs each 2-dB bin had and which bins were interpolated (bins with < 200 pairs are silently interpolated).

2. **MAJOR — PoPLR (D4) at 3 tests is included as a competitor although it cannot flag (Methods, "Stochastic detectors..." paragraph; Results RQ1 "7 of 10 detectors were valid").** With k = 3 there are 6 orderings, so the minimum p is 1/6. The same holds for D10, and D7 needs k ≥ 4. Counting D4, D7 and D10 as "valid" at k = 3 (0% false alarms and 0% sensitivity) inflates "7 of 10 valid" and adds three structurally null comparisons to the Holm family. *Fix:* mark these cells "not applicable" in Table 1, exclude them from the validity count and the Holm family at k = 3, and say so.

3. **MAJOR — D4 is labelled stochastic but is deterministic (Methods "Stochastic detectors (D4–D6, D8–D10)..."; `pvalue_within` enumerates all permutations for k ≤ 7).** Its "seed" variation (e.g., true-null SD 0.2 pp) comes entirely from the Artes time-label draws (`rng = default_rng(1000 + seed)`), which differ across seeds. D1–D3 and D7 use only seed 0's draws. Detectors are therefore not evaluated on identical Artes time-labelled windows: stochastic detectors average over 5 × 10 draws and deterministic ones use 10. *Fix:* fix the time-label draws once and share them across all detectors, so that the comparison is paired. Describe D4 as exact.

4. **MAJOR — Amendment A1 (borrowed clinic dates for weekly retests) changes the noise model (Methods E2; Limitations "Second").** Assigning UWHVF test dates to weekly tests keeps the null for rank-based statistics. For rate rules it does something else. The retest noise of one week is spread over about 2 years, which makes D2 and D3 slopes tiny and their false-alarm rates low (D2: 0.6–2.6%). The long-term fluctuation in a real clinic is not represented: media changes, learning, inter-visit variability that is larger than intra-week variability. The shuffle audit suggests it matters: D2 11.7% vs 2.6%, D7 11.7% vs 1.9%. The Limitations mention this only briefly. *Fix:* quantify long-term vs short-term variability. One way is to compare residual SD around the trend in UWHVF reference-stable eyes with the Artes within-patient SD. Report a sensitivity analysis in which Artes residuals are inflated to clinic-level variance. Interpret the "valid" verdict for rate and event rules as conditional on this.

5. **MODERATE — Practice and fatigue effects in the Artes series (Methods, Artes).** Weekly testing over 12 weeks in a research setting can produce learning effects in early tests, usually improvement. Windows that start at week 1 carry this effect. Improvement would *lower* false alarms for decline detectors. *Fix:* report false alarms by window start position. Repeat the analysis excluding tests 1–2.

6. **MODERATE — Reliability indices unused.** The Artes loader reads false-positive, false-negative and fixation-loss rates (`artes_retest.py`) but never uses them. UWHVF has none. *Fix:* report Artes reliability. Run a sensitivity analysis that excludes unreliable Artes tests.

7. **MODERATE — The "MD" definitions are inconsistent (Methods "Reference Standard" and D1/D2).** The reference uses the unweighted mean of 52 TD values (`md_series`). D1/D2 use mean raw sensitivity. Neither is HFA MD, which is weighted by location variance. *Fix:* rename the measures, and state the difference between TD and sensitivity slopes (the age-related component).

8. **MODERATE — D3 PLR-3 criterion.** The code uses a one-sided p < 0.01 and slope ≤ −1 dB/yr at ≥ 3 locations, with no spatial or confirmation requirement. Published PLR criteria usually require confirmation in subsequent series or clustering. The protocol says "one-sided", but the Methods text omits this. *Fix:* state "one-sided" in the Methods. Cite the specific PLR criterion being emulated, or acknowledge that this is an ad hoc variant.

9. **MODERATE — GRAPE perimeter and dB scale (Methods E4; Amendment A2).** The code docstring says Octopus G1 (59 points). Octopus dB are not on the HFA dB scale. D1 (t-statistic) is scale-invariant. D2 (−1 dB/yr) and the D8 level features are not. I could not verify the GRAPE perimeter details from the manuscript. *Fix:* name the perimeter and program. Justify keeping the −1 dB/yr threshold for D2 on Octopus data, or convert units.

10. **MINOR — Blind-spot handling in GRAPE.** Points coded −1 in any visit of an eye are dropped per eye (`valid = (V >= 0).all(0)`), so the number of points could vary between eyes. *Fix:* report the distribution of point counts and confirm that it is always 59.

11. **MINOR — PoPLR secondary reference (Methods, Reference Standard).** Calling a PoPLR reference "not tied to mean deviation" is fair. It is, however, tied to D4 and D10, which are PoPLR-type statistics. *Fix:* acknowledge the reverse circularity.
