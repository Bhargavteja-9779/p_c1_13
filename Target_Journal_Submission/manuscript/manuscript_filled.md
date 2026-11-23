# Early Detection of Glaucomatous Visual Field Progression Without False Alarms: A Benchmark With True No-Change Data

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, DEGREES AND ORCID IDS – TO BE COMPLETED BY THE AUTHORS]

**Affiliations:** [TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, POSTAL ADDRESS, EMAIL – TO BE COMPLETED BY THE AUTHORS]

**Running title:** False alarms in early visual field progression detection

# Abstract

**Introduction:** New methods for detecting glaucomatous visual field progression often flag more eyes than simple trend tests, but extra flags can be false alarms. We asked whether any detector finds progression earlier than a simple trend test without false alarms above the nominal level on data where no change is possible.

**Methods:** We compared ten detectors (trend, event, permutation, conformal and machine-learning; three were our own development variants) using only the first 3–6 tests of each series. Sensitivity and specificity were measured in University of Washington test-set eyes against a reference based on each eye's full follow-up (26 progressors, 26 stable eyes). False alarms were measured on 12-week retest series of 30 patients with glaucoma (true no change). External testing used 263 eyes from a clinic in China. The comparator was the least-squares trend of mean sensitivity (OLS-MD).

**Results:** At three tests, OLS-MD detected 19.2% (95% CI 7.4–33.3%) of progressors with 4.4% false alarms. The only significantly more sensitive detector, a pooled-detrended conformal variant from our development work (+38.5 percentage points [95% CI 19.4 to 57.7]), raised 22.4% false alarms, although its specificity against the full-series reference was 96.2%. Gradient-boosted trees thresholded at 95% specificity gave 27.7%, 9.4% and 18.8% false alarms at 3–5 tests. No detector without excess false alarms beat OLS-MD significantly, but the study could only detect differences of about 35 percentage points. A shuffle audit did not meet its pre-specified agreement target (Spearman ρ = 0.65). Externally, higher sensitivity again came with more false positives.

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

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [4]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [5], but routine care rarely reaches this frequency. Delays in follow-up are a documented cause of avoidable sight loss [6].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [7, 8]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [9–11]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [7]. Bayesian and spatial models share information across locations or patients [12–14]. More recently, machine-learning models have been trained to classify or forecast progression [15–20], and some newer studies use deep generative models or risk-based test scheduling [21, 22].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [9]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [23]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

We built an open benchmark to answer one practical question: how early can visual-field progression be detected without raising false alarms? The benchmark has a true no-change arm, a future-confirmed reference standard, and an external clinic. We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We hypothesised that no detector would flag substantially more future-confirmed progressors than the simple trend test of mean sensitivity while keeping a valid false-alarm rate on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate.

# Methods

## Study design and reporting

This was a retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [24]. The analysis plan, including all ten detectors, thresholds, reference standards and statistical tests, was written down and time-stamped in version control before the final analysis (code repository, `experiments/protocol.md`); it was not registered in a public registry. Two amendments were made before any final result was seen; both are reported below. Before the final run, a pipeline check ("quick mode", models trained on a subset of the development data) was also run on the Artes and GRAPE data; its output was not used for any decision, but these data were therefore not entirely unseen. Ideas that we developed and abandoned during the study, and all deviations from the plan, are listed in the Supplementary Material. Three detectors (D5, D6, D10) are our own development variants; D6 had already shown a high false-alarm rate on the Artes data during development and is included as a pre-specified example of an over-sensitive detector, not as a new method.

## Data sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains 28,943 24-2 tests from 7,428 eyes of 3,871 patients seen in routine care [25]. It includes sensitivities, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. The test set was used once, for the final analysis.

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [9]. Glaucoma does not change in 12 weeks in a measurable way, so any "progression" flag in these series is a false alarm. The data are distributed with the visualFields R package (version 1.0.7). We had used these data once during method development, only to check false-alarm rates of development variants; this is disclosed because it means the no-change arm was not fully unseen.

*GRAPE (external clinic).* The GRAPE data set contains 1,115 visual-field records from 263 eyes of 144 patients with glaucoma followed in Hangzhou, China [26]. Fields were measured with a different perimeter, and each eye carries progression labels computed by the data set authors with three criteria applied to the whole series (mean deviation, and two pointwise linear regression rules). We used the mean-deviation label as the primary label. Because these labels are computed from the same tests that the detectors see when an eye has only three or four visits, we repeated the analysis in eyes with at least two visits beyond those seen by the detectors (post hoc).

## Reference standard (UWHVF)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5. Other eyes were excluded from the sensitivity and specificity analysis. Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations), which is not tied to mean deviation. Both references use the whole series, including the first k tests seen by the detectors, and "stable" (one-sided p > 0.5) implies a non-negative full-series slope; specificity against this reference is therefore expected to be high by design. After peer review we added a post hoc future-only reference, computed only from tests after the first k (at least five later tests), with the same progression rule and two definitions of stable (p > 0.5; or no evidence of progression).

## Detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 OLS-MD:** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD rate:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [7], using all possible orders of the k tests.
- **D5 pooled-shuffle conformal test:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of other patients in the training set, matched by number of tests and mean sensitivity (a conformal p-value [27]).
- **D6 pooled-detrended conformal regional test:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [28]. This variant was the most sensitive approach during development.
- **D7 event analysis (simplified):** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to, but not the same as, Guided Progression Analysis [11]. Because the limits come from differences between single tests while the baseline is a mean of two tests, this version is conservative.
- **D8 machine learning, tabular:** gradient-boosted trees on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set stable eyes (a common choice). Labelled development data were limited to eyes with at least eight tests, and the same validation set served for model selection and threshold setting.
- **D9 machine learning, sequence:** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 self-supervised order network:** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [29].

Stochastic detectors (D4–D6, D8–D10) were run with five seeds.

## Evaluation

*E1 future reference.* In UWHVF test-set eyes with at least eight tests, we measured sensitivity (share of reference progressors flagged) and specificity (share of reference stable eyes not flagged) using only the first k tests.

*E2 true no-change.* In the Artes data we took every window of k consecutive tests. Because rate-based rules depend on the time scale, each window was given the test dates of a randomly chosen UWHVF test-set eye (ten draws per window; amendment A1). The share of windows flagged is the false-alarm rate.

*E3 shuffle audit.* In UWHVF test-set eyes, we randomly re-ordered the first k tests (ten times) and re-ran each detector. Shuffling removes any true trend, so the flag rate estimates the false-alarm rate without retest data.

*E4 external clinic.* In GRAPE, we applied the detectors to the first three or four tests of each eye and compared flags with the progression labels supplied with the data set. D5 and D7 were re-calibrated on GRAPE itself by five-fold patient-level cross-fitting, because the perimeter differs; D8 was transferred unchanged from UWHVF; the 24-2-specific detectors (D6, D9, D10) were not applied (amendment A2).

## Statistical analysis

Stochastic detectors were summarised by the mean flag over seeds; for paired tests we used the majority flag over seeds, and we report the between-seed standard deviation. Proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. We compared each detector with D1 on the same eyes using the exact McNemar test and corrected p-values for the nine comparisons within each number of tests with the Holm method. The McNemar test treats eyes as independent; confidence intervals for paired differences use the patient-cluster bootstrap. With 26 progressors, a difference needs at least 9 discordant eyes in one direction (about 35 percentage points) to reach Holm-adjusted significance, so RQ2 is mainly an estimation question. The protocol stated that the upper confidence limit of the false-alarm rate on true no-change data would be compared with 5%, without a fixed rule. We report three readings: (i) false alarms significantly above the nominal 5% (lower confidence limit above 5%); (ii) the rule written in our manuscript draft before the final results, but after the pipeline check (lower limit at or below 5% and upper limit at or below 10%); and (iii) the strict reading (upper limit at or below 5%). With 30 patients, the strict reading cannot be met even by a detector with an exact 5% rate, so we base conclusions on reading (i) and report where they change under the others. We call a detector "over-sensitive" when reading (i) applies. Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells and by their absolute difference, with a bootstrap confidence interval for the correlation (2,000 resamples of cells). We also report two pre-specified real-world measures: the expected number of false progression flags per 1,000 stable eyes at each detection opportunity (the true no-change false-alarm rate times 1,000), and, among reference progressors, the number of tests at which a detector first flagged the eye. Analyses used Python 3.13 with NumPy, SciPy, scikit-learn, LightGBM and PyTorch. An AI assistant (Claude, Anthropic) was used to write analysis code and draft text; [THE AUTHORS MUST STATE HOW THEY VERIFIED THE CODE AND ANALYSES].

## Ethics

This study used only publicly available, de-identified data sets released by their custodians under open licences (UWHVF: BSD-3; GRAPE: CC0; Artes data: distributed with the visualFields R package). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

# Results

## Study sample

The UWHVF test set contained 869 eyes of 457 patients with at least three tests; these eyes were used for the shuffle audit. Of the 132 test-set eyes with at least eight tests, 26 were reference progressors, 26 were reference stable and 80 were indeterminate and excluded. The 52 reference eyes came from 41 patients. Their median age at the first test was 58.8 years, median baseline mean total deviation was −4.4 dB, and they had a median of 11 tests over 12.9 years (median interval between tests 1.0 years). Development used 2,643 training and 940 validation eyes. The Artes data gave 300, 270, 240 and 210 no-change windows of 3, 4, 5 and 6 tests. In GRAPE, eyes had a median of 4 visits over 2.3 years; 27 eyes were labelled as progressing by the mean-deviation criterion, and 163 eyes had four or more tests.

## False alarms on true no-change data (RQ1)

Table 1 and Fig. 2 show all results. The simple trend test (D1) had false-alarm rates between 3.8% and 5.1% across 3–6 tests, for example 4.4% (95% CI 2.8–6.3%) at three tests. No detector based on a p-value or a fixed rule (D1–D5, D7, D10) had false alarms significantly above 5% at any number of tests. PoPLR, event analysis and the order network could not flag any eye at three tests, because three tests allow only six orderings or no confirmation test.

Three detectors had false alarms significantly above 5%. The pooled-detrended conformal test (D6) raised false alarms in 22.4% (95% CI 19.3–25.7%) of no-change windows at three tests; at 4–6 tests its rates were 5.1%, 6.2% and 7.6%. The tabular machine-learning model (D8) gave 27.7% (95% CI 22.7–32.9%) at three tests, 9.4% (95% CI 6.3–12.9%) at four and 18.8% (95% CI 13.1–24.9%) at five. The sequence model (D9) gave 12.7% (95% CI 6.2–20.0%) at three tests. Under the stricter readings of validity, more cells failed, including D1 at every number of tests under the strict reading (Table 1); the conclusions below about D6, D8 and D9 hold under all three readings.

