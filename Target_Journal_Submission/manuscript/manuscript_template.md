# Shuffle Calibration Controls False Alarms of Glaucoma Visual Field Progression Detectors: A Benchmark With a True No-Change Arm

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, AFFILIATIONS, ADDRESSES AND ORCID iDs — TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — TO BE COMPLETED]

**Prior presentation:** None. [AUTHORS TO CONFIRM]

## Abstract

**Introduction:** New detectors claim to find glaucomatous visual field progression earlier, which would allow earlier treatment escalation, but their false alarms are rarely measured on data without change, and clinics lack a simple way to set a detector's threshold safely.

**Methods:** In this retrospective benchmark of public data, ten detectors (trend, event, permutation, conformal, machine learning) saw the first 3–6 fields of each series. We measured sensitivity against a future-confirmed reference (University of Washington; {{n_prog}} progressing and {{n_stab}} stable held-out eyes; {{en_np}} and {{en_ns}} eyes for training-free detectors), false-alarm rates on true no-change series ({{n_artes}} patients, 12 fields at about weekly intervals) and external performance (China, {{n_grape_eyes}} eyes, different perimeter). In a pre-specified amendment, thresholds were reset to a 5% flag rate on shuffled series of the clinic's own records ("shuffle calibration").

**Results:** With three fields, a pooled-detrended conformal test and a machine-learning model flagged more progressors than the trend test ({{s_D6_3}}% and {{s_D8_3}}% versus {{s_D1_3}}%) but raised false alarms in {{f_D6_3}}% and {{f_D8_3}}% of no-change series; specificity in reference-stable eyes ({{sp_D6_3}}%, {{sp_D8_3}}%) missed this. Shuffle calibration removed every clear excess (machine learning: {{f_D8_3}}% to {{xf_D8_3}}%; external specificity {{gp_D8_3}}% to {{xgp_D8_3}}%), and the sensitivity gains disappeared: no calibrated detector was significantly more sensitive than the trend test. In {{en_np}} progressors, the MD rate rule flagged {{endS_D2_3}} points more than the trend test but also {{endF_D2_3}} points more stable eyes.

**Conclusion:** The apparent early-detection gains were false alarms. Calibrating a detector on a clinic's own shuffled fields is a simple way to keep false alarms near the nominal level, including after transfer to another perimeter, without retest data. With few fields, every method missed most progressing eyes.

**Keywords:** Calibration; False alarms; Glaucoma; Machine learning; Perimetry; Progression detection; Visual field

## Plain Language Summary

Glaucoma damages the nerve at the back of the eye and slowly narrows side vision. Doctors check this with a visual field test, in which the patient presses a button when they see small lights. If results get worse over time, the doctor may step up treatment with more eye drops, laser or surgery. Results vary from visit to visit, so several tests are needed to be sure that vision is really getting worse. Many new computer methods claim to spot worsening sooner. We tested ten methods on public data from the USA, Canada and China, including patients tested every week for 12 weeks, whose eyes could not really have changed. Some methods that seemed to find worsening sooner raised false alarms for about one in four of these unchanged patients, and the usual checks did not show this. We then tried a simple fix: each clinic jumbles the order of its own patients' past tests, which removes any real worsening, and sets the method's alarm level so that it rarely fires on the jumbled tests. This removed the excess false alarms, also in a clinic using a different machine, but the apparent advantage of the new methods then disappeared. With only three tests, every method missed most eyes that were really getting worse, so "no change" after a few tests is not reassurance. Testing more often early on is likely to help more than a more complicated method.

## Key Summary Points

**Why carry out this study?**

- Glaucoma treatment is escalated when visual field tests show progression, and new detectors claim to find progression earlier, but most are judged by how many eyes they flag rather than by how many of those flags are false.

- We asked whether any of ten detectors flags future-confirmed progression from three to six fields more often than a simple trend test while keeping false alarms on true no-change data near 5%, and whether setting thresholds on a clinic's own shuffled fields controls false alarms.

**What was learned from the study?**

