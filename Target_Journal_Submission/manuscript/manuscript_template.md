# How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm

**Running title:** False alarms in visual-field progression detection

**Authors:** [AUTHOR NAMES, AFFILIATIONS AND ORCID TO BE ADDED BY THE AUTHORS]

**Corresponding author:** [NAME, ADDRESS, E-MAIL TO BE ADDED]

**Article type:** Original Research

# Abstract

**Introduction:** Clinicians escalate glaucoma treatment when visual fields get worse. Many new methods claim to detect this change earlier, but few have been checked on eyes that truly did not change. We asked how early progression can be detected without raising false alarms.

**Methods:** We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods, using only the first 3–6 tests of each eye. Sensitivity and specificity were measured against a future-confirmed reference in a held-out test set of the University of Washington data set ({{c.uw_test_ref_prog}} progressors, {{c.uw_test_ref_stable}} stable eyes). False alarms were measured on {{c.artes_patients}} patients tested weekly for 12 weeks (true no change). External validity was tested in {{c.grape_eyes}} eyes from China (GRAPE). The analysis was pre-registered.

**Results:** With three tests, the simple trend test (OLS-MD) flagged {{m.D1.3.sens}} of progressors with {{m.D1.3.fpr_true_null}} false alarms. A pooled conformal detector flagged {{m.D6.3.sens}} ({{ptci.3.sens.D6}}) but raised false alarms on {{mci.D6.3.fpr_true_null}} of no-change series. Gradient-boosted trees raised {{mci.D8.3.fpr_true_null}}. Both looked about as specific as OLS-MD on reference-stable eyes ({{m.D6.3.spec}} and {{m.D8.3.spec}} vs {{m.D1.3.spec}}). No detector with a valid false-alarm rate flagged significantly more progressors than OLS-MD at any number of tests. Re-running detectors on shuffled tests tracked the true false-alarm rate moderately (Spearman ρ {{a.spearman_rho}}). In GRAPE, the higher sensitivity of a rate rule and of the machine-learning model came with {{pt.3.gfp.D2.absdiff}} and {{pt.3.gfp.D8.absdiff}} percentage points more false positives (Holm-adjusted p {{pt.3.gfp.D2.p_holm}} and {{pt.3.gfp.D8.p_holm}}).

**Conclusion:** Apparent early-detection gains were explained by false alarms that only a true no-change check revealed. New detectors should report false alarms on true no-change data before clinical use.

**Keywords:** Benchmark; False alarm; Glaucoma; Machine learning; Perimetry; Progression; Specificity; Visual field

# Key Summary Points

**Why carry out this study?**

- Many new methods claim to detect glaucomatous visual-field progression earlier, but their false-alarm rates are rarely measured on eyes that truly did not change.
- We hypothesised that no detector would flag substantially more future-confirmed progressors than a simple trend test while keeping a valid false-alarm rate.

**What was learned from the study?**

- With three tests, the most sensitive pooled conformal and machine-learning detectors raised false alarms on {{m.D6.3.fpr_true_null}} and {{m.D8.3.fpr_true_null}} of true no-change series, although they looked specific on reference-stable eyes.
- No detector with a valid false-alarm rate flagged significantly more progressors than the trend of mean sensitivity at 3–6 tests, in Seattle or in an external clinic in China.
- Before a new detector guides treatment escalation, it should report false alarms on true no-change data; a shuffle audit of a clinic's own records is a useful but imperfect screen.

# Introduction

Glaucoma is a leading cause of irreversible blindness. About 76 million people had glaucoma in 2020, and this number is expected to reach about 112 million by 2040 [@1]. Treatment lowers intraocular pressure and slows visual loss [@2,3]. The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.

Detecting this change early is hard. A single visual field test is noisy, and the noise grows as sensitivity falls [@8]. To separate true loss from noise, clinicians need a series of tests. Expert guidance suggests six tests in the first two years [@4], but routine care rarely reaches this frequency [@27]. Delays in follow-up are a documented cause of avoidable sight loss [@5].

