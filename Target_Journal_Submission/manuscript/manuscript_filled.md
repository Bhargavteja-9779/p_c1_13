# Apparent Gains in Detecting Glaucomatous Visual-Field Progression Disappear at Matched False-Alarm Rates: A Two-Stage Benchmark

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, DEGREES — to be completed by the authors]

**Affiliations:** [INSTITUTION, CITY, COUNTRY — to be completed by the authors]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — to be completed by the authors]

**ORCID iDs:** [to be completed by the authors]

**Prior presentation:** [TO BE CONFIRMED BY THE AUTHORS: none.]

## Abstract

**Introduction:** Decisions to escalate glaucoma treatment rely on detecting visual-field progression. New detectors, including machine-learning models, often claim earlier detection, but are rarely compared at the same false-alarm rate. We tested whether any detector beats a simple trend test of mean sensitivity when false alarms are matched.

**Methods:** Study 1 compared ten detectors on a locked test split of the University of Washington data set, using the first 3–6 tests, with false alarms measured on true no-change retest series (30 patients tested over about 3 months). Study 2, specified in a new protocol, used 5-fold cross-fitting across all 690 eyes with at least eight tests (150 progressing, 164 stable). Every detector's threshold was set to 5% false alarms on shuffled series from the clinic's own records ("shuffle calibration"). An external clinic (263 eyes) tested local recalibration.

**Results:** Gradient-boosted trees thresholded at 95% specificity on stable eyes, a common practice, appeared 22.0 percentage points more sensitive than the trend test at six tests, but raised false alarms in 15.3% of true no-change series. With shuffle calibration, the same model raised 2.6% false alarms and gained 2.2 points (95% CI −2.9 to 7.1). Across eight shuffle-calibrated detectors and 3–6 tests, no detector was significantly more sensitive than the trend test; all upper confidence limits for the gain were below 8.4 points. Controlling cumulative false alarms over repeated reviews to 5% reduced detection by the sixth test from 64.7% to 47.6%. In the external clinic, local recalibration restored specificity of the transferred model (93.2%) but reduced its sensitivity.

**Conclusion:** Apparent gains in early detection of visual-field progression can be explained by higher false-alarm rates. At matched false alarms, a plain trend test was as sensitive as machine-learning and permutation detectors. Detectors should be compared, and deployed, at a stated false-alarm rate.

## Keywords

Benchmark; False alarms; Glaucoma; Machine learning; Perimetry; Progression; Specificity; Visual field

## Key Summary Points

**Why carry out this study?**

- Escalating glaucoma treatment depends on detecting visual-field progression, and many new detectors claim to detect it earlier than simple trend analysis.
- We asked whether such gains persist when every detector is held to the same false-alarm rate, measured on data in which the disease did not change.

**What was learned from the study?**

- A machine-learning detector thresholded in the usual way appeared 22.0 percentage points more sensitive than a trend test of mean sensitivity, but raised false alarms in 15.3% of true no-change series.
- When thresholds were calibrated to 5% false alarms on shuffled series of the clinic's own records, no detector was significantly more sensitive than the trend test, and gains of 8.4 percentage points or more were excluded.
- Claims of earlier progression detection should report the false-alarm rate, per review and over repeated reviews, at which they were obtained.

## Plain Language Summary

Glaucoma slowly damages side vision. Doctors use a visual-field test to see whether the damage is getting worse, and if it is, they may add eye drops, laser or surgery. Each test result varies from day to day, so doctors need several tests before they can be sure. Many new computer methods, including artificial intelligence, promise to spot worsening sooner. But a method can look better simply because it raises more false alarms. We first compared ten methods and measured their false alarms in patients who were tested every week for three months, when their glaucoma could not really have changed. We then repeated the comparison in more than 300 eyes, after adjusting every method so that it raised the same small number of false alarms. We did this by mixing up the order of each patient's tests in the clinic's own records. Once false alarms were matched, no method found more worsening than the simplest one, which draws a straight line through the average results. An artificial-intelligence method that seemed to find much more worsening did so mainly by raising many more false alarms. Methods that wait for a second confirming test raised fewer false alarms but found worsening later. New methods should say how many false alarms they raise before they are used to guide treatment.

# Introduction

Glaucoma is a leading cause of irreversible blindness [1]. An estimated 76 million people aged 40–80 years had glaucoma in 2020, and this number was projected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and in damaged areas the variability is so large that sensitivities below about 15–19 dB carry little information [4]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [5], but routine care rarely reaches this frequency [6]. Delays in follow-up are a documented cause of avoidable sight loss [7].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through a global index, such as the mean deviation or the visual field index [8, 9], or through each test location [10]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [8, 11, 12]; Guided Progression Analysis is the most widely used example [8, 11]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [10]. Bayesian and spatial models share information across locations or patients [13–15]. More recently, machine-learning models have been trained to classify or forecast progression [16–21], and some newer studies use deep generative models or risk-based test scheduling [22, 23].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order [10, 14], by using eyes labelled stable by another criterion [21], or by simulation [8, 24, 25]. Few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over about three months [11, 15]. It is not known whether the indirect estimates agree with the direct ones. Second, labels for "progression" differ between studies, and the choice of label strongly affects how well machine-learning models appear to perform [26]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can prompt extra testing or unnecessary escalation, with extra drops, laser or surgery and their side effects [2, 3].

We addressed this problem in two stages. In Study 1, we built an open benchmark of ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods, with a true no-change arm, a future-confirmed reference and an external clinic. Study 1 showed that the detectors that flagged more eyes also raised more false alarms, but it had too few reference eyes to compare detectors precisely. In Study 2, we therefore held every detector to the same false-alarm rate with a simple procedure that any clinic can apply to its own records: calibrating each detector's threshold on randomly re-ordered ("shuffled") test series. We then asked whether, at matched false alarms, any detector would detect at least 10 percentage points more future-confirmed progression than the trend test of mean sensitivity. Our hypothesis was that none would.

# Methods

## Study design and reporting

This was a two-stage retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [27]. Before each stage, the analysis plan (detectors, thresholds, reference standards, hypotheses and statistical tests) was written down and time-stamped by a commit in the study's version-control repository; neither plan was registered with an external registry. The Study 1 plan was written before the Study 1 test data were analysed. The Study 2 plan was written after the Study 1 results were known, but before any Study 2 analysis was run. Deviations and analyses added after internal review are labelled as such. Ideas that we developed and abandoned during the study are listed in the Supplementary Material.

