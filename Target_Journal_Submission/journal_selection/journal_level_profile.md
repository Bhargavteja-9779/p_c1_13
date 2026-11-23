# Journal Level Profile — Ophthalmology and Therapy (from journal_benchmark.csv, 37 original research papers 2024-2026)

Numbers below are medians (IQR) or counts, computed by the benchmark extraction (code/scripts/benchmark_extract.py)
plus manual reading of abstracts/methods. ML subgroup = 14 papers.

| Dimension | All papers | ML subgroup | Our target (must meet/exceed median; aim for top quartile) |
|---|---|---|---|
| Datasets / cohorts | 1 (1-1) | 1 (1-2) | >= 3 (development + 2 external/independent) |
| Compared methods / comparators | 2 (2-4) | 2 (2-5) | >= 6 baselines incl. clinical standard methods |
| External validation | - | 4/14 | yes (independent cohort + true no-change data) |
| Confidence intervals | 21/37 | 8/14 | all main estimates with 95% CI (bootstrap by patient) |
| Robustness / sensitivity analysis | 6/37 | 3/14 | yes, several |
| Ablation | - | 3/14 | yes |
| Calibration | - | 3/14 | yes (where predictions are probabilistic) |
| Decision curve / clinical utility | 2/37 | 2/14 | yes (real-world units) |
| Code available | 2/37 | 2/14 | yes (full repository) |
| Data availability | "on request" 27/37 | | public datasets only |
| Reporting guideline cited | 2/37 | | TRIPOD+AI (prediction) / STARD where relevant |
| Main-text words | 3914 (3597-4500) | 3949 (3731-4194) | ~4000-4500 |
| Figures / tables | 3 / 3 | 3.5 / 3.5 | 4 figures / 3-4 tables (+ supplement) |
| References | 31 (26-44) | 34.5 (27.5-44) | 35-45 |
| Received -> accepted | 54 d (41-84) | 41.5 d (35-73.5) | - |

Kind of novelty typically claimed: new clinical application of AI/ML (most), real-world outcomes of a therapy,
predictors of response. Rarely new methodology or theory -> a paper with a clear methodological idea plus clinical
framing is above the journal's typical novelty level; the risk is scope (must be framed around therapy/monitoring
decisions, not as pure methods).
Statistics depth: mostly descriptive + regression; few multiple-comparison corrections; seeds rarely relevant.
Applied vs theoretical: strongly applied/clinical. Theory must be explained in plain clinical language, with math in
the supplement.