Many methods aim to detect progression from fewer tests. Trend methods fit a line through the mean deviation or through each test location [@6,12], sometimes after spatial or temporal smoothing [@36]. Event methods compare each follow-up test with a baseline, using limits taken from stable patients [@7,11,13]. Permutation methods, such as permutation of pointwise linear regression (PoPLR), compare the eye's real test order with shuffled orders of the same tests [@6]. Bayesian and spatial models share information across locations or patients [@9,10,35]. Machine-learning models have been trained to classify or forecast progression [@16-21], and newer studies use deep generative models or risk-based test scheduling [@23,24,34].

Two weaknesses run through this literature. First, most new detectors are judged by how many eyes they flag. More flags can mean better sensitivity, or simply more false alarms. Specificity is usually estimated indirectly: by shuffling test order, by using eyes labelled stable by another criterion, or by simulation. Only a few studies have measured false alarms on true no-change data, where the same patients were tested repeatedly over a few weeks [@7]. Second, labels for "progression" differ between studies, and models trained on one label may not transfer [@22]. As a result, clinicians cannot easily tell whether an earlier flag from a new method is real progression or a false alarm. A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery and their side effects and costs.

We built an open benchmark to answer one practical question: how early can visual-field progression be detected without raising false alarms? The benchmark has a true no-change arm, a future-confirmed reference standard and an external clinic. We compared ten detectors, from simple trend tests to permutation, conformal, event-based and machine-learning methods. We tested the hypothesis that no detector would flag substantially more future-confirmed progressors (by 10 percentage points or more) than the simple trend test of mean sensitivity while keeping a valid false-alarm rate on true no-change data. We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate.

# Methods

## Study Design and Reporting

This was a retrospective benchmark study of public, de-identified data. We followed the TRIPOD+AI reporting guidance where it applies to detection models [@32]. The analysis plan, including all ten detectors, thresholds, reference standards, research questions and statistical tests, was written down and time-stamped before the final test data were analysed (code repository, `experiments/protocol.md`). Two amendments were made before any final result was seen; both are reported below. The study was preceded by a development phase in which we tried, and abandoned, several new detection methods. Every idea from that phase, with its result, is listed in Supplementary Material S1.

## Data Sources

We used three data sets (Fig. 1).

*UWHVF (development and future-reference evaluation).* The University of Washington Humphrey Visual Field data set contains {{c.uw_fields}} 24-2 tests from {{c.uw_eyes}} eyes of {{c.uw_patients}} patients seen in routine care in Seattle, USA [@14]. It includes sensitivities, total deviation values, age and laterality, but no diagnosis or reliability indices. We split patients, not tests, into training (60%), validation (20%) and test (20%) sets using a fixed hash of the patient identifier. Both eyes of a patient were always in the same set. Eyes with at least three tests were used ({{c.uw_train_eyes_ge3}} training, {{c.uw_val_eyes_ge3}} validation and {{c.uw_test_eyes_ge3}} test eyes). The test set was used once, for the final analysis.

*Artes retest data (true no-change arm).* Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks [@7]. Glaucoma does not change measurably in 12 weeks, so any "progression" flag in these series is a false alarm. The data ({{c.artes_fields}} tests from {{c.artes_eyes}} eyes) are distributed with the visualFields R package (version 1.0.7).

*GRAPE (external clinic).* The GRAPE data set contains {{c.grape_records}} follow-up visual-field records from {{c.grape_eyes}} eyes of {{c.grape_patients}} patients with glaucoma followed in Hangzhou, China [@15]. Fields were measured with a different perimeter ({{c.grape_points}} analysable points after removing untested points). Each eye carries progression labels assigned with three criteria: mean deviation, and two pointwise linear regression rules. We used the mean-deviation label as the primary label ({{c.grape_md_prog}} progressing eyes).