- With three fields, the detectors that gained most over the trend test raised false alarms in {{f_D6_3}}% and {{f_D8_3}}% of series without change, which specificity in reference-stable eyes did not reveal.

- Shuffle calibration brought every detector's false-alarm rate close to 5%, also on another perimeter, and once false alarms were controlled no detector was significantly more sensitive than the simple trend test.

- With few fields, every method missed most progressing eyes; new detectors should be reported with true no-change false-alarm rates and calibrated on the clinic's own data before their flags guide escalation.

<<INTRO_METHODS>>

# Results

## Study data

Table 1 summarises the data sets. Of {{n_test8}} UWHVF test eyes with at least eight fields, {{n_prog}} were reference progressors, {{n_stab}} stable and {{n_indet}} indeterminate; the {{n_prog}} + {{n_stab}} reference eyes came from {{n_ref_pat}} patients, had a median baseline mean deviation of {{ref_md}} dB (interquartile range [IQR] {{ref_md_iqr}}) and were followed for a median of {{ref_fu}} years. Their first six fields were a median of {{ref_int}} years apart, so six fields took a median of {{ref_t6}} years. Across all splits, {{en_np}} progressors and {{en_ns}} stable eyes formed the enlarged reference. The true no-change arm gave {{artes_win_3}} to {{artes_win_6}} windows of three to six fields, and {{grape_md}} of {{n_grape_eyes}} GRAPE eyes ({{grape_md_pct}}%) carried the MD label.

{{TABLE1}}

**Table 1.** Data sets. IQR, interquartile range; MD, mean deviation; PLR2/PLR3, pointwise linear regression criteria with at least two or three progressing locations.

## False alarms with nominal thresholds (RQ1, RQ4)

The trend test (D1) had false-alarm rates close to 5% at every number of fields ({{f_D1_3}}%, {{f_D1_4}}%, {{f_D1_5}}% and {{f_D1_6}}% with three to six fields; Table 2, Fig. 2), and the pooled-shuffle conformal test (D5) behaved almost identically. False alarms were clearly above 5% for {{excess_list}}: with three fields, {{f_D6_3}}% (95% CI {{fci_D6_3}}) for D6, {{f_D8_3}}% ({{fci_D8_3}}) for D8 and {{f_D9_3}}% ({{fci_D9_3}}) for D9. D6's excess had been seen during development; D8 and D9 had not been run on these data before. The machine-learning models exceeded 5% clearly in {{ml_cells_above5}} of {{ml_cells}} combinations (H4 supported). Specificity in reference-stable eyes did not reveal these false alarms: with three fields it was {{sp_D1_3}}% for D1, {{sp_D6_3}}% for D6 and {{sp_D8_3}}% for D8.

Under the strictest rule (upper limit at most 5%), {{n_cells_strict}} of {{n_cells}} combinations qualified and D1 never did (upper limits {{D1_hi_range}}%), because {{n_artes}} patients cannot show a rate near 5% to be below 5%. In practical terms, among 1,000 stable eyes reviewed once with three fields, D1 would raise about {{ff_D1_3}} false flags, D6 about {{ff_D6_3}} and D8 about {{ff_D8_3}}; reviewed at three to six fields in turn, {{cum_D1}}% of no-change series received at least one false D1 flag, against {{cum_D6}}% for D6 and {{cum_D8}}% for D8 (post hoc). PoPLR (D4) and the order network (D10) cannot flag with three fields, because three fields have only six orders (smallest p-value 1/6), and event analysis (D7) needs two follow-up fields.

{{TABLE2}}

**Table 2.** Sensitivity against the future-confirmed reference (%) / false-alarm rate on true no-change series (%), with nominal thresholds. † Not valid (95% CI upper limit above 10% or lower limit above 5%). Reference: {{n_prog}} progressing and {{n_stab}} stable eyes; true no-change: {{artes_win_6}}–{{artes_win_3}} windows from {{n_artes}} patients, ten time-scale draws each. CIs are in Supplementary Table S1.

