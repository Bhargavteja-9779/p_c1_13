# Early Detection of Glaucomatous Visual Field Progression Without False Alarms: A Benchmark With True No-Change Data

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, DEGREES AND ORCID IDS – TO BE COMPLETED BY THE AUTHORS]

**Affiliations:** [TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, POSTAL ADDRESS, EMAIL – TO BE COMPLETED BY THE AUTHORS]

**Running title:** False alarms in early visual field progression detection

# Abstract

**Introduction:** New methods for detecting glaucomatous visual field progression often flag more eyes than simple trend tests, but extra flags can be false alarms. We asked which detectors find progression earlier without raising false alarms on data where no change is possible.

**Methods:** We compared ten detectors (trend, event, permutation, conformal and machine-learning) using only the first 3–6 tests of each series. Sensitivity and specificity were measured in University of Washington test-set eyes against a reference based on each eye's full follow-up ({{d:uwhvf.test_ge8.n_prog}} progressors, {{d:uwhvf.test_ge8.n_stable}} stable eyes). False alarms were measured on 12-week retest series of {{d:artes.n_patients}} patients with glaucoma (true no change). External testing used {{d:grape.n_eyes}} eyes from a clinic in China. The comparator was the ordinary least-squares trend of mean sensitivity (OLS-MD).

**Results:** At three tests, OLS-MD detected {{ci:D1:3:sens}} of progressors with {{m:D1:3:fpr_true_null}} false alarms. The only detector with significantly higher sensitivity (pooled-detrended conformal test, {{pp:D6:3:sensitivity}}; Holm p = {{ph:D6:3:sensitivity}}) raised {{m:D6:3:fpr_true_null}} false alarms on true no-change data, although its specificity against the reference was {{m:D6:3:spec}}. Gradient-boosted trees thresholded at 95% specificity, as is common practice, gave {{m:D8:3:fpr_true_null}}, {{m:D8:4:fpr_true_null}} and {{m:D8:5:fpr_true_null}} false alarms at 3–5 tests. No detector with valid false alarms beat OLS-MD significantly at any number of tests. A shuffle audit, which re-orders each eye's own tests, tracked true false-alarm rates (Spearman ρ = {{s:spearman_rho}}; median difference {{s:median_abs_diff}} percentage points). Externally, higher sensitivity again came with more false positives.

**Conclusion:** In this benchmark, apparent gains in early progression detection were explained by false alarms that standard specificity estimates missed. Clinics and developers should test detectors on true no-change data, or at least with a shuffle audit, before adopting them.

**Keywords:** Artificial intelligence; Benchmarking; Glaucoma; Machine learning; Perimetry; Sensitivity and specificity; Visual field progression

# Key Summary Points

**Why carry out this study?**

- Escalating glaucoma treatment depends on detecting visual field progression, and many new methods claim earlier detection from fewer tests.
- Most studies estimate false alarms indirectly, so an earlier flag may reflect real progression or simply more false alarms.
- We asked whether any of ten detectors flags more future-confirmed progressors than a simple trend test while keeping false alarms low on true no-change data.

**What was learned from the study?**

- The only significant sensitivity gain over the simple trend test came from a method with more than one false alarm in five no-change series; specificity against a conventional reference did not reveal this.
- No detector with valid false alarms beat the simple trend test, and a shuffle audit that any clinic can run on its own records identified the invalid detectors.

{{INTRO_METHODS}}

# Results

## Study sample

The UWHVF test set contained {{d:uwhvf.test.n_eyes_ge3}} eyes of {{d:uwhvf.test.n_patients_ge3}} patients with at least three tests; these eyes were used for the shuffle audit. Of the {{d:uwhvf.test_ge8.n_eyes}} test-set eyes with at least eight tests, {{d:uwhvf.test_ge8.n_prog}} were reference progressors, {{d:uwhvf.test_ge8.n_stable}} were reference stable and {{d:uwhvf.test_ge8.n_excluded}} were indeterminate and excluded. The {{meta:n_test_ref}} reference eyes came from {{d:uwhvf.test_ge8.n_ref_patients}} patients. Their median age at the first test was {{d:uwhvf.test_ge8.age_years.median}} years, median baseline mean total deviation was {{d:uwhvf.test_ge8.baseline_mtd_db.median}} dB, and they had a median of {{d:uwhvf.test_ge8.n_tests.median}} tests over {{d:uwhvf.test_ge8.followup_years.median}} years (median interval between tests {{d:uwhvf.test_ge8.interval_years.median}} years). Development used {{d:uwhvf.train.n_eyes_ge3}} training and {{d:uwhvf.val.n_eyes_ge3}} validation eyes. The Artes data gave {{d:artes.windows.3}}, {{d:artes.windows.4}}, {{d:artes.windows.5}} and {{d:artes.windows.6}} no-change windows of 3, 4, 5 and 6 tests. In GRAPE, eyes had a median of {{d:grape.n_visits.median}} visits over {{d:grape.followup_years.median}} years; {{d:grape.n_md_prog}} eyes were labelled as progressing by the mean-deviation criterion, and {{d:grape.n_ge4}} eyes had four or more tests.

