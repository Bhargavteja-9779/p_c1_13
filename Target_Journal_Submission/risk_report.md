# Risk report and final decision (2026-11-23, after revision R1)

## Target
Ophthalmology and Therapy (Springer Nature / Adis), ISSN 2193-8245 / 2193-6528. Received→accepted (research articles,
2025-06 to 2026-11, n = 266): median 52.5 days, 75th percentile 70.25 days (journal_selection/acceptance_time_evidence.csv).
Survivorship limitation: only accepted papers are visible. JCR quartile (Q1) UNVERIFIED against JCR itself. APC USD 8,050.

## Honest label
**NOT REMARKABLE: honest strongest result.** No new method was found that beats the simple trend test (six development
rounds, two restarts; journal_selection/novelty_escalation_log.md). The paper is an evaluation/benchmark study whose
finding is that apparent early-detection gains of the tested conformal and ML detectors came with excess false alarms.

## Review round 1 → what R1 fixed
| Issue | Status |
|---|---|
| F1 validity rule not the protocol's | Fixed: three rules reported; main text uses rule-free "excess false alarms" (CI lower > 5%); deviation in Table 4 |
| F2 reference includes first k tests | Disclosed in Methods + Limitations; exploratory future-only reference (Table S5, too few eyes) |
| F3 failing detectors are own implementations | Claims restricted to tested implementations (Abstract, Discussion, Limitations, Conclusions) |
| M1/M4 estimand, bootstrap unit | Fixed in summarise_v2.py (seed-mean flags, patient-cluster bootstrap) |
| M5 "stable" = non-negative slope | Stated with numbers |
| M7 cumulative false alarms | Added (D1 12.6% over four reviews) |
| M8/M9 GRAPE PLR2/PLR3/any | Added; D1 weak on PLR2 – reported prominently |
| M10–M13 wording/disclosures | "analysis plan committed before final run"; development use and quick-mode exposure disclosed |
| M16 N/A detectors | Excluded from counts and Holm families |
| M26 AI disclosure | Kept (Springer Nature policy requires it) |
| M30 single command | code/reproduce.sh |

## Not fixed (remaining risks)
1. Small reference groups (26/26); M3 (use all eligible eyes for untrained detectors) not done → low power. HIGH.
2. A1 time-label sensitivity analyses (weekly spacing, variance inflation) not done → validity of rate rules conditional. MEDIUM.
3. No published ML/Bayesian comparator (ANSWERS, published deep models) → novelty/generality critique (Reviewer 10: reject). HIGH.
4. ML feature ablation / threshold variability (M18, M19) not done. MEDIUM.
5. Scope: therapy journal vs methods content (M24). MEDIUM–HIGH desk-rejection risk.
6. Unit tests cover only core utilities (M28). (Full re-run reproduced all per-eye outputs exactly: results/reproducibility_check.json.) LOW for editors, MEDIUM for reviewers.
7. Timeline: p75 70.25 d is close to the 72-day limit; one major revision can exceed it. MEDIUM.
8. Author items still open: second author name, department, e-mail; suggested reviewers.

## Desk-rejection probability (judgement, not data)
Moderate to high. Strengths: real clinical question, three public data sets, true no-change arm, transparent deviations,
negative results reported. Weaknesses: no new method, small n, own implementations of comparators, methods-heavy for a
therapy journal.

## Final decision
Package complete and internally consistent (all numbers machine-generated, citations verified).
By the brief's strict standard the study is **NOT READY** as a high-confidence Q1 submission (items 1–3 above). It can be
submitted as is with the risks above, or improved first (recommended next steps: M3 analysis on all eligible eyes, A1
sensitivity analysis, one published comparator).
