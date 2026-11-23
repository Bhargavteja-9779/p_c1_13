# Reproducibility audit (2026-11-23)

1. Unit tests: `cd code && python -m pytest -q tests` -> 5 passed.
2. Statistics re-derivation: in a clean copy, `gunzip -k results/raw_results.csv.gz; python -m src.statistics.summarise`
   reproduced results/metrics.json, results/statistics.json and tables/table_metrics_all.csv byte-for-byte (cmp).
3. Quick mode end-to-end (`python run_all.py --mode quick`, validation data only): completed in 19 s.
4. Full re-run from scratch in a clean copy (`python run_all.py --mode full`, 2026-11-23, after restoring public data):
   results/raw_results.csv identical to the committed raw_results.csv.gz (1,106,158 rows, all values equal),
   including all stochastic detectors (seeds 0-4). Summary statistics are derived deterministically from it (item 2).
5. Manuscript numbers: every result number is inserted by manuscript/fill_values.py from results/*.json;
   42 textual claims are asserted programmatically (manuscript/claim_check_log.txt; all PASS).
6. Data: all three data sets are public; download commands are in code/README.md and PROGRESS.md.
   Patient-level split: results/split_assignment.csv (salted SHA-256, salt "uwhvf-split-v1").
