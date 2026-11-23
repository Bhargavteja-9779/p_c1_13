# Supplementary Material

Early Detection of Glaucomatous Visual Field Progression Without False Alarms: A Benchmark With True No-Change Data

## S1. Development history (all ideas tried, including failures)

The benchmark was the third framing of this project. Before it, we developed and tested on validation data only (never the locked test set) the following ideas, each with a hypothesis stated in advance. Full numbers are in the code repository (`journal_selection/novelty_escalation_log.md` and `results/pilot_*.json`, `results/d6_round5.json`).

1. Self-supervised temporal-order network as a learned permutation statistic (round 0): no gain over PoPLR or the mean-sensitivity trend; kept as detector D10.
2. Population-calibrated (pooled-shuffle) null for short series (round 1): valid false alarms, gains only at 3–4 tests; kept as D5.
3. Risk-controlled deferral of visual field tests (round 2): no gain over a simple severity rule; no deferral threshold could be certified.
4. Pooled null against a future reference (round 3): gains only at 3–4 tests, small sample.
5. A different disease area (neovascular AMD, injection rhythm and visual outcome, Moorfields open data; round 4): no added value.
6. Noise-stratified and regional detrended pooled nulls (round 5): the apparent gain at three tests was a false-alarm artefact on true no-change data (Artes); the regional variant is kept as D6.

The Artes retest data were used in round 5 only to check false-alarm rates of development variants. Because several ideas were tried, the benchmark comparisons were pre-registered and corrected for multiple comparisons (Holm), and we make no claim of a new superior method.

## S2. Analysis plan status and deviations

The analysis plan (`experiments/protocol.md`) was time-stamped in version control (commit c0dedb5, 2026-11-23 09:05 UTC) before the final run (results committed 09:33 UTC); it was not deposited in a public registry. A pipeline check in quick mode (models trained on a subset of development data; locked UWHVF test set not used) was run on the Artes and GRAPE data at about 09:08 UTC, before the validity rule in the manuscript draft (09:14 UTC) was written. Deviations from the plan:

1. Validity: the plan said only that the upper confidence limit would be compared with 5%. We report three readings (Methods); the manuscript draft rule (lower ≤5%, upper ≤10%) was written after the pipeline check.
2. RQ2 margin: the plan's hypothesis H2 named a 10-percentage-point margin; with 26 progressors this margin could not be tested with adequate power, and the manuscript reports estimates with confidence intervals instead.
3. Confidence intervals for paired differences were first computed at the eye level; after review they were recomputed with the patient-cluster bootstrap, as the plan specified. The McNemar test treats eyes as independent.
4. GRAPE D5 calibration: the plan named leave-one-patient-out; amendment A2 (before final results) changed this to five-fold patient-level cross-fitting.
5. D8 features: the plan listed example features (MD level/slope/z, PLR counts, PoPLR S, worst region slope, range, SD); the implemented set of 14 features (`tab_features` in `code/src/models/detectors.py`) uses mean sensitivity level, change, slope and its t statistic, pointwise-regression summaries (share of locations with fast significant loss, share with p < 0.05, mean −log p, mean of the worst 10% of slopes, slope SD), test-to-test variability, range, number of tests and follow-up time; it does not include the PoPLR statistic or a regional slope.
6. Pre-specified secondary GRAPE labels (PLR2, PLR3, any) are reported in Table S4 (they had been omitted from the first draft).
7. Post hoc analyses added after review (not in the original plan): future-only reference (Table S3); GRAPE eyes with at least k + 2 visits (Table S4); exact intervals (Table S1); minimum detectable difference; and analyses P1–P3 (Table S5), whose plan and expectations were added to `experiments/protocol.md` before they were run.
8. The bootstrap interval for the shuffle-audit correlation resamples detector × test-number cells, which are not independent; it is approximate.

Note on D4: PoPLR is deterministic for k ≤ 7; its between-seed variation on true no-change data comes only from the random assignment of test dates (amendment A1), which used different random draws for different seeds.

## Supplementary Fig. S1. Participant flow

![Participant flow](../figures/figS1_flow.png)

Numbers from results/descriptives.json. E1–E4: evaluation sets (see Methods).

## Table S1. Seed variability, secondary (PoPLR-based) reference and strict validity

{{SUPP_T1}}

## Table S2. All paired comparisons with D1 (exact McNemar test, Holm correction within each number of tests and endpoint)

{{SUPP_T2}}

pp, percentage points. Paired comparisons use the majority flag over seeds for stochastic detectors.

## Table S3. Post hoc future-only reference (UWHVF test set; reference computed only from tests after the first k, at least five later tests)

{{SUPP_T3N}}.

{{SUPP_T3}}

Patient-cluster bootstrap 95% CIs. Progressor: later-test slope of mean total deviation < −0.3 dB/year with one-sided p < 0.01.

## Table S4. GRAPE by label and by number of visits (post hoc restriction; secondary labels pre-specified)

{{SUPP_T4}}

MD, PLR2, PLR3: progression labels supplied with the GRAPE data set; any: any of the three. Patient-cluster bootstrap 95% CIs.

## Table S5. Post hoc analyses P1–P3 (seed 0)

{{SUPP_T5}}

P1, GRAPE shuffle audit (first k tests re-ordered, 10 times per eye). P2, Artes no-change windows with an added global visit shift (SD {{px:sig:add}} dB). P3, tabular model with threshold at the 95th percentile of scores on shuffled training series (E1, UWHVF test set; E2, true no-change). Patient-cluster bootstrap 95% CIs. Single seed, so the machine-learning rows in P2 differ from Table 1 partly because of seed variation.