## False alarms on true no-change data (RQ1)

Table 1 and Fig. 2 show all results. The simple trend test (D1) kept false alarms close to the nominal 5% at every number of tests, for example {{ci:D1:3:fpr_true_null}} at three tests{{check:valid:D1:3}}{{check:valid:D1:4}}{{check:valid:D1:5}}{{check:valid:D1:6}}. So did the rate rule, the pointwise rule, PoPLR, the pooled-shuffle conformal test, event analysis and the self-supervised order network{{check:valid:D2:3}}{{check:valid:D3:3}}{{check:valid:D4:3}}{{check:valid:D5:3}}{{check:valid:D7:3}}{{check:valid:D10:3}}. PoPLR, event analysis and the order network could not flag any eye at three tests, because three tests allow only six orderings or no confirmation test.

Three detectors were not valid. The pooled-detrended conformal test (D6) raised false alarms in {{ci:D6:3:fpr_true_null}} of no-change windows at three tests{{check:invalid:D6:3}} and {{m:D6:6:fpr_true_null}} at six tests{{check:invalid:D6:6}}. The tabular machine-learning model (D8) gave {{ci:D8:3:fpr_true_null}} at three tests, {{m:D8:4:fpr_true_null}} at four and {{m:D8:5:fpr_true_null}} at five{{check:invalid:D8:3}}{{check:invalid:D8:4}}{{check:invalid:D8:5}}. The sequence model (D9) gave {{ci:D9:3:fpr_true_null}} at three tests{{check:invalid:D9:3}}{{check:invalid:D9:5}}; at six tests its upper confidence limit was {{m:D9:6:fpr_true_null_hi}}, just above the 10% bound.

In contrast, specificity against the future reference hardly separated valid from invalid detectors. At three tests D6 had a specificity of {{m:D6:3:spec}} and D8 {{m:D8:3:spec}}, the same range as D1 ({{m:D1:3:spec}}).

## Sensitivity compared with the simple trend test (RQ2)

At three tests D1 flagged {{ci:D1:3:sens}} of reference progressors. Only D6 flagged significantly more: {{ci:D6:3:sens}}, a difference of {{pp:D6:3:sensitivity}} (discordant eyes {{n:D6:3:sensitivity}}; Holm p = {{ph:D6:3:sensitivity}}){{check:sig:D6:3:sensitivity}}, and D6 was not valid at this number of tests. The largest gain by a valid detector at three tests came from the rate rule D2 ({{pp:D2:3:sensitivity}}; Holm p = {{ph:D2:3:sensitivity}}){{check:ns:D2:3:sensitivity}}.

At four to six tests no detector differed significantly from D1 in sensitivity, except the pointwise rule D3, which was less sensitive at six tests (Holm p = {{ph:D3:6:sensitivity}}){{check:ns:D6:4:sensitivity}}{{check:ns:D7:5:sensitivity}}{{check:ns:D8:6:sensitivity}}{{check:ns:D10:5:sensitivity}}{{check:sig:D3:6:sensitivity}}. The largest point gain by a valid detector at four or more tests was D8 at six tests ({{pp:D8:6:sensitivity}}; Holm p = {{ph:D8:6:sensitivity}}){{check:valid:D8:6}}. Event analysis (D7) detected {{m:D7:5:sens}} at five tests against {{m:D1:5:sens}} for D1 (Holm p = {{ph:D7:5:sensitivity}}). The pooled-shuffle conformal test (D5) flagged exactly the same reference eyes as D1 at every number of tests{{check:same:D5}}. Our hypothesis that no valid detector would beat D1 by a significant margin was therefore not falsified. However, with {{d:uwhvf.test_ge8.n_prog}} progressors the confidence intervals are wide, and for several detectors the upper confidence limit of the gain exceeded 20 percentage points (for example D2 at three tests and D8 at four and six tests; Supplementary Table S2){{check:pairhi_gt:D2:3:sensitivity:0.2}}{{check:pairhi_gt:D8:4:sensitivity:0.2}}{{check:pairhi_gt:D8:6:sensitivity:0.2}}.

The secondary reference, based on PoPLR over the full series, gave the same ordering (Supplementary Table S1). For example, D1 detected {{ci:D1:6:sens_ref2}} of PoPLR-defined progressors at six tests.

