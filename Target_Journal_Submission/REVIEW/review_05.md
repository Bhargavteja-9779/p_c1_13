# Review 05 — Reproducibility and code audit

Reviewer role: independent reproducibility / code auditor (adversarial).
Material audited: `code/run_all.py`, `code/src/models/{detectors,conformal_vf,deferral}.py`, `code/src/data/{uwhvf,artes_retest,grape}.py`,
`code/src/statistics/{summarise,tests,descriptives}.py`, `manuscript/fill_values.py`, `code/tests/test_core.py`,
`code/experiments/protocol.md`, `code/experiments/leakage_audit.md`, `results/*.json`, `tables/*.csv`.
What I ran: read-only Python on the three public data sets and the result files; `python -m pytest -q tests`
(5 passed in 0.6 s). I did not re-run the 24-minute benchmark, and I ran no git commands, so I could not check commit timestamps.

## Summary

The pipeline is compact and mostly does what the Methods say. The patient-level hash split is deterministic and
correct (60/20/20 realised as 59.5/20.5/20.1% of patients; both eyes always in one split). E1–E3 use the locked test split
only. Calibration pools and ML thresholds use train/validation data only. Every number I checked in the manuscript
matches `metrics.json`, `statistics.json` or `descriptives.json` (spot checks: Table 2 all cells, D6/D2/D8 paired
differences, RQ3 numbers, tests-to-first-detection, Table 1 counts).

The audit did find problems that affect what the numbers mean:
1. The validity rule that classifies detectors as "valid" or "invalid" is implemented only in `manuscript/fill_values.py`.
   It is looser than the rule in the protocol, and it changes which cells count as valid, including D1 and D8 at six fields.
2. The paired-difference CIs and the McNemar tests ignore patient clustering, although the Methods say the CIs come
   from a patient bootstrap.
3. For GRAPE, the number of analysable points varies by eye (10 to 59), but Table 1 reports "59 analysable points".
4. The "true no-change" arm contains a series that is not 12 weekly fields.
5. D10 is described as failing at three fields for no stated reason, but it hits the same exact-permutation floor as PoPLR.
6. Several Methods descriptions differ from the code in small but reportable ways.
7. Some reproducibility metadata is missing: pinned versions, data checksums, saved models and a complete run script.

## Detector-by-detector check (Methods vs code)

| ID | Methods text | Code (`detectors.py`) | Verdict |
|---|---|---|---|
| D1 | OLS slope of mean sensitivity, one-sided t, p<0.05 | `stats.t.cdf(-stat_md)` with df=k−2; mean over 52 points | Matches |
| D2 | slope ≤ −1 dB/yr | `md_slope(t,Y)[0] <= -1.0` (mean sensitivity, not MD) | Matches the Methods; the label "MD rate" is a misnomer because it is mean sensitivity (MINOR) |
| D3 | ≥3 locations slope ≤ −1 and p<0.01 | one-sided t, df=k−2 | Matches |
| D4 | PoPLR, all orders | `pvalue_within`, exact enumeration for k≤7, Fisher −Σlog p | Matches. Deterministic for k≤6, yet listed in `STOCHASTIC` and run 5 times (harmless) |
| D5 | shuffled train series matched on k and mean sensitivity | `ConformalCalibrator(null='shuffle', n_null=20, strata=lvl3)`; tertiles <20/20–26/≥26 dB; falls back to the pooled-k reference if a stratum has <50 values | Matches. The fallback is not described (MINOR) |
| D6 | worst of four regional trends; reference from detrended shuffled series | `stat_region` max of 4 regional t-stats; `detrended_shuffle` removes each **training** eye's own full OLS trend and permutes residuals | Implemented as described. See issue 9 on the "Freedman–Lane" label |
| D7 | 5th percentile of short-interval test–retest change in training eyes with similar sensitivity; baseline mean of tests 1–2; ≥3 points on 2 consecutive follow-ups | "short interval" = consecutive tests ≤0.5 **years** apart; limits from single-test differences binned by the earlier test's value (2-dB bins, ≥200 pairs, interpolated) and applied to (test − mean of 2 baseline tests) | Partly matches. Details are not disclosed (issue 8) |
| D8 | LightGBM, 14 summary features, threshold at 95% specificity on validation reference-stable eyes | 14 features confirmed; per-k model chosen by validation AUC from 12 configs; threshold = 95th percentile of scores in **39** validation-stable eyes; trained on **192** labelled train eyes (93 progressors) | Matches. Sample sizes are not reported (issue 7) |
| D9 | GRU on raw fields + intervals, same labels/threshold/budget | 12-config grid (h×lr×epochs); `pos_weight` class weighting; Y/35 scaling | Matches. Class weighting is not reported |
| D10 | self-supervised order net used as a PoPLR-type permutation statistic | contrastive true-vs-31-shuffles loss; `pvalue_within` with exact enumeration | Matches. Its p-value floor is 1/6 at k=3 (issue 5) |

