# Detecting Glaucomatous Visual Field Progression From Few Tests Without False Alarms: A Benchmark With a True No-Change Arm

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, AFFILIATIONS, ADDRESSES AND ORCID iDs — TO BE COMPLETED BY THE AUTHORS]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — TO BE COMPLETED]

**Prior presentation:** None. [AUTHORS TO CONFIRM]

## Abstract

**Introduction:** Many new detectors claim to find glaucomatous visual field progression earlier, which would allow earlier treatment escalation, but their false-alarm rates are rarely measured on data without change. We asked how early progression can be detected from the first few fields without raising false alarms.

**Methods:** In this retrospective benchmark of public data, ten detectors (trend, event, permutation, conformal, machine learning) saw the first 3–6 fields of each series. We measured sensitivity and specificity against a future-confirmed reference in held-out eyes of the University of Washington data set ({{n_prog}} progressing, {{n_stab}} stable), false-alarm rates on true no-change series ({{n_artes}} patients tested weekly for 12 weeks), a "shuffle audit", and an external data set from China ({{n_grape_eyes}} eyes, different perimeter).

**Results:** With three fields, the trend test of mean sensitivity flagged {{s_D1_3}}% of progressors with a false-alarm rate of {{f_D1_3}}% (95% CI {{fci_D1_3}}). Two detectors flagged more progressors only with excess false alarms: a pooled-detrended conformal test ({{s_D6_3}}% sensitivity; {{f_D6_3}}% false alarms) and gradient-boosted trees thresholded at 95% specificity ({{s_D8_3}}%; {{f_D8_3}}%). Reference-stable eyes did not reveal this: their specificity was {{sp_D6_3}}% and {{sp_D8_3}}%. {{n_cells_invalid}} of {{n_cells}} detector–field-number combinations had invalid false-alarm rates. No detector with a valid false-alarm rate flagged significantly more progressors than the trend test at any number of fields. The shuffle audit tracked the true false-alarm rate (Spearman ρ = {{rq3_rho}}; {{rq3_within3}}% of combinations within 3 percentage points). Externally, the machine-learning detector had specificity {{gp_D8_3}}% versus {{gp_D1_3}}% for the trend test.

**Conclusion:** In this benchmark, the largest apparent early-detection gains were false alarms that standard specificity estimates missed. Progression detectors should be reported with false-alarm rates on true no-change data; a simple trend test remains a strong default, and clinics can check a detector on their own records with a shuffle audit.

**Keywords:** Benchmarking; False alarms; Glaucoma; Machine learning; Perimetry; Progression detection; Visual field

## Key Summary Points

**Why carry out this study?**

- Glaucoma treatment is escalated when visual field tests show progression, and many new detectors claim to find progression earlier, but most are judged by how many eyes they flag rather than by how many of those flags are false.

- We asked whether any of ten detectors could flag future-confirmed progression from three to six fields more often than a simple trend test while keeping false alarms on true no-change data at the nominal 5%.

**What was learned from the study?**

- With three fields, the two detectors that flagged the most progressors ({{s_D6_3}}% and {{s_D8_3}}% versus {{s_D1_3}}% for the trend test) raised false alarms in {{f_D6_3}}% and {{f_D8_3}}% of true no-change series, which specificity in reference-stable eyes did not reveal.

- No detector with a valid false-alarm rate beat the simple trend test significantly at any number of fields, so the evidence does not support replacing it in routine care.

- Reports of new progression detectors should include false-alarm rates on true no-change data, and a shuffle audit of a clinic's own records is a cheap first check.

<<INTRO_METHODS>>

# Results

## Study data

Table 1 summarises the three data sets. The UWHVF test set contained {{n_test_eyes}} eyes of {{n_test_pat}} patients with at least three fields; {{n_test8}} had at least eight fields, of which {{n_prog}} were reference progressors, {{n_stab}} reference stable and {{n_indet}} indeterminate. The {{n_prog}} + {{n_stab}} reference eyes came from {{n_ref_pat}} patients, had a median baseline mean deviation of {{ref_md}} dB (interquartile range [IQR] {{ref_md_iqr}}) and were followed for a median of {{ref_fu}} years. Their first six fields were a median of {{ref_int}} years apart (IQR {{ref_int_iqr}}), so six fields took a median of {{ref_t6}} years. The true no-change arm gave {{artes_win_3}}, {{artes_win_4}}, {{artes_win_5}} and {{artes_win_6}} windows of three to six consecutive fields. In GRAPE, {{grape_md}} of {{n_grape_eyes}} eyes ({{grape_md_pct}}%) carried the MD progression label.

