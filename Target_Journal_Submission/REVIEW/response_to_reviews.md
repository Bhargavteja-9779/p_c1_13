# Response to internal reviews (revision 1, 2026-11-23)

All numbers in the revised text come from result files via `manuscript/fill_values.py` (49 automated claim checks).
New analyses requested by reviewers are in `code/scripts/extra_stats.py` -> `results/extra_stats.json` and are labelled
in the manuscript and Supplement S4 as added after internal review.

| Issue (review) | Severity | Action |
|---|---|---|
| Validity rule applied after results; protocol says "upper bound vs 5%" (02 #1, 05 #2, 06 #1, 07 #2) | FATAL | Verified from git: protocol 09:05 ("upper bound vs 5%"); draft Methods 09:14, before results committed 09:33, stated "upper <=10% and point estimate within sampling error of 5%"; operational "lower CI <=5%" written after results. Now disclosed in Methods as a deviation; strict literal rule reported as sensitivity analysis (D1 fails it at all k; no strict-valid detector has a significant gain -> conclusions unchanged). |
| Headline (D6 invalid on Artes) known before protocol (02 #3, 07 #1) | FATAL | Disclosed in Methods (D6 description), Discussion ("confirmation on locked test data rather than a new discovery") and Limitations; Abstract now says "specified before the final analysis" instead of "pre-specified". |
| Pre-registration only an internal git commit (05 #2, 07 #3) | MAJOR | Methods now states it was time-stamped only in the study repository, not registered externally. |
| H2 practically unfalsifiable at n = 26 (02 #2, 09 #1) | FATAL | Minimum significant gain (9/26 = 34.6 pp) computed and reported in Methods, Results, Discussion, Limitations, Abstract; "supports" replaced by "consistent with"; "as good as any valid alternative" removed. |
| Placeholders for authors, COI, funding, repository (05 #1) | FATAL for submission | Cannot be filled by the agent (author-only information). Listed in risk report as blocking items. |
| Reference-stable = positive slope (01 #1, 08 #1) | MAJOR | Methods now states this; Discussion explains that specificity against such eyes is optimistic; Limitation 3. |
| Incorporation bias / >=8-test selection (01 #2, 08 #3, 08 #4, 07 #6) | MAJOR | Methods + Limitation 2 (132 of 869 eyes). |
| No flow diagram (08 #2) | MAJOR | Partly: counts (132 -> 26/26/80) given in Methods and Results. Formal STARD flow diagram not drawn (residual risk). |
| GRAPE labels are dataset criteria, 100 eyes with 3 visits (01 #3) | MAJOR | "clinicians' labels" replaced by "the data set's progression labels"; 3-visit overlap disclosed (Methods, Limitations); PLR2/PLR3 results added (Table S3). |
| GRAPE perimeter / dB-scale confounds D8 transfer (03 #4, 04 #3, 09 #5) | MAJOR | Stated in Methods and Results ("reflects a change of device as well as of clinic"). Device name not stated (not verified from the data paper). |
| D7 matches/beats D1 with fewer false alarms (01 #5) | MAJOR | Results and Discussion now report D7 at k=5-6 and its low cumulative false alarms (3.3% vs 15.3%); Conclusions revised. |
| Cumulative vs per-look false alarms (01 #6, 08 #5, stakeholder #2) | MAJOR | New repeated-looks analysis (Results section, Table S4, Abstract). |
| D9 "borderline" at 0.100002 (02 #5, 06 #2) | MAJOR | Table shows "no (borderline)"; text says borderline; not counted as clear support for H4. |
| H4 wording for D9 (02 #4) | MAJOR | Reworded to the validity rule. |
| Majority-vote paired tests vs seed means (02 #6, 06 #3, 10 #3) | MAJOR | Explained in Methods. Estimand not changed (pre-specified code). |
| Artes not strictly weekly; one 524-day series (03 #2) | MAJOR | Methods now gives median span 84 d and max 524 d. |
| Weekly retest lacks long-term fluctuation (03 #1) | MAJOR | Limitation 4. |
| D7 is not GPA (03 #3) | MAJOR | Methods and Discussion: "simplified event analysis on raw sensitivities, loosely modelled on GPA". |
| ML labelled sample small; selection and threshold on same 70 eyes (04 #1) | MAJOR | Counts (93/99 train; 31/39 val) in Methods; Limitation 8. Not re-run (would be a post-hoc change). |
| No ML variant calibrated against a shuffle null (04 #2) | MAJOR | Not added (new detector after results would be post hoc); D10 is a permutation-calibrated learned statistic; noted as residual risk. |
| PLS "two machine-learning methods" (04 #4, 09 #7, 10 #2) | MAJOR | PLS rewritten. |
| Scope: no therapy studied (01 #4, 05 #3) | MAJOR | Framing kept (treatment-escalation decisions) but harm wording softened ("extra tests or a change of treatment"). Residual risk. |
| Shuffle audit novelty undercut; H3 failure omitted from Abstract (05 #4, 05 #5, 07 #4) | MAJOR | Intro now says agreement between indirect and direct estimates is unknown; Abstract reports rho below 0.70; rho CI added. |
| "both identified the same invalid detectors" (stakeholder #4, 07 #5, 10 #1) | MAJOR | Removed; Results/Discussion/cover letter now list where the audit over- and under-estimated. |
| Shuffle includes identity order (06 #4) | MAJOR | Methods now states this. |
| README omits steps; unpinned packages (06 #5) | MAJOR | README updated; requirements-lock.txt added; run_all docstring corrected. |
| Secondary reference overlaps primary; valid detectors beat D1 at k=6 on it (09 #2) | MAJOR | Methods states overlap (58 incl. all 26); Results report D7/D10/D8 > D1 at k=6 on this reference. |
| "three independent data sources"; "better-timed testing" not tested (05 #6, 09 #5, 09 #6) | MAJOR | Removed / marked "we did not test this". |
| D1 misses most progressors early (stakeholder #1) | MAJOR | Stated in Results. |
| Sex not reported (05) | MAJOR (journal rule) | Female % added to Table 1 (UWHVF reference cohorts, GRAPE). |
| Detector naming inconsistent; MD used for mean sensitivity (10 #15) | MINOR/MAJOR | Unified short names in Methods and tables; Supplement maps code names. |
| Citation audit items (citation_audit.md) | NOT SUPPORTED / PARTLY | All applied: UWHVF eye count, prevalence wording, noise wording, trend/event/GPA citations, ML-threshold citations, labels wording, TRIPOD+AI DOI, EMGT authors, ref metadata, uncited claims cited. medRxiv preprint (ref on risk-weighted scheduling) still cited; flagged in risk report. |