## Evaluation check

- **E1:** test eyes with ≥8 tests; the primary reference uses the mean-TD slope over the whole series (`run_all.reference`).
  The code applies the stable rule of "one-sided p>0.5" exactly as the protocol says. Note that this means a **positive**
  estimated full-series slope (see issue 10).
- **E2:** 30 eyes × (12−k+1) windows × 10 donor time vectors drawn from UW **test** eyes with ≥k tests. Only the times
  are borrowed, so there is no outcome leakage. The donor RNG (`default_rng(1000+seed)`) is re-created for each detector,
  so donor draws are paired across detectors for a given seed. Correct.
- **E3:** 10 random permutations of the first k tests of every test eye with ≥k tests (8,690 rows at k=3). Correct.
- **E4:** Five-fold patient-level cross-fitting with `sha256('grape'+pid) % 5`. D8 is fitted once on UWHVF and transferred.
  D1–D4 have no-op `fit`. Label = `MD` column. Matches amendment A2.

## Statistics check

- `summarise.boot_prop`: cluster bootstrap over patients for E1–E4 proportions, with per-unit seed means. Correct as
  described. `cluster_of` correctly strips L/R and OD/OS.
- Holm correction is over 9 comparisons per k for UWHVF and 6 per k for GRAPE, separately for each endpoint. Matches.
- Seeds: 5 seeds (0–4) for stochastic detectors; `set_seed` + LightGBM `random_state` + `torch.manual_seed`.
  Deterministic torch algorithms are not enforced (MINOR).
- **Tests to first detection** (`descriptives.real_world`): for each detector and seed, the first k∈{3,4,5,6} with a
  flag, set to 7 if there is none. The code then takes the median within each seed and the median of those medians
  across seeds. The calculation is correct, but the definition differs from the protocol (issue 4).

## Issues

**1. MAJOR — The validity rule in the code is looser than the protocol rule, and the change is not disclosed.**
- Location: Methods, Statistical analysis: "A detector was considered valid if the upper limit of its false-alarm
  confidence interval on true no-change data did not exceed 10% and its point estimate did not exceed 5% by more than
  sampling error". Code: `fill_values.py`: `M['valid'] = (M.fpr_true_null_hi <= 0.10) & (M.fpr_true_null_lo <= 0.05)`.
  Protocol: "Validity: FPR CI upper bound vs 5%." RQ1: "keep the false-alarm rate ... at or below the nominal 5%".
- Problem: the rule lives in the manuscript-filling script, not in `src/`, and it is not listed as an amendment.
- Effect: read literally, the protocol rule (CI upper ≤5%) leaves 5/5/3/3 valid detectors at k=3/4/5/6, not 7/9/8/8.
  D1 itself would be invalid at every k (upper limits 6.3, 6.2, 7.5, 8.1%). D8 at k=6 would also be invalid (upper
  limit 6.0%), and D8 at k=6 is the manuscript's one example of a "valid" ML gain.
- Fix: state the protocol rule, explain why it cannot be met with 30 patients (D1's CI cannot sit below 5% when the
  true rate is 5%), and report the new rule as a dated, post hoc deviation. Show results under both rules in a
  supplementary table, and move the rule into `src/statistics`.

**2. MAJOR — Paired differences and McNemar tests are not clustered by patient, contrary to the Methods wording.**
- Location: `summarise.py` lines in the paired-tests loop: `bs = [diff[rng.integers(0, len(diff), len(diff))].mean() ...]`
  resamples **eyes**. `mcnemar()` treats eyes as independent.