Specificity against the full-series reference hardly separated these detectors from D1: at three tests D6 had a specificity of 96.2% and D8 94.6%, against 96.2% for D1. In the post hoc future-only reference, built from later tests only (17 progressors and 32 stable eyes at three tests), the difference appeared: specificity was 83.3% for D6 and 83.3% for D8, against 94.4% for D1 (Supplementary Table S3).

## Sensitivity compared with the simple trend test (RQ2)

At three tests D1 flagged 19.2% (95% CI 7.4–33.3%) of reference progressors. Only D6 flagged significantly more: 56.9% (95% CI 37.0–76.2%), a difference of +38.5 percentage points [95% CI 19.4 to 57.7] (discordant eyes 10 vs 0; Holm p = 0.018). The largest gain by a detector without excess false alarms at three tests came from the rate rule D2 (+19.2 percentage points [95% CI −3.4 to 41.7]; Holm p = 0.72).

At four to six tests no detector was significantly more sensitive than D1; the pointwise rule D3 was less sensitive at six tests (Holm p = 0.035). The largest point gain was D8 at six tests (+11.5 percentage points [95% CI −8.0 to 30.4]; Holm p = 1.00), where its false-alarm rate was 3.6%. Event analysis (D7) detected 50.0% at five tests against 42.3% for D1 (Holm p = 1.00). The pooled-shuffle conformal test (D5) flagged the same reference eyes as D1 at every number of tests. Our hypothesis that no detector without excess false alarms would beat D1 significantly was therefore not falsified. This is weak evidence: with 26 progressors, a difference needed about 35 percentage points to reach significance, and for several detectors the upper confidence limit of the gain exceeded 20 percentage points (for example D2 at three tests and D8 at four and six tests; Supplementary Table S2).

The secondary, PoPLR-based reference gave lower sensitivities for all detectors. At three tests D6 again had the highest sensitivity (46.2% vs 10.3% for D1). At six tests D1 detected 37.9% (95% CI 24.2–51.8%), and D6, D10 and D8 had slightly higher point estimates (43.1%, 43.1% and 42.1%; Supplementary Table S1); these differences were not tested.

## Machine-learning thresholds (RQ4)

Both supervised models were thresholded at 95% specificity on validation-set reference-stable eyes, and their specificity in test-set reference-stable eyes was at least 91.5%. Their false-alarm rates on true no-change data were D8: 27.7%, 9.4%, 18.8% and 3.6% at 3–6 tests; D9: 12.7%, 2.0%, 7.5% and 5.9%. The hypothesis that this thresholding gives too many false alarms was supported for D8 at three to five tests and for D9 at three tests, but not at six tests. The sequence model was unstable across seeds (between-seed standard deviation of sensitivity up to 13.2%; Supplementary Table S1).

## Shuffle audit (RQ3)

Across 40 detector and test-number cells, the false-alarm rate from the shuffle audit correlated with the true no-change rate (Spearman ρ = 0.65, 95% CI 0.35 to 0.85; Fig. 3), below the pre-specified target of 0.7, so H3 was not supported. The median absolute difference was 1.0 percentage points, and 80.0% of cells differed by 3 percentage points or less. The audit gave rates above 10% for D6 at three tests (22.5%) and D8 at three and five tests (17.3%, 16.1%), but also for the rate rule at three tests (11.7% vs 2.6% on true no-change data) and event analysis at six tests (11.7% vs 1.9%). It did not flag D6 at six tests (4.9% vs 7.6%). In a post hoc look, every cell with a difference above 3 percentage points belonged to the rate rule, event analysis or a machine-learning model.

## External clinic (RQ5)

In GRAPE (Table 2, Fig. 4), D1 detected 44.4% (95% CI 25.9–65.4%) of eyes labelled as progressing with three tests, at a specificity of 95.3% (95% CI 92.2–97.9%). The rate rule (D2) and the transferred tabular model (D8) detected more progressing eyes (59.3% and 65.9%), but neither gain was significant after correction (Holm p = 0.78 and 0.28, respectively). Both flagged significantly more non-progressing eyes (+16.5 percentage points [95% CI 11.0 to 22.2] and +33.5 percentage points [95% CI 27.4 to 40.3]; both Holm p <0.001). PoPLR, the pointwise rule and event analysis were less sensitive than D1 at three tests. At four tests, D2 and D8 again flagged more non-progressing eyes without a significant sensitivity gain. In the post hoc analysis restricted to eyes with at least five visits (88 eyes, 13 progressing), sensitivity at three tests was 23.1% for D1, 46.2% for D2 and 69.2% for D8, with specificity 93.3%, 77.3% and 62.7% (Supplementary Table S4). D6, D9 and D10 could not be tested in GRAPE, and GRAPE has no no-change arm.

## Real-world measures

At three tests, D6 would produce about 224 false progression flags per 1,000 stable eyes and D8 about 277, compared with 44 for D1 (Table 3). Followed to six tests, D1 flagged 69.2% of reference progressors, at a median of the 4th test among those flagged. D6 and D8 flagged 76.9% and 76.9%. These figures are per detection opportunity; repeated looks in the same eye accumulate false alarms.

# Discussion

