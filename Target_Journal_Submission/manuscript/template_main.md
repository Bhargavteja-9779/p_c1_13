# Early Detection of Glaucomatous Visual Field Progression Without False Alarms: A Benchmark With True No-Change Data

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, DEGREES AND ORCID IDS – TO BE COMPLETED BY THE AUTHORS]

**Affiliations:** [TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, POSTAL ADDRESS, EMAIL – TO BE COMPLETED BY THE AUTHORS]

**Running title:** False alarms in early visual field progression detection

# Abstract

**Introduction:** New methods for detecting glaucomatous visual field progression often flag more eyes than simple trend tests, but extra flags can be false alarms. We asked whether any detector finds progression earlier than a simple trend test without false alarms above the nominal level on data where no change is possible.

**Methods:** We compared ten detectors (trend, event, permutation, conformal and machine-learning; three were our own development variants) using only the first 3–6 tests of each series. Sensitivity and specificity were measured in University of Washington test-set eyes against a reference based on each eye's full follow-up ({{d:uwhvf.test_ge8.n_prog}} progressors, {{d:uwhvf.test_ge8.n_stable}} stable eyes). False alarms were measured on 12-week retest series of {{d:artes.n_patients}} patients with glaucoma (true no change). External testing used {{d:grape.n_eyes}} eyes from a clinic in China. The comparator was the least-squares trend of mean sensitivity (OLS-MD).

**Results:** At three tests, OLS-MD detected {{ci:D1:3:sens}} of progressors with {{m:D1:3:fpr_true_null}} false alarms. The only significantly more sensitive detector, a pooled-detrended conformal variant from our development work ({{pp:D6:3:sensitivity}}), raised {{m:D6:3:fpr_true_null}} false alarms, although its specificity against the full-series reference was {{m:D6:3:spec}}. Gradient-boosted trees thresholded at 95% specificity gave {{m:D8:3:fpr_true_null}}, {{m:D8:4:fpr_true_null}} and {{m:D8:5:fpr_true_null}} false alarms at 3–5 tests. No detector without excess false alarms beat OLS-MD significantly, but the study could only detect differences of about {{ph_mdd_pp}} percentage points. A shuffle audit did not meet its pre-specified agreement target (Spearman ρ = {{s:spearman_rho}}). Externally, higher sensitivity again came with more false positives.

**Conclusion:** In this benchmark, every significant early-detection gain over a simple trend test came with false alarms above the nominal level, which specificity against a full-series reference did not show. New progression detectors should be evaluated on true no-change data before clinical use.

**Keywords:** Artificial intelligence; Benchmarking; Glaucoma; Machine learning; Perimetry; Sensitivity and specificity; Visual field progression

# Key Summary Points

**Why carry out this study?**

- Escalating glaucoma treatment depends on detecting visual field progression, and many new methods claim earlier detection from fewer tests.
- Most studies estimate false alarms indirectly, so an earlier flag may reflect real progression or simply more false alarms.
- We asked whether any of ten detectors flags more future-confirmed progressors than a simple trend test while keeping false alarms at the nominal level on true no-change data.

**What was learned from the study?**

- The only significant sensitivity gain over the simple trend test came with false alarms in more than one in five no-change series, and a machine-learning model thresholded in a common way also had excess false alarms; specificity against a full-series reference did not reveal either problem.
- No detector without excess false alarms clearly beat the simple trend test, although small gains could not be excluded; true no-change data should be part of every evaluation of a new progression detector.

{{INTRO_METHODS}}

# Results

## Study sample

The UWHVF test set contained {{d:uwhvf.test.n_eyes_ge3}} eyes of {{d:uwhvf.test.n_patients_ge3}} patients with at least three tests; these eyes were used for the shuffle audit. Of the {{d:uwhvf.test_ge8.n_eyes}} test-set eyes with at least eight tests, {{d:uwhvf.test_ge8.n_prog}} were reference progressors, {{d:uwhvf.test_ge8.n_stable}} were reference stable and {{d:uwhvf.test_ge8.n_excluded}} were indeterminate and excluded. The {{meta:n_test_ref}} reference eyes came from {{d:uwhvf.test_ge8.n_ref_patients}} patients. Their median age at the first test was {{d:uwhvf.test_ge8.age_years.median}} years, median baseline mean total deviation was {{d:uwhvf.test_ge8.baseline_mtd_db.median}} dB, and they had a median of {{d:uwhvf.test_ge8.n_tests.median}} tests over {{d:uwhvf.test_ge8.followup_years.median}} years (median interval between tests {{d:uwhvf.test_ge8.interval_years.median}} years). Development used {{d:uwhvf.train.n_eyes_ge3}} training and {{d:uwhvf.val.n_eyes_ge3}} validation eyes. The Artes data gave {{d:artes.windows.3}}, {{d:artes.windows.4}}, {{d:artes.windows.5}} and {{d:artes.windows.6}} no-change windows of 3, 4, 5 and 6 tests. In GRAPE, eyes had a median of {{d:grape.n_visits.median}} visits over {{d:grape.followup_years.median}} years; {{d:grape.n_md_prog}} eyes were labelled as progressing by the mean-deviation criterion, and {{d:grape.n_ge4}} eyes had four or more tests.

