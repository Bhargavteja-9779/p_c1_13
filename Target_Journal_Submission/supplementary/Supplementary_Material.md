# Supplementary Material

**How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm**

## S1 Development history: ideas tried and abandoned

Before the final protocol, we tried to develop a new detection method. All development used the UWHVF training and validation sets only; the test set was locked. The full log, with every hypothesis, falsifier and result file, is in the code repository (`journal_selection/novelty_escalation_log.md`; result files `results/pilot_v0.json`, `pilot_v1.json`, `pilot_deferral.json`, `pilot_v2.json`, `d6_round5.json`). In summary:

- **Round 0.** A self-supervised network that recognises the true time order of tests, used as a within-eye permutation statistic (D10 in the final benchmark). It did not flag more eyes than PoPLR or the mean-sensitivity trend. Abandoned as a new method.
- **Round 1.** A pooled ("population-calibrated") null built from shuffled series of other eyes, to allow valid tests with three fields (D5 in the final benchmark). Gains were small and limited to three or four tests.
- **Round 2.** Reformulation as risk-controlled deferral of visual-field tests. Deferral rules delayed detection in most progressing eyes, and the risk-control procedure could not certify any useful threshold. Abandoned.
- **Round 3.** Pooled-detrended null against a future reference in the validation set. It appeared more sensitive at three and four tests.
- **Round 4.** A different clinical problem (anti-VEGF treatment rhythm in neovascular AMD, Moorfields open data). Treatment rhythm added no prognostic value. Abandoned.
- **Round 5.** The pooled-detrended variants (D6 in the final benchmark) were checked on the Artes retest data. They raised far more false alarms than the nominal 5%. This led to the final research question: whether apparent early-detection gains are explained by false alarms. This is the one development use of the Artes data, disclosed in the main text.

Ideas counted: six rounds, nine candidate method variants. Because no development idea is claimed as a new method, the final benchmark tests all ten detectors with Holm correction within each number of tests.

## S2 Sensitivity against the secondary (PoPLR-based) reference

**Table S2** Sensitivity, % (95% CI), against the secondary reference (full-series PoPLR p < 0.01)

| Detector | 3 tests | 4 tests | 5 tests | 6 tests |
|---|---|---|---|---|
| D1 OLS-MD | 10.3 (3.4–18.9) | 20.7 (10.5–31.8) | 27.6 (16.7–41.1) | 37.9 (24.2–51.8) |
| D2 MD rate | 24.1 (15.0–33.3) | 12.1 (4.8–20.7) | 13.8 (5.1–24.1) | 15.5 (7.1–24.6) |
| D3 PLR-3 | 1.7 (0.0–5.7) | 10.3 (3.4–18.0) | 15.5 (7.1–25.0) | 15.5 (5.8–26.8) |
| D4 PoPLR | 0.0 (0.0–0.0) | 8.6 (1.9–15.8) | 24.1 (13.3–37.7) | 36.2 (22.6–50.0) |
| D5 Pooled-shuffle conformal | 10.0 (3.3–18.3) | 20.7 (10.5–31.8) | 27.6 (16.7–41.1) | 37.6 (24.1–51.3) |
| D6 Pooled-detrended conformal | 46.2 (33.0–57.9) | 16.6 (8.2–25.4) | 21.0 (11.3–32.7) | 43.1 (29.8–55.7) |
| D7 Event analysis | 0.0 (0.0–0.0) | 13.8 (6.4–23.3) | 31.0 (18.5–45.3) | 39.7 (25.0–55.4) |
| D8 ML tabular (LightGBM) | 24.1 (15.2–34.2) | 24.8 (14.3–36.1) | 38.3 (26.2–51.9) | 42.1 (29.8–54.8) |
| D9 ML sequence (GRU) | 9.7 (4.1–16.0) | 7.2 (2.5–13.3) | 25.9 (15.3–37.5) | 21.0 (12.5–30.3) |
| D10 Self-supervised order net | 0.0 (0.0–0.0) | 12.1 (5.3–19.6) | 27.9 (17.5–40.3) | 43.1 (30.3–56.6) |

n = 58 secondary-reference progressors in the UWHVF test set. Mean over seeds for stochastic detectors.

## S3 All paired comparisons with D1

**Table S3** Paired comparisons with D1 (exact McNemar test, Holm correction within number of tests and endpoint)

