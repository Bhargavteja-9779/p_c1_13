# Novelty scorecard (D3) — topic: clinic-calibrated (conformal) visual-field progression testing

Searched: OpenAlex, PubMed/PMC, Europe PMC, Crossref, arXiv, medRxiv (via Crossref/OpenAlex), Semantic Scholar
(rate-limited), web search; 2026-11-23 (novelty_search_log.md). Google Scholar, IEEE Xplore, Scopus not reachable.
Novelty map: novelty_map.csv (55 rows).

Novelty types claimed (with evidence):
- N2 new method idea: conformal p-values for progression from a calibration pool of SHUFFLED (and detrended-shuffled)
  routine series of other patients, stratified (Mondrian) by order-invariant summaries; works for any trend statistic.
  Closest: PoPLR (within-eye permutation, O'Leary 2012); GPA (population test-retest limits from a dedicated cohort);
  conformal VF forecasting (Si et al. MICCAI 2025: intervals for forecasts, not tests); classification permutation
  test (statistics literature). None builds the null from shuffled clinic data.
- N3 analysis: finite-sample validity under within-eye exchangeability + exchangeability of eyes within a stratum.
- N5 evaluation: false-alarm rate on TRUE no-change data (Artes 12-week retest) in addition to shuffled data, plus
  future-reference and clinician-label evaluation — most VF-progression ML papers report neither.
- N6 external clinic (GRAPE, China) calibrated on its own data.

| Item | Score (0-5) | Evidence |
|---|---|---|
| 1. Distance from closest 5 papers | 4 | none uses shuffled-clinic conformal calibration; PoPLR/GPA/ANSWERS differ in null construction |
| 2. Strength of problem | 4 | escalation decisions; 5+ tests needed; documented PoPLR floor at k=3 |
| 3. Depth of idea | 4 | validity argument; detrending; Mondrian; applies to any statistic |
| 4. Strength of evidence | 3 | pilot gain only at k=3-4; small reference sets; to be strengthened with 3 datasets |
| 5. Generality | 4 | method applies to any repeated clinical measurement (VA, RNFL, IOP); 2 clinics + retest |
| 6. Journal level match | 3 | above the journal's typical evidence level, but methods-heavy for a therapy journal |
| **Total** | **22 / 30** | passes the start gate (>=22, none <3); far from the 26 "remarkable" bar |

## Reviewer Number Zero (hardest desk-reject sentences)
1. "This is PoPLR with a pooled permutation distribution; the advance is incremental."
2. "Borrowing a null from other patients breaks the exact within-eye guarantee; validity is only approximate."
3. "Gains appear only at 3-4 tests and the clinical value of a slightly earlier flag is not shown."
Reply (evidence-based): (1) the within-eye null is mathematically unable to reject at k=3 and is coarse at k=4; the
pooled conformal null removes that floor and works for any statistic — novelty map shows no prior use. (2) We state the
exact condition (exchangeability of eyes within a stratum) and test validity empirically on TRUE no-change data and on
held-out shuffled data in two clinics. (3) We quantify earlier detection in tests and years against a future reference
and clinician labels; if gains are small we will say so. Assessment: reply is reasonable for (1)-(2); (3) is the main
weakness -> addressed in D6 rounds.
