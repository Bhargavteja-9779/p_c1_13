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

- FULL RUN COMPLETED (2026-11-23, 1458 s). results/raw_results.csv.gz (gunzip before re-summarising), metrics.json,
  statistics.json, tables/table_metrics_all.csv, tables/table_paired_tests_vs_D1.csv, figures/fig1-4 committed.
  Test refs: 26 progressors / 26 stable (small -> wide CIs). Key findings (from metrics.json):
  * k=3: D1 OLS-MD sens 19.2%, true-null FPR 4.4% (valid); D6 pooled-detrended sens 56.9% but FPR 22.4% (invalid);
    D8 LightGBM FPR 27.7% at k=3, 18.8% at k=5 (invalid; supports H4); D4 PoPLR and D7 cannot flag at k=3.
  * k=4-6: no valid detector clearly beats D1 (D7 event analysis 50% vs 42% at k=5 with FPR 1.2% - check McNemar).
  * RQ3 shuffle audit vs true null: Spearman 0.65, median |diff| 1.0 pp, 80% of cells within 3 pp (H3 partly met).
  * GRAPE k=3: D1 sens 44% / spec 95%; D8 66% / 61%; D2 59% / 79%.
- 2026-11-23 (session 3): STEP 4 DONE. Data restored (UWHVF clone, GRAPE xlsx, visualFields tarball in data_raw/ext).
  New code/src/statistics/describe.py -> results/dataset_counts.json, results/realworld.json (pre-registered real-world
  measures + exploratory cumulative stable-eye flags). manuscript/manuscript_template.md + fill_values.py (all numbers
  are placeholders; citations [@n] renumbered by first use) -> manuscript_filled.md, Final_Manuscript.docx/.pdf,
  cover_letter.docx/.pdf, supplementary/Supplementary_Material.md, tables/table*_*.md. Rebuild: cd manuscript &&
  python3 fill_values.py && python3 build_docx.py && soffice --headless --convert-to pdf Final_Manuscript.docx
  Fixes: Artes data licence is Apache-2.0 (not GPL-3); TRIPOD+AI DOI -> 10.1136/bmj-2023-078378; EMGT authors from PubMed.
  Validity rule (fixed in methods draft commit bd2c2e2 BEFORE results commit 94777b8): CI upper <=10% and lower <=5%.
- Audits written: REVIEW/claim_evidence_audit.md, REVIEW/citation_audit.md. Reviews delegated to background agents
  (REVIEW/review_01..10.md, review_summary.md, review_stakeholder.md) - if missing in a new session, redo them.
- Reproducibility re-run launched (writes results/raw_results.csv + OVERWRITES results/run_meta_full.json -> after it
  finishes: mv run_meta_full.json run_meta_full_repro.json; git checkout results/run_meta_full.json; compare raw vs gz).
- REVIEW ROUND 1 DONE (REVIEW/review_01..10.md, review_summary.md, review_stakeholder.md): 9x major, 1x reject.
  FATAL: F1 validity rule not the protocol's literal rule (literal rule -> D1 invalid at every k); F2 reference includes
  the first k tests (incorporation/MD circularity); F3 failing "complex" detectors are own implementations -> claims too
  general. Key MAJOR: M1 majority-vote vs seed-mean estimands; M4 paired bootstrap by eye not patient; M5 "stable" =
  positive slope; M7 cumulative true-null FA missing; M8/M9 GRAPE PLR2/PLR3 labels unreported (D1 weak on PLR2);
  M11-M13 disclosure (quick mode touched Artes/GRAPE; D6 failure known from dev; "pre-registered" = git file);
  M16 D4/D7/D10 not applicable at k=3; M14 A1 time-label sensitivity. Decision: NOT READY -> revision R1.
- REVISION R1 DONE (commits up to 'Title page and heading font fixes'): results/v2/* (summarise_v2.py), manuscript
  rewritten (Table 4 deviations), authors set by user: P N Bhargav Teja (1st, all code) + [SECOND AUTHOR] (supervision,
  corresponding), both VIT Vellore; no funding; no competing interests. User asked to remove AI mentions: kept one short
  AI-use disclosure (Springer Nature policy requires it) - explained to user. risk_report.md: NOT READY (strict), package
  complete; remaining risks: small n, no published comparator, A1 sensitivity, scope.
- Repro re-run: all 1,106,158 per-eye flags identical (results/reproducibility_check.json). Submission_Package.zip built
  (Target_Journal_Submission/Submission_Package.zip; 99 files; excludes REVIEW/ and journal_selection/).
## NEXT ACTION
Wait for user: second author name/department/e-mail, date, suggested reviewers. Optional improvements to lower risk
(risk_report.md): M3 all-eligible-eyes analysis for untrained detectors, A1 time-label sensitivity, one published comparator.
To rebuild zip: re-run the packaging commands (see git log message 'Submission package').
