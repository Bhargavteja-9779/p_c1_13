# How Early Can Glaucomatous Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, DEGREES — to be completed by the authors]

**Affiliations:** [INSTITUTION, CITY, COUNTRY — to be completed by the authors]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — to be completed by the authors]

**ORCID iDs:** [to be completed by the authors]

**Prior presentation:** [TO BE CONFIRMED BY THE AUTHORS: none.]

## Abstract

**Introduction:** New methods for detecting glaucomatous visual-field progression often claim earlier detection. Their false-alarm rates are rarely measured on series in which no change occurred. We asked whether any detector finds more progression than a simple trend test of mean sensitivity while keeping false alarms at the nominal 5%.

**Methods:** Ten pre-specified detectors (trend, pointwise, permutation, conformal, event-based and machine-learning) used only the first 3–6 tests of each series. We measured sensitivity and specificity against a future-confirmed reference in held-out eyes of the University of Washington data set (26 progressing, 26 stable eyes); false alarms on 12-week retest series of 30 patients with glaucoma; and agreement with clinician labels in an external clinic (263 eyes). We also tested whether re-running detectors on shuffled test orders (a "shuffle audit") estimates the true false-alarm rate.

**Results:** At three tests, the trend test detected 19.2% of progressing eyes with a false-alarm rate of 4.4%. The only detector significantly more sensitive than the trend test, a pooled-detrended conformal test (sensitivity 56.9%), had a false-alarm rate of 22.4%. Gradient-boosted trees, thresholded at 95% specificity, had false-alarm rates of 27.7% at three tests and 18.8% at five tests. No detector with a valid false-alarm rate was significantly more sensitive than the trend test at any number of tests. The shuffle audit agreed with true false alarms within 3 percentage points in 80% of detector–test-number cells (Spearman ρ = 0.65). Externally, gradient-boosted trees had a specificity of 61.2%, compared with 95.3% for the trend test.

**Conclusion:** Apparent gains in early detection of visual-field progression can be false alarms. A plain trend test of mean sensitivity remained as good as any valid alternative. New detectors should report false alarms on true no-change data, or at least a shuffle audit, before they guide treatment escalation.

## Keywords

Benchmark; False alarms; Glaucoma; Machine learning; Perimetry; Progression; Specificity; Visual field

## Key Summary Points

**Why carry out this study?**

- Escalating glaucoma treatment depends on detecting visual-field progression, but each test is noisy and several tests are needed, which delays decisions.
- Many new detectors claim earlier detection, yet their false-alarm rates are seldom measured on data in which the disease did not change.
- We hypothesised that no detector would flag substantially more progressing eyes than a simple trend test of mean sensitivity while keeping a valid false-alarm rate.

**What was learned from the study?**

- Across ten detectors and 3–6 tests, the only detector that flagged significantly more progressing eyes than the trend test had a false-alarm rate of 22.4%, and a machine-learning model thresholded at 95% specificity reached 27.7%.
- Clinics and developers can check false alarms with a shuffle audit of their own records, and should require true no-change evidence before trusting a claim of earlier detection.

## Plain Language Summary

Glaucoma slowly damages side vision. Doctors use a visual-field test to see if the damage is getting worse. If it is, they may add eye drops, laser or surgery. Each test result varies from day to day, so doctors need several tests before they can be sure. This can take years. Many new computer methods promise to spot worsening sooner. But a method can look better simply because it raises more false alarms. A false alarm could lead to treatment that a patient does not need. We tested ten methods on records from three sources. One source had patients tested every week for 12 weeks, when their glaucoma could not really have changed. Any alarm in these patients was false. The simplest method, which draws a straight line through the average results, worked as well as any method that kept false alarms low. Methods that found more worsening, including two machine-learning methods, also gave many more false alarms. We also tested a simple check that any clinic can run on its own records: mixing up the order of each patient's tests and seeing how often a method still raises an alarm. This check gave a fair estimate of the false-alarm rate. New methods should report their false alarms before they are used to change treatment.

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [4]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [5], but routine care rarely reaches this frequency. Delays in follow-up are a documented cause of avoidable sight loss [6].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [7, 8]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [9–11]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [7]. Bayesian and spatial models share information across locations or patients [12–14]. More recently, machine-learning models have been trained to classify or forecast progression [15–20], and some newer studies use deep generative models or risk-based test scheduling [21, 22].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [9]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [23]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

We built an open benchmark to answer one practical question: how early can visual-field progression be detected without raising false alarms? The benchmark has a true no-change arm, a future-confirmed reference standard, and an external clinic. We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We hypothesised that no detector would flag substantially more future-confirmed progressors than the simple trend test of mean sensitivity while keeping a valid false-alarm rate on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate.