## Reference Standard (UWHVF)

For eyes with at least eight tests, we defined a future-confirmed reference from the whole series. An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01. An eye was stable if the one-sided p was above 0.5. Other eyes were excluded from the sensitivity and specificity analysis. Because this reference is based on mean deviation, we also report a secondary reference based on PoPLR over the whole series (2,000 permutations), which is not tied to mean deviation.

## Detectors

Each detector saw only the first k tests of a series (k = 3, 4, 5 or 6) and returned "progression" or "no progression". The two blind-spot locations were removed. All detectors used a nominal false-alarm level of 5% where a level applies.

- **D1 OLS-MD:** ordinary least-squares slope of mean sensitivity against time, one-sided t-test, p < 0.05.
- **D2 MD rate:** slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value).
- **D3 PLR-3:** at least three locations with a slope of −1 dB per year or worse and p < 0.01.
- **D4 PoPLR:** permutation of pointwise linear regression [@6], using all possible orders of the k tests.
- **D5 pooled-shuffle conformal test:** the trend statistic of D1 is compared with the same statistic computed on shuffled series of training-set eyes with the same number of tests and similar mean sensitivity (a conformal p-value [@31,29]).
- **D6 pooled-detrended conformal regional test:** as D5, but uses the worst of four regional trends and builds the reference from detrended, shuffled series [@30]. This variant was the most sensitive approach during development.
- **D7 event analysis:** a location is "deteriorated" if its loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; progression requires at least three deteriorated locations on two consecutive follow-up tests, similar in spirit to Guided Progression Analysis [@13]. It needs at least four tests.
- **D8 machine learning, tabular:** gradient-boosted trees (LightGBM) on 14 summary features of the first k tests, trained to predict the reference label; threshold set at 95% specificity on validation-set stable eyes, as is common in machine-learning studies.
- **D9 machine learning, sequence:** a gated recurrent unit network on the raw k fields and test intervals, with the same labels, threshold rule and tuning budget (12 configurations) as D8.
- **D10 self-supervised order network:** a network trained, without labels, to recognise the true time order of an eye's tests among shuffled orders; its score was used as a PoPLR-type permutation statistic [@33].

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

In the UWHVF test set, {{c.uw_test_eyes_ge8}} eyes had at least eight tests. Of these, {{c.uw_test_ref_prog}} were reference progressors, {{c.uw_test_ref_stable}} were reference stable and {{c.uw_test_ref_excluded}} were indeterminate. The {{c.uw_test_ref_prog}} + {{c.uw_test_ref_stable}} reference eyes came from {{c.uw_test_ref_patients}} patients. Their median age at the first test was {{c.uw_ref_age0_median}} years (interquartile range [IQR] {{c.uw_ref_age0_q1}}–{{c.uw_ref_age0_q3}}), median mean total deviation at the first test was {{c.uw_ref_md0_median}} dB (IQR {{c.uw_ref_md0_q1}} to {{c.uw_ref_md0_q3}}), and median follow-up was {{c.uw_ref_followup_y_median}} years with {{c.uw_ref_ntests_median.0}} tests. The median interval between tests was {{c.uw_ref_interval_y_median}} years, so each additional test represents about one more year of follow-up. The true no-change arm contributed {{n.D1.3.fpr_true_null_n}} three-test windows (including time-label draws). In GRAPE, all {{c.grape_eyes_ge3}} eyes had at least three visits and {{c.grape_eyes_ge4}} had at least four. The full run took {{meta.runtime_s}} seconds on a four-core CPU.

## False Alarms on True No-Change Data (RQ1)

