# ORIGINAL BRIEF (condensed faithfully; user's full prompt v2 "novelty-first, story-driven, journal-matched")

Goal: find, build, test, review, revise and package ONE research project solving a REAL-LIFE problem, novel enough to pass
editor desk check at a high-quality Q1 journal. Agent decides topic, dataset, model, gap, journal. Do not write paper first.
Earlier papers of the user were desk-rejected for "not enough novelty". If novelty weak: change the idea, don't hide it.

INTEGRITY (absolute): no fabrication (results, citations, datasets, p-values, novelty, journal data, acceptance times);
unrun experiment never appears as result; no "first/SOTA" without proof ("to the best of our knowledge, based on our search of
[databases, dates]..."); no seed/baseline/metric picking after results; no weak baselines; report negative results;
unavailable tool -> say so, mark UNVERIFIED; every paper number from machine-generated result file; no copied text.

JOURNAL CONSTRAINTS: submission->acceptance <= 72 days (evidence: >=20 recent articles' Received/Accepted dates, median well
under 72 AND 75th pct <= 72; save journal_selection/acceptance_time_evidence.csv); JCR-indexed Q1 high IF; established
publisher (OUP, CUP, Elsevier, Springer Nature, Wiley, T&F, IEEE, ACM, SAGE, IET); NO MDPI, no predatory. Scope fit > IF/speed.
Label first-decision time separately. Note survivorship limitation of dates.

PART A: >=10 candidate journals (internal), verify 72-day, check JCR/Q1/IF (UNVERIFIED if can't), select ONE, record fields:
TARGET JOURNAL / PUBLISHER / ISSN / JCR / QUARTILE / IF / CATEGORY / median & p75 days / first-decision (labeled) / APC /
scope fit / author rules / top rejection risks. If no journal meets all, choose strongest and list unmet rule.
PART B: benchmark >=25 recent papers (journal_benchmark.csv: problem, setting, datasets, #baselines, #datasets, #seeds, stats
tests, ablation, robustness, real-world evidence, code, length, figs/tables, refs, claimed novelty); journal_level_profile.md
(paper must meet/exceed median); style_notes.md (plain English).
PART C: >=15 candidate real problems with one-sentence story; Real-Problem Test (stakeholder, cited cost, documented failure,
legal data, real-world measure, scope fit); desk-rejection stress test.
PART D: novelty_map.csv >=30 closest papers; >=2 novelty types (N1 formulation, N2 method, N3 theory, N4 data, N5 eval
protocol, N6 real-world validation, N7 finding), one core scientific; scorecard 6 items 0-5 (>=22/30, none <3 to start);
Reviewer-Zero test; honest claims. D6 Novelty Escalation Loop (log experiments/novelty_escalation_log.md): diagnose, >=5
different families of fixes, check novelty map, pre-write hypotheses, fair test, keep only helpful+justified, rescore.
"Remarkable" = big real-world gain, step change w/ CI excl. 0, 2-sentence reusable idea, explains why, generalizes,
beats strong baselines, scorecard >=26 with distance & evidence >=4. Stop after remarkable or 6 rounds w/o gain -> change
angle; after 2 restarts deliver "NOT REMARKABLE: honest strongest result". Validation for selection, locked test touched once
per final candidate; count ideas, correct for multiple comparisons; report search in paper.
PART E: story spine (problem, tried, why not enough, idea, test, findings incl failures, meaning in real units, limits);
pilot evidence; hypothesis + 3-5 RQs; pre-register experiments/protocol.md (dated) with baselines (classical, conventional ML,
standard DL, strong recent, SOTA, lightweight), ablation, robustness, generalization, efficiency, sensitivity, error analysis,
real-world impact; same tuning budget; seeds; stats tests.
PART F: datasets (>1, license), leakage audit, project structure with config, seeds, CPU/CUDA/MPS, tests,
run_all.py --mode quick/full auto-generating results/figures/tables/stats.
PART G: fair baselines, relevant metrics + real-world measure, >=5 seeds (10 for small), mean±SD+CI, ablations, robustness,
generalization, proper stats (paired, Wilcoxon, McNemar, permutation, bootstrap, effect size, correction), error analysis,
case studies, explainability.
PART H: figures/tables from real data; manuscript in journal's guidelines & style; plain English; limitations; data/code
availability; declarations.
PART I: claim-evidence audit, citation audit (verify DOIs), plagiarism check, pre-submission desk check.
PART J: 10 adversarial reviews + stakeholder review (REVIEW/review_XX.md), FATAL/MAJOR/MODERATE/MINOR, fix research.
PART K: consistency audit, reproducibility audit, Final_Manuscript.docx (+pdf), cover_letter.docx, risk_report.md,
final decision READY FOR SUBMISSION / NOT READY (if not ready, keep going).
Output folder: /Target_Journal_Submission/{journal_selection, manuscript, code, results, figures, tables, supplementary, REVIEW}
Show user only: selected journal + 72-day evidence, one-sentence story, novelty scorecard, final package.
User added: SAVE EVERY STEP (commit+push) so another account can say "continue" and resume.
