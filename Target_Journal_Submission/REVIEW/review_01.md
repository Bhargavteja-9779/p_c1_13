# Review 01 — Biostatistician

**Manuscript:** "Detecting Glaucomatous Visual Field Progression From Few Tests Without False Alarms: An Open Benchmark With a True No-Change Arm"
**Reviewer focus:** multiplicity, confidence intervals, clustering, the validity rule, power, use of McNemar/Holm, circularity of the reference standard.

## Summary

The authors compare ten progression detectors using the first k = 3–6 fields. They report sensitivity against a future reference (26 progressing and 26 stable test-set eyes in UWHVF), false-alarm rates (FPR) on 30 Artes weekly-retest series, a "shuffle audit", and an external check in GRAPE. The main inferential claim is that "no detector with a valid false-alarm rate flagged significantly more progressors than the trend test at any number of fields". The secondary claims are that the abstract's headline detectors (D6, D8) have inflated FPRs, and that the shuffle audit tracks the true FPR.

I re-derived the reported numbers from `results/metrics.json`, `results/statistics.json`, `results/descriptives.json` and `results/raw_results.csv.gz`, and I read `code/src/statistics/summarise.py`, `manuscript/fill_values.py` and the git history of `code/experiments/protocol.md`. Most point estimates in the text match the result files. The inferential framework does not hold up:

- The primary hypothesis cannot be falsified at this sample size.
- The validity rule was set after the results were seen, and it differs from the protocol.
- The CIs for paired differences ignore the clustering that the Methods claim to handle.
- The primary reference partly re-uses the same fields the detectors see.
- The headline FPR finding for D6 had already been measured on the same Artes data before the protocol was written.

## Issues

### 1. FATAL — The primary hypothesis H2 cannot be falsified with 26 progressors; "not falsified" is presented as evidence of no benefit
*Location:* Results, "Sensitivity against the future reference (RQ2)": "No detector with a valid false-alarm rate flagged significantly more reference progressors than D1 at any number of fields … so the pre-specified hypothesis H2 was not falsified." Key Summary Points: "No detector with a valid false-alarm rate beat the simple trend test significantly at any number of fields, so the evidence does not support replacing it in routine care." Conclusion: "No valid detector beat a simple trend test."

*Problem:* H2 (protocol) is falsified only by a ≥10-point gain with Holm-adjusted exact McNemar p < 0.05 across 9 comparisons. With n = 26, I computed the exact two-sided McNemar values: 8 vs 0 discordant pairs gives p = 0.0078 (Holm ×9 = 0.070, not significant), and 10 vs 1 gives p = 0.0117 (×9 = 0.105). The smallest configuration that reaches significance is 9 vs 0, which is a gain of at least 35 percentage points with no losses at all. A 10-point gain is undetectable by design. The power for the pre-specified 10-point margin is close to α. The Limitations paragraph admits that "moderate gains (around 10 points) cannot be excluded", but the abstract, Key Summary Points and Conclusion still turn absence of evidence into "no valid detector beat" and "does not support replacing it".

*Fix:* Report a pre-analysis power or minimum-detectable-difference calculation, including the 9/0 configuration above. Reframe H2 as non-inferiority or estimation: report each valid detector's paired difference with its CI, and say which differences the data exclude. For example, D2 at k = 3 is +19 points (0 to 42), and D8 at k = 6 is +12 (−8 to 31); neither rules out large benefits. Remove "does not support replacing it" and "No valid detector beat …" from the Key Summary Points, abstract and Conclusion, or qualify them with "with 26 progressors we could only detect gains of about 35 points or more".

### 2. FATAL — The validity rule was chosen after the results and contradicts the protocol; it decides which detectors count as "valid"
*Location:* Methods, Statistical analysis: "A detector was considered valid if the upper limit of its false-alarm confidence interval on true no-change data did not exceed 10% and its point estimate did not exceed 5% by more than sampling error." Table 2 footnote: "† False-alarm rate not valid (95% CI upper limit above 10% or lower limit above 5%)."