## Sensitivity with nominal thresholds (RQ2)

No detector with a valid false-alarm rate was significantly more sensitive than D1 at any number of fields, so H2 {{h2_falsified}}; with {{n_prog}} progressors, however, gains of up to {{max_gain_hi}} points were within the CIs. The only nominally significant gain was D6 with three fields ({{dSa_D6_3}} points, 95% CI {{dSci_D6_3}}; adjusted p {{dSp_D6_3}} within three fields and {{dSpall_D6_3}} across all numbers of fields), at a false-alarm rate of {{f_D6_3}}%. D1 flagged {{by6_D1}}% of progressors by the sixth field (median {{tfd_D1}} fields to the first flag); D6 and D8 flagged earlier (median {{tfd_D6}} and {{tfd_D8}} fields) at the false-alarm cost above. With the secondary PoPLR-based reference and the post-hoc later-field reference, sensitivities were lower and the pattern was similar (Supplementary Tables S1, S4, S5).

## Shuffle calibration (RQ6)

Shuffle calibration removed every clear excess of false alarms (H5 {{H5}}; Fig. 5, Supplementary Table S6). With three fields, the false-alarm rate fell from {{f_D6_3}}% to {{xf_D6_3}}% (95% CI {{xfci_D6_3}}) for D6, from {{f_D8_3}}% to {{xf_D8_3}}% ({{xfci_D8_3}}) for D8 and from {{f_D9_3}}% to {{xf_D9_3}}% ({{xfci_D9_3}}) for D9; {{x_nvalid}} of {{x_ncells}} calibrated combinations were valid (exception: {{x_invalid_list}}, upper limit just above 10%). For D2, whose nominal threshold had a low false-alarm rate on the no-change series but many flags in shuffled clinic series, calibration raised the threshold and its false-alarm rate fell to {{xf_D2_3}}%.

The sensitivity gains disappeared with the false alarms. With three fields, calibrated D6 flagged {{xs_D6_3}}% and calibrated D8 {{xs_D8_3}}% of progressors, against {{s_D1_3}}% for D1 (differences {{xdS_D6_3}} and {{xdS_D8_3}} points; adjusted p values {{xdSpn_D6_3}} and {{xdSpn_D8_3}}). With six fields, calibrated D8 flagged {{xs_D8_6}}% with {{xf_D8_6}}% false alarms against {{s_D1_6}}% for D1 ({{xdS_D8_6}} points, 95% CI {{xdSci_D8_6}}; adjusted p {{xdSp_D8_6}}). No calibrated detector was significantly more sensitive than D1 (H6 {{H6}}).

In GRAPE, own-clinic calibration restored specificity with three fields from {{gp_D8_3}}% to {{xgp_D8_3}}% (95% CI {{xgpci_D8_3}}) for D8 and from {{gp_D2_3}}% to {{xgp_D2_3}}% for D2, matching D1 ({{gp_D1_3}}%); sensitivity against the MD label fell to {{xgs_D8_3}}% and {{xgs_D2_3}}%, below D1 ({{gs_D1_3}}%), whose result is close to circular for this label (D1 flagged {{g3_f}} of {{g3_n}} labelled progressors among eyes with exactly three visits and {{g4_f}} of {{g4_n}} among eyes with more).

## Confirmation and enlarged reference (A3)

Requiring a flag to be confirmed on the next field also controlled false alarms (H7): with four, five and six fields, confirmed D8 flagged {{cff_D8_4}}%, {{cff_D8_5}}% and {{cff_D8_6}}% of no-change series and confirmed D6 {{cff_D6_4}}%, {{cff_D6_5}}% and {{cff_D6_6}}%. Confirmation cost sensitivity: with six fields, confirmed D8 flagged {{cfs_D8_6}}% and confirmed D1 {{cfs_D1_6}}% of progressors, against {{s_D1_6}}% for unconfirmed D1 (Supplementary Table S7).

