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

| Tests | Detector | Seed SD of sensitivity, pp | Seed SD of true no-change false alarms, pp | Sensitivity, secondary PoPLR reference, % (95% CI) | Valid under strict reading (upper limit ≤5%) |
|---|---|---|---|---|---|
| 3 | D1 OLS-MD | 0.0 | 0.0 | 10.3 (3.4–18.9) | No |
| 3 | D2 MD rate | 0.0 | 0.0 | 24.1 (15.0–33.3) | Yes |
| 3 | D3 PLR-3 | 0.0 | 0.0 | 1.7 (0.0–5.7) | Yes |
| 3 | D4 PoPLR | 0.0 | 0.0 | 0.0 (0.0–0.0) | Yes |
| 3 | D5 Pooled-shuffle conformal | 0.0 | 0.4 | 10.0 (3.3–18.3) | No |
| 3 | D6 Pooled-detrended conformal | 1.7 | 0.7 | 46.2 (33.0–57.9) | No |
| 3 | D7 Event analysis | 0.0 | 0.0 | 0.0 (0.0–0.0) | Yes |
| 3 | D8 ML tabular | 5.0 | 5.1 | 24.1 (15.2–34.2) | No |
| 3 | D9 ML sequence (GRU) | 5.0 | 3.8 | 9.7 (4.1–16.0) | No |
| 3 | D10 Self-supervised order | 0.0 | 0.0 | 0.0 (0.0–0.0) | Yes |
| 4 | D1 OLS-MD | 0.0 | 0.0 | 20.7 (10.5–31.8) | No |
| 4 | D2 MD rate | 0.0 | 0.0 | 12.1 (4.8–20.7) | Yes |
| 4 | D3 PLR-3 | 0.0 | 0.0 | 10.3 (3.4–18.0) | Yes |
| 4 | D4 PoPLR | 0.0 | 0.2 | 8.6 (1.9–15.8) | Yes |
| 4 | D5 Pooled-shuffle conformal | 0.0 | 0.3 | 20.7 (10.5–31.8) | No |
| 4 | D6 Pooled-detrended conformal | 2.1 | 0.4 | 16.6 (8.2–25.4) | No |
| 4 | D7 Event analysis | 0.0 | 0.0 | 13.8 (6.4–23.3) | Yes |
| 4 | D8 ML tabular | 5.0 | 2.3 | 24.8 (14.3–36.1) | No |
| 4 | D9 ML sequence (GRU) | 3.8 | 1.5 | 7.2 (2.5–13.3) | Yes |
| 4 | D10 Self-supervised order | 4.2 | 0.6 | 12.1 (5.3–19.6) | No |
| 5 | D1 OLS-MD | 0.0 | 0.0 | 27.6 (16.7–41.1) | No |
| 5 | D2 MD rate | 0.0 | 0.0 | 13.8 (5.1–24.1) | Yes |
| 5 | D3 PLR-3 | 0.0 | 0.0 | 15.5 (7.1–25.0) | Yes |
| 5 | D4 PoPLR | 0.0 | 0.2 | 24.1 (13.3–37.7) | No |
| 5 | D5 Pooled-shuffle conformal | 0.0 | 0.2 | 27.6 (16.7–41.1) | No |
| 5 | D6 Pooled-detrended conformal | 1.7 | 0.2 | 21.0 (11.3–32.7) | No |
| 5 | D7 Event analysis | 0.0 | 0.0 | 31.0 (18.5–45.3) | Yes |
| 5 | D8 ML tabular | 2.1 | 2.2 | 38.3 (26.2–51.9) | No |
| 5 | D9 ML sequence (GRU) | 8.9 | 4.1 | 25.9 (15.3–37.5) | No |
| 5 | D10 Self-supervised order | 3.4 | 0.3 | 27.9 (17.5–40.3) | No |
| 6 | D1 OLS-MD | 0.0 | 0.0 | 37.9 (24.2–51.8) | No |
| 6 | D2 MD rate | 0.0 | 0.0 | 15.5 (7.1–24.6) | Yes |
| 6 | D3 PLR-3 | 0.0 | 0.0 | 15.5 (5.8–26.8) | Yes |
| 6 | D4 PoPLR | 0.0 | 0.2 | 36.2 (22.6–50.0) | No |
| 6 | D5 Pooled-shuffle conformal | 1.7 | 0.2 | 37.6 (24.1–51.3) | No |
| 6 | D6 Pooled-detrended conformal | 0.0 | 0.4 | 43.1 (29.8–55.7) | No |
| 6 | D7 Event analysis | 0.0 | 0.0 | 39.7 (25.0–55.4) | Yes |
| 6 | D8 ML tabular | 3.4 | 0.7 | 42.1 (29.8–54.8) | No |
| 6 | D9 ML sequence (GRU) | 13.2 | 4.2 | 21.0 (12.5–30.3) | No |
| 6 | D10 Self-supervised order | 3.2 | 0.5 | 43.1 (30.3–56.6) | No |

