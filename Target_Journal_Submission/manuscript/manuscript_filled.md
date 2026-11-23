# Detecting Glaucomatous Visual Field Progression From Few Tests Without False Alarms: A Benchmark With a True No-Change Arm

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, AFFILIATIONS, ADDRESSES AND ORCID iDs — TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — TO BE COMPLETED]

**Prior presentation:** None. [AUTHORS TO CONFIRM]

## Abstract

**Introduction:** Many new detectors claim to find glaucomatous visual field progression earlier, which would allow earlier treatment escalation, but their false-alarm rates are rarely measured on data without change. We asked how early progression can be detected from the first few fields without raising false alarms.

**Methods:** In this retrospective benchmark of public data, ten detectors (trend, event, permutation, conformal, machine learning) saw the first 3–6 fields of each series. We measured sensitivity and specificity against a future-confirmed reference in held-out eyes of the University of Washington data set (26 progressing, 26 stable), false-alarm rates on true no-change series (30 patients tested weekly for 12 weeks), a "shuffle audit", and an external data set from China (263 eyes, different perimeter).

**Results:** With three fields, the trend test of mean sensitivity flagged 19% of progressors with a false-alarm rate of 4.4% (95% CI 2.8–6.3). Two detectors flagged more progressors only with excess false alarms: a pooled-detrended conformal test (57% sensitivity; 22.4% false alarms) and gradient-boosted trees thresholded at 95% specificity (26%; 27.7%). Reference-stable eyes did not reveal this: their specificity was 96% and 95%. 8 of 40 detector–field-number combinations had invalid false-alarm rates. No detector with a valid false-alarm rate flagged significantly more progressors than the trend test at any number of fields. The shuffle audit tracked the true false-alarm rate (Spearman ρ = 0.65; 80% of combinations within 3 percentage points). Externally, the machine-learning detector had specificity 61% versus 95% for the trend test.

**Conclusion:** In this benchmark, the largest apparent early-detection gains were false alarms that standard specificity estimates missed. Progression detectors should be reported with false-alarm rates on true no-change data; a simple trend test remains a strong default, and clinics can check a detector on their own records with a shuffle audit.

**Keywords:** Benchmarking; False alarms; Glaucoma; Machine learning; Perimetry; Progression detection; Visual field

## Key Summary Points

**Why carry out this study?**

- Glaucoma treatment is escalated when visual field tests show progression, and many new detectors claim to find progression earlier, but most are judged by how many eyes they flag rather than by how many of those flags are false.

- We asked whether any of ten detectors could flag future-confirmed progression from three to six fields more often than a simple trend test while keeping false alarms on true no-change data at the nominal 5%.

**What was learned from the study?**

- With three fields, the two detectors that flagged the most progressors (57% and 26% versus 19% for the trend test) raised false alarms in 22.4% and 27.7% of true no-change series, which specificity in reference-stable eyes did not reveal.

- No detector with a valid false-alarm rate beat the simple trend test significantly at any number of fields, so the evidence does not support replacing it in routine care.

- Reports of new progression detectors should include false-alarm rates on true no-change data, and a shuffle audit of a clinic's own records is a cheap first check.

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [4]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [5], but routine care rarely reaches this frequency. Delays in follow-up are a documented cause of avoidable sight loss [6].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [7, 8]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [9–11]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [7]. Bayesian and spatial models share information across locations or patients [12–14]. More recently, machine-learning models have been trained to classify or forecast progression [15–20], and some newer studies use deep generative models or risk-based test scheduling [21, 22].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [9]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [23]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

We built a benchmark to answer one practical question: how early can visual-field progression be detected without raising false alarms? The benchmark has a true no-change arm, a future-confirmed reference standard, and an external clinic. We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We hypothesised that no detector would flag substantially more future-confirmed progressors than the simple trend test of mean sensitivity while keeping a valid false-alarm rate on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate.

# Methods

## Study design and reporting

This was a retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [24]. The analysis plan, including all ten detectors, thresholds, reference standards and statistical tests, was written down and time-stamped before the final test data were analysed (`experiments/protocol.md`, available with the code). Two amendments were made before any final result was seen; both are reported below. Ideas that we developed and abandoned during the study are listed in the Supplementary Material.