## False alarms on true no-change data (RQ1)

Table 1 and Fig. 2 show all results. The simple trend test (D1) had false-alarm rates between {{m:D1:4:fpr_true_null}} and {{m:D1:6:fpr_true_null}} across 3–6 tests, for example {{ci:D1:3:fpr_true_null}} at three tests{{check:notabove:D1:3}}{{check:notabove:D1:4}}{{check:notabove:D1:5}}{{check:notabove:D1:6}}. No detector based on a p-value or a fixed rule (D1–D5, D7, D10) had false alarms significantly above 5% at any number of tests. PoPLR, event analysis and the order network could not flag any eye at three tests, because three tests allow only six orderings or no confirmation test.

Three detectors had false alarms significantly above 5%. The pooled-detrended conformal test (D6) raised false alarms in {{ci:D6:3:fpr_true_null}} of no-change windows at three tests{{check:above:D6:3}}; at 4–6 tests its rates were {{m:D6:4:fpr_true_null}}, {{m:D6:5:fpr_true_null}} and {{m:D6:6:fpr_true_null}}. The tabular machine-learning model (D8) gave {{ci:D8:3:fpr_true_null}} at three tests, {{ci:D8:4:fpr_true_null}} at four and {{ci:D8:5:fpr_true_null}} at five{{check:above:D8:3}}{{check:above:D8:4}}{{check:above:D8:5}}. The sequence model (D9) gave {{ci:D9:3:fpr_true_null}} at three tests{{check:above:D9:3}}. Under the stricter readings of validity, more cells failed, including D1 at every number of tests under the strict reading (Table 1); the conclusions below about D6, D8 and D9 hold under all three readings.

Specificity against the full-series reference hardly separated these detectors from D1: at three tests D6 had a specificity of {{m:D6:3:spec}} and D8 {{m:D8:3:spec}}, against {{m:D1:3:spec}} for D1. In the post hoc future-only reference, built from later tests only ({{focount:3:prog}} progressors and {{focount:3:stable_p05}} stable eyes at three tests), the difference appeared: specificity was {{fo:D6:3:spec_p05}} for D6 and {{fo:D8:3:spec_p05}} for D8, against {{fo:D1:3:spec_p05}} for D1 (Supplementary Table S3).

## Sensitivity compared with the simple trend test (RQ2)

At three tests D1 flagged {{ci:D1:3:sens}} of reference progressors. Only D6 flagged significantly more: {{ci:D6:3:sens}}, a difference of {{pp:D6:3:sensitivity}} (discordant eyes {{n:D6:3:sensitivity}}; Holm p = {{ph:D6:3:sensitivity}}){{check:sig:D6:3:sensitivity}}. The largest gain by a detector without excess false alarms at three tests came from the rate rule D2 ({{pp:D2:3:sensitivity}}; Holm p = {{ph:D2:3:sensitivity}}){{check:ns:D2:3:sensitivity}}{{check:notabove:D2:3}}.

