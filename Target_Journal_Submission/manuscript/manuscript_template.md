# False Progression Flags and Treatment Escalation in Glaucoma: Benchmarking Visual Field Detectors and Calibrating Them on a Clinic's Own Data

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, AFFILIATIONS, ADDRESSES AND ORCID iDs — TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — TO BE COMPLETED]

**Prior presentation:** None. [AUTHORS TO CONFIRM]

## Abstract

**Introduction:** Treatment of glaucoma is escalated when visual fields show progression. New detectors claim earlier detection, but their false alarms are rarely measured on data without change, and clinics lack a simple way to set a detector's threshold safely.

**Methods:** In this retrospective benchmark of public data, ten detectors (trend, event, permutation, conformal, machine learning) saw the first 3–6 fields of each series (three fields spanned a median of {{ref_t3}} years in the US clinic). We measured sensitivity against a future-confirmed reference ({{n_prog}} progressing, {{n_stab}} stable held-out eyes), false alarms on true no-change series ({{n_artes}} patients retested about weekly) and transfer to a Chinese clinic ({{n_grape_eyes}} eyes, different perimeter). In an exploratory amendment, thresholds were reset to a 5% flag rate on shuffled series of the clinic's own records.

**Results:** With three fields, gradient-boosted trees thresholded at 95% specificity in reference-stable eyes flagged {{s_D8_3}}% of progressors versus {{s_D1_3}}% for the trend test, but raised false alarms in {{f_D8_3}}% of no-change series (trend test {{f_D1_3}}%); specificity in reference-stable eyes ({{sp_D8_3}}%) did not reveal this. No detector with an acceptable false-alarm rate was significantly more sensitive than the trend test, although gains up to about {{max_gain_hi}} points could not be excluded. Shuffle calibration brought every clear excess down (gradient-boosted trees: {{f_D8_3}}% to {{xf_D8_3}}%; external specificity {{gp_D8_3}}% to {{xgp_D8_3}}%), but at a cost: no calibrated detector was more sensitive than the trend test, and external sensitivity fell to {{xgs_D8_3}}% (trend test {{gs_D1_3}}%).

**Conclusion:** The largest apparent early-detection gains came with excess false alarms, and controlling false alarms removed them. Detectors should be reported with false-alarm rates on true no-change data and checked on local data before their flags guide escalation. With few fields, every method missed most progressing eyes.

**Keywords:** Calibration; False alarms; Glaucoma; Machine learning; Perimetry; Treatment escalation; Visual field

## Plain Language Summary

Glaucoma damages the nerve at the back of the eye and slowly narrows side vision. Doctors check this with a visual field test, in which the patient presses a button when they see small lights. If results get worse, the doctor may step up treatment with more eye drops, laser or surgery. Results vary from visit to visit, so several tests are needed to be sure that vision is really getting worse. New computer methods claim to spot worsening sooner. We tested ten methods on public data from the USA, Canada and China, including patients tested about once a week for about three months, whose eyes could not really have changed. One machine-learning method that seemed to spot worsening sooner raised false alarms in more than one in four of these unchanged test series, and the usual checks did not show this. We then tried a simple fix: a clinic jumbles the order of its own patients' past tests, which removes any real worsening, and sets the method's alarm level so that it rarely fires on the jumbled tests. This removed most extra false alarms, also in a clinic using a different machine, but the apparent advantage of the new methods disappeared. With only three tests, which took more than two years in routine care, every method missed most eyes that were really getting worse, so "no change" after a few tests is not reassurance.

## Key Summary Points

**Why carry out this study?**

- Glaucoma treatment is escalated when visual fields show progression, and new detectors claim to find it earlier, but they are usually judged by how many eyes they flag rather than by how many of those flags are false.

- We asked how often ten detectors raise false progression flags on true no-change data with three to six fields, whether any flags more truly progressing eyes than a simple trend test while keeping false alarms near 5%, and whether thresholds set on a clinic's own shuffled fields control false alarms.

**What was learned from the study?**

- With three fields, a machine-learning detector flagged more progressing eyes than the trend test ({{s_D8_3}}% versus {{s_D1_3}}%) but raised false alarms in {{f_D8_3}}% of series without change, which specificity in reference-stable eyes did not reveal.

- Shuffle calibration reduced false alarms close to 5%, also on another perimeter, but no calibrated detector was more sensitive than the trend test, and external sensitivity fell.