## Data sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains 28,943 24-2 tests from 7,428 eyes of 3,871 patients seen in routine care [25]. It includes sensitivities, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. The test set was used once, for the final analysis.

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [9]. Glaucoma does not change in 12 weeks in a measurable way, so any "progression" flag in these series is a false alarm. The data are distributed with the visualFields R package (version 1.0.7) [26].

*GRAPE (external clinic).* The GRAPE data set contains 1,115 visual-field records from 263 eyes of 144 patients with glaucoma followed in Hangzhou, China [27]. Fields were measured with the G1 pattern of the Octopus 900 perimeter (Haag-Streit, Köniz, Switzerland), not the Humphrey 24-2 pattern. The data set authors labelled each eye with three rule-based criteria applied to the whole follow-up: a negative slope of mean deviation with p < 0.05 (MD label), and at least two or three locations with a significant negative pointwise slope (PLR2, PLR3) [27]. We used the MD label as the primary label. These labels are not clinicians' judgements, and with a median of 4 visits per eye the first three or four fields make up most of the series on which each label was computed.

## Reference standard (UWHVF)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5. Other eyes were excluded from the sensitivity and specificity analysis. Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations), which is not tied to mean deviation.

## Detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 OLS-MD:** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD rate:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [7], using all possible orders of the k tests.
- **D5 pooled-shuffle conformal test:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of other patients in the training set, matched by number of tests and mean sensitivity (a conformal p-value [28]).
- **D6 pooled-detrended conformal regional test:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [29]. This variant was the most sensitive approach during development.
- **D7 event analysis:** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to Guided Progression Analysis [11].
- **D8 machine learning, tabular:** gradient-boosted trees on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set reference-stable eyes.
- **D9 machine learning, sequence:** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 self-supervised order network:** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [30].


## Evaluation

*E1 future reference.* In UWHVF test-set eyes with at least eight tests, we measured sensitivity (share of reference progressors flagged) and specificity (share of reference stable eyes not flagged) using only the first k tests.

*E2 true no-change.* In the Artes data we took every window of k consecutive tests. Because rate-based rules depend on the time scale, each window was given the test dates of a randomly chosen UWHVF test-set eye (ten draws per window; amendment A1). The share of windows flagged is the false-alarm rate.

*E3 shuffle audit.* In UWHVF test-set eyes, we randomly re-ordered the first k tests (ten times) and re-ran each detector. Shuffling removes any true trend, so the flag rate estimates the false-alarm rate without retest data.

*E4 external clinic.* In GRAPE, we applied the detectors to the first three or four tests of each eye and compared flags with the data set's progression labels. D5 and D7 were re-calibrated on GRAPE itself by five-fold patient-level cross-fitting, because the perimeter differs; D8 was transferred unchanged from UWHVF; the 24-2-specific detectors (D6, D9, D10) were not applied (amendment A2).

*Real-world measures (pre-specified).* We expressed false alarms as expected false progression flags per 1,000 stable eyes at one review, and earliness as the number of fields until the first flag among reference progressors (followed until six fields; eyes not flagged by six fields were counted as seven). Because the fields in UWHVF were a median of 1.3 years apart, we also give this time in years.

## Statistical analysis

Proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. We compared each detector with D1 on the same eyes using the exact McNemar test and corrected p-values for the nine comparisons within each number of tests with the Holm method. A detector was considered valid if the upper limit of its false-alarm confidence interval on true no-change data did not exceed 10% and its point estimate did not exceed 5% by more than sampling error. Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells and by their absolute difference. Stochastic detectors were run with 5 seeds; we report the seed mean and the largest seed standard deviation. Analyses used Python 3.13 with NumPy, SciPy, scikit-learn, LightGBM and PyTorch; the full run took 24 minutes on four central processing unit cores. The permutation p-values included the observed order, so they are never zero [31].

## Use of software assistance

The analysis code and a first draft of the text were prepared with the help of an AI coding and writing assistant (Claude Code, Anthropic). All numbers in this article are generated by the code from the result files; the authors checked the code, the results and the text and take full responsibility for them. [AUTHORS TO CONFIRM AND EDIT THIS STATEMENT]

## Ethics