## Machine-learning thresholds (RQ4)

Both supervised models were thresholded at 95% specificity on validation-set reference-stable eyes. Their specificity in test-set stable eyes was at least {{m:D9:6:spec}}{{check:minspec:D9:6}}, but their false-alarm rates on true no-change data were above 5% at most numbers of tests (D8: {{m:D8:3:fpr_true_null}}, {{m:D8:4:fpr_true_null}}, {{m:D8:5:fpr_true_null}} and {{m:D8:6:fpr_true_null}} at 3–6 tests; D9: {{m:D9:3:fpr_true_null}}, {{m:D9:4:fpr_true_null}}, {{m:D9:5:fpr_true_null}} and {{m:D9:6:fpr_true_null}}). The hypothesis that this common practice gives too many false alarms was supported at three to five tests for D8. The sequence model was also unstable across seeds (between-seed standard deviation of sensitivity up to {{m:D9:6:sens_seed_sd}}; Supplementary Table S1).

## Shuffle audit (RQ3)

Across {{s:n_cells}} detector and test-number cells, the false-alarm rate from the shuffle audit correlated with the true no-change rate (Spearman ρ = {{s:spearman_rho}}, 95% CI {{rq3ci}}; Fig. 3). The median absolute difference was {{s:median_abs_diff}} percentage points, and {{s:share_within_3pp}} of cells differed by 3 percentage points or less. The audit correctly identified the invalid detectors at three tests (D6: {{m:D6:3:fpr_shuffle}}; D8: {{m:D8:3:fpr_shuffle}}). The largest disagreement was {{s:max_abs_diff}} percentage points. The audit over-estimated false alarms for rules without a p-value, such as the rate rule ({{m:D2:3:fpr_shuffle}} vs {{m:D2:3:fpr_true_null}} at three tests) and event analysis ({{m:D7:6:fpr_shuffle}} vs {{m:D7:6:fpr_true_null}} at six tests), and under-estimated them for D8 at three tests. The pre-specified target of ρ ≥ 0.7 was therefore not met, In a post hoc look, every cell with a difference above 3 percentage points belonged to the rate rule, event analysis or a machine-learning model; for detectors based on a p-value, the audit was within 3 percentage points of the true rate.

## External clinic (RQ5)

In GRAPE (Table 2, Fig. 4), D1 detected {{ci:D1:3:grape_sens}} of clinician-labelled progressing eyes with three tests, at a specificity of {{ci:D1:3:grape_spec}}. The rate rule (D2) and the transferred tabular model (D8) detected more progressing eyes ({{m:D2:3:grape_sens}} and {{m:D8:3:grape_sens}}), but neither gain was significant after correction (Holm p = {{ph:D2:3:gsens}} and {{ph:D8:3:gsens}}, respectively){{check:ns:D2:3:gsens}}{{check:ns:D8:3:gsens}}. Both flagged significantly more non-progressing eyes ({{pp:D2:3:gfp}} and {{pp:D8:3:gfp}}; both Holm p {{ph:D8:3:gfp}}){{check:sig:D2:3:gfp}}{{check:sig:D8:3:gfp}}. PoPLR, the pointwise rule and event analysis were less sensitive than D1 at three tests{{check:sig:D3:3:gsens}}{{check:sig:D4:3:gsens}}{{check:sig:D7:3:gsens}}. The pattern was the same at four tests: no significant sensitivity gain, but more false positives for D2 and D8{{check:ns:D2:4:gsens}}{{check:ns:D8:4:gsens}}{{check:sig:D2:4:gfp}}{{check:sig:D8:4:gfp}}.

## Real-world measures

At three tests, D6 would produce about {{ff:D6:3}} false progression flags per 1,000 stable eyes and D8 about {{ff:D8:3}}, compared with {{ff:D1:3}} for D1 (Table 3). Followed to six tests, D1 flagged {{rw:D1:prog_detected_by_6}} of reference progressors, at a median of the {{rw:D1:prog_median_first_k_detected}}th test among those flagged. D6 and D8 flagged {{rw:D6:prog_detected_by_6}} and {{rw:D8:prog_detected_by_6}}, but at the cost of the false-alarm rates above.

# Discussion

We built an open benchmark for a simple clinical question: can visual field progression be detected earlier without raising false alarms? Using a true no-change arm, a future-confirmed reference and an external clinic, we compared ten detectors at three to six tests. The one detector that significantly beat a simple trend test did so by raising false alarms in more than one in five no-change series{{check:gt:D6:3:fpr_true_null:0.2}}. No valid detector beat the simple trend test. The usual way of estimating specificity, against reference-stable eyes, did not reveal the problem. A shuffle audit did.