At four to six tests no detector was significantly more sensitive than D1; the pointwise rule D3 was less sensitive at six tests (Holm p = {{ph:D3:6:sensitivity}}){{check:ns:D6:4:sensitivity}}{{check:ns:D7:5:sensitivity}}{{check:ns:D8:6:sensitivity}}{{check:ns:D10:5:sensitivity}}{{check:sig:D3:6:sensitivity}}. The largest point gain was D8 at six tests ({{pp:D8:6:sensitivity}}; Holm p = {{ph:D8:6:sensitivity}}){{check:notabove:D8:6}}, where its false-alarm rate was {{m:D8:6:fpr_true_null}}. Event analysis (D7) detected {{m:D7:5:sens}} at five tests against {{m:D1:5:sens}} for D1 (Holm p = {{ph:D7:5:sensitivity}}). The pooled-shuffle conformal test (D5) flagged the same reference eyes as D1 at every number of tests{{check:same:D5}}. Our hypothesis that no detector without excess false alarms would beat D1 significantly was therefore not falsified. This is weak evidence: with {{d:uwhvf.test_ge8.n_prog}} progressors, a difference needed about {{ph_mdd_pp}} percentage points to reach significance, and for several detectors the upper confidence limit of the gain exceeded 20 percentage points (for example D2 at three tests and D8 at four and six tests; Supplementary Table S2){{check:pairhi_gt:D2:3:sensitivity:0.2}}{{check:pairhi_gt:D8:4:sensitivity:0.2}}{{check:pairhi_gt:D8:6:sensitivity:0.2}}.

The secondary, PoPLR-based reference gave lower sensitivities for all detectors. At three tests D6 again had the highest sensitivity ({{m:D6:3:sens_ref2}} vs {{m:D1:3:sens_ref2}} for D1). At six tests D1 detected {{ci:D1:6:sens_ref2}}, and D6, D10 and D8 had slightly higher point estimates ({{m:D6:6:sens_ref2}}, {{m:D10:6:sens_ref2}} and {{m:D8:6:sens_ref2}}; Supplementary Table S1); these differences were not tested.

## Machine-learning thresholds (RQ4)

Both supervised models were thresholded at 95% specificity on validation-set reference-stable eyes, and their specificity in test-set reference-stable eyes was at least {{m:D9:6:spec}}{{check:minspec:D9:6}}. Their false-alarm rates on true no-change data were D8: {{m:D8:3:fpr_true_null}}, {{m:D8:4:fpr_true_null}}, {{m:D8:5:fpr_true_null}} and {{m:D8:6:fpr_true_null}} at 3–6 tests; D9: {{m:D9:3:fpr_true_null}}, {{m:D9:4:fpr_true_null}}, {{m:D9:5:fpr_true_null}} and {{m:D9:6:fpr_true_null}}. The hypothesis that this thresholding gives too many false alarms was supported for D8 at three to five tests and for D9 at three tests, but not at six tests. The sequence model was unstable across seeds (between-seed standard deviation of sensitivity up to {{m:D9:6:sens_seed_sd}}; Supplementary Table S1).

## Shuffle audit (RQ3)

Across {{s:n_cells}} detector and test-number cells, the false-alarm rate from the shuffle audit correlated with the true no-change rate (Spearman ρ = {{s:spearman_rho}}, 95% CI {{rq3ci}}; Fig. 3), below the pre-specified target of 0.7, so H3 was not supported. The median absolute difference was {{s:median_abs_diff}} percentage points, and {{s:share_within_3pp}} of cells differed by 3 percentage points or less. The audit gave rates above 10% for D6 at three tests ({{m:D6:3:fpr_shuffle}}) and D8 at three and five tests ({{m:D8:3:fpr_shuffle}}, {{m:D8:5:fpr_shuffle}}), but also for the rate rule at three tests ({{m:D2:3:fpr_shuffle}} vs {{m:D2:3:fpr_true_null}} on true no-change data) and event analysis at six tests ({{m:D7:6:fpr_shuffle}} vs {{m:D7:6:fpr_true_null}}). It did not flag D6 at six tests ({{m:D6:6:fpr_shuffle}} vs {{m:D6:6:fpr_true_null}}). In a post hoc look, every cell with a difference above 3 percentage points belonged to the rate rule, event analysis or a machine-learning model.

## External clinic (RQ5)