## Data sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains 28,943 24-2 tests from 7,428 eyes of 3,871 patients seen in routine care [28] (counts from the released file; the data paper reports 7,248 eyes). It includes sensitivities, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. In Study 1, the test set (777 patients, 869 eyes with at least three tests) was used once, for the final analysis. Study 2 used all patients with cross-fitting (see below).

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields at about weekly intervals [11] (median span 84 days; one series spanned 524 days). Glaucoma does not change measurably over this period, so any "progression" flag in these series is a false alarm. The data are distributed with the visualFields R package (version 1.0.7).

*GRAPE (external clinic).* The GRAPE data set contains 1,115 visual-field records from 263 eyes of 144 patients with glaucoma followed in Hangzhou, China [29]. Fields were measured with a different perimeter and test grid (59 analysable locations per field, median), and each eye carries progression labels supplied with the data set, assigned with three criteria (mean deviation, and two pointwise linear regression rules, PLR2 and PLR3) applied to the whole follow-up. We used the mean-deviation label as the primary label and report the other two in the Supplementary Material. Of the 263 eyes, 254 had open-angle and 9 angle-closure glaucoma.

## Reference standard (UWHVF, Study 1)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5, which means that its estimated full-series slope was zero or positive. Other eyes were excluded from the sensitivity and specificity analysis. Of 132 test-set eyes with at least eight tests, 26 were progressors, 26 were stable and 80 were excluded. The reference uses the whole series, including the first k tests that the detectors see. Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations; progressor p < 0.01, stable p > 0.5). It identified 58 progressors, which include all 26 primary progressors.

## Study 1 detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 Trend (mean sensitivity):** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 Rate rule:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3 (pointwise rule):** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [10], using all possible orders of the k tests. With three tests there are only six orders, so the smallest possible p-value is 1/6 and D4 cannot flag at the 5% level.
- **D5 Pooled conformal:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of other patients in the training set, matched by number of tests and mean sensitivity (a conformal p-value [30]).
- **D6 Pooled-detrended conformal:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [31]. It was the most sensitive variant during development, where it had already shown excess false alarms on the Artes data (Supplementary Material).
- **D7 Event analysis:** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests. This is a simplified event analysis on raw sensitivities, loosely modelled on Guided Progression Analysis [8, 11]; it does not use pattern deviation. D7 needs at least four tests.
- **D8 LightGBM (tabular machine learning):** gradient-boosted trees on 14 summary features of the first k tests, trained to predict the reference label in 93 progressing and 99 stable training eyes. Model selection and the threshold (95% specificity) used the validation eyes (31 progressing, 39 stable), a choice similar to stability limits derived from stable eyes in earlier work [18, 21].
- **D9 GRU (sequence machine learning):** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 Order network (self-supervised):** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [32].

Permutation p-values were computed so that they can never be zero [33]. Stochastic detectors (D4–D6, D8–D10) were run with five seeds. All detectors were fitted on training and validation data only.

## Study 1 evaluation

*E1 future reference:* sensitivity and specificity in test-set eyes with at least eight tests, using only the first k tests. *E2 true no-change:* the share of flagged windows among all windows of k consecutive Artes tests (300 to 210 windows). Because rate-based rules depend on time, each window was given the test dates of a randomly chosen UWHVF test-set eye (ten draws per window; amendment A1). *E3 shuffle audit:* the flag rate after randomly re-ordering the first k tests of test-set eyes (ten orders per eye), as an estimate of the false-alarm rate that needs no retest data. *E4 external clinic:* agreement with GRAPE's labels at three and four tests; D5 and D7 were re-calibrated on GRAPE by patient-level cross-fitting because the perimeter differs, D8 was transferred unchanged, and the 24-2-specific detectors were not applied (amendment A2). For 100 GRAPE eyes with only three visits, the labels were based on the same tests that the detectors saw.

## Study 2: comparison at matched false alarms

*Design.* We used 5-fold patient-level cross-fitting across all UWHVF patients. In each fold, detectors were fitted and calibrated on four fifths of the patients and evaluated on the remaining fifth, so that every eye was evaluated once, by detectors that had never seen it. Machine-learning models used a further patient-level split of the fitting patients (75% for fitting, 25% for model selection). Of 690 eyes of 379 patients with at least eight tests, 150 were progressors and 164 were stable by the Study 1 reference (R1). Because R1-stable eyes have flat or improving slopes, we also used a "flat stable" reference (R2: full-series slope between −0.3 and +0.3 dB per year and one-sided p > 0.1; 310 eyes) and a future-only reference that ignores the tests the detector saw (R3: the R1 rule applied to tests k+1 onwards, requiring at least five such tests).

*Shuffle calibration.* For a detector that produces a score, the threshold at k tests was the 95th percentile of the score over shuffled versions of the first k tests of the calibration eyes (20 random non-identity orders per eye, each eye keeping its own test dates). Shuffling removes any time trend but keeps each eye's level, noise, damage pattern and test spacing. The threshold therefore targets a 5% false-alarm rate per review in the clinic's own population, without a retest study.

*Detectors.* Ten per-review detectors were compared. D1 (the trend test, p < 0.05) and D7 (event analysis) were as in Study 1. Six detectors were shuffle-calibrated versions of established ideas: S1, the trend t-statistic; S2, the rate of change of mean sensitivity; S3, the PoPLR statistic [10], pooled across patients so that it can flag with three tests; S4, event analysis with its change-limit percentile (1% to 20%) and number of locations (two to four) chosen as the most liberal combination with at most 5% shuffled false alarms; S5, the Study 1 gradient-boosted-tree model (LightGBM); and S7, the Study 1 GRU network. S6 was a self-supervised detector: a LightGBM model trained, without any progression labels, to tell an eye's real test order from shuffled orders of the same tests, using all calibration eyes [32]. B8 was the Study 1 LightGBM model with its usual threshold (95% specificity on labelled stable eyes). Stochastic detectors were run with three seeds.

*Repeated reviews.* In practice, a detector is applied again at every new test. We therefore also compared four detectors designed to keep the cumulative false-alarm rate over the reviews at three, four, five and six tests at 5%: Q1, a sequential trend test with one common per-review level; Q2, a confirmed trend test that requires the trend criterion to be met at two consecutive reviews; Q3, a confirmed shuffle-calibrated event analysis; and Q4, a sequential version of S6. Their levels were chosen on shuffled six-test sequences of the calibration eyes. D1 and D7 applied at every review served as comparators.

