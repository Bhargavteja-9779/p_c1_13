# False Progression Flags and Treatment Escalation in Glaucoma: Benchmarking Visual Field Detectors and Calibrating Them on a Clinic's Own Data

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, AFFILIATIONS, ADDRESSES AND ORCID iDs — TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — TO BE COMPLETED]

**Prior presentation:** None. [AUTHORS TO CONFIRM]

## Abstract

**Introduction:** Treatment of glaucoma is escalated when visual fields show progression. New detectors claim earlier detection, but their false alarms are rarely measured on data without change, and clinics lack a simple way to set a detector's threshold safely.

**Methods:** In this retrospective benchmark of public data, ten detectors (trend, event, permutation, conformal, machine learning) saw the first 3–6 fields of each series (three fields spanned a median of 2.2 years in the US clinic). We measured sensitivity against a future-confirmed reference (26 progressing, 26 stable held-out eyes), false alarms on true no-change series (30 patients retested about weekly) and transfer to a Chinese clinic (263 eyes, different perimeter). In an exploratory amendment, thresholds were reset to a 5% flag rate on shuffled series of the clinic's own records.

**Results:** With three fields, gradient-boosted trees thresholded at 95% specificity in reference-stable eyes flagged 26% of progressors versus 19% for the trend test, but raised false alarms in 27.7% of no-change series (trend test 4.4%); specificity in reference-stable eyes (95%) did not reveal this. No detector with an acceptable false-alarm rate was significantly more sensitive than the trend test, although gains up to about 42 points could not be excluded. Shuffle calibration brought every clear excess down (gradient-boosted trees: 27.7% to 6.6%; external specificity 61% to 95%), but at a cost: no calibrated detector was more sensitive than the trend test, and external sensitivity fell to 10% (trend test 44%).

**Conclusion:** The largest apparent early-detection gains came with excess false alarms, and controlling false alarms removed them. Detectors should be reported with false-alarm rates on true no-change data and checked on local data before their flags guide escalation. With few fields, every method missed most progressing eyes.

**Keywords:** Calibration; False alarms; Glaucoma; Machine learning; Perimetry; Treatment escalation; Visual field

## Plain Language Summary

Glaucoma damages the nerve at the back of the eye and slowly narrows side vision. Doctors check this with a visual field test, in which the patient presses a button when they see small lights. If results get worse, the doctor may step up treatment with more eye drops, laser or surgery. Results vary from visit to visit, so several tests are needed to be sure that vision is really getting worse. New computer methods claim to spot worsening sooner. We tested ten methods on public data from the USA, Canada and China, including patients tested about once a week for about three months, whose eyes could not really have changed. One machine-learning method that seemed to spot worsening sooner raised false alarms in more than one in four of these unchanged test series, and the usual checks did not show this. We then tried a simple fix: a clinic jumbles the order of its own patients' past tests, which removes any real worsening, and sets the method's alarm level so that it rarely fires on the jumbled tests. This removed most extra false alarms, also in a clinic using a different machine, but the apparent advantage of the new methods disappeared. With only three tests, which took more than two years in routine care, every method missed most eyes that were really getting worse, so "no change" after a few tests is not reassurance.

## Key Summary Points

**Why carry out this study?**

- Glaucoma treatment is escalated when visual fields show progression, and new detectors claim to find it earlier, but they are usually judged by how many eyes they flag rather than by how many of those flags are false.

- We asked how often ten detectors raise false progression flags on true no-change data with three to six fields, whether any flags more truly progressing eyes than a simple trend test while keeping false alarms near 5%, and whether thresholds set on a clinic's own shuffled fields control false alarms.

**What was learned from the study?**

- With three fields, a machine-learning detector flagged more progressing eyes than the trend test (26% versus 19%) but raised false alarms in 27.7% of series without change, which specificity in reference-stable eyes did not reveal.

- Shuffle calibration reduced false alarms close to 5%, also on another perimeter, but no calibrated detector was more sensitive than the trend test, and external sensitivity fell.

