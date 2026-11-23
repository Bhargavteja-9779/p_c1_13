# PROGRESS (resume file)

## Environment facts (2026-11-23)
- 4 CPU, 15 GB RAM, no GPU. Python 3.13.
- Network: Crossref API, OpenAlex API, Semantic Scholar API, PyPI, UCI reachable. ScienceDirect web BLOCKED (403).
  -> journal dates gathered through Crossref "assertion" metadata (Springer Nature, T&F, etc.) where deposited.

## Phase status
- [x] STEP 0 journal selection -> Ophthalmology and Therapy (see journal_selection/selected_journal.md)
- [ ] STEP 1 benchmark/profile/style
- [ ] STEP 2 problem discovery
- [ ] STEP 3 novelty map/scorecard
- [ ] Build v1, D6 loop, protocol, experiments, manuscript, reviews, package

## Decisions log
- Elsevier/Wiley/IEEE/OUP/SAGE/ACM/CUP article pages blocked (403/418) and Elsevier/Wiley/IEEE do not deposit received/accepted
  dates in Crossref -> their acceptance times are UNVERIFIABLE here. Only Springer Nature and Taylor & Francis can be verified.
- First Crossref scan (journal_selection/dates_raw/, script code/scripts/journal_dates.py): all CS journals fail 72 days.
  Near misses: Critical Care 55/77 (median/p75), Cardiovasc Diabetol 63/87, Virtual & Physical Prototyping 64/86,
  Energy Informatics 71/90 (no IF shown on Springer page -> likely not JCR IF), JKSU-CIS 72/94, J Transl Med 96/141.
- Broad scan of 313 Springer/T&F journals (OpenAlex 2yr citedness>5, relevant fields) running ->
  journal_selection/scan_summary.txt. If interrupted rerun: xargs -a issns python3 code/scripts/journal_dates.py
- Springer journal pages are reachable with curl -L + cookie jar (shows IF and first-decision median).