This study used only publicly available, de-identified data sets released by their custodians under open licences (UWHVF: BSD-3; GRAPE: CC0; Artes data: distributed with the visualFields R package). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

# Results

## Study data

Table 1 summarises the three data sets. The UWHVF test set contained 869 eyes of 457 patients with at least three fields; 132 had at least eight fields, of which 26 were reference progressors, 26 reference stable and 80 indeterminate. The 26 + 26 reference eyes came from 41 patients, had a median baseline mean deviation of -4.4 dB (interquartile range [IQR] -6.0 to -3.2) and were followed for a median of 12.9 years. Their first six fields were a median of 1.3 years apart (IQR 1.0–1.6), so six fields took a median of 6.5 years. The true no-change arm gave 300, 270, 240 and 210 windows of three to six consecutive fields. In GRAPE, 27 of 263 eyes (10%) carried the MD progression label.

|  | UWHVF (Seattle, USA) | Artes retest (Halifax, Canada) | GRAPE (Hangzhou, China) |
|---|---|---|---|
| Role | Development; future-reference test set | True no-change (false alarms) | External clinic |
| Perimeter / pattern | Humphrey 24-2 | Humphrey 24-2 | Octopus 900 G1, 59 analysable points |
| Patients / eyes / fields | 3,871 / 7,428 / 28,943 | 30 / 30 / 360 | 144 / 263 / 1,115 |
| Analysis sets | Train 2,643 eyes; validation 940; test 869 (≥3 fields) | Windows of 3/4/5/6 tests: 300/270/240/210 | 263 eyes (≥3 fields); 163 with ≥4 |
| Follow-up | Reference eyes: median 11 fields over 12.9 years; interval 1.3 years | 12 weekly fields over median 84 days | Median 4 fields over 2.3 years |
| Age, years | Reference eyes: median 59 (IQR 50–64) | Not used | Median 41 (IQR 28–53) |
| Progression label | Future reference (≥8 fields): 26 progressors, 26 stable, 80 indeterminate | None (no change by design) | Rule-based MD label: 27 progressing (10%); PLR2 40; PLR3 14 |
| Licence | BSD-3-Clause | GPL-3 (visualFields R package) | CC0 |

**Table 1.** Data sets. IQR, interquartile range; MD, mean deviation; PLR2/PLR3, pointwise linear regression criteria with at least two or three progressing locations.

## False alarms on true no-change data (RQ1 and RQ4)

Table 2 and Fig. 2 show sensitivity against the future reference together with the false-alarm rate on true no-change series. The trend test of mean sensitivity (D1) kept its false-alarm rate near the nominal level at every number of fields (4.4%, 3.8%, 4.7% and 5.1% for three to six fields). The pooled-shuffle conformal test (D5) behaved almost identically to D1.

Three detectors had clearly inflated false-alarm rates with three fields: the pooled-detrended conformal test (D6, 22.4%, 95% CI 19.3–25.7), the tabular machine-learning model (D8, 27.7%, 22.7–32.9) and the sequence model (D9, 12.7%, 6.2–20.0). The machine-learning models were thresholded at 95% specificity on reference-stable validation eyes. On true no-change data, their false-alarm rate was significantly above 5% in 4 of 8 combinations, and it changed erratically with the number of fields (D8: 27.7%, 9.4%, 18.8% and 3.6%). The number of valid detectors was 7, 9, 8 and 8 of ten for three, four, five and six fields. Expressed per 1,000 stable eyes reviewed with three fields, D1 would raise about 44 false progression flags, D6 about 224 and D8 about 277.

Specificity against reference-stable eyes did not reveal these false alarms. With three fields, it was 96% for D1, 96% for D6 and 95% for D8 (Supplementary Table S1).

Two detectors could not flag any eye with three fields for structural reasons. PoPLR (D4) has only six possible orders of three fields, so its smallest p-value is 1/6, and event analysis (D7) needs two follow-up fields after a two-field baseline. The self-supervised order network (D10) also flagged no eye with three fields.

