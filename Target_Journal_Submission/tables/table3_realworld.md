**Table 3** Real-world measures: tests to first flag in future-confirmed progressors and false flags in no-change eyes

| Detector | Progressors flagged by test 4 / 5 / 6, % | Median tests to first flag | False flags per 1,000 no-change eyes at a single review with 3 / 4 / 5 / 6 tests | No-change series flagged at least once over four reviews (tests 3–6), % (95% CI) |
|---|---|---|---|---|
| D1 OLS-MD | 38 / 54 / 69 | 5 | 44 / 38 / 47 / 51 | 12.6% (95% CI 8.0–17.9%) |
| D2 MD rate | 38 / 46 / 46 | > 6 | 26 / 6 / 8 / 10 | 4.4% (95% CI 3.2–5.9%) |
| D3 PLR-3 | 19 / 31 / 38 | > 6 | 14 / 2 / 5 / 3 | 2.6% (95% CI 1.7–3.7%) |
| D4 PoPLR | 4 / 38 / 54 | 6 | 0 / 33 / 39 / 50 | 9.2% (95% CI 5.5–13.4%) |
| D5 Pooled-shuffle conformal | 38 / 54 / 68 | 5 | 40 / 36 / 44 / 50 | 12.2% (95% CI 7.6–17.2%) |
| D6 Pooled-detrended conformal | 58 / 65 / 77 | 3 | 224 / 51 / 62 / 76 | 29.8% (95% CI 24.6–35.4%) |
| D7 Event analysis | 23 / 50 / 58 | 5.5 | 0 / 11 / 12 / 19 | 1.9% (95% CI 0.5–3.8%) |
| D8 ML tabular (LightGBM) | 52 / 63 / 78 | 4 | 277 / 94 / 188 / 36 | 43.7% (95% CI 36.2–51.1%) |
| D9 ML sequence (GRU) | 16 / 46 / 59 | 6 | 127 / 20 / 76 / 59 | 20.9% (95% CI 10.8–31.7%) |
| D10 Self-supervised order net | 20 / 51 / 63 | 5 | 0 / 38 / 51 / 57 | 11.4% (95% CI 7.5–16.1%) |

Progressors: 26 UWHVF test-set reference progressors; an eye counts as flagged by test k if any review with 3..k tests flagged it. Median tests: '> 6' means fewer than half were flagged by 6 tests. In UWHVF the median interval between tests was 1.0 years. False flags per 1,000 = 1,000 × single-review true no-change false-alarm rate. Last column (exploratory, not pre-registered): Artes retest series reviewed four times, after 3, 4, 5 and 6 tests, the cumulative counterpart of the second column.
