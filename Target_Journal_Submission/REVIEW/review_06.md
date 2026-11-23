# Review 06 — Reproducibility / code reviewer

## Summary
I ran the unit tests, re-ran the statistics stage on the released raw results, re-ran the full benchmark in a scratch copy, and compared the Methods text with the code (`run_all.py`, `src/models/detectors.py`, `src/models/conformal_vf.py`, `src/statistics/summarise.py`, `src/statistics/describe.py`, `manuscript/fill_values.py`). The code is compact and readable. Number provenance via `fill_values.py` is a strength. Several Methods statements, however, do not describe what the code does, and the tests cover almost none of the analysis logic.

**Recommendation: Major revision.**

## What I ran
- `cd code && python -m pytest -q tests` → **5 passed in 0.81 s** (Python 3.13.18).
- `python -m src.statistics.summarise` on a scratch copy of `results/raw_results.csv.gz` → `metrics.json` and `statistics.json` **identical** to the released files.
- `python run_all.py --mode full` in a scratch copy (4 cores, shared with another concurrent job): the run executed without error through D1–D7, with UWHVF, Artes and GRAPE all loading from the default paths. I stopped it during D8 because LightGBM took about 22 min per seed under CPU contention. `run_all.py` writes raw output only at the end, so I could not compare partial raw flags with the released file. **An end-to-end bit-for-bit reproduction of the raw results is therefore NOT verified by this reviewer.** The authors should provide a checksum of `raw_results.csv.gz` and the expected runtime per detector. (The README says "1–3 h", while the manuscript gives 1,458 s.)

## Issues

1. **MAJOR — The test suite does not test the analysis (code/tests/test_core.py).** The five tests cover OLS slope, the k = 3 permutation floor, one conformal validity simulation, Holm and a bootstrap smoke test. Nothing tests:
   - D2, D3 or D6–D10;
   - the reference definition (`run_all.reference`);
   - the Artes windowing and A1 time-label assignment;
   - GRAPE cross-fitting;
   - `summarise.py` (cluster IDs, majority vote, McNemar, specificity inversion);
   - `describe.py` (tests to first flag);
   - the validity rule in `fill_values.py`.

   *Fix:* add tests for each, including a regression test that rebuilds Table 1 from a small fixture.

2. **MAJOR — Methods text vs code: majority vote (Methods "Statistical Analysis"; `summarise.py` "paired tests vs D1 (seed-0 flags; stochastic detectors use majority over seeds)").** The Methods say proportions are means over seeds and describe McNemar tests on "the same eyes". The code tests majority-vote flags. As a result, the reported differences do not equal the differences of the reported proportions (e.g., +38.5 vs 37.7 pp for D6 at k = 3; +25.9 vs 21.5 for GRAPE D8). Note also that the code comment says "seed-0 flags" while the code uses `.mean().round()`. *Fix:* align code, comment and Methods.

3. **MAJOR — Methods text vs code: the paired bootstrap is not patient-level.** Methods: "95% CIs from 2,000 bootstrap resamples of patients". `summarise.py` resamples eyes for paired differences (`diff[rng.integers(0, len(diff), len(diff))]`). Only `boot_prop` is cluster-level. *Fix:* implement a cluster bootstrap for the differences.

4. **MAJOR — The validity rule is in the manuscript filler, not the analysis code (`manuscript/fill_values.py::valid`).** A primary decision rule should live in the analysis package and be written to the results JSON. Today the "Valid" column exists only in the rendered manuscript. *Fix:* move it to `summarise.py`, write `valid` into `metrics.json`, and test it.

5. **MAJOR — The claim that one command reproduces everything is false (Methods last sentence of "Statistical Analysis").** `run_all.py --mode full` writes `raw_results.csv` (uncompressed) and `run_meta_full.json`. Its docstring says it then calls `summarise.py` and `figures.py`, but the code does not. `describe.py` reads `raw_results.csv.gz`, which `run_all.py` never writes. `fill_values.py` and `build_docx.py` are separate. The README omits `describe.py` and `fill_values.py`. *Fix:* add a `make`-style driver that runs all steps in order, and fix the docstring and README.

6. **MAJOR — Quick mode touches the external and true-null data (`run_all.py`, `if quick:` block; README "pipeline check on a validation subset").** Quick mode replaces only the UWHVF test split. It still computes E2 on all Artes windows and E4 on all GRAPE eyes with their labels. This contradicts the Methods ("GRAPE [was] not used before the final run") and the leakage-audit row "Quick mode ... OK". *Fix:* make quick mode skip E2 and E4, or use synthetic data. Disclose that the earlier quick run touched these data.

7. **MODERATE — D4 is labelled stochastic but is exact.** `pvalue_within` enumerates all permutations for k ≤ 7, so D4's `rng` is unused. Running D4 over five seeds changes only the Artes time-label draws (`rng = np.random.default_rng(1000 + seed)` in `run_all.py`). *Fix:* remove D4 from `STOCHASTIC`.

8. **MODERATE — Time-label draws are not shared across detectors.** Each detector-seed pair re-creates `rng(1000 + seed)` and consumes draws. Deterministic detectors see only the seed-0 draws; stochastic detectors average over five draw sets. The E2 comparisons between detectors are therefore not on identical windows. *Fix:* pre-generate the donor assignment once (saved to disk) and reuse it for all detectors.

9. **MODERATE — Protocol vs code: D8 features.** The protocol lists "PoPLR S, worst region slope". `tab_features` uses the mean −log p across points (not a permutation PoPLR S) and the mean of the lowest 10% pointwise slopes (not a region slope). *Fix:* list the 14 features in the Supplement and record the deviation.

10. **MODERATE — Protocol vs code: D7 limits.** The protocol says "short-interval (≤ 0.5 yr) test-pair differences ... binned by baseline sensitivity". The code bins by the first test of each pair and interpolates bins with < 200 pairs. Both choices are undocumented, and the limits are applied to change from a mean of two baselines (see review 03 #1). *Fix:* document this and report bin counts.

11. **MODERATE — Hard-coded data paths and unpinned dependencies.** The loaders default to `/home/user/p_c1_13/data_raw/...` (they can be overridden by environment variables). `requirements.txt` uses `>=` only, and LightGBM and PyTorch results are version-sensitive. *Fix:* pin exact versions (a lock file or `environment.yml` with versions) and record data checksums (SHA-256 of `alldata.json`, the `.rda` and the `.xlsx`).

12. **MODERATE — Quick-run artefacts are missing.** `results/run_meta_quick.json` is committed, but `raw_results_quick.csv` is not present. *Fix:* commit it, or state that it was deleted and why.

13. **MINOR — "The full run took 1,458 seconds on a four-core CPU" (Results "Study Data").** The runtime is in `run_meta_full.json`; the hardware is not recorded. *Fix:* record the hardware in the run metadata.

14. **MINOR — GRAPE per-eye point removal** (`valid = (V >= 0).all(0)` per eye) can produce different point counts per eye. *Fix:* assert 59 points, or document it.

15. **MINOR — The secondary-reference sensitivity has no seed SD.** `summarise.py` does not compute `sens_ref2_seed_sd`, although the protocol requires the seed SD. *Fix:* add it.