*Problem:* The protocol says only "Validity: FPR CI upper bound vs 5%" (RQ1: "at or below the nominal 5%"). The 10% upper-limit rule appears first in `manuscript/fill_values.py` line 41–42. PROGRESS.md records "Validity rule implemented: FPR CI hi <= 10% AND CI lo <= 5%" in the manuscript-filling session. That session came after the full results were committed (commit 94777b8 at 09:33; the protocol is commit c0dedb5 at 09:05). Neither A1 nor A2 mentions it. The rule decides the result. Under the literal protocol rule (upper bound ≤ 5%), D1 itself is invalid at every k: its upper limits are 6.3%, 6.2%, 7.5% and 8.1%. Under that reading, the "simple trend test remains a strong default" message reverses. Two further problems with the post-hoc rule:
- It is asymmetric. Upper ≤ 10% tolerates a true FPR of up to about 8%.
- It labels as "valid" detectors that cannot flag at all. D4, D7 and D10 at k = 3 have FPR 0.0 (0.0–0.0) and sensitivity 0, yet they count toward "7 of ten valid".

The Methods also state that "Two amendments were made before any final result was seen". That sentence is true only for A1/A2. The validity operationalisation is a third, undeclared, post-hoc change.

*Fix:* Declare the 10% rule as a post-hoc deviation in Methods and in the protocol amendment list, with the date. Report results under the protocol rule as the primary or a co-primary analysis, including D1's status. Consider a pre-justified tolerance, e.g. a one-sided test of FPR ≤ 5% + δ with δ stated and justified. Report "cannot flag" separately from "valid".

### 3. MAJOR — The headline D6 finding is not new evidence: D6's FPR on the same Artes data was known before the protocol
*Location:* Abstract: "a pooled-detrended conformal test (57% sensitivity; 22.4% false alarms)". Methods D6: "This variant was the most sensitive approach during development." Limitations: "the Artes data were used once during development to check false alarms".

*Problem:* `journal_selection/novelty_escalation_log.md` round 5 reports that "region-max detrended: sens 35.5%, FPR 20-22% -> INVALID (anti-conservative)" on the Artes data. The protocol was written after that, and it names D6 "Development variant that looked more sensitive". The final E2 run re-uses the same 30 Artes patients. So the 22.4% "finding" repeats a measurement made before pre-registration, on the same null data. It is not a held-out confirmation. The main text says D6 looked "most sensitive" and leaves out that it was already known to be invalid on this exact null. Supplementary Note S1 does disclose this, but readers of the abstract will not see it.

*Fix:* In Methods (D6 bullet), state that D6 had FPR 20–22% on the same Artes series during development. Then remove D6 from the abstract's evidence for the claim that "standard specificity estimates missed" the false alarms, or label it explicitly as a known-invalid positive control. A positive control is a legitimate and useful role for D6, but it must be called that.

### 4. MAJOR — Paired-difference CIs and McNemar tests ignore clustering, contrary to the Methods
*Location:* Methods: "Proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient … We compared each detector with D1 on the same eyes using the exact McNemar test".

*Problem:* `summarise.py` resamples eyes, not patients, for the paired difference CI: `diff[rng.integers(0, len(diff), len(diff))]`. The 52 reference eyes come from 41 patients, and GRAPE's 263 eyes come from 144 patients. Exact McNemar also assumes independent pairs. All CIs in Supplementary Table S2 and in the RQ2 and RQ5 text are therefore cluster-naive. Examples: "38 percentage points, 95% CI 19 to 58", "33 percentage points … (95% CI 28 to 39; adjusted p < 0.001)".

*Fix:* Use a patient-cluster bootstrap for the paired differences. Use a clustered McNemar test (e.g. Obuchowski 1998, or Durkalski et al. 2003), or a GEE/mixed logistic model with a patient random effect, for the tests.

### 5. MAJOR — Holm families are defined per k; the "any number of fields" claim needs correction across k, and the one "significant" result does not survive it
*Location:* Methods: "corrected p-values for the nine comparisons within each number of tests with the Holm method". Results: "The only significant gain in sensitivity was that of D6 with three fields (… Holm-adjusted p = 0.02)".

*Problem:* The claims are made across all four k values ("at any number of fields"), which is a family of 36 sensitivity comparisons, plus specificity and GRAPE endpoints. With Holm over 36 comparisons, D6's raw p = 0.00195 becomes 0.070. The paper also treats the two endpoints (sensitivity, specificity) and two datasets as separate families without justification.

*Fix:* Pre-specify the family. Either correct across k (and say that no comparison survives), or state clearly that only per-k conclusions are made and remove the cross-k statements.

### 6. MAJOR — Incorporation bias: the primary reference re-uses the detectors' input fields and is defined by the same statistic as D1/D2/D5
*Location:* Reference standard: "An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01." Limitations: "may favour detectors based on mean sensitivity".

