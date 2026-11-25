# Claim–evidence audit (2026-11-23)

Every number in Abstract/Results/Tables/KSP/cover letter is a placeholder resolved by manuscript/fill_values.py from
results/metrics.json, statistics.json, realworld.json, dataset_counts.json, run_meta_full.json. fill_values.py aborts if
any placeholder is unresolved. Numbers typed by hand in prose: only design constants from the protocol (k = 3–6, 5%
level, −0.3 dB/yr, p < 0.01 / 0.5, 60/20/20 split, 2,000 resamples, 10 draws, 12 configurations, 14 features, 5 seeds,
30 patients x 12 weekly tests, 10-percentage-point margin of H2, ρ ≥ 0.7 target of H3, validity rule 10% / 5%).

| # | Claim (location) | Evidence | Verdict / action |
|---|---|---|---|
| 1 | Pooled conformal (D6) and ML (D8) look specific on reference-stable eyes but raise many false alarms on true no-change data (Abstract, KSP, Results) | metrics.json D6/D8 k=3 spec, fpr_true_null; statistics.json fp McNemar | Supported |
| 2 | "only a true no-change check revealed" the false alarms (Abstract conclusion, Discussion) | Shuffle audit ALSO flagged D6/D8 at k=3 (fpr_shuffle 22.5%, 17.3%) | OVERSTATED -> rewritten: "that specificity on reference-stable eyes did not reveal"; Discussion now mentions the audit |
| 3 | No valid detector flagged significantly more progressors than D1 at any k (Abstract, KSP, Conclusions) | statistics.json: only significant sensitivity gain = D6 k=3 (invalid) | Supported |
| 4 | H2 not falsified; but gains ≥10 pp cannot be excluded (Results, Limitations) | paired CIs D2 k=3 (0.0 to 42.3), D8 k=6 (−7.7 to 30.8) | Supported; caveat present |
| 5 | "Rate and pointwise rules lost sensitivity with more tests" (Results) | D3 sens rises 3.8→23.1% | WRONG -> "gained little after four or five tests" |
| 6 | Reference-stable eyes "are easier" than typical stable eyes | inferred from selection rule, not measured | Softened to "may be easier to classify" |
| 7 | Secondary reference "gave the same ranking" | metrics.json sens_ref2; within-k Spearman 0.70–1.00 (computed in fill script) | Softened to "similar ordering" + ρ range |
| 8 | Shuffle audit over-estimates for rate/event rules | fpr_shuffle vs fpr_true_null D2, D7 | Supported; added under-estimation for ML at k=3 (D8, D9) |
| 9 | H3 only partly supported (ρ 0.65 < 0.7; 80% within 3 pp) | statistics.json rq3_audit_concordance | Supported |
| 10 | H4 supported for short series only | D8 k=3–5 > 5%, k=6 3.6%; D9 k=3, 5 | Supported |
| 11 | GRAPE: D2/D8 sensitivity gains came with significantly more false positives | statistics.json GRAPE false positives, Holm p | Supported |
| 12 | Real-world: D1 median 5 tests to first flag; ~1 test/year | realworld.json; dataset_counts uw_ref_interval_y_median | Supported (reference eyes only) |
| 13 | "224 and 277 unnecessary escalation discussions per 1,000 stable eyes" | 1000 × fpr_true_null | Supported as an arithmetic translation; assumes all flags discussed |
| 14 | D4/D10 cannot flag at k=3 | 3! = 6 orders, min p = 1/6 | Supported (design property) |
| 15 | Validity rule set before results | git: methods draft commit bd2c2e2 (09:14) precedes results commit 94777b8 (09:33) | Supported; disclosed as operationalisation of protocol wording |
| 16 | Artes data used once in development; did not change protocol | novelty_escalation_log.md round 5; protocol dated after round 5 | Supported; disclosed |
| 17 | "first"/"novel" claims | none made in manuscript | OK |
| 18 | Literature statements (Artes 2014 GPA specificity; Chauhan six tests in 2 y; Stagg testing intervals; Kim labels) | PubMed abstracts (citation_audit.md) | Verified at abstract level |
