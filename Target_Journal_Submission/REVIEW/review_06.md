# Review 06 — Research-integrity and claim–evidence audit

Reviewer role: research-integrity / claim–evidence auditor (adversarial).
Sources checked: `manuscript/manuscript_filled.md`, `manuscript/cover_letter_filled.md`, `results/metrics.json`,
`results/statistics.json`, `results/descriptives.json`, `results/d6_round5.json`, `tables/*.csv`,
`code/experiments/protocol.md` (with amendments A1 and A2), `code/experiments/leakage_audit.md`,
`journal_selection/novelty_escalation_log.md`, `journal_selection/novelty_map.csv`, and the visualFields 1.0.7 package
files in `data_raw/ext/visualFields`. No git history was inspected (not permitted).

## Summary

Every number in the manuscript that I traced comes from the result files; I found no fabricated value. The integrity
problems are about **framing and disclosure**:

- **(a) D6's false-alarm problem was known before the protocol.** The headline "apparent gain that was really false
  alarms" (D6) had already been shown to be anti-conservative on the same Artes data during development (round 5:
  region-max detrended conformal test, FPR 20–22% at k=3, labelled "INVALID"). The detector was then put into the
  "pre-specified" benchmark. The main text describes D6 only as "the most sensitive approach during development".
- **(b) The validity rule is not the protocol's.** The rule that decides which detectors are "valid" differs from the
  protocol and is not reported as a deviation.
- **(c) A Key Summary Point is factually wrong.** It names D6 and D8 as the two detectors that "flagged the most
  progressors" with three fields. The second-highest was D2 (38%), which had a 2.6% false-alarm rate. The cover letter
  repeats the error.
- **(d) The shuffle audit is over-sold.** The pre-specified criterion for H3 failed, yet the audit is recommended in the
  Abstract, the Key Summary Points and the Conclusion.
- **(e) Imprecision is understated.** The limitations admit that only "around 10 points" of gain cannot be excluded,
  whereas the confidence intervals reach 31–42 points.

The cover letter says "all deviations are reported". That is not yet true.

## A. Claim-by-claim check

Legend: S = supported by the result files; P = numbers supported, but the wording overreaches or omits a material
caveat; U = unsupported or contradicted; NV = cannot be verified from the files.

### Abstract

| # | Claim (quote) | Verdict | Evidence / comment |
|---|---|---|---|
| A1 | "their false-alarm rates are rarely measured on data without change" | P | True for *true no-change* data (only [9] is cited in the Introduction). However, the authors' own `novelty_map.csv` records that several cited studies ([9], [13], [14], [10]) matched or estimated false-positive rates by permutation or simulation. Rephrase: "rarely measured on *true* no-change data". |
| A2 | "ten detectors ... saw the first 3–6 fields" | S | `run_all.py` |
| A3 | "26 progressing, 26 stable" | S | `run_meta_full.json` |
| A4 | "30 patients tested weekly for 12 weeks" | P | Patient 7 has 116/175/156-day gaps (span 524 days), and several others have 14–32-day gaps (`load_artes`). |
| A5 | "263 eyes, different perimeter" | S | descriptives |
| A6 | "trend test ... 19% ... 4.4% (95% CI 2.8–6.3)" | S | metrics D1 k=3 |
| A7 | "Two detectors flagged more progressors only with excess false alarms: D6 (57%; 22.4%) and D8 (26%; 27.7%)" | P | Numbers are correct. But D2 flagged 38% with a 2.6% false-alarm rate (more than D8), so the sentence implies a general pattern that the data do not show. D8's gain over D1 (+8 points) has Holm p = 1.00. D6 was known to be invalid before the protocol (see B1). |
| A8 | "Reference-stable eyes did not reveal this: specificity 96% and 95%" | P | Correct (0.962, 0.946). "Reference-stable" means a *positive* full-series slope (`p > 0.5`) in only 26 eyes; say so. |
| A9 | "8 of 40 detector–field-number combinations had invalid false-alarm rates" | P | True under the manuscript's rule (upper CI >10% or lower CI >5%). Under the protocol's "CI upper bound vs 5%", 24/40 would be invalid, including D1 at every k. |
| A10 | "No detector with a valid false-alarm rate flagged significantly more progressors than the trend test at any number of fields" | P | True in `statistics.json`, but the McNemar tests ignore patient clustering, and with 26 progressors the test has power only for gains of about 35 points or more. |
| A11 | "The shuffle audit tracked the true false-alarm rate (Spearman ρ = 0.65; 80% within 3 pp)" | P | Numbers are correct. The pre-specified H3 required ρ ≥ 0.7 **and** most cells within 3 pp, so H3 failed. Three of the 40 cells are structural zeros (D4/D7/D10 at k=3); without them ρ = 0.56 and 78% are within 3 pp. The largest error (10.4 points) is an *under*-estimate for D8 at k=3 (17.3% vs 27.7%). |
| A12 | "Externally ... specificity 61% versus 95%" | S | metrics |
| A13 | "the largest apparent early-detection gains were false alarms that standard specificity estimates missed" | P | Holds for D6, the authors' own development variant whose inflation was already known (B1). D8's apparent gain was not significant. |
| A14 | "a simple trend test remains a strong default" | P | Not a tested hypothesis. The study did not test non-inferiority of D1; it only failed to show superiority of alternatives, with n = 26 progressors. |
| A15 | "clinics can check a detector on their own records with a shuffle audit" | U/P | The pre-specified accuracy criterion failed (A11). The audit would raise false warnings for D2 (11.7%), D7 at k=6 (11.7%) and D8 at k=6 (8.7%), and it under-estimated D8 at k=3 by 10 points. |