*Evaluation.* We measured sensitivity (R1 and R3) and specificity (R1 and R2) in held-out eyes using the first k tests, and false alarms on the Artes series as in Study 1. For repeated reviews, we measured the share of progressors and of true no-change series flagged at least once by the sixth test; for Artes, the first six tests of each series were used, with one set of borrowed test dates kept across reviews. In GRAPE, D1, S1, S5, S6 and B8 were applied at three and four tests, with thresholds either taken from UWHVF or recalibrated on GRAPE's own shuffled series by 5-fold patient-level cross-fitting ("local recalibration").

## Statistical analysis

Proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. Each detector was compared with D1 on the same eyes with the exact McNemar test, using each eye's majority flag across seeds, and p-values were corrected with the Holm method within each number of tests. A detector was called valid if, on true no-change data, the lower confidence limit of its false-alarm rate was at or below 5% and the upper limit at or below 10%. This rule differs from the literal wording of the Study 1 protocol (upper limit at or below 5%), which no detector near the nominal rate could meet with 30 patients; the rule was fixed in our draft Methods before the Study 1 results were available and made operational afterwards. The full Study 1 statistical methods, this deviation and a sensitivity analysis under the literal rule are given in the Supplementary Material. False alarms are also expressed as false flags per 1,000 stable eyes at one review. Analyses used Python 3.13 with NumPy, SciPy, pandas, scikit-learn, LightGBM and PyTorch on a 4-core CPU; the Study 1 run took 24 minutes.

In Study 2, the same bootstrap and exact McNemar methods were used, with Holm correction across the eight calibrated detectors (D7 and S1–S7) within each number of tests; B8 is reported without adjustment. The pre-specified hypotheses were that every shuffle-calibrated detector would be valid on true no-change data (H6); that at least one would be at least 10 percentage points more sensitive than D1 with a significant McNemar test (H7, our main question, which we expected to be rejected); that at a cumulative false-alarm rate of about 5% the best repeated-review detector would be non-inferior to D1 applied at every review, with a margin of 10 percentage points (H8); and that local recalibration in GRAPE would restore a specificity of at least 90% (H9). The Study 2 run took 7 minutes.

## Use of artificial intelligence tools

An AI assistant (Claude, Anthropic) was used to write analysis code, run the analyses, search and check the literature, and draft the text. The authors checked the code, the result files and every cited reference, and take full responsibility for the content. Every number in the text, tables and figures is inserted by a script from machine-generated result files.

## Ethics

This study used only publicly available, de-identified data sets released by their custodians under open licences (UWHVF: BSD-3; GRAPE: CC0; Artes data: distributed with the visualFields R package). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

# Results

## Study populations

Table 1 describes the data. In Study 1, 26 test-set eyes were reference progressors and 26 were reference stable. In Study 2, cross-fitting made 150 progressing and 164 stable eyes available, followed for a median of 13.3 and 12.9 years. In routine UWHVF care, the third test of progressing eyes came a median of 2.1 years after the first, and the sixth a median of 5.9 years after the first. The Artes data contributed 360 fields from 30 patients, with a median mean sensitivity of 26.9 dB. GRAPE contributed 263 eyes, of which 27 had progression by the mean-deviation criterion.

| Characteristic | UWHVF progressors (R1) | UWHVF stable (R1) | UWHVF flat stable (R2) | Artes retest (true no change) | GRAPE (external) |
|---|---|---|---|---|---|
| Patients / eyes, n | 116 / 150 | 125 / 164 | 214 / 310 | 30 / 30 | 144 / 263 |
| Of which in Study 1 test split, eyes | 26 | 26 | — | — | — |
| Female patients, n (%) | 58 (50%) | 80 (64%) | 122 (57%) | not available | 69 (48%) |
| Age at first test, years | 65.8 (58.4–72.0) | 56.0 (47.0–63.5) | 58.7 (52.4–65.6) | not used | 41.0 (28.5–53.0) |
| Tests per eye, n | 10 (9–12) | 9 (8–11) | 9 (8–11) | 12 | 4 (3–5) |
| Follow-up, years | 13.3 (10.5–14.6) | 12.9 (9.5–14.7) | 12.9 (10.4–14.7) | 0.23 (0.21–0.25) | 2.3 (1.7–3.3) |
| Time from first to sixth test, years | 5.9 (4.5–7.7) | 7.2 (4.7–9.7) | 7.4 (5.6–9.5) | about 5 weeks by design | not computed |
| Mean total deviation at first test, dB | −5.1 (−8.3 to −3.3) | −4.7 (−8.2 to −2.7) | −3.8 (−6.1 to −2.4) | not available | not available |
| Mean sensitivity, dB | not shown | not shown | not shown | 26.9 (25.1–28.2) | not shown |
| Progression label positive, n | 150 (reference) | 0 | 0 | 0 (by design) | 27 (MD criterion) |

*Table 1. Characteristics of the evaluation data. Values are median (interquartile range) unless stated. Study 2 reference eyes are all UWHVF eyes with at least eight tests (cross-fitted); Study 1 eyes are the test-split subset. Mean total deviation is the unweighted mean of total deviation values over the 52 non-blind-spot locations. MD, mean deviation.*

## Study 1: detectors that flagged more eyes raised more false alarms

Fig. 2 shows the Study 1 results (full results in Supplementary Table S1). The trend test (D1) detected 19.2% (95% CI 7.4–33.3%) of reference progressors at three tests and 57.7% (95% CI 38.4–76.9%) at six tests, with false-alarm rates on true no-change series between 3.8% and 5.1%. The only detector significantly more sensitive than D1 was the pooled-detrended conformal test at three tests (56.9%; +38.5 percentage points, 95% CI 19.2 to 57.7, Holm-adjusted p = 0.02), which raised false alarms in 22.4% (95% CI 19.3–25.7%) of true no-change series. LightGBM thresholded at 95% specificity raised false alarms in 27.7% at three tests and 18.8% at five tests. Yet specificity against reference-stable eyes was at least 91.5% for every detector, so this usual measure did not reveal the problem. With 26 progressors, only gains of 34.6 percentage points or more could reach significance. The shuffle audit (re-running detectors on shuffled orders) tracked true false-alarm rates moderately (Spearman ρ = 0.65; 80% of cells within 3 percentage points; Supplementary Material).

