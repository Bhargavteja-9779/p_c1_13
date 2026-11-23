**Table 3** Real-world measures: tests to first flag in future-confirmed progressors and false flags per 1,000 stable eyes

| Detector | Progressors flagged by test 4 / 5 / 6, % | Median tests to first flag | False flags per 1,000 no-change eyes at test 3 / 4 / 5 / 6 | Stable eyes ever flagged over tests 3–6, % (exploratory) |
|---|---|---|---|---|
| D1 OLS-MD | 38 / 54 / 69 | 5 | 44 / 38 / 47 / 51 | 4 |
| D2 MD rate | 38 / 46 / 46 | > 6 | 26 / 6 / 8 / 10 | 8 |
| D3 PLR-3 | 19 / 31 / 38 | > 6 | 14 / 2 / 5 / 3 | 4 |
| D4 PoPLR | 4 / 38 / 54 | 6 | 0 / 33 / 39 / 50 | 0 |
| D5 Pooled-shuffle conformal | 38 / 54 / 68 | 5 | 40 / 36 / 44 / 50 | 4 |
| D6 Pooled-detrended conformal | 58 / 65 / 77 | 3 | 224 / 51 / 62 / 76 | 4 |
| D7 Event analysis | 23 / 50 / 58 | 5.5 | 0 / 11 / 12 / 19 | 0 |
| D8 ML tabular (LightGBM) | 52 / 63 / 78 | 4 | 277 / 94 / 188 / 36 | 7 |
| D9 ML sequence (GRU) | 16 / 46 / 59 | 6 | 127 / 20 / 76 / 59 | 11 |
| D10 Self-supervised order net | 20 / 51 / 63 | 5 | 0 / 38 / 51 / 57 | 1 |

Progressors: 26 UWHVF test-set reference progressors; an eye counts as flagged by test k if any look at 3..k tests flagged it. Median tests: '> 6' means fewer than half were flagged by 6 tests. In UWHVF the median interval between tests was 1.0 years, so each extra test is roughly one extra year of follow-up. False flags per 1,000 = 1,000 × true no-change false-alarm rate. Last column: share of 26 reference-stable eyes flagged at least once over the four looks (not pre-registered).