We built an open benchmark for a simple clinical question: can visual field progression be detected earlier without raising false alarms? Using a true no-change arm, a future-confirmed reference and an external clinic, we compared ten detectors at three to six tests. Every significant sensitivity gain over a simple trend test came with false alarms well above the nominal level. No detector without excess false alarms beat the simple trend test, but the study was too small to exclude moderate gains.

Two findings deserve emphasis. First, the over-sensitive detectors included one of our own development variants (D6) and a machine-learning model thresholded in a common way (D8). The behaviour of D6 was already known to us from development, so its inclusion is an illustration rather than an independent discovery. The machine-learning result is more general: a threshold set at 95% specificity in reference-stable eyes gave false-alarm rates of 27.7% to 18.8% at three to five tests on true no-change data. Second, specificity against the conventional full-series reference did not reveal either problem. This is partly by design: "stable" eyes in such references have a non-negative trend over their whole series, which includes the tests the detector sees. When we built a reference from later tests only, the specificity of the over-sensitive detectors fell below that of the trend test. Evaluations that use full-series references should therefore not be read as evidence of a low false-alarm rate. Our findings agree with the view that test–retest variability limits how early change can be confirmed [4, 5, 30, 31], and with recent work showing that progression labels strongly affect machine-learning results [23].

Comparing a detector on the eye's real test order with shuffled orders is not new; it is the basis of PoPLR [7], and retest data have been used before to check the specificity of event analysis [9]. Our shuffle audit applies the same idea to any detector. It did not meet our agreement target, and it over-flagged rules without a p-value, so it is a screening tool, not a substitute for true no-change data.

For clinics, the practical message is modest. In our data a simple trend of mean sensitivity, tested at the 5% level, was not beaten by any detector without excess false alarms. A detector that flags many more eyes than this should be treated with caution until its false-alarm rate on no-change data is known. For developers and reviewers, we suggest that early-detection claims should report false-alarm rates on true no-change data alongside sensitivity, and that thresholds should not be set only against full-series reference-stable eyes.

This study has limitations. First, the future-reference test set was small (26 progressors and 26 stable eyes), so confidence intervals are wide; the McNemar test also treats the two eyes of a patient as independent. Second, the reference standards use the full series and favour mean-deviation detectors; the post hoc future-only reference had even fewer progressors. Third, the true no-change arm has only 30 patients from one centre, tested weekly. Weekly retests do not contain long-term fluctuation, so rate-based rules may look more valid than they would be in routine care; our assignment of clinical test intervals keeps the null valid but cannot add this variability. The arm had also been used during development and in a pipeline check. Fourth, the machine-learning models were trained on a few hundred labelled eyes and thresholded on the same validation set used for model selection; larger models trained on more data may behave differently. Fifth, GRAPE used a different perimeter and criterion-based labels computed from the same tests in eyes with few visits; three detectors could not be tested there, and the transferred machine-learning model faced a change in measurement scale. Sixth, our event analysis is a simplified, conservative version of Guided Progression Analysis, and we did not test the Visual Field Index, ANSWERS or other Bayesian hierarchical models [12, 14], smoothing [32] or forecasting-based schedules [33]. The benchmark code is open so that these can be added. Finally, a retrospective benchmark cannot show whether earlier detection changes visual outcomes.

# Conclusions

In this open benchmark, every significant early-detection gain over a simple trend test came with false alarms above the nominal level, and specificity against a full-series reference did not reveal this. A simple trend test was not clearly beaten at three to six tests, although the study was too small to exclude moderate gains. New progression detectors, including machine-learning tools, should be evaluated on true no-change data before clinical use, and prospective studies should test whether earlier valid detection improves outcomes.

# Declarations