| Detector | 3 tests | 4 tests | 5 tests | 6 tests |
|---|---|---|---|---|
| D1 OLS-MD | 19 / 4.4 | 31 / 3.8 | 42 / 4.7 | 58 / 5.1 |
| D2 MD rate | 38 / 2.6 | 23 / 0.6 | 23 / 0.8 | 23 / 1.0 |
| D3 PLR-3 | 4 / 1.4 | 15 / 0.2 | 23 / 0.5 | 23 / 0.3 |
| D4 PoPLR | 0 / 0.0 | 4 / 3.3 | 38 / 3.9 | 50 / 5.0 |
| D5 Pooled-shuffle conformal | 19 / 4.0 | 31 / 3.6 | 42 / 4.3 | 57 / 5.0 |
| D6 Pooled-detrended conformal | 57 / 22.4 † | 25 / 5.1 | 32 / 6.2 | 54 / 7.6 † |
| D7 Event analysis | 0 / 0.0 | 23 / 1.1 | 50 / 1.2 | 58 / 1.9 |
| D8 ML tabular (LightGBM) | 26 / 27.7 † | 42 / 9.4 † | 56 / 18.8 † | 71 / 3.6 |
| D9 ML sequence (GRU) | 12 / 12.7 † | 12 / 2.0 | 41 / 7.5 † | 38 / 5.9 † |
| D10 Self-supervised order net | 0 / 0.0 | 20 / 3.8 | 44 / 5.1 | 55 / 5.7 |

**Table 2.** Sensitivity against the future-confirmed reference (%) / false-alarm rate on true no-change series (%), by number of fields available. † False-alarm rate not valid (95% CI upper limit above 10% or lower limit above 5%). Reference: 26 progressing and 26 stable eyes; true no-change: 210–300 windows (three to six fields) from 30 patients, each with ten time-scale draws. Confidence intervals are given in Supplementary Table S1.

## Sensitivity against the future reference (RQ2)

No detector with a valid false-alarm rate flagged significantly more reference progressors than D1 at any number of fields (Supplementary Table S2), so the pre-specified hypothesis H2 was not falsified. The only significant gain in sensitivity was that of D6 with three fields (38 percentage points, 95% CI 19 to 58; Holm-adjusted p = 0.02), and this detector's false-alarm rate was 22.4%.

Several valid detectors had point estimates above D1, but the confidence intervals were wide with 26 progressors. With three fields, the MD rate rule (D2) flagged 38% (20–57) versus 19% (7–33) for D1, a difference of 19 percentage points (0 to 42; adjusted p = 0.72). With five fields, event analysis (D7) flagged 50% versus 42% (8 points, -12 to 27; adjusted p = 1.00). With six fields, D8 flagged 71% with a valid false-alarm rate of 3.6%, versus 58% for D1 (12 points, -8 to 31; adjusted p = 1.00). In total, 2 valid detector–field-number combinations had a point gain of 10 points or more, none of them significant after correction.

Among reference progressors, D1 flagged 69% by the sixth field, with a median of 5 fields to the first flag. D6 and D8 reached a first flag earlier (median 3 and 4 fields; 77% and 78% flagged by six fields), but at the false-alarm cost shown above. With fields 1.3 years apart, as in this clinic, one field less corresponds to roughly 1.3 years earlier.

With the secondary reference based on PoPLR over the whole series, sensitivity was lower for all detectors but the ranking was similar (for example, three fields: D1 10%, D6 46%, D8 24%; six fields: D1 38%, D8 42%; Supplementary Table S1). Across seeds, the largest standard deviation was 13.2 points for sensitivity (ML sequence (GRU), 6 fields) and 5.1 points for the false-alarm rate; all reported values are seed means.

## Shuffle audit (RQ3)

Across the 40 detector–field-number combinations, the false-alarm rate estimated by shuffling the order of each eye's fields agreed with the true no-change false-alarm rate (Spearman ρ = 0.65, p < 0.001; median absolute difference 1.0 points; 80% within 3 points; largest difference 10.4 points; Fig. 3). Hypothesis H3 was therefore partly met: most cells agreed closely, but the correlation was below the pre-specified 0.7. The audit identified every detector with a grossly inflated false-alarm rate (D6 three fields: 22.5%; D8 three fields: 17.3%; D8 five fields: 16.1%). It overestimated the false-alarm rate of rules without a p-value, such as the MD rate rule (D2 three fields: audit 11.7% versus true 2.6%) and event analysis (D7 six fields: 11.7% versus 1.9%).

