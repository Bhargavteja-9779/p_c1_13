# How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm

**Running title:** False alarms in visual-field progression detection

**Authors:** [AUTHOR NAMES, AFFILIATIONS AND ORCID TO BE ADDED BY THE AUTHORS]

**Corresponding author:** [NAME, ADDRESS, E-MAIL TO BE ADDED]

**Article type:** Original Research

# Abstract

**Introduction:** Clinicians escalate glaucoma treatment when visual fields get worse. Many new methods claim to detect this change earlier, but few have been checked on eyes that truly did not change. We asked how early progression can be detected without raising false alarms.

**Methods:** We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods, using only the first 3–6 tests of each eye. Sensitivity and specificity were measured against a future-confirmed reference in a held-out test set of the University of Washington data set (26 progressors, 26 stable eyes). False alarms were measured on 30 patients tested weekly for 12 weeks (true no change). External validity was tested in 263 eyes from China (GRAPE). The analysis was pre-registered.

**Results:** With three tests, the simple trend test (OLS-MD) flagged 19.2% of progressors with 4.4% false alarms. A pooled conformal detector flagged 56.9% (+38.5 percentage points vs D1; 95% CI 19.2 to 57.7; Holm-adjusted p = 0.018) but raised false alarms on 22.4% (95% CI 19.3–25.7%) of no-change series. Gradient-boosted trees raised 27.7% (95% CI 22.7–32.9%). Both looked about as specific as OLS-MD on reference-stable eyes (96.2% and 94.6% vs 96.2%). No detector with a valid false-alarm rate flagged significantly more progressors than OLS-MD at any number of tests. Re-running detectors on shuffled tests tracked the true false-alarm rate moderately (Spearman ρ 0.65). In GRAPE, the higher sensitivity of a rate rule and of the machine-learning model came with 16.5 and 33.5 percentage points more false positives (Holm-adjusted p < 0.001 and < 0.001).

**Conclusion:** Apparent early-detection gains were explained by false alarms that specificity on reference-stable eyes did not reveal. New detectors should report false alarms on true no-change data before clinical use.

**Keywords:** Benchmark; False alarm; Glaucoma; Machine learning; Perimetry; Progression; Specificity; Visual field

# Key Summary Points

**Why carry out this study?**

- Many new methods claim to detect glaucomatous visual-field progression earlier, but their false-alarm rates are rarely measured on eyes that truly did not change.
- We hypothesised that no detector would flag substantially more future-confirmed progressors than a simple trend test while keeping a valid false-alarm rate.

**What was learned from the study?**

- With three tests, the most sensitive pooled conformal and machine-learning detectors raised false alarms on 22.4% and 27.7% of true no-change series, although they looked specific on reference-stable eyes.
- No detector with a valid false-alarm rate flagged significantly more progressors than the trend of mean sensitivity at 3–6 tests, in Seattle or in an external clinic in China.
- Before a new detector guides treatment escalation, it should report false alarms on true no-change data; a shuffle audit of a clinic's own records is a useful but imperfect screen.

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [4]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [5], but routine care rarely reaches this frequency [6]. Delays in follow-up are a documented cause of avoidable sight loss [7].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [8, 9], sometimes after spatial or temporal smoothing [10]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [11–13]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [8]. Bayesian and spatial models share information across locations or patients [14–16]. Machine-learning models have been trained to classify or forecast progression [17–22], and newer studies use deep generative models or risk-based test scheduling [23–25].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [11]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [26]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

We built an open benchmark to answer one practical question: how early can visual-field progression be detected without raising false alarms? The benchmark has a true no-change arm, a future-confirmed reference standard and an external clinic. We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We tested the hypothesis that no detector would flag substantially more future-confirmed progressors (by 10 percentage points or more) than the simple trend test of mean sensitivity while keeping a valid false-alarm rate on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate.

# Methods

## Study Design and Reporting

This was a retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [27]. The analysis plan, including all ten detectors, thresholds, reference standards, research questions and statistical tests, was written down and time-stamped before the final test data were analysed (code repository, `experiments/protocol.md`). Two amendments were made before any final result was seen; both are reported below. The study was preceded by a development phase in which we tried, and abandoned, several new detection methods. Every idea from that phase, with its result, is listed in Supplementary Material S1.

