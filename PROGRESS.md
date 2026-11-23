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

## NEXT ACTION
1) Pilot the deferral idea on VALIDATION split (savings vs delay; baselines fixed thinning, severity rule).
2) When agents finish: journal_level_profile.md, style_notes.md, novelty scorecard, STEP 2 story file.