In GRAPE (Table 2, Fig. 4), D1 detected {{ci:D1:3:grape_sens}} of eyes labelled as progressing with three tests, at a specificity of {{ci:D1:3:grape_spec}}. The rate rule (D2) and the transferred tabular model (D8) detected more progressing eyes ({{m:D2:3:grape_sens}} and {{m:D8:3:grape_sens}}), but neither gain was significant after correction (Holm p = {{ph:D2:3:gsens}} and {{ph:D8:3:gsens}}, respectively){{check:ns:D2:3:gsens}}{{check:ns:D8:3:gsens}}. Both flagged significantly more non-progressing eyes ({{pp:D2:3:gfp}} and {{pp:D8:3:gfp}}; both Holm p {{ph:D8:3:gfp}}){{check:sig:D2:3:gfp}}{{check:sig:D8:3:gfp}}. PoPLR, the pointwise rule and event analysis were less sensitive than D1 at three tests{{check:sig:D3:3:gsens}}{{check:sig:D4:3:gsens}}{{check:sig:D7:3:gsens}}. At four tests, D2 and D8 again flagged more non-progressing eyes without a significant sensitivity gain{{check:ns:D2:4:gsens}}{{check:ns:D8:4:gsens}}{{check:sig:D2:4:gfp}}{{check:sig:D8:4:gfp}}. In the post hoc analysis restricted to eyes with at least five visits ({{gr:D1:3:MD:r:n}} eyes, {{gr:D1:3:MD:r:n_pos}} progressing), sensitivity at three tests was {{gr:D1:3:MD:r:sens}} for D1, {{gr:D2:3:MD:r:sens}} for D2 and {{gr:D8:3:MD:r:sens}} for D8, with specificity {{gr:D1:3:MD:r:spec}}, {{gr:D2:3:MD:r:spec}} and {{gr:D8:3:MD:r:spec}} (Supplementary Table S4). D6, D9 and D10 could not be tested in GRAPE, and GRAPE has no no-change arm.

## Real-world measures

At three tests, D6 would produce about {{ff:D6:3}} false progression flags per 1,000 stable eyes and D8 about {{ff:D8:3}}, compared with {{ff:D1:3}} for D1 (Table 3). Followed to six tests, D1 flagged {{rw:D1:prog_detected_by_6}} of reference progressors, at a median of the {{rw:D1:prog_median_first_k_detected}}th test among those flagged. D6 and D8 flagged {{rw:D6:prog_detected_by_6}} and {{rw:D8:prog_detected_by_6}}. These figures are per detection opportunity; repeated looks in the same eye accumulate false alarms.

# Discussion

We built an open benchmark for a simple clinical question: can visual field progression be detected earlier without raising false alarms? Using a true no-change arm, a future-confirmed reference and an external clinic, we compared ten detectors at three to six tests. Every significant sensitivity gain over a simple trend test came with false alarms well above the nominal level. No detector without excess false alarms beat the simple trend test, but the study was too small to exclude moderate gains.

Two findings deserve emphasis. First, the over-sensitive detectors included one of our own development variants (D6) and a machine-learning model thresholded in a common way (D8). The behaviour of D6 was already known to us from development, so its inclusion is an illustration rather than an independent discovery. The machine-learning result is more general: a threshold set at 95% specificity in reference-stable eyes gave false-alarm rates of {{m:D8:3:fpr_true_null}} to {{m:D8:5:fpr_true_null}} at three to five tests on true no-change data. Second, specificity against the conventional full-series reference did not reveal either problem. This is partly by design: "stable" eyes in such references have a non-negative trend over their whole series, which includes the tests the detector sees. When we built a reference from later tests only, the specificity of the over-sensitive detectors fell below that of the trend test. Evaluations that use full-series references should therefore not be read as evidence of a low false-alarm rate. Our findings agree with the view that test–retest variability limits how early change can be confirmed [4, 8, 25, 26], and with recent work showing that progression labels strongly affect machine-learning results [22].

Comparing a detector on the eye's real test order with shuffled orders is not new; it is the basis of PoPLR [6], and retest data have been used before to check the specificity of event analysis [7]. Our shuffle audit applies the same idea to any detector. It did not meet our agreement target, and it over-flagged rules without a p-value, so it is a screening tool, not a substitute for true no-change data.

For clinics, the practical message is modest. In our data a simple trend of mean sensitivity, tested at the 5% level, was not beaten by any detector without excess false alarms. A detector that flags many more eyes than this should be treated with caution until its false-alarm rate on no-change data is known. For developers and reviewers, we suggest that early-detection claims should report false-alarm rates on true no-change data alongside sensitivity, and that thresholds should not be set only against full-series reference-stable eyes.

