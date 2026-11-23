# Review 04 — Biostatistician

## Summary
I re-derived the summary statistics. I re-ran `src.statistics.summarise` on `results/raw_results.csv.gz` in a scratch copy, and `metrics.json` and `statistics.json` reproduced exactly. The numbers in the manuscript match the JSON files. The statistical design and reporting, however, have serious problems:

- the main validity criterion is not the pre-registered one;
- the reported proportions and the reported paired differences and tests are computed on different quantities;
- the confirmatory hypothesis (H2) cannot in practice be falsified with 26 progressors;
- the bootstrap is described as patient-level, but for paired differences it is eye-level.

**Recommendation: Major revision (borderline reject in current form).**

## Issues

1. **FATAL — The validity rule is not the pre-registered rule, and under the pre-registered rule the reference detector D1 is itself invalid (Methods "Statistical Analysis", sentences 3–4; Table 1 footnote "Valid").**
   - The protocol (`experiments/protocol.md`, Statistics) says: "Validity: FPR CI upper bound vs 5%."
   - The manuscript uses "upper limit ≤ 10% and lower limit ≤ 5%".
   - This rule is not an amendment in the protocol (only A1 and A2 exist). It first appears in a Methods draft (commit bd2c2e2, 09:14). That is after the protocol (09:05) and after the code and quick-run commit (09:08), and while the full run was probably executing: its runtime was 1,458 s and the results were committed at 09:33. The wording at that point also differed ("point estimate did not exceed 5% by more than sampling error"). The final wording is in `manuscript/fill_values.py`, written after the results.
   - Under the literal protocol rule (upper CI ≤ 5%), D1's upper limits are 6.3%, 6.2%, 7.5% and 8.1% at k = 3–6. D1 would be **invalid at every k**, and H2 ("no *valid* detector beats D1") would need reframing.

   *Fix:* report this as a protocol deviation (an amendment A3 with its true timestamp). Present RQ1 and RQ2 under both the literal rule and the 10% rule. Justify the 10% margin a priori, for example as twice nominal. Remove "Before the results were seen" unless it can be documented independently.

2. **MAJOR — Reported proportions and paired comparisons refer to different estimands (Abstract Results; Results RQ2; Table 1 vs Table S3).**
   - In `summarise.py`, the proportions are seed-averaged flags (mean over 5 seeds per eye). The McNemar tests and the "difference vs D1" use a **majority vote over seeds** (`.mean().round()`). The Methods do not say this; only the Table S3 footnote does.
   - Consequences:
     - D6 at k = 3 is reported as 56.9% with "+38.5 pp vs D1", but 56.9 − 19.2 = 37.7. The 95% CI for the difference (19.2 to 57.7) has an upper limit *above the detector's own sensitivity*, which is arithmetically impossible on the reported estimand.
     - D8 at k = 6 is 70.8% vs 57.7%, a difference of 13.1, reported as +11.5.
     - GRAPE D8 is 65.9% vs 44.4%, a difference of 21.5, reported as +25.9.
     - D8 specificity at k = 3 is reported as 94.6% vs 96.2%, yet the McNemar table shows 0/0 discordant pairs.

   *Fix:* use one estimand throughout. Preferably test the seed-averaged decision, or pre-specify one seed or the majority-vote detector as "the" detector and report its own proportions. State the choice in Methods.

3. **MAJOR — H2 cannot be falsified with this design (Introduction last para; Results RQ2 "the hypothesis was not falsified"; Conclusions).**
   - With 26 pairs and Holm over 9 comparisons, the smallest raw p must be < 0.0056.
   - An exact two-sided McNemar reaches this only with ≥ 9 discordant pairs in one direction and 0 in the other (2 × 0.5⁹ = 0.0039; 8:0 gives 0.0078). With one reverse discordance, 12:1 is needed.
   - So "falsification" requires a gain of at least about 35 percentage points. The pre-specified 10-pp margin is irrelevant to the decision.
   - "Not falsified" therefore carries almost no information. The text then reads it as evidence that D1 is "hard to beat" (Discussion para 1; Conclusions).

   *Fix:* report a power or precision analysis. Reframe RQ2 as estimation with CIs, or as a non-inferiority or equivalence question with a margin. Remove "hard to beat" and "not beaten by a valid detector" (Discussion para 3) unless an equivalence test supports them.