# Methods

## Study design and reporting

This was a retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [24]. The analysis plan, including all ten detectors, thresholds, reference standards and statistical tests, was written down and time-stamped before the final test data were analysed (code repository, `experiments/protocol.md`). Two amendments were made before any final result was seen; both are reported below. Ideas that we developed and abandoned during the study are listed in the Supplementary Material.

## Data sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains 28,943 24-2 tests from 7,428 eyes of 3,871 patients seen in routine care [25]. It includes sensitivities, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. The test set (777 patients, 869 eyes with at least three tests) was used once, for the final analysis.

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [9]. Glaucoma does not change in 12 weeks in a measurable way, so any "progression" flag in these series is a false alarm. The data are distributed with the visualFields R package (version 1.0.7).

*GRAPE (external clinic).* The GRAPE data set contains 1,115 visual-field records from 263 eyes of 144 patients with glaucoma followed in Hangzhou, China [26]. Fields were measured with a different perimeter and test grid (59 analysable locations per field, median), and each eye carries progression labels assigned with three criteria (mean deviation, and two pointwise linear regression rules). We used the mean-deviation label as the primary label.

## Reference standard (UWHVF)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5. Other eyes were excluded from the sensitivity and specificity analysis. Of 132 test-set eyes with at least eight tests, 26 were progressors, 26 were stable and 80 were excluded. Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations), which is not tied to mean deviation.

## Detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 OLS-MD:** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD rate:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [7], using all possible orders of the k tests. With three tests there are only six orders, so the smallest possible p-value is 1/6 and D4 cannot flag at the 5% level.
- **D5 pooled-shuffle conformal test:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of other patients in the training set, matched by number of tests and mean sensitivity (a conformal p-value [27]).
- **D6 pooled-detrended conformal regional test:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [28]. This variant was the most sensitive approach during development.
- **D7 event analysis:** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to Guided Progression Analysis [11]. D7 needs at least four tests.
- **D8 machine learning, tabular:** gradient-boosted trees on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set stable eyes, as is common in machine-learning studies.
- **D9 machine learning, sequence:** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 self-supervised order network:** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [29].

Permutation p-values were computed so that they can never be zero [30]. Stochastic detectors (D4–D6, D8–D10) were run with five seeds; we report the mean over seeds and give the standard deviation across seeds in the supplementary results table. D8 and D9 had the same tuning budget (12 configurations each) and, like all other detectors, used only training and validation data.

## Evaluation

*Number of tests (k).* With routine spacing in UWHVF, the third test of reference eyes was done a median of 2.3 years (progressors) and 2.2 years (stable eyes) after the first, and the sixth test a median of 6.3 and 7.3 years after the first.

*E1 future reference.* In UWHVF test-set eyes with at least eight tests, we measured sensitivity (share of reference progressors flagged) and specificity (share of reference stable eyes not flagged) using only the first k tests.

*E2 true no-change.* In the Artes data we took every window of k consecutive tests. Because rate-based rules depend on the time scale, each window was given the test dates of a randomly chosen UWHVF test-set eye (ten draws per window; amendment A1). There were 300, 270, 240 and 210 windows for k = 3, 4, 5 and 6. The share of windows flagged is the false-alarm rate.

*E3 shuffle audit.* In UWHVF test-set eyes, we randomly re-ordered the first k tests (ten times) and re-ran each detector. Shuffling removes any true trend, so the flag rate estimates the false-alarm rate without retest data.

*E4 external clinic.* In GRAPE, we applied the detectors to the first three or four tests of each eye and compared flags with the clinicians' labels. D5 and D7 were re-calibrated on GRAPE itself by five-fold patient-level cross-fitting, because the perimeter differs; D8 was transferred unchanged from UWHVF; the 24-2-specific detectors (D6, D9, D10) were not applied (amendment A2).

## Statistical analysis

Proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. We compared each detector with D1 on the same eyes using the exact McNemar test and corrected p-values for the nine comparisons within each number of tests and endpoint with the Holm method. For stochastic detectors, the paired tests used each eye's majority flag across seeds. Confidence intervals for paired differences came from 2,000 bootstrap resamples of eyes. A detector was considered valid at a given k if, on true no-change data, the lower limit of its false-alarm confidence interval was at or below 5% (no evidence of excess false alarms) and the upper limit did not exceed 10%. To express false alarms in clinical units, we report the expected number of false progression flags per 1,000 stable eyes at one review. We also report, among reference progressors, the share flagged by the sixth test. Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells and by their absolute difference. Analyses used Python 3.13 with NumPy, SciPy, pandas, scikit-learn, LightGBM and PyTorch. The full run took 24 minutes on a 4-core CPU without a graphics card.

