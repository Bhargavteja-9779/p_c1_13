# How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? A Benchmark With True No-Change Calibration

**Running title:** False alarms in visual-field progression detection

**Authors:** P N Bhargav Teja¹; Rajay Vedaraj I S¹∗

¹ Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India

**Corresponding author (marked ∗):** Rajay Vedaraj I S, Vellore Institute of Technology (VIT), Vellore 632014, Tamil Nadu, India. E-mail: rajay@vit.ac.in

**Article type:** Original Research

# Abstract

**Introduction:** Clinicians escalate glaucoma treatment when visual fields worsen. New detectors claim earlier detection, but few are checked on eyes that truly did not change. We asked how early progression can be detected without excess false alarms, and whether calibrating detectors on no-change data changes their ranking.

**Methods:** Ten detectors saw only the first 3–6 tests of each eye. Sensitivity was measured against a whole-series reference in a held-out University of Washington test set (26 progressors, 26 stable eyes); false alarms on 30 patients tested weekly for 12 weeks (true no change); agreement in 263 external eyes (GRAPE, China). In a pre-specified extension, five detectors were re-thresholded on retest data or on shuffled clinic records and compared at matched false-alarm rates.

**Results:** With three tests, a pooled conformal detector and a gradient-boosted tree model raised false alarms on 22.4% and 27.7% of no-change series, against 4.4% for the trend of mean sensitivity (D1), although all looked similarly specific on reference-stable eyes. After retest calibration, every detector had about 5% false alarms, and the conformal and machine-learning detectors no longer flagged significantly more progressors than D1 (differences −19.2 to +19.2 percentage points). A retest-calibrated rate-of-change score flagged 73.1% of progressors with five tests (+30.8 percentage points vs D1; 95% CI 14.8 to 50.0; Holm-adjusted p = 0.031), but at lower specificity in clinic stable eyes, and its threshold was about 3.0 times larger when set on shuffled clinic records, where it flagged fewer progressors than D1. D1's false-alarm rate stayed near 5% under every no-change source tested.

**Conclusion:** Apparent early-detection gains largely reflected where the threshold was set, not better discrimination. Detectors should be calibrated and compared on no-change data that match clinical test intervals.

**Keywords:** Benchmark; Calibration; False alarm; Glaucoma; Machine learning; Perimetry; Progression; Visual field

# Key Summary Points

**Why carry out this study?**

- New methods claim to detect glaucomatous visual-field progression earlier, but their false-alarm rates are rarely measured on eyes that truly did not change.
- We tested the hypothesis that no detector would flag substantially more future-confirmed progressors than the trend of mean sensitivity without excess false alarms.

**What was learned from the study?**

- With three tests, the most sensitive conformal and machine-learning detectors raised false alarms on 22.4% and 27.7% of true no-change series, although they looked specific on reference-stable eyes.
- When every detector was calibrated to the same false-alarm rate on retest data, the conformal and machine-learning detectors no longer flagged significantly more progressors than the simple trend test.
- A calibrated rate-of-change rule was more sensitive but less specific in clinic eyes, and its ranking depended on which no-change data set its threshold; the trend test kept a false-alarm rate near 5% under every no-change source tested.

# Plain Language Summary

Glaucoma damages the side vision slowly. Doctors use repeated visual field tests to see whether it is getting worse, and if it is, they step up treatment. Each test is noisy, so deciding early is hard. Many new computer methods claim to spot worsening sooner. We checked ten such methods in a new way: we also gave them test results from patients who were tested every week for 12 weeks. Glaucoma does not change in 12 weeks, so any "worsening" found in these patients is a false alarm. With only three tests, two of the newer methods that looked best raised false alarms in 22.4% and 27.7% of these test series, even though they looked accurate in the usual check. The simplest method, a straight line through the average sensitivity, raised false alarms at about the expected rate. When we adjusted every method so that it raised the same number of false alarms, the newer methods no longer found clearly more true worsening than the simple method. A rule based on the speed of loss looked better, but only when it was tuned on tests repeated a week apart, which are less noisy than yearly clinic tests. Our study was small. In a clinic in China, which method looked best depended on how worsening was defined. Patients and doctors should be careful with new methods that report earlier detection unless their false-alarm rate on stable eyes is known.

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [4]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [5], but routine care rarely reaches this frequency [6]. Delays in follow-up are a documented cause of avoidable sight loss [7].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [8, 9], sometimes after spatial or temporal smoothing [10]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [11–13]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [8]. Bayesian and spatial models share information across locations or patients [14–16]. Machine-learning models have been trained to classify or forecast progression [17–22], and newer studies use deep generative models or risk-based test scheduling [23–25].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [11]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [26]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

Artes and colleagues used short-interval retest data to measure the false-alarm rate of the event-based Guided Progression Analysis [11]. We extend this approach to trend, permutation, conformal and machine-learning detectors, and add a future-confirmed reference and an external clinic. We built an open benchmark to answer one practical question: how early can visual-field progression be detected without excess false alarms? We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We tested the hypothesis that no detector would flag substantially more future-confirmed progressors (by 10 percentage points or more) than the simple trend test of mean sensitivity without excess false alarms on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate. Finally, in a pre-specified extension, we re-set each detector's threshold on no-change data, so that all detectors could be compared at the same false-alarm rate, and asked whether the ranking depends on which no-change data are used.

# Methods

## Study Design and Reporting

This was a retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [27]. The analysis plan, including the ten detectors, thresholds, reference standards, research questions and statistical tests, was committed to the project repository before the final run (`experiments/protocol.md`). It was not registered in a public registry. Deviations from the plan are listed in Table 4.

The plan was written after a development phase in which we tried, and abandoned, several new detection methods (Supplementary Material S1). That phase used the Artes retest data once, and it already showed that the pooled-detrended conformal detector (D6) raised many false alarms on these data. The D6 result on the true no-change arm is therefore not a confirmatory finding. The UWHVF test set and the GRAPE labels were not used during development. A short software check ("quick mode") run before the final protocol amendments did process the Artes and GRAPE files; its outputs were not used to choose any detector, threshold or reference.

## Data Sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains 28,943 24-2 tests from 7,428 eyes of 3,871 patients seen in routine care in Seattle, USA [28]. It includes sensitivities, total deviation values, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. Eyes with at least three tests were used (2,643 training, 940 validation and 869 test eyes). The test set was used once, for the final analysis. Note that D1 and D2 use mean sensitivity, whereas the reference below uses mean total deviation (the unweighted mean of total-deviation values, not the instrument's weighted MD).

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [11]. Glaucoma does not change measurably in 12 weeks, so any "progression" flag in these series is a false alarm. The data (360 tests from 30 eyes) are distributed with the visualFields R package (version 1.0.7).

*GRAPE (external clinic).* The GRAPE data set contains 1,115 follow-up visual-field records from 263 eyes of 144 patients with glaucoma followed in Hangzhou, China [29]. Fields were measured with a different perimeter (59 analysable points after removing untested points). Each eye carries progression labels assigned with three criteria: mean deviation, and two pointwise linear regression rules. These labels were assigned by rule-based criteria, not by clinical judgement. We used the mean-deviation label as the primary label (27 progressing eyes) and the PLR2 label (40 progressing eyes) as the main secondary label, because it is not based on mean deviation.

## Reference Standard (UWHVF)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5. Other eyes were excluded from the sensitivity and specificity analysis. By this definition every reference-stable eye had a non-negative long-term slope (median 0.07 dB per year; progressors −0.54 dB per year). The reference uses the whole series, including the first k tests seen by the detectors. This overlap (incorporation) favours detectors based on mean sensitivity, such as D1. We therefore also report an exploratory future-only reference built from tests k+1 to the end (Supplementary Table S5). Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations), which is not tied to mean deviation.

## Detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 OLS-MD:** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD rate:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [8], using all possible orders of the k tests.
- **D5 pooled-shuffle conformal test:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of training-set eyes with the same number of tests and similar mean sensitivity (a conformal p-value [30, 31]).
- **D6 pooled-detrended conformal regional test:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [32]. This variant was the most sensitive approach during development.
- **D7 event analysis:** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to Guided Progression Analysis [13]. It uses raw sensitivity, not pattern deviation, so it is a simplified analogue rather than a re-implementation of the commercial software.
- **D8 machine learning, tabular:** gradient-boosted trees (LightGBM) on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set reference-stable eyes. These two models are deliberately simple baselines with a fixed tuning budget, not reproductions of published models.
- **D9 machine learning, sequence:** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 self-supervised order network:** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [33].

Detectors with a random component (D5, D6, D8–D10) were run with five seeds; D4 is exact for up to seven tests and gave identical results for every seed. For each eye, the flag was averaged over seeds. With three tests there are only six possible orders, so D4 and D10 cannot reach p < 0.05; this is a property of the methods, not a failure of the code. D7 also needs at least four tests. These three detectors are reported as not applicable with three tests and are excluded from counts and tests at that number.

## Evaluation

*E1 future reference.* In UWHVF test-set eyes with at least eight tests, we measured sensitivity (share of reference progressors flagged) and specificity (share of reference-stable eyes not flagged) using only the first k tests.

*E2 true no-change.* In the Artes data we took every window of k consecutive tests. Because rate-based rules depend on the time scale, each window was given the test dates of a randomly chosen UWHVF test-set eye (ten draws per window; amendment A1). The share of windows flagged is the false-alarm rate.

*E3 shuffle audit.* In UWHVF test-set eyes, we randomly re-ordered the first k tests (ten times) and re-ran each detector. Shuffling removes any true trend, so the flag rate estimates the false-alarm rate without retest data.

*E4 external clinic.* In GRAPE, we applied the detectors to the first three or four tests of each eye and compared flags with the clinicians' labels. D5 and D7 were re-calibrated on GRAPE itself by five-fold patient-level cross-fitting, because the perimeter differs; D8 was transferred unchanged from UWHVF; the 24-2-specific detectors (D6, D9, D10) were not applied (amendment A2).

*Real-world measures.* We translated results into two clinical units, as planned: the number of false progression flags per 1,000 stable eyes at each review, and the number of tests until a future-confirmed progressor is first flagged. For the second measure, an eye counted as flagged by test k if any review with 3 to k tests flagged it. Because clinics review the same eye repeatedly, we also report, as an exploratory measure, the share of true no-change series flagged at least once when reviewed after 3, 4, 5 and 6 tests.

## No-Change Calibration and Matched Comparison (Amendment B)

After the first round of results and peer review, we wrote and time-stamped a second amendment before running it (`experiments/protocol.md`, amendment B). For five detectors with a continuous score (D1 trend statistic; D2 minus the slope of mean sensitivity; D6 worst regional trend statistic; D8 and D9 model outputs), we replaced the original threshold by the 95th percentile of the score on no-change series. Two label-free sources were compared. Retest calibration (RC) used the Artes windows, with five-fold patient-level cross-fitting so that each window was judged with a threshold from other patients. Shuffle calibration (SC) used the clinic's own training eyes with their first k tests randomly re-ordered, which needs neither labels nor retest data. Pre-stated hypotheses were: HB1, after RC no detector has excess false alarms; HB2, after SC at least 75% of detector–test-number cells are within 3 percentage points of 5%; HB3, at RC-matched false-alarm rates no detector flags 10 percentage points or more progressors than RC-calibrated D1 with a Holm-adjusted p < 0.05. Amendment B also re-estimated the untrained detectors (D1–D4) on all UWHVF eyes with a reference label, and tested the time-label assumption (amendment A1) by giving the retest series annual spacing or the dates of reference-stable eyes.

## Statistical Analysis

For each eye or window, the flag was averaged over seeds; proportions and paired differences use these averaged flags. Proportions are reported with 95% confidence intervals (CIs) from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. Paired differences from D1 use the same patient-level bootstrap. Exact McNemar tests require one flag per eye, so they use the majority flag over seeds. We corrected p-values with the Holm method within each number of tests and endpoint, over the detectors that can flag at that number. With 26 progressors, only differences of about 35 percentage points or more could reach significance after correction (all discordant pairs favouring one detector), so we interpret the comparisons mainly through their CIs.

The protocol required the false-alarm CI on true no-change data to be judged against the nominal 5%, without fixing an exact rule. We report three rules (Table 4). The main rule, used in the text, is "excess false alarms": the whole 95% CI lies above 5%. This rule does not depend on the choice of a margin. We also report an operational validity rule (upper CI limit at most 10% and lower limit at most 5%), written into the methods draft while the final run was in progress, and the literal reading of the protocol (upper CI limit at most 5%), under which no detector that works at the nominal level, including D1, could be called valid with 30 retest patients.

Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells, with a CI from 500 joint bootstrap resamples of retest and UWHVF patients, and by their absolute difference. Analyses used Python 3.13 with NumPy, SciPy, scikit-learn, LightGBM and PyTorch. The code runs the benchmark (`run_all.py --mode full`) and then generates every statistic, table and figure from the saved per-eye outputs. A second, independent run in a fresh computing environment reproduced all 1,106,158 per-eye detector outputs exactly (0 differences).

## Ethics

This study used only publicly available, de-identified data sets released by their custodians (UWHVF: BSD-3 licence; GRAPE: CC0; Artes data: distributed with the visualFields R package, Apache-2.0 licence). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

# Results

## Study Data

In the UWHVF test set, 132 eyes had at least eight tests. Of these, 26 were reference progressors, 26 were reference stable and 80 were indeterminate. The reference eyes came from 41 patients. Their median age at the first test was 58.8 years (interquartile range [IQR] 50.3–64.4), median mean total deviation at the first test was −4.4 dB (IQR −6.0 to −3.2), and median follow-up was 12.9 years with 11 tests. The median interval between tests was 1.0 years. Progressors had a median whole-series slope of −0.54 dB per year, so most were slow progressors. The true no-change arm contributed 3,000 three-test windows (including time-label draws). In GRAPE, all 263 eyes had at least three visits and 163 had at least four.

## False Alarms on True No-Change Data (RQ1)

Table 1 and Fig. 2 show all results. With three tests, D6, D8 and D9 had excess false alarms. The pooled-detrended conformal detector (D6) raised false alarms on 22.4% (95% CI 19.3–25.7%) of no-change series, the tabular machine-learning model (D8) on 27.7% (95% CI 22.7–32.9%), and the sequence model (D9) on 12.7% (95% CI 6.2–20.0%). The simple trend test (D1) stayed close to its nominal level, at 4.4% (95% CI 2.8–6.3%). D8 still had excess false alarms with four tests, at 9.4% (95% CI 6.3–12.9%), and with five tests, at 18.8% (95% CI 13.1–24.9%), but not with six, at 3.6% (95% CI 1.7–6.0%). Under the operational validity rule, the invalid detectors were D6, D8 and D9 with three tests, D8 with four, D8 and D9 with five and D6 and D9 with six; D9 with six tests, at 5.9% (95% CI 2.3–10.0%), failed only narrowly.

## Specificity on Reference-Stable Eyes Hid These False Alarms

The usual check, specificity on reference-stable eyes, did not reveal these false alarms. With three tests, D6 was 96.2% specific and D8 94.6%, compared with 96.2% for D1 (false positives: +0.0 and +1.5 percentage points vs D1; Holm-adjusted p = 1.00 and = 1.00). Yet on true no-change series, D6 and D8 raised 5.0 and 6.3 times as many false alarms as D1. All reference-stable eyes had a non-negative long-term slope (share with a positive slope: 100%), which makes them easier to classify than typical stable eyes.

## Sensitivity Compared With the Trend Test (RQ2)

