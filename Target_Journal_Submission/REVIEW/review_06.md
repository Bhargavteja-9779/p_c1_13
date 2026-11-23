# Review 06: Reproducibility

**Reviewer role:** reproducibility. Can every number be regenerated, and does the paper describe what the code does?

## Summary

The pipeline holds together. A deterministic hashed split, one raw output file (`results/raw_results.csv`, 1,106,158 rows), a summariser and a fill script with assertion-based claim checks mean that most reported numbers can be traced to code. I re-derived the key cells of Table 2, Table 3, Table S2 and the RQ3 summary from `metrics.json`, `statistics.json` and `descriptives.json`, and they match. The problems are elsewhere. Several analysis choices that drive the headline verdicts are not in the protocol or the Methods, and are not even in the analysis code: the "valid" rule exists only in the manuscript fill script. The shuffle audit as coded is not the procedure described. And the paired effect sizes are computed on a different quantity from the one shown in the tables.

## Numbers I verified (no action needed)

- Split and cohort counts: train/val/test eyes with ≥3 tests are 2,643/940/869, and the test set has 777 patients (`run_meta_full.json`, `descriptives.json`). There are 132 eyes with ≥8 tests from 69 patients: 26 progressors, 26 stable and 80 excluded.
- E2 windows: 300/270/240/210 windows × 10 draws (n = 3,000/2,700/2,400/2,100 in `metrics.json`). E3 n = 8,690 at k = 3 (869 eyes × 10).
- RQ3: ρ = 0.648, median |diff| = 0.96 pp, 80% within 3 pp, maximum 10.39 pp (`statistics.json`).
- D6 k = 3 McNemar: 10 versus 0 discordant, p = 0.00195, Holm p = 0.0176. Runtime 1,458 s ≈ 24 min. Python 3.13 is consistent with the `cpython-313` caches.
- D8 has 14 tabular features (`tab_features`, detectors.py lines 98–103). The 12-configuration grids for D8 and D9 match the Methods.

## Issues

**1. MAJOR — The validity rule behind the "Valid" column and every validity claim is in no analysis code and no protocol.**
- Location: Methods, Statistical analysis: "A detector was considered valid at a given k if … the lower limit of its false-alarm confidence interval was at or below 5% … and the upper limit did not exceed 10%". Also the Table 2 "Valid" column.
- Evidence: the rule appears only in `manuscript/fill_values.py` (`def valid(code, k): … fpr_true_null_lo <= 0.05 and fpr_true_null_hi <= 0.10`). `summarise.py` never computes validity. The protocol says only "Validity: FPR CI upper bound vs 5%." git shows `fill_values.py` was first committed at 2026‑11‑23 10:22:55, after the full results at 09:33:48.
- Fix:
  - Move the rule into `summarise.py`, so it writes a `valid` field to `metrics.json`.
  - State in Methods that this rule is an operationalisation added after the protocol.
  - Report a sensitivity analysis under the literal protocol rule (upper CI ≤ 5%). Under that rule D1 itself is invalid at every k: its upper limits are 6.27%, 6.22%, 7.50% and 8.14%.

**2. MAJOR — The D9 k = 6 validity verdict depends on a bootstrap-quantile rounding artefact.**
- Location: Results: "D9 had 5.9% (95% CI 2.3–10.0%), so both were again not valid; D9 only just exceeded the 10% upper limit."
- Evidence: `fpr_true_null_hi` = 0.100002381 in `metrics.json`. The verdict flips on 2.4 × 10⁻⁶. It is a percentile from a single bootstrap seed (`boot_prop`, seed = 0, B = 2,000), so another seed would very likely flip it.
- Fix: replace the hard CI-limit rule with a pre-stated test, for example a one-sided cluster-robust test of FA > 5%. Alternatively, report the verdict's stability over bootstrap seeds and call borderline cells "indeterminate".

**3. MAJOR — Paired differences use a different estimand from the table proportions, so the text does not reconcile with the tables.**
- Locations:
  - Results: "D8 … flagged more labelled progressors (65.9%; +25.9 percentage points …)". The table shows 65.9% against D1's 44.4%, which is a difference of 21.5 pp.
  - Results: "D6 at three tests, with a sensitivity of 56.9% … and a difference of +38.5 percentage points". 56.9 − 19.2 = 37.7.
  - Results: "At six tests, D8 detected 70.8% … (+11.5 percentage points …)". 70.8 − 57.7 = 13.1.