## Study 2: usual-practice thresholds inflate apparent gains

In Study 2 (Table 2, Fig. 3), LightGBM with its usual threshold (B8) appeared more sensitive than D1 at four to six tests, by +18.2 percentage points, 95% CI 9.7 to 26.8, p < 0.001 at four tests and +22.0 percentage points, 95% CI 15.3 to 28.5, p < 0.001 at six tests. This apparent gain came with false alarms in 21.7% (95% CI 17.3–26.1%) of true no-change series at four tests and 15.3% (95% CI 11.5–19.1%) at six tests, and with lower specificity against flat-stable eyes (−15.8 percentage points, 95% CI −20.0 to −11.7, p < 0.001 at six tests).

## Study 2: at matched false alarms, no detector beat the trend test

Shuffle calibration brought the false-alarm rates of the machine-learning detectors on true no-change data down to 2.6–8.1% for S5, 2.2–4.4% for S6 and 1.5–2.9% for S7, depending on the number of tests. All shuffle-calibrated detectors met the validity rule at every number of tests, except S5 at three tests (8.1% (95% CI 6.2–10.1%)) and five tests (7.6% (95% CI 5.0–10.5%)), whose upper limits slightly exceeded 10%. Hypothesis H6 was therefore supported for seven of the eight calibrated detectors. Several calibrated detectors (S2, S3, S4) were conservative on true no-change data, with false-alarm rates of 1% or less.

At matched false alarms, no detector was significantly more sensitive than D1 at any number of tests, so H7 was rejected. The largest point estimates were +2.7 percentage points, 95% CI 0.7 to 5.3, Holm-adjusted p = 0.12 for the calibrated trend statistic at four tests and +2.2 percentage points, 95% CI −2.9 to 7.1, Holm-adjusted p = 1.00 for calibrated LightGBM at six tests. Across all 32 comparisons, the upper confidence limit of the gain did not exceed 8.4 percentage points. Several detectors were significantly less sensitive than D1, including the calibrated event analysis and the calibrated GRU at five and six tests (Table 2). The self-supervised order model (S6), trained without labels, matched D1 at three tests (+0.7 percentage points, 95% CI −5.0 to 5.8, Holm-adjusted p = 1.00) but was less sensitive at four tests (−6.4 percentage points, 95% CI −11.4 to −1.4, Holm-adjusted p = 0.003). Against the future-only reference R3, which had fewer progressors (95 at three tests and 34 at six tests), no calibrated detector exceeded the sensitivity of D1 by more than 7.8 percentage points, whereas B8 again gained sensitivity at the cost of specificity (Supplementary Table S2).