4. **MAJOR — The paired bootstrap ignores clustering (Methods: "95% CI from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient").** In `summarise.py` the difference CI resamples *eyes* (`diff[rng.integers(0, len(diff), len(diff))]`), not patients. The 52 reference eyes come from 41 patients. The exact McNemar test also assumes independent pairs. *Fix:* use a patient-cluster bootstrap for the differences and a clustered McNemar test (e.g., Obuchowski / Durkalski), or include one eye per patient as a sensitivity analysis.

5. **MAJOR — The sample size is self-imposed and avoidable (Results "Study Data": 26 + 26).**
   - D1–D4 need no training data at all. D5–D7 only need training eyes for calibration.
   - Across the whole UWHVF there are 690 eyes with ≥ 8 tests. In my re-run of the reference function, 150 were progressors and 164 stable: 93/99 in train, 31/39 in validation, 26/26 in test.
   - The non-learned detectors could have been compared on all of these, and the calibrated ones on val + test (57 progressors, 65 stable). That gives 2–6 times the sample size.

   *Fix:* add this as a pre-declared secondary analysis, labelled post hoc. If the conclusions hold with n ≈ 300 for D1–D4, the paper is much stronger.

6. **MAJOR — Multiplicity across numbers of tests, endpoints and data sets (Methods "Statistical Analysis"; Results RQ2 "This was the only significant gain in the study").**
   - Holm is applied within each k × endpoint (9 or 6 tests). Overall there are 96 paired tests (4 k × 2 endpoints × 9, plus 2 k × 2 endpoints × 6).
   - k = 3..6 are nested looks at the same eyes.
   - Calling one result "the only significant gain in the study" invites study-wide interpretation without study-wide control.

   *Fix:* state the family explicitly. Either control across the whole study or present the results as descriptive. Avoid study-wide language.

7. **MODERATE — RQ3 inference is invalid and incomplete (Results "The Shuffle Audit"; Fig. 3).**
   - The 40 cells are not independent: 10 detectors × 4 nested k on the same eyes.
   - Three k = 3 cells are structural zeros in both measures (D4, D7, D10).
   - D5 is calibrated on shuffled training series, and D4/D10 are within-eye permutation tests that are exact under shuffling. Their agreement is guaranteed by construction.
   - The p < 0.001 for ρ is therefore meaningless. The protocol's bootstrap CI for ρ is not reported.

   *Fix:* drop the p-value. Report a patient-cluster bootstrap CI for ρ. Repeat the analysis excluding structural zeros and detectors that are exact under permutation.

8. **MODERATE — Degenerate percentile-bootstrap CIs (Table 1, many cells "100.0 (100.0–100.0)" and "0.0 (0.0–0.0)").** A CI of zero width for 26/26 is not credible: the exact lower limit for 26/26 is 86.8%. *Fix:* use cluster-adjusted Wilson or Clopper–Pearson intervals for boundary proportions.

9. **MODERATE — The validity dichotomy is fragile (Results RQ1; Table 1).**
   - D9 at k = 6 is "invalid" with an upper limit of 0.100002, displayed as "10.0".
   - D6 at k = 5 is "valid" with a point estimate of 6.2%.
   - D6 at k = 4 and D10 at k = 5 are "valid" at 5.1%.

   *Fix:* report the CIs and let readers judge. If a rule is kept, report how sensitive it is to the bootstrap seed.

10. **MODERATE — Pre-registered items are not reported:** the per-seed SD ("All seeds reported (mean ± SD)", which is in the JSON but not in any table); the bootstrap CI for ρ; specificity against the secondary reference; and the GRAPE secondary labels PLR2, PLR3 and "any". *Fix:* report all of them, at least in the Supplement.

11. **MODERATE — Wording that treats non-significance as equivalence.** Examples: "Both looked about as specific" (Abstract); "Neither difference was significant" (Results); "D5 matched D1"; "was not beaten by a valid detector". *Fix:* use estimation language with CIs and avoid equivalence claims.

12. **MINOR — The cumulative-look analysis (Table 3) combines a cumulative sensitivity with a per-look false-alarm rate.** *Fix:* compute the cumulative true-null false-alarm probability on Artes over looks 3..6, using the same windows.

13. **MINOR — Median tests to first flag of 5.5 for D7.** This is the average of the 13th and 14th order statistics of a discrete, censored variable (`describe.py`). *Fix:* use the smallest k at which the cumulative detection reaches ≥ 50%, i.e., Kaplan–Meier style.

14. **MINOR — No inferential comparison of true-null false-alarm rates with D1 (RQ1).** "5.0 and 6.3 times as many" has no CI. *Fix:* add a patient-cluster bootstrap CI for the ratio or the difference.
