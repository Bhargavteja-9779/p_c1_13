# Detecting Glaucomatous Visual Field Progression From Few Tests Without False Alarms: A Benchmark With a True No-Change Arm

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, AFFILIATIONS, ADDRESSES AND ORCID iDs — TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — TO BE COMPLETED]

**Prior presentation:** None. [AUTHORS TO CONFIRM]

## Abstract

**Introduction:** Many new detectors claim to find glaucomatous visual field progression earlier, which would allow earlier treatment escalation, but their false-alarm rates are rarely measured on data without change. We asked how early progression can be detected from the first three to six fields without excess false alarms.

**Methods:** In this retrospective benchmark, ten detectors (trend, event, permutation, conformal, machine learning) saw the first 3–6 fields of each series. We measured sensitivity against a future-confirmed reference in held-out University of Washington eyes ({{n_prog}} progressing, {{n_stab}} stable), false-alarm rates on true no-change series ({{n_artes}} patients, 12 fields at about weekly intervals), a "shuffle audit", and performance in an external data set from China ({{n_grape_eyes}} eyes, different perimeter).

**Results:** With three fields, the trend test of mean sensitivity flagged {{s_D1_3}}% of progressors with a false-alarm rate of {{f_D1_3}}% (95% CI {{fci_D1_3}}). A pooled-detrended conformal test flagged {{s_D6_3}}% but had {{f_D6_3}}% false alarms; gradient-boosted trees thresholded at 95% specificity had {{f_D8_3}}%. Specificity in reference-stable eyes ({{sp_D6_3}}% and {{sp_D8_3}}%) did not reveal this. In {{n_cells_excess}} of {{n_cells}} detector–field-number combinations, false alarms were clearly above 5%. No detector with acceptable false alarms flagged significantly more progressors than the trend test, but intervals were wide: gains of up to {{max_gain_hi}} percentage points could not be excluded. The shuffle audit was within 3 points of the true false-alarm rate in {{rq3_within3}}% of combinations (ρ = {{rq3_rho}}, below the pre-specified 0.7) and detected {{aud_det}} of {{aud_inv}} invalid combinations. Externally, the machine-learning detector had specificity {{gp_D8_3}}% versus {{gp_D1_3}}% for the trend test.

**Conclusion:** The largest apparent early-detection gains in this benchmark came with excess false alarms that specificity in reference-stable eyes missed. The trend test was well calibrated but slow, and with few fields every method missed most progressing eyes. Reports of new detectors should include false-alarm rates on true no-change data.

**Keywords:** Benchmarking; False alarms; Glaucoma; Machine learning; Perimetry; Progression detection; Visual field

## Plain Language Summary

Glaucoma damages the nerve at the back of the eye and slowly narrows side vision. Doctors check this with a visual field test, in which the patient presses a button when they see small lights. If the results get worse over time, the doctor may step up treatment with more eye drops, laser or surgery. The test results vary from visit to visit, so it takes several tests to be sure that vision is really getting worse. Many new computer methods claim to spot worsening sooner. We tested ten such methods on public data from the USA, Canada and China. Importantly, we also tested them on patients who were tested every week for 12 weeks, when their eyes could not really have changed, so any alarm from a method was a false alarm. Some methods that seemed to find worsening sooner raised false alarms for one in five to one in four of these unchanged patients, and the usual checks did not show this. No method with few false alarms did clearly better than the simple method already used in clinics, although our study was too small to rule out modest gains. With only three tests, every method missed most eyes that were really getting worse, so a "no change" result after a few tests is not reassurance that the eye is safe. Testing more often early on is likely to help more than a more complicated method. Anyone proposing a new method should show how often it raises false alarms in patients whose eyes are not changing.

## Key Summary Points

**Why carry out this study?**

- Glaucoma treatment is escalated when visual field tests show progression, and many new detectors claim to find progression earlier, but most are judged by how many eyes they flag rather than by how many of those flags are false.

- We asked whether any of ten detectors could flag future-confirmed progression from three to six fields more often than a simple trend test while keeping false alarms on true no-change data near the nominal 5%.

**What was learned from the study?**

- With three fields, a pooled-detrended conformal test and a machine-learning model raised false alarms in {{f_D6_3}}% and {{f_D8_3}}% of series without change, which specificity in reference-stable eyes did not reveal; no detector with acceptable false alarms was significantly better than the trend test, although the study could exclude only large gains.