Table 1 and Fig. 2 show all results. With three tests, {{nvalid.3}} of 10 detectors were valid. The invalid detectors were {{valid.3.no}}. The pooled-detrended conformal detector (D6) raised false alarms on {{mci.D6.3.fpr_true_null}} of no-change series. The tabular machine-learning model (D8) raised {{mci.D8.3.fpr_true_null}}, and the sequence model (D9) raised {{mci.D9.3.fpr_true_null}}. The simple trend test (D1) stayed close to its nominal level, at {{mci.D1.3.fpr_true_null}}. The invalid detectors were {{valid.4.no}} with four tests, {{valid.5.no}} with five tests and {{valid.6.no}} with six tests. D8 remained invalid with four tests, at {{mci.D8.4.fpr_true_null}}, and with five tests, at {{mci.D8.5.fpr_true_null}}. D9 with six tests, at {{mci.D9.6.fpr_true_null}}, failed the rule only narrowly.

## Specificity on Reference-Stable Eyes Hid These False Alarms

The usual check, specificity on reference-stable eyes, did not reveal these false alarms. With three tests, D6 was {{m.D6.3.spec}} specific and D8 was {{m.D8.3.spec}} specific, compared with {{m.D1.3.spec}} for D1. Neither difference was significant (exact McNemar test, Holm-adjusted p {{pt.3.fp.D6.p_holm}} for D6 and p {{pt.3.fp.D8.p_holm}} for D8). Yet on true no-change series, D6 and D8 raised {{ratio.D6.3.fpr_true_null}} and {{ratio.D8.3.fpr_true_null}} times as many false alarms as D1. Reference-stable eyes are selected for a flat long-term course, so they are easier than typical stable eyes.

## Sensitivity Compared With the Trend Test (RQ2)

With three tests, D1 flagged {{mci.D1.3.sens}} of reference progressors. The largest gain came from D6, which flagged {{m.D6.3.sens}} ({{ptci.3.sens.D6}}). This was the only significant gain in the study, and it came from an invalid detector. Among valid detectors, the rate rule D2 had the largest point gain with three tests: it flagged {{m.D2.3.sens}} ({{ptci.3.sens.D2}}). With four to six tests, D1 flagged {{m.D1.4.sens}}, {{m.D1.5.sens}} and {{m.D1.6.sens}} of progressors. Event analysis (D7) flagged {{m.D7.5.sens}} at five tests ({{ptci.5.sens.D7}}). With six tests, D8 was valid and flagged {{m.D8.6.sens}} ({{ptci.6.sens.D8}}). Rate and pointwise rules lost sensitivity with more tests; at six tests, D3 flagged {{m.D3.6.sens}} ({{ptci.6.sens.D3}}). Therefore, the hypothesis was not falsified: no valid detector beat D1 by 10 percentage points or more with a Holm-adjusted p < 0.05. However, the CIs were wide, and gains of this size cannot be excluded for D2 at three tests or D8 at six tests.

The secondary, PoPLR-based reference gave the same ranking (Supplementary Table S2). For example, with five tests D1 flagged {{m.D1.5.sens_ref2}} and D7 flagged {{m.D7.5.sens_ref2}} of the {{n.D1.5.sens_ref2_n}} secondary-reference progressors.

## Machine-Learning Detectors Under the Usual Threshold Rule (RQ4)

Both supervised models were thresholded at 95% specificity on validation-set reference-stable eyes, as is common in machine-learning studies. On true no-change data, D8 exceeded the nominal 5% at three, four and five tests ({{m.D8.3.fpr_true_null}}, {{m.D8.4.fpr_true_null}} and {{m.D8.5.fpr_true_null}}) but not at six tests ({{m.D8.6.fpr_true_null}}). D9 exceeded it at three tests ({{m.D9.3.fpr_true_null}}) and five tests ({{m.D9.5.fpr_true_null}}). The hypothesis that this threshold rule gives too many false alarms was therefore supported for short series, but not at every number of tests.

## The Shuffle Audit (RQ3)

