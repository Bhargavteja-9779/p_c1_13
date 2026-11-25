# Review summary: deduplicated issues across reviews 01–10

Reviewers:
- R01 editor
- R02 glaucoma clinician
- R03 perimetry methods
- R04 biostatistics
- R05 machine learning
- R06 reproducibility
- R07 reference standard
- R08 external validity
- R09 research integrity
- R10 novelty

Where reviewers disagreed on severity, the highest tag is kept.

Recommendations:
- R01 major (return before review)
- R02 major
- R03 major
- R04 major (borderline reject)
- R05 major
- R06 major
- R07 major
- R08 major
- R09 major (integrity conditions)
- R10 reject

| ID | Severity | Raised by | Issue | Suggested fix |
|---|---|---|---|---|
| F1 | FATAL | R04, R09 (R01, R10) | The validity rule "upper CI ≤ 10% and lower ≤ 5%" is not the protocol rule ("FPR CI upper bound vs 5%") and is not a declared amendment. It first appears in a Methods draft (09:14), during the full run, and in final form in `fill_values.py`. Under the literal protocol rule, D1 is invalid at every k (upper limits 6.3–8.1%). | Declare it as amendment A3 with its true timestamp. Report RQ1/RQ2 under both rules. Remove "before the results were seen" unless it can be evidenced. |
| F2 | FATAL | R07 (R05, R09) | Incorporation and MD-on-MD circularity: the whole-series MD-slope reference includes the first k tests that D1 (a mean-sensitivity slope test) uses. The leakage audit says this is "stated as a limitation", but it is not. | Use a future-only (tests k+1..end) reference. Disclose the overlap in Limitations. Add a non-MD reference. |
| F3 | FATAL | R10 (R05) | The "complex" detectors that fail are the authors' own: D6 comes from failed development, and D8/D9 are small in-house ML models. No published new method (ANSWERS, Bayesian, smoothing, published ML) is tested, yet the claims are general. | Add published comparators, or restrict every claim to the detectors tested. |
| M1 | MAJOR | R04, R06, R09 | Proportions are seed means, but the differences and McNemar tests use a majority vote, which is not disclosed in Methods. Consequences: D6 is reported as "+38.5 pp" although 56.9 − 19.2 = 37.7, and the difference CI's upper limit (57.7) exceeds the detector's own sensitivity; D8 at k = 6 is +11.5 vs 13.1; GRAPE D8 is +25.9 vs 21.5; D8 specificity is 94.6 vs 96.2 with 0/0 discordant pairs. | Use one estimand throughout and state it in Methods. |
| M2 | MAJOR | R04, R10, R02, R01 | H2 cannot be falsified. With n = 26 and Holm over 9 comparisons, significance needs ≥ 9:0 discordant pairs (≈ +35 pp). "Not falsified" is then read as D1 being "hard to beat" or "not beaten". | Add a power/precision analysis. Reframe as estimation or equivalence. Remove "hard to beat". |
| M3 | MAJOR | R04, R10 | The small n is self-imposed. D1–D4 need no training and could use all 314 reference eyes in UWHVF (150 progressors, 164 stable). | Add an analysis on all eligible eyes for the untrained or calibrated detectors. |
| M4 | MAJOR | R04, R06 | The paired bootstrap resamples eyes, not patients as Methods state. McNemar ignores 52 eyes from 41 patients. | Use a cluster bootstrap and a clustered McNemar test, or one eye per patient. |
| M5 | MAJOR | R02, R07 | "Stable" (one-sided p > 0.5) means a positive slope: all 164 stable eyes are improving. 80 of 132 eyes (61%) are excluded as indeterminate (spectrum bias), so specificity is near 100% by construction. | State the definition plainly. Add a clinically stable (flat) class. Report flag rate against the full slope distribution. |
| M6 | MAJOR | R02, R05, R10 | The conclusion "gains were explained by false alarms that only a true no-change check revealed" is contradicted by: D2 at k = 3 (valid, +19 pp), D8 at k = 6 (valid, highest sensitivity, 78% by test 6), and the shuffle audit, which also caught D6 and D8. | Rewrite the Abstract, Conclusions and Key Summary Points to match the evidence. |
| M7 | MAJOR | R02, R04 | Table 3 compares cumulative sensitivity over looks with a per-look false-alarm rate. The cumulative true-null false alarm over serial looks is not reported. | Compute cumulative false alarms on Artes over looks 3..6. |
| M8 | MAJOR | R04, R07, R08, R09, R06 | Pre-registered outputs are not reported: GRAPE PLR2/PLR3/"any" labels (stored in the raw file), secondary-reference specificity, the bootstrap CI for ρ, and per-seed SDs. | Report them all, or explain omissions in a deviations table. |
| M9 | MAJOR | R07, R08 | GRAPE "clinician labels" are MD-criterion labels (MD-on-MD circularity). Reviewer computation from the raw file: on PLR2, D1 sensitivity is 17.5% vs 61.0% for D8 and 45.0% for D2. Non-progressors by MD are called "false positives". | Report all labels. Use "criterion-based labels". Discuss the circularity. |
| M10 | MAJOR | R08, R01 | "No valid detector ... in Seattle or in China": validity is undefined in GRAPE (no true-null data). | Reword the Key Summary Points, Abstract and Discussion. |
| M11 | MAJOR | R09, R08, R06 | Quick mode processed Artes and GRAPE (with labels) before A1/A2 were committed in the same commit. Methods say GRAPE was "not used before the final run". The quick raw output is missing. | Disclose. Provide the output. Make quick mode skip E2/E4. |
| M12 | MAJOR | R09, R10 | The D6 true-null failure (20–22%) was already known from development Round 5 on the same Artes data, and it shaped the question. The paper presents it as a pre-registered finding. | Label it as non-confirmatory and report the development result. |
| M13 | MAJOR | R01, R09, R10 | "Pre-registered" refers to a private git file committed 3 minutes before the implementation, with no registry. | Use "analysis plan committed before final run (commit hash)". Make the history public. |
| M14 | MAJOR | R03, R08, R02 | Amendment A1 (donor clinic dates on weekly retests) spreads short-term noise over years, so rate and event rules look valid (D2: 2.6% vs 11.7% in the shuffle audit and +16.5 pp false positives in GRAPE). Donor eyes are not reference eyes. Clinic long-term variability is absent. | Run sensitivity analyses with weekly spacing, reference-stable donors and variance inflation. Make the "valid" verdict for D2, D3 and D7 conditional. |
| M15 | MAJOR | R03, R06 | D7 is not GPA: it uses raw sensitivity, not pattern deviation; its limits come from single-pair differences binned on the first test and are applied to a 2-test baseline; small bins are silently interpolated. This makes D7 conservative. | Re-derive the limits correctly, or rename the detector. Document the bins. |
| M16 | MAJOR | R03, R04 | D4, D7 and D10 cannot flag at k = 3, yet they are counted as "valid" ("7 of 10") and included in the Holm family. | Mark them not applicable. Exclude them from the count and the Holm family. |
| M17 | MAJOR | R03, R06 | D4 is exact, yet called stochastic. The Artes time-label draws differ by detector and seed, so the E2 comparisons are not paired. | Use one shared, saved donor assignment. Reclassify D4. |
| M18 | MAJOR | R05 | The ML models are trained on about 190 labelled eyes. The threshold is the 95th percentile of 39 validation stable scores, and the same validation set is used for model selection (double use). | Report the counts. Use cross-validated or separate calibration. Report threshold variability. |
| M19 | MAJOR | R05 | The D8 features include span and level. Progressors are tested more often (span 2.08 vs 2.37 years at k = 3) and are worse. Artes donor spans resemble progressors, so the RQ4 attribution to "the threshold rule" is confounded. | Ablate these features, use change-only features, report SHAP. |
| M20 | MAJOR | R05 | "As is common in machine-learning studies" (the 95%-specificity threshold) has no citation. | Cite specific studies or remove the claim. |
| M21 | MAJOR | R05 | The ML tuning and architecture budget is weak (a small GRU, no early stopping), and the claims about "ML detectors" are generic. | Call them simple baselines, or add a strong published model. |
| M22 | MAJOR | R07, R03 | The secondary PoPLR reference is a superset of the primary (all 26 primary progressors are included; the 17 stable eyes are a subset). Its specificity is unreported. "Same ranking" is false: at k = 6, D1 ranks fifth. It is circular with D4 and D10. | Correct the text. Report specificity and tests. Add an independent reference. |
| M23 | MAJOR | R04 | There are 96 paired tests, with Holm only within k × endpoint. "The only significant gain in the study" is study-wide language without study-wide control. | Define the family. Use descriptive language. |
| M24 | MAJOR | R01, R10 | Scope fit for a therapy journal is weak; there is no therapy outcome. | Reframe around escalation decisions, or consider a perimetry or methods journal. |
| M25 | MAJOR | R01, R10 | Declarations contain placeholders (authors, funding, contributions, disclosures, code URL). | Complete them before submission. |
| M26 | MAJOR | R01, R09, R10 | AI use is understated: the repository shows the AI did the design, protocol, code, analysis and drafting, with no human commits. | Write a precise AI statement in Methods, describe the human verification, and name a guarantor. |
| M27 | MAJOR | R10 | Novelty over Artes et al. 2014 [11], which used the same retest data for specificity, is not shown. | Add a "what this adds" paragraph with quantitative contrasts. |
| M28 | MAJOR | R06 | The 5 unit tests (all pass) do not cover the detectors, the reference, windowing, summarise, describe or the validity rule. | Add tests and a regression test for Table 1. |
| M29 | MAJOR | R06 | The primary validity rule lives in the manuscript filler (`fill_values.py`), not in the analysis output. | Move it to `summarise.py`, write it to JSON, and test it. |
| M30 | MAJOR | R06, R09 | "One command reproduces every number" is false. `run_all` does not call summarise, describe, figures or fill, and it writes `.csv` while describe reads `.csv.gz`. | Add a single driver. Fix the docstring and README. |
| M31 | MAJOR | R02 | The progressors are slow (median −0.57 dB/yr). There is no analysis by progression rate or severity. | Stratify by full-series rate and baseline MD. |
| O1 | MODERATE | R04, R10 | RQ3: the 40 cells are non-independent and include structural zeros and detectors that agree with the shuffle by construction (D4, D5, D10). The p < 0.001 is meaningless. | Report a cluster bootstrap CI and restricted analyses. Drop the p-value. |
| O2 | MODERATE | R04 | Degenerate percentile CIs such as 100.0 (100.0–100.0) and 0.0 (0.0–0.0). | Use Wilson or Clopper–Pearson intervals (cluster-adjusted). |
| O3 | MODERATE | R04, R09 | The validity dichotomy is fragile: D9 at k = 6 is invalid by 0.000002; D6 at k = 5 is "valid" at 6.2%. | Emphasise CIs and report robustness to the bootstrap seed. |
| O4 | MODERATE | R04 | Non-significance is presented as equivalence ("about as specific", "matched D1", "not beaten"). | Use estimation language. |
| O5 | MODERATE | R02, R10, R01 | "224 and 277 unnecessary escalation discussions" is a hypothetical extrapolation. | Present it as a scenario and add a confirmation-on-next-test analysis. |
| O6 | MODERATE | R02 | "Front-loading ... likely to help more" was not tested. | Label it as speculation or remove it. |
| O7 | MODERATE | R03 | Practice effects in early Artes windows; reliability indices loaded but unused. | Report results by window start and with unreliable tests excluded. |
| O8 | MODERATE | R03, R02 | "MD" is used inconsistently: the reference uses unweighted mean TD, D1/D2 use mean sensitivity, and neither is HFA MD. | Rename and define. |
| O9 | MODERATE | R03 | The D3 PLR criterion is ad hoc, and "one-sided" is not stated in Methods. | Cite the source criterion and state "one-sided". |
| O10 | MODERATE | R03, R05, R08 | GRAPE perimeter and dB scale: the −1 dB/yr threshold and D8 level/span features are applied unchanged, and the GRAPE intervals are short. D8 is not recalibrated. | Name the perimeter. Add a recalibrated D8. Report the intervals. Qualify the Abstract. |
| O11 | MODERATE | R05 | Separate ML models per k explain the erratic false-alarm pattern (27.7 → 9.4 → 18.8 → 3.6%). | Use a single model with k as an input, or report the per-k configurations. |
| O12 | MODERATE | R07 | The reference thresholds (−0.3 dB/yr, p < 0.01, p > 0.5) are not justified. | Justify them and show sensitivity to alternative thresholds. |
| O13 | MODERATE | R08 | Representativeness of reference eyes (≥ 8 tests over 13 years); the GRAPE baseline visit may be excluded. | Compare reference with non-reference eyes. Clarify the GRAPE visit handling. |
| O14 | MODERATE | R09 | Supplement S1 says development used only UWHVF train/val, which is contradicted by Rounds 4 and 5. It omits the voided Round 5 bug. | Correct S1 and link the full log. |
| O15 | MODERATE | R06 | Protocol vs code deviations: D8 features (no PoPLR S or region slope) and D7 binning. | Add a deviations table. |
| O16 | MODERATE | R06 | Hard-coded data paths, unpinned dependencies, no data checksums, and the quick-run raw file missing. | Pin versions and add checksums. |
| O17 | MODERATE | R01, R09 | References: ref. 28 has an article-number/DOI mismatch; the ref. 23 DOI prefix is atypical; 2026 refs 6, 23 and 26 are unverified. Licence claims are also unverified. | Re-verify the references and cite licence URLs. |
| O18 | MODERATE | R01 | Figure legends are missing from the manuscript, and the ethics text is duplicated. | Add a legends section and consolidate the ethics text. |
| O19 | MODERATE | R02 | No diagnoses, treatment or IOP data in UWHVF; the cohort may include non-glaucoma eyes. | Make this prominent as a limitation. |
| m1 | MINOR | R01, R08 | Key Summary Points wording ("in China"; "two clinics"). | Reword. |
| m2 | MINOR | R01 | No line numbers or plain-language summary. | Add them. |
| m3 | MINOR | R02, R10 | The title promises "how early", but the Abstract gives no tests-to-detection number. | Add the median of 5 tests (≈ 5 years) to the Abstract. |
| m4 | MINOR | R04 | D7 median of 5.5 is computed by averaging a censored discrete variable. | Use the cumulative ≥ 50% rule. |
| m5 | MINOR | R04 | False-alarm ratios ("5.0 and 6.3 times") have no CI. | Add bootstrap CIs. |
| m6 | MINOR | R05 | Inconsistent class weighting (GRU vs LightGBM); the D10 citation [33] overstated. | Harmonise; write "inspired by". |
| m7 | MINOR | R06, R09 | "Four-core CPU" is not recorded in the run metadata. | Record the hardware. |
| m8 | MINOR | R03, R06 | GRAPE per-eye point removal may vary the point count. | Assert or document 59 points. |
| m9 | MINOR | R07 | "Future-confirmed" is a misnomer while the reference includes the first k tests. | Use "whole-series reference". |