- With three fields the trend test flagged only {{s_D1_3}}% of eyes that later progressed, so a "no progression" result after a few fields is not reassurance; more frequent early testing is a more promising route to earlier detection than a more complex detector.

- Reports of new progression detectors should include false-alarm rates on true no-change data; a shuffle audit of a clinic's own records is a cheap first check but also gives false warnings.

<<INTRO_METHODS>>

# Results

## Study data

Table 1 summarises the three data sets. The UWHVF test set contained {{n_test_eyes}} eyes of {{n_test_pat}} patients with at least three fields; {{n_test8}} had at least eight fields, of which {{n_prog}} were reference progressors, {{n_stab}} reference stable and {{n_indet}} indeterminate. The {{n_prog}} + {{n_stab}} reference eyes came from {{n_ref_pat}} patients, had a median baseline mean deviation of {{ref_md}} dB (interquartile range [IQR] {{ref_md_iqr}}) and were followed for a median of {{ref_fu}} years. Their first six fields were a median of {{ref_int}} years apart (IQR {{ref_int_iqr}}), so six fields took a median of {{ref_t6}} years. The true no-change arm gave {{artes_win_3}}, {{artes_win_4}}, {{artes_win_5}} and {{artes_win_6}} windows of three to six consecutive fields. In GRAPE, {{grape_md}} of {{n_grape_eyes}} eyes ({{grape_md_pct}}%) carried the MD progression label.

{{TABLE1}}

**Table 1.** Data sets. IQR, interquartile range; MD, mean deviation; PLR2/PLR3, pointwise linear regression criteria with at least two or three progressing locations.

## False alarms on true no-change data (RQ1 and RQ4)

Table 2 and Fig. 2 show sensitivity against the future reference together with the false-alarm rate on true no-change series. The trend test of mean sensitivity (D1) had false-alarm rates close to the nominal 5% at every number of fields ({{f_D1_3}}%, {{f_D1_4}}%, {{f_D1_5}}% and {{f_D1_6}}% for three to six fields). The pooled-shuffle conformal test (D5) behaved almost identically to D1.

False-alarm rates were clearly above 5% (lower confidence limit above 5%) for {{excess_list}}. With three fields these were {{f_D6_3}}% (95% CI {{fci_D6_3}}) for the pooled-detrended conformal test (D6), {{f_D8_3}}% ({{fci_D8_3}}) for the tabular machine-learning model (D8) and {{f_D9_3}}% ({{fci_D9_3}}) for the sequence model (D9). D6's excess was already known from development (Supplementary Note S1); D8 and D9 had not been evaluated on these data before. Thresholded at 95% specificity in reference-stable validation eyes, the machine-learning models had false-alarm rates clearly above 5% in {{ml_cells_above5}} of {{ml_cells}} combinations, supporting H4, and their rate changed erratically with the number of fields (D8: {{f_D8_3}}%, {{f_D8_4}}%, {{f_D8_5}}% and {{f_D8_6}}%). Under our primary rule, {{nvalid_3}}, {{nvalid_4}}, {{nvalid_5}} and {{nvalid_6}} of ten detectors had valid false-alarm rates with three, four, five and six fields. Under the strictest rule (upper limit at most 5%), only {{n_cells_strict}} of {{n_cells}} combinations qualified and D1 never did (upper limits {{D1_hi_range}}%), mainly because a no-change arm of {{n_artes}} patients cannot show a rate near 5% to be below 5%.

In practical terms, if 1,000 stable eyes were reviewed once with three fields, D1 would raise about {{ff_D1_3}} false progression flags, D6 about {{ff_D6_3}} and D8 about {{ff_D8_3}}. Reviewed at three, four, five and six fields in turn (post hoc), {{cum_D1}}% (95% CI {{cumci_D1}}) of no-change series received at least one false D1 flag, compared with {{cum_D6}}% ({{cumci_D6}}) for D6 and {{cum_D8}}% ({{cumci_D8}}) for D8.

Specificity against reference-stable eyes did not reveal these false alarms. With three fields, it was {{sp_D1_3}}% for D1, {{sp_D6_3}}% for D6 and {{sp_D8_3}}% for D8 (Supplementary Table S1).

Three detectors could not flag any eye with three fields for structural reasons. PoPLR (D4) and the self-supervised order network (D10) use within-eye permutation, and three fields have only six possible orders, so the smallest p-value is 1/6; event analysis (D7) needs two follow-up fields after a two-field baseline.

{{TABLE2}}

