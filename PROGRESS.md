# PROGRESS (resume file)

## Environment facts (2026-11-23)
- 4 CPU, 15 GB RAM, no GPU. Python 3.13.
- Network: Crossref API, OpenAlex API, Semantic Scholar API, PyPI, UCI reachable. ScienceDirect web BLOCKED (403).
  -> journal dates gathered through Crossref "assertion" metadata (Springer Nature, T&F, etc.) where deposited.

## Phase status
- [x] STEP 0 journal selection -> Ophthalmology and Therapy (see journal_selection/selected_journal.md)
- [x] STEP 1 benchmark/profile/style
- [x] STEP 2 problem discovery
- [x] STEP 3 novelty map/scorecard
- [x] Build v1, D6 loop, protocol, experiments, manuscript, reviews, package (decision: NOT READY - author items)

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
- STEP 4 DONE (2026-11-23, session 3): data restored; code/scripts/descriptives.py -> results/descriptives.json (cohort,
  Artes windows, GRAPE, time-to-detection). manuscript/fill_values.py fills front_template.md + sections_intro_methods.md +
  results_discussion_template.md + back_template.md -> manuscript_filled.md (37 automated claim checks in claim_checks.json;
  citations renumbered in first-citation order; all 36 refs cited). build_docx.py -> Final_Manuscript.docx/.pdf, cover_letter.docx.
  build_supplementary.py -> supplementary/Supplementary_Material.{md,docx,pdf}. Fig 1 label fixed.
  Rebuild: cd manuscript && python3 fill_values.py && python3 build_supplementary.py && python3 build_docx.py &&
  soffice --headless --convert-to pdf Final_Manuscript.docx
  Key wording facts: D9 k=6 FPR upper CI 10.0002% -> invalid by rule (text says "only just exceeded"); D5 = D1 sens at k3-5.
  Placeholders left for AUTHORS: names/affiliations, funding, contributions, COI, repo URL, prior presentation.

- Step 5 in progress: REVIEW/citation_audit.md DONE (agent). references.json metadata fixed by hand (field manual_fix;
  do NOT rerun build_refs.py without re-applying). TRIPOD+AI now 10.1136/bmj-2023-078378. UWHVF: release README says
  7,428 eyes (our count), data paper says 7,248 -> state both. Text fixes from citation audit still TO APPLY in templates
  (prevalence wording ages 40-80; ML-threshold citation -> orig refs 18(TVST? check) & 21... see citation_audit.md).
  Reviews 01-05+stakeholder and 06-10 launched as agents (check REVIEW/ for files; redo missing ones).
- STEP 5 DONE (2026-11-23): 10 reviews + stakeholder + citation audit in REVIEW/; revision 1 applied (see
  REVIEW/response_to_reviews.md). New: code/scripts/extra_stats.py -> results/extra_stats.json (strict validity, MDD 34.6 pp,
  cumulative FA: D1 15.3%, D7 3.3%, D8 50.8%; rho cell-CI; GRAPE PLR labels). 49 claim checks pass. risk_report.md written:
  FINAL DECISION = NOT READY (author-only blockers); label NOT REMARKABLE: honest strongest result; rescored 19/30.

- USER REQUEST (2026-11-23): "make paper very strong, avoid desk rejection, more experiments/new models OK, APC OK,
  code available on request". -> STUDY 2 started. Protocol: code/experiments/protocol_v2.md (commit e51bd2b, 10:51,
  before any run). Code: code/study2.py (5-fold cross-fit over all UWHVF: 150 R1 progressors / 164 stable; shuffle
  calibration S1-S7, Order-LightGBM, cumulative-controlled Q1-Q4, GRAPE local recalibration). Full run launched in
  background: `cd code && python3 study2.py --mode full > ../results/study2_full.log` (~1 h). If lost: rerun.
  Rotterdam longitudinal VF data (139 pts) would be a strong 2nd cohort but rodrep.com unreachable -> ask user.

- STUDY 2 DONE (2026-11-23, 441 s): results/study2_*.json, tables/study2_*.csv, figs 5-6 (Fig 3-4 in paper).
  Key: at matched (shuffle-calibrated) FA no detector beats D1 (all upper CI < 8.4 pp; 150/164 eyes); B8 usual threshold
  +18-22 pp sens with 14-26% true-null FA; S5 calibrated FA 2.6-8.1% (invalid by hair at k3,k5); H8 rejected (cum
  control costs 17-52 pp); H9 supported (local recal spec 93%) but sens collapses. Manuscript fully rewritten
  (new title "Apparent Gains ... Disappear at Matched False-Alarm Rates: A Two-Stage Benchmark"); 73 claim checks;
  data/code "available on request". Supplement rebuilt (Tables S1-S7, Figs S1-S2).

## NEXT ACTION (new session)
Review round 2 (fresh agents) on revised manuscript -> fix -> rebuild -> update risk_report.md, cover letter, final decision.
Rebuild: cd manuscript && python3 fill_values.py && python3 build_supplementary.py && python3 build_docx.py && soffice ...
Ask user: can they download Rotterdam longitudinal VF data (rodrep.com) manually? (would add a 2nd routine-care cohort)
