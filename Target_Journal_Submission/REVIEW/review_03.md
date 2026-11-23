# Review 03 — Perimetry / visual-field methods

**Recommendation:** Major revision.

## Summary

The idea of using the Artes weekly retest series as a true no-change arm is sound. Re-timing the windows with routine-care dates (amendment A1) is clever but conceptually fragile. The perimetric implementations have several problems: D7 is not GPA-like, the "MD" label is applied to mean sensitivity, the cross-perimeter GRAPE analysis is under-described, and the retest data contain a series that is not 12 weeks long. Most importantly, a weekly retest null captures only short-term fluctuation, whereas the clinical null over years also contains long-term fluctuation. The false-alarm rates are therefore probably lower bounds, and the bias differs between detector families.

## Issues

### 1. MAJOR — The weekly-retest null with re-assigned dates captures short-term, not long-term, variability
**Location:** "Because rate-based rules depend on the time scale, each window was given the test dates of a randomly chosen UWHVF test-set eye (ten draws per window; amendment A1)." "Glaucoma does not change in 12 weeks in a measurable way, so any "progression" flag in these series is a false alarm."
**Problem:** Variability between visits years apart includes long-term fluctuation from media changes, pupil size, learning and fatigue, and changes in reliability. Weekly retests do not contain these components. Mapping weekly fields onto 2–7-year time stamps makes the rate-based rules (D2, D3) and the ML models see an unrealistically quiet null. This is the most likely explanation for the large gaps between true no-change and shuffle-audit false alarms for D2 at k = 3 (2.6% vs 11.7%) and D7 at k = 6 (1.9% vs 11.7%). The authors instead attribute these to "routine-care eyes are noisier", which is the same phenomenon under another name. The bias is not uniform across detectors, so the validity classification is affected. In particular, D1 is "valid" partly because its null is quiet.
**Fix:** Discuss long-term fluctuation explicitly. Add a sensitivity analysis that inflates Artes residual variance to match the UWHVF short-interval (≤ 0.5 yr) test–retest variance at matched sensitivity, or that uses UWHVF eyes with near-zero full-series slope and ≥ 10 tests as a second, long-term quasi-null. Rename the arm "short-term no-change".

### 2. MAJOR — One Artes series spans 524 days, contradicting "12 visual fields in 12 consecutive weeks"
**Location:** "Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [9]." Table 1: "Follow-up, years ... 0.23 (0.21–0.25)".
**Evidence:** `descriptives.json` gives Artes `span_days` mean 100.4 and SD 80.7 against a median of 84 (IQR 77–93), which implies an outlier. From the `vfpwgRetest24d2` data used by the loader, the spans range from 63 to 105 days for 29 patients and are **524 days** for one patient. "Glaucoma does not change ... in 12 weeks" does not hold for that series.
**Fix:** Report the range, explain the outlier (data error, or an interrupted series), and either exclude it or show results without it. Correct the sentence about "12 consecutive weeks".

### 3. MAJOR — D7 is not "similar in spirit to Guided Progression Analysis"
**Location:** "D7 event analysis: a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to Guided Progression Analysis [11]."
**Problems** (from `detectors.py::EventAnalysis`):
- (a) GPA works on **pattern deviation**, to remove diffuse loss. D7 uses raw sensitivity, so cataract-type diffuse loss triggers events.
- (b) The GPA limits come from short-term (weeks) test–retest data in stable patients. D7 uses pairs of routine-care tests up to 0.5 years apart. These contain real change and long-term fluctuation, so the limits are too wide.
- (c) The limits are derived from **single-test minus single-test** differences, Var = 2σ², but are applied to **single test minus mean of two baseline tests**, Var = 1.5σ². The 5th-percentile limit is therefore conservative, at roughly the 2nd–3rd percentile of the actual statistic.
- (d) The bins are indexed by the sensitivity of a single test, not by the baseline mean.

Points (b) and (c) explain D7's low true no-change false-alarm rate (1.1–1.9%) and probably part of its high shuffle-audit rate. The comparison of D7 with D1 is therefore not a comparison with GPA, and the discussion of event vs trend methods [10, 11] over-reaches.
**Fix:** Either implement a closer GPA analogue (PD-based, limits from the Artes-like short-term data or published GPA limits, with "possible" and "likely" progression), or rename D7 "a simple pointwise event rule" and remove the GPA analogy. Correct the variance mismatch: either derive limits from (test − mean of two tests) differences or scale them by √(1.5/2).

### 4. MAJOR — GRAPE perimeter, dB scale and grid are not described adequately for a cross-device analysis
**Location:** "Fields were measured with a different perimeter and test grid (59 analysable locations per field, median)". Amendment A2 (protocol): "dB scale differs from Humphrey".
**Problem:** The manuscript never names the GRAPE perimeter or pattern. The code comment in `detectors.py` says "Octopus G1 (59 points)". Octopus and Humphrey dB scales are referenced to different maximum stimulus luminances, so absolute sensitivities differ by several dB at the same retinal threshold. The G pattern also extends beyond 24°. This matters because:
- (a) D2 and D3 apply Humphrey-derived −1 dB/yr rules unchanged.
- (b) D8 uses absolute level features (`md[-1]`, `md.mean()` in `tab_features`) learned on HFA data, so its GRAPE specificity collapse may be a scale artefact (see Review 04).
- (c) Pointwise exclusion of "points coded −1 in any visit" (`grape.py`) removes different locations in different eyes. The point count ranges down to well below 59 (`n_points` mean 54.7, SD 9.3), so D3's "≥ 3 locations" means something different from eye to eye.