This study has limitations. First, the future-reference test set was small ({{d:uwhvf.test_ge8.n_prog}} progressors and {{d:uwhvf.test_ge8.n_stable}} stable eyes), so confidence intervals are wide; the McNemar test also treats the two eyes of a patient as independent. Second, the reference standards use the full series and favour mean-deviation detectors; the post hoc future-only reference had even fewer progressors. Third, the true no-change arm has only {{d:artes.n_patients}} patients from one centre, tested weekly. Weekly retests do not contain long-term fluctuation, so rate-based rules may look more valid than they would be in routine care; our assignment of clinical test intervals keeps the null valid but cannot add this variability. The arm had also been used during development and in a pipeline check. Fourth, the machine-learning models were trained on a few hundred labelled eyes and thresholded on the same validation set used for model selection; larger models trained on more data may behave differently. Fifth, GRAPE used a different perimeter and criterion-based labels computed from the same tests in eyes with few visits; three detectors could not be tested there, and the transferred machine-learning model faced a change in measurement scale. Sixth, our event analysis is a simplified, conservative version of Guided Progression Analysis, and we did not test the Visual Field Index, ANSWERS or other Bayesian hierarchical models [9, 35], smoothing [36] or forecasting-based schedules [34]. The benchmark code is open so that these can be added. Finally, a retrospective benchmark cannot show whether earlier detection changes visual outcomes.

# Conclusions

In this open benchmark, every significant early-detection gain over a simple trend test came with false alarms above the nominal level, and specificity against a full-series reference did not reveal this. A simple trend test was not clearly beaten at three to six tests, although the study was too small to exclude moderate gains. New progression detectors, including machine-learning tools, should be evaluated on true no-change data before clinical use, and prospective studies should test whether earlier valid detection improves outcomes.

# Declarations

**Funding.** [TO BE COMPLETED BY THE AUTHORS: state funding, or "No funding or sponsorship was received for this study or publication of this article." Include who funds the journal's publication fee.]

**Medical Writing/Editorial Assistance.** An AI assistant (Claude, Anthropic) was used to write analysis code and draft the manuscript (see Methods). [THE AUTHORS MUST CONFIRM AND DESCRIBE THEIR VERIFICATION, AND COMPLETE ANY OTHER ASSISTANCE.]

**Author Contributions.** [TO BE COMPLETED BY THE AUTHORS (CRediT roles).]

**Conflict of Interest.** [TO BE COMPLETED BY THE AUTHORS.]

**Ethical Approval.** This study used only publicly available, de-identified data sets released by their custodians under open licences (UWHVF: BSD-3; GRAPE: CC0; Artes retest data: distributed with the visualFields R package). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

**Data Availability.** All data are public: UWHVF (https://github.com/uw-biomedical-ml/uwhvf), GRAPE (figshare, DOI in reference [15]) and the Artes retest data (visualFields R package 1.0.7 on CRAN). All code, the pre-registered protocol, raw per-eye results and the patient-level split are available at [REPOSITORY URL – TO BE COMPLETED BY THE AUTHORS BEFORE SUBMISSION].

<!--REFS-->

# References

{{REFS}}

# Tables

**Table 1** Sensitivity and specificity against the future reference (UWHVF test set) and false-alarm rates on true no-change data (Artes retest) and in the shuffle audit, by number of tests

{{TABLE1}}

CI, confidence interval (patient-cluster bootstrap, 2,000 resamples); GRU, gated recurrent unit; ML, machine learning; OLS-MD, ordinary least-squares trend of mean sensitivity; PLR, pointwise linear regression; PoPLR, permutation of pointwise linear regression. Validity readings for the true no-change false-alarm rate: (i) lower 95% confidence limit above 5% (false alarms significantly above nominal); (ii) lower limit ≤5% and upper limit ≤10%; (iii) upper limit ≤5%. n = 26 progressors and 26 stable eyes for sensitivity and specificity; when all or no eyes were flagged the bootstrap interval is degenerate (exact Clopper–Pearson intervals in Supplementary Table S1). Specificity is against a full-series reference and is high by design (see Methods).

**Table 2** External clinic (GRAPE): detection of progression labelled by the mean-deviation criterion supplied with the data set, from the first three or four tests

{{TABLE2}}

pp, percentage points; Holm p, exact McNemar test with Holm correction within each number of tests. D6, D9 and D10 use the 24-2 grid and were not applied (protocol amendment A2). At four tests only eyes with four or more tests were included.

**Table 3** Real-world measures: expected false progression flags and timing of first detection

{{TABLE3}}

False flags per 1,000 stable eyes = false-alarm rate on true no-change data × 1,000, per detection opportunity. *Among reference progressors flagged by test 6 (UWHVF test set, n = 26 progressors, 26 stable eyes); flags are evaluated at tests 3, 4, 5 and 6.
