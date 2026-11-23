# Supplementary Material

Early Detection of Glaucomatous Visual Field Progression Without False Alarms: A Benchmark With True No-Change Data

## S1. Development history (all ideas tried, including failures)

The benchmark was the third framing of this project. Before it, we developed and tested on validation data only (never the locked test set) the following ideas, each with a hypothesis stated in advance. Full numbers are in the code repository (`journal_selection/novelty_escalation_log.md` and `results/pilot_*.json`, `results/d6_round5.json`).

1. Self-supervised temporal-order network as a learned permutation statistic (round 0): no gain over PoPLR or the mean-sensitivity trend; kept as detector D10.
2. Population-calibrated (pooled-shuffle) null for short series (round 1): valid false alarms, gains only at 3–4 tests; kept as D5.
3. Risk-controlled deferral of visual field tests (round 2): no gain over a simple severity rule; no deferral threshold could be certified.
4. Pooled null against a future reference (round 3): gains only at 3–4 tests, small sample.
5. A different disease area (neovascular AMD, injection rhythm and visual outcome, Moorfields open data; round 4): no added value.
6. Noise-stratified and regional detrended pooled nulls (round 5): the apparent gain at three tests was a false-alarm artefact on true no-change data (Artes); the regional variant is kept as D6.

The Artes retest data were used in round 5 only to check false-alarm rates of development variants. Because several ideas were tried, the benchmark comparisons were pre-registered and corrected for multiple comparisons (Holm), and we make no claim of a new superior method.

## S2. Protocol deviations

- Validity definition: the protocol stated that the upper confidence limit of the false-alarm rate would be compared with 5%. The manuscript draft written before the final results operationalised validity as lower limit ≤5% and upper limit ≤10%. Table S1 reports the stricter reading (upper limit ≤5%).
- The bootstrap confidence interval for the shuffle-audit correlation resamples detector × test-number cells.
- No other deviations: detectors, thresholds, references, seeds and tests were as pre-registered (amendments A1 and A2 were made before any final result).

## Table S1. Seed variability, secondary (PoPLR-based) reference and strict validity

{{SUPP_T1}}

## Table S2. All paired comparisons with D1 (exact McNemar test, Holm correction within each number of tests and endpoint)

{{SUPP_T2}}

pp, percentage points. Paired comparisons use the majority flag over seeds for stochastic detectors.