### Key Summary Points

| # | Claim | Verdict | Comment |
|---|---|---|---|
| K1 | "most are judged by how many eyes they flag rather than by how many of those flags are false" | U | No citation. Contradicted in part by the authors' own novelty map, where PoPLR/ANSWERS/Bayesian/GPA comparisons match specificity by permutation. |
| K2 | "...while keeping false alarms on true no-change data at the nominal 5%" | P | The validity rule actually used allows a point estimate above 5% and an upper CI up to 10% (D6 at k=5: 6.2%; D10 at k=6: 5.7% are "valid"). |
| K3 | "the two detectors that flagged the most progressors (57% and 26% versus 19%)" | **U (factual error)** | At k=3: D6 57%, **D2 38%**, D8 26%, D1 19%. Repeated in the cover letter. |
| K4 | "No detector with a valid false-alarm rate beat the simple trend test significantly ... evidence does not support replacing it" | P | Acceptable only with the power caveat. |
| K5 | "a shuffle audit of a clinic's own records is a cheap first check" | P | See A15. |

### Results

| # | Claim | Verdict | Comment |
|---|---|---|---|
| R1 | "869 eyes of 457 patients ... 132 ≥8 ... 26/26/80 ... 41 patients ... MD −4.4 (−6.0 to −3.2) ... 12.9 years ... 1.3 years (1.0–1.6) ... 6.5 years ... 300/270/240/210 windows ... 27 of 263" | S | descriptives |
| R2 | Table 1 "Octopus 900 G1, 59 analysable points" | U | Points per eye range from 10 to 59 (86/263 eyes < 59). The code reports the first eye's count. |
| R3 | Table 1 / Ethics: Artes data licence "GPL-3" | U | visualFields 1.0.7 `DESCRIPTION`: "License: Apache License 2.0". |
| R4 | "D1 kept its false-alarm rate near nominal (4.4, 3.8, 4.7, 5.1%)" | S | |
| R5 | "D6 22.4 (19.3–25.7), D8 27.7 (22.7–32.9), D9 12.7 (6.2–20.0)" | S | |
| R6 | "significantly above 5% in 4 of 8 combinations"; "D8: 27.7, 9.4, 18.8, 3.6%" | S | |
| R7 | "number of valid detectors 7, 9, 8 and 8" | P | Uses the post hoc rule (B2). |
| R8 | "per 1,000 ... 44, 224, 277" | S | |
| R9 | "Specificity ... 96% D1, 96% D6, 95% D8" | S | |
| R10 | "Two detectors could not flag any eye with three fields for structural reasons ... D10 also flagged no eye" | P | D10 is structural too (exact enumeration, p ≥ 1/6). |
| R11 | "H2 was not falsified"; "D6 +38 (19 to 58; Holm p = 0.02)" | P | Correct per file. The CIs are eye-level, not patient-level, and McNemar is unclustered. |
| R12 | "D2 38% (20–57) vs 19% (7–33), +19 (0 to 42; adj p = 0.72)" | S | |
| R13 | "D7 50% vs 42% (8, −12 to 27; p = 1.00)" | S | |
| R14 | "D8 flagged 71% with a valid false-alarm rate of 3.6%, versus 58% for D1 (12 points ...)" | P | 70.8 − 57.7 = 13. The 12 comes from majority-vote flags. "Valid" holds only under the post hoc rule (upper CI 6.0%). |
| R15 | "2 valid ... combinations had a point gain of 10 points or more" | S | D2 at k=3, D8 at k=6 |
| R16 | "D1 69% by sixth field, median 5; D6/D8 median 3 and 4; 77% and 78%" | S | The censoring rule differs from the protocol (B3). |
| R17 | Secondary reference: "sensitivity was lower for all detectors but the ranking was similar" | P | Three cells are 0 vs 0 (not lower). At k=6, D10 and D6 (43%) rank above D8 (42%) and D1 (38%). "Similar ranking" was not tested. n = 58 progressors is not reported. |
| R18 | "largest SD 13.2 points (GRU, 6 fields) and 5.1 points" | S | |
| R19 | RQ3 numbers | S | |
| R20 | "H3 was therefore partly met" | U | Protocol H3 is a conjunction ("≤3 pp for most cells **and** ρ ≥ 0.7"). It was not met. |
| R21 | "The audit identified every detector with a grossly inflated false-alarm rate" | P | "Grossly" is undefined. D9 at k=3 (12.7% true) shows 8.5% on audit, and D8 at k=3 is under-estimated by 10 points. |
| R22 | "It overestimated the false-alarm rate of rules without a p-value" | P | This assumes the Artes arm is the truth for rate rules. Weekly retest variability under-represents long-term fluctuation (acknowledged in Limitations), and D2's specificity was only 79% in GRAPE and 92% in UW reference-stable eyes. The Artes arm may therefore under-estimate the false-alarm rate of D2/D7, rather than the audit over-estimating it. |
| R23 | GRAPE paragraph (44/95; 66/61; +33 (28 to 39); D2 59/79; D4/D7 22/17; D5 41/95) | S | The CI for the +33 is an eye-level bootstrap. |