Across the {{a.n_cells}} detector–test-number cells, the shuffle audit and the true no-change false-alarm rate were correlated (Spearman ρ {{a.spearman_rho}}, p {{a.spearman_p}}; Fig. 3). The median absolute difference was {{a.median_abs_diff}}, and {{a.share_within_3pp}} of cells differed by 3 percentage points or less. The audit correctly flagged D6 and D8 at three tests as invalid (shuffle false-alarm rates {{m.D6.3.fpr_shuffle}} and {{m.D8.3.fpr_shuffle}}). It over-estimated false alarms for rate rules and event analysis (for example, D2 at three tests: {{m.D2.3.fpr_shuffle}} vs {{m.D2.3.fpr_true_null}}; D7 at six tests: {{m.D7.6.fpr_shuffle}} vs {{m.D7.6.fpr_true_null}}). The largest difference was {{a.max_abs_diff}}. The pre-registered target of ρ ≥ 0.7 was not met, so the hypothesis was only partly supported.

## External Clinic (RQ5)

In GRAPE (Table 2, Fig. 4), D1 flagged {{mci.D1.3.grape_sens}} of clinician-labelled progressors with three tests, with {{m.D1.3.grape_spec}} specificity. The rate rule D2 flagged {{m.D2.3.grape_sens}} ({{ptci.3.gsens.D2}}), but its specificity fell to {{m.D2.3.grape_spec}} ({{pt.3.gfp.D2.absdiff}} percentage points more false positives; Holm-adjusted p {{pt.3.gfp.D2.p_holm}}). The machine-learning model D8, transferred unchanged, flagged {{m.D8.3.grape_sens}} ({{ptci.3.gsens.D8}}), with specificity {{m.D8.3.grape_spec}} ({{pt.3.gfp.D8.absdiff}} percentage points more false positives; Holm-adjusted p {{pt.3.gfp.D8.p_holm}}). With four tests, the pattern was the same: D2 and D8 gained sensitivity only with significantly more false positives ({{pt.4.gfp.D2.absdiff}} and {{pt.4.gfp.D8.absdiff}} percentage points more false positives; Holm-adjusted p {{pt.4.gfp.D2.p_holm}} and {{pt.4.gfp.D8.p_holm}}). The re-calibrated conformal test (D5) matched D1 ({{m.D5.3.grape_sens}} vs {{m.D1.3.grape_sens}} sensitivity at three tests). The GRAPE progressor group was small ({{n.D1.3.grape_sens_n}} eyes at three tests and {{n.D1.4.grape_sens_n}} at four), so these sensitivity estimates are imprecise.

## Real-World Measures

Table 3 translates the results into clinical units. With D1, {{rw.D1.cum_detected_by_k4}} of future-confirmed progressors were flagged by the fourth test, {{rw.D1.cum_detected_by_k5}} by the fifth and {{rw.D1.cum_detected_by_k6}} by the sixth; the median was {{rw.D1.median_tests_to_first_flag}} tests. D1 produced about {{rw.D1.false_flags_per_1000_k3}} false flags per 1,000 no-change eyes at the three-test review. D6 flagged progressors earlier (median {{rw.D6.median_tests_to_first_flag}} tests) but would raise about {{rw.D6.false_flags_per_1000_k3}} false flags per 1,000 no-change eyes at the three-test review. D8 would raise about {{rw.D8.false_flags_per_1000_k3}}. In a clinic reviewing 1,000 stable eyes, that is roughly {{rw.D6.false_flags_per_1000_k3}} and {{rw.D8.false_flags_per_1000_k3}} unnecessary escalation discussions instead of {{rw.D1.false_flags_per_1000_k3}}.

# Discussion

This benchmark asked a simple question: how early can visual-field progression be detected without raising false alarms? The answer, in two clinics, was that the simple trend of mean sensitivity was hard to beat. More complex detectors did flag more progressors in short series. But when they did, they also raised far more false alarms on eyes that truly did not change. The usual check, specificity on reference-stable eyes, missed these false alarms.