- Problem: the 26+26 reference eyes come from 41 patients, and the 263 GRAPE eyes from 144 patients. The Methods
  imply patient-level resampling ("bootstrap resamples of patients, which accounts for two eyes per patient"), and the
  abstract's key D6 result (38 points, 95% CI 19 to 58; Holm p = 0.02) comes from the unclustered procedure.
- Fix: resample patients and recompute the mean paired difference. Replace McNemar with a cluster-adjusted test (for
  example, a patient-level permutation of detector labels, or the Obuchowski / Durkalski clustered McNemar). Otherwise,
  state plainly that the paired tests ignore clustering.
- A second inconsistency: the paired tests use the **majority vote across seeds** (`.mean().round()`), whereas the
  point estimates use seed means. This produces the visible mismatch "D8 flagged 71% ... versus 58% for D1 (12
  points ...)", where 71 − 58 = 13. Disclose it in Methods, or use seed-mean differences throughout.

**3. MODERATE — GRAPE: the number of analysable points varies by eye, but Table 1 reports one number.**
- Location: Table 1, "Octopus 900 G1, 59 analysable points". `grape.py`: `valid = (V >= 0).all(0)` is computed
  **per eye**. `descriptives.grape_block` reports `G[0]['sens'].shape[1]`, the count for the first eye only.
- Data: the number of analysable points ranges from 10 to 59 (median 59). 86/263 eyes have fewer than 59 and 43 have
  fewer than 50. As a result, D3 (a count of ≥3 points), D7 and the D8 features see a different grid in each eye.
- Fix: report the distribution. Then either restrict to points valid in all eyes, or justify per-eye exclusion and
  run a sensitivity analysis on eyes with all 59 points.

**4. MODERATE — Tests to first detection: the censoring rule differs from the protocol.**
- Location: Methods "(followed until six fields; eyes not flagged by six fields were counted as seven)". Protocol:
  "number of tests to first detection among reference progressors (eyes followed to 8 tests)". The docstring of
  `descriptives.py` still calls these measures "pre-registered".
- Notes: the "first flag" is the first k with a flag. Flags are not monotone in k (D8 uses a separate model and
  threshold for each k), so "flagged by six fields" counts eyes flagged at any k ≤ 6, even if they were not flagged at
  larger k. For stochastic detectors the reported value is a median of per-seed medians.
- Fix: list this as a deviation, state the non-monotonicity, and report the mean with censoring (already computed as
  `mean_first_capped7`) or Kaplan–Meier-type curves.

**5. MODERATE — D10's failure at k=3 is structural but is presented as if it were not.**
- Location: Results: "Two detectors could not flag any eye with three fields for structural reasons ... The
  self-supervised order network (D10) also flagged no eye with three fields."
- Problem: D10 uses `pvalue_within` with exact enumeration, so its minimum p is 1/6, the same as D4. Its zero
  sensitivity and zero false-alarm rate at k=3 are therefore guaranteed, not an empirical finding. These three
  structural-zero cells (D4, D7, D10 at k=3) also inflate the RQ3 agreement statistics. Without them: Spearman ρ =
  0.56 (not 0.65), and 78% of cells are within 3 points.
- Fix: list D10 among the structural cases. Report RQ3 with and without structural-zero cells.

**6. MODERATE — The true no-change arm contains a series that is not 12 weekly fields.**
- Location: Methods: "Thirty patients ... had 12 visual fields in 12 consecutive weeks". Abstract: "tested weekly
  for 12 weeks".
- Data (`load_artes`): patient 7 has intervals of 116, 175 and 156 days before the weekly block, a 524-day span in
  all. Several others have 14–32-day gaps. Because A1 replaces the times, this hardly affects the detector inputs. It
  does undermine the claim "Glaucoma does not change in 12 weeks" for patient 7's early windows.
- Fix: report the spans, and either exclude windows of patient 7 that span >12 weeks or run a sensitivity analysis.

**7. MODERATE — Key ML sample sizes and design details are not reported.**
- D8 and D9 are trained on 192 labelled train eyes (93 progressors / 99 stable). The 95%-specificity threshold is
  the 95th percentile of scores in only **39** validation-stable eyes, which is essentially the second-highest score.
  This imprecision is a plausible cause of the "erratic" false-alarm rates (27.7, 9.4, 18.8, 3.6%), and readers need
  these numbers to interpret them.