## Data Sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains 28,943 24-2 tests from 7,428 eyes of 3,871 patients seen in routine care in Seattle, USA [28]. It includes sensitivities, total deviation values, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. Eyes with at least three tests were used (2,643 training, 940 validation and 869 test eyes). The test set was used once, for the final analysis.

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [11]. Glaucoma does not change measurably in 12 weeks, so any "progression" flag in these series is a false alarm. The data (360 tests from 30 eyes) are distributed with the visualFields R package (version 1.0.7).

*GRAPE (external clinic).* The GRAPE data set contains 1,115 follow-up visual-field records from 263 eyes of 144 patients with glaucoma followed in Hangzhou, China [29]. Fields were measured with a different perimeter (59 analysable points after removing untested points). Each eye carries progression labels assigned with three criteria: mean deviation, and two pointwise linear regression rules. We used the mean-deviation label as the primary label (27 progressing eyes).

## Reference Standard (UWHVF)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5. Other eyes were excluded from the sensitivity and specificity analysis. Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations), which is not tied to mean deviation.

## Detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 OLS-MD:** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD rate:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [8], using all possible orders of the k tests.
- **D5 pooled-shuffle conformal test:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of training-set eyes with the same number of tests and similar mean sensitivity (a conformal p-value [30, 31]).
- **D6 pooled-detrended conformal regional test:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [32]. This variant was the most sensitive approach during development.
- **D7 event analysis:** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to Guided Progression Analysis [13]. It needs at least four tests.
- **D8 machine learning, tabular:** gradient-boosted trees (LightGBM) on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set stable eyes, as is common in machine-learning studies.
- **D9 machine learning, sequence:** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 self-supervised order network:** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [33].

Stochastic detectors (D4–D6, D8–D10) were run with five seeds; we report the mean over seeds. With three tests there are only six possible orders, so D4 and D10 cannot reach p < 0.05; this is a property of the methods, not a failure of the code.

## Evaluation

*E1 future reference.* In UWHVF test-set eyes with at least eight tests, we measured sensitivity (share of reference progressors flagged) and specificity (share of reference-stable eyes not flagged) using only the first k tests.

*E2 true no-change.* In the Artes data we took every window of k consecutive tests. Because rate-based rules depend on the time scale, each window was given the test dates of a randomly chosen UWHVF test-set eye (ten draws per window; amendment A1). The share of windows flagged is the false-alarm rate.

*E3 shuffle audit.* In UWHVF test-set eyes, we randomly re-ordered the first k tests (ten times) and re-ran each detector. Shuffling removes any true trend, so the flag rate estimates the false-alarm rate without retest data.

*E4 external clinic.* In GRAPE, we applied the detectors to the first three or four tests of each eye and compared flags with the clinicians' labels. D5 and D7 were re-calibrated on GRAPE itself by five-fold patient-level cross-fitting, because the perimeter differs; D8 was transferred unchanged from UWHVF; the 24-2-specific detectors (D6, D9, D10) were not applied (amendment A2).

*Real-world measures.* We translated results into two clinical units, as planned: the number of false progression flags per 1,000 stable eyes at each review, and the number of tests until a future-confirmed progressor is first flagged. For the second measure, an eye counted as flagged by test k if any review with 3 to k tests flagged it. As an exploratory measure that was not pre-registered, we also report the share of reference-stable eyes flagged at least once over the four reviews.

## Statistical Analysis

Proportions are reported with 95% confidence intervals (CIs) from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. We compared each detector with D1 on the same eyes using the exact McNemar test and corrected p-values for the nine comparisons within each number of tests and endpoint with the Holm method. The protocol required the false-alarm CI on true no-change data to be judged against the nominal 5%. Before the results were seen, we made this rule operational: a detector was valid if the upper limit of its false-alarm CI did not exceed 10% and the lower limit did not exceed 5%. Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells and by their absolute difference. Analyses used Python 3.13 with NumPy, SciPy, scikit-learn, LightGBM and PyTorch. One command (`run_all.py --mode full`) reproduces every number, table and figure.

## Disclosure of Development Use of Data

During development, the Artes data were used once to check the false-alarm rate of candidate methods (Supplementary Material S1). This check led us to abandon these methods as new proposals; it did not change any detector, threshold or reference in the final protocol. The UWHVF test set and GRAPE were not used before the final run.