**Fix:** Name the device, strategy and pattern. State the dB offset and whether any conversion was applied. Report the distribution of analysable points. Run D8 with level features removed or standardised within device, and D2/D3 with thresholds re-scaled.

### 5. MODERATE — "MD" labels are applied to mean sensitivity
**Location:** Table 2/3 rows "D1 Trend, MD" and "D2 MD rate"; Abstract and Methods correctly say "mean sensitivity".
**Problem:** D1 and D2 use the unweighted mean of raw sensitivities (`Y.mean(1)`), which is not age-corrected and is not MD (MD is a variance-weighted mean of total deviation). The reference uses unweighted mean TD. Over 6–7 years the normal age decline (≈ −0.07 to −0.1 dB/yr) adds a small negative trend to D1 and D2 but not to the reference. Labelling the rows "MD" misleads readers who will compare with HFA MD-based slopes.
**Fix:** Relabel the rows "Trend, mean sensitivity (MS)" and "MS rate". Optionally add a TD-based D1 as a sensitivity analysis.

### 6. MODERATE — The PoPLR implementation details and the secondary reference need clarification
**Location:** "D4 PoPLR: permutation of pointwise linear regression [7], using all possible orders of the k tests." "a secondary reference based on PoPLR over the whole series (2,000 permutations)".
**Problems:**
- (a) Name the combining function, which should be Fisher's method on one-sided pointwise p-values as in O'Leary et al.
- (b) The statement that D4 "cannot flag" at k = 3 is correct (minimum p = 1/6). At k = 4 the minimum p is 1/24 ≈ 0.042, so D4 can flag only on the single most extreme ordering. This is a granularity artefact that should be stated.
- (c) For the secondary reference, the stable cut-off (PoPLR p > 0.5), the number of stable eyes and the specificity are not reported.
- (d) The secondary reference is circular for D4 and D10, as the primary one is for D1.

**Fix:** Add these details and report specificity for the secondary reference.

### 7. MODERATE — A perimetric learning effect in the Artes series is not considered
**Location:** E2 description: "In the Artes data we took every window of k consecutive tests."
**Problem:** Windows that start at tests 1–2 may contain a learning effect (improving sensitivity), which lowers false progression flags. Artes et al. [9] discuss perimetric experience. In addition, the Artes reliability indices (`fpr`, `fnr`, `fl`, loaded in `artes_retest.py`) are not reported or used.
**Fix:** Report results excluding windows that include test 1 or 2. Report the Artes reliability indices, and state whether unreliable fields were kept.

### 8. MODERATE — Treatment of the blind spot and grid in D6 and D10 on non-24-2 data
**Location:** "the 24-2-specific detectors (D6, D9, D10) were not applied (amendment A2)".
**Problem:** This is appropriate, but `make_regions` falls back to splitting by index for non-24-2 grids. Please confirm that this path was never used in any reported number. Also justify the four D6 regions (superior/inferior × central/peripheral) against the nerve-fibre-bundle layout (Garway-Heath), because hemifield-based clusters are standard.
**Fix:** Add a sentence confirming this, and either justify the region map or use the Garway-Heath sectors.

### 9. MINOR — The Table 1 Artes "Time from first to third test: 2 weeks by design" is not what the detectors saw
**Location:** Table 1.
**Fix:** Add a footnote saying that under amendment A1 the windows were analysed with UWHVF donor dates (median about 2.2–2.3 years to the third test).

### 10. MINOR — Reference 9 title is truncated, and reference 25 DOI looks inconsistent
**Location:** Reference 9: "Artes PH, ... Visual Field Progression in Glaucoma. Ophthalmology. 2014;121(10):2023-2027." Reference 25: "Trans. Vis. Sci. Tech.. 2022;11(1):2. https://doi.org/10.1167/tvst.11.1.1".
**Problem:** The full title of reference 9 includes "What Is the Specificity of the Guided Progression Analysis?", which is directly relevant, because the Artes data were originally used to measure GPA specificity. That makes the authors' novelty claim weaker and should be discussed. For reference 25, the article number (2) and the DOI suffix (.1) disagree. Please verify against the publisher.
**Fix:** Correct both references. In the Introduction, say explicitly that Artes et al. already used these data to estimate the false-positive rate of GPA.

### 11. MINOR — Spatial filtering, censoring at 0 dB and floor effects are not discussed
**Location:** Methods/Detectors.
**Fix:** State how values < 0 dB and floor locations were handled in the regressions (D3, D4). Floor locations have zero variance, and the supplement records a division-by-zero bug in development ("Weighted MD had a division-by-zero bug"). Confirm that the final code is free of it.