### Discussion

| # | Claim | Verdict | Comment |
|---|---|---|---|
| D-1 | "the detectors that flagged the most progressors from three fields did so mainly by flagging more of everything" | U | D2 (second-highest sensitivity) had a 2.6% true false-alarm rate. |
| D-2 | "the usual way to measure specificity ... missed this" | S | (n = 26, stable = positive slope) |
| D-3 | "no detector with a valid false-alarm rate beat the plain trend test significantly ..., in one clinic or in a second clinic using a different perimeter" | P | "Valid false-alarm rate" cannot be assessed in GRAPE (there is no Octopus no-change arm). |
| D-4 | "the borrowed distribution was too narrow; the shuffle audit and the true no-change arm both exposed this" | P | True, but this had already been established in development round 5 on the same Artes data (B1). |
| D-5 | ML mechanism: "the threshold inherits the selection of those eyes ... Specificity measured in them is therefore optimistic" | P | A plausible mechanism that was not tested. It omits a simpler contributor: the threshold is the 95th percentile of only 39 validation-stable scores. |
| D-6 | "Labels also differ ... [23]; in GRAPE, the transferred model lost 33 percentage points of specificity" | P | Implies label mismatch as the cause. The result is confounded by perimeter dB scale (D8 features include absolute mean sensitivity), variable point count (10–59), age (41 vs 59) and visit spacing. [23] compares labeling strategies; per its abstract it does not test cross-label transfer. |
| D-7 | "We extend this approach ... and add a check that any clinic can run without retest data" | P | Random re-ordering to estimate specificity is already used in [9] (1,000 reorderings per the novelty map), [13] and [14]. The new element is the *comparison* of shuffle versus true null. |
| D-8 | "a large excess is a warning sign" | P | The audit would wrongly warn for D2/D7/D8 at k=6 (A15). |
| D-9 | "the main limit to earlier detection is the number and spacing of fields, not the detector" | U | Spacing and frequency were never varied in this study. |
| D-10 | "these strategies ... are where earlier detection is likely to come from" | U | Speculative. Mark it as opinion or delete it. |
| D-11 | "Until a detector shows a valid false-alarm rate on true no-change data, a flag from it should not by itself trigger escalation" | P | Normative recommendation. Under the protocol rule, D1 itself would not qualify. |
| D-12 | Limitations: "moderate gains (around 10 points) cannot be excluded" | U | Upper 95% CI limits of valid-detector gains: D2 at k=3 **42**, D8 at k=6 **31**, D7 at k=5 **27** points. |
| D-13 | "the secondary PoPLR-based reference gave a similar ranking" | P | Not tested (R17). |
| D-14 | "the Artes data were used once during development to check false alarms" | P | Incomplete (B1). |
| D-15 | "The final test data were analysed once, as planned." / "Two amendments were made before any final result was seen" | NV | All files are dated 2026-11-23. Provide commit hashes or a public deposit. |

