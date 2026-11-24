# How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? A Benchmark With True No-Change Calibration

**Running title:** False alarms in visual-field progression detection

**Authors:** P N Bhargav Teja¹; [SECOND AUTHOR NAME]¹∗

¹ [Department], Vellore Institute of Technology (VIT), Vellore, Tamil Nadu, India

**Corresponding author (marked ∗):** [SECOND AUTHOR NAME], [Department], Vellore Institute of Technology (VIT), Vellore 632014, Tamil Nadu, India. E-mail: [CORRESPONDING AUTHOR E-MAIL]

**Article type:** Original Research

# Abstract

**Introduction:** Clinicians escalate glaucoma treatment when visual fields worsen. New detectors claim earlier detection, but few are checked on eyes that truly did not change. We asked how early progression can be detected without excess false alarms, and whether calibrating detectors on no-change data changes their ranking.

**Methods:** Ten detectors saw only the first 3–6 tests of each eye. Sensitivity was measured against a whole-series reference in a held-out University of Washington test set ({{c.uw_test_ref_prog}} progressors, {{c.uw_test_ref_stable}} stable eyes); false alarms on {{c.artes_patients}} patients tested weekly for 12 weeks (true no change); agreement in {{c.grape_eyes}} external eyes (GRAPE, China). In a pre-specified extension, five detectors were re-thresholded on retest data or on shuffled clinic records and compared at matched false-alarm rates.

**Results:** With three tests, a pooled conformal detector and a gradient-boosted tree model raised false alarms on {{m.D6.3.fpr_true_null}} and {{m.D8.3.fpr_true_null}} of no-change series, against {{m.D1.3.fpr_true_null}} for the trend of mean sensitivity (D1), although all looked similarly specific on reference-stable eyes. After retest calibration, every detector had about 5% false alarms, and the conformal and machine-learning detectors no longer flagged significantly more progressors than D1 (differences {{b.range.RC.D6+D8+D9.lo}} to {{b.range.RC.D6+D8+D9.hi}} percentage points). A retest-calibrated rate-of-change score flagged {{b.m.D2.5.RC.sens}} of progressors with five tests ({{b.ptci.RC.5.D2}}), but at lower specificity in clinic stable eyes, and its threshold was about {{b.ratioD2.mean}} times larger when set on shuffled clinic records, where it flagged fewer progressors than D1. D1's false-alarm rate stayed near 5% under every no-change source tested.

**Conclusion:** Apparent early-detection gains largely reflected where the threshold was set, not better discrimination. Detectors should be calibrated and compared on no-change data that match clinical test intervals.

**Keywords:** Benchmark; Calibration; False alarm; Glaucoma; Machine learning; Perimetry; Progression; Visual field

# Key Summary Points

**Why carry out this study?**

- New methods claim to detect glaucomatous visual-field progression earlier, but their false-alarm rates are rarely measured on eyes that truly did not change.
- We tested the hypothesis that no detector would flag substantially more future-confirmed progressors than the trend of mean sensitivity without excess false alarms.

**What was learned from the study?**

- With three tests, the most sensitive conformal and machine-learning detectors raised false alarms on {{m.D6.3.fpr_true_null}} and {{m.D8.3.fpr_true_null}} of true no-change series, although they looked specific on reference-stable eyes.
- When every detector was calibrated to the same false-alarm rate on retest data, the conformal and machine-learning detectors no longer flagged significantly more progressors than the simple trend test.
- A calibrated rate-of-change rule was more sensitive but less specific in clinic eyes, and its ranking depended on which no-change data set its threshold; the trend test kept a false-alarm rate near 5% under every no-change source tested.

# Plain Language Summary