| Detector | k | Sensitivity, % (95% CI) | Gain vs D1, pp (Holm p) | Spec R1, % | Spec R2, % | False alarms, true no-change, % (95% CI) | Valid |
|---|---|---|---|---|---|---|---|
| D1 Trend | 3 | 14.7 (9.3–20.5) | — | 96.3 | 95.2 | 4.2 (2.8–5.7) | yes |
| D7 Event analysis | 3 | 0.0 (0.0–0.0) | −14.7 (<0.001) | 100.0 | 100.0 | 0.0 (0.0–0.0) | yes |
| S1 SC trend | 3 | 15.3 (9.9–21.4) | +0.7 (1.00) | 96.3 | 95.2 | 4.6 (3.1–6.2) | yes |
| S2 SC rate | 3 | 5.3 (1.9–9.7) | −9.3 (0.06) | 89.6 | 96.1 | 0.7 (0.4–0.9) | yes |
| S3 SC PoPLR | 3 | 16.0 (9.7–22.6) | +1.3 (1.00) | 91.5 | 91.6 | 0.1 (0.0–0.2) | yes |
| S4 SC event | 3 | 5.3 (2.0–9.6) | −9.3 (0.03) | 95.7 | 98.1 | 0.0 (0.0–0.0) | yes |
| S5 SC LightGBM | 3 | 14.2 (9.3–19.7) | −0.4 (1.00) | 97.4 | 95.6 | 8.1 (6.2–10.1) | **no** |
| S6 Order LightGBM | 3 | 15.3 (10.7–20.5) | +0.7 (1.00) | 90.9 | 92.6 | 2.2 (1.6–2.8) | yes |
| S7 SC GRU | 3 | 6.9 (3.5–10.9) | −7.8 (0.18) | 94.5 | 96.0 | 2.9 (1.1–5.3) | yes |
| B8 LightGBM, 95% spec | 3 | 18.7 (12.7–25.4) | +4.0 (0.47) | 94.7 | 91.8 | 13.9 (10.9–17.1) | **no** |
| D1 Trend | 4 | 26.7 (19.7–34.0) | — | 95.7 | 93.2 | 3.9 (2.1–6.2) | yes |
| D7 Event analysis | 4 | 16.0 (10.3–22.7) | −10.7 (0.06) | 93.3 | 96.1 | 0.8 (0.0–1.9) | yes |
| S1 SC trend | 4 | 29.3 (22.1–36.9) | +2.7 (0.12) | 95.3 | 92.9 | 4.2 (2.2–6.6) | yes |
| S2 SC rate | 4 | 16.0 (10.7–21.6) | −10.7 (0.06) | 93.3 | 97.1 | 0.6 (0.4–0.8) | yes |
| S3 SC PoPLR | 4 | 27.3 (20.7–34.7) | +0.7 (1.00) | 89.8 | 88.5 | 0.2 (0.0–0.4) | yes |
| S4 SC event | 4 | 13.3 (8.0–19.4) | −13.3 (0.00) | 95.1 | 97.4 | 0.2 (0.0–0.7) | yes |
| S5 SC LightGBM | 4 | 18.0 (12.6–24.0) | −8.7 (0.12) | 97.8 | 95.9 | 7.0 (4.8–9.5) | yes |
| S6 Order LightGBM | 4 | 20.2 (14.9–26.0) | −6.4 (0.00) | 93.7 | 92.3 | 2.3 (1.5–3.2) | yes |
| S7 SC GRU | 4 | 8.0 (4.4–12.2) | −18.7 (<0.001) | 93.9 | 96.2 | 1.5 (0.5–2.6) | yes |
| B8 LightGBM, 95% spec | 4 | 44.9 (36.6–53.2) | +18.2 (<0.001) | 90.0 | 86.9 | 21.7 (17.3–26.1) | **no** |
| D1 Trend | 5 | 40.0 (32.2–47.9) | — | 97.6 | 94.5 | 4.5 (2.0–7.2) | yes |
| D7 Event analysis | 5 | 32.7 (24.8–41.4) | −7.3 (0.36) | 90.9 | 93.9 | 0.9 (0.0–2.1) | yes |
| S1 SC trend | 5 | 40.4 (32.4–48.4) | +0.4 (1.00) | 97.6 | 94.5 | 4.6 (2.1–7.4) | yes |
| S2 SC rate | 5 | 24.7 (18.1–32.4) | −15.3 (0.00) | 94.5 | 96.9 | 0.6 (0.4–0.8) | yes |
| S3 SC PoPLR | 5 | 39.6 (31.3–47.8) | −0.4 (1.00) | 96.1 | 92.3 | 0.5 (0.0–1.3) | yes |
| S4 SC event | 5 | 18.7 (12.4–25.2) | −21.3 (<0.001) | 95.7 | 97.1 | 0.0 (0.0–0.0) | yes |
| S5 SC LightGBM | 5 | 28.9 (22.3–36.1) | −11.1 (0.05) | 98.2 | 94.8 | 7.6 (5.0–10.5) | **no** |
| S6 Order LightGBM | 5 | 35.1 (28.6–42.2) | −4.9 (0.41) | 96.3 | 92.7 | 2.8 (1.8–4.0) | yes |
| S7 SC GRU | 5 | 18.2 (12.6–24.7) | −21.8 (<0.001) | 95.9 | 96.3 | 2.2 (0.9–3.8) | yes |
| B8 LightGBM, 95% spec | 5 | 58.9 (51.7–66.4) | +18.9 (<0.001) | 90.9 | 86.1 | 26.4 (20.9–31.8) | **no** |
| D1 Trend | 6 | 57.3 (49.0–66.4) | — | 99.4 | 94.8 | 5.5 (2.9–8.4) | yes |
| D7 Event analysis | 6 | 46.0 (37.8–54.7) | −11.3 (0.02) | 89.0 | 91.0 | 1.5 (0.3–3.1) | yes |
| S1 SC trend | 6 | 56.7 (48.4–65.6) | −0.7 (1.00) | 99.4 | 95.1 | 5.5 (2.9–8.4) | yes |
| S2 SC rate | 6 | 34.0 (26.7–41.9) | −23.3 (<0.001) | 97.0 | 97.7 | 0.5 (0.4–0.7) | yes |
| S3 SC PoPLR | 6 | 47.8 (39.1–56.9) | −9.6 (0.08) | 97.4 | 90.6 | 0.1 (0.0–0.3) | yes |
| S4 SC event | 6 | 22.2 (15.8–29.2) | −35.1 (<0.001) | 99.0 | 99.1 | 0.0 (0.0–0.0) | yes |
| S5 SC LightGBM | 6 | 59.6 (51.1–68.5) | +2.2 (1.00) | 99.0 | 94.5 | 2.6 (1.1–4.4) | yes |
| S6 Order LightGBM | 6 | 54.2 (46.5–62.4) | −3.1 (1.00) | 97.0 | 91.2 | 4.4 (2.8–6.4) | yes |
| S7 SC GRU | 6 | 20.7 (14.8–27.4) | −36.7 (<0.001) | 95.7 | 96.3 | 1.6 (0.5–2.9) | yes |
| B8 LightGBM, 95% spec | 6 | 79.3 (72.7–86.2) | +22.0 (<0.001) | 88.8 | 79.0 | 15.3 (11.5–19.1) | **no** |

*Table 2. Study 2: sensitivity (R1 progressors, n = 150), specificity against R1-stable (n = 164) and flat-stable (R2, n = 310) eyes, and false-alarm rate on true no-change series, by number of tests k. Values are means over folds and seeds; 95% CIs from patient-level bootstrap. Gain: paired difference in sensitivity versus D1 (percentage points), with Holm-adjusted exact McNemar p (B8 unadjusted). "Valid": lower limit of the false-alarm CI at or below 5% and upper limit at or below 10%. SC, shuffle-calibrated.*

## Study 2: repeated reviews

Applied at every review from the third to the sixth test, D1 flagged 64.7% of progressors by the sixth test, but also 15.2% (95% CI 6.5–25.9%) of true no-change series (Table 3, Fig. 4). Detectors designed to keep cumulative false alarms at 5% did so on true no-change data (between 0.0% and 5.3%), but flagged fewer progressors by the sixth test: 47.6% for the confirmed trend test (difference −17.1 percentage points; 95% CI −23.7 to −11.1) and 41.3% for the sequential trend test. Event analysis applied at every review flagged 46.0% of progressors with 2.0% cumulative false alarms. None of the repeated-review detectors was non-inferior to D1 within the 10-point margin, so H8 was rejected: lowering cumulative false alarms to 5% or less cost between 17.1 and 52.0 percentage points of detection by the sixth test.

| Detector | Progressors flagged by test 6, % (95% CI) | Difference vs D1, pp (95% CI) | Flat-stable eyes flagged, % | True no-change series flagged, % (95% CI) |
|---|---|---|---|---|
| D1 trend, every review | 64.7 (56.8–72.8) | — | 14.5 | 15.2 (6.5–25.9) |
| D7 event, every review | 46.0 (37.8–54.7) | −18.7 (−25.8 to −11.0) | 9.0 | 2.0 (0.0–6.0) |
| Q1 Sequential trend | 41.3 (33.8–49.8) | −23.3 (−30.5 to −16.2) | 5.3 | 5.3 (1.1–10.8) |
| Q2 Confirmed trend | 47.6 (39.0–56.4) | −17.1 (−23.7 to −11.1) | 5.9 | 5.0 (1.0–10.0) |
| Q3 Confirmed SC event | 12.7 (7.6–18.4) | −52.0 (−60.5 to −43.9) | 2.3 | 0.0 (0.0–0.0) |
| Q4 Sequential order LightGBM | 38.9 (31.8–46.8) | −25.8 (−32.2 to −19.1) | 7.4 | 1.1 (0.4–1.8) |