With three tests, D1 flagged 19.2% (95% CI 7.4–33.3%) of reference progressors. D6 flagged 56.9% (+37.7 percentage points vs D1; 95% CI 18.5 to 57.7; Holm-adjusted p = 0.012), the only significant gain, from a detector with excess false alarms. Among detectors without excess false alarms, the rate rule D2 had the largest point gain with three tests: it flagged 38.5% (+19.2 percentage points vs D1; 95% CI −3.4 to 41.7; Holm-adjusted p = 0.72). With four to six tests, D1 flagged 30.8%, 42.3% and 57.7%. Event analysis (D7) flagged 50.0% with five tests (+7.7 percentage points vs D1; 95% CI −10.3 to 26.1; Holm-adjusted p = 1.00). With six tests, D8 no longer had excess false alarms and flagged 70.8% (+13.1 percentage points vs D1; 95% CI −5.2 to 31.1; Holm-adjusted p = 1.00). Rate and pointwise rules gained little after four tests; with six tests, D3 flagged 23.1% (−34.6 percentage points vs D1; 95% CI −53.8 to −16.0; Holm-adjusted p = 0.035). Thus the hypothesis was not falsified, but the study cannot exclude gains of 10–30 percentage points for D2 with three tests or D8 with six tests.

The secondary, PoPLR-based reference gave lower sensitivities and a similar ordering of detectors (Spearman ρ between 0.70 and 1.00 within each number of tests; Supplementary Table S2). The exploratory future-only reference had too few eyes for firm conclusions (Supplementary Table S5).

## Machine-Learning Detectors Under the Usual Threshold Rule (RQ4)

Both supervised models were thresholded at 95% specificity on validation-set reference-stable eyes. On true no-change data, D8 exceeded the nominal 5% with three, four and five tests (27.7%, 9.4% and 18.8%) but not with six (3.6%). D9 exceeded it with three tests (12.7%) and five tests (7.5%). The hypothesis that this threshold rule gives too many false alarms was supported for short series, but not at every number of tests.

## The Shuffle Audit (RQ3)

Across the 40 detector–test-number cells, the shuffle audit and the true no-change false-alarm rate were correlated (Spearman ρ 0.65, 95% CI 0.51–0.72; Fig. 3). Excluding the 3 cells where a detector cannot flag, ρ was 0.56 (0.39–0.65). The median absolute difference was 1.0 percentage points, and 80% of cells differed by 3 percentage points or less. The audit caught D6 and D8 with three tests (shuffle false-alarm rates 22.5% and 17.3%). It over-estimated false alarms for rate rules and event analysis (D2 with three tests: 11.7% vs 2.6%; D7 with six tests: 11.7% vs 1.9%) and under-estimated them for the machine-learning models with three tests (D8: 17.3% vs 27.7%; D9: 8.5% vs 12.7%). The pre-specified target of ρ ≥ 0.7 was not met.

## External Clinic (RQ5)

In GRAPE (Table 2, Fig. 4), validity could not be assessed, because no true no-change data exist there; we report agreement with the two criterion-based labels. Against the mean-deviation label, D1 flagged 44.4% (95% CI 25.9–65.4%) of progressors with three tests, at 95.3% specificity. D2 flagged 59.3% at 78.8% specificity (16.5 percentage points more false positives; Holm-adjusted p < 0.001). D8, transferred unchanged, flagged 65.9% at 61.2% specificity (34.2 percentage points more false positives; Holm-adjusted p < 0.001).

Against the pointwise PLR2 label, which is not based on mean deviation, D1 flagged only 17.5% (95% CI 7.0–30.0%) of progressors. D2 flagged 45.0% (+27.5 percentage points vs D1; 95% CI 10.8 to 42.5; Holm-adjusted p = 0.022) and D8 61.0% (+43.5 percentage points vs D1; 95% CI 29.0 to 56.8; Holm-adjusted p < 0.001), but both again with more false positives (specificity 78.5% and 61.9% vs 92.8%). Thus, in this clinic, the detector that looked best depended on the label, and every gain in sensitivity came with lower specificity.

## No-Change Calibration and Matched Comparison (Amendment B)

Retest calibration brought every detector to about the nominal false-alarm rate: none of the 20 detector–test-number cells had excess false alarms (HB1 supported; Table 5, Fig. 5). Shuffle calibration came within 3 percentage points of 5% in 70% of cells, short of the pre-specified 75% (HB2 not supported); it was very conservative for the rate score (D2 false alarms 0.4% to 1.0%).

At retest-matched false-alarm rates, the conformal and machine-learning detectors (D6, D8, D9) no longer flagged significantly more progressors than D1: differences ranged from −19.2 to +19.2 percentage points, with no significant difference (smallest Holm-adjusted p = 0.38). For example, with three tests, retest-calibrated D8 had 5.2% (95% CI 3.5–7.1%) false alarms and flagged 14.6% of progressors, compared with 19.2% for D1.

HB3 was falsified by the rate score. With retest calibration, D2 flagged 73.1% of progressors with five tests (+30.8 percentage points vs D1; 95% CI 14.8 to 50.0; Holm-adjusted p = 0.031) and 84.6% with six (+30.8 percentage points vs D1; 95% CI 15.4 to 48.0; Holm-adjusted p = 0.031), at false-alarm rates of 5.5% and 5.2%. The gain was also seen against the PoPLR-based secondary reference (46.6% vs 27.6% with five tests). The retest-calibrated slope threshold was small: 0.30 dB per year with five tests, close to the −0.3 dB per year used to define reference progressors. When the same score was calibrated on shuffled clinic records, the threshold was about 3.0 times larger at every number of tests, and D2 flagged fewer progressors than D1 (differences −30.8 to −15.4 percentage points). For all other detectors, the two calibration sources gave thresholds within a factor of 0.90 to 1.27.

The time-label check supported D1's robustness: its false-alarm rate stayed between 3.3% and 5.8% whether the retest series were given clinic dates, annual spacing or the dates of reference-stable eyes. The pointwise rule D3, in contrast, raised false alarms on 18.3% of three-test series with annual spacing. On all 314 UWHVF eyes with a reference label (150 progressors, 164 stable, 236 patients), the fixed rate rule D2 flagged more progressors than D1 with three tests (+8.7 percentage points vs D1; 95% CI 0.7 to 16.4; Holm-adjusted p = 0.047), at lower specificity (85.4% vs 96.3%); with four to six tests, D1 flagged more progressors than D2, D3 and D4 (Supplementary Table S6).

Two post-hoc checks, requested in review, tested whether the gain of the retest-calibrated rate score was an artefact of the slope-based reference, whose −0.3 dB per year cut-off is close to the calibrated threshold. Because D1 and D2 need no training, we applied their retest-calibrated thresholds to all 314 labelled UWHVF eyes and to alternative references (Supplementary Table S7). D2 flagged 11 to 35 percentage points more progressors than D1 under every definition, including a −1.0 dB per year cut-off and a future-only reference built from the tests after those seen by the detectors. The gain therefore did not depend on the reference definition. It came at a cost in clinic eyes: specificity in reference-stable eyes was 80–90% for D2 against 95–99% for D1, and among the 376 indeterminate eyes D2 flagged 20–39% against 10–22% for D1. This is the pattern expected if weekly retests under-represent the year-to-year noise of clinic tests. Finally, HB3 was falsified with the pre-specified Holm correction within each number of tests; with a correction across all 16 retest-calibrated comparisons, the smallest adjusted p was = 0.12.

## Real-World Measures

Table 3 translates the results into clinical units. With D1, 38% of reference progressors were flagged by the fourth test, 54% by the fifth and 69% by the sixth; the median was 5 tests, or about 4 years after the first test at the observed testing interval. At a single review with three tests, D1 would raise about 44 false flags per 1,000 no-change eyes, D6 about 224 and D8 about 277. Repeated reviews add up: over four reviews, D1 flagged 12.6% (95% CI 8.0–17.9%) of no-change series at least once, D6 29.8% (95% CI 24.6–35.4%) and D8 43.7% (95% CI 36.2–51.1%).

# Discussion