- With few fields every method missed most progressing eyes; new detectors should be reported with true no-change false-alarm rates and checked on local data before their flags guide escalation.

<<INTRO_METHODS>>

# Results

## Study data

Table 1 summarises the data sets. Of {{n_test8}} UWHVF test eyes with at least eight fields, {{n_prog}} were reference progressors, {{n_stab}} stable and {{n_indet}} indeterminate; the reference eyes came from {{n_ref_pat}} patients, had a median baseline mean deviation of {{ref_md}} dB (interquartile range [IQR] {{ref_md_iqr}}) and were followed for a median of {{ref_fu}} years, with fields a median of {{ref_int}} years apart. Across all splits, {{en_np}} progressors and {{en_ns}} stable eyes formed the enlarged reference. The no-change arm gave {{artes_win_3}} to {{artes_win_6}} windows of three to six fields, and {{grape_md}} of {{n_grape_eyes}} GRAPE eyes ({{grape_md_pct}}%) carried the MD label.

{{TABLE1}}

**Table 1.** Data sets. IQR, interquartile range; MD, mean deviation; PLR2/PLR3, pointwise linear regression criteria with at least two or three progressing locations.

## False alarms and sensitivity with nominal thresholds

The trend test kept false alarms close to 5% at every number of fields ({{f_D1_3}}%, {{f_D1_4}}%, {{f_D1_5}}% and {{f_D1_6}}% with three to six fields; Table 2, Fig. 2), and the pooled conformal test behaved almost identically. False-alarm rates were invalid in {{n_cells_invalid}} of {{n_cells}} detector–field-number combinations (Table 2). The gradient-boosted trees had {{f_D8_3}}% false alarms with three fields (95% CI {{fci_D8_3}}), and the two machine-learning detectors were invalid in {{ml_invalid}} of {{ml_cells}} combinations, as hypothesised. The detrended conformal test had {{f_D6_3}}% ({{fci_D6_3}}), as already seen during development. Specificity in reference-stable eyes did not reveal these false alarms: with three fields it was {{sp_D1_3}}% for the trend test, {{sp_D8_3}}% for the gradient-boosted trees and {{sp_D6_3}}% for the detrended conformal test. Under the strictest rule (upper CI limit at most 5%), even the trend test never qualified (upper limits {{D1_hi_range}}%), because {{n_artes}} patients cannot show a rate near 5% to be below 5%.

No detector with a valid false-alarm rate was significantly more sensitive than the trend test at any number of fields, so our hypothesis {{h2_falsified}}. This is not evidence of equivalence: with {{n_prog}} progressors, gains up to {{max_gain_hi}} points were within the CIs. With three fields, the MD-rate rule flagged {{s_D2_3}}% versus {{s_D1_3}}% at a valid false-alarm rate of {{f_D2_3}}% ({{dSa_D2_3}} points, 95% CI {{dSci_D2_3}}; adjusted p {{dSp_D2_3}}). With six fields, the gradient-boosted trees flagged {{s_D8_6}}% versus {{s_D1_6}}% ({{dSa_D8_6}} points, {{dSci_D8_6}}; adjusted p {{dSp_D8_6}}). The only nominally significant gain was the detrended conformal test with three fields ({{dSa_D6_3}} points; adjusted p {{dSp_D6_3}} within three fields and {{dSpall_D6_3}} across all numbers of fields), whose false-alarm rate was invalid. Secondary and later-field references gave lower sensitivities and a similar pattern (Supplementary Tables S1, S4, S5).

{{TABLE2}}

**Table 2.** Sensitivity against the future-confirmed reference (%) / false-alarm rate on true no-change series (%), nominal thresholds. † Not valid (95% CI upper limit above 10% or lower limit above 5%). Reference: {{n_prog}} progressing and {{n_stab}} stable eyes; no-change: {{artes_win_6}}–{{artes_win_3}} windows from {{n_artes}} patients, ten time-scale draws each. PoPLR and the order network cannot flag with three fields (six possible orders, smallest p-value 1/6); event analysis needs four. CIs in Supplementary Table S1.

## What the flags mean for escalation decisions

