# RECHECK PROGRESS (Prompt 2 run: "RECHECK EVERYTHING AND ELEVATE THE PAPER"; full prompt = user's Prompt 2)
Prompt 1 did NOT finish: no final manuscript/DOCX/reviews/cover letter existed (only intro+methods draft
Target_Journal_Submission/manuscript/sections_intro_methods.md and full run-1 results). This run must re-verify AND complete them.

## Restore environment (new container)
pip install -r Target_Journal_Submission/code/requirements.txt
GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 https://github.com/uw-biomedical-ml/uwhvf /home/user/uw-biomedical-ml/uwhvf
mkdir -p data_raw/ext/grape && cd data_raw/ext && curl -sLO https://cloud.r-project.org/src/contrib/visualFields_1.0.7.tar.gz && tar xzf visualFields_1.0.7.tar.gz
curl -sL -o data_raw/ext/grape/vf_clinical.xlsx https://ndownloader.figshare.com/files/41670009
Check sha256 against RECHECK/data_checksums.txt. (Default paths in code match these locations.)

## Stage status
- [x] STAGE 1 journal (stage1_journal_reverification.md): KEEP Ophthalmology and Therapy. 72-day rule NOT MET on recent data
  (last 12 m: median 54.5 d, p75 74 d, n=180; last 6 m p75 78 d). 15 alternatives re-scanned: none passes + fits scope.
  IF 4.2 / Q1 UNVERIFIED in run 2 (Springer page behind bot challenge; headless browser blocked by permission policy).
- [~] STAGE 2 story (stage2_problem_story.md): draft. Harm-of-false-alarm citation found: Gedde 2012 AJO TVT 5-yr
  (10.1016/j.ajo.2011.10.026; failure 29.8% tube / 46.9% trab; reoperation 9%/29%) and Lee 2006 Arch Ophthalmol
  (10.1001/archopht.124.1.12; costs rise with severity) -> add as refs 37, 38. Final story after Stage 4/5 results.
- [x] STAGE 3 prior art (agent): novelty_map_v2.csv (86 rows), prior_art_search_log.md, close_calls.md.
  VERDICT: true-null (retest) evaluation and shuffle-based specificity are ESTABLISHED (Artes 2014; Marin-Franch 2021;
  Montesano 2021; Gardiner & Demirel 2017; Garway-Heath 2018 HTA; Yousefi 2018 AJO calibrated ML at 95% spec on
  10-week retest data). I verified Yousefi 2018, Marin-Franch 2021, Montesano 2021, Gardiner&Demirel 2017 abstracts myself.
  Must NOT claim "first true-null evaluation". Surviving framings: (1) mechanism: clinic "stable" reference (one-sided
  p>0.5 = POSITIVE full-series slope) selects improving eyes -> ML thresholds set on it do not control true-null FPR;
  (2) retest-free fix: null-calibrated ML (threshold from SHUFFLED clinic series; Yousefi needed a retest cohort);
  (3) audit-of-the-audit (shuffle vs true null per detector; full-text check of O'Leary 2012/Artes 2014/Montesano 2021 needed);
  (4) future-only reference (removes circularity).
- [~] STAGE 4 novelty: stage4_scorecard_before.md = honest re-score 17/30 (run-1 22/30 was for an abandoned framing).
  novelty_elevation_log.md Round 1 written with 7 ideas + pre-stated H1/H2/H3 BEFORE running.
  Script Target_Journal_Submission/code/experiments/recheck_elev_r1.py (VALIDATION only) -> results/recheck_elev_r1.json.
  It was RUNNING when session ended (very slow: ~10 min per LightGBM seed, per-row predict). NOT FINISHED -> rerun:
  cd Target_Journal_Submission/code && python3 experiments/recheck_elev_r1.py   (consider batch predict to speed up)
- [~] STAGE 5 experiments:
  * Fresh clean-clone rerun `run_all.py --mode full` was running (reached D8 seed 0 at 836 s; logs RECHECK/logs/fresh_full.log)
    NOT FINISHED. Redo in a fresh clone: git clone <repo> /tmp/fresh && cd .../code && python3 run_all.py --mode full,
    then python -m src.statistics.summarise and diff metrics.json against committed results/metrics.json (mismatch = bug).
    D1-D7 timings matched; D8 is the slow part (~15 min/seed).
  * NEW run_v2.py (protocol Amendment A3 in code/experiments/protocol.md, written before running): whole-cohort 5-fold
    cross-fit (150 prog / 164 stable full-series reference, ~6x run 1), future-only reference E1F/E1S, D11 null-calibrated ML.
    Quick mode verified working. Full run was at fold 0 when session ended -> rerun: cd code && python3 run_v2.py
    (est. 1-2 h) then python -m src.statistics.summarise_v2 (writes metrics_v2.json, statistics_v2.json, tables/table_v2_*).
  * Bugs/weaknesses found so far: (a) run-1 McNemar/paired bootstrap not clustered by patient (fixed in summarise_v2);
    (b) reference circularity (first k tests inside the reference) -> E1F; (c) stable reference = improving eyes (H1);
    (d) D8 includes order-invariant level/variability features (tested by D8change in elev r1);
    (e) Artes/UWHVF point order checked: both right-eye format, blind spot 25/34 -> no bug.
- [~] STAGE 6 citations: all 36 DOIs re-verified on Crossref (stage6_crossref_recheck.json: titles/years/first authors
  match; #32 TRIPOD+AI group author). Abstracts in stage6_abstracts.json (25/36). Still to do: claim-by-claim attribution
  check, claim-evidence table, add new close-call refs (Yousefi 2018, Marin-Franch 2021 already #10, Gardiner&Demirel 2017,
  Garway-Heath 2018 HTA, Gedde 2012, Lee 2006). Fix intro gap sentence "Only a few studies have measured false alarms on
  true no-change data [7]" -> must cite Artes 2014, Yousefi 2018, Gardiner&Demirel 2017, Montesano 2021, Garway-Heath 2018.
- [ ] STAGE 7 rewrite (manuscript_filled.md from results via fill script; build_docx.py exists) 
- [ ] STAGE 8 reviews R1-R6  - [ ] STAGE 9 audit  - [ ] STAGE 10 final_recheck_report.md

## NEXT ACTION
1. Restore env/data. 2. Run in parallel (4 CPUs): elev r1 (validation), run_v2.py full, fresh run_all --mode full.
3. Log r1 results vs H1-H3 in novelty_elevation_log.md (keep/drop honestly), run summarise_v2, compare fresh vs committed.
4. Re-score novelty (stage4), further rounds if needed (max 6), then Stages 6-10. Commit+push after every step.