*Table 3. Study 2: repeated reviews at three, four, five and six tests. Share of R1 progressors and of flat-stable (R2) eyes flagged at least once by the sixth test, and share of true no-change series flagged at least once over the same reviews. Difference: versus D1 applied at every review, with 95% CI.*

## External clinic

In GRAPE (Table 4), LightGBM with its usual threshold had a specificity of only 74.1% against the mean-deviation label at three tests. With shuffle-calibrated UWHVF thresholds, specificity rose to 83.5%, and with local recalibration on GRAPE's own records it reached 93.2% (95% CI 90.7–95.3%), supporting H9. However, the sensitivity of the recalibrated model fell to 7.4%, compared with 44.4% for D1, whose specificity was 95.3%. The calibrated trend statistic behaved like D1 with either threshold.

| Detector | k | Sensitivity, % (95% CI) | Specificity, % (95% CI) |
|---|---|---|---|
| D1 Trend | 3 | 44.4 (25.9–65.4) | 95.3 (92.2–97.9) |
| B8 LightGBM, 95% spec (UW threshold) | 3 | 36.5 (24.0–50.5) | 74.1 (69.7–78.4) |
| S1 SC trend, UW threshold | 3 | 46.4 (27.6–66.7) | 95.3 (92.2–97.9) |
| S1 SC trend, local threshold | 3 | 44.4 (25.9–65.4) | 95.2 (92.1–97.9) |
| S5 SC LightGBM, UW threshold | 3 | 24.0 (13.8–35.3) | 83.5 (80.1–87.0) |
| S5 SC LightGBM, local threshold | 3 | 7.4 (2.1–14.6) | 93.2 (90.7–95.3) |
| S6 Order LightGBM, UW threshold | 3 | 13.1 (5.4–22.1) | 96.7 (95.1–98.1) |
| S6 Order LightGBM, local threshold | 3 | 18.5 (9.4–28.7) | 95.0 (93.2–96.6) |
| D1 Trend | 4 | 33.3 (11.8–52.9) | 95.9 (92.4–98.7) |
| B8 LightGBM, 95% spec (UW threshold) | 4 | 70.4 (58.2–82.7) | 60.0 (53.2–66.3) |
| S1 SC trend, UW threshold | 4 | 33.3 (11.8–52.9) | 94.9 (91.2–97.9) |
| S1 SC trend, local threshold | 4 | 33.3 (11.8–52.9) | 94.6 (90.8–97.7) |
| S5 SC LightGBM, UW threshold | 4 | 36.3 (22.7–52.2) | 82.7 (77.2–87.8) |
| S5 SC LightGBM, local threshold | 4 | 16.7 (8.9–25.9) | 92.2 (88.8–95.0) |
| S6 Order LightGBM, UW threshold | 4 | 22.2 (9.6–35.3) | 94.0 (91.2–96.4) |
| S6 Order LightGBM, local threshold | 4 | 23.0 (10.2–36.1) | 93.1 (90.1–95.6) |

*Table 4. Study 2, external clinic (GRAPE): agreement with the data set's mean-deviation progression label (27 labelled progressors and 236 non-progressors at three tests). UW threshold: calibrated on UWHVF; local threshold: recalibrated on GRAPE's own shuffled series by patient-level cross-fitting. Means over UWHVF folds and seeds; 95% CIs from patient-level bootstrap.*

# Discussion

Our main finding is that, once detectors were held to the same false-alarm rate, none detected more glaucomatous visual-field progression than a plain trend test of mean sensitivity. This was true for permutation, event-based, supervised machine-learning and self-supervised detectors, from the third to the sixth test, and the study had enough eyes to exclude gains of 8.4 percentage points or more. By contrast, a machine-learning detector thresholded in the usual way appeared up to 22.0 points more sensitive, because it raised false alarms in up to 26.4% of series in which nothing had changed. The apparent advantage was a choice of operating point, not a better detector.

Why does the usual threshold mislead? Setting a threshold at 95% specificity in labelled stable eyes controls false alarms only in eyes like those eyes. Labelled stable eyes are selected by their long-term course; in our data they had flat or improving slopes. Eyes seen at an ordinary review, and short series in particular, are noisier. Stability limits based on stable eyes are widely used [18, 21], and labels themselves vary between studies [26]. Shuffle calibration sidesteps both problems: it uses every eye in the clinic's records, needs no labels, and keeps each eye's own noise and test dates. In our data it brought machine-learning false alarms close to the target on true no-change data that it had never seen. It is simple enough for any clinic or software vendor to apply.

These results fit with what is known about the information in a few visual fields. In routine care, the third test came a median of 2.1 years after the first and the sixth a median of 5.9 years after the first. With so few, noisy measurements, a well-calibrated linear trend appears to capture most of the available signal. Earlier work has shown that the number and timing of tests largely determine how quickly progression can be confirmed [5, 6, 24, 25]. More tests early in follow-up [34] or risk-guided scheduling [22, 35] are therefore more promising ways to gain time than more complex detection rules, although we did not test them.

The repeated-review analysis shows a trade-off that single-review studies hide. Applied at every review, the trend test flagged 64.7% of progressors by the sixth test, but also 15.2% of series in which glaucoma had not changed. Requiring confirmation at two consecutive reviews kept cumulative false alarms at 5% but missed 25 of the 97 progressors that the unconfirmed test found by the sixth test. Neither choice is right for every patient. A clinician may accept more false alarms in an eye at high risk, and fewer in an eye with mild, stable disease. Detectors should therefore report their cumulative false-alarm rate, so that the choice can be made explicitly. Event and trend methods [8] and different event criteria [12] have been compared before; our simplified event analysis was not Guided Progression Analysis, and its low false-alarm rate needs confirmation with the commercial software.

The external results add a practical warning. A model trained in one clinic and moved to another clinic and perimeter lost specificity. Local recalibration on the new clinic's shuffled records restored specificity, but in our data the model then detected few progressors, while the plain trend test kept its performance without any recalibration. Transferring a complex detector is therefore riskier than transferring a simple one.

Within-eye permutation methods such as PoPLR are valid by design [10] but cannot flag any eye with three tests, because there are only six possible orders. Pooling the permutation reference across patients removes this floor [30–33]; in Study 2, the pooled PoPLR statistic was conservative on true no-change data and matched the trend test at three to five tests. The self-supervised order model, which learns what a real time order looks like from thousands of unlabelled eyes, also matched the trend test at three tests. Neither improved on it. We had already seen excess false alarms for a pooled and detrended method during development, so the Study 1 finding about that method is a confirmation on locked test data rather than a new discovery; the Study 2 analyses were all new.