**Funding.** [TO BE COMPLETED BY THE AUTHORS: state funding, or "No funding or sponsorship was received for this study or publication of this article." Include who funds the journal's publication fee.]

**Medical Writing/Editorial Assistance.** An AI assistant (Claude, Anthropic) was used to write analysis code and draft the manuscript (see Methods). [THE AUTHORS MUST CONFIRM AND DESCRIBE THEIR VERIFICATION, AND COMPLETE ANY OTHER ASSISTANCE.]

**Author Contributions.** [TO BE COMPLETED BY THE AUTHORS (CRediT roles).]

**Conflict of Interest.** [TO BE COMPLETED BY THE AUTHORS.]

**Ethical Approval.** This study used only publicly available, de-identified data sets released by their custodians under open licences (UWHVF: BSD-3; GRAPE: CC0; Artes retest data: distributed with the visualFields R package). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

**Data Availability.** All data are public: UWHVF (https://github.com/uw-biomedical-ml/uwhvf), GRAPE (figshare, DOI in reference [26]) and the Artes retest data (visualFields R package 1.0.7 on CRAN). All code, the pre-registered protocol, raw per-eye results and the patient-level split are available at [REPOSITORY URL – TO BE COMPLETED BY THE AUTHORS BEFORE SUBMISSION].

# References

1. Tham YC, Li X, Wong TY, Quigley HA, Aung T, Cheng CY. Global Prevalence of Glaucoma and Projections of Glaucoma Burden through 2040. Ophthalmology. 2014;121(11):2081-2090. https://doi.org/10.1016/j.ophtha.2014.05.013
2. Weinreb RN, Aung T, Medeiros FA. The Pathophysiology and Treatment of Glaucoma. JAMA. 2014;311(18):1901. https://doi.org/10.1001/jama.2014.3192
3. Heijl A. Reduction of Intraocular Pressure and Glaucoma Progression. Arch Ophthalmol. 2002;120(10):1268. https://doi.org/10.1001/archopht.120.10.1268
4. Gardiner SK, Swanson WH, Goren D, Mansberger SL, Demirel S. Assessment of the Reliability of Standard Automated Perimetry in Regions of Glaucomatous Damage. Ophthalmology. 2014;121(7):1359-1369. https://doi.org/10.1016/j.ophtha.2014.01.020
5. Chauhan BC, Garway-Heath DF, Goni FJ, Rossetti L, Bengtsson B, Viswanathan AC, et al. Practical recommendations for measuring rates of visual field change in glaucoma. British Journal of Ophthalmology. 2008;92(4):569-573. https://doi.org/10.1136/bjo.2007.135012
6. Foot B, MacEwen C. Surveillance of sight loss due to delay in ophthalmic treatment or review: frequency, cause and outcome. Eye. 2017;31(5):771-775. https://doi.org/10.1038/eye.2017.1
7. O'Leary N, Chauhan BC, Artes PH. Visual Field Progression in Glaucoma: Estimating the Overall Significance of Deterioration with Permutation Analyses of Pointwise Linear Regression (PoPLR). Invest. Ophthalmol. Vis. Sci.. 2012;53(11):6776. https://doi.org/10.1167/iovs.12-10049
8. Bengtsson B, Heijl A. A Visual Field Index for Calculation of Glaucoma Rate of Progression. American Journal of Ophthalmology. 2008;145(2):343-353. https://doi.org/10.1016/j.ajo.2007.09.038
9. Artes PH, O'Leary N, Nicolela MT, Chauhan BC, Crabb DP. Visual Field Progression in Glaucoma. Ophthalmology. 2014;121(10):2023-2027. https://doi.org/10.1016/j.ophtha.2014.04.015
10. Wu Z, Medeiros FA. Comparison of Visual Field Point-Wise Event-Based and Global Trend-Based Analysis for Detecting Glaucomatous Progression. Trans. Vis. Sci. Tech.. 2018;7(4):20. https://doi.org/10.1167/tvst.7.4.20
11. Heijl A, Bengtsson B, Chauhan BC, Lieberman MF, Cunliffe I, Hyman L, et al. A Comparison of Visual Field Progression Criteria of 3 Major Glaucoma Trials in Early Manifest Glaucoma Trial Patients. Ophthalmology. 2008;115(9):1557-1565. https://doi.org/10.1016/j.ophtha.2008.02.005
12. Zhu H, Crabb DP, Ho T, Garway-Heath DF. More Accurate Modeling of Visual Field Progression in Glaucoma: ANSWERS. Invest. Ophthalmol. Vis. Sci.. 2015;56(10):6077. https://doi.org/10.1167/iovs.15-16957
13. Marín-Franch I, Artes PH, Turpin A, Racette L. Visual Field Progression in Glaucoma: Comparison Between PoPLR and ANSWERS. Trans. Vis. Sci. Tech.. 2021;10(14):13. https://doi.org/10.1167/tvst.10.14.13
14. Montesano G, Garway-Heath DF, Ometto G, Crabb DP. Hierarchical Censored Bayesian Analysis of Visual Field Progression. Trans. Vis. Sci. Tech.. 2021;10(12):4. https://doi.org/10.1167/tvst.10.12.4
15. Saeedi O, Boland MV, D'Acunto L, Swamy R, Hegde V, Gupta S, et al. Development and Comparison of Machine Learning Algorithms to Determine Visual Field Progression. Trans. Vis. Sci. Tech.. 2021;10(7):27. https://doi.org/10.1167/tvst.10.7.27
16. Dixit A, Yohannan J, Boland MV. Assessing Glaucoma Progression Using Machine Learning Trained on Longitudinal Visual Field and Clinical Data. Ophthalmology. 2021;128(7):1016-1026. https://doi.org/10.1016/j.ophtha.2020.12.020
17. Wang M, Shen LQ, Pasquale LR, Petrakos P, Formica S, Boland MV, et al. An Artificial Intelligence Approach to Detect Visual Field Progression in Glaucoma Based on Spatial Pattern Analysis. Invest. Ophthalmol. Vis. Sci.. 2019;60(1):365. https://doi.org/10.1167/iovs.18-25568
18. Wen JC, Lee CS, Keane PA, Xiao S, Rokem AS, Chen PP, et al. Forecasting future Humphrey Visual Fields using deep learning. PLoS ONE. 2019;14(4):e0214875. https://doi.org/10.1371/journal.pone.0214875
19. Berchuck SI, Mukherjee S, Medeiros FA. Estimating Rates of Progression and Predicting Future Visual Fields in Glaucoma Using a Deep Variational Autoencoder. Sci Rep. 2019;9(1). https://doi.org/10.1038/s41598-019-54653-6
20. Yousefi S, Balasubramanian M, Goldbaum MH, Medeiros FA, Zangwill LM, Weinreb RN, et al. Unsupervised Gaussian Mixture-Model With Expectation Maximization for Detecting Glaucomatous Progression in Standard Automated Perimetry Visual Fields. Trans. Vis. Sci. Tech.. 2016;5(3):2. https://doi.org/10.1167/tvst.5.3.2
21. Chen L, Fujita A, Moradi M, Eslami M, Elze T, Zebardast N. Earlier confirmation of glaucoma progression with risk-weighted visual field and OCT scheduling. medRxiv. 2026. https://doi.org/10.64898/2026.11.16.26368187
22. Si W, Lin V, Sun B, Jang KJ, Xing R, Saeed A, et al. Reliable and Interpretable Visual Field Progression Prediction with Diffusion Models and Conformal Risk Control. Lecture Notes in Computer Science. 2025:543-552. https://doi.org/10.1007/978-3-032-05182-0_53
23. Kim H, Kim E, Moon S, Jin SW, Kim JL, Lee SU, et al. Labeling matters: A multicenter machine learning study on visual field progression in Glaucoma. PLoS One. 2026;21(8):e0357179. https://doi.org/10.1371/journal.pone.0357179
24. Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378
25. Montesano G, Chen A, Lu R, Lee CS, Lee AY. UWHVF: A Real-World, Open Source Dataset of Perimetry Tests From the Humphrey Field Analyzer at the University of Washington. Trans. Vis. Sci. Tech.. 2022;11(1):2. https://doi.org/10.1167/tvst.11.1.1
26. Huang X, Kong X, Shen Z, Ouyang J, Li Y, Jin K, et al. GRAPE: A multi-modal dataset of longitudinal follow-up visual field and fundus images for glaucoma management. Sci Data. 2023;10(1). https://doi.org/10.1038/s41597-023-02424-4
27. Angelopoulos AN, Bates S. Conformal Prediction: A Gentle Introduction. Foundations and Trends® in Machine Learning. 2023;16(4):494-591. https://doi.org/10.1561/2200000101
28. Freedman D, Lane D. A Nonstochastic Interpretation of Reported Significance Levels. Journal of Business & Economic Statistics. 1983;1(4):292-298. https://doi.org/10.1080/07350015.1983.10509354
29. Gagnon-Bartsch J, Shem-Tov Y. The classification permutation test: A flexible approach to testing for covariate imbalance in observational studies. Ann. Appl. Stat.. 2019;13(3):1464-1483. https://doi.org/10.1214/19-aoas1241
30. Wu Z, Saunders LJ, Daga FB, Diniz-Filho A, Medeiros FA. Frequency of Testing to Detect Visual Field Progression Derived Using a Longitudinal Cohort of Glaucoma Patients. Ophthalmology. 2017;124(6):786-792. https://doi.org/10.1016/j.ophtha.2017.01.027
31. Crabb DP, Garway-Heath DF. Intervals between Visual Field Tests When Monitoring the Glaucomatous Patient: Wait-and-See Approach. Invest. Ophthalmol. Vis. Sci.. 2012;53(6):2770. https://doi.org/10.1167/iovs.12-9476
32. Mohammadzadeh V, Li L, Fei Z, Davis T, Morales E, Wu K, et al. Efficacy of Smoothing Algorithms to Enhance Detection of Visual Field Progression in Glaucoma. Ophthalmology Science. 2024;4(2):100423. https://doi.org/10.1016/j.xops.2023.100423
33. Schell GJ, Lavieri MS, Helm JE, Liu X, Musch DC, Van Oyen MP, et al. Using Filtered Forecasting Techniques to Determine Personalized Monitoring Schedules for Patients with Open-Angle Glaucoma. Ophthalmology. 2014;121(8):1539-1546. https://doi.org/10.1016/j.ophtha.2014.02.021

# Tables

**Table 1** Sensitivity and specificity against the future reference (UWHVF test set) and false-alarm rates on true no-change data (Artes retest) and in the shuffle audit, by number of tests

| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | False alarms, true no-change, % (95% CI) | False alarms, shuffle audit, % | Above 5% (i) / rule (ii) / strict (iii) |
|---|---|---|---|---|---|---|
| 3 | D1 OLS-MD | 19.2 (7.4–33.3) | 96.2 (87.0–100.0) | 4.4 (2.8–6.3) | 4.8 | No / met / not met |
| 3 | D2 MD rate | 38.5 (20.0–56.5) | 92.3 (80.0–100.0) | 2.6 (1.5–3.9) | 11.7 | No / met / met |
| 3 | D3 PLR-3 | 3.8 (0.0–12.5) | 96.2 (88.0–100.0) | 1.4 (1.0–1.8) | 1.8 | No / met / met |
| 3 | D4 PoPLR | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | No / met / met |
| 3 | D5 Pooled-shuffle conformal | 19.2 (7.4–33.3) | 96.2 (87.0–100.0) | 4.0 (2.7–5.6) | 4.6 | No / met / not met |
| 3 | D6 Pooled-detrended conformal | 56.9 (37.0–76.2) | 96.2 (87.0–100.0) | 22.4 (19.3–25.7) | 22.5 | **Yes** / not met / not met |
| 3 | D7 Event analysis | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | No / met / met |
| 3 | D8 ML tabular | 26.2 (12.3–43.2) | 94.6 (84.8–100.0) | 27.7 (22.7–32.9) | 17.3 | **Yes** / not met / not met |
| 3 | D9 ML sequence (GRU) | 12.3 (2.4–24.8) | 95.4 (88.8–100.0) | 12.7 (6.2–20.0) | 8.5 | **Yes** / not met / not met |
| 3 | D10 Self-supervised order | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | No / met / met |
| 4 | D1 OLS-MD | 30.8 (14.3–48.1) | 100.0 (100.0–100.0) | 3.8 (1.9–6.2) | 4.7 | No / met / not met |
| 4 | D2 MD rate | 23.1 (8.0–40.0) | 96.2 (87.5–100.0) | 0.6 (0.4–0.9) | 6.4 | No / met / met |
| 4 | D3 PLR-3 | 15.4 (3.6–30.8) | 100.0 (100.0–100.0) | 0.2 (0.0–0.3) | 1.5 | No / met / met |
| 4 | D4 PoPLR | 3.8 (0.0–12.5) | 100.0 (100.0–100.0) | 3.3 (1.8–4.9) | 4.1 | No / met / met |
| 4 | D5 Pooled-shuffle conformal | 30.8 (14.3–48.1) | 100.0 (100.0–100.0) | 3.6 (1.8–5.9) | 4.9 | No / met / not met |
| 4 | D6 Pooled-detrended conformal | 25.4 (10.3–44.0) | 100.0 (100.0–100.0) | 5.1 (3.4–7.2) | 5.5 | No / met / not met |
| 4 | D7 Event analysis | 23.1 (7.7–40.0) | 100.0 (100.0–100.0) | 1.1 (0.0–2.6) | 5.2 | No / met / met |
| 4 | D8 ML tabular | 41.5 (23.7–59.2) | 99.2 (97.4–100.0) | 9.4 (6.3–12.9) | 7.7 | **Yes** / not met / not met |
| 4 | D9 ML sequence (GRU) | 11.5 (2.8–23.2) | 99.2 (97.6–100.0) | 2.0 (0.6–3.7) | 4.7 | No / met / met |
| 4 | D10 Self-supervised order | 20.0 (7.7–35.8) | 100.0 (100.0–100.0) | 3.8 (2.5–5.1) | 4.1 | No / met / not met |
| 5 | D1 OLS-MD | 42.3 (23.1–61.5) | 100.0 (100.0–100.0) | 4.7 (2.2–7.5) | 5.1 | No / met / not met |
| 5 | D2 MD rate | 23.1 (7.7–41.4) | 100.0 (100.0–100.0) | 0.8 (0.5–1.2) | 3.6 | No / met / met |
| 5 | D3 PLR-3 | 23.1 (8.0–40.0) | 100.0 (100.0–100.0) | 0.5 (0.1–1.1) | 1.4 | No / met / met |
| 5 | D4 PoPLR | 38.5 (20.0–57.7) | 100.0 (100.0–100.0) | 3.9 (1.9–6.2) | 4.3 | No / met / not met |
| 5 | D5 Pooled-shuffle conformal | 42.3 (23.1–61.5) | 100.0 (100.0–100.0) | 4.3 (2.0–7.1) | 4.9 | No / met / not met |
| 5 | D6 Pooled-detrended conformal | 31.5 (16.0–48.5) | 100.0 (100.0–100.0) | 6.2 (3.7–8.9) | 5.0 | No / met / not met |
| 5 | D7 Event analysis | 50.0 (30.4–69.6) | 100.0 (100.0–100.0) | 1.2 (0.0–2.9) | 7.9 | No / met / met |
| 5 | D8 ML tabular | 56.2 (36.1–74.8) | 99.2 (97.6–100.0) | 18.8 (13.1–24.9) | 16.1 | **Yes** / not met / not met |
| 5 | D9 ML sequence (GRU) | 40.8 (22.8–59.2) | 93.8 (82.4–100.0) | 7.5 (2.8–13.3) | 8.1 | No / not met / not met |
| 5 | D10 Self-supervised order | 43.8 (28.0–60.0) | 100.0 (100.0–100.0) | 5.1 (2.9–7.6) | 4.2 | No / met / not met |
| 6 | D1 OLS-MD | 57.7 (38.4–76.9) | 100.0 (100.0–100.0) | 5.1 (2.5–8.1) | 5.9 | No / met / not met |
| 6 | D2 MD rate | 23.1 (8.3–38.5) | 100.0 (100.0–100.0) | 1.0 (0.6–1.5) | 2.8 | No / met / met |
| 6 | D3 PLR-3 | 23.1 (7.7–41.7) | 100.0 (100.0–100.0) | 0.3 (0.0–0.8) | 1.2 | No / met / met |
| 6 | D4 PoPLR | 50.0 (30.8–67.9) | 100.0 (100.0–100.0) | 5.0 (2.4–8.4) | 4.8 | No / met / not met |
| 6 | D5 Pooled-shuffle conformal | 56.9 (37.7–76.0) | 100.0 (100.0–100.0) | 5.0 (2.4–7.9) | 5.0 | No / met / not met |
| 6 | D6 Pooled-detrended conformal | 53.8 (37.0–71.4) | 100.0 (100.0–100.0) | 7.6 (4.5–11.1) | 4.9 | No / not met / not met |
| 6 | D7 Event analysis | 57.7 (36.0–77.8) | 100.0 (100.0–100.0) | 1.9 (0.5–3.8) | 11.7 | No / met / met |
| 6 | D8 ML tabular | 70.8 (51.7–88.8) | 100.0 (100.0–100.0) | 3.6 (1.7–6.0) | 8.7 | No / met / not met |
| 6 | D9 ML sequence (GRU) | 37.7 (22.3–53.8) | 91.5 (75.2–100.0) | 5.9 (2.3–10.0) | 8.6 | No / not met / not met |
| 6 | D10 Self-supervised order | 54.6 (36.9–70.8) | 99.2 (97.6–100.0) | 5.7 (3.0–9.2) | 4.7 | No / met / not met |

CI, confidence interval (patient-cluster bootstrap, 2,000 resamples); GRU, gated recurrent unit; ML, machine learning; OLS-MD, ordinary least-squares trend of mean sensitivity; PLR, pointwise linear regression; PoPLR, permutation of pointwise linear regression. Validity readings for the true no-change false-alarm rate: (i) lower 95% confidence limit above 5% (false alarms significantly above nominal); (ii) lower limit ≤5% and upper limit ≤10%; (iii) upper limit ≤5%. n = 26 progressors and 26 stable eyes for sensitivity and specificity; when all or no eyes were flagged the bootstrap interval is degenerate (exact Clopper–Pearson intervals in Supplementary Table S1). Specificity is against a full-series reference and is high by design (see Methods).

**Table 2** External clinic (GRAPE): detection of progression labelled by the mean-deviation criterion supplied with the data set, from the first three or four tests

| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | Sensitivity vs D1, pp (Holm p) | False positives vs D1, pp (Holm p) |
|---|---|---|---|---|---|
| 3 | D1 OLS-MD | 44.4 (25.9–65.4) | 95.3 (92.2–97.9) | reference | reference |
| 3 | D2 MD rate | 59.3 (40.7–76.9) | 78.8 (73.5–83.9) | +14.8 (0.78) | +16.5 (<0.001) |
| 3 | D3 PLR-3 | 3.7 (0.0–11.5) | 95.8 (92.7–98.3) | -40.7 (0.014) | -0.4 (1.00) |
| 3 | D4 PoPLR | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | -44.4 (0.003) | -4.7 (0.004) |
| 3 | D5 Pooled-shuffle conformal | 41.5 (23.8–60.0) | 95.4 (92.4–98.0) | -3.7 (1.00) | +0.0 (1.00) |
| 3 | D7 Event analysis | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | -44.4 (0.003) | -4.7 (0.004) |
| 3 | D8 ML tabular | 65.9 (50.8–80.0) | 61.2 (54.6–67.1) | +25.9 (0.28) | +33.5 (<0.001) |
| 4 | D1 OLS-MD | 33.3 (11.8–55.0) | 95.9 (92.2–98.6) | reference | reference |
| 4 | D2 MD rate | 55.6 (35.3–76.5) | 86.2 (79.4–92.1) | +22.2 (1.00) | +9.7 (0.007) |
| 4 | D3 PLR-3 | 11.1 (0.0–25.0) | 97.9 (95.2–100.0) | -22.2 (0.75) | -2.1 (1.00) |
| 4 | D4 PoPLR | 22.2 (5.9–41.2) | 95.2 (91.4–98.0) | -11.1 (1.00) | +0.7 (1.00) |
| 4 | D5 Pooled-shuffle conformal | 33.3 (11.8–55.0) | 94.5 (90.8–97.7) | +0.0 (1.00) | +1.4 (1.00) |
| 4 | D7 Event analysis | 16.7 (0.0–33.3) | 95.9 (92.4–98.7) | -16.7 (1.00) | +0.0 (1.00) |
| 4 | D8 ML tabular | 48.9 (31.8–65.9) | 81.5 (74.2–87.9) | +16.7 (1.00) | +14.5 (<0.001) |

pp, percentage points; Holm p, exact McNemar test with Holm correction within each number of tests. D6, D9 and D10 use the 24-2 grid and were not applied (protocol amendment A2). At four tests only eyes with four or more tests were included.

**Table 3** Real-world measures: expected false progression flags and timing of first detection

| Detector | False flags per 1,000 stable eyes at 3 / 4 / 5 / 6 tests | Progressors flagged by test 6, % | Median test of first flag* | Reference-stable eyes ever flagged by test 6, % |
|---|---|---|---|---|
| D1 OLS-MD | 44 / 38 / 47 / 51 | 69.2 | 4 | 3.8 |
| D2 MD rate | 26 / 6 / 8 / 10 | 46.2 | 3 | 7.7 |
| D3 PLR-3 | 14 / 2 / 5 / 3 | 38.5 | 4.5 | 3.8 |
| D4 PoPLR | 0 / 33 / 39 / 50 | 53.8 | 5 | 0.0 |
| D5 Pooled-shuffle conformal | 40 / 36 / 44 / 50 | 69.2 | 4 | 3.8 |
| D6 Pooled-detrended conformal | 224 / 51 / 62 / 76 | 76.9 | 3 | 3.8 |
| D7 Event analysis | 0 / 11 / 12 / 19 | 57.7 | 5 | 0.0 |
| D8 ML tabular | 277 / 94 / 188 / 36 | 76.9 | 4 | 3.8 |
| D9 ML sequence (GRU) | 127 / 20 / 76 / 59 | 65.4 | 5 | 7.7 |
| D10 Self-supervised order | 0 / 38 / 51 / 57 | 65.4 | 5 | 0.0 |

False flags per 1,000 stable eyes = false-alarm rate on true no-change data × 1,000, per detection opportunity. *Among reference progressors flagged by test 6 (UWHVF test set, n = 26 progressors, 26 stable eyes); flags are evaluated at tests 3, 4, 5 and 6.