The main lesson is about evaluation, not about any one method. Our own development history shows the risk. A pooled-detrended conformal test looked like a clear gain with three tests: it raised sensitivity {{ratio.D6.3.sens}}-fold, with the same specificity as the trend test on reference-stable eyes. Only the true no-change arm showed that it flagged {{m.D6.3.fpr_true_null}} of no-change series. The cause was simple. With three tests, detrending leaves one residual degree of freedom, and the pooled reference does not reflect the eye's own noise. Similar problems can affect any method whose false-alarm rate is set on selected stable eyes rather than on true no-change data.

These findings agree with earlier work. Artes and colleagues used the same retest data to examine the specificity of event-based Guided Progression Analysis [@7]. Wu and Medeiros compared pointwise event-based and global trend-based analyses for detecting progression [@11]. Machine-learning studies of progression have mostly been evaluated against labels derived from other progression criteria [@16-21], and a multicentre study found that results depend strongly on the progression label [@22]. Our results add a direct test: with the usual threshold rule, two machine-learning models exceeded the nominal false-alarm rate on true no-change data in short series. The models may still be useful, but their thresholds need to be set on no-change data. Studies of testing frequency show that clinics often need many years to confirm progression [@25-27]. Our real-world measures agree: with about one test per year, the trend test needed a median of {{rw.D1.median_tests_to_first_flag}} tests. Front-loading or clustering tests [@28,4] is therefore likely to help more than a more complex detector.

What should a clinic do? First, the trend of mean sensitivity, with a p-value, remains a sound default. It kept its nominal false-alarm rate and was not beaten by a valid detector. Second, a fast-rate rule without a p-value (D2) had the largest point gain among valid detectors with three tests. But in the external clinic, the same rule raised false positives significantly. Third, before adopting a new detector, a clinic can run a shuffle audit on its own records. In our data the audit caught the largest problems. However, it over-estimated false alarms for rate and event rules and agreed only moderately overall. It is a screen, not a replacement for true no-change data.

For method developers, we suggest three reporting items. Report false alarms on true no-change series, not only specificity on stable eyes. Report sensitivity at a fixed, small number of tests. Report results from a second clinic with its own labels. Our code and data pipeline are open, so new detectors can be added and compared on the same terms.

This study has limitations. First, the reference groups were small ({{c.uw_test_ref_prog}} progressors and {{c.uw_test_ref_stable}} stable eyes), so CIs were wide. We cannot exclude gains of 10–20 percentage points for some valid detectors, such as D2 at three tests and D8 at six tests. Second, the true no-change arm had only {{c.artes_patients}} patients, tested a week apart. We gave each series the test dates of a clinic eye, which keeps it a valid null but does not reproduce long-term changes in noise, such as cataract or learning. Third, the primary reference is based on mean deviation, which may favour detectors based on mean sensitivity; the PoPLR-based secondary reference gave the same ranking. Fourth, reference-stable eyes were chosen for a very flat course, which makes specificity look better than in typical stable eyes; we regard this as a finding, but it also means our specificity estimates are optimistic. Fifth, UWHVF has no reliability indices or diagnoses, and GRAPE uses a different perimeter, so several detectors had to be re-calibrated or omitted there. Sixth, we re-implemented event analysis and did not test commercial software. Seventh, the machine-learning models used a fixed tuning budget; larger models or other thresholds may behave differently. Finally, we used the Artes data once during development, which we disclose; it did not change the final protocol.

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

All data sets are public: UWHVF (https://github.com/uw-biomedical-ml/uwhvf), GRAPE (Figshare file 41670009, "VF and clinical information.xlsx", described in [@15]) and the Artes retest data (visualFields R package 1.0.7, CRAN). The analysis code, pre-registered protocol, raw per-eye detector outputs and all result files are available from [CODE REPOSITORY URL TO BE ADDED ON SUBMISSION].

# References

{{REFERENCES}}

# Tables

{{TABLE1}}

{{TABLE2}}

{{TABLE3}}