- Model selection is by validation AUC on the same 70 validation eyes that set the threshold.
- D9 uses class weighting (`pos_weight`). The trained models are not saved or released.
- Fix: report these numbers, release the fitted models (or a script that regenerates them deterministically), and
  add a bootstrap of the threshold.

**8. MODERATE — The D7 description differs from the code.**
- "Short-interval test–retest change" in the code means consecutive clinical tests up to 6 months apart, in a
  population that includes progressing eyes. The limits come from single-test differences (variance ≈ 2σ²) but are
  applied to differences from a 2-test baseline mean (≈1.5σ²). Both choices make D7 conservative.
- The GPA analogue uses sensitivity, not pattern deviation. A rule of "≥3 points on 2 consecutive" corresponds to
  GPA "possible", not "likely", progression.
- On GRAPE, only 153 short-interval visit pairs exist, and only 10 of the 21 sensitivity bins reach the 200-pair
  minimum (fewer within each cross-fitting fold). The other bins are interpolated or extrapolated.
- Fix: describe these choices in Methods and add them to Limitations.

**9. MINOR — D6 is called "Freedman–Lane" in code and citation, but that is not what it does.**
- `conformal_vf.detrended_shuffle` says "Freedman-Lane-type null: remove the eye's own pointwise OLS trend". Freedman–Lane
  permutes residuals of the **reduced** (null) model, which here is the mean only. Removing the full-model trend is
  closer to ter Braak's residual permutation.
- This matters because it explains the anti-conservatism at k=3: one residual df gives a null reference that is too
  narrow, which the Discussion correctly identifies.
- Fix: relabel the method and correct the citation (see review 08).

**10. MINOR — The "stable" reference class means a positive full-series slope.**
- `reference()`: `0 if p > 0.5`, where p is the one-sided p for a negative slope. p > 0.5 if and only if the slope
  is > 0. So "reference-stable" eyes are eyes whose MD improved over about 13 years.
- Problem: this is a highly selected group. It is the mechanism behind "specificity in reference-stable eyes did not
  reveal this".
- Fix: state the definition in plain words in Methods and in the Table 2 footnote.

**11. MINOR — The reproducibility metadata is incomplete.**
- (a) `requirements.txt` uses `>=` bounds and `environment.yml` pins Python 3.12, whereas the manuscript says Python
  3.13. Neither gives exact versions of LightGBM or PyTorch. Provide a lock file (`pip freeze`) from the run that made
  `raw_results.csv.gz`.
- (b) No checksums (SHA-256) are given for `alldata.json`, `vfpwgRetest24d2.rda` and `vf_clinical.xlsx`, and the
  UWHVF commit is not recorded. Add them.
- (c) The README run sequence omits `python -m src.statistics.descriptives` and `manuscript/fill_values.py`.
  `summarise.py` defaults to `results/raw_results.csv`, but only `raw_results.csv.gz` is shipped. The README says
  "~1–3 h", while the manuscript says 24 min. "Four CPU cores" is not recorded in `run_meta_full.json`. Add a single
  `make all` / `run_everything.sh` and record hardware in `run_meta`.
- (d) The tests cover only OLS, the permutation floor, one conformal null, Holm and the bootstrap. There are no tests
  for D5–D10, E2 window construction, `cluster_of`, the validity rule or `real_world()`. Add at least smoke tests.

**12. MINOR — The pre-registration claim cannot be verified from the files.**
- `protocol.md` is dated "2026-11-23", the same day as both amendments, the leakage audit and all result files. I was
  not permitted to inspect git history.
- Fix: cite the commit hash and timestamp of `protocol.md` and of the first full run, or deposit the protocol
  (OSF / Zenodo) before submission.

**13. MINOR — The secondary reference is incompletely reported.**
- `sens_ref2` is computed over **58** PoPLR-reference progressors, more than twice the 26 primary progressors, because
  E1 includes eyes that are indeterminate on the primary reference. No specificity against PoPLR-stable eyes is
  computed.
- Fix: report the n and the specificity.

## Recommendation

**Major revision.** The code is honest and reproducible in outline, and the headline numbers are computed as stated.
The validity rule was changed post hoc without disclosure, and the paired inference ignores clustering. Both affect
which detectors are called valid and which comparisons are called significant. Fix issues 1–2 before submission and
disclose issues 3–8 in the text.