## External data set (RQ5)

In GRAPE (Table 3, Fig. 4), D1 had a sensitivity of 44% (26–65) and a specificity of 95% (92–98) with three fields. D8, transferred unchanged from UWHVF, flagged more labelled progressors (66%) but its specificity fell to 61% (55–67): it flagged 33 percentage points more non-progressing eyes than D1 (95% CI 28 to 39; adjusted p < 0.001). The MD rate rule (D2) showed the same pattern (sensitivity 59%, specificity 79%). PoPLR (D4) and event analysis (D7) could not flag with three fields; with four fields their sensitivities were 22% and 17%. D5, calibrated on GRAPE itself, matched D1 (41% and 95%).

| Detector | Sensitivity, 3 tests | Specificity, 3 tests | Sensitivity, 4 tests | Specificity, 4 tests |
|---|---|---|---|---|
| D1 OLS-MD | 44 (26–65) | 95 (92–98) | 33 (12–55) | 96 (92–99) |
| D2 MD rate | 59 (41–77) | 79 (73–84) | 56 (35–76) | 86 (79–92) |
| D3 PLR-3 | 4 (0–12) | 96 (93–98) | 11 (0–25) | 98 (95–100) |
| D4 PoPLR | 0 (0–0) | 100 (100–100) | 22 (6–41) | 95 (91–98) |
| D5 Pooled-shuffle conformal | 41 (24–60) | 95 (92–98) | 33 (12–55) | 94 (91–98) |
| D7 Event analysis | 0 (0–0) | 100 (100–100) | 17 (0–33) | 96 (92–99) |
| D8 ML tabular (LightGBM) | 66 (51–80) | 61 (55–67) | 49 (32–66) | 82 (74–88) |

**Table 3.** External data set (GRAPE): sensitivity and specificity (%, 95% CI) against the MD progression label supplied with the data set, using the first three or four fields. D6, D9 and D10 require the 24-2 pattern and were not applied.

# Discussion

We compared ten detectors of glaucomatous visual field progression on the question that matters for a treatment decision: how early can progression be flagged without raising false alarms? Three findings stand out. First, the detectors that flagged the most progressors from three fields did so mainly by flagging more of everything. On series in which nothing changed, the pooled-detrended conformal test flagged 22.4% and a gradient-boosted tree model 27.7% of windows, against a nominal 5%. Second, the usual way to measure specificity, in eyes labelled stable by the full series, missed this. Third, no detector with a valid false-alarm rate beat the plain trend test of mean sensitivity significantly at any number of fields, in one clinic or in a second clinic using a different perimeter.

These results fit what is known about the information in a short series. A trend line through three or four noisy fields has very few degrees of freedom, and the noise of perimetry rises as sensitivity falls [4]. Methods that pool information across patients or locations can add power [12–14], but only if the pooled reference matches the eye being tested. Our pooled-detrended test borrowed its null distribution from other patients' detrended and shuffled series [28, 29]. With three fields, detrending leaves one residual degree of freedom, and the borrowed distribution was too narrow; the shuffle audit and the true no-change arm both exposed this. The within-eye permutation test PoPLR avoids this problem by design [7], but with three fields it has only six orders and cannot reach p < 0.05. This floor is a property of the method, not a fault of its implementation.

The machine-learning results deserve attention because supervised models are increasingly proposed for this task [15–20]. When such a model is thresholded at a target specificity in reference-stable eyes, as D8 and D9 were, the threshold inherits the selection of those eyes. Eyes that remain stable over eight or more fields tend to be eyes whose early fields also looked stable. Specificity measured in them is therefore optimistic, and the threshold does not control false alarms in a new eye with short follow-up. In our data the true false-alarm rate of the tabular model ranged from 3.6% to 27.7% depending on the number of fields. Labels also differ between studies, and models trained on one label may not transfer [23]; in GRAPE, the transferred model lost 33 percentage points of specificity relative to the trend test. This does not mean that machine learning cannot help, but it does mean that a model's flag rate on true no-change data should be reported before any claim of earlier detection.