- With few fields every method missed most progressing eyes; new detectors should be reported with true no-change false-alarm rates and checked on local data before their flags guide escalation.

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [1]. Treatment lowers intraocular pressure and slows visual loss [2, 3]. The key clinical decision is when to escalate treatment, and clinicians make it mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [4]. Expert guidance suggests six tests in the first two years [5], but routine care rarely reaches this frequency, and delays in follow-up are a documented cause of avoidable sight loss [6]. Many methods therefore aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [7, 8]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [9–11]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [7]. Bayesian and spatial models share information across locations or patients [12–14], and machine-learning models have been trained to classify or forecast progression [15–20], recently with conformal error control of forecasts [21].

A new detector that flags more progressing eyes may simply flag more eyes. False alarms matter clinically, because a false progression flag can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs. Yet specificity is often estimated in eyes labelled stable by another criterion, and only a few studies have measured false alarms on true no-change data, in which the same patients were tested repeatedly over a few weeks [9]. Labels for "progression" also differ between studies, and models trained on one label may not transfer [22]. Finally, a clinic that wants to use a detector has no simple way to check or set its threshold on its own patients.

We therefore asked three practical questions about the decision to escalate treatment. First, how often do ten detectors, from a simple trend test to permutation, conformal, event-based and machine-learning methods, raise false progression flags on true no-change series when given three to six fields? Second, does any of them flag more eyes that later progress than the simple trend test while keeping false alarms near the nominal 5%? Our pre-specified hypothesis was that none would do so by 10 percentage points or more. Third, can a clinic make any detector safe to use by setting its threshold on shuffled copies of its own past fields ("shuffle calibration")?

# Methods

## Study design and reporting

This was a retrospective benchmark study of public, de-identified data, reported following the TRIPOD+AI guidance where it applies to detection models [23]. The analysis plan (detectors, thresholds, reference standards, statistical tests) was written and time-stamped in the project's version-control history before the final test data were analysed; it was not registered externally. Amendments A1 and A2 were made before any final result was seen. Amendment A3 (shuffle calibration, confirmation and an enlarged reference) was prompted by an internal review of the first results; it was written and time-stamped before any A3 analysis was run, but the choice of detectors to calibrate depended on the first results, so A3 is exploratory. Ideas developed and abandoned before the protocol are listed in Supplementary Note S1.

## Data sources

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains 28,943 24-2 tests from 7,428 eyes of 3,871 patients seen in routine care [24]. It includes sensitivities, age and laterality, but no diagnosis, treatment or reliability indices. Patients, not tests, were split into training (60%), validation (20%) and test (20%) sets by a fixed hash of the patient identifier; the test set was used once for the main analysis and once for amendment A3.

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 Humphrey 24-2 fields at approximately weekly intervals (median span 84 days, IQR 77–93; one series spanned 524 days) [9]. Glaucoma is not expected to change measurably over this period, so we treated any "progression" flag as a false alarm. These series contain short-term test–retest variability but not fluctuation over months or years. The data are distributed with the visualFields R package (version 1.0.7) [25].

*GRAPE (external data set).* GRAPE contains 1,115 visual-field records from 263 eyes of 144 patients with glaucoma followed in Hangzhou, China [26], measured with the G1 pattern of the Octopus 900 perimeter (Haag-Streit, Köniz, Switzerland). We used locations with a valid value at every visit of an eye (median 59; 86 eyes had fewer, minimum 10). The data set authors labelled each eye with rule-based criteria applied to the whole follow-up: a negative slope of mean deviation with p < 0.05 (MD label, our primary label) and at least two or three significantly progressing locations (PLR2, PLR3) [26]. These are not clinicians' judgements, and with a median of 4 visits per eye (100 eyes had exactly three) the MD label is close to the trend test itself.

## Reference standard (UWHVF)

For eyes with at least eight fields, an eye was a progressor if the slope of mean total deviation over all its fields was worse than −0.3 dB per year with one-sided p < 0.01, and stable if the one-sided p was above 0.5; other eyes were excluded. Because this reference uses a mean-deviation slope over a series that includes the fields the detectors see, it may favour the trend test. We therefore also report a secondary reference based on PoPLR over the whole series (2,000 permutations [27]) and, post hoc, a reference computed only from fields after the first k.

## Detectors

Each detector saw only the first k fields (k = 3, 4, 5 or 6) with the two blind-spot locations removed, and returned "progression" or "no progression" at a nominal false-alarm level of 5% where a level applies.