## Use of artificial intelligence tools

An AI assistant (Claude, Anthropic) was used to write analysis code, run the analyses, search and check the literature, and draft the text. The authors checked the code, the result files and every cited reference, and take full responsibility for the content. Every number in the text, tables and figures is inserted by a script from machine-generated result files.

## Ethics

This study used only publicly available, de-identified data sets released by their custodians under open licences (UWHVF: BSD-3; GRAPE: CC0; Artes data: distributed with the visualFields R package). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

# Results

## Study population

Table 1 describes the three data sets. In the UWHVF test set, 132 eyes of 69 patients had at least eight tests. Of these, 26 eyes were reference progressors and 26 were reference stable. Reference eyes were followed for a median of 13.5 years (progressors) and 12.7 years (stable eyes). The Artes data contributed 360 fields from 30 patients, with a median mean sensitivity of 26.9 dB. GRAPE contributed 263 eyes with a median of 4 visits; 27 eyes had progression by the mean-deviation criterion.

| Characteristic | UWHVF reference progressors | UWHVF reference stable | Artes retest (true no change) | GRAPE (external) |
|---|---|---|---|---|
| Patients / eyes, n | 23 / 26 | 20 / 26 | 30 / 30 | 144 / 263 |
| Age at first test, years | 63.3 (54.1–67.7) | 54.0 (48.3–60.1) | not used | 41.0 (28.5–53.0) |
| Tests per eye, n | 12 (10–12) | 9 (8–12) | 12 | 4 (3–5) |
| Follow-up, years | 13.5 (10.8–15.6) | 12.7 (9.7–13.8) | 0.23 (0.21–0.25) | 2.3 (1.7–3.3) |
| Time from first to third test, years | 2.3 (1.9–3.4) | 2.2 (1.8–3.4) | 2 weeks by design | not computed |
| Mean total deviation at first test, dB | −4.3 (−6.3 to −3.2) | −4.4 (−5.9 to −3.1) | not available | not available |
| Mean sensitivity, dB | not shown | not shown | 26.9 (25.1–28.2) | not shown |
| Progression label positive, n | 26 (reference) | 0 | 0 (by design) | 27 (MD criterion) |

*Table 1. Characteristics of the evaluation data. Values are median (interquartile range) unless stated. UWHVF reference eyes are test-set eyes with at least eight tests. Mean total deviation is the unweighted mean of total deviation values over the 52 non-blind-spot locations. MD, mean deviation.*

## False alarms on true no-change data (validity)

Table 2 and Fig. 2 show all results. The trend test of mean sensitivity (D1) had a false-alarm rate between 3.8% and 5.1% at four to six tests, and 4.4% at three tests. It was valid at every number of tests. In clinical units, D1 raised about 44 false progression flags per 1,000 stable eyes at a review based on three tests.

Three detectors were not valid at three tests. The pooled-detrended conformal test (D6) had a false-alarm rate of 22.4% (95% CI 19.3–25.7%), or about 224 false flags per 1,000 stable eyes. Gradient-boosted trees (D8) had 27.7% (95% CI 22.7–32.9%), and the recurrent network (D9) had 12.7% (95% CI 6.2–20.0%). D8 also exceeded the validity limits at four tests (9.4%) and five tests (18.8%), and D9 at five tests (7.5%). At six tests, D6 had 7.6% (95% CI 4.5–11.1%) and D9 had 5.9% (95% CI 2.3–10.0%), so both were again not valid; D9 only just exceeded the 10% upper limit.

Three detectors could not flag any eye at three tests: PoPLR (D4) and the self-supervised order network (D10), because six orderings cannot give a p-value below 5%, and event analysis (D7), which needs a fourth test. The pointwise rule (D3) was conservative at every number of tests, with false alarms of 1.4% or less.