*Problem:* The reference slope is fitted over all tests, including the first k that D1 sees. Reference eyes have a median of 11 tests, so at k = 6 more than half the reference data are D1's own input. D1 tests the same quantity, the OLS slope of mean sensitivity, and mean TD differs from mean sensitivity only by a fixed age term. This is partial verification and incorporation bias in D1's favour, and it biases the comparison toward the paper's conclusion that the trend test is a strong default. `code/experiments/leakage_audit.md` says this overlap is "stated as a limitation", but the manuscript's Limitations paragraph never mentions the overlap of the first k fields.

*Fix:* Define the reference on fields k+1 onward only (a "future-only" reference). With ≥ 8 tests this leaves at least 2–5 independent fields; use eyes with ≥ 10 if needed. Report the main tables under that reference. At minimum, state the overlap explicitly in Limitations.

### 7. MAJOR — The secondary reference is not an independent check, and the claim "the ranking was similar" is not supported
*Location:* Results: "With the secondary reference based on PoPLR over the whole series, sensitivity was lower for all detectors but the ranking was similar". Limitations: "the secondary PoPLR-based reference gave a similar ranking."

*Problem:* From `raw_results.csv.gz`, the 58 secondary-reference progressors are the 26 primary progressors plus 32 primary-indeterminate eyes. The secondary reference is a superset and shares all primary progressors. Only 17 secondary-stable eyes exist, and no specificity or paired tests are reported for it. The ranking does change. At k = 6 (sens_ref2): D6 43.1, D10 43.1, D8 42.1, D7 39.7, D1 37.9. Under the primary reference D1 is tied second (57.7). So two valid detectors, D10 (FPR 5.7%) and D7 (1.9%), rank above D1 under the secondary reference. The secondary reference is also PoPLR-based, which favours D4/D10 in the same way the primary favours D1. That circularity is not acknowledged.

*Fix:* Report specificity and paired McNemar tests under the secondary reference. Give rank correlations between the two references. Correct the "ranking was similar" sentence. Acknowledge that the PoPLR reference is circular for D4/D10.

### 8. MAJOR — Degenerate bootstrap CIs at 0% and 100%
*Location:* Table 3: "0 (0–0)", "100 (100–100)". Supplementary Table S1: specificity 100 (100–100) for nearly all detectors at k ≥ 4. Table 2 / S1: D4, D7, D10 FPR "0.0 (0.0–0.0)".

*Problem:* Percentile bootstrap intervals collapse at the boundary. A specificity of 26/26 has a Clopper–Pearson 95% CI of 86.8–100%, not 100–100. Reporting zero-width CIs overstates precision. They also feed into the validity rule, which uses the CI limits.

*Fix:* Use Clopper–Pearson or Wilson intervals with a design-effect adjustment, or a cluster-adjusted score interval, for proportions near 0 or 1. Report these in all tables.

### 9. MAJOR — Specificity against 26 stable eyes is uninformative, so the claim that specificity "did not reveal" the false alarms is overstated
*Location:* Abstract: "Reference-stable eyes did not reveal this: their specificity was 96% and 95%." Discussion: "the usual way to measure specificity … missed this."

*Problem:* At k ≥ 4, all paired specificity comparisons have zero or one discordant pair (Supplementary Table S2). Stable eyes are defined as one-sided p > 0.5, i.e. a non-negative full-series slope. That makes them a "super-stable", partly improving subset (median 9 tests versus 12 in progressors). The mechanism the Discussion offers ("Eyes that remain stable … tend to be eyes whose early fields also looked stable") is plausible but untested.

*Fix:* Test the mechanism. Report flag rates in the 80 indeterminate eyes and under a less selective stable definition (e.g. |slope| < 0.2 dB/yr). Give the CI on the specificity: D6 at k = 3 is 96% (87–100), which is compatible with an FPR of up to 13%. Moderate the wording.

### 10. MAJOR — RQ3/H3: the concordance analysis is weak, the pre-specified CI is missing, and "partly met" is spin
*Location:* Results RQ3: "Spearman ρ = 0.65, p < 0.001 … Hypothesis H3 was therefore partly met". Abstract: "The shuffle audit tracked the true false-alarm rate (Spearman ρ = 0.65; 80% of combinations within 3 percentage points)."