In the enlarged reference ({{en_np}} progressors, {{en_ns}} stable eyes), D1 flagged {{ens_D1_3}}% ({{ensci_D1_3}}), {{ens_D1_4}}%, {{ens_D1_5}}% and {{ens_D1_6}}% of progressors with three to six fields. With three fields, the MD rate rule (D2) flagged {{endS_D2_3}} points more progressors than D1 (95% CI {{endSci_D2_3}}; adjusted p {{endSp_D2_3}}; H8 {{H8}}) but also {{endF_D2_3}} points more stable eyes ({{endFci_D2_3}}; adjusted p {{endFp_D2_3}}), and it was less sensitive than D1 from four fields on. PLR-3 (D3) and PoPLR (D4) were less sensitive than D1 with three to five fields (Supplementary Table S8).

## Shuffle audit and external data (RQ3, RQ5)

The shuffle audit's false-alarm estimate correlated with the true rate (Spearman ρ = {{rq3_rho}}, 95% CI {{rq3_lo}}–{{rq3_hi}}; {{rq3_within3}}% of combinations within 3 points; Fig. 3), below the pre-specified 0.7, so H3 was not met. It identified {{aud_det}} of {{aud_inv}} invalid combinations (missed: {{aud_missed}}) but gave false warnings for {{aud_fw}} of {{aud_nv}} valid ones, mostly rules without a p-value. With nominal thresholds in GRAPE (Table 3, Fig. 4), D8 transferred from UWHVF flagged more labelled progressors than D1 ({{gs_D8_3}}% versus {{gs_D1_3}}%) but {{dGFa_D8_3}} points more non-progressing eyes (95% CI {{dGFci_D8_3}}); at the GRAPE prevalence of {{grape_prev}}%, {{ppvg_D1_3}}% of D1 flags and {{ppvg_D8_3}}% of D8 flags were labelled progression.

{{TABLE3}}

**Table 3.** External data set (GRAPE), nominal thresholds: sensitivity and specificity (%, 95% CI) against the MD label, first three or four fields ({{g_np_3}} labelled progressors and {{g_ns_3}} non-progressors with at least three fields; {{g_np_4}} and {{g_ns_4}} with at least four). D6, D9 and D10 require the 24-2 pattern and were not applied.

# Discussion

We compared ten detectors of glaucomatous visual field progression on a question that matters for treatment decisions: how early can progression be flagged without raising false alarms? With nominal thresholds, the detectors that gained most over the trend test with three fields did so by flagging more of everything, and specificity measured in reference-stable eyes did not show this. When each detector's threshold was reset on shuffled copies of the clinic's own series, the excess false alarms disappeared, and so did the gains in sensitivity. This is direct evidence that the apparent early-detection gains were false alarms: once every detector worked at the same false-alarm rate, none was significantly more sensitive than the trend test of mean sensitivity.

The mechanism differs between detectors. Our pooled-detrended test borrowed its null distribution from other patients' detrended series [30, 31]; with three fields, detrending leaves one residual degree of freedom, and the borrowed distribution was probably too narrow. The machine-learning models were trained to predict future progression and thresholded in reference-stable eyes, which tend to be eyes whose early fields also looked stable, so the threshold was optimistic; they also partly predict risk, because features such as the level of mean sensitivity raise their output in an eye that is not changing. The MD rate rule has no p-value, so its false-alarm rate depends on the spacing and noise of a clinic's fields. Shuffle calibration addresses all three in the same way: shuffling destroys any trend but keeps each eye's level, spread and test dates, so the calibrated threshold reflects how the detector behaves on stable eyes like the clinic's own. Within-eye permutation (PoPLR) uses the same idea for a single eye [6] but cannot reach p < 0.05 with three fields; pooling shuffles across a clinic's eyes, as in conformal inference [31] and the classification permutation test [33], lifts this floor and applies to any score, including a machine-learning output. To our knowledge, based on our searches of OpenAlex, PubMed, Europe PMC, Crossref and preprint servers (November 2026), this has not been used to set the thresholds of visual field progression detectors.