## Ethics

This study used only publicly available, de-identified data sets released by their custodians (UWHVF: BSD-3 licence; GRAPE: CC0; Artes data: distributed with the visualFields R package, Apache-2.0 licence). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

# Results

## Study Data

In the UWHVF test set, 132 eyes had at least eight tests. Of these, 26 were reference progressors, 26 were reference stable and 80 were indeterminate. The 26 + 26 reference eyes came from 41 patients. Their median age at the first test was 58.8 years (interquartile range [IQR] 50.3–64.4), median mean total deviation at the first test was −4.4 dB (IQR −6.0 to −3.2), and median follow-up was 12.9 years with 11 tests. The median interval between tests was 1.0 years, so each additional test represents about one more year of follow-up. The true no-change arm contributed 3,000 three-test windows (including time-label draws). In GRAPE, all 263 eyes had at least three visits and 163 had at least four. The full run took 1,458 seconds on a four-core CPU.

## False Alarms on True No-Change Data (RQ1)

Table 1 and Fig. 2 show all results. With three tests, 7 of 10 detectors were valid. The invalid detectors were D6, D8 and D9. The pooled-detrended conformal detector (D6) raised false alarms on 22.4% (95% CI 19.3–25.7%) of no-change series. The tabular machine-learning model (D8) raised 27.7% (95% CI 22.7–32.9%), and the sequence model (D9) raised 12.7% (95% CI 6.2–20.0%). The simple trend test (D1) stayed close to its nominal level, at 4.4% (95% CI 2.8–6.3%). The invalid detectors were D8 with four tests, D8 and D9 with five tests and D6 and D9 with six tests. D8 remained invalid with four tests, at 9.4% (95% CI 6.3–12.9%), and with five tests, at 18.8% (95% CI 13.1–24.9%). D9 with six tests, at 5.9% (95% CI 2.3–10.0%), failed the rule only narrowly.

## Specificity on Reference-Stable Eyes Hid These False Alarms

The usual check, specificity on reference-stable eyes, did not reveal these false alarms. With three tests, D6 was 96.2% specific and D8 was 94.6% specific, compared with 96.2% for D1. Neither difference was significant (exact McNemar test, Holm-adjusted p = 1.00 for D6 and p = 1.00 for D8). Yet on true no-change series, D6 and D8 raised 5.0 and 6.3 times as many false alarms as D1. Reference-stable eyes are selected for a flat long-term course, so they may be easier to classify than typical stable eyes.

## Sensitivity Compared With the Trend Test (RQ2)

With three tests, D1 flagged 19.2% (95% CI 7.4–33.3%) of reference progressors. The largest gain came from D6, which flagged 56.9% (+38.5 percentage points vs D1; 95% CI 19.2 to 57.7; Holm-adjusted p = 0.018). This was the only significant gain in the study, and it came from an invalid detector. Among valid detectors, the rate rule D2 had the largest point gain with three tests: it flagged 38.5% (+19.2 percentage points vs D1; 95% CI 0.0 to 42.3; Holm-adjusted p = 0.72). With four to six tests, D1 flagged 30.8%, 42.3% and 57.7% of progressors. Event analysis (D7) flagged 50.0% at five tests (+7.7 percentage points vs D1; 95% CI −11.5 to 26.9; Holm-adjusted p = 1.00). With six tests, D8 was valid and flagged 70.8% (+11.5 percentage points vs D1; 95% CI −7.7 to 30.8; Holm-adjusted p = 1.00). Rate and pointwise rules gained little after four or five tests; at six tests, D3 flagged 23.1% (-34.6 percentage points vs D1; 95% CI −53.8 to −19.2; Holm-adjusted p = 0.035). Therefore, the hypothesis was not falsified: no valid detector beat D1 by 10 percentage points or more with a Holm-adjusted p < 0.05. However, the CIs were wide, and gains of this size cannot be excluded for D2 at three tests or D8 at six tests.

The secondary, PoPLR-based reference gave lower sensitivities but a similar ordering of detectors (Spearman ρ between 0.70 and 1.00 across detectors, within each number of tests; Supplementary Table S2). For example, with five tests D1 flagged 27.6% and D7 flagged 31.0% of the 58 secondary-reference progressors.