Our study has limitations. First, the reference standard was based on the long-term slope of mean deviation, which may favour the trend test. The future-only and flat-stable references, which address incorporation bias and the improving-eye problem, did not change the conclusions, but a reference based on expert review of whole series would be stronger. Second, the true no-change arm had only 30 patients, mostly with early to moderate damage, tested over about three months, with test dates borrowed from routine care. It lacks long-term fluctuation, so false alarms in eyes with advanced damage may be higher. Third, the Study 2 protocol was written after the Study 1 results were known, and neither protocol was registered externally; in Study 1, we also changed how the validity rule was applied after seeing the results (the conclusions hold under the strict rule). Fourth, UWHVF does not include diagnoses or reliability indices. Fifth, GRAPE used a different perimeter, had only 27 labelled progressing eyes, and its labels came from criteria applied to the whole series. Sixth, our machine-learning detectors used summary features or a small recurrent network with a modest tuning budget; larger models such as deep forecasting [19, 20] or diffusion models [23], Bayesian spatial models [13–15] and smoothing methods [36] were not tested. Shuffle calibration can be applied to any of them, and our results predict that their advantages will shrink at matched false alarms. Finally, we did not measure the clinical consequences of false alarms or delayed detection.

# Conclusions

Across two studies, three data sources and 21 detector variants, apparent gains in early detection of glaucomatous visual-field progression disappeared when false alarms were matched. A plain trend test of mean sensitivity was as sensitive as machine-learning, permutation and event-based detectors at the same false-alarm rate. Detectors should be compared, and deployed, at a stated false-alarm rate, measured on shuffled or true no-change data and reported per review and over repeated reviews. Shuffle calibration offers a simple way to do this with a clinic's own records.

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

