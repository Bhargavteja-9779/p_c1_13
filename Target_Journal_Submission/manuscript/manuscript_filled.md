# How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm

**Running title:** False alarms in visual-field progression detection

**Authors:** P N Bhargav Teja¹; [SECOND AUTHOR NAME]¹*

¹ [Department], Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India

\* **Corresponding author:** [SECOND AUTHOR NAME], [Department], Vellore Institute of Technology (VIT), Vellore 632014, Tamil Nadu, India. E-mail: [CORRESPONDING AUTHOR E-MAIL]

**Article type:** Original Research

# Abstract

**Introduction:** Clinicians escalate glaucoma treatment when visual fields get worse. New methods claim to detect this earlier, but few have been checked on eyes that truly did not change. We asked how early progression can be detected without excess false alarms.

**Methods:** Ten detectors (trend, pointwise, permutation, conformal, event-based and machine-learning) saw only the first 3–6 tests of each eye. Sensitivity and specificity were measured against a whole-series reference in a held-out University of Washington test set (26 progressors, 26 stable eyes). False alarms were measured on 30 patients tested weekly for 12 weeks (true no change), and agreement with two criterion-based labels in 263 eyes from China (GRAPE). The analysis plan was committed before the final run.

**Results:** With three tests, the trend of mean sensitivity (D1) flagged 19.2% of progressors with 4.4% false alarms. A pooled conformal detector flagged 56.9% but raised false alarms on 22.4% (95% CI 19.3–25.7%) of no-change series; a gradient-boosted tree model raised 27.7% (95% CI 22.7–32.9%). On reference-stable eyes, both looked about as specific as D1 (96.2% and 94.6% vs 96.2%). No detector without excess false alarms flagged significantly more reference progressors than D1, but confidence intervals were wide. Reviewed four times, D1 flagged 12.6% of no-change series at least once. In GRAPE, the ranking depended on the label: against a pointwise label, D1 found 17.5% of progressors and the tree model 61.0%, at specificities of 92.8% and 61.9%.

**Conclusion:** In this benchmark, apparent early-detection gains of the tested conformal and machine-learning detectors came with excess false alarms that specificity on reference-stable eyes did not reveal. New detectors should report false alarms on true no-change data before they guide treatment escalation.

**Keywords:** Benchmark; False alarm; Glaucoma; Machine learning; Perimetry; Progression; Specificity; Visual field

# Key Summary Points

**Why carry out this study?**

- New methods claim to detect glaucomatous visual-field progression earlier, but their false-alarm rates are rarely measured on eyes that truly did not change.
- We tested the hypothesis that no detector would flag substantially more future-confirmed progressors than the trend of mean sensitivity without excess false alarms.

**What was learned from the study?**

- With three tests, the most sensitive conformal and machine-learning detectors raised false alarms on 22.4% and 27.7% of true no-change series, although they looked specific on reference-stable eyes.
- No detector without excess false alarms flagged significantly more progressors than the simple trend test, but the study could not exclude moderate gains, and in an external clinic the ranking depended on the progression label.
- Before a new detector guides treatment escalation, it should report false alarms on true no-change data, including after repeated reviews.

# Plain Language Summary

Glaucoma damages the side vision slowly. Doctors use repeated visual field tests to see whether it is getting worse, and if it is, they step up treatment. Each test is noisy, so deciding early is hard. Many new computer methods claim to spot worsening sooner. We checked ten such methods in a new way: we also gave them test results from patients who were tested every week for 12 weeks. Glaucoma does not change in 12 weeks, so any "worsening" found in these patients is a false alarm. With only three tests, two of the newer methods that looked best raised false alarms in 22.4% and 27.7% of these test series, even though they looked accurate in the usual check. The simplest method, a straight line through the average sensitivity, raised false alarms at about the expected rate. No method that avoided extra false alarms clearly found more true worsening than this simple method, although our study was small. In a clinic in China, which method looked best depended on how worsening was defined. Patients and doctors should be careful with new methods that report earlier detection unless their false-alarm rate on stable eyes is known.

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [4]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [5], but routine care rarely reaches this frequency [6]. Delays in follow-up are a documented cause of avoidable sight loss [7].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [8, 9], sometimes after spatial or temporal smoothing [10]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [11–13]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [8]. Bayesian and spatial models share information across locations or patients [14–16]. Machine-learning models have been trained to classify or forecast progression [17–22], and newer studies use deep generative models or risk-based test scheduling [23–25].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [11]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [26]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