### Conclusion

| # | Claim | Verdict | Comment |
|---|---|---|---|
| C1 | "largest apparent gains ... came with false-alarm rates far above the nominal level, and standard specificity estimates did not reveal them" | P | See A13. |
| C2 | "No valid detector beat a simple trend test of mean sensitivity." | U as worded | It omits "significantly". Point estimates of valid detectors exceeded D1 by 19 (D2, k=3) and 13 (D8, k=6) points. |
| C3 | "clinics can screen a detector with a shuffle audit" | P | See A15 / R20. |

## B. Protocol vs Methods: deviations

| # | Protocol says | Manuscript / code does | Disclosed? |
|---|---|---|---|
| B1 | D6 = "development variant that looked more sensitive". The log (round 5) shows it was already found invalid on Artes (FPR 20–22% at k=3) | Main text: "This variant was the most sensitive approach during development"; Limitations: "Artes data were used once during development to check false alarms" | **No** (not in the main text; only in the development log, which is promised as Supplementary Note S1 but does not exist as a supplement file) |
| B2 | Validity: "FPR CI upper bound vs 5%"; RQ1 "at or below the nominal 5%" | upper CI ≤10% and lower CI ≤5% (`fill_values.py`) | **No** |
| B3 | Tests to first detection "eyes followed to 8 tests" | followed to 6, never-flagged = 7 | **No** (Methods state the rule but do not flag it as a change) |
| B4 | RQ3: Spearman ρ "(bootstrap CI)" | p-value only, no CI | No |
| B5 | H3 = both criteria | reported as "partly met" | Misreported |
| B6 | D8 features include "PoPLR S, worst region slope" | mean −log p over points; mean of the worst-decile pointwise slopes (no regions) | No |
| B7 | "All seeds reported (mean ± SD)" | seed means; only the maximum SD in the text (S1 may contain more) | Partly |
| B8 | E1/E4 "patient-cluster bootstrap"; paired effect "paired bootstrap 95% CI" | paired CIs resample eyes; McNemar unclustered; majority vote across seeds | No |
| B9 | RQ5 "clinician-applied criteria" (GRAPE) | correctly described as rule-based in the manuscript | Not flagged as a correction of the protocol |
| B10 | D5 GRAPE pool "leave-one-patient-out" | 5-fold cross-fitting | Yes (A2) |
| B11 | Artes times | donor UW spacing | Yes (A1) |
| B12 | D6/D9/D10 on GRAPE | not applied | Yes (A2) |
| B13 | D7 "short-interval (≤0.5 yr)" | same in code; Methods say "short-interval test–retest change" without the 0.5-year definition | Partly |
| B14 | none | GRAPE per-eye point exclusion (10–59 points) | No |

## C. Issues