All three data sets analysed are publicly available from their custodians: UWHVF (https://github.com/uw-biomedical-ml/uwhvf), GRAPE (figshare file https://ndownloader.figshare.com/files/41670009, described in Huang et al., Sci Data 2023) and the Artes retest data (visualFields R package version 1.0.7 on CRAN). The analysis code, the two time-stamped protocols, the patient-level split and fold assignments, and all raw detector outputs are available from the corresponding author on reasonable request.

# References

1. Tham YC, Li X, Wong TY, Quigley HA, Aung T, Cheng CY. Global Prevalence of Glaucoma and Projections of Glaucoma Burden through 2040. Ophthalmology. 2014;121(11):2081-2090. https://doi.org/10.1016/j.ophtha.2014.05.013

2. Weinreb RN, Aung T, Medeiros FA. The Pathophysiology and Treatment of Glaucoma. JAMA. 2014;311(18):1901. https://doi.org/10.1001/jama.2014.3192

3. Heijl A, Leske MC, Bengtsson B, Hyman L, Bengtsson B, Hussein M; Early Manifest Glaucoma Trial Group. Reduction of intraocular pressure and glaucoma progression: results from the Early Manifest Glaucoma Trial. Arch Ophthalmol. 2002;120(10):1268-1279. https://doi.org/10.1001/archopht.120.10.1268

4. Gardiner SK, Swanson WH, Goren D, Mansberger SL, Demirel S. Assessment of the Reliability of Standard Automated Perimetry in Regions of Glaucomatous Damage. Ophthalmology. 2014;121(7):1359-1369. https://doi.org/10.1016/j.ophtha.2014.01.020

5. Chauhan BC, Garway-Heath DF, Goni FJ, Rossetti L, Bengtsson B, Viswanathan AC, et al. Practical recommendations for measuring rates of visual field change in glaucoma. British Journal of Ophthalmology. 2008;92(4):569-573. https://doi.org/10.1136/bjo.2007.135012

6. Stagg BC, Brintz BJ, Stein JD, Hess R, Kawamoto K, Jammal AA, et al. Time to Identify Glaucoma Progression Given Typical Visual Field Testing Frequencies in a US Nationwide Insured Population. Ophthalmology Glaucoma. 2026;9(3):250-256. https://doi.org/10.1016/j.ogla.2025.11.004

7. Foot B, MacEwen C. Surveillance of sight loss due to delay in ophthalmic treatment or review: frequency, cause and outcome. Eye. 2017;31(5):771-775. https://doi.org/10.1038/eye.2017.1

8. Wu Z, Medeiros FA. Comparison of Visual Field Point-Wise Event-Based and Global Trend-Based Analysis for Detecting Glaucomatous Progression. Trans. Vis. Sci. Tech.. 2018;7(4):20. https://doi.org/10.1167/tvst.7.4.20

9. Bengtsson B, Heijl A. A Visual Field Index for Calculation of Glaucoma Rate of Progression. American Journal of Ophthalmology. 2008;145(2):343-353. https://doi.org/10.1016/j.ajo.2007.09.038

10. O'Leary N, Chauhan BC, Artes PH. Visual Field Progression in Glaucoma: Estimating the Overall Significance of Deterioration with Permutation Analyses of Pointwise Linear Regression (PoPLR). Invest. Ophthalmol. Vis. Sci.. 2012;53(11):6776. https://doi.org/10.1167/iovs.12-10049

11. Artes PH, O'Leary N, Nicolela MT, Chauhan BC, Crabb DP. Visual field progression in glaucoma: what is the specificity of the Guided Progression Analysis? Ophthalmology. 2014;121(10):2023-2027. https://doi.org/10.1016/j.ophtha.2014.04.015

12. Heijl A, Bengtsson B, Chauhan BC, Lieberman MF, Cunliffe I, Hyman L, et al. A Comparison of Visual Field Progression Criteria of 3 Major Glaucoma Trials in Early Manifest Glaucoma Trial Patients. Ophthalmology. 2008;115(9):1557-1565. https://doi.org/10.1016/j.ophtha.2008.02.005

13. Zhu H, Crabb DP, Ho T, Garway-Heath DF. More Accurate Modeling of Visual Field Progression in Glaucoma: ANSWERS. Invest. Ophthalmol. Vis. Sci.. 2015;56(10):6077. https://doi.org/10.1167/iovs.15-16957

14. Marín-Franch I, Artes PH, Turpin A, Racette L. Visual Field Progression in Glaucoma: Comparison Between PoPLR and ANSWERS. Trans. Vis. Sci. Tech.. 2021;10(14):13. https://doi.org/10.1167/tvst.10.14.13

15. Montesano G, Garway-Heath DF, Ometto G, Crabb DP. Hierarchical Censored Bayesian Analysis of Visual Field Progression. Trans. Vis. Sci. Tech.. 2021;10(12):4. https://doi.org/10.1167/tvst.10.12.4

16. Saeedi O, Boland MV, D'Acunto L, Swamy R, Hegde V, Gupta S, et al. Development and Comparison of Machine Learning Algorithms to Determine Visual Field Progression. Trans. Vis. Sci. Tech.. 2021;10(7):27. https://doi.org/10.1167/tvst.10.7.27

17. Dixit A, Yohannan J, Boland MV. Assessing Glaucoma Progression Using Machine Learning Trained on Longitudinal Visual Field and Clinical Data. Ophthalmology. 2021;128(7):1016-1026. https://doi.org/10.1016/j.ophtha.2020.12.020

18. Wang M, Shen LQ, Pasquale LR, Petrakos P, Formica S, Boland MV, et al. An Artificial Intelligence Approach to Detect Visual Field Progression in Glaucoma Based on Spatial Pattern Analysis. Invest. Ophthalmol. Vis. Sci.. 2019;60(1):365. https://doi.org/10.1167/iovs.18-25568

19. Wen JC, Lee CS, Keane PA, Xiao S, Rokem AS, Chen PP, et al. Forecasting future Humphrey Visual Fields using deep learning. PLoS ONE. 2019;14(4):e0214875. https://doi.org/10.1371/journal.pone.0214875

20. Berchuck SI, Mukherjee S, Medeiros FA. Estimating rates of progression and predicting future visual fields in glaucoma using a deep variational autoencoder. Sci Rep. 2019;9(1):18113. https://doi.org/10.1038/s41598-019-54653-6

21. Yousefi S, Balasubramanian M, Goldbaum MH, Medeiros FA, Zangwill LM, Weinreb RN, et al. Unsupervised Gaussian Mixture-Model With Expectation Maximization for Detecting Glaucomatous Progression in Standard Automated Perimetry Visual Fields. Trans. Vis. Sci. Tech.. 2016;5(3):2. https://doi.org/10.1167/tvst.5.3.2

22. Chen L, Fujita A, Moradi M, Eslami M, Elze T, Zebardast N. Earlier confirmation of glaucoma progression with risk-weighted visual field and OCT scheduling. medRxiv. 2026. https://doi.org/10.64898/2026.11.16.26368187

23. Si W, Lin V, Sun B, Jang KJ, Xing R, Saeed A, et al. Reliable and Interpretable Visual Field Progression Prediction with Diffusion Models and Conformal Risk Control. Lecture Notes in Computer Science. 2025:543-552. https://doi.org/10.1007/978-3-032-05182-0_53

24. Wu Z, Saunders LJ, Daga FB, Diniz-Filho A, Medeiros FA. Frequency of Testing to Detect Visual Field Progression Derived Using a Longitudinal Cohort of Glaucoma Patients. Ophthalmology. 2017;124(6):786-792. https://doi.org/10.1016/j.ophtha.2017.01.027

25. Crabb DP, Garway-Heath DF. Intervals between Visual Field Tests When Monitoring the Glaucomatous Patient: Wait-and-See Approach. Invest. Ophthalmol. Vis. Sci.. 2012;53(6):2770. https://doi.org/10.1167/iovs.12-9476

26. Kim H, Kim E, Moon S, Jin SW, Kim JL, Lee SU, et al. Labeling matters: A multicenter machine learning study on visual field progression in Glaucoma. PLoS One. 2026;21(8):e0357179. https://doi.org/10.1371/journal.pone.0357179

27. Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378

28. Montesano G, Chen A, Lu R, Lee CS, Lee AY. UWHVF: A Real-World, Open Source Dataset of Perimetry Tests From the Humphrey Field Analyzer at the University of Washington. Trans. Vis. Sci. Tech.. 2022;11(1):2. https://doi.org/10.1167/tvst.11.1.1

29. Huang X, Kong X, Shen Z, Ouyang J, Li Y, Jin K, et al. GRAPE: A multi-modal dataset of longitudinal follow-up visual field and fundus images for glaucoma management. Sci Data. 2023;10(1):520. https://doi.org/10.1038/s41597-023-02424-4

30. Angelopoulos AN, Bates S. Conformal Prediction: A Gentle Introduction. Foundations and Trends® in Machine Learning. 2023;16(4):494-591. https://doi.org/10.1561/2200000101

31. Freedman D, Lane D. A Nonstochastic Interpretation of Reported Significance Levels. Journal of Business & Economic Statistics. 1983;1(4):292-298. https://doi.org/10.1080/07350015.1983.10509354

32. Gagnon-Bartsch J, Shem-Tov Y. The classification permutation test: A flexible approach to testing for covariate imbalance in observational studies. Ann. Appl. Stat.. 2019;13(3):1464-1483. https://doi.org/10.1214/19-aoas1241

33. Phipson B, Smyth GK. Permutation P-values Should Never Be Zero: Calculating Exact P-values When Permutations Are Randomly Drawn. Statistical Applications in Genetics and Molecular Biology. 2010;9(1). https://doi.org/10.2202/1544-6115.1585

34. Phu J, Kalloniatis M. The Frontloading Fields Study (FFS): Detecting Changes in Mean Deviation in Glaucoma Using Multiple Visual Field Tests Per Clinical Visit. Trans. Vis. Sci. Tech.. 2021;10(13):21. https://doi.org/10.1167/tvst.10.13.21

35. Schell GJ, Lavieri MS, Helm JE, Liu X, Musch DC, Van Oyen MP, et al. Using Filtered Forecasting Techniques to Determine Personalized Monitoring Schedules for Patients with Open-Angle Glaucoma. Ophthalmology. 2014;121(8):1539-1546. https://doi.org/10.1016/j.ophtha.2014.02.021

36. Mohammadzadeh V, Li L, Fei Z, Davis T, Morales E, Wu K, et al. Efficacy of Smoothing Algorithms to Enhance Detection of Visual Field Progression in Glaucoma. Ophthalmology Science. 2024;4(2):100423. https://doi.org/10.1016/j.xops.2023.100423