## Table S2. All paired comparisons with D1 (exact McNemar test, Holm correction within each number of tests and endpoint)

| Tests | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Only detector / only D1 | McNemar p | Holm p |
|---|---|---|---|---|---|---|---|
| 3 | sensitivity | D10 Self-supervised order | 26 | -19.2 (-34.6 to -3.8) | 0 / 5 | 0.062 | 0.50 |
| 3 | sensitivity | D2 MD rate | 26 | +19.2 (0.0 to 42.3) | 7 / 2 | 0.18 | 0.72 |
| 3 | sensitivity | D3 PLR-3 | 26 | -15.4 (-30.8 to -3.8) | 0 / 4 | 0.12 | 0.62 |
| 3 | sensitivity | D4 PoPLR | 26 | -19.2 (-34.6 to -3.8) | 0 / 5 | 0.062 | 0.50 |
| 3 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | sensitivity | D6 Pooled-detrended conformal | 26 | +38.5 (19.2 to 57.7) | 10 / 0 | 0.002 | 0.018 |
| 3 | sensitivity | D7 Event analysis | 26 | -19.2 (-34.6 to -3.8) | 0 / 5 | 0.062 | 0.50 |
| 3 | sensitivity | D8 ML tabular | 26 | +7.7 (-11.5 to 26.9) | 4 / 2 | 0.69 | 1.00 |
| 3 | sensitivity | D9 ML sequence (GRU) | 26 | -3.8 (-23.1 to 15.4) | 3 / 4 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D10 Self-supervised order | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D2 MD rate | 26 | +3.8 (0.0 to 11.5) | 1 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (-11.5 to 11.5) | 1 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D4 PoPLR | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D7 Event analysis | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D8 ML tabular | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | GRAPE sensitivity | D2 MD rate | 27 | +14.8 (-11.1 to 37.0) | 8 / 4 | 0.39 | 0.78 |
| 3 | GRAPE sensitivity | D3 PLR-3 | 27 | -40.7 (-63.0 to -18.5) | 1 / 12 | 0.003 | 0.014 |
| 3 | GRAPE sensitivity | D4 PoPLR | 27 | -44.4 (-63.0 to -25.9) | 0 / 12 | <0.001 | 0.003 |
| 3 | GRAPE sensitivity | D5 Pooled-shuffle conformal | 27 | -3.7 (-11.1 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | GRAPE sensitivity | D7 Event analysis | 27 | -44.4 (-63.0 to -25.9) | 0 / 12 | <0.001 | 0.003 |
| 3 | GRAPE sensitivity | D8 ML tabular | 27 | +25.9 (0.0 to 48.1) | 10 / 3 | 0.092 | 0.28 |
| 3 | GRAPE false positives | D2 MD rate | 236 | +16.5 (11.0 to 22.0) | 44 / 5 | <0.001 | <0.001 |
| 3 | GRAPE false positives | D3 PLR-3 | 236 | -0.4 (-3.8 to 2.5) | 7 / 8 | 1.00 | 1.00 |
| 3 | GRAPE false positives | D4 PoPLR | 236 | -4.7 (-7.6 to -2.1) | 0 / 11 | <0.001 | 0.004 |
| 3 | GRAPE false positives | D5 Pooled-shuffle conformal | 236 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | GRAPE false positives | D7 Event analysis | 236 | -4.7 (-7.6 to -2.1) | 0 / 11 | <0.001 | 0.004 |
| 3 | GRAPE false positives | D8 ML tabular | 236 | +33.5 (27.5 to 39.4) | 79 / 0 | <0.001 | <0.001 |
| 4 | sensitivity | D10 Self-supervised order | 26 | -11.5 (-30.8 to 3.8) | 1 / 4 | 0.38 | 1.00 |
| 4 | sensitivity | D2 MD rate | 26 | -7.7 (-23.1 to 7.7) | 1 / 3 | 0.62 | 1.00 |
| 4 | sensitivity | D3 PLR-3 | 26 | -15.4 (-34.6 to 0.0) | 1 / 5 | 0.22 | 1.00 |
| 4 | sensitivity | D4 PoPLR | 26 | -26.9 (-46.2 to -11.5) | 0 / 7 | 0.016 | 0.14 |
| 4 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | sensitivity | D6 Pooled-detrended conformal | 26 | -3.8 (-19.2 to 7.7) | 1 / 2 | 1.00 | 1.00 |
| 4 | sensitivity | D7 Event analysis | 26 | -7.7 (-26.9 to 11.5) | 2 / 4 | 0.69 | 1.00 |
| 4 | sensitivity | D8 ML tabular | 26 | +11.5 (-3.8 to 30.8) | 4 / 1 | 0.38 | 1.00 |
| 4 | sensitivity | D9 ML sequence (GRU) | 26 | -19.2 (-38.5 to 3.8) | 2 / 7 | 0.18 | 1.00 |
| 4 | false positives (1-spec) | D10 Self-supervised order | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D2 MD rate | 26 | +3.8 (0.0 to 11.5) | 1 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D8 ML tabular | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | GRAPE sensitivity | D2 MD rate | 18 | +22.2 (-5.6 to 50.0) | 6 / 2 | 0.29 | 1.00 |
| 4 | GRAPE sensitivity | D3 PLR-3 | 18 | -22.2 (-38.9 to -5.6) | 0 / 4 | 0.12 | 0.75 |
| 4 | GRAPE sensitivity | D4 PoPLR | 18 | -11.1 (-27.8 to 0.0) | 0 / 2 | 0.50 | 1.00 |
| 4 | GRAPE sensitivity | D5 Pooled-shuffle conformal | 18 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | GRAPE sensitivity | D7 Event analysis | 18 | -16.7 (-44.4 to 11.1) | 2 / 5 | 0.45 | 1.00 |
| 4 | GRAPE sensitivity | D8 ML tabular | 18 | +16.7 (-5.6 to 38.9) | 4 / 1 | 0.38 | 1.00 |
| 4 | GRAPE false positives | D2 MD rate | 145 | +9.7 (4.8 to 15.2) | 16 / 2 | 0.001 | 0.007 |
| 4 | GRAPE false positives | D3 PLR-3 | 145 | -2.1 (-6.2 to 2.1) | 3 / 6 | 0.51 | 1.00 |
| 4 | GRAPE false positives | D4 PoPLR | 145 | +0.7 (-4.1 to 5.5) | 6 / 5 | 1.00 | 1.00 |
| 4 | GRAPE false positives | D5 Pooled-shuffle conformal | 145 | +1.4 (0.0 to 3.4) | 2 / 0 | 0.50 | 1.00 |
| 4 | GRAPE false positives | D7 Event analysis | 145 | +0.0 (-4.8 to 4.8) | 6 / 6 | 1.00 | 1.00 |
| 4 | GRAPE false positives | D8 ML tabular | 145 | +14.5 (9.0 to 20.7) | 21 / 0 | <0.001 | <0.001 |
| 5 | sensitivity | D10 Self-supervised order | 26 | +7.7 (-7.7 to 23.1) | 3 / 1 | 0.62 | 1.00 |
| 5 | sensitivity | D2 MD rate | 26 | -19.2 (-38.5 to 0.0) | 1 / 6 | 0.12 | 1.00 |
| 5 | sensitivity | D3 PLR-3 | 26 | -19.2 (-34.6 to -3.8) | 0 / 5 | 0.062 | 0.56 |
| 5 | sensitivity | D4 PoPLR | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 5 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | sensitivity | D6 Pooled-detrended conformal | 26 | -11.5 (-30.8 to 7.7) | 2 / 5 | 0.45 | 1.00 |
| 5 | sensitivity | D7 Event analysis | 26 | +7.7 (-11.5 to 26.9) | 4 / 2 | 0.69 | 1.00 |
| 5 | sensitivity | D8 ML tabular | 26 | +11.5 (0.0 to 26.9) | 3 / 0 | 0.25 | 1.00 |
| 5 | sensitivity | D9 ML sequence (GRU) | 26 | +0.0 (-23.1 to 23.1) | 5 / 5 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D10 Self-supervised order | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D2 MD rate | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D8 ML tabular | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +7.7 (0.0 to 19.2) | 2 / 0 | 0.50 | 1.00 |
| 6 | sensitivity | D10 Self-supervised order | 26 | +0.0 (-19.2 to 19.2) | 3 / 3 | 1.00 | 1.00 |
| 6 | sensitivity | D2 MD rate | 26 | -34.6 (-57.7 to -15.4) | 1 / 10 | 0.012 | 0.094 |
| 6 | sensitivity | D3 PLR-3 | 26 | -34.6 (-53.8 to -19.2) | 0 / 9 | 0.004 | 0.035 |
| 6 | sensitivity | D4 PoPLR | 26 | -7.7 (-26.9 to 11.5) | 2 / 4 | 0.69 | 1.00 |
| 6 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | sensitivity | D6 Pooled-detrended conformal | 26 | -3.8 (-19.2 to 11.5) | 2 / 3 | 1.00 | 1.00 |
| 6 | sensitivity | D7 Event analysis | 26 | +0.0 (-19.2 to 15.4) | 3 / 3 | 1.00 | 1.00 |
| 6 | sensitivity | D8 ML tabular | 26 | +11.5 (-7.7 to 30.8) | 5 / 2 | 0.45 | 1.00 |
| 6 | sensitivity | D9 ML sequence (GRU) | 26 | -11.5 (-38.5 to 11.5) | 4 / 7 | 0.55 | 1.00 |
| 6 | false positives (1-spec) | D10 Self-supervised order | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D2 MD rate | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D8 ML tabular | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +7.7 (0.0 to 19.2) | 2 / 0 | 0.50 | 1.00 |

pp, percentage points. Paired comparisons use the majority flag over seeds for stochastic detectors.
