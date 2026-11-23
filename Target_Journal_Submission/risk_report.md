# Risk report and final decision (2026-11-23)

## Honest label
**NOT REMARKABLE: honest strongest result.** Six development rounds and two restarts produced no method that beats a
simple trend test (journal_selection/novelty_escalation_log.md). The paper is an evaluation/benchmark study whose main
finding is negative: every significant early-detection gain came with excess false alarms, invisible to full-series
reference specificity. Novelty scorecard at start was 22/30 (journal_selection/novelty_scorecard.md); after review the
novelty of the shuffle audit is weaker (prior PoPLR / Artes 2014 work) and H3 was not supported.

## Final decision: NOT READY FOR SUBMISSION
Blocking items that only the authors can resolve:
1. Author names, affiliations, ORCID, corresponding author, funding, conflicts, CRediT contributions, repository URL
   (placeholders "[TO BE COMPLETED BY THE AUTHORS]" in manuscript and cover letter).
2. A statement of how the authors verified AI-written code and analyses (journal AI policy).
3. Decision on APC (USD 8,050) and direct JCR quartile check (UNVERIFIED here).
Post hoc analyses P1-P3 (GRAPE shuffle audit, no-change arm with long-term fluctuation, shuffle-calibrated ML threshold)
were planned, run and reported (Table S5). Scientific items still open: nested-CV ML, refitted D8 on GRAPE (I11),
published comparators VFI/ANSWERS (I21), flow diagram and TRIPOD+AI checklist.

## Top desk-rejection risks
| Risk | Likelihood | Mitigation |
|---|---|---|
| "Not enough novelty" (negative benchmark; shuffle idea not new) | HIGH | Frame as evaluation-standard paper; emphasise ML-threshold finding and built-in specificity of full-series references |
| Scope: methods paper in a therapy journal | MEDIUM | Framed around treatment-escalation decisions; consider TVST or Ophthalmology Glaucoma as alternatives (not 72-day verified) |
| Small samples (26/26; 30 null patients) | HIGH | Stated prominently; MDD reported |
| Development data reused (Artes) and own variants as detectors | MEDIUM | Fully disclosed |
| Timeline: p75 acceptance 70 d vs 72-d rule | MEDIUM | journal_selection/selected_journal.md |
| JCR Q1 not directly verified | MEDIUM | User asked to check |

## Integrity checks performed
- Every result number filled from results/*.json by manuscript/fill_values.py; 34 programmatic claim checks pass.
- Statistics reproduce byte-for-byte from raw results (audits/reproducibility_audit.md); full re-run: see audit.
- 33 cited DOIs re-resolved on Crossref (audits/citation_audit.md).
- Post hoc analyses labelled post hoc; protocol deviations listed (Supplementary S2).
- Plagiarism: all text written fresh; no copied passages (automated plagiarism service not available -> UNVERIFIED by tool).