*Problem:*
- (a) H3 required both "most cells ≤ 3 points" and ρ ≥ 0.7. ρ = 0.65 means H3 was not met. "Partly met" is not a pre-specified outcome.
- (b) The protocol specified a bootstrap CI for ρ, and none is reported.
- (c) The 40 cells are not independent: they share detectors and overlapping windows.
- (d) Several cells are structural zeros (D4, D7, D10 at k = 3, where both rates are 0.0). These inflate "within 3 points" and make the Spearman p-value meaningless.
- (e) The audit's ability to classify validity is what matters clinically, and it is not reported. I applied a simple audit threshold of > 7.5%. That threshold flags 11 cells, of which 7 are truly invalid (PPV 64%). It misses D6 at k = 6 (true 7.6%, invalid; audit 4.9%). It gives false warnings for D2 at k = 3 (11.7% vs 2.6%), D7 at k = 5 and k = 6, and D8 at k = 6. The text claims "The audit identified every detector with a grossly inflated false-alarm rate", but "grossly" is defined after the fact.

*Fix:* State "H3 not met". Report the bootstrap CI for ρ, Lin's concordance coefficient or Bland–Altman limits, and a pre-specified audit decision rule with its sensitivity/PPV for detecting invalid cells. Exclude the structural-zero cells in a sensitivity analysis.

### 11. MODERATE — Inconsistent aggregation over seeds between tables and tests
*Location:* Methods: "we report the seed mean". `summarise.py`: paired tests use "majority over seeds" (`.mean().round()`).

*Problem:* Tables use seed means, but the differences in text use majority-vote flags, so the numbers disagree. Results: D8 at k = 6 "12 points" in the text (seed mean 70.8 − 57.7 = 13.1). GRAPE: "33 percentage points more non-progressing eyes" in the text, while Table 3 implies 95.3 − 61.2 = 34.1.

*Fix:* Use one aggregation throughout, or state both explicitly. Preferably, run the tests per seed and report the range of p-values.

### 12. MODERATE — The E2 effective sample size is 30 patients; the 10 donor draws add no information but give an impression of n = 3,000
*Location:* Table 2 footnote, and metrics `fpr_true_null_n = 3000`.

*Problem:* The overlapping windows and 10 time draws per window are pseudo-replicates. The patient bootstrap is the right approach, but 30 clusters is small for percentile bootstrap coverage. D8's FPR also varies widely by seed: 21.9–33.2% at k = 3, which is larger than its CI.

*Fix:* Report n as 30 patients in all tables. Consider BCa or a cluster-robust Wilson interval. Report per-seed FPR ranges for the stochastic detectors.

### 13. MODERATE — Small-sample instability visible in the development history is not discussed
*Location:* Discussion, generalisability.

*Problem:* `novelty_escalation_log.md` round 5 reports D1-equivalent ("OLS MD parametric") k = 3 sensitivity of 3.2% on the validation set (31 progressors). The test set gives 19.2%. Such a six-fold swing between two random patient splits shows how unstable the 26-eye estimates are.

*Fix:* Report validation-set results alongside the test set as a sensitivity analysis, or pool validation and test with cross-validation for the ML-free detectors.

### 14. MODERATE — The time to first detection is defined inconsistently with the protocol
*Location:* Methods, Real-world measures: "followed until six fields; eyes not flagged by six fields were counted as seven". Protocol: "number of tests to first detection among reference progressors (eyes followed to 8 tests)".

*Fix:* Align with the protocol or declare the deviation. Use a survival or restricted-mean approach rather than imputing 7 (D1 median 5, but 31% are censored).

### 15. MINOR — Spearman p-value on dependent cells
*Location:* "(Spearman ρ = 0.65, p < 0.001 …)".

*Fix:* Drop the p-value or replace it with the cluster bootstrap CI.

### 16. MINOR — "Significantly above 5% in 4 of 8 combinations" uses the CI lower bound as a test without stating so
*Location:* Results.

*Fix:* State that this is a one-sided 2.5%-level test per cell, with no multiplicity correction.

## Recommendation

**Major revision**, bordering on reject. The study could become a useful estimation paper. As written, its central inferential claims rest on an unfalsifiable primary hypothesis (H2), a validity rule chosen after the results that contradicts the protocol, cluster-naive paired inference, and a reference standard that overlaps with the detectors' inputs. Issues 1 and 2 must be resolved before the conclusions can be evaluated.
