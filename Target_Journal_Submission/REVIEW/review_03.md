# Review 03: Biostatistician

## Summary
I checked the statistical methods against `code/src/statistics/summarise.py`, `descriptives.py`, `results/metrics.json`, `results/statistics.json` and `results/realworld.json`. Most numbers in the text and tables reproduce from the JSON files. However:

- The paired analyses do not do what the Methods say: they ignore patient clustering.
- The CIs degenerate at the boundaries.
- The validity rule was changed from the protocol, and it is fragile at the fourth decimal.
- The main negative conclusion comes from a test with very low power.

## Recommendation
**Major revision.**

## Issues

1. **FATAL – The validity rule is not the protocol rule, and conclusions depend on it.**
   - *Location:* Methods, Statistical analysis; Supplement S2; Table S1.
   - *Problem:* The protocol says "Validity: FPR CI upper bound vs 5%". The manuscript uses "lower ≤5% and upper ≤10%". Under the protocol rule:
     - D1 is invalid at every k (upper limits 6.27, 6.22, 7.50, 8.14%);
     - D4 and D5 are invalid at 5–6 tests;
     - only D2, D3, D7 (and D9 at k = 4) are valid.

     RQ2 compares "valid" detectors with D1, so the inferential frame changes. Moreover, "lower ≤5%" means "not significantly above 5%", which rewards imprecision: a detector with a wider CI is more likely to pass.
   - *Fix:*
     - Pre-specify the rule as a one-sided test of H0: FPR ≤ 5% against a tolerance (e.g. upper one-sided 95% limit ≤ 7.5%).
     - Report the protocol rule in the main Table 1.
     - State plainly in the Abstract that D1's upper limit exceeds 5% at every k.

2. **MAJOR – The paired differences and McNemar tests ignore clustering, contrary to the Methods and the protocol.**
   - *Location:* Methods ("Proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients"); Results (+38.5 pp [19.2 to 57.7]); Table 2; Table S2.
   - *Problem:* In `summarise.py`, the difference CI uses `diff[rng.integers(0, len(diff), len(diff))]`, which resamples **eyes**. McNemar treats eyes as independent. This matters because:
     - the 52 reference eyes come from 41 patients;
     - GRAPE has 263 eyes from 144 patients.

     The protocol required a patient-cluster bootstrap for E1/E4.
   - *Fix:* Use a patient-cluster bootstrap for the differences and a clustered McNemar test (Obuchowski 1998, or GEE with a binomial link). Re-compute the Holm p-values.

3. **MAJOR – Power is too low to support "not falsified"; the hypothesis structure is inverted.**
   - *Location:* Introduction final paragraph; Results RQ2 ("Our hypothesis … was therefore not falsified").
   - *Problem:* With n = 26 and an exact McNemar test, raw p < 0.05/9 = 0.0056 needs at least 9 discordant pairs, all favouring the detector (2·0.5⁹ = 0.0039). That is a ≥35-pp gain. The study could therefore only detect enormous gains, and absence of significance is uninformative. Most CIs for valid detectors include +20 pp (Table S2). The protocol margin ("≥10 percentage points") is not tested anywhere: Holm p < 0.05 tests a difference > 0, not > 10 pp.
   - *Fix:*
     - Add a power / minimum-detectable-difference statement.
     - Recast RQ2 as estimation, judging each CI against the 10-pp margin (superiority if the lower limit is > 0, a clinically important gain excluded if the upper limit is < 10).
     - Report which detectors can exclude a 10-pp gain. None can.

4. **MAJOR – Percentile bootstrap CIs are degenerate at 0% and 100%.**
   - *Location:* Table 1 (e.g. "0.0 (0.0–0.0)", "100.0 (100.0–100.0)"); Table 2.
   - *Problem:* A 0/26 or 26/26 result does not imply zero uncertainty. The exact one-sided 97.5% bound for 0/26 is 13.2%.
   - *Fix:* Use cluster-adjusted Wilson or Clopper–Pearson intervals (design-effect corrected), or a BCa bootstrap with a boundary fallback.