- Evidence: `summarise.py` lines 56–68. The tables use the seed-averaged flag (`groupby('unit').flag.mean()`). The differences and McNemar tests use `.round()`, the majority flag across seeds. Methods mentions the majority flag only for the p-values, not for the differences or their CIs.
- Fix: choose one of two options.
  - Report the majority-flag sensitivity next to each difference.
  - Compute differences on seed means, with a seed-and-cluster bootstrap.
  
  In either case, add one sentence to Methods and Table S2.

**4. MAJOR — The shuffle audit does not match its description: it includes unshuffled series and series with real trends.**
- Location: Methods E3: "we randomly re-ordered the first k tests (ten times) … Shuffling removes any true trend".
- Evidence: `run_all.py` line 81 draws `P = rng.permutation(k)` with no exclusion of the identity. The identity is drawn with probability 1/k!: 16.7% of draws at k = 3 and 4.2% at k = 4, and in those draws the series keeps its real order.
- Size of the effect: I re-ran D1 and D2 on the unshuffled first k tests of the 869 test eyes. They flag 7.2% and 15.2% at k = 3, and 12.1% and 11.2% at k = 4. So about 1.2 pp of D1's 4.8% audit rate at k = 3, and about 2.5 pp of D2's 11.7%, come from unshuffled draws.
- Fix: sample from non-identity permutations, or report audit rates restricted to non-identity draws. Rerun RQ3.

**5. MAJOR — The pipeline as documented does not regenerate the manuscript.**
- Evidence:
  - The `code/README.md` run block omits `python scripts/descriptives.py` (Table 1 and the "69% by the sixth test" figures) and `python manuscript/fill_values.py`, which generates every number in the text.
  - The `run_all.py` docstring says it "then calls src/statistics/summarise.py and src/visualization/figures.py", but `main()` does not call them.
  - `requirements.txt` gives only lower bounds (`numpy>=2.0`, `lightgbm>=4.3`, `torch>=2.3`) and has no lock file.
  - The UWHVF version (git commit of `alldata.json`) is not recorded.
  - The README gives the runtime as "~1–3 h", against 24 min reported.
- Fix:
  - List the full ordered command chain.
  - Pin exact package versions (`pip freeze` or a conda lock).
  - Record the UWHVF commit hash and SHA-256 hashes of the three input files in `run_meta`.
  - Add a `make all` or single driver script.
  - Fix the docstring and the runtime.

**6. MODERATE — LightGBM and PyTorch outputs are not guaranteed to be bit-reproducible.**
- Location: Methods: "Stochastic detectors … were run with five seeds".
- Evidence: LightGBM is fit with `random_state` but without `deterministic=True` or `num_threads` pinned. The PyTorch GRU sets no `torch.use_deterministic_algorithms`. D8 sensitivity has a seed SD of 5.0 pp at k = 3, so small numerical differences can change flags.
- Fix: set the deterministic flags, pin threads, and state the expected tolerance of reproduction.

**7. MODERATE — D4 is called stochastic but is deterministic, and the E2 design differs between detectors.**
- Location: Methods: "Stochastic detectors (D4–D6, D8–D10) were run with five seeds".
- Evidence:
  - `pvalue_within` enumerates all k! permutations for k ≤ 7, and the `rng` is unused (conformal_vf.py lines 72–79). D4's non-zero E2 "seed SD" (0.2 pp) therefore comes only from the Amendment‑A1 donor-date draws (`rng = default_rng(1000 + seed)`).
  - Deterministic detectors (D1–D3, D7) see one set of donor dates; "stochastic" ones see five. The false-alarm estimates for D1 and its comparators therefore use different numbers of donor draws.
- Fix: run every detector under all five donor-date sets. Remove D4 from the stochastic list. Report donor-draw variability separately from model-seed variability.

**8. MODERATE — Detector definitions in the Methods differ from the code.**
- D5:
  - Methods: "matched by number of tests and mean sensitivity".
  - Code: three fixed strata at <20, 20–26 and ≥26 dB (`lvl3`). Each train eye gives 20 shuffles. If a stratum has fewer than 50 values, it falls back to the pool across all strata (`ConformalCalibrator.pvalue`).
  - In GRAPE the same Humphrey-dB cut-offs are applied to another perimeter's dB scale.
- D6:
  - Methods: "worst of four regional trends".
  - Code: "central" is rows 2–5 × columns 2–6 of the 9-column grid (`make_regions`). This is not symmetric about fixation, which lies between columns 4 and 5, and left eyes are not mirrored.