Artes and colleagues used short-interval retest data to measure the false-alarm rate of the event-based Guided Progression Analysis [11]. We extend this approach to trend, permutation, conformal and machine-learning detectors, and add a future-confirmed reference and an external clinic. We built an open benchmark to answer one practical question: how early can visual-field progression be detected without excess false alarms? We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We tested the hypothesis that no detector would flag substantially more future-confirmed progressors (by 10 percentage points or more) than the simple trend test of mean sensitivity without excess false alarms on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate.

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

## Statistical Analysis

For each eye or window, the flag was averaged over seeds; proportions and paired differences use these averaged flags. Proportions are reported with 95% confidence intervals (CIs) from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. Paired differences from D1 use the same patient-level bootstrap. Exact McNemar tests require one flag per eye, so they use the majority flag over seeds. We corrected p-values with the Holm method within each number of tests and endpoint, over the detectors that can flag at that number. With 26 progressors, only differences of about 35 percentage points or more could reach significance after correction (all discordant pairs favouring one detector), so we interpret the comparisons mainly through their CIs.

The protocol required the false-alarm CI on true no-change data to be judged against the nominal 5%, without fixing an exact rule. We report three rules (Table 4). The main rule, used in the text, is "excess false alarms": the whole 95% CI lies above 5%. This rule does not depend on the choice of a margin. We also report an operational validity rule (upper CI limit at most 10% and lower limit at most 5%), written into the methods draft while the final run was in progress, and the literal reading of the protocol (upper CI limit at most 5%), under which no detector that works at the nominal level, including D1, could be called valid with 30 retest patients.

Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells, with a CI from 500 joint bootstrap resamples of retest and UWHVF patients, and by their absolute difference. Analyses used Python 3.13 with NumPy, SciPy, scikit-learn, LightGBM and PyTorch. The code runs the benchmark (`run_all.py --mode full`) and then generates every statistic, table and figure from the saved per-eye outputs.

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

## Real-World Measures

Table 3 translates the results into clinical units. With D1, 38% of reference progressors were flagged by the fourth test, 54% by the fifth and 69% by the sixth; the median was 5 tests, or about 4 years after the first test at the observed testing interval. At a single review with three tests, D1 would raise about 44 false flags per 1,000 no-change eyes, D6 about 224 and D8 about 277. Repeated reviews add up: over four reviews, D1 flagged 12.6% (95% CI 8.0–17.9%) of no-change series at least once, D6 29.8% (95% CI 24.6–35.4%) and D8 43.7% (95% CI 36.2–51.1%).

# Discussion

This benchmark asked how early visual-field progression can be detected without excess false alarms. In short series, the tested conformal and machine-learning detectors flagged more progressors than the trend of mean sensitivity, but they also raised far more false alarms on eyes that truly did not change. Specificity on reference-stable eyes missed these false alarms. Among detectors without excess false alarms, none flagged significantly more progressors than the trend test, but our small reference groups leave room for moderate gains.

The main lesson concerns evaluation. A pooled-detrended conformal test looked like a clear gain with three tests: it raised sensitivity 3.0-fold, with the same specificity as the trend test on reference-stable eyes. The true no-change arm, and the shuffle audit, showed that it flagged about 22.4% of no-change series. With three tests, detrending leaves one residual degree of freedom, and the pooled reference does not reflect each eye's own noise. Reference-stable eyes, defined by a long-term slope that is not negative, are an easy test of specificity. Any method whose threshold is set or checked on such eyes may look better than it is.

These findings agree with earlier work. Artes and colleagues found that the "possible progression" alert of the Guided Progression Analysis was much less specific than its "likely progression" alert, and that false alerts varied greatly between patients [11]. Wu and Medeiros compared event-based and trend-based analyses for detecting progression [12]. Machine-learning studies of progression have mostly been evaluated against labels derived from other progression criteria [17–22], and a multicentre study found that results depend strongly on the label [26]. Our external-clinic results agree: the trend test looked best against a mean-deviation label and weak against a pointwise label. Our results add a direct test of false alarms for several classes of detectors, at a fixed small number of tests, together with an estimate of how false alarms accumulate over repeated reviews.

Repeated review matters in practice. A test with a 5% false-alarm rate at each review flags more than 5% of stable eyes over several reviews. In our data, the trend test flagged 12.6% of no-change series at least once over four reviews. A practical safeguard, used in many clinics, is to confirm a flag on the next test before escalating treatment; we did not evaluate this rule. Studies of testing frequency show that clinics often need many years to confirm progression [6, 34, 35], and our real-world measures agree. Front-loading or clustering tests [5, 36] may help, but we did not test this.