This benchmark asked how early visual-field progression can be detected without excess false alarms. In short series, the tested conformal and machine-learning detectors flagged more progressors than the trend of mean sensitivity, but they also raised far more false alarms on eyes that truly did not change. Specificity on reference-stable eyes missed these false alarms. Among detectors without excess false alarms, none flagged significantly more progressors than the trend test, but our small reference groups leave room for moderate gains.

The main lesson concerns evaluation. A pooled-detrended conformal test looked like a clear gain with three tests: it raised sensitivity 3.0-fold, with the same specificity as the trend test on reference-stable eyes. The true no-change arm, and the shuffle audit, showed that it flagged about 22.4% of no-change series. With three tests, detrending leaves one residual degree of freedom, and the pooled reference does not reflect each eye's own noise. Reference-stable eyes, defined by a long-term slope that is not negative, are an easy test of specificity. Any method whose threshold is set or checked on such eyes may look better than it is.

The calibration extension sharpens this lesson. When every detector was held to the same false-alarm rate on retest data, the conformal and machine-learning detectors no longer showed a significant advantage. Most of their earlier "gain" reflected a different operating point rather than better discrimination, although moderate differences cannot be excluded; for D8 with six tests the difference was +19.2 percentage points; 95% CI 0.8 to 37.1; Holm-adjusted p = 0.54. The rate-of-change score behaved differently: it looked clearly better than the trend test after retest calibration, but clearly worse after calibration on the clinic's own shuffled records. The reason is noise. Weekly retests contain only short-term variability, whereas shuffled clinic series spread years of variability, and any true progression, across the series. A raw slope threshold depends directly on this noise level, so the retest threshold is probably too liberal for yearly clinic tests and the shuffle threshold too strict. Our post-hoc checks support this explanation: with the retest threshold, the rate rule was more sensitive under every reference definition, but it flagged clearly more clinic eyes that were stable or indeterminate. Its advantage is therefore a trade-off between sensitivity and specificity, whose terms depend on noise that weekly retests do not capture. The trend test divides the slope by the eye's own scatter. Its false-alarm rate stayed between 3.3% and 5.8% under every no-change source we tried, including different time labels. The regional trend statistic (D6) and the machine-learning scores also had similar thresholds under the two calibration sources, but they were not part of the time-label check. The trend test is therefore a safe default when the noise of a clinic's own tests is unknown. A rate rule calibrated on long-interval no-change data, which do not yet exist publicly, could offer a better trade-off and deserves study.

These findings agree with earlier work. Artes and colleagues found that the "possible progression" alert of the Guided Progression Analysis was much less specific than its "likely progression" alert, and that false alerts varied greatly between patients [11]. Wu and Medeiros compared event-based and trend-based analyses for detecting progression [12]. Machine-learning studies of progression have mostly been evaluated against labels derived from other progression criteria [17–22], and a multicentre study found that results depend strongly on the label [26]. Our external-clinic results agree: the trend test looked best against a mean-deviation label and weak against a pointwise label. Our results add a direct test of false alarms for several classes of detectors, at a fixed small number of tests, together with an estimate of how false alarms accumulate over repeated reviews.

Repeated review matters in practice. A test with a 5% false-alarm rate at each review flags more than 5% of stable eyes over several reviews. In our data, the trend test flagged 12.6% of no-change series at least once over four reviews. A practical safeguard, used in many clinics, is to confirm a flag on the next test before escalating treatment; we did not evaluate this rule. Studies of testing frequency show that clinics often need many years to confirm progression [6, 34, 35], and our real-world measures agree. Front-loading or clustering tests [5, 36] may help, but we did not test this.

What does this mean for a clinic? First, the trend of mean sensitivity with a p-value kept its nominal false-alarm rate at each review, and no detector without excess false alarms clearly beat it in our data. Second, simple rate rules without a p-value had few false alarms on our no-change data, but in the external clinic they raised false positives against both labels. Third, before adopting a new detector, a clinic can run a shuffle audit on its own records. It caught the largest problems here, but it over- or under-estimated false alarms for some detectors, so it is a screen, not a replacement for true no-change data. For commercial software that cannot be re-run, clinics can ask vendors for false-alarm rates on short-interval retest data and over repeated reviews.

For method developers, we suggest five reporting items: false alarms on true no-change series, not only specificity on stable eyes; comparisons at matched false-alarm rates, with the source of the no-change data stated; cumulative false alarms over repeated reviews; sensitivity at a fixed, small number of tests; and results against more than one progression label. Our code and per-eye outputs are open, so new detectors can be added and compared on the same terms.

This study has limitations. First, the reference groups were small (26 progressors and 26 stable eyes), so CIs were wide, and the comparisons with D1 had low power. Second, the reference uses the whole series, including the first k tests, and is based on mean total deviation; this favours D1. The secondary PoPLR reference reduced, but did not remove, this bias, and the future-only reference had too few eyes. Third, reference-stable eyes had non-negative slopes and 80 indeterminate eyes were excluded, so specificity on UWHVF is optimistic. Fourth, the true no-change arm had only 30 patients tested a week apart. We gave each series the test dates of a clinic eye (amendment A1). This keeps it a valid null, but it does not reproduce long-term changes in noise, such as cataract, learning or fatigue, and it may favour rate rules. Fifth, the "complex" detectors are our own implementations: D6 came from our development work, D7 is a simplified analogue of commercial event analysis, and D8 and D9 are simple machine-learning baselines trained on few labelled eyes. Our conclusions apply to these detectors and should not be generalised to all conformal or machine-learning methods. Sixth, GRAPE used a different perimeter, its labels are criterion-based, and several detectors were re-calibrated or omitted there. Seventh, UWHVF has no reliability indices or diagnoses. Eighth, the calibration extension was planned after the first results and reviews; it was time-stamped before it was run, but it is not independent of them. Retest calibration makes HB1 nearly true by construction, shuffle calibration scored the machine-learning models on their own training eyes, and the falsification of HB3 depends on the pre-specified within-test-number Holm correction. Finally, the analysis plan was committed to our repository rather than a public registry, and it followed a development phase that used the retest data once (Table 4).

# Conclusions

In this benchmark, apparent early-detection gains of the tested conformal and machine-learning detectors were explained by their false alarms; at matched false-alarm rates they did not flag significantly more progressors than the trend of mean sensitivity. A retest-calibrated rate-of-change rule was more sensitive but less specific in clinic eyes, and its ranking reversed when it was calibrated on clinic records. The trend test kept a false-alarm rate near 5% under every no-change source we tried. Detectors should be calibrated and compared on no-change data that match clinical test intervals before they guide treatment escalation.

# Declarations

## Acknowledgements

We thank the creators of the UWHVF, GRAPE and Artes retest data sets, and the maintainers of the visualFields R package, for making their data openly available.

## Funding

No funding or sponsorship was received for this study or publication of this article.

## Medical Writing, Editorial and Other Assistance

During this work the authors used an AI-based assistant (Claude, Anthropic) to help write analysis code and draft and edit the manuscript text. The first author directed and checked this work; all numbers were generated by the analysis code from the public data. The authors reviewed all code, results and text and take full responsibility for the content of the article.

## Author Contributions

P N Bhargav Teja: conceptualisation, methodology, software, data curation, formal analysis, visualisation, writing – original draft. Rajay Vedaraj I S: supervision, validation, writing – review and editing. Both authors read and approved the final manuscript.

## Disclosures

P N Bhargav Teja and Rajay Vedaraj I S declare that they have no competing interests.

## Compliance With Ethics Guidelines

This study used only publicly available, de-identified data sets released by their custodians under open licences. The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

## Data Availability