| Detector | k | Sensitivity, % (95% CI) | Specificity, % | False alarms, true no-change, % (95% CI) | False alarms, shuffle audit, % | Valid |
|---|---|---|---|---|---|---|
| D1 Trend, MD | 3 | 19.2 (7.4–33.3) | 96.2 | 4.4 (2.8–6.3) | 4.8 | yes |
| D2 MD rate | 3 | 38.5 (20.0–56.5) | 92.3 | 2.6 (1.5–3.9) | 11.7 | yes |
| D3 PLR-3 | 3 | 3.8 (0.0–12.5) | 96.2 | 1.4 (1.0–1.8) | 1.8 | yes |
| D4 PoPLR | 3 | 0.0 (0.0–0.0) | 100.0 | 0.0 (0.0–0.0) | 0.0 | yes |
| D5 Pooled conformal | 3 | 19.2 (7.4–33.3) | 96.2 | 4.0 (2.7–5.6) | 4.6 | yes |
| D6 Pooled-detrended | 3 | 56.9 (37.0–76.2) | 96.2 | 22.4 (19.3–25.7) | 22.5 | **no** |
| D7 Event | 3 | 0.0 (0.0–0.0) | 100.0 | 0.0 (0.0–0.0) | 0.0 | yes |
| D8 LightGBM | 3 | 26.2 (12.3–43.2) | 94.6 | 27.7 (22.7–32.9) | 17.3 | **no** |
| D9 GRU | 3 | 12.3 (2.4–24.8) | 95.4 | 12.7 (6.2–20.0) | 8.5 | **no** |
| D10 Order net | 3 | 0.0 (0.0–0.0) | 100.0 | 0.0 (0.0–0.0) | 0.0 | yes |
| D1 Trend, MD | 4 | 30.8 (14.3–48.1) | 100.0 | 3.8 (1.9–6.2) | 4.7 | yes |
| D2 MD rate | 4 | 23.1 (8.0–40.0) | 96.2 | 0.6 (0.4–0.9) | 6.4 | yes |
| D3 PLR-3 | 4 | 15.4 (3.6–30.8) | 100.0 | 0.2 (0.0–0.3) | 1.5 | yes |
| D4 PoPLR | 4 | 3.8 (0.0–12.5) | 100.0 | 3.3 (1.8–4.9) | 4.1 | yes |
| D5 Pooled conformal | 4 | 30.8 (14.3–48.1) | 100.0 | 3.6 (1.8–5.9) | 4.9 | yes |
| D6 Pooled-detrended | 4 | 25.4 (10.3–44.0) | 100.0 | 5.1 (3.4–7.2) | 5.5 | yes |
| D7 Event | 4 | 23.1 (7.7–40.0) | 100.0 | 1.1 (0.0–2.6) | 5.2 | yes |
| D8 LightGBM | 4 | 41.5 (23.7–59.2) | 99.2 | 9.4 (6.3–12.9) | 7.7 | **no** |
| D9 GRU | 4 | 11.5 (2.8–23.2) | 99.2 | 2.0 (0.6–3.7) | 4.7 | yes |
| D10 Order net | 4 | 20.0 (7.7–35.8) | 100.0 | 3.8 (2.5–5.1) | 4.1 | yes |
| D1 Trend, MD | 5 | 42.3 (23.1–61.5) | 100.0 | 4.7 (2.2–7.5) | 5.1 | yes |
| D2 MD rate | 5 | 23.1 (7.7–41.4) | 100.0 | 0.8 (0.5–1.2) | 3.6 | yes |
| D3 PLR-3 | 5 | 23.1 (8.0–40.0) | 100.0 | 0.5 (0.1–1.1) | 1.4 | yes |
| D4 PoPLR | 5 | 38.5 (20.0–57.7) | 100.0 | 3.9 (1.9–6.2) | 4.3 | yes |
| D5 Pooled conformal | 5 | 42.3 (23.1–61.5) | 100.0 | 4.3 (2.0–7.1) | 4.9 | yes |
| D6 Pooled-detrended | 5 | 31.5 (16.0–48.5) | 100.0 | 6.2 (3.7–8.9) | 5.0 | yes |
| D7 Event | 5 | 50.0 (30.4–69.6) | 100.0 | 1.2 (0.0–2.9) | 7.9 | yes |
| D8 LightGBM | 5 | 56.2 (36.1–74.8) | 99.2 | 18.8 (13.1–24.9) | 16.1 | **no** |
| D9 GRU | 5 | 40.8 (22.8–59.2) | 93.8 | 7.5 (2.8–13.3) | 8.1 | **no** |
| D10 Order net | 5 | 43.8 (28.0–60.0) | 100.0 | 5.1 (2.9–7.6) | 4.2 | yes |
| D1 Trend, MD | 6 | 57.7 (38.4–76.9) | 100.0 | 5.1 (2.5–8.1) | 5.9 | yes |
| D2 MD rate | 6 | 23.1 (8.3–38.5) | 100.0 | 1.0 (0.6–1.5) | 2.8 | yes |
| D3 PLR-3 | 6 | 23.1 (7.7–41.7) | 100.0 | 0.3 (0.0–0.8) | 1.2 | yes |
| D4 PoPLR | 6 | 50.0 (30.8–67.9) | 100.0 | 5.0 (2.4–8.4) | 4.8 | yes |
| D5 Pooled conformal | 6 | 56.9 (37.7–76.0) | 100.0 | 5.0 (2.4–7.9) | 5.0 | yes |
| D6 Pooled-detrended | 6 | 53.8 (37.0–71.4) | 100.0 | 7.6 (4.5–11.1) | 4.9 | **no** |
| D7 Event | 6 | 57.7 (36.0–77.8) | 100.0 | 1.9 (0.5–3.8) | 11.7 | yes |
| D8 LightGBM | 6 | 70.8 (51.7–88.8) | 100.0 | 3.6 (1.7–6.0) | 8.7 | yes |
| D9 GRU | 6 | 37.7 (22.3–53.8) | 91.5 | 5.9 (2.3–10.0) | 8.6 | **no** |
| D10 Order net | 6 | 54.6 (36.9–70.8) | 99.2 | 5.7 (3.0–9.2) | 4.7 | yes |