**Table 2.** Sensitivity against the future-confirmed reference (%) / false-alarm rate on true no-change series (%), by number of fields available. † False-alarm rate not valid under the primary rule (95% CI upper limit above 10% or lower limit above 5%). Reference: {{n_prog}} progressing and {{n_stab}} stable eyes; true no-change: {{artes_win_6}}–{{artes_win_3}} windows (three to six fields) from {{n_artes}} patients, each with ten time-scale draws. Confidence intervals are given in Supplementary Table S1.

## Sensitivity against the future reference (RQ2)

No detector with a valid false-alarm rate flagged significantly more reference progressors than D1 at any number of fields (Supplementary Table S2), so the pre-specified hypothesis H2 {{h2_falsified}}. This is weak evidence of equivalence: with {{n_prog}} progressors, gains of up to {{max_gain_hi}} percentage points were within the confidence intervals of valid detectors. The only nominally significant gain was that of D6 with three fields ({{dSa_D6_3}} percentage points, 95% CI {{dSci_D6_3}}; Holm-adjusted p {{dSp_D6_3}} within three fields, p {{dSpall_D6_3}} when corrected across all numbers of fields), and its false-alarm rate was {{f_D6_3}}%.

Several valid detectors had point estimates above D1. With three fields, the MD rate rule (D2) flagged {{s_D2_3}}% ({{sci_D2_3}}) versus {{s_D1_3}}% ({{sci_D1_3}}) for D1, a difference of {{dSa_D2_3}} percentage points ({{dSci_D2_3}}; adjusted p {{dSp_D2_3}}). With five fields, event analysis (D7) flagged {{s_D7_5}}% versus {{s_D1_5}}% ({{dSa_D7_5}} points, {{dSci_D7_5}}; adjusted p {{dSp_D7_5}}). With six fields, D8 flagged {{s_D8_6}}% with a valid false-alarm rate of {{f_D8_6}}%, versus {{s_D1_6}}% for D1 ({{dSa_D8_6}} points, {{dSci_D8_6}}; adjusted p {{dSp_D8_6}}).

Among reference progressors, D1 flagged {{by6_D1}}% by the sixth field, with a median of {{tfd_D1}} fields to the first flag (about {{ref_t6}} years for six fields in this clinic). D6 and D8 reached a first flag earlier (median {{tfd_D6}} and {{tfd_D8}} fields; {{by6_D6}}% and {{by6_D8}}% flagged by six fields), at the false-alarm cost shown above. At a prevalence of progression of 10%, the share of three-field flags that would be true progression was {{ppv10_D1_3}}% for D1, {{ppv10_D2_3}}% for D2, {{ppv10_D6_3}}% for D6 and {{ppv10_D8_3}}% for D8 (post hoc).

With the secondary reference based on PoPLR over the whole series, sensitivity was lower for all detectors; with three fields it was {{r2_D1_3}}% for D1, {{r2_D2_3}}% for D2, {{r2_D6_3}}% for D6 and {{r2_D8_3}}% for D8, and with six fields {{r2_D1_6}}% for D1 against {{r2_D10_6}}% for D10, {{r2_D6_6}}% for D6, {{r2_D8_6}}% for D8 and {{r2_D7_6}}% for D7 (Supplementary Table S1). With the post-hoc reference computed only from fields after the first k, the reference sets were small ({{lr_np_3}} progressing and {{lr_ns_3}} stable eyes for three fields; {{lr_np_6}} and {{lr_ns_6}} for six). D6 again flagged more progressors than D1 with three fields ({{lr_s_D6_3}}% versus {{lr_s_D1_3}}%; adjusted p {{lr_d6_p}}), and {{lr_nsig}} comparisons with D1 were significant (Supplementary Tables S4 and S5). Across seeds, the largest standard deviation was {{max_seed_sd_sens}} points for sensitivity ({{max_seed_det}}) and {{max_seed_sd_fpr}} points for the false-alarm rate.

## Shuffle audit (RQ3)

