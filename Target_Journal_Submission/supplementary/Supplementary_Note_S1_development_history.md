# Supplementary Note S1. Development history, including abandoned ideas

This study did not start as a benchmark. We report every idea we tested before the analysis plan was fixed, so that
readers can judge how many analyses were tried. All pilot analyses below used only the UWHVF training and validation
sets; the UWHVF test set and the GRAPE data were not used before the final run. The Artes retest data were used once
during development (round 5) to check false alarms. Full numbers are in the code repository
(journal_selection/novelty_escalation_log.md; results/pilot_v0.json, pilot_v1.json, pilot_v2.json,
pilot_deferral.json, d6_round5.json).

| Round | Idea | Hypothesis (stated before the test) | Outcome |
|---|---|---|---|
| 0 | Self-supervised "true order versus shuffled order" network as a test statistic, calibrated by within-eye permutation (became D10) | Flags more eyes than PoPLR or a mean-sensitivity permutation test at the same level | Rejected: no gain at 4–8 fields; within-eye permutation cannot reach p < 0.05 with 3 fields |
| 1 | Null distribution pooled from shuffled series of other (training) eyes, stratified by number of fields and mean sensitivity (became D5) | Valid false-alarm rate and more power with few fields | Small gain at 3–4 fields only; no gain at 5 or more |
| 2 | Re-framing: risk-controlled deferral of visual field tests (defer a test when predicted risk is low, threshold chosen by distribution-free risk control) | Saves tests while bounding delayed detection | Rejected: a learned risk model saved no more tests than a simple severity rule at the same delay, and no threshold could be certified |
| 3 | Pooled null evaluated against a future-confirmed reference (validation set) | Higher sensitivity at matched specificity | Gain at 3–4 fields only, in a small sample |
| 4 | Different problem: injection rhythm in neovascular age-related macular degeneration (public Moorfields data) | Year-1 injection rhythm adds prognostic value for 3-year visual acuity | Rejected: no added value |
| 5 | Detrended pooled null and regional (worst-region) statistics (became D6), checked on true no-change data (Artes) | Added power at 3 fields with valid false alarms | Rejected: the apparent gain at 3 fields came with false-alarm rates of about 13–22% on true no-change data |

Because no method idea produced a valid gain, we changed the question to an evaluation question and wrote the
benchmark protocol (dated 2026-11-23) before the final run. Detectors D5, D6 and D10 in the benchmark are the
development ideas above; they were kept, unchanged, so that their final performance on held-out data is reported.