*Table 2. Sensitivity against the future-confirmed reference (26 progressors), specificity (26 stable eyes), and false-alarm rates on true no-change series (Artes) and in the shuffle audit (UWHVF test set), using only the first k tests. Values for stochastic detectors are means over five seeds. 95% CIs from patient-level bootstrap. "Valid" means that the lower limit of the false-alarm CI was at or below 5% and the upper limit at or below 10%.*

## Sensitivity compared with the trend test

D1 detected 19.2% (95% CI 7.4–33.3%) of reference progressors at three tests, 30.8% at four, 42.3% at five and 57.7% (95% CI 38.4–76.9%) at six tests. Only one detector was significantly more sensitive than D1 at any number of tests: D6 at three tests, with a sensitivity of 56.9% (95% CI 37.0–76.2%) and a difference of +38.5 percentage points (95% CI 19.2 to 57.7; Holm-adjusted p = 0.02). This gain came with the invalid false-alarm rate described above. The hypothesis that no valid detector would beat D1 by 10 percentage points or more with a significant McNemar test was therefore not rejected at any number of tests.

Some valid detectors had higher point estimates than D1, but none of the differences was significant. At three tests, the rate rule D2 detected 38.5% of progressors (+19.2 percentage points (95% CI 0.0 to 42.3; Holm-adjusted p = 0.72)). Its false-alarm rate on true no-change data was low (2.6%), but its false-alarm rate in the shuffle audit was 11.7%. At six tests, D8 detected 70.8% of progressors with a valid false-alarm rate of 3.6% (+11.5 percentage points (95% CI −7.7 to 30.8; Holm-adjusted p = 1.00)). The pooled-shuffle conformal test (D5) had exactly the same sensitivity as D1 at three to five tests and almost the same at six tests (56.9%). The pointwise rule D3 was significantly less sensitive than D1 at six tests (−34.6 percentage points (95% CI −53.8 to −19.2; Holm-adjusted p = 0.04)).

Specificity against reference-stable eyes did not separate the detectors. It was at least 91.5% for every detector at every number of tests, and no difference from D1 was significant. For example, D6 had a specificity of 96.2% at three tests, while its false-alarm rate on true no-change data was 22.4%.

## Machine-learning detectors

D8 and D9 were thresholded at 95% specificity on validation-set stable eyes, as is common practice. On true no-change data, D8 had false-alarm rates of 27.7%, 9.4%, 18.8% and 3.6% at three to six tests. D9 had 12.7%, 2.0%, 7.5% and 5.9%. By our validity rule, the hypothesis that these detectors exceed the nominal 5% was supported for D8 at three to five tests and for D9 at three, five and six tests. D8 was valid at six tests, and D9 at four tests. Results varied across seeds: the seed standard deviation of D8 sensitivity was 5.0 percentage points at three tests.

## Shuffle audit

Across the 40 detector–test-number cells, the shuffle-audit false-alarm rate in UWHVF correlated with the true no-change rate (Spearman ρ = 0.65; Fig. 3). The median absolute difference was 1.0 percentage points, and 80% of cells differed by 3 percentage points or less. The pre-specified target of ρ ≥ 0.70 was not met. The largest difference was 10.4 percentage points. The audit gave higher rates than true no-change data for event analysis (D7 at six tests: 11.7% versus 1.9%) and for D2 at three tests. It identified the invalid D6 at three tests (22.5%) and the excess false alarms of D8 (17.3% at three tests), but it underestimated the false alarms of D9 at three tests (8.5% versus 12.7%).

## External clinic