Across the {{rq3_cells}} detector–field-number combinations, the false-alarm rate estimated by shuffling the order of each eye's fields was correlated with the true no-change false-alarm rate (Spearman ρ = {{rq3_rho}}, 95% CI {{rq3_lo}}–{{rq3_hi}}; {{rq3_rho_nz}} after excluding combinations that were zero by construction; Fig. 3). The median absolute difference was {{rq3_med}} points, {{rq3_within3}}% of combinations were within 3 points, and the largest difference was {{rq3_max}} points. Because the correlation was below the pre-specified 0.7, H3 was not met. As a screening tool (post hoc), the audit identified {{aud_det}} of {{aud_inv}} combinations with invalid true false-alarm rates (missed: {{aud_missed}}), including all with grossly inflated rates (D6 with three fields: audit {{a_D6_3}}%; D8 with three and five fields: {{a_D8_3}}% and {{a_D8_5}}%). It also gave false warnings for {{aud_fw}} of {{aud_nv}} valid combinations, mostly rules without a p-value, such as the MD rate rule (D2 three fields: audit {{a_D2_3}}% versus true {{f_D2_3}}%) and event analysis (D7 six fields: {{a_D7_6}}% versus {{f_D7_6}}%).

## External data set (RQ5)

In GRAPE (Table 3, Fig. 4), D1 had a sensitivity of {{gs_D1_3}}% ({{gsci_D1_3}}) and a specificity of {{gp_D1_3}}% ({{gpci_D1_3}}) with three fields. This result is close to circular: the MD label is a slope test of mean deviation over a short series, and D1 flagged {{g3_f}} of {{g3_n}} labelled progressors among eyes with exactly three visits, compared with {{g4_f}} of {{g4_n}} among eyes with more visits (post hoc). D8, transferred unchanged from UWHVF, flagged more labelled progressors ({{gs_D8_3}}%) but its specificity fell to {{gp_D8_3}}% ({{gpci_D8_3}}): it flagged {{dGFa_D8_3}} percentage points more non-progressing eyes than D1 (95% CI {{dGFci_D8_3}}; adjusted p {{dGFp_D8_3}}). At the GRAPE prevalence of {{grape_prev}}%, {{ppvg_D1_3}}% of D1 flags and {{ppvg_D8_3}}% of D8 flags corresponded to labelled progression. The MD rate rule (D2) also lost specificity (sensitivity {{gs_D2_3}}%, specificity {{gp_D2_3}}%). PoPLR (D4) and event analysis (D7) could not flag with three fields; with four fields their sensitivities were {{gs_D4_4}}% and {{gs_D7_4}}%. D5, calibrated on GRAPE itself, matched D1 ({{gs_D5_3}}% and {{gp_D5_3}}%). GRAPE has no true no-change arm, so it tests transfer and specificity against the label, not validity.

{{TABLE3}}

**Table 3.** External data set (GRAPE): sensitivity and specificity (%, 95% CI) against the MD progression label supplied with the data set, using the first three or four fields ({{g_np_3}} labelled progressors and {{g_ns_3}} non-progressors with at least three fields; {{g_np_4}} and {{g_ns_4}} with at least four). D6, D9 and D10 require the 24-2 pattern and were not applied.

# Discussion

We compared ten detectors of glaucomatous visual field progression on a question that matters for treatment decisions: how early can progression be flagged without raising false alarms? Three findings stand out. First, the detectors that gained most over the trend test with three fields did so mainly by flagging more of everything: on series in which nothing changed, the pooled-detrended conformal test flagged {{f_D6_3}}% and a gradient-boosted tree model {{f_D8_3}}% of windows, against a nominal 5%. Second, specificity measured in eyes labelled stable by the full series, a common way of estimating it, did not show this; re-ordering-based checks, as used in earlier work [6, 7], did. Third, no detector with an acceptable false-alarm rate was significantly more sensitive than the plain trend test of mean sensitivity; our study could exclude only large gains, so this is absence of evidence rather than evidence of equivalence.

These results fit what is known about the information in a short series. A trend line through three or four noisy fields has very few degrees of freedom, and the noise of perimetry rises as sensitivity falls [8]. Methods that pool information across patients or locations can add power [9, 10, 35], but only if the pooled reference matches the eye being tested. Our pooled-detrended test borrowed its null distribution from other patients' detrended and shuffled series [30, 31]. With three fields, detrending leaves one residual degree of freedom, and the borrowed distribution was probably too narrow; we had already seen this during development, and the held-out shuffle audit confirmed it. The within-eye permutation test PoPLR avoids this problem by design [6], but with three fields it has only six orders and cannot reach p < 0.05. This floor is a property of the method, not a fault of its implementation.