Artes and colleagues previously used the same retest series to estimate the specificity of the Guided Progression Analysis [9]. We extend this approach to ten detectors and four series lengths, and add a check that any clinic can run without retest data. The shuffle audit agreed with the true false-alarm rate within 3 points in 80% of combinations and flagged every detector with a grossly inflated rate. It was conservative for rules that use a size threshold without a p-value, probably because shuffling a truly progressing series keeps its spread of values and creates steep slopes in both directions. A clinic that adopts a new detector can therefore shuffle its own records, re-run the detector and compare the flag rate with the nominal level; a large excess is a warning sign.

For clinical practice, the main limit to earlier detection is the number and spacing of fields, not the detector. In UWHVF, fields were a median of 1.3 years apart, so the trend test needed a median of 5 fields, several years, to flag a reference progressor. This agrees with earlier work showing that routine testing frequencies delay the identification of progression [32–34]. Testing more often early in follow-up [5], clustering tests [35], personalised schedules [21, 36] or smoothing [37] address the amount of information directly. Our results suggest that these strategies, rather than a more complex detector applied to the same sparse fields, are where earlier detection is likely to come from. Until a detector shows a valid false-alarm rate on true no-change data, a flag from it should not by itself trigger escalation of treatment.

This study has several limitations. The future reference set was small (26 progressing and 26 stable eyes), so confidence intervals for sensitivity are wide and moderate gains (around 10 points) cannot be excluded. The primary reference is based on the slope of mean deviation over the whole series, which may favour detectors based on mean sensitivity; the secondary PoPLR-based reference gave a similar ranking. The true no-change arm included only 30 patients from one centre, retested weekly; we assigned clinical test intervals from UWHVF to these series (amendment A1), which keeps them a valid null but does not capture fluctuation over months or years. UWHVF has no diagnoses or reliability indices, so the cohort may include eyes without glaucoma. GRAPE used a different perimeter, its labels are rule-based criteria computed on short series that overlap heavily with the fields given to the detectors, and its patients were younger (median age 41 versus 59 years in the UWHVF reference eyes); external results should therefore be read as a test of transfer and of false alarms, not as an independent accuracy estimate. Finally, we developed and abandoned several method ideas before writing the analysis plan, and the Artes data were used once during development to check false alarms; we report these steps in the Supplementary Material. The final test data were analysed once, as planned.

# Conclusion

In this benchmark, the largest apparent gains in early detection of glaucomatous visual field progression came with false-alarm rates far above the nominal level, and standard specificity estimates did not reveal them. No valid detector beat a simple trend test of mean sensitivity. New detectors should be reported with their false-alarm rate on true no-change data, and clinics can screen a detector with a shuffle audit of their own records before relying on its flags to escalate treatment.

# Declarations

## Acknowledgements

We thank the University of Washington team for releasing UWHVF, Paul Artes and colleagues for making the retest data available through the visualFields R package, and the GRAPE investigators for releasing their data set. [AUTHORS: ADD ANY OTHER ACKNOWLEDGEMENTS]

## Funding

No funding or sponsorship was received for this study or publication of this article.

## Medical Writing, Editorial, and Other Assistance

An AI coding and writing assistant (Claude Code, Anthropic) was used to write analysis code and to draft the text, under the authors' direction; see Methods. [AUTHORS TO CONFIRM]

## Author Contributions

[AUTHORS TO COMPLETE using the CRediT roles: conceptualisation, methodology, software, formal analysis, writing – original draft, writing – review and editing.]

## Conflict of Interest

All authors declare that they have no competing interests. [AUTHORS: the journal asks for one statement per author by name, e.g. "[Name] declares that they have no competing interests."]

## Ethical Approval

This study used only publicly available, de-identified data released by their custodians (UWHVF, BSD-3-Clause licence; GRAPE, CC0; Artes retest data, distributed with the visualFields R package under GPL-3). The original studies obtained ethical approval. No new data were collected, and this article does not contain any new studies with human participants or animals performed by any of the authors.

## Data Availability

The data sets analysed during the current study are available in public repositories: UWHVF at https://github.com/uw-biomedical-ml/uwhvf; the Artes retest data in the visualFields R package version 1.0.7 at https://cran.r-project.org/package=visualFields; GRAPE at figshare (https://doi.org/10.6084/m9.figshare.c.6406319.v1). Result files generated during the study (per-eye flags for every detector, seed and number of fields) are available from the corresponding author on reasonable request.