In GRAPE (Table 3, Fig. 4), D1 detected 44.4% (95% CI 25.9–65.4%) of eyes labelled as progressing by the clinicians' mean-deviation criterion at three tests, with a specificity of 95.3% (95% CI 92.2–97.9%). D5, calibrated on GRAPE itself, gave similar results (sensitivity 41.5%, specificity 95.4%). D8, transferred from UWHVF without change, flagged more labelled progressors (65.9%; +25.9 percentage points (95% CI 0.0 to 48.1; Holm-adjusted p = 0.28)), but its specificity fell to 61.2% (+33.5 percentage points (95% CI 27.5 to 39.4; Holm-adjusted p < 0.001) in false positives). The rate rule D2 also raised more false positives than D1 (+16.5 percentage points (95% CI 11.0 to 22.0; Holm-adjusted p < 0.001)). With four tests, D8 again had more false positives than D1 (+14.5 percentage points (95% CI 9.0 to 20.7; Holm-adjusted p < 0.001)). PoPLR, D3 and event analysis flagged few or no eyes with three tests.

| Detector | k | Sensitivity, % (95% CI) | Specificity, % (95% CI) |
|---|---|---|---|
| D1 Trend, MD | 3 | 44.4 (25.9–65.4) | 95.3 (92.2–97.9) |
| D2 MD rate | 3 | 59.3 (40.7–76.9) | 78.8 (73.5–83.9) |
| D3 PLR-3 | 3 | 3.7 (0.0–11.5) | 95.8 (92.7–98.3) |
| D4 PoPLR | 3 | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) |
| D5 Pooled conformal | 3 | 41.5 (23.8–60.0) | 95.4 (92.4–98.0) |
| D7 Event | 3 | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) |
| D8 LightGBM | 3 | 65.9 (50.8–80.0) | 61.2 (54.6–67.1) |
| D1 Trend, MD | 4 | 33.3 (11.8–55.0) | 95.9 (92.2–98.6) |
| D2 MD rate | 4 | 55.6 (35.3–76.5) | 86.2 (79.4–92.1) |
| D3 PLR-3 | 4 | 11.1 (0.0–25.0) | 97.9 (95.2–100.0) |
| D4 PoPLR | 4 | 22.2 (5.9–41.2) | 95.2 (91.4–98.0) |
| D5 Pooled conformal | 4 | 33.3 (11.8–55.0) | 94.5 (90.8–97.7) |
| D7 Event | 4 | 16.7 (0.0–33.3) | 95.9 (92.4–98.7) |
| D8 LightGBM | 4 | 48.9 (31.8–65.9) | 81.5 (74.2–87.9) |

*Table 3. External clinic (GRAPE): agreement with clinicians' mean-deviation progression label using the first k tests (27 labelled progressors and 236 non-progressors with at least three tests). D5 and D7 were calibrated on GRAPE by patient-level cross-fitting; D8 was trained on UWHVF only. 95% CIs from patient-level bootstrap.*

## Secondary reference and time to detection

Against the secondary PoPLR reference, D1 detected 10.3% of progressors at three tests and 37.9% at six tests (58 progressors). D6 detected 46.2% at three tests, but with the same invalid false-alarm rate. By the sixth test, D1 had flagged 69% of reference progressors. The most sensitive detectors by this measure were D8 (78%) and D6 (77%), the two detectors with the highest false-alarm rates. In routine UWHVF care, the sixth test came a median of 6.3 years after the first in progressing eyes.

# Discussion

In this benchmark, no detector found significantly more future-confirmed progression than a simple trend test of mean sensitivity while keeping a valid false-alarm rate. This result supports our main hypothesis. The one detector that was significantly more sensitive, a conformal test with a pooled and detrended reference, raised a false alarm in about one in five true no-change series. Machine-learning models thresholded at 95% specificity raised false alarms in up to 27.7% of such series. The gains these detectors seemed to offer were, at least in large part, false alarms.

The usual way of measuring specificity did not reveal this problem. All detectors had high specificity against reference-stable eyes, including D6, which flagged 22.4% of true no-change series. Reference-stable eyes are selected because their long-term course is flat, and there were only 26 of them. Such a set can be easier than the stable eyes a clinic sees at an ordinary visit. True no-change data and the shuffle audit both measure the false-alarm rate more directly. In our study, both identified the same invalid detectors.

The machine-learning result has a simple explanation. A threshold chosen to give 95% specificity in labelled stable eyes controls false alarms only in eyes that resemble those eyes. Short series, and series from other clinics, may not. Thresholds chosen on labelled stable eyes are a natural choice for machine-learning detectors of progression [15–17], but our results show that they should also be checked on true no-change data. Our external results point the same way: the model transferred from UWHVF to GRAPE lost specificity, while a simple test calibrated on the external clinic's own data did not. Labels also differ between studies, and models trained on one label may not transfer [23].

