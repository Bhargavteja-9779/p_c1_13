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
- Session 3 (2026-11-23): data restored (uwhvf clone, GRAPE xlsx, visualFields tarball into data_raw/ext). Added
  code/src/statistics/descriptives.py -> results/descriptives.json (data counts) + results/realworld.json
  (pre-registered real-world measures: false flags/1,000, tests to first detection; bootstrap CI for RQ3 rho 0.35-0.85).
  Note: D5 flags identical to D1 on E1 at every k (conformal pool reproduces the t-test) - report honestly.
  H2 note: D8 k=6 sens 70.8 vs D1 57.7 (+11.5 pp, Holm p=1.0, FPR 3.6% valid) -> not significant; H2 not falsified.
- Step 4 DONE (session 3): manuscript/template_main.md + template_cover_letter.md + template_figure_legends.json +
  template_supplementary.md -> fill_values.py (resolver placeholders, 42 claim checks, Vancouver renumbering) ->
  manuscript_filled.md, cover_letter_filled.md, figure_legends.json, supplementary/Supplementary_Material.md,
  claim_check_log.txt -> build_docx.py -> Final_Manuscript.docx/.pdf (27 pp), cover_letter.docx/.pdf.
  Abstract 283 words; main text ~3,500 words; 34 refs. TRIPOD+AI DOI fixed (bmj-2023-078378).
  Author names/affiliations/funding/COI/repo URL left as [TO BE COMPLETED BY THE AUTHORS] (cannot be fabricated).
- Step 5 DONE (session 3): REVIEW/review_01-10.md + stakeholder_review.md (independent agent; R01-R09 major, R10 reject),
  REVIEW/summary_of_issues.md, REVIEW/response_to_reviews.md. Revision: post hoc analyses in
  code/src/statistics/sensitivity.py -> results/posthoc_sensitivity.json (future-only reference, GRAPE >= k+2 visits +
  PLR labels, exact CIs, cluster CIs, MDD = 9 discordant ~35 pp); summarise.py paired CIs now patient-cluster;
  three validity readings; honest reframing (D6 = own dev variant known invalid; H3 not supported; "time-stamped plan",
  quick-run disclosure). Key new fact: future-only reference DOES lower D6/D8 specificity (83% vs 94% D1 at k3).
  audits/citation_audit.md, audits/reproducibility_audit.md, risk_report.md.
  FINAL DECISION: NOT READY FOR SUBMISSION (author-only items + open scientific items I08, I10-I12, I21);
  label NOT REMARKABLE: honest strongest result.
- Session 3 continued: post hoc plan P1-P3 appended to protocol.md (committed BEFORE running), run via
  code/experiments/posthoc_extra.py (seed 0, 213 s) -> results/posthoc_extra.json, posthoc_extra_raw.csv.gz.
  P1 GRAPE shuffle k3: D1 5.2%, D2 19.6%, D8 40.9%. P2 Artes + global fluctuation (SD 1.13 dB): p-value tests ~5%,
  D2 12.1% k3, D7 8.6% k6. P3 shuffle-calibrated D8: false alarms 7.2/6.9/5.1/1.9%, no sensitivity difference vs D1.
  Added to Results ("Post hoc robustness analyses"), limitations, Table S5; flow diagram Supplementary Fig. S1
  (code/src/visualization/flow.py). Full raw re-run reproduced exactly.
## NEXT ACTION
1. Remaining optional science: VFI/ANSWERS comparators (I21), nested-CV ML (I10), refit D8 on GRAPE (I11),
   TRIPOD+AI checklist (needs the official item list; do not invent item numbers).
2. Rebuild after any change: cd Target_Journal_Submission/code; python -m src.statistics.summarise (needs gunzip -k of
   raw); python -m src.statistics.descriptives; python -m src.statistics.sensitivity; cd ../manuscript;
   python fill_values.py; python build_docx.py; soffice --headless --convert-to pdf Final_Manuscript.docx;
   supplementary: pandoc Supplementary_Material.md --resource-path=. -o Supplementary_Material.docx.
3. Author items (only the user): names/affiliations/funding/COI/AI-verification statement/repo URL; JCR quartile; APC.
FINAL DECISION still NOT READY (author items). Label NOT REMARKABLE: honest strongest result.