- STEP 0 DONE: selected Ophthalmology and Therapy (IF 4.2, research median 52.5 d / p75 70.25 d, n=266). Critical Care & ICM failed p75.
- Leading topic idea (not yet gated): glaucoma visual-field progression detection with fewer tests. Data: UWHVF (BSD-3,
  28,943 VFs, cloned at /home/user/uw-biomedical-ml/uwhvf; re-clone: GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1
  https://github.com/uw-biomedical-ml/uwhvf). Core idea candidate: self-supervised temporal-order classifier as learned test
  statistic + within-eye permutation calibration (exact type-I control, borrowed from classification permutation test).
- PhysioNet 2019 sepsis data partially downloaded in data_raw/ (S3 mirror physionet-open) - fallback topic only.

- Pilot rounds 0-1 (detection power) -> no remarkable gain; pivot to risk-controlled VF test DEFERRAL (see
  Target_Journal_Submission/journal_selection/novelty_escalation_log.md). External data found:
  * Artes 2014 retest data (30 glaucoma pts x 12 weekly VFs) in CRAN visualFields_1.0.7 data/vfpwgRetest24d2.rda
    (download https://cloud.r-project.org/src/contrib/visualFields_1.0.7.tar.gz; read with pyreadr) -> true no-change data.
  * GRAPE (Sci Data 2023, CC0) figshare file 41670009 "VF and clinical information.xlsx" (263 eyes, ~4 visits, clinical
    progression labels PLR2/PLR3/MD) -> external validation. Stored in data_raw/ext (gitignored).
- Background agents launched: journal benchmark (writes journal_benchmark.csv, style_raw_notes.md) and novelty map
  (novelty_map.csv, novelty_search_log.md; told to prioritise G5 = VF scheduling/deferral + conformal risk control).
  If they did not finish (files missing), redo those tasks.

- Benchmark agent DONE: journal_benchmark.csv (37 papers), style_raw_notes.md. ML subgroup median: 1 dataset,
  2 comparators, 4/14 external validation, 3/14 calibration, 2/14 code. -> our paper must exceed these.
- Moorfields CC0 datasets downloaded from Zenodo mirrors into data_raw/moorfields/z<record> (records 4247292 12-yr
  nAMD 7,802 eyes; 3962247 DMO 4-yr; 4361633 nAMD report 2; 4509402 OCT volumes + VA; 4088863 OCT baseline;
  3965967 nAMD report 1; 4086324 10-yr). Download: zenodo.org/api/records/<id> -> files links.
- Pilots rounds 2-4 failed to show a step change (see escalation log).

- User offered help (2026-11-23). Asked user for: (1) manual Dryad download of AMD_longitudinal_MEH_v4.csv
  (doi 10.5061/dryad.8cz8w9h0v) into data_external/; (2) JCR quartile check for Ophthalmol Ther; (3) APC USD 8,050 OK?
  Hugging Face reachable (mostly image datasets).

- FINAL TOPIC (after failed method ideas): open benchmark of 10 glaucoma VF progression detectors with a TRUE
  NO-CHANGE arm (Artes retest), future reference (UWHVF test split), shuffle audit, external GRAPE. Honest label
  expected: NOT REMARKABLE (strongest honest result). Protocol: code/experiments/protocol.md (+ amendments A1, A2).
- Code: code/run_all.py (quick/full), src/models/detectors.py (D1-D10), src/statistics/summarise.py,
  src/visualization/figures.py, tests/ (5 pass), leakage_audit.md, README.md.
- Full run launched: `cd code && nohup python3 run_all.py --mode full > ../results/full_run.log &`
  Output results/raw_results.csv. If interrupted: rerun same command (takes ~1-3 h).

- 2026-11-23 handover: full benchmark run was IN PROGRESS when the session ended (container is ephemeral, so the run
  and data_raw/ are lost). Manuscript drafts: manuscript/sections_intro_methods.md (placeholders {{...}}),
  manuscript/build_docx.py (python-docx builder; expects manuscript_filled.md, cover_letter_filled.md,
  figure_legends.json), manuscript/references.json (36 verified DOIs; numbering in intro = order of DOIS list in
  code/scripts/build_refs.py).

## NEXT ACTION (new session: do these in order)
1. Restore data (all public):
   GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/uw-biomedical-ml/uwhvf /home/user/uw-biomedical-ml/uwhvf
   mkdir -p data_raw/ext/grape && cd data_raw/ext && curl -sLO https://cloud.r-project.org/src/contrib/visualFields_1.0.7.tar.gz && tar xzf visualFields_1.0.7.tar.gz
   curl -sL -o grape/vf_clinical.xlsx https://ndownloader.figshare.com/files/41670009
   pip install scikit-learn scipy lightgbm matplotlib pyreadr openpyxl python-docx; pip install torch --index-url https://download.pytorch.org/whl/cpu
2. cd Target_Journal_Submission/code && python -m pytest -q tests && nohup python3 run_all.py --mode full > ../results/full_run.log 2>&1 &
   (~20-40 min on 4 CPUs; writes results/raw_results.csv). Commit results when done.
3. python -m src.statistics.summarise ; python -m src.visualization.figures ; commit.
4. Write Results/Discussion/Abstract/Key Summary Points from metrics.json/statistics.json (fill script must insert
   numbers; never hand-type), assemble manuscript_filled.md, figure_legends.json, cover_letter_filled.md, run
   build_docx.py, render to PDF and inspect.
5. Claim-evidence + citation audit, 10 reviews + stakeholder review in REVIEW/, risk_report.md, final decision.
   Honest label expected: "NOT REMARKABLE: honest strongest result" (see novelty_escalation_log.md).
6. Open user requests: manual Dryad download (AMD_longitudinal_MEH_v4.csv), JCR quartile check, APC USD 8,050 OK?