The second lesson is that the information in a few tests is limited. In routine care in Seattle, the third test of reference eyes came a median of 2.3 years after the first, and the sixth test a median of 6.3 years after the first (progressing eyes). Even so, the trend test flagged only about 69% of reference progressors by the sixth test. More complex statistics did not overcome this limit without paying in false alarms. This agrees with earlier work showing that the number and timing of tests largely determine how quickly progression can be confirmed [5, 31–33]. Practical ways to gain time are therefore more tests early in follow-up [34] or scheduling guided by risk [21, 35], rather than more aggressive detection rules.

Within-eye permutation methods such as PoPLR are valid by design [7]. However, they cannot flag any eye with three tests, because there are only six possible orders. Pooling permutation references across patients, using ideas from permutation and conformal inference [27–30], removes this floor, and we expected this to help. It did not: the pooled test without detrending (D5) matched the trend test almost exactly, and the detrended version was not valid. Event and trend methods have been compared before [10, 11]. In our data, event analysis was valid on true no-change data and had the highest point estimate of sensitivity among valid detectors at five tests, but its difference from the trend test was small and not significant.

The shuffle audit is a practical tool. Any clinic or developer can run it on routine records without a retest study. In our data it ranked detectors much like true no-change data did and flagged D6 and D8 as invalid at three tests. Its agreement fell short of our pre-specified target, however. The audit overestimated false alarms for event analysis and for the rate rule, probably because routine-care eyes are noisier than the early-glaucoma eyes in the retest study, whose median mean sensitivity was 26.9 dB. We therefore see the audit as a screening check, not a replacement for true no-change data.

For treatment decisions, these results matter in a direct way. A false progression flag can lead to additional drops, laser or surgery, with side effects and costs [2, 3]. At a false-alarm rate of 22.4%, a clinic reviewing 1,000 stable eyes would see about 224 false flags, compared with about 44 with the trend test. Claims of earlier detection should therefore be read together with false-alarm rates measured on data in which the disease did not change.

Our study has limitations. First, the future-confirmed reference set was small (26 progressors and 26 stable eyes), so confidence intervals for sensitivity were wide. The study could miss real differences of about 10–20 percentage points. Second, the primary reference was based on mean deviation, which may favour detectors based on mean sensitivity, such as D1. Against a secondary reference based on PoPLR, the pattern was the same: the largest sensitivity at three tests again belonged to the invalid D6. Third, the true no-change arm had only 30 patients, mostly with early to moderate damage, tested weekly. We gave each window the test dates of routine-care eyes, but false alarms in eyes with more damage may be higher than we measured. Fourth, UWHVF does not include diagnoses or reliability indices, so some eyes may not have glaucoma and some tests may be unreliable. Fifth, GRAPE used a different perimeter and had only 27 eyes labelled as progressing, and its labels came from criteria applied to the full series. Sixth, the Artes data were used once during development, to check false alarms of a candidate method; this is disclosed in the Supplementary Material. Seventh, we did not test every published detector, such as Bayesian spatial models [12–14], smoothing methods [36], deep forecasting models [18, 19] or diffusion-based models [22], and our machine-learning detectors had a fixed and modest tuning budget. Finally, we did not measure the clinical consequences of false alarms.

# Conclusions

In three independent data sources, a plain trend test of mean sensitivity was as good as any detector that kept false alarms at the nominal level, from the third to the sixth visual-field test. Detectors that appeared to find progression earlier did so largely by raising false alarms. Before a new detector is used to guide treatment escalation in glaucoma, it should report its false-alarm rate on true no-change data, or at least a shuffle audit. Faster confirmation of progression will more likely come from better-timed testing than from more aggressive analysis. Prospective studies should test this in clinical care.

# Declarations

## Acknowledgements

We thank the custodians of the UWHVF, GRAPE and Artes retest data sets for making their data openly available.

## Funding