## Machine-Learning Detectors Under the Usual Threshold Rule (RQ4)

Both supervised models were thresholded at 95% specificity on validation-set reference-stable eyes, as is common in machine-learning studies. On true no-change data, D8 exceeded the nominal 5% at three, four and five tests (27.7%, 9.4% and 18.8%) but not at six tests (3.6%). D9 exceeded it at three tests (12.7%) and five tests (7.5%). The hypothesis that this threshold rule gives too many false alarms was therefore supported for short series, but not at every number of tests.

## The Shuffle Audit (RQ3)

Across the 40 detector–test-number cells, the shuffle audit and the true no-change false-alarm rate were correlated (Spearman ρ 0.65, p < 0.001; Fig. 3). The median absolute difference was 1.0 percentage points, and 80% of cells differed by 3 percentage points or less. The audit correctly flagged D6 and D8 at three tests as invalid (shuffle false-alarm rates 22.5% and 17.3%). It over-estimated false alarms for rate rules and event analysis (for example, D2 at three tests: 11.7% vs 2.6%; D7 at six tests: 11.7% vs 1.9%). It under-estimated them for the machine-learning models with three tests (D8: 17.3% vs 27.7%; D9: 8.5% vs 12.7%). The largest difference was 10.4 percentage points. The pre-registered target of ρ ≥ 0.7 was not met, so the hypothesis was only partly supported.

## External Clinic (RQ5)

In GRAPE (Table 2, Fig. 4), D1 flagged 44.4% (95% CI 25.9–65.4%) of clinician-labelled progressors with three tests, with 95.3% specificity. The rate rule D2 flagged 59.3% (+14.8 percentage points vs D1; 95% CI −11.1 to 37.0; Holm-adjusted p = 0.78), but its specificity fell to 78.8% (16.5 percentage points more false positives; Holm-adjusted p < 0.001). The machine-learning model D8, transferred unchanged, flagged 65.9% (+25.9 percentage points vs D1; 95% CI 0.0 to 48.1; Holm-adjusted p = 0.28), with specificity 61.2% (33.5 percentage points more false positives; Holm-adjusted p < 0.001). With four tests, the pattern was the same: D2 and D8 gained sensitivity only with significantly more false positives (9.7 and 14.5 percentage points more false positives; Holm-adjusted p = 0.007 and < 0.001). The re-calibrated conformal test (D5) matched D1 (41.5% vs 44.4% sensitivity at three tests). The GRAPE progressor group was small (27 eyes at three tests and 18 at four), so these sensitivity estimates are imprecise.

## Real-World Measures

Table 3 translates the results into clinical units. With D1, 38% of future-confirmed progressors were flagged by the fourth test, 54% by the fifth and 69% by the sixth; the median was 5 tests. D1 produced about 44 false flags per 1,000 no-change eyes at the three-test review. D6 flagged progressors earlier (median 3 tests) but would raise about 224 false flags per 1,000 no-change eyes at the three-test review. D8 would raise about 277. In a clinic reviewing 1,000 stable eyes, that is roughly 224 and 277 unnecessary escalation discussions instead of 44.

# Discussion

This benchmark asked a simple question: how early can visual-field progression be detected without raising false alarms? The answer, in two clinics, was that the simple trend of mean sensitivity was hard to beat. More complex detectors did flag more progressors in short series. But when they did, they also raised far more false alarms on eyes that truly did not change. The usual check, specificity on reference-stable eyes, missed these false alarms.

The main lesson is about evaluation, not about any one method. Our own development history shows the risk. A pooled-detrended conformal test looked like a clear gain with three tests: it raised sensitivity 3.0-fold, with the same specificity as the trend test on reference-stable eyes. Only the true no-change arm, and the shuffle audit, showed that it flagged about 22.4% of no-change series. The cause was simple. With three tests, detrending leaves one residual degree of freedom, and the pooled reference does not reflect the eye's own noise. Similar problems can affect any method whose false-alarm rate is set on selected stable eyes rather than on true no-change data.

