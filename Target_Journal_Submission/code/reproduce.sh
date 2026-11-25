#!/usr/bin/env bash
# One command to reproduce every number, table and figure (about 30-45 min on 4 CPU cores).
# Data paths: see README.md (UWHVF_JSON, ARTES_RDA, GRAPE_XLSX environment variables).
set -euo pipefail
cd "$(dirname "$0")"
python3 -m pytest -q tests
python3 run_all.py --mode full                         # -> ../results/raw_results.csv
gzip -c ../results/raw_results.csv > ../results/raw_results.csv.gz
python3 -m src.statistics.summarise ../results/raw_results.csv.gz   # first-round outputs (kept for the record)
python3 -m src.statistics.summarise_v2                 # revised statistics used in the manuscript
python3 -m src.statistics.describe                     # cohort counts and real-world measures
python3 experiments/amendment_b.py                    # amendment B scores (~7 min)
python3 -m src.statistics.amendment_b_stats
python3 -m src.statistics.amendment_b_robust            # post-hoc robustness (review round 2)
python3 -m src.visualization.figures
python3 -m src.visualization.fig5_calibration
python3 experiments/amendment_c.py                    # amendment C scores (~1-2 min)
python3 -m src.statistics.amendment_c_stats
python3 -m src.visualization.fig6_clinic_noise
cd ../manuscript && python3 fill_values.py && python3 build_docx.py