**1. FATAL (as submitted) — The headline D6 result is presented as confirmatory, but the main text does not disclose
that it was known in advance.**
- Location: Methods, D6 ("This variant was the most sensitive approach during development"); Limitations ("the Artes
  data were used once during development to check false alarms"); Abstract and Conclusion lead results.
- Evidence: `novelty_escalation_log.md` round 5 and `results/d6_round5.json`
  (`region|detrended|lvl`: Artes FPR 0.203 at k=3, sensitivity 0.355). The log concludes that "The earlier 'valid from
  the 3rd test' gain was a false-alarm artefact".
- Consequence: the study's flagship example of an "apparent gain that was really false alarms" is a home-made,
  unpublished detector. It was entered into the benchmark *after* its invalidity was observed on the same no-change
  data used for the final evaluation, and the reader is not told this.
- Fix: state explicitly in Methods and Limitations that D6 was included as a known-anti-conservative positive control
  (its Artes FPR at k=3 was about 20% in development), and that its final result is therefore not an independent
  finding. Re-centre the Abstract on findings that were not known in advance: the D8/D9 threshold-transfer failure,
  the reference-stable specificity blind spot, and the D2/D8 external specificity loss. Supply Supplementary Note S1
  as an actual file.

**2. MAJOR — The validity rule was changed post hoc without disclosure** (B2; see review 05, issue 1).
- Fix: disclose the change, give the rationale, and add a sensitivity table under the protocol rule. Revise "8 of 40",
  "7, 9, 8 and 8" and the "valid" status of D8 at k=6 accordingly.

**3. MAJOR — A Key Summary Point and the cover letter contain a factual error.**
- Location: "the two detectors that flagged the most progressors (57% and 26% versus 19% for the trend test)".
- Fix: replace it with "the pooled-detrended conformal test and the gradient-boosted tree model flagged 57% and 26%
  ... (the MD rate rule flagged 38% with a 2.6% false-alarm rate, a non-significant difference)". Correct the cover
  letter likewise. Also revise the Discussion sentence "did so mainly by flagging more of everything" (D-1).

**4. MAJOR — The shuffle audit is promoted although its pre-specified criterion failed.**
- Location: Abstract ("tracked"), Key Summary Points, Results ("partly met"), Discussion, Conclusion.
- Fix: report "H3 was not met (ρ = 0.65 < 0.70)". Give ρ with and without the three structural-zero cells (0.56).
  State that the audit under-estimated D8 at k=3 by 10 points and would raise false warnings for D2, D7 and D8 at k=6.
  Downgrade the recommendation to "a screening heuristic that needs further validation".

**5. MAJOR — Imprecision is understated, and the conclusion omits "significantly".**
- Location: Limitations ("moderate gains (around 10 points) cannot be excluded"); Conclusion ("No valid detector beat a
  simple trend test").
- Fix: "gains of up to 30–40 percentage points (upper 95% confidence limits: D2 at three fields 42; D8 at six fields
  31) cannot be excluded". Use "no valid detector was significantly more sensitive". State in Methods that the study
  had power only for very large differences (no sample-size justification was pre-specified).

**6. MAJOR — The paired inference ignores patient clustering, contrary to the Methods** (B8; see review 05, issue 2).
- Fix: use clustered tests and CIs, or disclose the limitation.

**7. MODERATE — The validity of rate rules (D2, D7) depends on short-term noise.**
- Location: Results R22, Discussion D-8.
- Problem: the manuscript treats the Artes arm as ground truth for every detector. For rules without a p-value, the
  weekly-retest null (time stretched to 1.3-year intervals) contains no long-term fluctuation, so it may
  under-estimate their real false-alarm rate. GRAPE specificity (D2 79%) and the shuffle audit (11.7%) point the
  same way.
- Fix: present this as an alternative explanation and soften "valid" for D2/D7.

**8. MODERATE — The GRAPE specificity loss of D8 is attributed to labels without evidence** (D-6).
- Fix: list the confounders (dB scale difference between Octopus and Humphrey, point count, age, spacing) and remove
  the implied causal link to [23].

**9. MODERATE — Factual errors in data description.**
- Table 1 "59 analysable points" (R2).
- Artes licence "GPL-3" in Table 1 and in Ethical Approval. The package DESCRIPTION states Apache License 2.0 (R3).
- "12 visual fields in 12 consecutive weeks" (A4).
- Fix: correct all three.

**10. MODERATE — Novelty of the "shuffle audit" is overstated** (D-7, K1).
- Fix: cite the prior use of reordered series to estimate specificity ([9], [13], [14]; see review 08), and frame
  the contribution as the first comparison of shuffle-based against true-no-change false-alarm rates across many
  detectors (if that is indeed so).

**11. MODERATE — Unsupported clinical generalisations** (D-9, D-10).
- Fix: delete them or mark them as hypotheses.

**12. MINOR — Small reporting gaps.**
- D10 is not listed among the structural zeros (R10).
- The "12 points" vs 71 − 58 mismatch (R14).
- n = 58 for the secondary reference is not reported (R17).
- "Reference-stable" (positive slope) is not defined in plain words.
- The cover letter says "all deviations are reported".
- Fix: correct each.

**13. MINOR — The pre-registration claim cannot be verified** (D-15).
- Fix: provide commit hashes or a time-stamped public deposit, and use "pre-specified (internally time-stamped)" rather
  than implying registration.

## Recommendation

**Major revision; do not submit in the current form.** No number is fabricated. However, the main text does not
disclose that the flagship invalid detector was known to be invalid before the analysis plan. The validity rule was
silently relaxed, a Key Summary Point is factually wrong, and the conclusions about the shuffle audit and about "no
detector beat the trend test" go beyond what pre-specified criteria and n = 26 can support. All of these can be fixed
by disclosure and rewording, without new experiments, except the clustered paired tests.