{{TABLE1}}

**Table 1.** Data sets. IQR, interquartile range; MD, mean deviation; PLR2/PLR3, pointwise linear regression criteria with at least two or three progressing locations.

## False alarms on true no-change data (RQ1 and RQ4)

Table 2 and Fig. 2 show sensitivity against the future reference together with the false-alarm rate on true no-change series. The trend test of mean sensitivity (D1) kept its false-alarm rate near the nominal level at every number of fields ({{f_D1_3}}%, {{f_D1_4}}%, {{f_D1_5}}% and {{f_D1_6}}% for three to six fields). The pooled-shuffle conformal test (D5) behaved almost identically to D1.

Three detectors had clearly inflated false-alarm rates with three fields: the pooled-detrended conformal test (D6, {{f_D6_3}}%, 95% CI {{fci_D6_3}}), the tabular machine-learning model (D8, {{f_D8_3}}%, {{fci_D8_3}}) and the sequence model (D9, {{f_D9_3}}%, {{fci_D9_3}}). The machine-learning models were thresholded at 95% specificity on reference-stable validation eyes. On true no-change data, their false-alarm rate was significantly above 5% in {{ml_cells_above5}} of {{ml_cells}} combinations, and it changed erratically with the number of fields (D8: {{f_D8_3}}%, {{f_D8_4}}%, {{f_D8_5}}% and {{f_D8_6}}%). The number of valid detectors was {{nvalid_3}}, {{nvalid_4}}, {{nvalid_5}} and {{nvalid_6}} of ten for three, four, five and six fields. Expressed per 1,000 stable eyes reviewed with three fields, D1 would raise about {{ff_D1_3}} false progression flags, D6 about {{ff_D6_3}} and D8 about {{ff_D8_3}}.

Specificity against reference-stable eyes did not reveal these false alarms. With three fields, it was {{sp_D1_3}}% for D1, {{sp_D6_3}}% for D6 and {{sp_D8_3}}% for D8 (Supplementary Table S1).

Two detectors could not flag any eye with three fields for structural reasons. PoPLR (D4) has only six possible orders of three fields, so its smallest p-value is 1/6, and event analysis (D7) needs two follow-up fields after a two-field baseline. The self-supervised order network (D10) also flagged no eye with three fields.

{{TABLE2}}

**Table 2.** Sensitivity against the future-confirmed reference (%) / false-alarm rate on true no-change series (%), by number of fields available. † False-alarm rate not valid (95% CI upper limit above 10% or lower limit above 5%). Reference: {{n_prog}} progressing and {{n_stab}} stable eyes; true no-change: {{artes_win_6}}–{{artes_win_3}} windows (three to six fields) from {{n_artes}} patients, each with ten time-scale draws. Confidence intervals are given in Supplementary Table S1.

## Sensitivity against the future reference (RQ2)

No detector with a valid false-alarm rate flagged significantly more reference progressors than D1 at any number of fields (Supplementary Table S2), so the pre-specified hypothesis H2 {{h2_falsified}}. The only significant gain in sensitivity was that of D6 with three fields ({{dSa_D6_3}} percentage points, 95% CI {{dSci_D6_3}}; Holm-adjusted p {{dSp_D6_3}}), and this detector's false-alarm rate was {{f_D6_3}}%.

Several valid detectors had point estimates above D1, but the confidence intervals were wide with {{n_prog}} progressors. With three fields, the MD rate rule (D2) flagged {{s_D2_3}}% ({{sci_D2_3}}) versus {{s_D1_3}}% ({{sci_D1_3}}) for D1, a difference of {{dSa_D2_3}} percentage points ({{dSci_D2_3}}; adjusted p {{dSp_D2_3}}). With five fields, event analysis (D7) flagged {{s_D7_5}}% versus {{s_D1_5}}% ({{dSa_D7_5}} points, {{dSci_D7_5}}; adjusted p {{dSp_D7_5}}). With six fields, D8 flagged {{s_D8_6}}% with a valid false-alarm rate of {{f_D8_6}}%, versus {{s_D1_6}}% for D1 ({{dSa_D8_6}} points, {{dSci_D8_6}}; adjusted p {{dSp_D8_6}}). In total, {{n_valid_gain10}} valid detector–field-number combinations had a point gain of 10 points or more, none of them significant after correction.