- D7:
  - Methods: "beyond the 5th percentile of short-interval test–retest change in training eyes with similar sensitivity".
  - Code: limits come from single consecutive-pair differences (≤0.5 yr apart), binned in 2-dB bins of the first test of each pair. Bins with fewer than 200 pairs are dropped and filled by interpolation. The limits are then applied to the difference from a two-test mean baseline.
  - That difference has a smaller variance (≈1.5σ² against 2σ²), so D7 is conservative by construction, which may explain its 1.1–1.9% false-alarm rate.
- D8:
  - Protocol features include "PoPLR S, worst region slope". The code uses the mean −log p and the worst-decile pointwise slope.
  - Training uses only labelled train eyes with ≥8 tests (93 progressors, 99 stable; my count). The model is selected by validation AUROC.
  - The threshold is the 95th percentile of scores in **39** validation stable eyes.
  - None of this is in the paper.
- D9 and D10: undocumented details include the class-weighting (`pos_weight`), input scaling (/35), the D10 training regime (15 epochs, 31 shuffles, random windows of 3–8 tests) and the GRU input of `dt` rather than test dates.
- Fix: add a Supplementary "Implementation details" table, one row per detector, listing every constant above, and reference `detectors.py` line numbers.

**9. MODERATE — The secondary reference is under-reported and is not independent of the primary.**
- Location: "we also report a secondary reference based on PoPLR … which is not tied to mean deviation"; "Against the secondary PoPLR reference, D1 detected … (58 progressors)".
- Evidence from `raw_results.csv`, E1 at k = 3: the secondary reference has 58 progressors and 17 stable eyes. All 26 primary progressors are among the 58. None of the 26 primary-stable eyes is a PoPLR progressor, and 9 of them are indeterminate.
- Specificity against the secondary reference is never computed (`summarise.py` lines 47–50 compute only `sens_ref2`), and no paired tests are run.
- Fix: report the secondary-reference 2 × 2 cross-tabulation with the primary reference, specificity against the 17 stable eyes, and paired tests against D1.

**10. MODERATE — Pre-specified outputs that the code computes, or that the protocol requires, are missing from the paper.**
- The protocol asks for "Spearman rho across cells (bootstrap CI)". No CI is computed.
- The protocol lists GRAPE secondary labels "PLR2, PLR3, any". These are stored in `raw_results.csv` (`extra`) but never summarised.
- The protocol asks for "number of tests to first detection". This is computed (`mean_first_k_detected` in `descriptives.json`) but not reported.
- The protocol asks for "patient-cluster bootstrap". The paired-difference CIs resample eyes (`summarise.py` line 67).
- Fix: compute and report these, or list each as a deviation in a "Deviations from protocol" table.

**11. MODERATE — GRAPE preprocessing is undocumented and affects D8 transfer.**
- Location: Methods E4 and Amendment A2: "grid-agnostic features".
- Evidence (`grape.py`):
  - A location is dropped for the whole eye if it is coded −1 at any visit, so the number of points varies (mean 54.7, SD 9.3, median 59).
  - Time is taken from spreadsheet column 3 and assumed to be in years.
  - The D8 features include absolute levels (`md[-1]`, `md.mean()`), even though the amendment itself says the "dB scale differs from Humphrey".
- Fix: document these steps. Either use scale-free D8 features for transfer, or state that the GRAPE D8 result mixes threshold transfer with a dB-scale shift.

**12. MINOR — The reference standard and the detectors use two different OLS implementations.**
- Evidence: the reference uses `deferral.ols` (standard error + 1e‑9), which lives in a module from the abandoned deferral project. The detectors use `conformal_vf._ols`, whose standard error is `sqrt(s2/sxx + 1e-6)`. That floor slightly shrinks |t| for near-perfectly linear short series.
- Fix: use one function, or state the regularisation.

**13. MINOR — One Artes series is not weekly.**
- Location: "Thirty patients … had 12 visual fields in 12 consecutive weeks".
- Evidence: `load_artes()` shows one patient whose span is 524 days, with first gaps of 116, 175 and 156 days. All others span 63–105 days. This does not affect the E2 timing, because donor dates replace the real ones (A1), but it does affect the "no-change" premise for that patient's early windows.
- Fix: exclude that patient or report results with and without them, and correct the description.

**14. MINOR — The Table 1 note on Artes timing is not the timing that was analysed.**
- Location: Table 1, "Time from first to third test … 2 weeks by design".
- Evidence: the analysed timing is the donor timing, about 2.2–2.3 years.
- Fix: add a footnote.

**15. MINOR — Results are written to shared paths.**
- Evidence: `summarise.py` and `descriptives.py` overwrite shared result files, and there is no checksum manifest of `raw_results.csv`.
- Fix: add a `SHA256SUMS` file for `results/` and record it in the manuscript's Data Availability statement.