Table 3 translates the results into clinical terms. With three fields, among 1,000 stable eyes reviewed once, the trend test would raise about {{ff_D1_3}} false progression flags and the gradient-boosted trees about {{ff_D8_3}}; at 10% prevalence, {{ppv10_D1_3}}% of trend-test flags and {{ppv10_D8_3}}% of gradient-boosted-tree flags would be true progression (MD-rate rule {{ppv10_D2_3}}%). Reviewed at three, four, five and six fields in turn, {{cum_D1}}% of no-change series received at least one false trend-test flag, against {{cum_D8}}% for the gradient-boosted trees. The trend test flagged {{by6_D1}}% of progressors at one or more of fields 3–6 (median {{tfd_D1}} fields to the first flag, several years at this clinic's spacing).

{{TABLE_CLIN}}

**Table 3.** Clinical implications (UWHVF reference and true no-change arm). Share of flags that are true progression assumes 10% prevalence. Cumulative columns count a flag at any review with three, four, five or six fields. Shuffle-calibrated rows: amendment A3 (exploratory).

## Calibrating thresholds on the clinic's own shuffled fields (exploratory)

Shuffle calibration removed every clear excess of false alarms (Fig. 4; Supplementary Table S6). With three fields, the false-alarm rate fell from {{f_D8_3}}% to {{xf_D8_3}}% (95% CI {{xfci_D8_3}}) for the gradient-boosted trees, from {{f_D9_3}}% to {{xf_D9_3}}% for the recurrent network and from {{f_D6_3}}% to {{xf_D6_3}}% for the detrended conformal test; {{x_nvalid}} of {{x_ncells}} calibrated combinations were valid (exception: {{x_invalid_list}}, upper limit just above 10%). For the MD-rate rule, calibration was over-conservative ({{xf_D2_3}}% false alarms, {{xs_D2_3}}% sensitivity), probably because shuffled clinic series contain more long-term fluctuation than the weekly retest series.

Once false alarms were controlled, no detector was more sensitive than the trend test. With three fields, the calibrated gradient-boosted trees flagged {{xs_D8_3}}% of progressors (trend test {{s_D1_3}}%); with six fields, {{xs_D8_6}}% at {{xf_D8_6}}% false alarms versus {{s_D1_6}}% ({{xdS_D8_6}} points, 95% CI {{xdSci_D8_6}}; adjusted p {{xdSp_D8_6}}). In GRAPE, own-clinic calibration restored the specificity of the transferred gradient-boosted trees from {{gp_D8_3}}% to {{xgp_D8_3}}% (95% CI {{xgpci_D8_3}}), matching the trend test ({{gp_D1_3}}%), but their sensitivity against the MD label fell to {{xgs_D8_3}}% versus {{gs_D1_3}}% for the trend test ({{xdGSa_D8_3}} points lower; adjusted p {{xdGSp_D8_3}}). The trend test's GRAPE result is partly circular, because the MD label is itself a slope test of a short series (it flagged {{g3_f}} of {{g3_n}} labelled progressors among eyes with exactly three visits and {{g4_f}} of {{g4_n}} among eyes with more; Supplementary Table S9).

Requiring a flag to be confirmed on the next field also controlled false alarms (gradient-boosted trees {{cff_D8_4}}%–{{cff_D8_6}}%, detrended conformal test {{cff_D6_4}}%–{{cff_D6_6}}% with four to six fields) but cost sensitivity (confirmed trend test {{cfs_D1_6}}% versus {{s_D1_6}}% unconfirmed with six fields; Supplementary Table S7). In the enlarged reference ({{en_np}} progressors, {{en_ns}} stable eyes), the MD-rate rule flagged {{endS_D2_3}} points more progressors than the trend test with three fields (95% CI {{endSci_D2_3}}; adjusted p {{endSp_D2_3}}) but also {{endF_D2_3}} points more stable eyes (adjusted p {{endFp_D2_3}}), and PLR-3 and PoPLR were less sensitive than the trend test with three to five fields (Supplementary Table S8). A shuffle audit without recalibration identified {{aud_det}} of {{aud_inv}} invalid combinations but gave false warnings for {{aud_fw}} of {{aud_nv}} valid ones (Spearman ρ with the true rate {{rq3_rho}}, below the pre-specified 0.7; Supplementary Fig. S1).

# Discussion

We compared ten detectors of glaucomatous visual field progression on a question that matters for treatment decisions: how early can progression be flagged without raising false alarms? With nominal thresholds, the detectors that gained most over the trend test with three fields also flagged many series without change, and specificity measured in reference-stable eyes did not show this. When each detector's threshold was reset on shuffled copies of the clinic's own series, the excess false alarms largely disappeared, and so did the gains in sensitivity. This supports the view that most of the apparent early-detection advantage came from a more permissive threshold rather than from more information. It does not prove equivalence: our held-out reference was small, and one valid rule (the MD-rate rule) showed a non-significant gain with nominal thresholds.

The mechanisms differ. The detrended conformal test borrowed its null distribution from other patients' detrended series; with three fields, detrending leaves one residual degree of freedom, and the borrowed distribution was probably too narrow. The machine-learning models were trained to predict future progression and thresholded in reference-stable eyes, which tend to be eyes whose early fields also looked stable; they also partly predict risk, so features such as the level of mean sensitivity raise their output in an eye that is not changing. Shuffle calibration addresses both in the same way: shuffling destroys any trend but keeps each eye's level, spread and test dates, so the threshold reflects how the detector behaves on stable eyes like the clinic's own. Within-eye permutation (PoPLR) uses the same idea for one eye [6] but cannot reach p < 0.05 with three fields; pooling shuffles across a clinic's eyes, by analogy with conformal inference [31] and the classification permutation test [33], applies to any score, including a machine-learning output. To our knowledge, based on searches of OpenAlex, PubMed, Europe PMC, Crossref and preprint servers (November 2026), this has not been used to set the thresholds of visual field progression detectors.

Calibration needs only a clinic's past fields and the ability to run the detector outside the perimeter software, with no retest series and no labels. In GRAPE it restored the specificity of a model trained on another perimeter and population. Its cost is equally clear: it does not add information, it lowered sensitivity, and it was over-conservative for a rule without a p-value. It is therefore a safety check that makes detectors comparable at a stated false-alarm rate, not a way to detect progression earlier. Confirming flags on the next field is a simpler alternative that also controls false alarms, at the cost of one more field.

For clinical practice, the main limit to earlier detection is the number and spacing of fields, not the detector. In UWHVF, three fields took a median of {{ref_t3}} years; with three fields the trend test flagged only {{s_D1_3}}% of eyes that later progressed ({{ens_D1_3}}% in the enlarged reference). A "no progression" result after a few fields is therefore not reassurance. This agrees with work showing that routine testing frequencies delay the identification of progression [25–27]. Testing more often early in follow-up [4], clustering tests [28], personalised schedules [23, 34] or smoothing [36] address the amount of information directly and are more likely to bring detection forward than a more complex detector applied to the same sparse fields. A flag from a detector whose false-alarm rate has not been shown to be acceptable on true no-change or locally shuffled data should not by itself trigger escalation of treatment.

This study has limitations. The held-out reference was small and limited to clear-cut eyes; the enlarged reference could be used only for training-free detectors. The primary reference uses a mean-deviation slope over a series that includes the fields the detectors see, which may favour the trend test. The no-change arm included only {{n_artes}} patients retested over a few weeks, without long-term fluctuation, so real-world false-alarm rates are probably higher for all detectors. The detrended conformal test's behaviour on these data was known from development, and the calibration analyses were exploratory, added after an internal review. Our machine-learning models were not replicas of published systems [16–21]. UWHVF has no diagnoses, treatment or reliability indices, so flags could not be linked to treatment decisions or outcomes. GRAPE used a different perimeter, its labels are rule-based criteria computed on short series that overlap with the detectors' input, and its patients were younger (median age {{grape_age}} versus {{ref_age}} years).

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

{{REFERENCES}}

# Supplementary Material

Supplementary Table S1: all metrics with 95% confidence intervals (sensitivity, specificity, true no-change and shuffle-audit false-alarm rates, secondary-reference sensitivity, GRAPE results) for every detector and number of fields. Supplementary Table S2: paired comparisons with D1 (difference, bootstrap 95% CI, exact McNemar p, Holm-adjusted p). Supplementary Table S3: fields to first flag among reference progressors, by detector (seed means). Supplementary Tables S4 and S5 (post hoc): sensitivity, specificity and paired tests against the reference computed only from fields after the first k. Supplementary Tables S6–S8 (amendment A3, exploratory): shuffle calibration, confirmation, and the enlarged reference for training-free detectors. Supplementary Table S9: external data set (GRAPE) with nominal thresholds. Supplementary Fig. S1: shuffle audit versus true no-change false-alarm rate. Supplementary Note S1: development history, including abandoned method ideas.