- **D1 trend test (OLS-MD):** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD-rate rule:** slope of mean sensitivity of −1 dB per year or worse (a "fast progression" rule without a p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [7], using all orders of the k fields.
- **D5 pooled conformal test:** the D1 statistic compared with the same statistic on shuffled series of training patients matched by number of fields and mean sensitivity (a conformal p-value [28]).
- **D6 detrended conformal test:** as D5, with the worst of four regional trends and a reference built from shuffled residuals after removing each series' trend, an idea borrowed from residual permutation [29]. This was the most sensitive variant during development, and its false-alarm rate on the Artes data had already been measured then (Supplementary Note S1), so its Artes result is not an independent test.
- **D7 event analysis (GPA-inspired):** a location is deteriorated if its loss from the baseline (mean of fields 1–2) is beyond the 5th percentile of change between training test pairs less than six months apart with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-ups. Unlike the commercial Guided Progression Analysis [11], it uses total rather than pattern-deviation sensitivity and routine-care rather than dedicated retest limits.
- **D8 gradient-boosted trees:** gradient-boosted trees on 14 summary features of the first k fields (level, slope and range of mean sensitivity, pointwise slope summaries), trained to predict the reference label of training eyes, with the configuration chosen by validation area under the curve (12 configurations) and the threshold set at 95% specificity in validation reference-stable eyes.
- **D9 recurrent network:** a gated recurrent unit network on the raw fields and test intervals, with the same labels, threshold rule and tuning budget as D8.
- **D10 order network:** a network trained without labels to recognise the true order of an eye's fields, used as a PoPLR-type within-eye permutation statistic [30].

## Evaluation

*E1 future reference:* sensitivity and specificity in UWHVF test eyes with at least eight fields, using only the first k fields. *E2 true no-change:* the share of all Artes windows of k consecutive fields that were flagged; because rate-based rules depend on the time scale, each window was given the test dates of a randomly chosen UWHVF test eye (ten draws per window; amendment A1). *E3 shuffle audit:* the flag rate after randomly re-ordering the first k fields of each UWHVF test eye (ten orders). *E4 external:* sensitivity and specificity in GRAPE against the MD label with three or four fields; D5 and D7 were recalibrated on GRAPE by five-fold patient-level cross-fitting, D8 was transferred unchanged, and the 24-2-specific detectors D6, D9 and D10 were not applied (amendment A2).

*Amendment A3 (exploratory).* (a) Shuffle calibration: for the detectors whose nominal threshold was invalid or depended on the time scale (D2, D6, D8, D9), we replaced the threshold by the 95th percentile of the detector's own score on shuffled series of the validation eyes (first k fields, ten random orders per eye); models were otherwise unchanged. Shuffling removes any trend while keeping each eye's level, spread and test dates, so this threshold targets a 5% flag rate in eyes like the clinic's own that are not changing. In GRAPE, D2 and D8 were calibrated on shuffled GRAPE series by five-fold patient-level cross-fitting. (b) Confirmation: a flag with k fields counted only if the detector had also flagged with k − 1 fields. (c) Enlarged reference: because D1–D4 use no training data, we applied them to all UWHVF eyes with at least eight fields and a reference label, across all three splits. The stated hypotheses were that no calibrated detector would have a false-alarm rate clearly above 5% (lower CI limit above 5%), that none would be at least 10 points more sensitive than D1, that confirmation would bring D6 and D8 to at most 5%, and that D2 would be more sensitive than D1 with three fields in the enlarged reference.

*Real-world measures.* We report false progression flags per 1,000 stable eyes at one review and, post hoc, the share of no-change series flagged at least once when reviewed at three, four, five and six fields; the number of fields to the first flag among reference progressors (counted as seven if not flagged by six); and, post hoc, the share of flags that are true progression (positive predictive value) at 10% prevalence and at the GRAPE prevalence.

## Statistical analysis

Proportions are reported with 95% confidence intervals (CIs) from 2,000 bootstrap resamples of patients; when all or none of the eyes were flagged, we report the exact Clopper–Pearson interval. Each detector was compared with D1 on the same eyes with the exact McNemar test, with Holm correction within each number of fields and, as a sensitivity analysis, across all numbers of fields; CIs for paired differences used the same patient bootstrap. Stochastic detectors were run with 5 seeds; tables give seed means and paired tests use the majority flag across seeds. A false-alarm rate was classed as valid if its CI upper limit was at most 10% and its lower limit at most 5% (no clear excess); because this rule was made exact after the main results were available, we also report the stricter rule (upper limit at most 5%). Agreement between the shuffle audit and the true false-alarm rate was summarised by the Spearman correlation across detector–field-number combinations (bootstrap CI), their absolute differences and, post hoc, the audit's accuracy in classifying combinations as valid or invalid. Analyses used Python 3.13 with NumPy, SciPy, scikit-learn, LightGBM and PyTorch; the main run took 24 minutes and amendment A3 7 minutes on four processor cores.

## Deviations from the protocol

(1) The validity rule was made exact after the main results were available (see above). (2) Fields to first detection were followed to six, not eight, fields. (3) After the internal review we corrected the paired CIs to patient-level resampling as the protocol stated, replaced zero-width bootstrap intervals with exact intervals, added Holm correction across numbers of fields, a CI for the Spearman correlation, and the post-hoc analyses named above. (4) The GRAPE labels were first described as clinician labels; this was corrected. (5) Amendment A3 was added after the internal review, before its analyses were run (exploratory).

## Use of software assistance

The analysis code and a first draft of the text were prepared with the help of an AI coding and writing assistant (Claude Code, Anthropic). All numbers in this article are generated by the code from the result files; the authors checked the code, the results and the text and take full responsibility for them. [AUTHORS TO CONFIRM AND EDIT THIS STATEMENT]

## Ethics

This study used only publicly available, de-identified data released by their custodians under open licences (UWHVF: BSD-3-Clause; GRAPE: CC0; Artes data: Apache License 2.0 within the visualFields R package). The original studies obtained ethical approval. No new data were collected, and this article does not contain any new studies with human participants or animals performed by any of the authors.

# Results

## Study data

Table 1 summarises the data sets. Of 132 UWHVF test eyes with at least eight fields, 26 were reference progressors, 26 stable and 80 indeterminate; the reference eyes came from 41 patients, had a median baseline mean deviation of −4.4 dB (interquartile range [IQR] −6.0 to −3.2) and were followed for a median of 12.9 years, with fields a median of 1.3 years apart. Across all splits, 150 progressors and 164 stable eyes formed the enlarged reference. The no-change arm gave 300 to 210 windows of three to six fields, and 27 of 263 GRAPE eyes (10%) carried the MD label.

|  | UWHVF (Seattle, USA) | Artes retest (Halifax, Canada) | GRAPE (Hangzhou, China) |
|---|---|---|---|
| Role | Development; future-reference test set | True no-change (false alarms) | External clinic |
| Perimeter / pattern | Humphrey 24-2 | Humphrey 24-2 | Octopus 900 G1, 59 analysable points |
| Patients / eyes / fields | 3,871 / 7,428 / 28,943 | 30 / 30 / 360 | 144 / 263 / 1,115 |
| Analysis sets | Train 2,643 eyes; validation 940; test 869 (≥3 fields) | Windows of 3/4/5/6 tests: 300/270/240/210 | 263 eyes (≥3 fields); 163 with ≥4 |
| Follow-up | Reference eyes: median 11 fields over 12.9 years; interval 1.3 years | 12 weekly fields over median 84 days | Median 4 fields over 2.3 years |
| Age, years | Reference eyes: median 59 (IQR 50–64) | Not used | Median 41 (IQR 28–53) |
| Progression label | Future reference (≥8 fields): 26 progressors, 26 stable, 80 indeterminate | None (no change by design) | Rule-based MD label: 27 progressing (10%); PLR2 40; PLR3 14 |
| Licence | BSD-3-Clause | Apache-2.0 (visualFields R package) | CC0 |

**Table 1.** Data sets. IQR, interquartile range; MD, mean deviation; PLR2/PLR3, pointwise linear regression criteria with at least two or three progressing locations.

## False alarms and sensitivity with nominal thresholds

The trend test kept false alarms close to 5% at every number of fields (4.4%, 3.8%, 4.7% and 5.1% with three to six fields; Table 2, Fig. 2), and the pooled conformal test behaved almost identically. False-alarm rates were invalid in 8 of 40 detector–field-number combinations (Table 2). The gradient-boosted trees had 27.7% false alarms with three fields (95% CI 22.7–32.9), and the two machine-learning detectors were invalid in 6 of 8 combinations, as hypothesised. The detrended conformal test had 22.4% (19.3–25.7), as already seen during development. Specificity in reference-stable eyes did not reveal these false alarms: with three fields it was 96% for the trend test, 95% for the gradient-boosted trees and 96% for the detrended conformal test. Under the strictest rule (upper CI limit at most 5%), even the trend test never qualified (upper limits 6.2–8.1%), because 30 patients cannot show a rate near 5% to be below 5%.

No detector with a valid false-alarm rate was significantly more sensitive than the trend test at any number of fields, so our hypothesis was not falsified. This is not evidence of equivalence: with 26 progressors, gains up to 42 points were within the CIs. With three fields, the MD-rate rule flagged 38% versus 19% at a valid false-alarm rate of 2.6% (19 points, 95% CI −3 to 42; adjusted p = 0.72). With six fields, the gradient-boosted trees flagged 71% versus 58% (12 points, −8 to 30; adjusted p = 1.00). The only nominally significant gain was the detrended conformal test with three fields (38 points; adjusted p = 0.018 within three fields and = 0.070 across all numbers of fields), whose false-alarm rate was invalid. Secondary and later-field references gave lower sensitivities and a similar pattern (Supplementary Tables S1, S4, S5).

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

**Table 2.** Sensitivity against the future-confirmed reference (%) / false-alarm rate on true no-change series (%), nominal thresholds. † Not valid (95% CI upper limit above 10% or lower limit above 5%). Reference: 26 progressing and 26 stable eyes; no-change: 210–300 windows from 30 patients, ten time-scale draws each. PoPLR and the order network cannot flag with three fields (six possible orders, smallest p-value 1/6); event analysis needs four. CIs in Supplementary Table S1.

## What the flags mean for escalation decisions

Table 3 translates the results into clinical terms. With three fields, among 1,000 stable eyes reviewed once, the trend test would raise about 44 false progression flags and the gradient-boosted trees about 277; at 10% prevalence, 33% of trend-test flags and 9% of gradient-boosted-tree flags would be true progression (MD-rate rule 62%). Reviewed at three, four, five and six fields in turn, 13% of no-change series received at least one false trend-test flag, against 44% for the gradient-boosted trees. The trend test flagged 69% of progressors at one or more of fields 3–6 (median 5 fields to the first flag, several years at this clinic's spacing).

| Detector (threshold) | Sensitivity, 3 fields (%) | False flags per 1,000 stable eyes, 3 fields | True flags among all flags at 10% prevalence, 3 fields (%) | Progressors flagged at any of fields 3–6 (%) | No-change series falsely flagged at any of fields 3–6 (%) |
|---|---|---|---|---|---|
| D1 trend test (OLS-MD), nominal | 19 | 44 | 33 | 69 | 13 |
| D2 MD-rate rule, nominal | 38 | 26 | 62 | 46 | 4 |
| D3 PLR-3, nominal | 4 | 14 | 23 | 38 | 3 |
| D4 PoPLR, nominal | 0 | 0 | – | 54 | 9 |
| D5 pooled conformal test, nominal | 19 | 40 | 35 | 68 | 12 |
| D6 detrended conformal test, nominal | 57 | 224 | 22 | 77 | 30 |
| D7 event analysis, nominal | 0 | 0 | – | 58 | 2 |
| D8 gradient-boosted trees, nominal | 26 | 277 | 9 | 78 | 44 |
| D9 recurrent network, nominal | 12 | 127 | 10 | 59 | 21 |
| D10 order network, nominal | 0 | 0 | – | 63 | 11 |
| D2 MD-rate rule, shuffle-calibrated | 4 | 3 | 56 | – | – |
| D6 detrended conformal test, shuffle-calibrated | 15 | 47 | 26 | – | – |
| D8 gradient-boosted trees, shuffle-calibrated | 15 | 66 | 21 | – | – |
| D9 recurrent network, shuffle-calibrated | 11 | 42 | 22 | – | – |

**Table 3.** Clinical implications (UWHVF reference and true no-change arm). Share of flags that are true progression assumes 10% prevalence. Cumulative columns count a flag at any review with three, four, five or six fields. Shuffle-calibrated rows: amendment A3 (exploratory).

## Calibrating thresholds on the clinic's own shuffled fields (exploratory)

Shuffle calibration removed every clear excess of false alarms (Fig. 4; Supplementary Table S6). With three fields, the false-alarm rate fell from 27.7% to 6.6% (95% CI 4.7–8.9) for the gradient-boosted trees, from 12.7% to 4.2% for the recurrent network and from 22.4% to 4.7% for the detrended conformal test; 15 of 16 calibrated combinations were valid (exception: D6 with 6 fields, upper limit just above 10%). For the MD-rate rule, calibration was over-conservative (0.3% false alarms, 4% sensitivity), probably because shuffled clinic series contain more long-term fluctuation than the weekly retest series.

Once false alarms were controlled, no detector was more sensitive than the trend test. With three fields, the calibrated gradient-boosted trees flagged 15% of progressors (trend test 19%); with six fields, 64% at 2.2% false alarms versus 58% (+8 points, 95% CI −13 to 28; adjusted p = 1.00). In GRAPE, own-clinic calibration restored the specificity of the transferred gradient-boosted trees from 61% to 95% (95% CI 92–97), matching the trend test (95%), but their sensitivity against the MD label fell to 10% versus 44% for the trend test (33 points lower; adjusted p = 0.008). The trend test's GRAPE result is partly circular, because the MD label is itself a slope test of a short series (it flagged 8 of 9 labelled progressors among eyes with exactly three visits and 4 of 18 among eyes with more; Supplementary Table S9).

Requiring a flag to be confirmed on the next field also controlled false alarms (gradient-boosted trees 3.7%–2.0%, detrended conformal test 2.8%–2.5% with four to six fields) but cost sensitivity (confirmed trend test 35% versus 58% unconfirmed with six fields; Supplementary Table S7). In the enlarged reference (150 progressors, 164 stable eyes), the MD-rate rule flagged 9 points more progressors than the trend test with three fields (95% CI 1 to 16; adjusted p = 0.047) but also 11 points more stable eyes (adjusted p < 0.001), and PLR-3 and PoPLR were less sensitive than the trend test with three to five fields (Supplementary Table S8). A shuffle audit without recalibration identified 7 of 8 invalid combinations but gave false warnings for 7 of 32 valid ones (Spearman ρ with the true rate 0.65, below the pre-specified 0.7; Supplementary Fig. S1).

# Discussion

We compared ten detectors of glaucomatous visual field progression on a question that matters for treatment decisions: how early can progression be flagged without raising false alarms? With nominal thresholds, the detectors that gained most over the trend test with three fields also flagged many series without change, and specificity measured in reference-stable eyes did not show this. When each detector's threshold was reset on shuffled copies of the clinic's own series, the excess false alarms largely disappeared, and so did the gains in sensitivity. This supports the view that most of the apparent early-detection advantage came from a more permissive threshold rather than from more information. It does not prove equivalence: our held-out reference was small, and one valid rule (the MD-rate rule) showed a non-significant gain with nominal thresholds.

The mechanisms differ. The detrended conformal test borrowed its null distribution from other patients' detrended series; with three fields, detrending leaves one residual degree of freedom, and the borrowed distribution was probably too narrow. The machine-learning models were trained to predict future progression and thresholded in reference-stable eyes, which tend to be eyes whose early fields also looked stable; they also partly predict risk, so features such as the level of mean sensitivity raise their output in an eye that is not changing. Shuffle calibration addresses both in the same way: shuffling destroys any trend but keeps each eye's level, spread and test dates, so the threshold reflects how the detector behaves on stable eyes like the clinic's own. Within-eye permutation (PoPLR) uses the same idea for one eye [7] but cannot reach p < 0.05 with three fields; pooling shuffles across a clinic's eyes, by analogy with conformal inference [28] and the classification permutation test [30], applies to any score, including a machine-learning output. To our knowledge, based on searches of OpenAlex, PubMed, Europe PMC, Crossref and preprint servers (November 2026), this has not been used to set the thresholds of visual field progression detectors.

Calibration needs only a clinic's past fields and the ability to run the detector outside the perimeter software, with no retest series and no labels. In GRAPE it restored the specificity of a model trained on another perimeter and population. Its cost is equally clear: it does not add information, it lowered sensitivity, and it was over-conservative for a rule without a p-value. It is therefore a safety check that makes detectors comparable at a stated false-alarm rate, not a way to detect progression earlier. Confirming flags on the next field is a simpler alternative that also controls false alarms, at the cost of one more field.

For clinical practice, the main limit to earlier detection is the number and spacing of fields, not the detector. In UWHVF, three fields took a median of 2.2 years; with three fields the trend test flagged only 19% of eyes that later progressed (15% in the enlarged reference). A "no progression" result after a few fields is therefore not reassurance. This agrees with work showing that routine testing frequencies delay the identification of progression [31–33]. Testing more often early in follow-up [5], clustering tests [34], personalised schedules [35, 36] or smoothing [37] address the amount of information directly and are more likely to bring detection forward than a more complex detector applied to the same sparse fields. A flag from a detector whose false-alarm rate has not been shown to be acceptable on true no-change or locally shuffled data should not by itself trigger escalation of treatment.

This study has limitations. The held-out reference was small and limited to clear-cut eyes; the enlarged reference could be used only for training-free detectors. The primary reference uses a mean-deviation slope over a series that includes the fields the detectors see, which may favour the trend test. The no-change arm included only 30 patients retested over a few weeks, without long-term fluctuation, so real-world false-alarm rates are probably higher for all detectors. The detrended conformal test's behaviour on these data was known from development, and the calibration analyses were exploratory, added after an internal review. Our machine-learning models were not replicas of published systems [15–20]. UWHVF has no diagnoses, treatment or reliability indices, so flags could not be linked to treatment decisions or outcomes. GRAPE used a different perimeter, its labels are rule-based criteria computed on short series that overlap with the detectors' input, and its patients were younger (median age 41 versus 59 years).

# Conclusion

In this benchmark, the largest apparent gains of newer detectors in early detection of glaucomatous visual field progression came with excess false alarms, and setting thresholds on shuffled copies of a clinic's own fields removed both the excess and the gains. A simple trend test of mean sensitivity was well calibrated but slow. New detectors should be reported with false-alarm rates on true no-change data and checked on local data before their flags guide escalation of treatment.

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

This study used only publicly available, de-identified data released by their custodians (UWHVF, BSD-3-Clause licence; GRAPE, CC0; Artes retest data, distributed with the visualFields R package under the Apache License 2.0). The original studies obtained ethical approval. No new data were collected, and this article does not contain any new studies with human participants or animals performed by any of the authors.

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

21. Si W, Lin V, Sun B, Jang KJ, Xing R, Saeed A, et al. Reliable and Interpretable Visual Field Progression Prediction with Diffusion Models and Conformal Risk Control. Lecture Notes in Computer Science. 2025:543-552. https://doi.org/10.1007/978-3-032-05182-0_53

22. Kim H, Kim E, Moon S, Jin SW, Kim JL, Lee SU, et al. Labeling matters: A multicenter machine learning study on visual field progression in Glaucoma. PLoS One. 2026;21(8):e0357179. https://doi.org/10.1371/journal.pone.0357179

23. Collins GS, Moons KGM, Dhiman P, Riley RD, Beam AL, Van Calster B, et al. TRIPOD+AI statement: updated guidance for reporting clinical prediction models that use regression or machine learning methods. BMJ. 2024;385:e078378. https://doi.org/10.1136/bmj-2023-078378

24. Montesano G, Chen A, Lu R, Lee CS, Lee AY. UWHVF: A Real-World, Open Source Dataset of Perimetry Tests From the Humphrey Field Analyzer at the University of Washington. Trans. Vis. Sci. Tech.. 2022;11(1):2. https://doi.org/10.1167/tvst.11.1.1

25. Marin-Franch I, Swanson WH. The visualFields package: A tool for analysis and visualization of visual fields. Journal of Vision. 2013;13(4):10-10. https://doi.org/10.1167/13.4.10

26. Huang X, Kong X, Shen Z, Ouyang J, Li Y, Jin K, et al. GRAPE: A multi-modal dataset of longitudinal follow-up visual field and fundus images for glaucoma management. Sci Data. 2023;10(1). https://doi.org/10.1038/s41597-023-02424-4

27. Phipson B, Smyth GK. Permutation P-values Should Never Be Zero: Calculating Exact P-values When Permutations Are Randomly Drawn. Statistical Applications in Genetics and Molecular Biology. 2010;9(1). https://doi.org/10.2202/1544-6115.1585

28. Angelopoulos AN, Bates S. Conformal Prediction: A Gentle Introduction. Foundations and Trends® in Machine Learning. 2023;16(4):494-591. https://doi.org/10.1561/2200000101

29. Freedman D, Lane D. A Nonstochastic Interpretation of Reported Significance Levels. Journal of Business & Economic Statistics. 1983;1(4):292-298. https://doi.org/10.1080/07350015.1983.10509354

30. Gagnon-Bartsch J, Shem-Tov Y. The classification permutation test: A flexible approach to testing for covariate imbalance in observational studies. Ann. Appl. Stat.. 2019;13(3):1464-1483. https://doi.org/10.1214/19-aoas1241

31. Wu Z, Saunders LJ, Daga FB, Diniz-Filho A, Medeiros FA. Frequency of Testing to Detect Visual Field Progression Derived Using a Longitudinal Cohort of Glaucoma Patients. Ophthalmology. 2017;124(6):786-792. https://doi.org/10.1016/j.ophtha.2017.01.027

32. Crabb DP, Garway-Heath DF. Intervals between Visual Field Tests When Monitoring the Glaucomatous Patient: Wait-and-See Approach. Invest. Ophthalmol. Vis. Sci.. 2012;53(6):2770. https://doi.org/10.1167/iovs.12-9476

33. Stagg BC, Brintz BJ, Stein JD, Hess R, Kawamoto K, Jammal AA, et al. Time to Identify Glaucoma Progression Given Typical Visual Field Testing Frequencies in a US Nationwide Insured Population. Ophthalmology Glaucoma. 2026;9(3):250-256. https://doi.org/10.1016/j.ogla.2025.11.004

34. Phu J, Kalloniatis M. The Frontloading Fields Study (FFS): Detecting Changes in Mean Deviation in Glaucoma Using Multiple Visual Field Tests Per Clinical Visit. Trans. Vis. Sci. Tech.. 2021;10(13):21. https://doi.org/10.1167/tvst.10.13.21

35. Chen L, Fujita A, Moradi M, Eslami M, Elze T, Zebardast N. Earlier confirmation of glaucoma progression with risk-weighted visual field and OCT scheduling. medRxiv [Preprint]. 2026. https://doi.org/10.64898/2026.11.16.26368187

36. Schell GJ, Lavieri MS, Helm JE, Liu X, Musch DC, Van Oyen MP, et al. Using Filtered Forecasting Techniques to Determine Personalized Monitoring Schedules for Patients with Open-Angle Glaucoma. Ophthalmology. 2014;121(8):1539-1546. https://doi.org/10.1016/j.ophtha.2014.02.021

37. Mohammadzadeh V, Li L, Fei Z, Davis T, Morales E, Wu K, et al. Efficacy of Smoothing Algorithms to Enhance Detection of Visual Field Progression in Glaucoma. Ophthalmology Science. 2024;4(2):100423. https://doi.org/10.1016/j.xops.2023.100423

# Supplementary Material

Supplementary Table S1: all metrics with 95% confidence intervals (sensitivity, specificity, true no-change and shuffle-audit false-alarm rates, secondary-reference sensitivity, GRAPE results) for every detector and number of fields. Supplementary Table S2: paired comparisons with D1 (difference, bootstrap 95% CI, exact McNemar p, Holm-adjusted p). Supplementary Table S3: fields to first flag among reference progressors, by detector (seed means). Supplementary Tables S4 and S5 (post hoc): sensitivity, specificity and paired tests against the reference computed only from fields after the first k. Supplementary Tables S6–S8 (amendment A3, exploratory): shuffle calibration, confirmation, and the enlarged reference for training-free detectors. Supplementary Table S9: external data set (GRAPE) with nominal thresholds. Supplementary Fig. S1: shuffle audit versus true no-change false-alarm rate. Supplementary Note S1: development history, including abandoned method ideas.