[TO BE CONFIRMED BY THE AUTHORS] No funding or sponsorship was received for this study or publication of this article. [If the journal's Rapid Service Fee is paid by a funder, state it here.]

## Medical Writing, Editorial and Other Assistance

An AI assistant (Claude, Anthropic) was used to write and run the analysis code, check references and draft the manuscript, as described in the Methods. The authors reviewed and verified all content. No other writing assistance was received.

## Author Contributions

[TO BE COMPLETED BY THE AUTHORS, e.g. Conceptualization: …; Methodology: …; Software and formal analysis: …; Writing – original draft: …; Writing – review and editing: …. All authors read and approved the final manuscript.]

## Conflict of Interest

[TO BE COMPLETED BY THE AUTHORS for each author by name.]

## Ethical Approval

This study used only publicly available, de-identified data sets released by their custodians under open licences (UWHVF: BSD-3; GRAPE: CC0; Artes data: distributed with the visualFields R package). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

## Data Availability

All data used are publicly available. UWHVF: https://github.com/uw-biomedical-ml/uwhvf. GRAPE: figshare, https://ndownloader.figshare.com/files/41670009 (described in Huang et al., Sci Data 2023). Artes retest data: visualFields R package version 1.0.7 on CRAN. The code, the pre-specified protocol, the patient-level split, all raw detector outputs and the scripts that generate every number, table and figure in this article are available at [PUBLIC REPOSITORY URL — to be added by the authors before submission].

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

24. . TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024:q902. https://doi.org/10.1136/bmj.q902

25. Montesano G, Chen A, Lu R, Lee CS, Lee AY. UWHVF: A Real-World, Open Source Dataset of Perimetry Tests From the Humphrey Field Analyzer at the University of Washington. Trans. Vis. Sci. Tech.. 2022;11(1):2. https://doi.org/10.1167/tvst.11.1.1

26. Huang X, Kong X, Shen Z, Ouyang J, Li Y, Jin K, et al. GRAPE: A multi-modal dataset of longitudinal follow-up visual field and fundus images for glaucoma management. Sci Data. 2023;10(1). https://doi.org/10.1038/s41597-023-02424-4

27. Angelopoulos AN, Bates S. Conformal Prediction: A Gentle Introduction. Foundations and Trends® in Machine Learning. 2023;16(4):494-591. https://doi.org/10.1561/2200000101

28. Freedman D, Lane D. A Nonstochastic Interpretation of Reported Significance Levels. Journal of Business & Economic Statistics. 1983;1(4):292-298. https://doi.org/10.1080/07350015.1983.10509354

29. Gagnon-Bartsch J, Shem-Tov Y. The classification permutation test: A flexible approach to testing for covariate imbalance in observational studies. Ann. Appl. Stat.. 2019;13(3):1464-1483. https://doi.org/10.1214/19-aoas1241

30. Phipson B, Smyth GK. Permutation P-values Should Never Be Zero: Calculating Exact P-values When Permutations Are Randomly Drawn. Statistical Applications in Genetics and Molecular Biology. 2010;9(1). https://doi.org/10.2202/1544-6115.1585

31. Wu Z, Saunders LJ, Daga FB, Diniz-Filho A, Medeiros FA. Frequency of Testing to Detect Visual Field Progression Derived Using a Longitudinal Cohort of Glaucoma Patients. Ophthalmology. 2017;124(6):786-792. https://doi.org/10.1016/j.ophtha.2017.01.027

32. Crabb DP, Garway-Heath DF. Intervals between Visual Field Tests When Monitoring the Glaucomatous Patient: Wait-and-See Approach. Invest. Ophthalmol. Vis. Sci.. 2012;53(6):2770. https://doi.org/10.1167/iovs.12-9476

33. Stagg BC, Brintz BJ, Stein JD, Hess R, Kawamoto K, Jammal AA, et al. Time to Identify Glaucoma Progression Given Typical Visual Field Testing Frequencies in a US Nationwide Insured Population. Ophthalmology Glaucoma. 2026;9(3):250-256. https://doi.org/10.1016/j.ogla.2025.11.004

34. Phu J, Kalloniatis M. The Frontloading Fields Study (FFS): Detecting Changes in Mean Deviation in Glaucoma Using Multiple Visual Field Tests Per Clinical Visit. Trans. Vis. Sci. Tech.. 2021;10(13):21. https://doi.org/10.1167/tvst.10.13.21

35. Schell GJ, Lavieri MS, Helm JE, Liu X, Musch DC, Van Oyen MP, et al. Using Filtered Forecasting Techniques to Determine Personalized Monitoring Schedules for Patients with Open-Angle Glaucoma. Ophthalmology. 2014;121(8):1539-1546. https://doi.org/10.1016/j.ophtha.2014.02.021

36. Mohammadzadeh V, Li L, Fei Z, Davis T, Morales E, Wu K, et al. Efficacy of Smoothing Algorithms to Enhance Detection of Visual Field Progression in Glaucoma. Ophthalmology Science. 2024;4(2):100423. https://doi.org/10.1016/j.xops.2023.100423