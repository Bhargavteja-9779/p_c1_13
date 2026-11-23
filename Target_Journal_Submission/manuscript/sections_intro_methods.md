# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [8]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [4], but routine care rarely reaches this frequency. Delays in follow-up are a documented cause of avoidable sight loss [5].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [6, 12]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [7, 11, 13]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [6]. Bayesian and spatial models share information across locations or patients [9, 10, 35]. More recently, machine-learning models have been trained to classify or forecast progression [16–21], and some newer studies use deep generative models or risk-based test scheduling [23, 24].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [7]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [22]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

We built an open benchmark to answer one practical question: how early can visual-field progression be detected without raising false alarms? The benchmark has a true no-change arm, a future-confirmed reference standard, and an external clinic. We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We hypothesised that no detector would flag substantially more future-confirmed progressors than the simple trend test of mean sensitivity while keeping a valid false-alarm rate on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate.

# Methods

## Study design and reporting

This was a retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [32]. The analysis plan, including all ten detectors, thresholds, reference standards and statistical tests, was written down and time-stamped before the final test data were analysed (code repository, `experiments/protocol.md`). Two amendments were made before any final result was seen; both are reported below. Ideas that we developed and abandoned during the study are listed in the Supplementary Material.

## Data sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains {{d:uw_all.n_fields:int}} 24-2 tests from {{d:uw_all.n_eyes:int}} eyes of {{d:uw_all.n_patients:int}} patients seen in routine care [14]. It includes sensitivities, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. The test set ({{d:uw_test.n_patients:int}} patients, {{d:uw_test.n_eyes_ge3:int}} eyes with at least three tests) was used once, for the final analysis.

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [7]. Glaucoma does not change in 12 weeks in a measurable way, so any "progression" flag in these series is a false alarm. The data are distributed with the visualFields R package (version 1.0.7).

*GRAPE (external clinic).* The GRAPE data set contains {{d:grape.n_records:int}} visual-field records from {{d:grape.n_eyes:int}} eyes of {{d:grape.n_patients:int}} patients with glaucoma followed in Hangzhou, China [15]. Fields were measured with a different perimeter and test grid ({{d:grape.n_points.median:int}} analysable locations per field, median), and each eye carries progression labels assigned with three criteria (mean deviation, and two pointwise linear regression rules). We used the mean-deviation label as the primary label.

## Reference standard (UWHVF)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5. Other eyes were excluded from the sensitivity and specificity analysis. Of {{d:uw_test_ge8.n_eyes:int}} test-set eyes with at least eight tests, {{d:ref_progressors.n_eyes:int}} were progressors, {{d:ref_stable.n_eyes:int}} were stable and {{d:ref_excluded_eyes:int}} were excluded. Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations), which is not tied to mean deviation.

## Detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 OLS-MD:** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD rate:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [6], using all possible orders of the k tests. With three tests there are only six orders, so the smallest possible p-value is 1/6 and D4 cannot flag at the 5% level.
- **D5 pooled-shuffle conformal test:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of other patients in the training set, matched by number of tests and mean sensitivity (a conformal p-value [31]).
- **D6 pooled-detrended conformal regional test:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [30]. This variant was the most sensitive approach during development.
- **D7 event analysis:** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to Guided Progression Analysis [13]. D7 needs at least four tests.
- **D8 machine learning, tabular:** gradient-boosted trees on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set stable eyes, as is common in machine-learning studies.
- **D9 machine learning, sequence:** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 self-supervised order network:** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [33].

Permutation p-values were computed so that they can never be zero [29]. Stochastic detectors (D4–D6, D8–D10) were run with five seeds; we report the mean over seeds and give the standard deviation across seeds in the supplementary results table. D8 and D9 had the same tuning budget (12 configurations each) and, like all other detectors, used only training and validation data.

## Evaluation

*Number of tests (k).* With routine spacing in UWHVF, the third test of reference eyes was done a median of {{d:ref_progressors.years_to_test3.median:1}} years (progressors) and {{d:ref_stable.years_to_test3.median:1}} years (stable eyes) after the first, and the sixth test a median of {{d:ref_progressors.years_to_test6.median:1}} and {{d:ref_stable.years_to_test6.median:1}} years after the first.

*E1 future reference.* In UWHVF test-set eyes with at least eight tests, we measured sensitivity (share of reference progressors flagged) and specificity (share of reference stable eyes not flagged) using only the first k tests.

*E2 true no-change.* In the Artes data we took every window of k consecutive tests. Because rate-based rules depend on the time scale, each window was given the test dates of a randomly chosen UWHVF test-set eye (ten draws per window; amendment A1). There were {{d:artes.windows.3:int}}, {{d:artes.windows.4:int}}, {{d:artes.windows.5:int}} and {{d:artes.windows.6:int}} windows for k = 3, 4, 5 and 6. The share of windows flagged is the false-alarm rate.

*E3 shuffle audit.* In UWHVF test-set eyes, we randomly re-ordered the first k tests (ten times) and re-ran each detector. Shuffling removes any true trend, so the flag rate estimates the false-alarm rate without retest data.

*E4 external clinic.* In GRAPE, we applied the detectors to the first three or four tests of each eye and compared flags with the clinicians' labels. D5 and D7 were re-calibrated on GRAPE itself by five-fold patient-level cross-fitting, because the perimeter differs; D8 was transferred unchanged from UWHVF; the 24-2-specific detectors (D6, D9, D10) were not applied (amendment A2).

## Statistical analysis

Proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. We compared each detector with D1 on the same eyes using the exact McNemar test and corrected p-values for the nine comparisons within each number of tests and endpoint with the Holm method. For stochastic detectors, the paired tests used each eye's majority flag across seeds. Confidence intervals for paired differences came from 2,000 bootstrap resamples of eyes. A detector was considered valid at a given k if, on true no-change data, the lower limit of its false-alarm confidence interval was at or below 5% (no evidence of excess false alarms) and the upper limit did not exceed 10%. To express false alarms in clinical units, we report the expected number of false progression flags per 1,000 stable eyes at one review. We also report, among reference progressors, the share flagged by the sixth test. Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells and by their absolute difference. Analyses used Python 3.13 with NumPy, SciPy, pandas, scikit-learn, LightGBM and PyTorch. The full run took {{m:runtime_min}} minutes on a 4-core CPU without a graphics card.

## Use of artificial intelligence tools

An AI assistant (Claude, Anthropic) was used to write analysis code, run the analyses, search and check the literature, and draft the text. The authors checked the code, the result files and every cited reference, and take full responsibility for the content. Every number in the text, tables and figures is inserted by a script from machine-generated result files.

## Ethics

This study used only publicly available, de-identified data sets released by their custodians under open licences (UWHVF: BSD-3; GRAPE: CC0; Artes data: distributed with the visualFields R package). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.