These findings agree with earlier work. Artes and colleagues used the same retest data to examine the specificity of the event-based Guided Progression Analysis [11]. Its "possible progression" alert was much less specific than its "likely progression" alert, and false alerts varied greatly between patients. Our study extends this approach to trend, permutation, conformal and machine-learning detectors. Wu and Medeiros compared pointwise event-based and global trend-based analyses for detecting progression [12]. Machine-learning studies of progression have mostly been evaluated against labels derived from other progression criteria [17–22], and a multicentre study found that results depend strongly on the progression label [26]. Our results add a direct test: with the usual threshold rule, two machine-learning models exceeded the nominal false-alarm rate on true no-change data in short series. The models may still be useful, but their thresholds need to be set on no-change data. Studies of testing frequency show that clinics often need many years to confirm progression [6, 34, 35]. Our real-world measures agree: with about one test per year, the trend test needed a median of 5 tests. Front-loading or clustering tests [5, 36] is therefore likely to help more than a more complex detector.

What should a clinic do? First, the trend of mean sensitivity, with a p-value, remains a sound default. It kept its nominal false-alarm rate and was not beaten by a valid detector. Second, a fast-rate rule without a p-value (D2) had the largest point gain among valid detectors with three tests. But in the external clinic, the same rule raised false positives significantly. Third, before adopting a new detector, a clinic can run a shuffle audit on its own records. In our data the audit caught the largest problems. However, it over-estimated false alarms for rate and event rules and agreed only moderately overall. It is a screen, not a replacement for true no-change data.

For method developers, we suggest three reporting items. Report false alarms on true no-change series, not only specificity on stable eyes. Report sensitivity at a fixed, small number of tests. Report results from a second clinic with its own labels. Our code and data pipeline are open, so new detectors can be added and compared on the same terms.

This study has limitations. First, the reference groups were small (26 progressors and 26 stable eyes), so CIs were wide. We cannot exclude gains of 10–20 percentage points for some valid detectors, such as D2 at three tests and D8 at six tests. Second, the true no-change arm had only 30 patients, tested a week apart. We gave each series the test dates of a clinic eye, which keeps it a valid null but does not reproduce long-term changes in noise, such as cataract or learning. Third, the primary reference is based on mean deviation, which may favour detectors based on mean sensitivity; the PoPLR-based secondary reference gave a similar ordering. Fourth, reference-stable eyes were chosen for a very flat course, which makes specificity look better than in typical stable eyes; we regard this as a finding, but it also means our specificity estimates are optimistic. Fifth, UWHVF has no reliability indices or diagnoses, and GRAPE uses a different perimeter, so several detectors had to be re-calibrated or omitted there. Sixth, we re-implemented event analysis and did not test commercial software. Seventh, the machine-learning models used a fixed tuning budget; larger models or other thresholds may behave differently. Finally, we used the Artes data once during development, which we disclose; it did not change the final protocol.

# Conclusions

In this benchmark, no detector with a valid false-alarm rate flagged significantly more future-confirmed progressors than the simple trend of mean sensitivity. Apparent early-detection gains of conformal and machine-learning detectors came with false alarms that specificity on stable eyes did not reveal. Treatment escalation decisions should not rely on a new detector until its false-alarm rate on true no-change data is known. Prospective studies with repeated short-interval testing in more clinics are needed to confirm these findings and to set valid thresholds.

# Declarations

## Acknowledgements

We thank the creators of the UWHVF, GRAPE and Artes retest data sets, and the maintainers of the visualFields R package, for making their data openly available.

## Funding

[AUTHORS TO CONFIRM: No funding or sponsorship was received for this study or publication of this article.] The journal's Rapid Service Fee: [AUTHORS TO CONFIRM WHO PAYS].

## Medical Writing, Editorial and Other Assistance

An AI assistant (Claude, Anthropic) was used to write analysis code and to draft and edit the manuscript under the authors' direction. All numbers were generated by the analysis code from the public data. The authors checked all content and take full responsibility for it.

## Author Contributions

[AUTHORS TO ADD, CRediT format: conceptualisation, methodology, software, formal analysis, writing – original draft, writing – review and editing.]

## Disclosures

[AUTHORS TO ADD. Suggested: The authors declare no competing interests.]

## Compliance With Ethics Guidelines

This study used only publicly available, de-identified data sets released by their custodians under open licences. The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

## Data Availability

