# True no-change benchmark for glaucoma visual-field progression detectors

Reproduces every number, table and figure of the manuscript.

## Data (all public)
1. UWHVF (BSD-3): `git clone https://github.com/uw-biomedical-ml/uwhvf` -> set `UWHVF_JSON=/path/uwhvf/alldata.json`.
2. Artes 2014 retest data: download `https://cloud.r-project.org/src/contrib/visualFields_1.0.7.tar.gz`, extract,
   set `ARTES_RDA=/path/visualFields/data/vfpwgRetest24d2.rda`.
3. GRAPE (CC0): `https://ndownloader.figshare.com/files/41670009` -> set `GRAPE_XLSX=/path/vf_clinical.xlsx`.

## Run
One command (about 30-45 min on 4 CPU cores):
```
pip install -r requirements.txt
bash reproduce.sh
```
Steps inside reproduce.sh: unit tests -> run_all.py --mode full (raw per-eye flags) -> summarise.py (first-round
statistics, kept for the record) -> summarise_v2.py (revised statistics used in the paper: results/v2/) -> describe.py
(cohort counts, real-world measures) -> figures -> manuscript/fill_values.py (inserts every number) -> build_docx.py.
`python run_all.py --mode quick` is a fast pipeline check on a validation subset.
CPU, CUDA and Apple MPS are detected automatically (src/utils.py); all experiments ran on CPU.
Seeds: 0-4 for detectors with a random component; split = salted hash of patient id (no RNG).
Analysis plan: experiments/protocol.md (committed before the final run). Deviations: manuscript Table 4.