## Code Availability

The code, the pre-specified analysis plan with its dated amendments, and the scripts that generate every number, table and figure in this article are available from the corresponding author on request.

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

26. Marin-Franch I, Swanson WH. The visualFields package: A tool for analysis and visualization of visual fields. Journal of Vision. 2013;13(4):10-10. https://doi.org/10.1167/13.4.10

27. Huang X, Kong X, Shen Z, Ouyang J, Li Y, Jin K, et al. GRAPE: A multi-modal dataset of longitudinal follow-up visual field and fundus images for glaucoma management. Sci Data. 2023;10(1). https://doi.org/10.1038/s41597-023-02424-4

28. Angelopoulos AN, Bates S. Conformal Prediction: A Gentle Introduction. Foundations and Trends® in Machine Learning. 2023;16(4):494-591. https://doi.org/10.1561/2200000101

29. Freedman D, Lane D. A Nonstochastic Interpretation of Reported Significance Levels. Journal of Business & Economic Statistics. 1983;1(4):292-298. https://doi.org/10.1080/07350015.1983.10509354

30. Gagnon-Bartsch J, Shem-Tov Y. The classification permutation test: A flexible approach to testing for covariate imbalance in observational studies. Ann. Appl. Stat.. 2019;13(3):1464-1483. https://doi.org/10.1214/19-aoas1241

31. Phipson B, Smyth GK. Permutation P-values Should Never Be Zero: Calculating Exact P-values When Permutations Are Randomly Drawn. Statistical Applications in Genetics and Molecular Biology. 2010;9(1). https://doi.org/10.2202/1544-6115.1585

32. Wu Z, Saunders LJ, Daga FB, Diniz-Filho A, Medeiros FA. Frequency of Testing to Detect Visual Field Progression Derived Using a Longitudinal Cohort of Glaucoma Patients. Ophthalmology. 2017;124(6):786-792. https://doi.org/10.1016/j.ophtha.2017.01.027

33. Crabb DP, Garway-Heath DF. Intervals between Visual Field Tests When Monitoring the Glaucomatous Patient: Wait-and-See Approach. Invest. Ophthalmol. Vis. Sci.. 2012;53(6):2770. https://doi.org/10.1167/iovs.12-9476

34. Stagg BC, Brintz BJ, Stein JD, Hess R, Kawamoto K, Jammal AA, et al. Time to Identify Glaucoma Progression Given Typical Visual Field Testing Frequencies in a US Nationwide Insured Population. Ophthalmology Glaucoma. 2026;9(3):250-256. https://doi.org/10.1016/j.ogla.2025.11.004

35. Phu J, Kalloniatis M. The Frontloading Fields Study (FFS): Detecting Changes in Mean Deviation in Glaucoma Using Multiple Visual Field Tests Per Clinical Visit. Trans. Vis. Sci. Tech.. 2021;10(13):21. https://doi.org/10.1167/tvst.10.13.21

36. Schell GJ, Lavieri MS, Helm JE, Liu X, Musch DC, Van Oyen MP, et al. Using Filtered Forecasting Techniques to Determine Personalized Monitoring Schedules for Patients with Open-Angle Glaucoma. Ophthalmology. 2014;121(8):1539-1546. https://doi.org/10.1016/j.ophtha.2014.02.021

37. Mohammadzadeh V, Li L, Fei Z, Davis T, Morales E, Wu K, et al. Efficacy of Smoothing Algorithms to Enhance Detection of Visual Field Progression in Glaucoma. Ophthalmology Science. 2024;4(2):100423. https://doi.org/10.1016/j.xops.2023.100423

# Supplementary Material

Supplementary Table S1: all metrics with 95% confidence intervals (sensitivity, specificity, true no-change and shuffle-audit false-alarm rates, secondary-reference sensitivity, GRAPE results) for every detector and number of fields. Supplementary Table S2: paired comparisons with D1 (difference, bootstrap 95% CI, exact McNemar p, Holm-adjusted p). Supplementary Table S3: fields to first flag among reference progressors, by detector (seed means). Supplementary Note S1: development history, including abandoned method ideas.
