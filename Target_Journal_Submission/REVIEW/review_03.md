# Review 03 — Glaucoma clinician / perimetry expert

**Focus:** clinical relevance, accuracy of the GPA/PoPLR descriptions, use of the Artes retest data (including amendment A1), GRAPE label use, and UWHVF's lack of diagnoses.

## Summary

The question is clinically important: can progression be called from fewer fields without false calls that lead to unnecessary escalation? A true no-change arm is a good idea, and the message that inflated flag rates need checking is welcome. The clinical framing, however, does not match the data.

- In the "few fields" scenario, fields are 1.3 years apart, so k = 3 already means 2.6 years of follow-up.
- The cohort is undiagnosed routine-care perimetry.
- The no-change arm lacks long-term variability.
- The external "glaucoma clinic" labels are largely computed from the same fields the detectors see.
- The event-analysis detector is described as GPA-like but differs from GPA in clinically important ways.

## Issues

### 1. MAJOR — The GRAPE "external validation" is close to circular for D1/D2
*Location:* Data sources: "with a median of 4 visits per eye the first three or four fields make up most of the series on which each label was computed". Results RQ5: "In GRAPE … D1 had a sensitivity of 44% (26–65) and a specificity of 95% (92–98) with three fields." Discussion: "in one clinic or in a second clinic using a different perimeter."

*Problem:* I checked the GRAPE data. 100 of 263 eyes (38%) have exactly three visits, and 9 of the 27 MD-label progressors are among them. For these eyes, the MD label (MD slope p < 0.05) is computed on exactly the three fields given to D1, and D1 is essentially the same test on the same data. In 3-visit eyes, D1 has sensitivity 8/9 and specificity 90/91. In eyes with ≥ 4 visits, its sensitivity is only 4/18 (22%). So the external D1 performance is largely the label reproducing itself. The Discussion statement that no detector beat the trend test "in a second clinic" therefore carries little weight.

*Fix:* Restrict the external analysis to eyes with at least k + 2 visits, and score them against labels recomputed on fields after k only. Report the 3-visit and ≥ 4-visit strata separately. Delete "in a second clinic" from the main conclusions, or qualify it there.

### 2. MAJOR — The GRAPE description is factually inaccurate: not all eyes have 59 points
*Location:* Table 1: "Octopus 900 G1, 59 analysable points".

*Problem:* `grape.py` removes, per eye, every point coded −1 at any visit. In the loaded data, 86 of 263 eyes have fewer than 59 points: the median is 59, the 10th percentile 42, the minimum 10, and 21 eyes have fewer than 40. Mean sensitivity over 10–40 points is not comparable across eyes. PLR-3 ("at least three locations") also behaves differently on 10 points than on 59. In addition, the G1 pattern is a 30° pattern with dense macular sampling, so "mean sensitivity" is not equivalent to the HFA 24-2 mean.

*Fix:* Correct Table 1. Report the distribution of analysable points, and exclude eyes below a minimum (e.g. < 50 points) as a sensitivity analysis. Explain how the −1 codes arise (untested points versus blind spot).

### 3. MAJOR — The Artes weekly retest arm underestimates clinical noise; A1 fixes the time axis but not the variance
*Location:* Methods E2: "each window was given the test dates of a randomly chosen UWHVF test-set eye … (amendment A1)". Limitations: "which keeps them a valid null but does not capture fluctuation over months or years."

*Problem:* Variability between visits months apart (long-term fluctuation, changes in media, pupil and learning, different technicians) is larger than variability between weekly tests. Borrowing UWHVF timestamps makes the slope units realistic, but the residual noise is still weekly. Every FPR in Table 2 is therefore likely an underestimate at clinical spacing, including D1's. "Valid" status near the margin (D1 at 5.1%, upper CI 8.1% at k = 6) may not hold in clinic. The miscalibration also differs by detector. D7's limits come from UWHVF routine-care pairs ≤ 0.5 yr apart (wider noise), so D7 looks very conservative on Artes (1.1–1.9%) but flags 5–12% in the UW shuffle audit. The Artes arm thus rewards detectors calibrated on noisier data. One Artes patient's series actually spans 524 days, not 12 weeks (the other 29 span 63–105 days).

*Fix:* Discuss the direction of the bias explicitly. Complement Artes with a clinical-spacing no-change surrogate, e.g. pairs of fields from stable eyes months apart. Report a sensitivity analysis that excludes D7's calibration mismatch. Correct "12 visual fields in 12 consecutive weeks" to give the actual range of spans (median 84 days, one outlier of 524 days).

### 4. MAJOR — D7 is not GPA; the "similar in spirit" description overstates the comparison
*Location:* Methods D7: "a location is 'deteriorated' if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes … similar in spirit to Guided Progression Analysis [11]." Intro: "Event methods compare each follow-up test with a baseline, using limits taken from stable patients [9–11]."

*Problem:* GPA works on pattern deviation, not raw sensitivity. That is a clinically crucial difference, because it removes diffuse loss from cataract. GPA's limits come from short-term retest of stable glaucoma patients (Heijl et al.). Here, the limits come from UWHVF routine-care pairs ≤ 6 months apart, in undiagnosed eyes, possibly including real change. They are derived from single-test differences but applied to differences from a two-test mean, which have smaller variance, so the limits are too wide. D7's flag rule (≥ 3 points on 2 consecutive tests) corresponds to GPA "possible progression", not "likely progression" (3 consecutive tests). The citation [11] is the EMGT criteria comparison, not the GPA method description.