| Tests | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Flagged only by detector / only by D1 | p | Holm p |
|---|---|---|---|---|---|---|---|
| 3 | GRAPE false positives | D2 MD rate | 236 | +16.5 (11.0 to 22.0) | 44 / 5 | < 0.001 | < 0.001 |
| 3 | GRAPE false positives | D3 PLR-3 | 236 | -0.4 (-3.8 to 2.5) | 7 / 8 | 1.00 | 1.00 |
| 3 | GRAPE false positives | D4 PoPLR | 236 | -4.7 (-7.6 to -2.1) | 0 / 11 | < 0.001 | 0.004 |
| 3 | GRAPE false positives | D5 Pooled-shuffle conformal | 236 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | GRAPE false positives | D7 Event analysis | 236 | -4.7 (-7.6 to -2.1) | 0 / 11 | < 0.001 | 0.004 |
| 3 | GRAPE false positives | D8 ML tabular (LightGBM) | 236 | +33.5 (27.5 to 39.4) | 79 / 0 | < 0.001 | < 0.001 |
| 3 | GRAPE sensitivity | D2 MD rate | 27 | +14.8 (-11.1 to 37.0) | 8 / 4 | 0.39 | 0.78 |
| 3 | GRAPE sensitivity | D3 PLR-3 | 27 | -40.7 (-63.0 to -18.5) | 1 / 12 | 0.003 | 0.014 |
| 3 | GRAPE sensitivity | D4 PoPLR | 27 | -44.4 (-63.0 to -25.9) | 0 / 12 | < 0.001 | 0.003 |
| 3 | GRAPE sensitivity | D5 Pooled-shuffle conformal | 27 | -3.7 (-11.1 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | GRAPE sensitivity | D7 Event analysis | 27 | -44.4 (-63.0 to -25.9) | 0 / 12 | < 0.001 | 0.003 |
| 3 | GRAPE sensitivity | D8 ML tabular (LightGBM) | 27 | +25.9 (0.0 to 48.1) | 10 / 3 | 0.092 | 0.28 |
| 3 | false positives (1-spec) | D2 MD rate | 26 | +3.8 (0.0 to 11.5) | 1 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (-11.5 to 11.5) | 1 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D4 PoPLR | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D7 Event analysis | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D8 ML tabular (LightGBM) | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D10 Self-supervised order net | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | sensitivity | D2 MD rate | 26 | +19.2 (0.0 to 42.3) | 7 / 2 | 0.18 | 0.72 |
| 3 | sensitivity | D3 PLR-3 | 26 | -15.4 (-30.8 to -3.8) | 0 / 4 | 0.12 | 0.62 |
| 3 | sensitivity | D4 PoPLR | 26 | -19.2 (-34.6 to -3.8) | 0 / 5 | 0.062 | 0.50 |
| 3 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | sensitivity | D6 Pooled-detrended conformal | 26 | +38.5 (19.2 to 57.7) | 10 / 0 | 0.002 | 0.018 |
| 3 | sensitivity | D7 Event analysis | 26 | -19.2 (-34.6 to -3.8) | 0 / 5 | 0.062 | 0.50 |
| 3 | sensitivity | D8 ML tabular (LightGBM) | 26 | +7.7 (-11.5 to 26.9) | 4 / 2 | 0.69 | 1.00 |
| 3 | sensitivity | D9 ML sequence (GRU) | 26 | -3.8 (-23.1 to 15.4) | 3 / 4 | 1.00 | 1.00 |
| 3 | sensitivity | D10 Self-supervised order net | 26 | -19.2 (-34.6 to -3.8) | 0 / 5 | 0.062 | 0.50 |
| 4 | GRAPE false positives | D2 MD rate | 145 | +9.7 (4.8 to 15.2) | 16 / 2 | 0.001 | 0.007 |
| 4 | GRAPE false positives | D3 PLR-3 | 145 | -2.1 (-6.2 to 2.1) | 3 / 6 | 0.51 | 1.00 |
| 4 | GRAPE false positives | D4 PoPLR | 145 | +0.7 (-4.1 to 5.5) | 6 / 5 | 1.00 | 1.00 |
| 4 | GRAPE false positives | D5 Pooled-shuffle conformal | 145 | +1.4 (0.0 to 3.4) | 2 / 0 | 0.50 | 1.00 |
| 4 | GRAPE false positives | D7 Event analysis | 145 | +0.0 (-4.8 to 4.8) | 6 / 6 | 1.00 | 1.00 |
| 4 | GRAPE false positives | D8 ML tabular (LightGBM) | 145 | +14.5 (9.0 to 20.7) | 21 / 0 | < 0.001 | < 0.001 |
| 4 | GRAPE sensitivity | D2 MD rate | 18 | +22.2 (-5.6 to 50.0) | 6 / 2 | 0.29 | 1.00 |
| 4 | GRAPE sensitivity | D3 PLR-3 | 18 | -22.2 (-38.9 to -5.6) | 0 / 4 | 0.12 | 0.75 |
| 4 | GRAPE sensitivity | D4 PoPLR | 18 | -11.1 (-27.8 to 0.0) | 0 / 2 | 0.50 | 1.00 |
| 4 | GRAPE sensitivity | D5 Pooled-shuffle conformal | 18 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | GRAPE sensitivity | D7 Event analysis | 18 | -16.7 (-44.4 to 11.1) | 2 / 5 | 0.45 | 1.00 |
| 4 | GRAPE sensitivity | D8 ML tabular (LightGBM) | 18 | +16.7 (-5.6 to 38.9) | 4 / 1 | 0.38 | 1.00 |
| 4 | false positives (1-spec) | D2 MD rate | 26 | +3.8 (0.0 to 11.5) | 1 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D8 ML tabular (LightGBM) | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D10 Self-supervised order net | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | sensitivity | D2 MD rate | 26 | -7.7 (-23.1 to 7.7) | 1 / 3 | 0.62 | 1.00 |
| 4 | sensitivity | D3 PLR-3 | 26 | -15.4 (-34.6 to 0.0) | 1 / 5 | 0.22 | 1.00 |
| 4 | sensitivity | D4 PoPLR | 26 | -26.9 (-46.2 to -11.5) | 0 / 7 | 0.016 | 0.14 |
| 4 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | sensitivity | D6 Pooled-detrended conformal | 26 | -3.8 (-19.2 to 7.7) | 1 / 2 | 1.00 | 1.00 |
| 4 | sensitivity | D7 Event analysis | 26 | -7.7 (-26.9 to 11.5) | 2 / 4 | 0.69 | 1.00 |
| 4 | sensitivity | D8 ML tabular (LightGBM) | 26 | +11.5 (-3.8 to 30.8) | 4 / 1 | 0.38 | 1.00 |
| 4 | sensitivity | D9 ML sequence (GRU) | 26 | -19.2 (-38.5 to 3.8) | 2 / 7 | 0.18 | 1.00 |
| 4 | sensitivity | D10 Self-supervised order net | 26 | -11.5 (-30.8 to 3.8) | 1 / 4 | 0.38 | 1.00 |
| 5 | false positives (1-spec) | D2 MD rate | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D8 ML tabular (LightGBM) | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +7.7 (0.0 to 19.2) | 2 / 0 | 0.50 | 1.00 |
| 5 | false positives (1-spec) | D10 Self-supervised order net | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | sensitivity | D2 MD rate | 26 | -19.2 (-38.5 to 0.0) | 1 / 6 | 0.12 | 1.00 |
| 5 | sensitivity | D3 PLR-3 | 26 | -19.2 (-34.6 to -3.8) | 0 / 5 | 0.062 | 0.56 |
| 5 | sensitivity | D4 PoPLR | 26 | -3.8 (-11.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 5 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | sensitivity | D6 Pooled-detrended conformal | 26 | -11.5 (-30.8 to 7.7) | 2 / 5 | 0.45 | 1.00 |
| 5 | sensitivity | D7 Event analysis | 26 | +7.7 (-11.5 to 26.9) | 4 / 2 | 0.69 | 1.00 |
| 5 | sensitivity | D8 ML tabular (LightGBM) | 26 | +11.5 (0.0 to 26.9) | 3 / 0 | 0.25 | 1.00 |
| 5 | sensitivity | D9 ML sequence (GRU) | 26 | +0.0 (-23.1 to 23.1) | 5 / 5 | 1.00 | 1.00 |
| 5 | sensitivity | D10 Self-supervised order net | 26 | +7.7 (-7.7 to 23.1) | 3 / 1 | 0.62 | 1.00 |
| 6 | false positives (1-spec) | D2 MD rate | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D8 ML tabular (LightGBM) | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +7.7 (0.0 to 19.2) | 2 / 0 | 0.50 | 1.00 |
| 6 | false positives (1-spec) | D10 Self-supervised order net | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | sensitivity | D2 MD rate | 26 | -34.6 (-57.7 to -15.4) | 1 / 10 | 0.012 | 0.094 |
| 6 | sensitivity | D3 PLR-3 | 26 | -34.6 (-53.8 to -19.2) | 0 / 9 | 0.004 | 0.035 |
| 6 | sensitivity | D4 PoPLR | 26 | -7.7 (-26.9 to 11.5) | 2 / 4 | 0.69 | 1.00 |
| 6 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | sensitivity | D6 Pooled-detrended conformal | 26 | -3.8 (-19.2 to 11.5) | 2 / 3 | 1.00 | 1.00 |
| 6 | sensitivity | D7 Event analysis | 26 | +0.0 (-19.2 to 15.4) | 3 / 3 | 1.00 | 1.00 |
| 6 | sensitivity | D8 ML tabular (LightGBM) | 26 | +11.5 (-7.7 to 30.8) | 5 / 2 | 0.45 | 1.00 |
| 6 | sensitivity | D9 ML sequence (GRU) | 26 | -11.5 (-38.5 to 11.5) | 4 / 7 | 0.55 | 1.00 |
| 6 | sensitivity | D10 Self-supervised order net | 26 | +0.0 (-19.2 to 19.2) | 3 / 3 | 1.00 | 1.00 |

pp, percentage points. Stochastic detectors: majority flag over five seeds. GRAPE endpoints at 3 and 4 tests only.