Among reference progressors, D1 flagged {{by6_D1}}% by the sixth field, with a median of {{tfd_D1}} fields to the first flag. D6 and D8 reached a first flag earlier (median {{tfd_D6}} and {{tfd_D8}} fields; {{by6_D6}}% and {{by6_D8}}% flagged by six fields), but at the false-alarm cost shown above. With fields {{ref_int}} years apart, as in this clinic, one field less corresponds to roughly {{ref_int}} years earlier.

With the secondary reference based on PoPLR over the whole series, sensitivity was lower for all detectors but the ranking was similar (for example, three fields: D1 {{r2_D1_3}}%, D6 {{r2_D6_3}}%, D8 {{r2_D8_3}}%; six fields: D1 {{r2_D1_6}}%, D8 {{r2_D8_6}}%; Supplementary Table S1). Across seeds, the largest standard deviation was {{max_seed_sd_sens}} points for sensitivity ({{max_seed_det}}) and {{max_seed_sd_fpr}} points for the false-alarm rate; all reported values are seed means.

## Shuffle audit (RQ3)

Across the {{rq3_cells}} detector–field-number combinations, the false-alarm rate estimated by shuffling the order of each eye's fields agreed with the true no-change false-alarm rate (Spearman ρ = {{rq3_rho}}, p {{rq3_p}}; median absolute difference {{rq3_med}} points; {{rq3_within3}}% within 3 points; largest difference {{rq3_max}} points; Fig. 3). Hypothesis H3 was therefore {{h3_status}}: most cells agreed closely, but the correlation was below the pre-specified 0.7. The audit identified every detector with a grossly inflated false-alarm rate (D6 three fields: {{a_D6_3}}%; D8 three fields: {{a_D8_3}}%; D8 five fields: {{a_D8_5}}%). It overestimated the false-alarm rate of rules without a p-value, such as the MD rate rule (D2 three fields: audit {{a_D2_3}}% versus true {{f_D2_3}}%) and event analysis (D7 six fields: {{a_D7_6}}% versus {{f_D7_6}}%).

## External data set (RQ5)

In GRAPE (Table 3, Fig. 4), D1 had a sensitivity of {{gs_D1_3}}% ({{gsci_D1_3}}) and a specificity of {{gp_D1_3}}% ({{gpci_D1_3}}) with three fields. D8, transferred unchanged from UWHVF, flagged more labelled progressors ({{gs_D8_3}}%) but its specificity fell to {{gp_D8_3}}% ({{gpci_D8_3}}): it flagged {{dGFa_D8_3}} percentage points more non-progressing eyes than D1 (95% CI {{dGFci_D8_3}}; adjusted p {{dGFp_D8_3}}). The MD rate rule (D2) showed the same pattern (sensitivity {{gs_D2_3}}%, specificity {{gp_D2_3}}%). PoPLR (D4) and event analysis (D7) could not flag with three fields; with four fields their sensitivities were {{gs_D4_4}}% and {{gs_D7_4}}%. D5, calibrated on GRAPE itself, matched D1 ({{gs_D5_3}}% and {{gp_D5_3}}%).

{{TABLE3}}

**Table 3.** External data set (GRAPE): sensitivity and specificity (%, 95% CI) against the MD progression label supplied with the data set, using the first three or four fields. D6, D9 and D10 require the 24-2 pattern and were not applied.

# Discussion

We compared ten detectors of glaucomatous visual field progression on the question that matters for a treatment decision: how early can progression be flagged without raising false alarms? Three findings stand out. First, the detectors that flagged the most progressors from three fields did so mainly by flagging more of everything. On series in which nothing changed, the pooled-detrended conformal test flagged {{f_D6_3}}% and a gradient-boosted tree model {{f_D8_3}}% of windows, against a nominal 5%. Second, the usual way to measure specificity, in eyes labelled stable by the full series, missed this. Third, no detector with a valid false-alarm rate beat the plain trend test of mean sensitivity significantly at any number of fields, in one clinic or in a second clinic using a different perimeter.