5. **MAJOR – The validity decision for D9 at six tests depends on Monte-Carlo noise.**
   - *Location:* RQ1 ("at six tests its upper confidence limit was 10.0%, just above the 10% bound"); Table 1 row "6 | D9 | 5.9 (2.3–10.0) | No".
   - *Problem:* `fpr_true_null_hi` = 0.100002381, i.e. 0.0000024 above the bound. Another bootstrap seed would likely reverse the call. The table shows "10.0", which a reader will read as ≤10%.
   - *Fix:* Report more decimals or the Monte-Carlo error of the bootstrap limit, and avoid knife-edge binary labels. D9 at 5 tests (7.5% [2.8–13.3]) is also invalid but is not mentioned in the RQ1 paragraph; add it.

6. **MAJOR – The RQ3 concordance statistics are inflated and the CI is invalid.**
   - *Location:* Shuffle audit section; `descriptives.realworld()`.
   - *Problem:*
     - Three of the 40 cells (D4, D7 and D10 at k = 3) are structurally 0/0. They add perfect agreement by construction. Excluding them, Spearman ρ = 0.56 (my recomputation from `metrics.json`), and the share within 3 pp falls.
     - The cells are not independent: the same detector appears at four k, and the same eyes and windows are used throughout. Resampling cells i.i.d. therefore understates uncertainty.
     - The pre-specified target ρ ≥ 0.7 was missed.
   - *Fix:*
     - Exclude structural zeros.
     - Bootstrap at the patient level (re-computing both rates) or by detector.
     - Report agreement as a Bland–Altman bias with limits, and state in the Abstract that H3 failed.

7. **MODERATE – Multiplicity across k and endpoints is not addressed.**
   - *Location:* Statistical analysis.
   - *Problem:* Holm is applied within each k and endpoint (9 tests). There are 4 k × 2 endpoints in UWHVF plus 2 × 2 in GRAPE, i.e. 12 families. The single significant finding (D6, k = 3) is robust to this, but the issue should be stated.
   - *Fix:* Either declare k = 3 as primary or apply a gatekeeping/hierarchical procedure.

8. **MODERATE – Seed handling is inconsistent.**
   - *Location:* Statistical analysis ("Stochastic detectors were summarised by the mean flag over seeds"); `run_all.py` lines 57, 64.
   - *Problem:* The E2 donor time-draws use `rng = default_rng(1000 + seed)`. Deterministic detectors (D1–D3, D7) are run with seed 0 only, so they get one set of donor draws, while "stochastic" detectors get five. D4 is deterministic for k ≤ 7 (exact enumeration), so its "seed SD" (0.2 pp) is donor-draw variance, not detector stochasticity. Comparisons with D1 therefore use different Monte-Carlo designs.
   - *Fix:* Use identical donor draws for all detectors (common random numbers) and run all detectors over the same seeds.

9. **MODERATE – The Artes effective sample size is overstated.**
   - *Location:* Table 1 ("n" behind FA = 3,000 at k = 3).
   - *Problem:* The 300 windows × 10 draws come from 30 eyes of 30 patients. The windows overlap and the draws only relabel time. The patient bootstrap is the right approach, but readers will see 300/270/240/210 "windows". With 30 clusters, percentile CIs are known to under-cover.
   - *Fix:* State that the effective n is 30. Consider a bootstrap-t or a cluster-robust binomial GLM.

10. **MINOR – Arithmetic and reporting checks.**
    - *Location:* Throughout.
    - *What I verified:* Every Table 1 cell matches `metrics.json`; the Table 2 and S2 differences and Holm p-values match `statistics.json`; ρ = 0.648 (CI 0.354–0.853); median absolute difference 0.96 pp; 80% within 3 pp; Table 3 matches `realworld.json`.
    - *Problems found:*
      - "D5 flagged exactly the same reference eyes as D1 at every number of tests" holds only for majority flags. The seed-averaged sensitivity at k = 6 differs (56.9% vs 57.7%).
      - Typo: "was therefore not met, In a post hoc look".
    - *Fix:* Qualify the D5 sentence and correct the typo.
