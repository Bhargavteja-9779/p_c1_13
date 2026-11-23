# Review 05: Reproducibility and code reviewer

## Summary
I read `run_all.py`, `src/models/detectors.py`, `src/models/conformal_vf.py`, `src/statistics/summarise.py`, `src/statistics/descriptives.py` and the data loaders, and cross-checked every table cell against `results/*.json`.

The numbers in Tables 1–3 and S1–S2 reproduce exactly from the JSON files. The pipeline is compact and readable. However, several methods are described differently from how they are coded, and reproducing the results requires local data paths and two external data files that are not fetched by the code.

## Recommendation
**Major revision** (mostly fixable by correcting the text and adding a few analyses).

## Issues

1. **MAJOR – The paired-difference CIs are eye-level, not patient-level.**
   - *Location:* Methods, Statistical analysis; `summarise.py` lines 66–67.
   - *Problem:* `bs = [diff[rng.integers(0, len(diff), len(diff))].mean() …]` resamples eyes. The text says "bootstrap resamples of patients", and the protocol requires patient clusters. The single-proportion CIs (`boot_prop`) are cluster-based. The difference CIs are not.
   - *Fix:* Resample clusters in the difference bootstrap, or correct the text.

2. **MAJOR – The "stable" reference is coded as a positive slope.**
   - *Location:* Methods, Reference standard; `run_all.reference` → `deferral.ols` (`p = stats.t.cdf(b/se)`; stable if `p > 0.5`).
   - *Problem:* One-sided p > 0.5 ⇔ slope > 0. The text ("one-sided p was above 0.5") is accurate but hides that stable eyes are improving eyes.
   - *Fix:* State this explicitly, and see Review 06 for the consequences.

3. **MAJOR – Quick mode touched Artes and GRAPE before the "final run"; this contradicts the protocol and the audit.**
   - *Location:* Protocol ("GRAPE … Never used before the final run"); `leakage_audit.md` ("Quick mode … never touches the test split"); `results/run_meta_quick.json` (`n_artes: 30, n_grape: 263`); `run_all.py` lines 44–48, 72–109.
   - *Problem:* Quick mode evaluates E2 (Artes) and E4 (GRAPE, at k = 4) in full. It was committed together with the amendments (commit 60ba7b2, 09:08). The manuscript draft defining the ≤10% validity rule followed at 09:14 (commit bd2c2e2), before the full run at 09:33. The audit statement is literally true about the UW test split, but it is incomplete.
   - *Fix:* Disclose that a quick run on Artes and GRAPE (k = 4, validation-trained models) preceded the validity-rule wording, and deposit `raw_results_quick.csv`. Alternatively, show that the rule was fixed before that run.

4. **MAJOR – D4 is described as stochastic but is deterministic.**
   - *Location:* Methods ("Stochastic detectors (D4–D6, D8–D10) were run with five seeds"); D4 ("using all possible orders"); `conformal_vf.pvalue_within` (exact enumeration for k ≤ 7).
   - *Problem:* D4 has no randomness at k = 3–6. Its non-zero seed SD in Table S1 (0.2 pp) comes from different Artes donor-time draws (`rng = default_rng(1000 + seed)`), which deterministic detectors D1–D3 and D7 never receive.
   - *Fix:* Remove D4 from the stochastic set, use common donor draws for all detectors, and correct Table S1.

5. **MAJOR – The D7 implementation differs from the description in a way that makes D7 conservative.**
   - *Location:* D7 ("loss from the baseline (mean of tests 1 and 2) is beyond the 5th percentile of short-interval test–retest change"); `EventAnalysis.fit/flag`.
   - *Problem:* The limits come from single-test-to-single-test differences (variance about 2σ²). They are applied to a single test minus the mean of two baselines (variance about 1.5σ²). They are also binned by the sensitivity of the first test of each pair, but applied using the baseline mean. Both choices make the limits too wide. This plausibly explains D7's true-null false-alarm rate of 0–1.9% against a nominal ~5% per point, and its gap to the shuffle audit (up to 9.8 pp).
   - *Fix:* Derive limits from baseline-mean differences, or scale by √(1.5/2), and report the per-point false-positive rate on Artes.

6. **MODERATE – D5/D6 "matched by mean sensitivity" means three fixed tertile bins.**
   - *Location:* D5 description; `lvl3` (`np.digitize(level, [20, 26])`).
   - *Problem:* The bins are three fixed HFA-dB cut-offs, not matching. The same cut-offs are reused on GRAPE (different dB scale). The protocol also specified a leave-one-patient-out pool on GRAPE, whereas A2 and the code use 5-fold cross-fitting.
   - *Fix:* Describe the bins exactly and note the LOPO → 5-fold change as a protocol deviation.

7. **MODERATE – GRAPE D7 calibration is under-powered and extrapolated.**
   - *Location:* E4; `EventAnalysis.fit` (bins need ≥200 point-pairs, then `np.interp`).
   - *Problem:* By my count, GRAPE has only 153 visit pairs ≤0.5 years apart in total (about 120 per training fold). On the full GRAPE set, bins below 12 dB have fewer than 200 point-pairs. Within a training fold (about 80% of eyes), bins below about 14 dB fall short. Those bins receive interpolated or flat-extrapolated limits.
   - *Fix:* Report the number of pairs and bins used per fold. Consider pooling bins or using a parametric variance model.

8. **MODERATE – GRAPE points are removed per eye, so grids differ between eyes.**
   - *Location:* `grape.py` (`valid = (V >= 0).all(0)`); Data sources.
   - *Problem:* Any point coded −1 at any visit is removed for that eye. Most eyes keep 59 points, but some keep as few as 36 (my count: 5 eyes with 36 points). Rules with a fixed count ("≥3 locations") then have eye-specific stringency.
   - *Fix:* Report the distribution and do a sensitivity analysis restricted to eyes with ≥56 points.

9. **MODERATE – The environment is not self-contained.**
   - *Location:* `artes_retest.py` / `grape.py` default paths (`/home/user/p_c1_13/data_raw/...`); Data Availability.
   - *Problem:* The paths are absolute and local. There is no download script for GRAPE (figshare) or for the `visualFields` .rda file. The repository URL is a placeholder.
   - *Fix:* Add fetch scripts with checksums and environment-variable documentation, and archive the code (Zenodo DOI).

10. **MINOR – The secondary reference is computed but only partly reported.**
    - *Location:* Results ("The secondary reference … gave the same ordering"); `summarise.py` lines 47–51.
    - *Problem:* Only sensitivity is computed (58 progressors). Specificity (17 stable eyes) and paired tests are never computed.
    - *Fix:* Compute and report them.

11. **MINOR – Real-world "first flag" logic.**
    - *Location:* `descriptives.realworld`.
    - *Problem:* "Detected by test 6" counts an eye that was flagged at k = 3 and un-flagged later (D1 sensitivity at k = 6 is 57.7%, but 69.2% are "detected by 6"). This is fine for a "first alarm" metric, but the text should say so.
    - *Fix:* Add one sentence of explanation.