These results fit what is known about the information in a short series. A trend line through three or four noisy fields has very few degrees of freedom, and the noise of perimetry rises as sensitivity falls [8]. Methods that pool information across patients or locations can add power [9, 10, 35], but only if the pooled reference matches the eye being tested. Our pooled-detrended test borrowed its null distribution from other patients' detrended and shuffled series [30, 31]. With three fields, detrending leaves one residual degree of freedom, and the borrowed distribution was too narrow; the shuffle audit and the true no-change arm both exposed this. The within-eye permutation test PoPLR avoids this problem by design [6], but with three fields it has only six orders and cannot reach p < 0.05. This floor is a property of the method, not a fault of its implementation.

The machine-learning results deserve attention because supervised models are increasingly proposed for this task [16–21]. When such a model is thresholded at a target specificity in reference-stable eyes, as D8 and D9 were, the threshold inherits the selection of those eyes. Eyes that remain stable over eight or more fields tend to be eyes whose early fields also looked stable. Specificity measured in them is therefore optimistic, and the threshold does not control false alarms in a new eye with short follow-up. In our data the true false-alarm rate of the tabular model ranged from {{f_D8_6}}% to {{f_D8_3}}% depending on the number of fields. Labels also differ between studies, and models trained on one label may not transfer [22]; in GRAPE, the transferred model lost {{dGFa_D8_3}} percentage points of specificity relative to the trend test. This does not mean that machine learning cannot help, but it does mean that a model's flag rate on true no-change data should be reported before any claim of earlier detection.

Artes and colleagues previously used the same retest series to estimate the specificity of the Guided Progression Analysis [7]. We extend this approach to ten detectors and four series lengths, and add a check that any clinic can run without retest data. The shuffle audit agreed with the true false-alarm rate within 3 points in {{rq3_within3}}% of combinations and flagged every detector with a grossly inflated rate. It was conservative for rules that use a size threshold without a p-value, probably because shuffling a truly progressing series keeps its spread of values and creates steep slopes in both directions. A clinic that adopts a new detector can therefore shuffle its own records, re-run the detector and compare the flag rate with the nominal level; a large excess is a warning sign.

For clinical practice, the main limit to earlier detection is the number and spacing of fields, not the detector. In UWHVF, fields were a median of {{ref_int}} years apart, so the trend test needed a median of {{tfd_D1}} fields, several years, to flag a reference progressor. This agrees with earlier work showing that routine testing frequencies delay the identification of progression [25–27]. Testing more often early in follow-up [4], clustering tests [28], personalised schedules [23, 34] or smoothing [36] address the amount of information directly. Our results suggest that these strategies, rather than a more complex detector applied to the same sparse fields, are where earlier detection is likely to come from. Until a detector shows a valid false-alarm rate on true no-change data, a flag from it should not by itself trigger escalation of treatment.

This study has several limitations. The future reference set was small ({{n_prog}} progressing and {{n_stab}} stable eyes), so confidence intervals for sensitivity are wide and moderate gains (around 10 points) cannot be excluded. The primary reference is based on the slope of mean deviation over the whole series, which may favour detectors based on mean sensitivity; the secondary PoPLR-based reference gave a similar ranking. The true no-change arm included only {{n_artes}} patients from one centre, retested weekly; we assigned clinical test intervals from UWHVF to these series (amendment A1), which keeps them a valid null but does not capture fluctuation over months or years. UWHVF has no diagnoses or reliability indices, so the cohort may include eyes without glaucoma. GRAPE used a different perimeter, its labels are rule-based criteria computed on short series that overlap heavily with the fields given to the detectors, and its patients were younger (median age {{grape_age}} versus {{ref_age}} years in the UWHVF reference eyes); external results should therefore be read as a test of transfer and of false alarms, not as an independent accuracy estimate. Finally, we developed and abandoned several method ideas before writing the analysis plan, and the Artes data were used once during development to check false alarms; we report these steps in the Supplementary Material. The final test data were analysed once, as planned.

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

{{REFERENCES}}

# Supplementary Material

Supplementary Table S1: all metrics with 95% confidence intervals (sensitivity, specificity, true no-change and shuffle-audit false-alarm rates, secondary-reference sensitivity, GRAPE results) for every detector and number of fields. Supplementary Table S2: paired comparisons with D1 (difference, bootstrap 95% CI, exact McNemar p, Holm-adjusted p). Supplementary Table S3: fields to first flag among reference progressors, by detector (seed means). Supplementary Note S1: development history, including abandoned method ideas.