*Fix:* Describe D7 as a "pointwise event analysis on total sensitivity". List the differences from GPA, compute D7 on pattern deviation (UWHVF provides TD, from which PD can be derived), and cite the GPA method papers.

### 5. MAJOR — Clinical relevance: "few fields" here means years, and the conclusion about escalation is not supported
*Location:* Results: "six fields took a median of 6.5 years". Abstract/Introduction framing about "earlier treatment escalation". Discussion: "Until a detector shows a valid false-alarm rate on true no-change data, a flag from it should not by itself trigger escalation of treatment."

*Problem:* Three fields at UW spacing span about 2.6 years, and the reference eyes were followed for a median of 12.9 years. That is a long-term surveillance setting, not the "first two years, six fields" setting recommended by Chauhan et al. [5], which the paper cites as the motivation. Results at UW spacing cannot be translated into "how early" in a clinic that follows the guidance. The study does not examine treatment, IOP or escalation at all: UWHVF contains no treatment data. So the claim about escalation is a recommendation that goes beyond the data. Real clinicians do not escalate on one algorithmic flag; they confirm it. Confirmation is missing from all detectors (D1–D6 and D8–D10 flag on a single analysis).

*Fix:* Add a scenario that re-times the series to guideline spacing, or analyse eyes with dense early testing. Add confirmation rules (e.g. a flag that persists at k + 1), which is how detectors are used clinically and which will change FPRs a lot. Soften the escalation statements.

### 6. MAJOR — UWHVF has no diagnoses; the population and the reference eyes are undefined
*Location:* Data sources: "It includes sensitivities, age and laterality, but no diagnosis or reliability indices." Limitations: "the cohort may include eyes without glaucoma."

*Problem:* The reference eyes have a median baseline MD of −4.4 dB. Without diagnoses, the sample may include neuro-ophthalmic disease, ocular hypertension, suspects and normal eyes. Non-glaucomatous causes of MD decline, such as cataract and retinal disease, can drive "progressor" labels, and these would favour MD-based detectors (D1/D2/D5) over pointwise ones (D3/D4/D7). Reliability indices are unavailable, so unreliable fields cannot be excluded. In Artes, reliability indices are loaded but not used. Note also that UWHVF provides gender, which is not reported (see the journal's SAGER requirement).

*Fix:* Use proxies, such as excluding eyes with a normal 24-2 at all visits, or requiring a glaucomatous PSD/cluster pattern. Report sex. Report results stratified by severity (MD > −6 versus ≤ −6 dB), because noise and detector behaviour depend strongly on severity [4].

### 7. MODERATE — The PoPLR description and the k = 3 floor
*Location:* Introduction: "Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [7]". Discussion: "with three fields it has only six orders and cannot reach p < 0.05. This floor is a property of the method".

*Problem:* The description is acceptable. It would help to add that PoPLR combines one-sided pointwise p-values into Fisher's S. Clinically, the more relevant point is that O'Leary et al. designed PoPLR for series of ≥ 5–6 fields. Including k = 3–4 tests the method outside its intended use, and counting it as "valid" at k = 3 (FPR 0, sensitivity 0) is meaningless.

*Fix:* Report D4 (and D7/D10) only where they can operate, or label those cells "not applicable".

### 8. MODERATE — The "MD rate" rule uses mean sensitivity, and its sensitivity decreases as k increases
*Location:* Methods D2: "slope of mean sensitivity of −1 dB per year or worse (a common 'fast progression' rule…)". Table 2: D2 sensitivity is 38% at k = 3, then 23% at k = 4–6.

*Problem:* The clinical fast-progression rule uses MD (age-corrected), and is usually applied over longer series. The fall in sensitivity with more fields shows that the k = 3 "gain" is noise. That matches the 11.7% shuffle-audit rate and the 79% GRAPE specificity, and should be said.

*Fix:* Comment on this non-monotonicity, and do not present D2 at k = 3 as a candidate improvement ("D2 flagged 38% … versus 19%").

### 9. MODERATE — GRAPE population
*Location:* Table 1: "Median 41 (IQR 28–53)".

*Problem:* A median age of 41 in a glaucoma cohort suggests a large share of juvenile-onset or primary angle-closure disease, whose progression dynamics differ. The glaucoma subtypes in GRAPE should be reported.

*Fix:* Report the GRAPE diagnosis mix from the source paper, and stratify if possible.

### 10. MINOR — Wording and accuracy
- "Glaucoma does not change in 12 weeks in a measurable way". This is acceptable, but cite Artes 2014 for it and note that learning effects were checked. I found no trend in mean sensitivity across the 12 sessions (26.4 → 26.3 dB), which is reassuring and worth reporting.
- Reference 9's title is truncated ("Visual Field Progression in Glaucoma."). The full title is "…: What Is the Specificity of the Guided Progression Analysis?" Verify it against Crossref.
- "D1 OLS-MD" is named MD but uses mean sensitivity. Rename it "OLS-MS" or explain.

## Recommendation

**Major revision.** The true-null concept is valuable. But the external validation is largely circular, the Artes noise structure biases the null in favour of some detectors, D7 is mislabelled as GPA-like, and the clinical framing (earlier escalation) is not supported by a dataset with no treatment information and 1.3-year spacing.