What does this mean for a clinic? First, the trend of mean sensitivity with a p-value kept its nominal false-alarm rate at each review, and no detector without excess false alarms clearly beat it in our data. Second, simple rate rules without a p-value had few false alarms on our no-change data, but in the external clinic they raised false positives against both labels. Third, before adopting a new detector, a clinic can run a shuffle audit on its own records. It caught the largest problems here, but it over- or under-estimated false alarms for some detectors, so it is a screen, not a replacement for true no-change data. For commercial software that cannot be re-run, clinics can ask vendors for false-alarm rates on short-interval retest data and over repeated reviews.

For method developers, we suggest four reporting items: false alarms on true no-change series, not only specificity on stable eyes; cumulative false alarms over repeated reviews; sensitivity at a fixed, small number of tests; and results against more than one progression label. Our code and per-eye outputs are open, so new detectors can be added and compared on the same terms.

This study has limitations. First, the reference groups were small (26 progressors and 26 stable eyes), so CIs were wide, and the comparisons with D1 had low power. Second, the reference uses the whole series, including the first k tests, and is based on mean total deviation; this favours D1. The secondary PoPLR reference reduced, but did not remove, this bias, and the future-only reference had too few eyes. Third, reference-stable eyes had non-negative slopes and 80 indeterminate eyes were excluded, so specificity on UWHVF is optimistic. Fourth, the true no-change arm had only 30 patients tested a week apart. We gave each series the test dates of a clinic eye (amendment A1). This keeps it a valid null, but it does not reproduce long-term changes in noise, such as cataract, learning or fatigue, and it may favour rate rules. Fifth, the "complex" detectors are our own implementations: D6 came from our development work, D7 is a simplified analogue of commercial event analysis, and D8 and D9 are simple machine-learning baselines trained on few labelled eyes. Our conclusions apply to these detectors and should not be generalised to all conformal or machine-learning methods. Sixth, GRAPE used a different perimeter, its labels are criterion-based, and several detectors were re-calibrated or omitted there. Seventh, UWHVF has no reliability indices or diagnoses. Finally, the analysis plan was committed to our repository rather than a public registry, and it followed a development phase that used the retest data once (Table 4).

# Conclusions

In this benchmark, the tested conformal and machine-learning detectors flagged more progressors in short series only by raising excess false alarms, which specificity on reference-stable eyes did not reveal. No detector without excess false alarms flagged significantly more progressors than the trend of mean sensitivity, although moderate gains could not be excluded. Treatment escalation should not rely on a new detector until its false-alarm rate on true no-change data, including over repeated reviews, is known. Larger prospective studies with repeated short-interval testing in several clinics are needed.

# Declarations

## Acknowledgements

We thank the creators of the UWHVF, GRAPE and Artes retest data sets, and the maintainers of the visualFields R package, for making their data openly available.

## Funding

No funding or sponsorship was received for this study or publication of this article.

## Medical Writing, Editorial and Other Assistance

During this work the authors used an AI-based assistant (Claude, Anthropic) to help write analysis code and draft and edit the manuscript text. The first author directed and checked this work; all numbers were generated by the analysis code from the public data. The authors reviewed all code, results and text and take full responsibility for the content of the article.

## Author Contributions

P N Bhargav Teja: conceptualisation, methodology, software, data curation, formal analysis, visualisation, writing – original draft. [SECOND AUTHOR NAME]: supervision, validation, writing – review and editing. Both authors read and approved the final manuscript.

## Disclosures

P N Bhargav Teja and [SECOND AUTHOR NAME] declare that they have no competing interests.

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
| Added analyses | — | Cumulative false alarms over four reviews; future-only reference; GRAPE PLR2/PLR3/any labels in tables | Requested in review; exploratory except GRAPE secondary labels (planned) |
| Development use of data | Artes used once in development | D6 false-alarm excess on Artes known before the plan | D6 result is not confirmatory |
| Quick software check | Quick mode on validation subset | Quick mode also processed Artes and GRAPE files before A1/A2 | Outputs not used for any choice |
| D8 features | Features incl. PoPLR statistic and worst-region slope | 14 features: number of tests, span, level and change of mean sensitivity, its slope and z, share of declining points, mean pointwise −log p, worst-decile pointwise slope, spread measures | PoPLR-type summary (mean −log p) and worst-decile slope used instead; fixed before the final run |