The machine-learning results need careful reading. Our models were trained on a few hundred labelled eyes, with a modest tuning budget, and are not replicas of published models [16–21]; the finding concerns a way of setting thresholds, not any specific published detector. When a model is trained to predict future progression and thresholded at a target specificity in reference-stable eyes, as D8 and D9 were, two things happen. The threshold inherits the selection of those eyes, which tend to be eyes whose early fields also looked stable, so the specificity is optimistic. And the model partly predicts risk: features such as the level of mean sensitivity can raise its output in an eye that is not changing. In our data, the true false-alarm rate of the tabular model ranged from {{f_D8_6}}% to {{f_D8_3}}% depending on the number of fields. Labels also differ between studies, and models trained on one label may not transfer [22]; in GRAPE, the transferred model lost {{dGFa_D8_3}} percentage points of specificity relative to the trend test. Machine learning may still help, but a model's flag rate on true no-change data should be reported before claims of earlier detection.

Artes and colleagues previously used the same retest series to estimate the specificity of the Guided Progression Analysis [7]. We extended this approach to ten detectors and four series lengths and examined a check that a clinic can run without retest data. The shuffle audit picked out the grossly inflated detectors, but its agreement with the true rate fell short of our pre-specified target, and it gave false warnings, mostly for rules that use a size threshold without a p-value. A likely reason is that shuffling a truly progressing series keeps its spread of values and creates steep slopes in both directions. Running the audit also requires access to raw field data and the ability to run the detector outside the perimeter's software. It is therefore best seen as a screening check that can raise a question about a detector, not as a substitute for a true no-change test.

For clinical practice, the main limit to earlier detection is the number and spacing of fields, not the detector. In UWHVF, fields were a median of {{ref_int}} years apart; with three fields the trend test flagged only {{s_D1_3}}% of eyes that later progressed, and it needed a median of {{tfd_D1}} fields to flag a progressor. A "no progression" result after a few fields is therefore not reassurance. This agrees with earlier work showing that routine testing frequencies delay the identification of progression [25–27]. Testing more often early in follow-up [4], clustering tests [28], personalised schedules [23, 34] or smoothing [36] address the amount of information directly, and our results suggest that earlier detection is more likely to come from such strategies than from a more complex detector applied to the same sparse fields. Until a detector shows an acceptable false-alarm rate on true no-change data, a flag from it should not by itself trigger escalation of treatment.

This study has several limitations. The reference set was small ({{n_prog}} progressing and {{n_stab}} stable eyes from {{n_ref_pat}} patients) and limited to clear-cut eyes ({{n_indet}} indeterminate eyes were excluded), so sensitivity estimates are imprecise and may not apply to borderline eyes. The primary reference uses a mean-deviation slope over a series that includes the fields the detectors saw, which may favour D1; the secondary and later-field references reduce but do not remove this concern. The true no-change arm included only {{n_artes}} patients from one centre, retested over a few weeks; it lacks long-term fluctuation, so false-alarm rates in routine care are probably higher than our estimates for all detectors, and we assigned clinical test intervals to these series (amendment A1). D6's behaviour on these data was known from development. UWHVF has no diagnoses, treatment information or reliability indices, so the cohort may include eyes without glaucoma, and we could not relate flags to treatment decisions or outcomes. GRAPE used a different perimeter with a variable number of analysable locations, its labels are rule-based criteria computed on short series that overlap with the fields given to the detectors, and its patients were younger (median age {{grape_age}} versus {{ref_age}} years); its results test transfer, not independent accuracy. The protocol was time-stamped in version control but not registered externally, and the deviations listed in the Methods include analyses added after an internal review. Finally, we developed and abandoned several method ideas before writing the protocol (Supplementary Note S1); the final test data were analysed once, as planned.

# Conclusion

In this benchmark, the largest apparent gains in early detection of glaucomatous visual field progression came with false-alarm rates well above the nominal level, and specificity measured in reference-stable eyes did not reveal them. No detector with acceptable false alarms was significantly better than a simple trend test of mean sensitivity, which was well calibrated but slow; larger studies would be needed to exclude modest gains. New detectors should be reported with their false-alarm rate on true no-change data before their flags are used to escalate treatment.

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

Supplementary Table S1: all metrics with 95% confidence intervals (sensitivity, specificity, true no-change and shuffle-audit false-alarm rates, secondary-reference sensitivity, GRAPE results) for every detector and number of fields. Supplementary Table S2: paired comparisons with D1 (difference, bootstrap 95% CI, exact McNemar p, Holm-adjusted p). Supplementary Table S3: fields to first flag among reference progressors, by detector (seed means). Supplementary Tables S4 and S5 (post hoc): sensitivity, specificity and paired tests against the reference computed only from fields after the first k. Supplementary Note S1: development history, including abandoned method ideas.
