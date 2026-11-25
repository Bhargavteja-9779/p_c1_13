# Supplementary Material

**How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm**

## S1 Development history: ideas tried and abandoned

Before the final protocol, we tried to develop a new detection method. Rounds 0–3 and 5 used the UWHVF training and validation sets; Round 4 used a different open data set (Moorfields neovascular AMD), and Round 5 also used the Artes retest data. The UWHVF test set and the GRAPE labels were locked. A Round 5 variant (weighted mean sensitivity) had a division-by-zero error; its results were void and it was not carried forward. The full log, with every hypothesis, falsifier and result file, is in the code repository (`code/experiments/development_log.md`; result files `results/pilot_v0.json`, `pilot_v1.json`, `pilot_deferral.json`, `pilot_v2.json`, `d6_round5.json`). In summary:

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
| 3 | GRAPE MD false positives | D2 MD rate | 236 | +16.5 (11.0 to 22.2) | 44 / 5 | < 0.001 | < 0.001 |
| 3 | GRAPE MD false positives | D3 PLR-3 | 236 | -0.4 (-4.2 to 3.3) | 7 / 8 | 1.00 | 1.00 |
| 3 | GRAPE MD false positives | D5 Pooled-shuffle conformal | 236 | -0.1 (-0.3 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | GRAPE MD false positives | D8 ML tabular (LightGBM) | 236 | +34.2 (28.3 to 40.6) | 79 / 0 | < 0.001 | < 0.001 |
| 3 | GRAPE MD sensitivity | D2 MD rate | 27 | +14.8 (-7.8 to 37.0) | 8 / 4 | 0.39 | 0.78 |
| 3 | GRAPE MD sensitivity | D3 PLR-3 | 27 | -40.7 (-61.5 to -19.2) | 1 / 12 | 0.003 | 0.014 |
| 3 | GRAPE MD sensitivity | D5 Pooled-shuffle conformal | 27 | -3.0 (-8.5 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | GRAPE MD sensitivity | D8 ML tabular (LightGBM) | 27 | +21.5 (-1.5 to 42.9) | 10 / 3 | 0.092 | 0.28 |
| 3 | GRAPE PLR2 false positives | D2 MD rate | 223 | +14.3 (8.5 to 20.4) | 39 / 7 | < 0.001 | < 0.001 |
| 3 | GRAPE PLR2 false positives | D3 PLR-3 | 223 | -5.4 (-10.0 to -1.3) | 4 / 16 | 0.012 | 0.024 |
| 3 | GRAPE PLR2 false positives | D5 Pooled-shuffle conformal | 223 | -0.4 (-1.2 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 3 | GRAPE PLR2 false positives | D8 ML tabular (LightGBM) | 223 | +30.9 (24.7 to 37.1) | 70 / 3 | < 0.001 | < 0.001 |
| 3 | GRAPE PLR2 sensitivity | D2 MD rate | 40 | +27.5 (10.8 to 42.5) | 13 / 2 | 0.007 | 0.022 |
| 3 | GRAPE PLR2 sensitivity | D3 PLR-3 | 40 | +0.0 (-14.3 to 14.0) | 4 / 4 | 1.00 | 1.00 |
| 3 | GRAPE PLR2 sensitivity | D5 Pooled-shuffle conformal | 40 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | GRAPE PLR2 sensitivity | D8 ML tabular (LightGBM) | 40 | +43.5 (29.0 to 56.8) | 19 / 0 | < 0.001 | < 0.001 |
| 3 | false positives (1-spec) | D2 MD rate | 26 | +3.8 (0.0 to 12.5) | 1 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (-12.0 to 10.4) | 1 / 1 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D8 ML tabular (LightGBM) | 26 | +1.5 (0.0 to 5.5) | 0 / 0 | 1.00 | 1.00 |
| 3 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +0.8 (-10.8 to 9.7) | 0 / 1 | 1.00 | 1.00 |
| 3 | sensitivity | D2 MD rate | 26 | +19.2 (-3.4 to 41.7) | 7 / 2 | 0.18 | 0.72 |
| 3 | sensitivity | D3 PLR-3 | 26 | -15.4 (-28.6 to -4.0) | 0 / 4 | 0.12 | 0.62 |
| 3 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 3 | sensitivity | D6 Pooled-detrended conformal | 26 | +37.7 (18.5 to 57.7) | 10 / 0 | 0.002 | 0.012 |
| 3 | sensitivity | D8 ML tabular (LightGBM) | 26 | +6.9 (-8.6 to 24.6) | 4 / 2 | 0.69 | 1.00 |
| 3 | sensitivity | D9 ML sequence (GRU) | 26 | -6.9 (-24.4 to 12.0) | 3 / 4 | 1.00 | 1.00 |
| 4 | GRAPE MD false positives | D2 MD rate | 145 | +9.7 (4.0 to 16.1) | 16 / 2 | 0.001 | 0.007 |
| 4 | GRAPE MD false positives | D3 PLR-3 | 145 | -2.1 (-6.2 to 2.0) | 3 / 6 | 0.51 | 1.00 |
| 4 | GRAPE MD false positives | D4 PoPLR | 145 | +0.7 (-3.6 to 5.1) | 6 / 5 | 1.00 | 1.00 |
| 4 | GRAPE MD false positives | D5 Pooled-shuffle conformal | 145 | +1.4 (0.3 to 3.0) | 2 / 0 | 0.50 | 1.00 |
| 4 | GRAPE MD false positives | D7 Event analysis | 145 | +0.0 (-4.8 to 4.8) | 6 / 6 | 1.00 | 1.00 |
| 4 | GRAPE MD false positives | D8 ML tabular (LightGBM) | 145 | +14.3 (8.6 to 21.0) | 21 / 0 | < 0.001 | < 0.001 |
| 4 | GRAPE MD sensitivity | D2 MD rate | 18 | +22.2 (-5.9 to 52.9) | 6 / 2 | 0.29 | 1.00 |
| 4 | GRAPE MD sensitivity | D3 PLR-3 | 18 | -22.2 (-42.2 to -5.3) | 0 / 4 | 0.12 | 0.75 |
| 4 | GRAPE MD sensitivity | D4 PoPLR | 18 | -11.1 (-27.8 to 0.0) | 0 / 2 | 0.50 | 1.00 |
| 4 | GRAPE MD sensitivity | D5 Pooled-shuffle conformal | 18 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | GRAPE MD sensitivity | D7 Event analysis | 18 | -16.7 (-44.4 to 10.5) | 2 / 5 | 0.45 | 1.00 |
| 4 | GRAPE MD sensitivity | D8 ML tabular (LightGBM) | 18 | +15.6 (-3.3 to 35.3) | 4 / 1 | 0.38 | 1.00 |
| 4 | GRAPE PLR2 false positives | D2 MD rate | 132 | +8.3 (2.5 to 14.3) | 14 / 3 | 0.013 | 0.064 |
| 4 | GRAPE PLR2 false positives | D3 PLR-3 | 132 | -5.3 (-9.2 to -2.1) | 0 / 7 | 0.016 | 0.064 |
| 4 | GRAPE PLR2 false positives | D4 PoPLR | 132 | -2.3 (-6.9 to 2.2) | 3 / 6 | 0.51 | 1.00 |
| 4 | GRAPE PLR2 false positives | D5 Pooled-shuffle conformal | 132 | +0.5 (0.0 to 1.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | GRAPE PLR2 false positives | D7 Event analysis | 132 | -2.3 (-7.3 to 3.0) | 4 / 7 | 0.55 | 1.00 |
| 4 | GRAPE PLR2 false positives | D8 ML tabular (LightGBM) | 132 | +11.4 (6.4 to 16.6) | 16 / 0 | < 0.001 | < 0.001 |
| 4 | GRAPE PLR2 sensitivity | D2 MD rate | 31 | +22.6 (6.1 to 40.6) | 8 / 1 | 0.039 | 0.20 |
| 4 | GRAPE PLR2 sensitivity | D3 PLR-3 | 31 | +0.0 (-15.6 to 16.1) | 3 / 3 | 1.00 | 1.00 |
| 4 | GRAPE PLR2 sensitivity | D4 PoPLR | 31 | +6.5 (-5.9 to 20.7) | 3 / 1 | 0.62 | 1.00 |
| 4 | GRAPE PLR2 sensitivity | D5 Pooled-shuffle conformal | 31 | +4.5 (0.0 to 11.3) | 2 / 0 | 0.50 | 1.00 |
| 4 | GRAPE PLR2 sensitivity | D7 Event analysis | 31 | +0.0 (-21.9 to 19.4) | 4 / 4 | 1.00 | 1.00 |
| 4 | GRAPE PLR2 sensitivity | D8 ML tabular (LightGBM) | 31 | +27.7 (10.0 to 46.7) | 9 / 1 | 0.021 | 0.13 |
| 4 | false positives (1-spec) | D2 MD rate | 26 | +3.8 (0.0 to 12.5) | 1 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D8 ML tabular (LightGBM) | 26 | +0.8 (0.0 to 2.6) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +0.8 (0.0 to 2.4) | 0 / 0 | 1.00 | 1.00 |
| 4 | false positives (1-spec) | D10 Self-supervised order net | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | sensitivity | D2 MD rate | 26 | -7.7 (-23.1 to 7.1) | 1 / 3 | 0.62 | 1.00 |
| 4 | sensitivity | D3 PLR-3 | 26 | -15.4 (-33.3 to 0.0) | 1 / 5 | 0.22 | 1.00 |
| 4 | sensitivity | D4 PoPLR | 26 | -26.9 (-44.0 to -11.1) | 0 / 7 | 0.016 | 0.14 |
| 4 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 4 | sensitivity | D6 Pooled-detrended conformal | 26 | -5.4 (-18.5 to 8.0) | 1 / 2 | 1.00 | 1.00 |
| 4 | sensitivity | D7 Event analysis | 26 | -7.7 (-26.9 to 11.1) | 2 / 4 | 0.69 | 1.00 |
| 4 | sensitivity | D8 ML tabular (LightGBM) | 26 | +10.8 (-7.2 to 30.0) | 4 / 1 | 0.38 | 1.00 |
| 4 | sensitivity | D9 ML sequence (GRU) | 26 | -19.2 (-40.0 to 1.5) | 2 / 7 | 0.18 | 1.00 |
| 4 | sensitivity | D10 Self-supervised order net | 26 | -10.8 (-24.4 to 1.7) | 1 / 4 | 0.38 | 1.00 |
| 5 | false positives (1-spec) | D2 MD rate | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D8 ML tabular (LightGBM) | 26 | +0.8 (0.0 to 2.4) | 0 / 0 | 1.00 | 1.00 |
| 5 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +6.2 (0.0 to 17.6) | 2 / 0 | 0.50 | 1.00 |
| 5 | false positives (1-spec) | D10 Self-supervised order net | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | sensitivity | D2 MD rate | 26 | -19.2 (-36.0 to -4.0) | 1 / 6 | 0.12 | 1.00 |
| 5 | sensitivity | D3 PLR-3 | 26 | -19.2 (-33.3 to -4.3) | 0 / 5 | 0.062 | 0.56 |
| 5 | sensitivity | D4 PoPLR | 26 | -3.8 (-12.0 to 0.0) | 0 / 1 | 1.00 | 1.00 |
| 5 | sensitivity | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 5 | sensitivity | D6 Pooled-detrended conformal | 26 | -10.8 (-32.6 to 8.8) | 2 / 5 | 0.45 | 1.00 |
| 5 | sensitivity | D7 Event analysis | 26 | +7.7 (-10.3 to 26.1) | 4 / 2 | 0.69 | 1.00 |
| 5 | sensitivity | D8 ML tabular (LightGBM) | 26 | +13.8 (3.2 to 28.0) | 3 / 0 | 0.25 | 1.00 |
| 5 | sensitivity | D9 ML sequence (GRU) | 26 | -1.5 (-21.6 to 17.7) | 5 / 5 | 1.00 | 1.00 |
| 5 | sensitivity | D10 Self-supervised order net | 26 | +1.5 (-10.4 to 12.9) | 3 / 1 | 0.62 | 1.00 |
| 6 | false positives (1-spec) | D2 MD rate | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D3 PLR-3 | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D4 PoPLR | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D5 Pooled-shuffle conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D6 Pooled-detrended conformal | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D7 Event analysis | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D8 ML tabular (LightGBM) | 26 | +0.0 (0.0 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | false positives (1-spec) | D9 ML sequence (GRU) | 26 | +8.5 (0.0 to 24.8) | 2 / 0 | 0.50 | 1.00 |
| 6 | false positives (1-spec) | D10 Self-supervised order net | 26 | +0.8 (0.0 to 2.4) | 0 / 0 | 1.00 | 1.00 |
| 6 | sensitivity | D2 MD rate | 26 | -34.6 (-54.2 to -18.5) | 1 / 10 | 0.012 | 0.094 |
| 6 | sensitivity | D3 PLR-3 | 26 | -34.6 (-53.8 to -16.0) | 0 / 9 | 0.004 | 0.035 |
| 6 | sensitivity | D4 PoPLR | 26 | -7.7 (-26.9 to 10.3) | 2 / 4 | 0.69 | 1.00 |
| 6 | sensitivity | D5 Pooled-shuffle conformal | 26 | -0.8 (-2.3 to 0.0) | 0 / 0 | 1.00 | 1.00 |
| 6 | sensitivity | D6 Pooled-detrended conformal | 26 | -3.8 (-20.0 to 12.0) | 2 / 3 | 1.00 | 1.00 |
| 6 | sensitivity | D7 Event analysis | 26 | +0.0 (-20.0 to 17.9) | 3 / 3 | 1.00 | 1.00 |
| 6 | sensitivity | D8 ML tabular (LightGBM) | 26 | +13.1 (-5.2 to 31.1) | 5 / 2 | 0.45 | 1.00 |
| 6 | sensitivity | D9 ML sequence (GRU) | 26 | -20.0 (-41.7 to 2.1) | 4 / 7 | 0.55 | 1.00 |
| 6 | sensitivity | D10 Self-supervised order net | 26 | -3.1 (-20.7 to 12.6) | 3 / 3 | 1.00 | 1.00 |

pp, percentage points. Stochastic detectors: majority flag over five seeds. GRAPE endpoints at 3 and 4 tests only.

## S4 GRAPE: PLR3 and any-criterion labels

**Table S4** GRAPE: sensitivity / specificity, % , against the PLR3 and any-criterion labels

| Tests | Detector | PLR3 sensitivity | PLR3 specificity | Any-criterion sensitivity | Any-criterion specificity |
|---|---|---|---|---|---|
| 3 | D1 OLS-MD | 21.4 | 92.0 | 31.5 | 97.1 |
| 3 | D2 MD rate | 57.1 | 76.7 | 51.9 | 81.8 |
| 3 | D3 PLR-3 | 28.6 | 97.2 | 13.0 | 98.1 |
| 3 | D5 Pooled-shuffle conformal | 21.4 | 92.4 | 30.0 | 97.2 |
| 3 | D8 ML tabular (LightGBM) | 72.9 | 60.2 | 61.9 | 63.6 |
| 4 | D1 OLS-MD | 16.7 | 93.4 | 19.4 | 96.1 |
| 4 | D2 MD rate | 50.0 | 84.1 | 44.4 | 89.0 |
| 4 | D3 PLR-3 | 33.3 | 99.3 | 13.9 | 100.0 |
| 4 | D4 PoPLR | 33.3 | 95.4 | 19.4 | 96.9 |
| 4 | D5 Pooled-shuffle conformal | 23.3 | 92.6 | 23.3 | 95.6 |
| 4 | D7 Event analysis | 33.3 | 96.7 | 13.9 | 96.9 |
| 4 | D8 ML tabular (LightGBM) | 53.3 | 80.7 | 47.2 | 85.4 |

## S5 Exploratory future-only reference

**Table S5** Exploratory future-only reference (tests k+1 to end; at least 5 tests), among the eyes evaluated in E1

| Tests | Detector | Sensitivity, % (n progressors) | Specificity, % (n stable) |
|---|---|---|---|
| 3 | D1 OLS-MD | 5.9 (17) | 94.4 (18) |
| 3 | D2 MD rate | 17.6 (17) | 88.9 (18) |
| 3 | D3 PLR-3 | 0.0 (17) | 100.0 (18) |
| 3 | D5 Pooled-shuffle conformal | 5.9 (17) | 94.4 (18) |
| 3 | D6 Pooled-detrended conformal | 52.9 (17) | 83.3 (18) |
| 3 | D8 ML tabular (LightGBM) | 16.5 (17) | 82.2 (18) |
| 3 | D9 ML sequence (GRU) | 7.1 (17) | 93.3 (18) |
| 4 | D1 OLS-MD | 21.4 (14) | 92.3 (13) |
| 4 | D2 MD rate | 7.1 (14) | 92.3 (13) |
| 4 | D3 PLR-3 | 21.4 (14) | 100.0 (13) |
| 4 | D4 PoPLR | 7.1 (14) | 100.0 (13) |
| 4 | D5 Pooled-shuffle conformal | 21.4 (14) | 92.3 (13) |
| 4 | D6 Pooled-detrended conformal | 21.4 (14) | 92.3 (13) |
| 4 | D7 Event analysis | 7.1 (14) | 92.3 (13) |
| 4 | D8 ML tabular (LightGBM) | 20.0 (14) | 83.1 (13) |
| 4 | D9 ML sequence (GRU) | 5.7 (14) | 93.8 (13) |
| 4 | D10 Self-supervised order net | 12.9 (14) | 100.0 (13) |
| 5 | D1 OLS-MD | 33.3 (6) | 85.7 (14) |
| 5 | D2 MD rate | 16.7 (6) | 92.9 (14) |
| 5 | D3 PLR-3 | 33.3 (6) | 85.7 (14) |
| 5 | D4 PoPLR | 33.3 (6) | 85.7 (14) |
| 5 | D5 Pooled-shuffle conformal | 33.3 (6) | 85.7 (14) |
| 5 | D6 Pooled-detrended conformal | 16.7 (6) | 85.7 (14) |
| 5 | D7 Event analysis | 33.3 (6) | 78.6 (14) |
| 5 | D8 ML tabular (LightGBM) | 50.0 (6) | 72.9 (14) |
| 5 | D9 ML sequence (GRU) | 40.0 (6) | 82.9 (14) |
| 5 | D10 Self-supervised order net | 40.0 (6) | 78.6 (14) |
| 6 | D1 OLS-MD | 25.0 (4) | 75.0 (16) |
| 6 | D2 MD rate | 0.0 (4) | 75.0 (16) |
| 6 | D3 PLR-3 | 0.0 (4) | 87.5 (16) |
| 6 | D4 PoPLR | 25.0 (4) | 75.0 (16) |
| 6 | D5 Pooled-shuffle conformal | 25.0 (4) | 76.2 (16) |
| 6 | D6 Pooled-detrended conformal | 50.0 (4) | 62.5 (16) |
| 6 | D7 Event analysis | 50.0 (4) | 68.8 (16) |
| 6 | D8 ML tabular (LightGBM) | 75.0 (4) | 66.2 (16) |
| 6 | D9 ML sequence (GRU) | 15.0 (4) | 70.0 (16) |
| 6 | D10 Self-supervised order net | 45.0 (4) | 62.5 (16) |

Exploratory: among the E1 eyes (primary or secondary reference), reference recomputed from tests k+1..end only (>= 5 tests required), same thresholds as the primary reference. Sample sizes shrink quickly with k; results are imprecise and shown for completeness.


## S6 Untrained detectors on all eligible eyes

**Table S6** Untrained detectors on all UWHVF eyes with a reference label (amendment B3)

| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | Sensitivity difference vs D1, pp (95% CI; Holm p) |
|---|---|---|---|---|
| 3 | D1 OLS-MD | 14.7 (9.5–20.6) | 96.3 (93.2–98.8) | — |
| 3 | D2 MD rate | 23.3 (16.1–30.9) | 85.4 (79.0–90.9) | +8.7; 95% CI 0.7 to 16.4; Holm-adjusted p = 0.047 |
| 3 | D3 PLR-3 | 3.3 (0.7–6.4) | 98.2 (95.8–100.0) | −11.3; 95% CI −17.1 to −6.2; Holm-adjusted p < 0.001 |
| 4 | D1 OLS-MD | 26.7 (19.9–33.8) | 95.7 (92.6–98.8) | — |
| 4 | D2 MD rate | 20.0 (14.5–26.4) | 89.6 (84.1–94.5) | −6.7; 95% CI −13.4 to 0.0; Holm-adjusted p = 0.11 |
| 4 | D3 PLR-3 | 10.0 (5.7–15.1) | 97.6 (95.0–99.4) | −16.7; 95% CI −24.5 to −9.4; Holm-adjusted p < 0.001 |
| 4 | D4 PoPLR | 13.3 (8.4–18.6) | 94.5 (91.0–97.7) | −13.3; 95% CI −20.8 to −6.2; Holm-adjusted p = 0.002 |
| 5 | D1 OLS-MD | 40.0 (32.2–48.2) | 97.6 (94.9–99.4) | — |
| 5 | D2 MD rate | 18.7 (12.4–25.5) | 94.5 (90.0–98.2) | −21.3; 95% CI −28.6 to −14.5; Holm-adjusted p < 0.001 |
| 5 | D3 PLR-3 | 19.3 (13.2–25.7) | 98.2 (96.0–100.0) | −20.7; 95% CI −28.4 to −14.0; Holm-adjusted p < 0.001 |
| 5 | D4 PoPLR | 33.3 (25.8–41.1) | 97.0 (94.0–99.4) | −6.7; 95% CI −12.8 to −1.3; Holm-adjusted p = 0.052 |
| 6 | D1 OLS-MD | 57.3 (48.7–66.4) | 99.4 (98.1–100.0) | — |
| 6 | D2 MD rate | 18.0 (12.2–24.5) | 97.6 (94.4–100.0) | −39.3; 95% CI −47.3 to −31.5; Holm-adjusted p < 0.001 |
| 6 | D3 PLR-3 | 33.3 (25.8–41.6) | 99.4 (98.1–100.0) | −24.0; 95% CI −32.3 to −15.5; Holm-adjusted p < 0.001 |
| 6 | D4 PoPLR | 53.3 (45.3–61.9) | 97.6 (95.0–99.4) | −4.0; 95% CI −10.1 to 1.4; Holm-adjusted p = 0.26 |

314 eyes (150 progressors, 164 stable) of 236 patients from the training, validation and test sets; D1–D4 need no training. Patient-level bootstrap CIs.


## S7 Post-hoc robustness of the calibrated rate rule

**Table S7** Post-hoc robustness: retest-calibrated D1 and D2 on all UWHVF eyes with at least eight tests, under four reference definitions

| Reference | Tests | Progressors / stable eyes | D1 sensitivity, % | D2 sensitivity, % | Difference, pp (95% CI) | D1 specificity, % | D2 specificity, % |
|---|---|---|---|---|---|---|---|
| Primary (−0.3 dB/yr) | 3 | 150 / 164 | 15.3 | 32.0 | +16.7 (9.1 to 24.2) | 96.3 | 82.3 |
| Primary (−0.3 dB/yr) | 4 | 150 / 164 | 32.7 | 52.7 | +20.0 (11.9 to 28.5) | 95.1 | 79.9 |
| Primary (−0.3 dB/yr) | 5 | 150 / 164 | 42.0 | 68.0 | +26.0 (19.4 to 32.9) | 97.6 | 84.1 |
| Primary (−0.3 dB/yr) | 6 | 150 / 164 | 56.0 | 81.3 | +25.3 (18.4 to 32.5) | 99.4 | 90.2 |
| Cut-off −0.5 dB/yr | 3 | 93 / 164 | 19.4 | 38.7 | +19.4 (10.0 to 29.0) | 96.3 | 82.3 |
| Cut-off −0.5 dB/yr | 4 | 93 / 164 | 41.9 | 65.6 | +23.7 (14.4 to 34.1) | 95.1 | 79.9 |
| Cut-off −0.5 dB/yr | 5 | 93 / 164 | 50.5 | 76.3 | +25.8 (17.2 to 35.2) | 97.6 | 84.1 |
| Cut-off −0.5 dB/yr | 6 | 93 / 164 | 65.6 | 89.2 | +23.7 (15.3 to 32.6) | 99.4 | 90.2 |
| Cut-off −1.0 dB/yr | 3 | 23 / 164 | 21.7 | 47.8 | +26.1 (8.7 to 43.5) | 96.3 | 82.3 |
| Cut-off −1.0 dB/yr | 4 | 23 / 164 | 34.8 | 65.2 | +30.4 (13.0 to 47.8) | 95.1 | 79.9 |
| Cut-off −1.0 dB/yr | 5 | 23 / 164 | 47.8 | 78.3 | +30.4 (13.0 to 47.8) | 97.6 | 84.1 |
| Cut-off −1.0 dB/yr | 6 | 23 / 164 | 56.5 | 91.3 | +34.8 (17.4 to 56.5) | 99.4 | 90.2 |
| Future-only (tests k+1 to end) | 3 | 95 / 187 | 8.4 | 18.9 | +10.5 (4.0 to 17.5) | 92.5 | 76.5 |
| Future-only (tests k+1 to end) | 4 | 67 / 119 | 19.4 | 37.3 | +17.9 (8.6 to 28.6) | 86.6 | 73.9 |
| Future-only (tests k+1 to end) | 5 | 43 / 91 | 27.9 | 58.1 | +30.2 (16.7 to 44.5) | 89.0 | 65.9 |
| Future-only (tests k+1 to end) | 6 | 34 / 73 | 29.4 | 61.8 | +32.4 (17.1 to 48.5) | 84.9 | 63.0 |

Post-hoc (review round 2). RC thresholds from amendB.json; eyes from all splits (D1, D2 untrained). Patient-level bootstrap CIs. Indeterminate eyes (primary reference): see main text.

## S8 Semi-synthetic sensitivity (amendment C)

**Table S8** Semi-synthetic sensitivity (amendment C): held-out clinic-noise null series with a known injected loss; thresholds from the clinic-noise null (5% false alarms)

| Pattern | Loss, dB/yr | Detector | 3 tests | 4 tests | 5 tests | 6 tests |
|---|---|---|---|---|---|---|
| Global | 0.5 | D1 | 12.6 | 26.6 | 43.4 | 57.1 |
| Global | 0.5 | D2c | 7.4 | 10.2 | 16.4 | 30.6 |
| Global | 0.5 | D6s | 11.6 | 24.2 | 39.8 | 57.4 |
| Global | 0.5 | D8c | 7.6 | 9.2 | 22.6 | 49.9 |
| Global | 0.5 | D11 | 16.6 | 32.1 | 47.9 | 60.5 |
| Global | 1.0 | D1 | 21.8 | 49.6 | 70.5 | 81.9 |
| Global | 1.0 | D2c | 11.9 | 29.4 | 70.5 | 88.2 |
| Global | 1.0 | D6s | 18.3 | 44.5 | 67.7 | 82.1 |
| Global | 1.0 | D8c | 10.1 | 8.8 | 31.7 | 80.2 |
| Global | 1.0 | D11 | 35.2 | 59.7 | 75.5 | 84.7 |
| Global | 2.0 | D1 | 37.1 | 74.3 | 89.1 | 93.9 |
| Global | 2.0 | D2c | 45.5 | 88.5 | 95.4 | 97.6 |
| Global | 2.0 | D6s | 30.5 | 69.4 | 87.6 | 93.7 |
| Global | 2.0 | D8c | 8.9 | 4.7 | 23.8 | 90.4 |
| Global | 2.0 | D11 | 63.4 | 84.1 | 91.9 | 94.8 |
| Localised | 0.5 | D1 | 12.5 | 26.3 | 43.2 | 56.5 |
| Localised | 0.5 | D2c | 7.3 | 10.1 | 16.2 | 30.3 |
| Localised | 0.5 | D6s | 14.4 | 47.8 | 71.8 | 83.5 |
| Localised | 0.5 | D8c | 11.6 | 24.9 | 45.3 | 62.9 |
| Localised | 0.5 | D11 | 16.6 | 32.1 | 47.7 | 60.0 |
| Localised | 1.0 | D1 | 21.3 | 47.8 | 66.6 | 76.3 |
| Localised | 1.0 | D2c | 11.7 | 27.7 | 59.0 | 75.9 |
| Localised | 1.0 | D6s | 23.1 | 68.5 | 85.9 | 93.1 |
| Localised | 1.0 | D8c | 16.5 | 38.4 | 60.4 | 79.2 |
| Localised | 1.0 | D11 | 34.6 | 58.1 | 72.4 | 79.7 |
| Localised | 2.0 | D1 | 31.4 | 59.0 | 71.0 | 74.8 |
| Localised | 2.0 | D2c | 37.9 | 65.8 | 72.6 | 75.9 |
| Localised | 2.0 | D6s | 28.1 | 61.9 | 69.8 | 75.3 |
| Localised | 2.0 | D8c | 19.6 | 23.6 | 34.8 | 74.8 |
| Localised | 2.0 | D11 | 60.0 | 76.1 | 80.9 | 81.8 |

Values are % of series flagged. Global: equal loss at every location; localised: loss concentrated in one of four regions with the same loss in mean sensitivity. Patient-cluster bootstrap CIs are in results/amendC/amendC.json.

## S9 Literature search for amendment C (prior art)

On 25 November 2026 we searched OpenAlex (titles and abstracts), Crossref, Europe PMC and the web for combinations of "visual field", "progression", "moderated t", "empirical Bayes", "variance shrinkage", "sequential monitoring", "CUSUM", "cumulative false positive", "repeated testing" and "simulation". The closest prior work was: CUSUM charts for visual fields and nerve-fibre-layer thickness (Ledolter and Kardon, 2013); hierarchical Bayesian models, which shrink slopes and model variance (Montesano et al., 2021; Mohammadzadeh et al., 2025); and data-driven simulation of longitudinal fields from clinic residuals (Wu and Medeiros, 2018; Li et al., 2023). We found no study that used a clinic-residual null to set detector thresholds, compared threshold sources on true no-change data, applied a closed-form empirical-Bayes moderated trend test to visual fields, or calibrated a monitoring rule to a cumulative false-alarm budget. Google Scholar, Scopus and Web of Science could not be searched from our computing environment, so this claim is limited to the sources named.