Glaucoma damages the side vision slowly. Doctors use repeated visual field tests to see whether it is getting worse, and if it is, they step up treatment. Each test is noisy, so deciding early is hard. Many new computer methods claim to spot worsening sooner. We checked ten such methods in a new way: we also gave them test results from patients who were tested every week for 12 weeks. Glaucoma does not change in 12 weeks, so any "worsening" found in these patients is a false alarm. With only three tests, two of the newer methods that looked best raised false alarms in {{m.D6.3.fpr_true_null}} and {{m.D8.3.fpr_true_null}} of these test series, even though they looked accurate in the usual check. The simplest method, a straight line through the average sensitivity, raised false alarms at about the expected rate. When we adjusted every method so that it raised the same number of false alarms, the newer methods no longer found clearly more true worsening than the simple method. A rule based on the speed of loss looked better, but only when it was tuned on tests repeated a week apart, which are less noisy than yearly clinic tests. Our study was small. In a clinic in China, which method looked best depended on how worsening was defined. Patients and doctors should be careful with new methods that report earlier detection unless their false-alarm rate on stable eyes is known.

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [@1]. Treatment lowers intraocular pressure and slows visual loss [@2,3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [@8]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [@4], but routine care rarely reaches this frequency [@27]. Delays in follow-up are a documented cause of avoidable sight loss [@5].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [@6,12], sometimes after spatial or temporal smoothing [@36]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [@7,11,13]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [@6]. Bayesian and spatial models share information across locations or patients [@9,10,35]. Machine-learning models have been trained to classify or forecast progression [@16-21], and newer studies use deep generative models or risk-based test scheduling [@23,24,34].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [@7]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [@22]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

Artes and colleagues used short-interval retest data to measure the false-alarm rate of the event-based Guided Progression Analysis [@7]. We extend this approach to trend, permutation, conformal and machine-learning detectors, and add a future-confirmed reference and an external clinic. We built an open benchmark to answer one practical question: how early can visual-field progression be detected without excess false alarms? We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We tested the hypothesis that no detector would flag substantially more future-confirmed progressors (by 10 percentage points or more) than the simple trend test of mean sensitivity without excess false alarms on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate. Finally, in a pre-specified extension, we re-set each detector's threshold on no-change data, so that all detectors could be compared at the same false-alarm rate, and asked whether the ranking depends on which no-change data are used.

# Methods

## Study Design and Reporting

This was a retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [@32]. The analysis plan, including the ten detectors, thresholds, reference standards, research questions and statistical tests, was committed to the project repository before the final run (`experiments/protocol.md`). It was not registered in a public registry. Deviations from the plan are listed in Table 4.

The plan was written after a development phase in which we tried, and abandoned, several new detection methods (Supplementary Material S1). That phase used the Artes retest data once, and it already showed that the pooled-detrended conformal detector (D6) raised many false alarms on these data. The D6 result on the true no-change arm is therefore not a confirmatory finding. The UWHVF test set and the GRAPE labels were not used during development. A short software check ("quick mode") run before the final protocol amendments did process the Artes and GRAPE files; its outputs were not used to choose any detector, threshold or reference.

## Data Sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains {{c.uw_fields}} 24-2 tests from {{c.uw_eyes}} eyes of {{c.uw_patients}} patients seen in routine care in Seattle, USA [@14]. It includes sensitivities, total deviation values, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. Eyes with at least three tests were used ({{c.uw_train_eyes_ge3}} training, {{c.uw_val_eyes_ge3}} validation and {{c.uw_test_eyes_ge3}} test eyes). The test set was used once, for the final analysis. Note that D1 and D2 use mean sensitivity, whereas the reference below uses mean total deviation (the unweighted mean of total-deviation values, not the instrument's weighted MD).

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [@7]. Glaucoma does not change measurably in 12 weeks, so any "progression" flag in these series is a false alarm. The data ({{c.artes_fields}} tests from {{c.artes_eyes}} eyes) are distributed with the visualFields R package (version 1.0.7).

*GRAPE (external clinic).* The GRAPE data set contains {{c.grape_records}} follow-up visual-field records from {{c.grape_eyes}} eyes of {{c.grape_patients}} patients with glaucoma followed in Hangzhou, China [@15]. Fields were measured with a different perimeter ({{c.grape_points}} analysable points after removing untested points). Each eye carries progression labels assigned with three criteria: mean deviation, and two pointwise linear regression rules. These labels were assigned by rule-based criteria, not by clinical judgement. We used the mean-deviation label as the primary label ({{c.grape_md_prog}} progressing eyes) and the PLR2 label ({{c.grape_plr2_prog}} progressing eyes) as the main secondary label, because it is not based on mean deviation.

## Reference Standard (UWHVF)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5. Other eyes were excluded from the sensitivity and specificity analysis. By this definition every reference-stable eye had a non-negative long-term slope (median {{slope.0.median}} dB per year; progressors {{slope.1.median}} dB per year). The reference uses the whole series, including the first k tests seen by the detectors. This overlap (incorporation) favours detectors based on mean sensitivity, such as D1. We therefore also report an exploratory future-only reference built from tests k+1 to the end (Supplementary Table S5). Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations), which is not tied to mean deviation.

## Detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 OLS-MD:** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD rate:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [@6], using all possible orders of the k tests.
- **D5 pooled-shuffle conformal test:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of training-set eyes with the same number of tests and similar mean sensitivity (a conformal p-value [@31,29]).
- **D6 pooled-detrended conformal regional test:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [@30]. This variant was the most sensitive approach during development.
- **D7 event analysis:** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to Guided Progression Analysis [@13]. It uses raw sensitivity, not pattern deviation, so it is a simplified analogue rather than a re-implementation of the commercial software.
- **D8 machine learning, tabular:** gradient-boosted trees (LightGBM) on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set reference-stable eyes. These two models are deliberately simple baselines with a fixed tuning budget, not reproductions of published models.
- **D9 machine learning, sequence:** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 self-supervised order network:** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [@33].

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

For each eye or window, the flag was averaged over seeds; proportions and paired differences use these averaged flags. Proportions are reported with 95% confidence intervals (CIs) from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. Paired differences from D1 use the same patient-level bootstrap. Exact McNemar tests require one flag per eye, so they use the majority flag over seeds. We corrected p-values with the Holm method within each number of tests and endpoint, over the detectors that can flag at that number. With {{c.uw_test_ref_prog}} progressors, only differences of about {{x.mindiff}} percentage points or more could reach significance after correction (all discordant pairs favouring one detector), so we interpret the comparisons mainly through their CIs.

The protocol required the false-alarm CI on true no-change data to be judged against the nominal 5%, without fixing an exact rule. We report three rules (Table 4). The main rule, used in the text, is "excess false alarms": the whole 95% CI lies above 5%. This rule does not depend on the choice of a margin. We also report an operational validity rule (upper CI limit at most 10% and lower limit at most 5%), written into the methods draft while the final run was in progress, and the literal reading of the protocol (upper CI limit at most 5%), under which no detector that works at the nominal level, including D1, could be called valid with 30 retest patients.

Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells, with a CI from 500 joint bootstrap resamples of retest and UWHVF patients, and by their absolute difference. Analyses used Python 3.13 with NumPy, SciPy, scikit-learn, LightGBM and PyTorch. The code runs the benchmark (`run_all.py --mode full`) and then generates every statistic, table and figure from the saved per-eye outputs. A second, independent run in a fresh computing environment reproduced all {{rep.rows_repro}} per-eye detector outputs exactly ({{rep.flag_mismatches}} differences).

## Ethics

This study used only publicly available, de-identified data sets released by their custodians (UWHVF: BSD-3 licence; GRAPE: CC0; Artes data: distributed with the visualFields R package, Apache-2.0 licence). The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

# Results

## Study Data

In the UWHVF test set, {{c.uw_test_eyes_ge8}} eyes had at least eight tests. Of these, {{c.uw_test_ref_prog}} were reference progressors, {{c.uw_test_ref_stable}} were reference stable and {{c.uw_test_ref_excluded}} were indeterminate. The reference eyes came from {{c.uw_test_ref_patients}} patients. Their median age at the first test was {{c.uw_ref_age0_median}} years (interquartile range [IQR] {{c.uw_ref_age0_q1}}–{{c.uw_ref_age0_q3}}), median mean total deviation at the first test was {{c.uw_ref_md0_median}} dB (IQR {{c.uw_ref_md0_q1}} to {{c.uw_ref_md0_q3}}), and median follow-up was {{c.uw_ref_followup_y_median}} years with {{c.uw_ref_ntests_median.0}} tests. The median interval between tests was {{c.uw_ref_interval_y_median}} years. Progressors had a median whole-series slope of {{slope.1.median}} dB per year, so most were slow progressors. The true no-change arm contributed {{n.D1.3.fpr_true_null_n}} three-test windows (including time-label draws). In GRAPE, all {{c.grape_eyes_ge3}} eyes had at least three visits and {{c.grape_eyes_ge4}} had at least four.

## False Alarms on True No-Change Data (RQ1)

Table 1 and Fig. 2 show all results. With three tests, {{excess.3.yes}} had excess false alarms. The pooled-detrended conformal detector (D6) raised false alarms on {{mci.D6.3.fpr_true_null}} of no-change series, the tabular machine-learning model (D8) on {{mci.D8.3.fpr_true_null}}, and the sequence model (D9) on {{mci.D9.3.fpr_true_null}}. The simple trend test (D1) stayed close to its nominal level, at {{mci.D1.3.fpr_true_null}}. D8 still had excess false alarms with four tests, at {{mci.D8.4.fpr_true_null}}, and with five tests, at {{mci.D8.5.fpr_true_null}}, but not with six, at {{mci.D8.6.fpr_true_null}}. Under the operational validity rule, the invalid detectors were {{valid.3.no}} with three tests, {{valid.4.no}} with four, {{valid.5.no}} with five and {{valid.6.no}} with six; D9 with six tests, at {{mci.D9.6.fpr_true_null}}, failed only narrowly.

## Specificity on Reference-Stable Eyes Hid These False Alarms

The usual check, specificity on reference-stable eyes, did not reveal these false alarms. With three tests, D6 was {{m.D6.3.spec}} specific and D8 {{m.D8.3.spec}}, compared with {{m.D1.3.spec}} for D1 (false positives: {{pt.3.fp.D6.diff}} and {{pt.3.fp.D8.diff}} percentage points vs D1; Holm-adjusted p {{pt.3.fp.D6.p_holm}} and {{pt.3.fp.D8.p_holm}}). Yet on true no-change series, D6 and D8 raised {{ratio.D6.3.fpr_true_null}} and {{ratio.D8.3.fpr_true_null}} times as many false alarms as D1. All reference-stable eyes had a non-negative long-term slope (share with a positive slope: {{slope.0.share_positive}}), which makes them easier to classify than typical stable eyes.

## Sensitivity Compared With the Trend Test (RQ2)

With three tests, D1 flagged {{mci.D1.3.sens}} of reference progressors. D6 flagged {{m.D6.3.sens}} ({{ptci.3.sens.D6}}), the only significant gain, from a detector with excess false alarms. Among detectors without excess false alarms, the rate rule D2 had the largest point gain with three tests: it flagged {{m.D2.3.sens}} ({{ptci.3.sens.D2}}). With four to six tests, D1 flagged {{m.D1.4.sens}}, {{m.D1.5.sens}} and {{m.D1.6.sens}}. Event analysis (D7) flagged {{m.D7.5.sens}} with five tests ({{ptci.5.sens.D7}}). With six tests, D8 no longer had excess false alarms and flagged {{m.D8.6.sens}} ({{ptci.6.sens.D8}}). Rate and pointwise rules gained little after four tests; with six tests, D3 flagged {{m.D3.6.sens}} ({{ptci.6.sens.D3}}). Thus the hypothesis was not falsified, but the study cannot exclude gains of 10–30 percentage points for D2 with three tests or D8 with six tests.

The secondary, PoPLR-based reference gave lower sensitivities and a similar ordering of detectors (Spearman ρ between {{x.refcorr_min}} and {{x.refcorr_max}} within each number of tests; Supplementary Table S2). The exploratory future-only reference had too few eyes for firm conclusions (Supplementary Table S5).

## Machine-Learning Detectors Under the Usual Threshold Rule (RQ4)

Both supervised models were thresholded at 95% specificity on validation-set reference-stable eyes. On true no-change data, D8 exceeded the nominal 5% with three, four and five tests ({{m.D8.3.fpr_true_null}}, {{m.D8.4.fpr_true_null}} and {{m.D8.5.fpr_true_null}}) but not with six ({{m.D8.6.fpr_true_null}}). D9 exceeded it with three tests ({{m.D9.3.fpr_true_null}}) and five tests ({{m.D9.5.fpr_true_null}}). The hypothesis that this threshold rule gives too many false alarms was supported for short series, but not at every number of tests.

## The Shuffle Audit (RQ3)

Across the {{rq.all_cells.n_cells}} detector–test-number cells, the shuffle audit and the true no-change false-alarm rate were correlated (Spearman ρ {{rq.all_cells.spearman_rho}}, 95% CI {{rq.all_cells.rho_lo}}–{{rq.all_cells.rho_hi}}; Fig. 3). Excluding the {{x.na_cells}} cells where a detector cannot flag, ρ was {{rq.applicable_cells.spearman_rho}} ({{rq.applicable_cells.rho_lo}}–{{rq.applicable_cells.rho_hi}}). The median absolute difference was {{rq.all_cells.median_abs_diff}}, and {{rq.all_cells.share_within_3pp}} of cells differed by 3 percentage points or less. The audit caught D6 and D8 with three tests (shuffle false-alarm rates {{m.D6.3.fpr_shuffle}} and {{m.D8.3.fpr_shuffle}}). It over-estimated false alarms for rate rules and event analysis (D2 with three tests: {{m.D2.3.fpr_shuffle}} vs {{m.D2.3.fpr_true_null}}; D7 with six tests: {{m.D7.6.fpr_shuffle}} vs {{m.D7.6.fpr_true_null}}) and under-estimated them for the machine-learning models with three tests (D8: {{m.D8.3.fpr_shuffle}} vs {{m.D8.3.fpr_true_null}}; D9: {{m.D9.3.fpr_shuffle}} vs {{m.D9.3.fpr_true_null}}). The pre-specified target of ρ ≥ 0.7 was not met.

## External Clinic (RQ5)

In GRAPE (Table 2, Fig. 4), validity could not be assessed, because no true no-change data exist there; we report agreement with the two criterion-based labels. Against the mean-deviation label, D1 flagged {{mci.D1.3.grape_sens}} of progressors with three tests, at {{m.D1.3.grape_spec}} specificity. D2 flagged {{m.D2.3.grape_sens}} at {{m.D2.3.grape_spec}} specificity ({{pt.3.gfp.D2.absdiff}} percentage points more false positives; Holm-adjusted p {{pt.3.gfp.D2.p_holm}}). D8, transferred unchanged, flagged {{m.D8.3.grape_sens}} at {{m.D8.3.grape_spec}} specificity ({{pt.3.gfp.D8.absdiff}} percentage points more false positives; Holm-adjusted p {{pt.3.gfp.D8.p_holm}}).

Against the pointwise PLR2 label, which is not based on mean deviation, D1 flagged only {{mci.D1.3.grape_plr2_sens}} of progressors. D2 flagged {{m.D2.3.grape_plr2_sens}} ({{ptci.3.p2sens.D2}}) and D8 {{m.D8.3.grape_plr2_sens}} ({{ptci.3.p2sens.D8}}), but both again with more false positives (specificity {{m.D2.3.grape_plr2_spec}} and {{m.D8.3.grape_plr2_spec}} vs {{m.D1.3.grape_plr2_spec}}). Thus, in this clinic, the detector that looked best depended on the label, and every gain in sensitivity came with lower specificity.

## No-Change Calibration and Matched Comparison (Amendment B)

Retest calibration brought every detector to about the nominal false-alarm rate: none of the {{b.hyp.HB1_cells}} detector–test-number cells had excess false alarms (HB1 supported; Table 5, Fig. 5). Shuffle calibration came within 3 percentage points of 5% in {{b.hyp.HB2_SC_share_within_3pp}} of cells, short of the pre-specified 75% (HB2 not supported); it was very conservative for the rate score (D2 false alarms {{b.fprrange.SC.D2.lo}} to {{b.fprrange.SC.D2.hi}}).

At retest-matched false-alarm rates, the conformal and machine-learning detectors (D6, D8, D9) no longer flagged significantly more progressors than D1: differences ranged from {{b.range.RC.D6+D8+D9.lo}} to {{b.range.RC.D6+D8+D9.hi}} percentage points, with no significant difference (smallest Holm-adjusted p {{b.minholm.RC.D6+D8+D9}}). For example, with three tests, retest-calibrated D8 had {{b.mci.D8.3.RC.fpr_true_null}} false alarms and flagged {{b.m.D8.3.RC.sens}} of progressors, compared with {{b.m.D1.3.RC.sens}} for D1.

HB3 was falsified by the rate score. With retest calibration, D2 flagged {{b.m.D2.5.RC.sens}} of progressors with five tests ({{b.ptci.RC.5.D2}}) and {{b.m.D2.6.RC.sens}} with six ({{b.ptci.RC.6.D2}}), at false-alarm rates of {{b.m.D2.5.RC.fpr_true_null}} and {{b.m.D2.6.RC.fpr_true_null}}. The gain was also seen against the PoPLR-based secondary reference ({{b.r2.D2.5.sens_ref2}} vs {{b.r2.D1.5.sens_ref2}} with five tests). The retest-calibrated slope threshold was small: {{b.thr.D2.5.thr_RC}} dB per year with five tests, close to the −0.3 dB per year used to define reference progressors. When the same score was calibrated on shuffled clinic records, the threshold was about {{b.ratioD2.mean}} times larger at every number of tests, and D2 flagged fewer progressors than D1 (differences {{b.range.SC.D2.lo}} to {{b.range.SC.D2.hi}} percentage points). For all other detectors, the two calibration sources gave thresholds within a factor of {{b.ratiomin}} to {{b.ratiomax}}.

The time-label check supported D1's robustness: its false-alarm rate stayed between {{b4.range.D1.lo}} and {{b4.range.D1.hi}} whether the retest series were given clinic dates, annual spacing or the dates of reference-stable eyes. The pointwise rule D3, in contrast, raised false alarms on {{b4.D3.3.annual}} of three-test series with annual spacing. On all {{b3.c.eyes}} UWHVF eyes with a reference label ({{b3.c.progressors}} progressors, {{b3.c.stable}} stable, {{b3.c.patients}} patients), the fixed rate rule D2 flagged more progressors than D1 with three tests ({{b3.ptci.3.D2}}), at lower specificity ({{b3.m.D2.3.spec}} vs {{b3.m.D1.3.spec}}); with four to six tests, D1 flagged more progressors than D2, D3 and D4 (Supplementary Table S6).

Two post-hoc checks, requested in review, tested whether the gain of the retest-calibrated rate score was an artefact of the slope-based reference, whose −0.3 dB per year cut-off is close to the calibrated threshold. Because D1 and D2 need no training, we applied their retest-calibrated thresholds to all {{b3.c.eyes}} labelled UWHVF eyes and to alternative references (Supplementary Table S7). D2 flagged {{rb.range.diff_sens.lo}} to {{rb.range.diff_sens.hi}} percentage points more progressors than D1 under every definition, including a −1.0 dB per year cut-off and a future-only reference built from the tests after those seen by the detectors. The gain therefore did not depend on the reference definition. It came at a cost in clinic eyes: specificity in reference-stable eyes was {{rb.range.D2_spec.lo.primary}}–{{rb.range.D2_spec.hi.primary}}% for D2 against {{rb.range.D1_spec.lo.primary}}–{{rb.range.D1_spec.hi.primary}}% for D1, and among the {{rb.nind}} indeterminate eyes D2 flagged {{rb.ind.D2.lo}}–{{rb.ind.D2.hi}}% against {{rb.ind.D1.lo}}–{{rb.ind.D1.hi}}% for D1. This is the pattern expected if weekly retests under-represent the year-to-year noise of clinic tests. Finally, HB3 was falsified with the pre-specified Holm correction within each number of tests; with a correction across all {{x.nhb3}} retest-calibrated comparisons, the smallest adjusted p was {{hb3global}}.

## Real-World Measures

Table 3 translates the results into clinical units. With D1, {{rw.D1.cum_detected_by_k4}} of reference progressors were flagged by the fourth test, {{rw.D1.cum_detected_by_k5}} by the fifth and {{rw.D1.cum_detected_by_k6}} by the sixth; the median was {{rw.D1.median_tests_to_first_flag}} tests, or about {{x.years_to_flag}} years after the first test at the observed testing interval. At a single review with three tests, D1 would raise about {{rw.D1.false_flags_per_1000_k3}} false flags per 1,000 no-change eyes, D6 about {{rw.D6.false_flags_per_1000_k3}} and D8 about {{rw.D8.false_flags_per_1000_k3}}. Repeated reviews add up: over four reviews, D1 flagged {{cum.D1}} of no-change series at least once, D6 {{cum.D6}} and D8 {{cum.D8}}.

# Discussion

This benchmark asked how early visual-field progression can be detected without excess false alarms. In short series, the tested conformal and machine-learning detectors flagged more progressors than the trend of mean sensitivity, but they also raised far more false alarms on eyes that truly did not change. Specificity on reference-stable eyes missed these false alarms. Among detectors without excess false alarms, none flagged significantly more progressors than the trend test, but our small reference groups leave room for moderate gains.

The main lesson concerns evaluation. A pooled-detrended conformal test looked like a clear gain with three tests: it raised sensitivity {{ratio.D6.3.sens}}-fold, with the same specificity as the trend test on reference-stable eyes. The true no-change arm, and the shuffle audit, showed that it flagged about {{m.D6.3.fpr_true_null}} of no-change series. With three tests, detrending leaves one residual degree of freedom, and the pooled reference does not reflect each eye's own noise. Reference-stable eyes, defined by a long-term slope that is not negative, are an easy test of specificity. Any method whose threshold is set or checked on such eyes may look better than it is.

The calibration extension sharpens this lesson. When every detector was held to the same false-alarm rate on retest data, the conformal and machine-learning detectors no longer showed a significant advantage. Most of their earlier "gain" reflected a different operating point rather than better discrimination, although moderate differences cannot be excluded; for D8 with six tests the difference was {{d8k6}}. The rate-of-change score behaved differently: it looked clearly better than the trend test after retest calibration, but clearly worse after calibration on the clinic's own shuffled records. The reason is noise. Weekly retests contain only short-term variability, whereas shuffled clinic series spread years of variability, and any true progression, across the series. A raw slope threshold depends directly on this noise level, so the retest threshold is probably too liberal for yearly clinic tests and the shuffle threshold too strict. Our post-hoc checks support this explanation: with the retest threshold, the rate rule was more sensitive under every reference definition, but it flagged clearly more clinic eyes that were stable or indeterminate. Its advantage is therefore a trade-off between sensitivity and specificity, whose terms depend on noise that weekly retests do not capture. The trend test divides the slope by the eye's own scatter. Its false-alarm rate stayed between {{b4.range.D1.lo}} and {{b4.range.D1.hi}} under every no-change source we tried, including different time labels. The regional trend statistic (D6) and the machine-learning scores also had similar thresholds under the two calibration sources, but they were not part of the time-label check. The trend test is therefore a safe default when the noise of a clinic's own tests is unknown. A rate rule calibrated on long-interval no-change data, which do not yet exist publicly, could offer a better trade-off and deserves study.

These findings agree with earlier work. Artes and colleagues found that the "possible progression" alert of the Guided Progression Analysis was much less specific than its "likely progression" alert, and that false alerts varied greatly between patients [@7]. Wu and Medeiros compared event-based and trend-based analyses for detecting progression [@11]. Machine-learning studies of progression have mostly been evaluated against labels derived from other progression criteria [@16-21], and a multicentre study found that results depend strongly on the label [@22]. Our external-clinic results agree: the trend test looked best against a mean-deviation label and weak against a pointwise label. Our results add a direct test of false alarms for several classes of detectors, at a fixed small number of tests, together with an estimate of how false alarms accumulate over repeated reviews.

Repeated review matters in practice. A test with a 5% false-alarm rate at each review flags more than 5% of stable eyes over several reviews. In our data, the trend test flagged {{cum.D1.p}} of no-change series at least once over four reviews. A practical safeguard, used in many clinics, is to confirm a flag on the next test before escalating treatment; we did not evaluate this rule. Studies of testing frequency show that clinics often need many years to confirm progression [@25-27], and our real-world measures agree. Front-loading or clustering tests [@28,4] may help, but we did not test this.

What does this mean for a clinic? First, the trend of mean sensitivity with a p-value kept its nominal false-alarm rate at each review, and no detector without excess false alarms clearly beat it in our data. Second, simple rate rules without a p-value had few false alarms on our no-change data, but in the external clinic they raised false positives against both labels. Third, before adopting a new detector, a clinic can run a shuffle audit on its own records. It caught the largest problems here, but it over- or under-estimated false alarms for some detectors, so it is a screen, not a replacement for true no-change data. For commercial software that cannot be re-run, clinics can ask vendors for false-alarm rates on short-interval retest data and over repeated reviews.

For method developers, we suggest five reporting items: false alarms on true no-change series, not only specificity on stable eyes; comparisons at matched false-alarm rates, with the source of the no-change data stated; cumulative false alarms over repeated reviews; sensitivity at a fixed, small number of tests; and results against more than one progression label. Our code and per-eye outputs are open, so new detectors can be added and compared on the same terms.

This study has limitations. First, the reference groups were small ({{c.uw_test_ref_prog}} progressors and {{c.uw_test_ref_stable}} stable eyes), so CIs were wide, and the comparisons with D1 had low power. Second, the reference uses the whole series, including the first k tests, and is based on mean total deviation; this favours D1. The secondary PoPLR reference reduced, but did not remove, this bias, and the future-only reference had too few eyes. Third, reference-stable eyes had non-negative slopes and {{c.uw_test_ref_excluded}} indeterminate eyes were excluded, so specificity on UWHVF is optimistic. Fourth, the true no-change arm had only {{c.artes_patients}} patients tested a week apart. We gave each series the test dates of a clinic eye (amendment A1). This keeps it a valid null, but it does not reproduce long-term changes in noise, such as cataract, learning or fatigue, and it may favour rate rules. Fifth, the "complex" detectors are our own implementations: D6 came from our development work, D7 is a simplified analogue of commercial event analysis, and D8 and D9 are simple machine-learning baselines trained on few labelled eyes. Our conclusions apply to these detectors and should not be generalised to all conformal or machine-learning methods. Sixth, GRAPE used a different perimeter, its labels are criterion-based, and several detectors were re-calibrated or omitted there. Seventh, UWHVF has no reliability indices or diagnoses. Eighth, the calibration extension was planned after the first results and reviews; it was time-stamped before it was run, but it is not independent of them. Retest calibration makes HB1 nearly true by construction, shuffle calibration scored the machine-learning models on their own training eyes, and the falsification of HB3 depends on the pre-specified within-test-number Holm correction. Finally, the analysis plan was committed to our repository rather than a public registry, and it followed a development phase that used the retest data once (Table 4).

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

P N Bhargav Teja: conceptualisation, methodology, software, data curation, formal analysis, visualisation, writing – original draft. [SECOND AUTHOR NAME]: supervision, validation, writing – review and editing. Both authors read and approved the final manuscript.

## Disclosures

P N Bhargav Teja and [SECOND AUTHOR NAME] declare that they have no competing interests.

## Compliance With Ethics Guidelines

This study used only publicly available, de-identified data sets released by their custodians under open licences. The original studies obtained ethical approval. No new data were collected, and no further ethical approval was required. This article does not contain any new studies with human participants or animals performed by any of the authors.

## Data Availability

All data sets are public: UWHVF (https://github.com/uw-biomedical-ml/uwhvf), GRAPE (Figshare file 41670009, "VF and clinical information.xlsx", described in [@15]) and the Artes retest data (visualFields R package 1.0.7, CRAN). The analysis code, analysis plan, per-eye detector outputs and all result files are provided as supplementary material and will be deposited in a public repository on acceptance.

# References

{{REFERENCES}}

# Tables

{{TABLE1}}

{{TABLE2}}

{{TABLE3}}

{{TABLE4}}

{{TABLE5}}