Calibration is practical. A clinic needs only its own past fields (no retest series), the detector's score, and the ability to run the detector outside the perimeter software: shuffle the order of each eye's first k fields, score the shuffled series and set the threshold at the 95th percentile. In GRAPE, this restored the specificity of a model trained on another perimeter and population from {{gp_D8_3}}% to {{xgp_D8_3}}% without any labels. Calibration controls false alarms; it does not add information, and it cannot make a detector more sensitive than the data allow. The simpler alternative, confirming a flag on the next field, also controlled false alarms but cost sensitivity and time. Shuffle-based auditing alone, without recalibration, was less useful: it raised false warnings for several valid rules.

For clinical practice, the main limit to earlier detection is the number and spacing of fields, not the detector. In UWHVF, fields were a median of {{ref_int}} years apart; with three fields the trend test flagged only {{s_D1_3}}% of eyes that later progressed (and {{ens_D1_3}}% in the enlarged reference), and it needed a median of {{tfd_D1}} fields to flag a progressor. A "no progression" result after a few fields is therefore not reassurance. This agrees with earlier work showing that routine testing frequencies delay the identification of progression [25–27]. Testing more often early in follow-up [4], clustering tests [28], personalised schedules [23, 34] or smoothing [36] address the amount of information directly, and our results suggest that earlier detection is more likely to come from such strategies than from a more complex detector applied to the same sparse fields. A flag from a detector that has not been shown to have an acceptable false-alarm rate on true no-change data, or calibrated on the clinic's own fields, should not by itself trigger escalation of treatment.

This study has limitations. The held-out reference was small ({{n_prog}} progressing and {{n_stab}} stable eyes) and limited to clear-cut eyes, so moderate gains of learned detectors cannot be excluded; the enlarged reference ({{en_np}} and {{en_ns}} eyes) could be used only for training-free detectors. The primary reference uses a mean-deviation slope over a series that includes the fields the detectors see, which may favour the trend test; the secondary and later-field references reduce but do not remove this concern. The true no-change arm included only {{n_artes}} patients retested over a few weeks; it lacks long-term fluctuation, so real-world false-alarm rates are probably higher for all detectors, and we assigned clinical test intervals to these series. D6's behaviour on these data was known from development, and amendment A3 was added after an internal review of the first results, although before its analyses were run. Our machine-learning models were not replicas of published systems [16–21]. UWHVF has no diagnoses, treatment or reliability indices, so flags could not be linked to treatment decisions or outcomes. GRAPE used a different perimeter, its labels are rule-based criteria computed on short series that overlap with the detectors' input, and its patients were younger (median age {{grape_age}} versus {{ref_age}} years); its results test transfer and specificity, not independent accuracy.

# Conclusion

In this benchmark, the apparent gains of newer detectors in early detection of glaucomatous visual field progression were explained by false alarms. Setting each detector's threshold on shuffled copies of a clinic's own fields kept false alarms near the nominal level, also after transfer to another perimeter, and after this no detector was significantly more sensitive than a simple trend test, which was well calibrated but slow. New detectors should be reported with false-alarm rates on true no-change data and calibrated on local data before their flags guide escalation of treatment.

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

{{REFERENCES}}

# Supplementary Material

Supplementary Table S1: all metrics with 95% confidence intervals (sensitivity, specificity, true no-change and shuffle-audit false-alarm rates, secondary-reference sensitivity, GRAPE results) for every detector and number of fields. Supplementary Table S2: paired comparisons with D1 (difference, bootstrap 95% CI, exact McNemar p, Holm-adjusted p). Supplementary Table S3: fields to first flag among reference progressors, by detector (seed means). Supplementary Tables S4 and S5 (post hoc): sensitivity, specificity and paired tests against the reference computed only from fields after the first k. Supplementary Tables S6–S8 (amendment A3): shuffle calibration (false-alarm rates, sensitivity, specificity, paired tests, GRAPE), confirmation, and the enlarged reference for training-free detectors. Supplementary Note S1: development history, including abandoned method ideas.