All data sets are public: UWHVF (https://github.com/uw-biomedical-ml/uwhvf), GRAPE (Figshare file 41670009, "VF and clinical information.xlsx", described in [29]) and the Artes retest data (visualFields R package 1.0.7, CRAN). The analysis code, analysis plan, per-eye detector outputs and all result files are provided as supplementary material and will be deposited in a public repository on acceptance.

# References

1. Tham YC, Li X, Wong TY, Quigley HA, Aung T, Cheng CY. Global Prevalence of Glaucoma and Projections of Glaucoma Burden through 2040. Ophthalmology. 2014;121(11):2081-2090. https://doi.org/10.1016/j.ophtha.2014.05.013

2. Weinreb RN, Aung T, Medeiros FA. The Pathophysiology and Treatment of Glaucoma: A Review. JAMA. 2014;311(18):1901. https://doi.org/10.1001/jama.2014.3192

3. Heijl A, Leske MC, Bengtsson B, Hyman L, Bengtsson B, Hussein M; Early Manifest Glaucoma Trial Group. Reduction of Intraocular Pressure and Glaucoma Progression: Results From the Early Manifest Glaucoma Trial. Arch Ophthalmol. 2002;120(10):1268-1279. https://doi.org/10.1001/archopht.120.10.1268

4. Gardiner SK, Swanson WH, Goren D, Mansberger SL, Demirel S. Assessment of the Reliability of Standard Automated Perimetry in Regions of Glaucomatous Damage. Ophthalmology. 2014;121(7):1359-1369. https://doi.org/10.1016/j.ophtha.2014.01.020

5. Chauhan BC, Garway-Heath DF, Goni FJ, Rossetti L, Bengtsson B, Viswanathan AC, et al. Practical recommendations for measuring rates of visual field change in glaucoma. British Journal of Ophthalmology. 2008;92(4):569-573. https://doi.org/10.1136/bjo.2007.135012

6. Stagg BC, Brintz BJ, Stein JD, Hess R, Kawamoto K, Jammal AA, et al. Time to Identify Glaucoma Progression Given Typical Visual Field Testing Frequencies in a US Nationwide Insured Population. Ophthalmology Glaucoma. 2026;9(3):250-256. https://doi.org/10.1016/j.ogla.2025.11.004

7. Foot B, MacEwen C. Surveillance of sight loss due to delay in ophthalmic treatment or review: frequency, cause and outcome. Eye. 2017;31(5):771-775. https://doi.org/10.1038/eye.2017.1

8. O'Leary N, Chauhan BC, Artes PH. Visual Field Progression in Glaucoma: Estimating the Overall Significance of Deterioration with Permutation Analyses of Pointwise Linear Regression (PoPLR). Invest. Ophthalmol. Vis. Sci. 2012;53(11):6776. https://doi.org/10.1167/iovs.12-10049

9. Bengtsson B, Heijl A. A Visual Field Index for Calculation of Glaucoma Rate of Progression. American Journal of Ophthalmology. 2008;145(2):343-353. https://doi.org/10.1016/j.ajo.2007.09.038

10. Mohammadzadeh V, Li L, Fei Z, Davis T, Morales E, Wu K, et al. Efficacy of Smoothing Algorithms to Enhance Detection of Visual Field Progression in Glaucoma. Ophthalmology Science. 2024;4(2):100423. https://doi.org/10.1016/j.xops.2023.100423

11. Artes PH, O'Leary N, Nicolela MT, Chauhan BC, Crabb DP. Visual Field Progression in Glaucoma: What Is the Specificity of the Guided Progression Analysis? Ophthalmology. 2014;121(10):2023-2027. https://doi.org/10.1016/j.ophtha.2014.04.015

12. Wu Z, Medeiros FA. Comparison of Visual Field Point-Wise Event-Based and Global Trend-Based Analysis for Detecting Glaucomatous Progression. Trans. Vis. Sci. Tech. 2018;7(4):20. https://doi.org/10.1167/tvst.7.4.20

13. Heijl A, Bengtsson B, Chauhan BC, Lieberman MF, Cunliffe I, Hyman L, et al. A Comparison of Visual Field Progression Criteria of 3 Major Glaucoma Trials in Early Manifest Glaucoma Trial Patients. Ophthalmology. 2008;115(9):1557-1565. https://doi.org/10.1016/j.ophtha.2008.02.005

14. Zhu H, Crabb DP, Ho T, Garway-Heath DF. More Accurate Modeling of Visual Field Progression in Glaucoma: ANSWERS. Invest. Ophthalmol. Vis. Sci. 2015;56(10):6077. https://doi.org/10.1167/iovs.15-16957

15. Marín-Franch I, Artes PH, Turpin A, Racette L. Visual Field Progression in Glaucoma: Comparison Between PoPLR and ANSWERS. Trans. Vis. Sci. Tech. 2021;10(14):13. https://doi.org/10.1167/tvst.10.14.13

16. Montesano G, Garway-Heath DF, Ometto G, Crabb DP. Hierarchical Censored Bayesian Analysis of Visual Field Progression. Trans. Vis. Sci. Tech. 2021;10(12):4. https://doi.org/10.1167/tvst.10.12.4

17. Saeedi O, Boland MV, D'Acunto L, Swamy R, Hegde V, Gupta S, et al. Development and Comparison of Machine Learning Algorithms to Determine Visual Field Progression. Trans. Vis. Sci. Tech. 2021;10(7):27. https://doi.org/10.1167/tvst.10.7.27

18. Dixit A, Yohannan J, Boland MV. Assessing Glaucoma Progression Using Machine Learning Trained on Longitudinal Visual Field and Clinical Data. Ophthalmology. 2021;128(7):1016-1026. https://doi.org/10.1016/j.ophtha.2020.12.020

19. Wang M, Shen LQ, Pasquale LR, Petrakos P, Formica S, Boland MV, et al. An Artificial Intelligence Approach to Detect Visual Field Progression in Glaucoma Based on Spatial Pattern Analysis. Invest. Ophthalmol. Vis. Sci. 2019;60(1):365. https://doi.org/10.1167/iovs.18-25568

20. Wen JC, Lee CS, Keane PA, Xiao S, Rokem AS, Chen PP, et al. Forecasting future Humphrey Visual Fields using deep learning. PLoS ONE. 2019;14(4):e0214875. https://doi.org/10.1371/journal.pone.0214875

21. Berchuck SI, Mukherjee S, Medeiros FA. Estimating Rates of Progression and Predicting Future Visual Fields in Glaucoma Using a Deep Variational Autoencoder. Sci Rep. 2019;9(1). https://doi.org/10.1038/s41598-019-54653-6

22. Yousefi S, Balasubramanian M, Goldbaum MH, Medeiros FA, Zangwill LM, Weinreb RN, et al. Unsupervised Gaussian Mixture-Model With Expectation Maximization for Detecting Glaucomatous Progression in Standard Automated Perimetry Visual Fields. Trans. Vis. Sci. Tech. 2016;5(3):2. https://doi.org/10.1167/tvst.5.3.2

23. Chen L, Fujita A, Moradi M, Eslami M, Elze T, Zebardast N. Earlier confirmation of glaucoma progression with risk-weighted visual field and OCT scheduling. medRxiv. 2026. https://doi.org/10.64898/2026.11.16.26368187

24. Si W, Lin V, Sun B, Jang KJ, Xing R, Saeed A, et al. Reliable and Interpretable Visual Field Progression Prediction with Diffusion Models and Conformal Risk Control. Lecture Notes in Computer Science. 2025:543-552. https://doi.org/10.1007/978-3-032-05182-0_53

25. Schell GJ, Lavieri MS, Helm JE, Liu X, Musch DC, Van Oyen MP, et al. Using Filtered Forecasting Techniques to Determine Personalized Monitoring Schedules for Patients with Open-Angle Glaucoma. Ophthalmology. 2014;121(8):1539-1546. https://doi.org/10.1016/j.ophtha.2014.02.021

26. Kim H, Kim E, Moon S, Jin SW, Kim JL, Lee SU, et al. Labeling matters: A multicenter machine learning study on visual field progression in Glaucoma. PLoS One. 2026;21(8):e0357179. https://doi.org/10.1371/journal.pone.0357179

27. Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378

28. Montesano G, Chen A, Lu R, Lee CS, Lee AY. UWHVF: A Real-World, Open Source Dataset of Perimetry Tests From the Humphrey Field Analyzer at the University of Washington. Trans. Vis. Sci. Tech. 2022;11(1):2. https://doi.org/10.1167/tvst.11.1.1

29. Huang X, Kong X, Shen Z, Ouyang J, Li Y, Jin K, et al. GRAPE: A multi-modal dataset of longitudinal follow-up visual field and fundus images for glaucoma management. Sci Data. 2023;10(1). https://doi.org/10.1038/s41597-023-02424-4

30. Angelopoulos AN, Bates S. Conformal Prediction: A Gentle Introduction. Foundations and Trends® in Machine Learning. 2023;16(4):494-591. https://doi.org/10.1561/2200000101

31. Phipson B, Smyth GK. Permutation P-values Should Never Be Zero: Calculating Exact P-values When Permutations Are Randomly Drawn. Statistical Applications in Genetics and Molecular Biology. 2010;9(1). https://doi.org/10.2202/1544-6115.1585

32. Freedman D, Lane D. A Nonstochastic Interpretation of Reported Significance Levels. Journal of Business & Economic Statistics. 1983;1(4):292-298. https://doi.org/10.1080/07350015.1983.10509354

33. Gagnon-Bartsch J, Shem-Tov Y. The classification permutation test: A flexible approach to testing for covariate imbalance in observational studies. Ann. Appl. Stat. 2019;13(3):1464-1483. https://doi.org/10.1214/19-aoas1241

34. Wu Z, Saunders LJ, Daga FB, Diniz-Filho A, Medeiros FA. Frequency of Testing to Detect Visual Field Progression Derived Using a Longitudinal Cohort of Glaucoma Patients. Ophthalmology. 2017;124(6):786-792. https://doi.org/10.1016/j.ophtha.2017.01.027

35. Crabb DP, Garway-Heath DF. Intervals between Visual Field Tests When Monitoring the Glaucomatous Patient: Wait-and-See Approach. Invest. Ophthalmol. Vis. Sci. 2012;53(6):2770. https://doi.org/10.1167/iovs.12-9476

36. Phu J, Kalloniatis M. The Frontloading Fields Study (FFS): Detecting Changes in Mean Deviation in Glaucoma Using Multiple Visual Field Tests Per Clinical Visit. Trans. Vis. Sci. Tech. 2021;10(13):21. https://doi.org/10.1167/tvst.10.13.21

# Tables

**Table 1** Detection of future-confirmed progression (UWHVF test set) and false alarms on true no-change series

| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | False alarms, true no-change, % (95% CI) | False alarms, shuffle audit, % | Excess false alarms | Valid (rule A3) |
|---|---|---|---|---|---|---|---|
| 3 | D1 OLS-MD | 19.2 (7.4–33.3) | 96.2 (87.0–100.0) | 4.4 (2.8–6.3) | 4.8 | No | Yes |
| 3 | D2 MD rate | 38.5 (20.0–56.5) | 92.3 (80.0–100.0) | 2.6 (1.5–3.9) | 11.7 | No | Yes |
| 3 | D3 PLR-3 | 3.8 (0.0–12.5) | 96.2 (88.0–100.0) | 1.4 (1.0–1.8) | 1.8 | No | Yes |
| 3 | D4 PoPLR | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | n/a | n/a |
| 3 | D5 Pooled-shuffle conformal | 19.2 (7.4–33.3) | 96.2 (87.0–100.0) | 4.0 (2.7–5.6) | 4.6 | No | Yes |
| 3 | D6 Pooled-detrended conformal | 56.9 (37.0–76.2) | 96.2 (87.0–100.0) | 22.4 (19.3–25.7) | 22.5 | **Yes** | **No** |
| 3 | D7 Event analysis | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | n/a | n/a |
| 3 | D8 ML tabular (LightGBM) | 26.2 (12.3–43.2) | 94.6 (84.8–100.0) | 27.7 (22.7–32.9) | 17.3 | **Yes** | **No** |
| 3 | D9 ML sequence (GRU) | 12.3 (2.4–24.8) | 95.4 (88.8–100.0) | 12.7 (6.2–20.0) | 8.5 | **Yes** | **No** |
| 3 | D10 Self-supervised order net | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | n/a | n/a |
| 4 | D1 OLS-MD | 30.8 (14.3–48.1) | 100.0 (100.0–100.0) | 3.8 (1.9–6.2) | 4.7 | No | Yes |
| 4 | D2 MD rate | 23.1 (8.0–40.0) | 96.2 (87.5–100.0) | 0.6 (0.4–0.9) | 6.4 | No | Yes |
| 4 | D3 PLR-3 | 15.4 (3.6–30.8) | 100.0 (100.0–100.0) | 0.2 (0.0–0.3) | 1.5 | No | Yes |
| 4 | D4 PoPLR | 3.8 (0.0–12.5) | 100.0 (100.0–100.0) | 3.3 (1.8–4.9) | 4.1 | No | Yes |
| 4 | D5 Pooled-shuffle conformal | 30.8 (14.3–48.1) | 100.0 (100.0–100.0) | 3.6 (1.8–5.9) | 4.9 | No | Yes |
| 4 | D6 Pooled-detrended conformal | 25.4 (10.3–44.0) | 100.0 (100.0–100.0) | 5.1 (3.4–7.2) | 5.5 | No | Yes |
| 4 | D7 Event analysis | 23.1 (7.7–40.0) | 100.0 (100.0–100.0) | 1.1 (0.0–2.6) | 5.2 | No | Yes |
| 4 | D8 ML tabular (LightGBM) | 41.5 (23.7–59.2) | 99.2 (97.4–100.0) | 9.4 (6.3–12.9) | 7.7 | **Yes** | **No** |
| 4 | D9 ML sequence (GRU) | 11.5 (2.8–23.2) | 99.2 (97.6–100.0) | 2.0 (0.6–3.7) | 4.7 | No | Yes |
| 4 | D10 Self-supervised order net | 20.0 (7.7–35.8) | 100.0 (100.0–100.0) | 3.8 (2.5–5.1) | 4.1 | No | Yes |
| 5 | D1 OLS-MD | 42.3 (23.1–61.5) | 100.0 (100.0–100.0) | 4.7 (2.2–7.5) | 5.1 | No | Yes |
| 5 | D2 MD rate | 23.1 (7.7–41.4) | 100.0 (100.0–100.0) | 0.8 (0.5–1.2) | 3.6 | No | Yes |
| 5 | D3 PLR-3 | 23.1 (8.0–40.0) | 100.0 (100.0–100.0) | 0.5 (0.1–1.1) | 1.4 | No | Yes |
| 5 | D4 PoPLR | 38.5 (20.0–57.7) | 100.0 (100.0–100.0) | 3.9 (1.9–6.2) | 4.3 | No | Yes |
| 5 | D5 Pooled-shuffle conformal | 42.3 (23.1–61.5) | 100.0 (100.0–100.0) | 4.3 (2.0–7.1) | 4.9 | No | Yes |
| 5 | D6 Pooled-detrended conformal | 31.5 (16.0–48.5) | 100.0 (100.0–100.0) | 6.2 (3.7–8.9) | 5.0 | No | Yes |
| 5 | D7 Event analysis | 50.0 (30.4–69.6) | 100.0 (100.0–100.0) | 1.2 (0.0–2.9) | 7.9 | No | Yes |
| 5 | D8 ML tabular (LightGBM) | 56.2 (36.1–74.8) | 99.2 (97.6–100.0) | 18.8 (13.1–24.9) | 16.1 | **Yes** | **No** |
| 5 | D9 ML sequence (GRU) | 40.8 (22.8–59.2) | 93.8 (82.4–100.0) | 7.5 (2.8–13.3) | 8.1 | No | **No** |
| 5 | D10 Self-supervised order net | 43.8 (28.0–60.0) | 100.0 (100.0–100.0) | 5.1 (2.9–7.6) | 4.2 | No | Yes |
| 6 | D1 OLS-MD | 57.7 (38.4–76.9) | 100.0 (100.0–100.0) | 5.1 (2.5–8.1) | 5.9 | No | Yes |
| 6 | D2 MD rate | 23.1 (8.3–38.5) | 100.0 (100.0–100.0) | 1.0 (0.6–1.5) | 2.8 | No | Yes |
| 6 | D3 PLR-3 | 23.1 (7.7–41.7) | 100.0 (100.0–100.0) | 0.3 (0.0–0.8) | 1.2 | No | Yes |
| 6 | D4 PoPLR | 50.0 (30.8–67.9) | 100.0 (100.0–100.0) | 5.0 (2.4–8.4) | 4.8 | No | Yes |
| 6 | D5 Pooled-shuffle conformal | 56.9 (37.7–76.0) | 100.0 (100.0–100.0) | 5.0 (2.4–7.9) | 5.0 | No | Yes |
| 6 | D6 Pooled-detrended conformal | 53.8 (37.0–71.4) | 100.0 (100.0–100.0) | 7.6 (4.5–11.1) | 4.9 | No | **No** |
| 6 | D7 Event analysis | 57.7 (36.0–77.8) | 100.0 (100.0–100.0) | 1.9 (0.5–3.8) | 11.7 | No | Yes |
| 6 | D8 ML tabular (LightGBM) | 70.8 (51.7–88.8) | 100.0 (100.0–100.0) | 3.6 (1.7–6.0) | 8.7 | No | Yes |
| 6 | D9 ML sequence (GRU) | 37.7 (22.3–53.8) | 91.5 (75.2–100.0) | 5.9 (2.3–10.0) | 8.6 | No | **No** |
| 6 | D10 Self-supervised order net | 54.6 (36.9–70.8) | 99.2 (97.6–100.0) | 5.7 (3.0–9.2) | 4.7 | No | Yes |

Sensitivity: 26 reference progressors; specificity: 26 reference-stable eyes (first k tests only). True no-change: all windows of k consecutive tests in 30 Artes retest patients, 10 time-label draws per window. Shuffle audit: UWHVF test-set eyes with their first k tests randomly re-ordered, 10 times. Excess false alarms: the whole 95% CI of the true no-change false-alarm rate lies above 5%. Valid (rule A3, a deviation from the protocol, see Methods): upper CI limit at most 10% and lower limit at most 5%. Under the protocol's literal rule (upper limit at most 5%) no detector that can flag at the nominal level, including D1, would be valid with 30 retest patients. Stochastic detectors (D5, D6, D8–D10): each eye's flag averaged over 5 seeds. CI: patient-level bootstrap (2,000 resamples). n/a: D4, D7 and D10 cannot flag with 3 tests by design.

**Table 2** External clinic (GRAPE): sensitivity and specificity against two criterion-based progression labels

| Tests | Detector | MD label: sensitivity, % (95% CI) | MD label: specificity, % (95% CI) | PLR2 label: sensitivity, % (95% CI) | PLR2 label: specificity, % (95% CI) |
|---|---|---|---|---|---|
| 3 | D1 OLS-MD | 44.4 (25.9–65.4) | 95.3 (92.2–97.9) | 17.5 (7.0–30.0) | 92.8 (88.5–96.4) |
| 3 | D2 MD rate | 59.3 (40.7–76.9) | 78.8 (73.5–83.9) | 45.0 (30.8–58.5) | 78.5 (72.4–84.1) |
| 3 | D3 PLR-3 | 3.7 (0.0–11.5) | 95.8 (92.7–98.3) | 17.5 (5.1–31.0) | 98.2 (96.3–99.6) |
| 3 | D4 PoPLR | n/a | n/a | n/a | n/a |
| 3 | D5 Pooled-shuffle conformal | 41.5 (23.8–60.0) | 95.4 (92.4–98.0) | 17.5 (7.0–30.0) | 93.3 (89.4–96.5) |
| 3 | D7 Event analysis | n/a | n/a | n/a | n/a |
| 3 | D8 ML tabular (LightGBM) | 65.9 (50.8–80.0) | 61.2 (54.6–67.1) | 61.0 (45.9–75.1) | 61.9 (55.2–68.3) |
| 4 | D1 OLS-MD | 33.3 (11.8–55.0) | 95.9 (92.2–98.6) | 16.1 (3.2–31.2) | 94.7 (90.8–97.9) |
| 4 | D2 MD rate | 55.6 (35.3–76.5) | 86.2 (79.4–92.1) | 38.7 (22.2–58.1) | 86.4 (80.3–91.9) |
| 4 | D3 PLR-3 | 11.1 (0.0–25.0) | 97.9 (95.2–100.0) | 16.1 (3.7–28.1) | 100.0 (100.0–100.0) |
| 4 | D4 PoPLR | 22.2 (5.9–41.2) | 95.2 (91.4–98.0) | 22.6 (9.7–36.7) | 97.0 (93.9–99.3) |
| 4 | D5 Pooled-shuffle conformal | 33.3 (11.8–55.0) | 94.5 (90.8–97.7) | 20.6 (6.7–36.3) | 94.2 (90.4–97.7) |
| 4 | D7 Event analysis | 16.7 (0.0–33.3) | 95.9 (92.4–98.7) | 16.1 (3.4–28.6) | 97.0 (93.8–99.3) |
| 4 | D8 ML tabular (LightGBM) | 48.9 (31.8–65.9) | 81.5 (74.2–87.9) | 43.9 (29.3–59.3) | 83.3 (77.0–89.0) |

Labels are those distributed with GRAPE, assigned by rule-based criteria: MD (mean-deviation criterion; primary) and PLR2 (pointwise linear regression criterion). Progressors at 3 tests: 27.0 (MD) and 40.0 (PLR2) of 263.0 eyes; at 4 tests: 18.0 and 31.0 of 163.0. PLR3 and any-criterion results: Supplementary Table S4. D5 and D7 calibrated on GRAPE by 5-fold patient-level cross-fitting; D8 transferred unchanged from UWHVF; D6, D9, D10 not applicable (24-2 specific). n/a: cannot flag with 3 tests by design. CI: patient-level bootstrap.

**Table 3** Real-world measures: tests to first flag in future-confirmed progressors and false flags in no-change eyes

| Detector | Progressors flagged by test 4 / 5 / 6, % | Median tests to first flag | False flags per 1,000 no-change eyes at a single review with 3 / 4 / 5 / 6 tests | No-change series flagged at least once over four reviews (tests 3–6), % (95% CI) |
|---|---|---|---|---|
| D1 OLS-MD | 38 / 54 / 69 | 5 | 44 / 38 / 47 / 51 | 12.6% (95% CI 8.0–17.9%) |
| D2 MD rate | 38 / 46 / 46 | > 6 | 26 / 6 / 8 / 10 | 4.4% (95% CI 3.2–5.9%) |
| D3 PLR-3 | 19 / 31 / 38 | > 6 | 14 / 2 / 5 / 3 | 2.6% (95% CI 1.7–3.7%) |
| D4 PoPLR | 4 / 38 / 54 | 6 | 0 / 33 / 39 / 50 | 9.2% (95% CI 5.5–13.4%) |
| D5 Pooled-shuffle conformal | 38 / 54 / 68 | 5 | 40 / 36 / 44 / 50 | 12.2% (95% CI 7.6–17.2%) |
| D6 Pooled-detrended conformal | 58 / 65 / 77 | 3 | 224 / 51 / 62 / 76 | 29.8% (95% CI 24.6–35.4%) |
| D7 Event analysis | 23 / 50 / 58 | 5.5 | 0 / 11 / 12 / 19 | 1.9% (95% CI 0.5–3.8%) |
| D8 ML tabular (LightGBM) | 52 / 63 / 78 | 4 | 277 / 94 / 188 / 36 | 43.7% (95% CI 36.2–51.1%) |
| D9 ML sequence (GRU) | 16 / 46 / 59 | 6 | 127 / 20 / 76 / 59 | 20.9% (95% CI 10.8–31.7%) |
| D10 Self-supervised order net | 20 / 51 / 63 | 5 | 0 / 38 / 51 / 57 | 11.4% (95% CI 7.5–16.1%) |

Progressors: 26 UWHVF test-set reference progressors; an eye counts as flagged by test k if any review with 3..k tests flagged it. Median tests: '> 6' means fewer than half were flagged by 6 tests. In UWHVF the median interval between tests was 1.0 years. False flags per 1,000 = 1,000 × single-review true no-change false-alarm rate. Last column (exploratory, not pre-registered): Artes retest series reviewed four times, after 3, 4, 5 and 6 tests, the cumulative counterpart of the second column.

**Table 4** Deviations from the analysis plan and other disclosures

| Item | Plan (protocol.md) | What was done | Reason / effect |
|---|---|---|---|
| A1 time labels | Not specified | Each Artes window given the test dates of a random UWHVF test eye (10 draws) | Rate rules depend on time scale; amendment committed before the final run |
| A2 GRAPE | All detectors | D5, D7 re-calibrated on GRAPE by cross-fitting; D6, D9, D10 not applied | Different perimeter and grid; amendment committed before the final run |
| Validity rule | "FPR CI upper bound vs 5%" | Three rules reported; main text uses "excess false alarms" (CI lower limit > 5%) | Literal reading cannot be met by a correctly sized test with 30 patients; operational rule (upper ≤ 10%, lower ≤ 5%) written during the final run |
| Estimand | Not specified | Seed-averaged flags for proportions and differences; majority flag for McNemar | First analysis used majority flags for differences; corrected after review |
| Paired CI | Patient bootstrap | Patient bootstrap | First analysis resampled eyes; corrected after review |
| Not-applicable detectors | Not specified | D4, D7, D10 at 3 tests excluded from counts and Holm families | Cannot flag by design |
| Amendment B | — | No-change calibration (RC, SC) of D1, D2, D6, D8, D9; matched comparison; all eligible eyes for D1–D4; time-label check | Written and time-stamped after round-1 results and review, before running; hypotheses HB1–HB3 pre-stated |
| Post-hoc robustness | — | Retest-calibrated D1 and D2 applied to all eyes, alternative reference cut-offs, future-only reference, indeterminate eyes | Requested in review round 2; exploratory |
| Added analyses | — | Cumulative false alarms over four reviews; future-only reference; GRAPE PLR2/PLR3/any labels in tables | Requested in review; exploratory except GRAPE secondary labels (planned) |
| Development use of data | Artes used once in development | D6 false-alarm excess on Artes known before the plan | D6 result is not confirmatory |
| Quick software check | Quick mode on validation subset | Quick mode also processed Artes and GRAPE files before A1/A2 | Outputs not used for any choice |
| D8 features | Features incl. PoPLR statistic and worst-region slope | 14 features: number of tests, span, level and change of mean sensitivity, its slope and z, share of declining points, mean pointwise −log p, worst-decile pointwise slope, spread measures | PoPLR-type summary (mean −log p) and worst-decile slope used instead; fixed before the final run |

**Table 5** No-change calibration (amendment B): thresholds set on retest data (RC) or on shuffled clinic records (SC)

| Tests | Detector | RC: false alarms, % (95% CI) | RC: sensitivity, % | RC: difference vs D1, pp (95% CI) | SC: false alarms, % (95% CI) | SC: sensitivity, % | Threshold ratio SC/RC |
|---|---|---|---|---|---|---|---|
| 3 | D1 OLS-MD | 5.4 (3.5–7.8) | 19.2 | — | 4.3 (2.7–6.1) | 19.2 | 1.17 |
| 3 | D2 MD rate | 5.1 (3.3–7.2) | 46.2 | +26.9 (8.0 to 47.8) | 0.4 (0.2–0.6) | 3.8 | 2.97 |
| 3 | D6 Pooled-detrended conformal | 5.0 (3.6–6.7) | 15.4 | −3.8 (−20.8 to 12.0) | 5.0 (3.6–6.5) | 15.4 | 1.00 |
| 3 | D8 ML tabular (LightGBM) | 5.2 (3.5–7.1) | 14.6 | −4.6 (−17.9 to 9.6) | 6.5 (4.5–8.7) | 15.4 | 0.99 |
| 3 | D9 ML sequence (GRU) | 5.7 (1.9–10.1) | 11.5 | −7.7 (−25.7 to 11.7) | 7.0 (2.7–12.1) | 11.5 | 0.90 |
| 4 | D1 OLS-MD | 5.2 (2.8–8.6) | 34.6 | — | 3.6 (1.8–6.0) | 30.8 | 1.15 |
| 4 | D2 MD rate | 5.2 (2.5–8.4) | 57.7 | +23.1 (4.2 to 43.3) | 0.4 (0.2–0.7) | 11.5 | 3.02 |
| 4 | D6 Pooled-detrended conformal | 5.2 (3.4–7.5) | 26.9 | −7.7 (−18.5 to 0.0) | 4.6 (2.9–6.7) | 26.9 | 1.04 |
| 4 | D8 ML tabular (LightGBM) | 5.1 (2.9–7.6) | 26.2 | −8.5 (−27.7 to 10.7) | 6.2 (3.7–8.9) | 29.2 | 0.99 |
| 4 | D9 ML sequence (GRU) | 5.3 (1.4–10.4) | 15.4 | −19.2 (−41.8 to 3.2) | 2.8 (1.1–4.8) | 15.4 | 1.13 |
| 5 | D1 OLS-MD | 5.5 (2.6–8.8) | 42.3 | — | 4.5 (2.1–7.2) | 42.3 | 1.09 |
| 5 | D2 MD rate | 5.5 (3.0–8.5) | 73.1 | +30.8 (14.8 to 50.0) | 0.9 (0.5–1.3) | 26.9 | 2.98 |
| 5 | D6 Pooled-detrended conformal | 5.2 (2.8–8.0) | 23.1 | −19.2 (−38.5 to 0.0) | 6.3 (3.7–9.2) | 30.8 | 0.92 |
| 5 | D8 ML tabular (LightGBM) | 5.3 (2.6–8.3) | 33.8 | −8.5 (−17.8 to −0.8) | 5.1 (2.7–7.8) | 31.5 | 1.00 |
| 5 | D9 ML sequence (GRU) | 6.0 (1.6–11.6) | 34.6 | −7.7 (−26.9 to 11.1) | 3.2 (0.6–6.7) | 27.7 | 1.13 |
| 6 | D1 OLS-MD | 5.2 (2.7–8.3) | 53.8 | — | 5.1 (2.5–8.1) | 61.5 | 0.98 |
| 6 | D2 MD rate | 5.2 (3.2–7.5) | 84.6 | +30.8 (15.4 to 48.0) | 1.0 (0.6–1.5) | 30.8 | 2.98 |
| 6 | D6 Pooled-detrended conformal | 5.4 (3.0–8.2) | 50.0 | −3.8 (−20.8 to 12.5) | 7.0 (4.1–10.2) | 53.8 | 0.90 |
| 6 | D8 ML tabular (LightGBM) | 5.3 (2.8–8.3) | 73.1 | +19.2 (0.8 to 37.1) | 1.8 (0.5–3.5) | 61.5 | 1.02 |
| 6 | D9 ML sequence (GRU) | 5.5 (1.7–10.1) | 42.3 | −11.5 (−34.8 to 11.5) | 1.6 (0.3–3.2) | 21.5 | 1.27 |

Each detector's continuous score was thresholded at the 95th percentile of its scores on no-change series: RC, Artes retest windows (false-alarm rate cross-fitted over five patient folds); SC, the clinic's own training eyes with their first k tests randomly re-ordered (no labels and no retest data needed). D2 score: minus the slope of mean sensitivity; D6: worst regional trend statistic. Sensitivity: 26 UWHVF test-set reference progressors. Differences: paired, patient-level bootstrap CI. pp, percentage points. Threshold ratio: SC threshold divided by RC threshold (1 = calibration source does not matter).
