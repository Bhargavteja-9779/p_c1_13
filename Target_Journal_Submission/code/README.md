# True no-change benchmark for glaucoma visual-field progression detectors

Reproduces every number, table and figure of the manuscript.

## Data (all public)
1. UWHVF (BSD-3): `git clone https://github.com/uw-biomedical-ml/uwhvf` -> set `UWHVF_JSON=/path/uwhvf/alldata.json`.
2. Artes 2014 retest data: download `https://cloud.r-project.org/src/contrib/visualFields_1.0.7.tar.gz`, extract,
   set `ARTES_RDA=/path/visualFields/data/vfpwgRetest24d2.rda`.
3. GRAPE (CC0): `https://ndownloader.figshare.com/files/41670009` -> set `GRAPE_XLSX=/path/vf_clinical.xlsx`.

## Run
```
pip install -r requirements.txt
python -m pytest -q tests
python run_all.py --mode quick     # pipeline check on a validation subset (~1 min)
python run_all.py --mode full      # full benchmark (CPU, ~1-3 h)
python -m src.statistics.summarise # metrics.json, statistics.json, tables/
python -m src.visualization.figures
python scripts/descriptives.py     # cohort descriptives, time to detection -> results/descriptives.json
python scripts/extra_stats.py      # post-review analyses -> results/extra_stats.json
cd ../manuscript && python fill_values.py && python build_supplementary.py && python build_docx.py
soffice --headless --convert-to pdf Final_Manuscript.docx   # optional PDF
```
Data versions used: UWHVF GitHub default branch as cloned on 2026-11-23 (README states 28,943 fields / 7,428 eyes /
3,871 patients); visualFields 1.0.7; GRAPE figshare file 41670009. Python package versions: see requirements.txt
(minimum versions) and requirements-lock.txt (versions installed for the 2026-11-23 manuscript build; the full run in the earlier session may have used slightly different versions).
CPU, CUDA and Apple MPS are detected automatically (src/utils.py); all experiments run on CPU.
Seeds: 0-4 for stochastic detectors; split = salted hash of patient id (no RNG).
Pre-registered protocol: experiments/protocol.md. Development history incl. failed ideas: ../journal_selection/novelty_escalation_log.md.