Why did reference-stable eyes miss the false alarms? Stable eyes in a future-reference design are selected because their whole series shows no trend. Such eyes are likely to have low test–retest variability, so they rarely produce chance trends in their first few tests. True no-change data from patients with typical glaucoma and typical variability are a harder test. This matters for machine-learning studies, which usually set the threshold at a fixed specificity in reference-stable eyes [16, 17, 22]. In our data that practice gave false-alarm rates several times higher than intended. Our findings agree with the long-standing view that variability limits how early change can be confirmed [4, 8, 25, 26], and with recent work showing that progression labels strongly affect machine-learning results [22].

The development history of this study illustrates the same point. During development, a regional pooled-detrended variant (D6) appeared to give valid detection from the third test. A check on true no-change data showed that this gain was a false-alarm artefact. We kept D6 in the benchmark as a pre-specified example and report it as it performed. Permutation of residuals in a model with very few degrees of freedom is known to be fragile [30]; with three tests, a detrended series has only one residual degree of freedom.

For clinics, the practical message is modest but useful. A simple trend of mean sensitivity, tested at the 5% level, gave the best balance of earlier detection and false alarms in both clinics. More frequent early testing, as recommended by expert guidance [4] and supported by frontloading studies [28], is likely to help more than a more complex detector. When a new detector or commercial tool is considered, the clinic can run the shuffle audit on its own records: re-order each eye's tests at random and count how often the tool still flags progression. If this rate is well above the nominal level, the tool's extra flags are probably false alarms. For developers and reviewers, we suggest that early-detection claims should report false-alarm rates on true no-change data, or at least a shuffle audit, alongside sensitivity.

This study has limitations. First, the future-reference test set was small ({{d:uwhvf.test_ge8.n_prog}} progressors and {{d:uwhvf.test_ge8.n_stable}} stable eyes), so confidence intervals for sensitivity are wide and modest gains cannot be excluded. Second, the reference standard is based on the mean-deviation trend, which favours mean-deviation detectors; the PoPLR-based secondary reference gave the same conclusions, but no reference is free of this circularity. Third, the true no-change arm has only {{d:artes.n_patients}} patients from one centre, tested weekly; we assigned clinical test intervals from other eyes, which keeps the null valid but cannot reproduce long-term fluctuation, such as seasonal or learning effects. The arm had also been used once during development. Fourth, UWHVF lacks reliability indices and diagnoses, and GRAPE used a different perimeter, so we re-calibrated two detectors there and did not test three others. Fifth, we did not test every published method, including Bayesian hierarchical models [9, 35], smoothing [36] and forecasting-based schedules [34]. The benchmark code is open so that these can be added. Finally, a benchmark on retrospective data cannot show whether earlier detection changes visual outcomes.

# Conclusions

In this open benchmark, the only significant early-detection gain over a simple trend test was explained by false alarms that conventional specificity estimates did not reveal. A simple trend test remained hard to beat at three to six tests. We recommend that new progression detectors, including machine-learning tools, be evaluated on true no-change data or with a shuffle audit before clinical use, and that prospective studies test whether earlier valid detection improves outcomes.

# Declarations

**Funding.** [TO BE COMPLETED BY THE AUTHORS: state funding, or "No funding or sponsorship was received for this study or publication of this article." Include who funds the journal's publication fee.]

**Medical Writing/Editorial Assistance.** [TO BE COMPLETED BY THE AUTHORS. An AI assistant (Claude, Anthropic) was used for code, analysis and drafting under author supervision; disclose according to journal policy.]

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

CI, confidence interval (patient-cluster bootstrap, 2,000 resamples); GRU, gated recurrent unit; ML, machine learning; OLS-MD, ordinary least-squares trend of mean sensitivity; PLR, pointwise linear regression; PoPLR, permutation of pointwise linear regression. Valid: lower confidence limit of the true no-change false-alarm rate ≤5% and upper limit ≤10%. n = 26 progressors and 26 stable eyes for sensitivity and specificity.

**Table 2** External clinic (GRAPE): detection of clinician-labelled progression (mean-deviation criterion) from the first three or four tests

{{TABLE2}}

pp, percentage points; Holm p, exact McNemar test with Holm correction within each number of tests. D6, D9 and D10 use the 24-2 grid and were not applied (protocol amendment A2). At four tests only eyes with four or more tests were included.

**Table 3** Real-world measures: expected false progression flags and timing of first detection

{{TABLE3}}

False flags per 1,000 stable eyes = false-alarm rate on true no-change data × 1,000, per detection opportunity. *Among reference progressors flagged by test 6 (UWHVF test set, n = 26 progressors, 26 stable eyes); flags are evaluated at tests 3, 4, 5 and 6.