All data sets are public: UWHVF (https://github.com/uw-biomedical-ml/uwhvf), GRAPE (Figshare file 41670009, "VF and clinical information.xlsx", described in [29]) and the Artes retest data (visualFields R package 1.0.7, CRAN). The analysis code, pre-registered protocol, raw per-eye detector outputs and all result files are available from [CODE REPOSITORY URL TO BE ADDED ON SUBMISSION].

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

| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | False alarms, true no-change, % (95% CI) | False alarms, shuffle audit, % | Valid |
|---|---|---|---|---|---|---|
| 3 | D1 OLS-MD | 19.2 (7.4–33.3) | 96.2 (87.0–100.0) | 4.4 (2.8–6.3) | 4.8 | Yes |
| 3 | D2 MD rate | 38.5 (20.0–56.5) | 92.3 (80.0–100.0) | 2.6 (1.5–3.9) | 11.7 | Yes |
| 3 | D3 PLR-3 | 3.8 (0.0–12.5) | 96.2 (88.0–100.0) | 1.4 (1.0–1.8) | 1.8 | Yes |
| 3 | D4 PoPLR | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | Yes |
| 3 | D5 Pooled-shuffle conformal | 19.2 (7.4–33.3) | 96.2 (87.0–100.0) | 4.0 (2.7–5.6) | 4.6 | Yes |
| 3 | D6 Pooled-detrended conformal | 56.9 (37.0–76.2) | 96.2 (87.0–100.0) | 22.4 (19.3–25.7) | 22.5 | **No** |
| 3 | D7 Event analysis | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | Yes |
| 3 | D8 ML tabular (LightGBM) | 26.2 (12.3–43.2) | 94.6 (84.8–100.0) | 27.7 (22.7–32.9) | 17.3 | **No** |
| 3 | D9 ML sequence (GRU) | 12.3 (2.4–24.8) | 95.4 (88.8–100.0) | 12.7 (6.2–20.0) | 8.5 | **No** |
| 3 | D10 Self-supervised order net | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | 0.0 (0.0–0.0) | 0.0 | Yes |
| 4 | D1 OLS-MD | 30.8 (14.3–48.1) | 100.0 (100.0–100.0) | 3.8 (1.9–6.2) | 4.7 | Yes |
| 4 | D2 MD rate | 23.1 (8.0–40.0) | 96.2 (87.5–100.0) | 0.6 (0.4–0.9) | 6.4 | Yes |
| 4 | D3 PLR-3 | 15.4 (3.6–30.8) | 100.0 (100.0–100.0) | 0.2 (0.0–0.3) | 1.5 | Yes |
| 4 | D4 PoPLR | 3.8 (0.0–12.5) | 100.0 (100.0–100.0) | 3.3 (1.8–4.9) | 4.1 | Yes |
| 4 | D5 Pooled-shuffle conformal | 30.8 (14.3–48.1) | 100.0 (100.0–100.0) | 3.6 (1.8–5.9) | 4.9 | Yes |
| 4 | D6 Pooled-detrended conformal | 25.4 (10.3–44.0) | 100.0 (100.0–100.0) | 5.1 (3.4–7.2) | 5.5 | Yes |
| 4 | D7 Event analysis | 23.1 (7.7–40.0) | 100.0 (100.0–100.0) | 1.1 (0.0–2.6) | 5.2 | Yes |
| 4 | D8 ML tabular (LightGBM) | 41.5 (23.7–59.2) | 99.2 (97.4–100.0) | 9.4 (6.3–12.9) | 7.7 | **No** |
| 4 | D9 ML sequence (GRU) | 11.5 (2.8–23.2) | 99.2 (97.6–100.0) | 2.0 (0.6–3.7) | 4.7 | Yes |
| 4 | D10 Self-supervised order net | 20.0 (7.7–35.8) | 100.0 (100.0–100.0) | 3.8 (2.5–5.1) | 4.1 | Yes |
| 5 | D1 OLS-MD | 42.3 (23.1–61.5) | 100.0 (100.0–100.0) | 4.7 (2.2–7.5) | 5.1 | Yes |
| 5 | D2 MD rate | 23.1 (7.7–41.4) | 100.0 (100.0–100.0) | 0.8 (0.5–1.2) | 3.6 | Yes |
| 5 | D3 PLR-3 | 23.1 (8.0–40.0) | 100.0 (100.0–100.0) | 0.5 (0.1–1.1) | 1.4 | Yes |
| 5 | D4 PoPLR | 38.5 (20.0–57.7) | 100.0 (100.0–100.0) | 3.9 (1.9–6.2) | 4.3 | Yes |
| 5 | D5 Pooled-shuffle conformal | 42.3 (23.1–61.5) | 100.0 (100.0–100.0) | 4.3 (2.0–7.1) | 4.9 | Yes |
| 5 | D6 Pooled-detrended conformal | 31.5 (16.0–48.5) | 100.0 (100.0–100.0) | 6.2 (3.7–8.9) | 5.0 | Yes |
| 5 | D7 Event analysis | 50.0 (30.4–69.6) | 100.0 (100.0–100.0) | 1.2 (0.0–2.9) | 7.9 | Yes |
| 5 | D8 ML tabular (LightGBM) | 56.2 (36.1–74.8) | 99.2 (97.6–100.0) | 18.8 (13.1–24.9) | 16.1 | **No** |
| 5 | D9 ML sequence (GRU) | 40.8 (22.8–59.2) | 93.8 (82.4–100.0) | 7.5 (2.8–13.3) | 8.1 | **No** |
| 5 | D10 Self-supervised order net | 43.8 (28.0–60.0) | 100.0 (100.0–100.0) | 5.1 (2.9–7.6) | 4.2 | Yes |
| 6 | D1 OLS-MD | 57.7 (38.4–76.9) | 100.0 (100.0–100.0) | 5.1 (2.5–8.1) | 5.9 | Yes |
| 6 | D2 MD rate | 23.1 (8.3–38.5) | 100.0 (100.0–100.0) | 1.0 (0.6–1.5) | 2.8 | Yes |
| 6 | D3 PLR-3 | 23.1 (7.7–41.7) | 100.0 (100.0–100.0) | 0.3 (0.0–0.8) | 1.2 | Yes |
| 6 | D4 PoPLR | 50.0 (30.8–67.9) | 100.0 (100.0–100.0) | 5.0 (2.4–8.4) | 4.8 | Yes |
| 6 | D5 Pooled-shuffle conformal | 56.9 (37.7–76.0) | 100.0 (100.0–100.0) | 5.0 (2.4–7.9) | 5.0 | Yes |
| 6 | D6 Pooled-detrended conformal | 53.8 (37.0–71.4) | 100.0 (100.0–100.0) | 7.6 (4.5–11.1) | 4.9 | **No** |
| 6 | D7 Event analysis | 57.7 (36.0–77.8) | 100.0 (100.0–100.0) | 1.9 (0.5–3.8) | 11.7 | Yes |
| 6 | D8 ML tabular (LightGBM) | 70.8 (51.7–88.8) | 100.0 (100.0–100.0) | 3.6 (1.7–6.0) | 8.7 | Yes |
| 6 | D9 ML sequence (GRU) | 37.7 (22.3–53.8) | 91.5 (75.2–100.0) | 5.9 (2.3–10.0) | 8.6 | **No** |
| 6 | D10 Self-supervised order net | 54.6 (36.9–70.8) | 99.2 (97.6–100.0) | 5.7 (3.0–9.2) | 4.7 | Yes |

Sensitivity: 26 reference progressors; specificity: 26 reference-stable eyes (first k tests only). True no-change: all windows of k consecutive tests in 30 Artes retest patients, 10 time-label draws per window. Shuffle audit: UWHVF test-set eyes with their first k tests randomly re-ordered, 10 times. Valid: 95% CI of the true no-change false-alarm rate has an upper limit of at most 10% and a lower limit of at most 5%. Stochastic detectors (D4–D6, D8–D10): mean over 5 seeds. CI: patient-level bootstrap (2,000 resamples). D4, D7 and D10 cannot flag at 3 tests by design.

**Table 2** External clinic (GRAPE): agreement with the clinicians' mean-deviation progression label

| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | Change in false positives vs D1, pp (Holm p) |
|---|---|---|---|---|
| 3 | D1 OLS-MD | 44.4 (25.9–65.4) | 95.3 (92.2–97.9) | — |
| 3 | D2 MD rate | 59.3 (40.7–76.9) | 78.8 (73.5–83.9) | +16.5 (<0.001) |
| 3 | D3 PLR-3 | 3.7 (0.0–11.5) | 95.8 (92.7–98.3) | -0.4 (1.00) |
| 3 | D4 PoPLR | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | -4.7 (0.004) |
| 3 | D5 Pooled-shuffle conformal | 41.5 (23.8–60.0) | 95.4 (92.4–98.0) | +0.0 (1.00) |
| 3 | D7 Event analysis | 0.0 (0.0–0.0) | 100.0 (100.0–100.0) | -4.7 (0.004) |
| 3 | D8 ML tabular (LightGBM) | 65.9 (50.8–80.0) | 61.2 (54.6–67.1) | +33.5 (<0.001) |
| 4 | D1 OLS-MD | 33.3 (11.8–55.0) | 95.9 (92.2–98.6) | — |
| 4 | D2 MD rate | 55.6 (35.3–76.5) | 86.2 (79.4–92.1) | +9.7 (0.007) |
| 4 | D3 PLR-3 | 11.1 (0.0–25.0) | 97.9 (95.2–100.0) | -2.1 (1.00) |
| 4 | D4 PoPLR | 22.2 (5.9–41.2) | 95.2 (91.4–98.0) | +0.7 (1.00) |
| 4 | D5 Pooled-shuffle conformal | 33.3 (11.8–55.0) | 94.5 (90.8–97.7) | +1.4 (1.00) |
| 4 | D7 Event analysis | 16.7 (0.0–33.3) | 95.9 (92.4–98.7) | +0.0 (1.00) |
| 4 | D8 ML tabular (LightGBM) | 48.9 (31.8–65.9) | 81.5 (74.2–87.9) | +14.5 (<0.001) |

n = 27 labelled progressors and 236 non-progressors at 3 tests; 18 and 145 at 4 tests. D5 and D7 calibrated on GRAPE by 5-fold patient-level cross-fitting; D8 transferred unchanged from UWHVF; D6, D9, D10 not applicable (24-2 specific). pp, percentage points; Holm p, exact McNemar test vs D1 with Holm correction.

**Table 3** Real-world measures: tests to first flag in future-confirmed progressors and false flags per 1,000 stable eyes

| Detector | Progressors flagged by test 4 / 5 / 6, % | Median tests to first flag | False flags per 1,000 no-change eyes at test 3 / 4 / 5 / 6 | Stable eyes ever flagged over tests 3–6, % (exploratory) |
|---|---|---|---|---|
| D1 OLS-MD | 38 / 54 / 69 | 5 | 44 / 38 / 47 / 51 | 4 |
| D2 MD rate | 38 / 46 / 46 | > 6 | 26 / 6 / 8 / 10 | 8 |
| D3 PLR-3 | 19 / 31 / 38 | > 6 | 14 / 2 / 5 / 3 | 4 |
| D4 PoPLR | 4 / 38 / 54 | 6 | 0 / 33 / 39 / 50 | 0 |
| D5 Pooled-shuffle conformal | 38 / 54 / 68 | 5 | 40 / 36 / 44 / 50 | 4 |
| D6 Pooled-detrended conformal | 58 / 65 / 77 | 3 | 224 / 51 / 62 / 76 | 4 |
| D7 Event analysis | 23 / 50 / 58 | 5.5 | 0 / 11 / 12 / 19 | 0 |
| D8 ML tabular (LightGBM) | 52 / 63 / 78 | 4 | 277 / 94 / 188 / 36 | 7 |
| D9 ML sequence (GRU) | 16 / 46 / 59 | 6 | 127 / 20 / 76 / 59 | 11 |
| D10 Self-supervised order net | 20 / 51 / 63 | 5 | 0 / 38 / 51 / 57 | 1 |

Progressors: 26 UWHVF test-set reference progressors; an eye counts as flagged by test k if any look at 3..k tests flagged it. Median tests: '> 6' means fewer than half were flagged by 6 tests. In UWHVF the median interval between tests was 1.0 years, so each extra test is roughly one extra year of follow-up. False flags per 1,000 = 1,000 × true no-change false-alarm rate. Last column: share of 26 reference-stable eyes flagged at least once over the four looks (not pre-registered).
