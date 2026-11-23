# Review 02 — Biostatistician

**Recommendation:** Reject in current form; could be reconsidered after a fundamental re-analysis.

## Summary

The central inferential claim is that no "valid" detector is significantly more sensitive than D1. It rests on three things: a validity rule that was written after the results were available and differs from the protocol, a McNemar/Holm test in 26 progressors that cannot reach significance for any difference below about 35 percentage points, and a "pre-specified" foil (D6) whose invalidity was already known from development on the same no-change data. On top of that, the point estimates (seed means) and the paired tests (seed majority vote) refer to different quantities, and several validity classifications depend on bootstrap Monte Carlo noise. I checked every number in the text against `results/metrics.json`, `results/statistics.json` and `results/descriptives.json`. Most numbers transcribe correctly; the problems are in inference and interpretation.

## Issues

### 1. FATAL — The validity rule is post hoc and differs from the protocol; under the protocol rule the comparator D1 is invalid at every k
**Location:** Methods: "A detector was considered valid at a given k if, on true no-change data, the lower limit of its false-alarm confidence interval was at or below 5% (no evidence of excess false alarms) and the upper limit did not exceed 10%." Methods: "Two amendments were made before any final result was seen; both are reported below."
**Evidence:**
- `code/experiments/protocol.md` (Statistics) says: "Validity: FPR CI upper bound vs 5%." There is no lower-limit criterion and no 10% margin, and neither amendment (A1, A2) changes this.
- The rule used in the paper appears only in `manuscript/fill_values.py` (`valid()`: `fpr_true_null_lo <= 0.05 and fpr_true_null_hi <= 0.10`). It was committed in fbd3f75 (2026-11-23 10:22), about 50 minutes after the full results were committed (94777b8, 09:33).
- Under the protocol rule (upper CI ≤ 5%), D1 fails at every k: upper limits are 6.3%, 6.2%, 7.5% and 8.1% (`metrics.json`). D5 fails at every k too (5.6, 5.9, 7.1, 7.9). The only "valid" detectors would be D2, D3, D4, D7 and D10 at k = 3; D2, D3, D4, D7 and D9 at k = 4; and D2, D3 and D7 at k = 5–6.

The headline sentences "It was valid at every number of tests" (D1), "No detector with a valid false-alarm rate was significantly more sensitive than the trend test", and the whole classification in Table 2 therefore depend on an undisclosed, result-dependent change of the primary validity criterion. This is the kind of deviation that the protocol's own sentence ("any deviation will be reported") forbids.
**Fix:** Report the deviation openly as a third, post hoc amendment with its timing and reason (the protocol rule is unattainable even for an exactly nominal test). Present results under both rules. If a margin-based rule is kept, justify the 10% margin clinically and treat it as post hoc. Rewrite "valid" claims accordingly, and remove "Two amendments were made" unless it becomes "three".

### 2. MAJOR — Hypothesis H2 cannot be falsified with 26 progressors and Holm correction; "supports our main hypothesis" is an absence-of-evidence fallacy
**Location:** "This result supports our main hypothesis." "The hypothesis that no valid detector would beat D1 by 10 percentage points or more with a significant McNemar test was therefore not rejected at any number of tests." Limitations: "The study could miss real differences of about 10–20 percentage points."
**Evidence:** In the best case for the challenger (all discordant pairs in its favour, c = 0), the exact McNemar p is 2·0.5^b. For Holm with 9 comparisons, the smallest p must satisfy p·9 < 0.05, so p < 0.0056, which requires b ≥ 9 discordant eyes, i.e. a sensitivity difference of at least 9/26 = 34.6 percentage points. Even without multiplicity correction, b ≥ 6 (≥ 23 pp) is needed. This matches `statistics.json`: the only significant gain (D6, k = 3) had b = 10, c = 0. A 10 pp margin (H2) was therefore untestable by design. Two valid detectors had point estimates above the 10 pp margin (D2 at k = 3: +19.2 pp, 95% CI 0.0 to 42.3; D8 at k = 6: +11.5 pp, CI −7.7 to 30.8), so the data are entirely compatible with H2 being false. The limitation's "about 10–20 percentage points" understates the problem by a factor of 2–3.
**Fix:** Add a formal power or minimum-detectable-difference statement (≈35 pp under Holm). Reframe H2 as an estimation question (paired differences with CIs), or as a non-inferiority/equivalence analysis with a pre-specified margin that is reported as unachievable. Delete "supports our main hypothesis" and "remained as good as". Report the 80 excluded reference eyes and consider a larger reference set, for example by using eyes with ≥ 7 tests or by pooling validation and test after model freezing for the non-trained detectors.

### 3. MAJOR — D6 was known to be invalid on the same Artes data before the protocol was written; the "only significant gain is invalid" result was predictable
**Location:** "D6 pooled-detrended conformal regional test: ... This variant was the most sensitive approach during development." Limitations: "Sixth, the Artes data were used once during development, to check false alarms of a candidate method; this is disclosed in the Supplementary Material."
**Evidence:** `results/d6_round5.json`, key `region|detrended|lvl` at k = 3, gives Artes FPR 0.203 and shuffle FPR 0.215. The Supplementary Material (Round 5) states: "region-max detrended: sens 35.5%, FPR 20-22% -> INVALID (anti-conservative)" and "The earlier 'valid from the 3rd test' gain was a false-alarm artefact of detrending with 1 residual df." The protocol then lists D6 as "development variant that looked more sensitive". The main text describes Artes use as checking "a candidate method" and does not say that the result was "D6 is invalid at k = 3".
**Fix:** State in the Methods that D6 was included **because** it had already been shown to be anti-conservative on the Artes data (as a positive control for the true no-change arm), and remove D6 from any confirmatory claim. Treat the D6 contrast as a demonstration, not a finding. The abstract sentence "The only detector significantly more sensitive than the trend test ... had a false-alarm rate of 22.4%" should be qualified accordingly.

### 4. MAJOR — "Excess false alarms supported" is claimed where the CI includes 5%
**Location:** "By our validity rule, the hypothesis that these detectors exceed the nominal 5% was supported for D8 at three to five tests and for D9 at three, five and six tests."
**Evidence:** For D9, the k = 5 CI is 2.8–13.3% and the k = 6 CI is 2.3–10.0%. Both lower limits are below 5%, so there is no evidence that these detectors exceed 5%. They fail the rule only because their CIs are wide, partly because of seed variance (seed SD 4.1 and 4.2 pp). Being "not valid" under a two-sided-margin rule is not the same as "exceeds 5%". This sentence misstates H4.
**Fix:** Say: "H4 was supported (lower CI > 5%) for D8 at k = 3–5 and D9 at k = 3. For D9 at k = 5–6, the false-alarm rate was too imprecise to establish validity."

### 5. MAJOR — D9 at k = 6 is classified by bootstrap Monte Carlo noise, and the table contradicts itself
**Location:** "D9 had 5.9% (95% CI 2.3–10.0%), so both were again not valid; D9 only just exceeded the 10% upper limit." Table 2 row "D9 GRU | 6 | ... | 5.9 (2.3–10.0) | 8.6 | **no**".
**Evidence:** `fpr_true_null_hi = 0.100002381`, which exceeds 10% by 0.0002 pp. A percentile bootstrap with 2,000 resamples has Monte Carlo error of several tenths of a percentage point at the 97.5th percentile. A reader sees "10.0" and the rule "did not exceed 10%" and concludes the label "no" is an error.
**Fix:** Flag any classification within Monte Carlo error as indeterminate. Increase B (e.g., 20,000) for the validity CIs. Print two decimals in the table where a classification depends on it.

### 6. MAJOR — Point estimates (seed means) and paired tests (seed majority vote) estimate different detectors
**Location:** "we report the mean over seeds"; "For stochastic detectors, the paired tests used each eye's majority flag across seeds."
**Evidence:** The reported paired differences do not equal the differences between the reported point estimates:
- D6 at k = 3: 56.9 − 19.2 = 37.7, but the text gives "+38.5 percentage points".
- D8 at k = 6: 70.8 − 57.7 = 13.1, but the text gives "+11.5".
- GRAPE D8 at k = 3: 65.9 − 44.4 = 21.5, but the text gives "+25.9".
- GRAPE false positives at k = 3: 95.3 − 61.2 = 34.1, but the text gives "+33.5".

A 5-seed majority vote is a different detector (an ensemble) from any single seed, and it is not the one a clinic would deploy. The protocol does not mention majority voting ("All seeds reported (mean ± SD)").
**Fix:** Pick one estimand. Preferred: run the paired test per seed and report the distribution of p-values (or combine them), with the seed-mean difference as the effect. Alternatively, report everything, including Table 2, for the majority-vote ensemble. Disclose this as a deviation from the protocol.

### 7. MODERATE — The bootstrap unit is inconsistent between proportions and paired differences
**Location:** "Proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient". "Confidence intervals for paired differences came from 2,000 bootstrap resamples of eyes."
**Evidence:** In `summarise.py`, paired differences resample eyes (`diff[rng.integers(0, len(diff), len(diff))]`). The 26 progressors come from 23 patients and the 26 stable eyes from 20. The protocol says "paired bootstrap", with patient as the cluster for E1.
**Fix:** Use patient-cluster resampling for the paired differences as well.

### 8. MODERATE — The Holm family includes comparisons that are degenerate by construction
**Location:** "corrected p-values for the nine comparisons within each number of tests and endpoint with the Holm method".
**Evidence:** At k = 3, D4, D7 and D10 cannot flag any eye by construction (as the paper itself states), yet they occupy 3 of the 9 Holm slots. The family also mixes valid and invalid detectors, even though H2 concerns only valid ones. For GRAPE there are 6 comparisons, not nine, so the sentence is inaccurate for E4. There is no adjustment across k, although H2 is stated "at any number of tests".
**Fix:** Define the confirmatory family as valid detectors only (pre-specified per k), or justify the chosen family. Correct the count for E4. Discuss multiplicity across k.

### 9. MODERATE — The shuffle-audit concordance is reported selectively, and H3 failed
**Location:** Abstract: "The shuffle audit agreed with true false alarms within 3 percentage points in 80% of detector–test-number cells (Spearman ρ = 0.65)." Results: "The largest difference was 10.4 percentage points."
**Evidence:** `statistics.json` gives rho 0.648 and max |diff| 0.1039, so the numbers are correct. However:
- (a) The pre-specified H3 (ρ ≥ 0.70) failed, and the abstract does not say so.
- (b) Three of the 40 cells are structural zeros (D4, D7 and D10 at k = 3 cannot flag), which inflates both the "within 3 pp" share and the rank agreement.
- (c) The largest discrepancy (10.4 pp) is D8 at k = 3, where the audit **underestimates** (17.3 vs 27.7). The Results mention only the overestimates for D2/D7 and the D9 underestimate.
- (d) The protocol asked for a bootstrap CI for ρ; none is reported.
- (e) The 40 cells are not independent (10 detectors × 4 correlated k).

**Fix:** State in the abstract that H3 was not met. Exclude the structural-zero cells, or report results with and without them. Report a cluster bootstrap CI for ρ (resampling detectors). Name D8 at k = 3 as the largest discrepancy.

### 10. MODERATE — "Seed SD" mixes algorithmic randomness with randomness in the donor-date draws
**Location:** "Stochastic detectors (D4–D6, D8–D10) were run with five seeds"; "D4 PoPLR: ... using all possible orders of the k tests."
**Evidence:** For k ≤ 7, D4 uses exact enumeration (`pvalue_within`) and is deterministic. Its non-zero seed SD (0.2 pp) arises because the Artes donor time stamps are drawn with `rng = default_rng(1000 + seed)`. Deterministic detectors (D1–D3, D7) are evaluated on a single donor draw set (seed 0), whereas stochastic detectors are evaluated on five. Comparisons on E2 therefore use different null samples.
**Fix:** Fix the donor draws independently of the detector seed, so that all detectors see identical E2 windows. Call D4 deterministic. Report the donor-draw variance separately.

### 11. MODERATE — Equivalence language is used without equivalence testing
**Location:** "The pooled-shuffle conformal test (D5) had exactly the same sensitivity as D1 at three to five tests"; "remained as good as any valid alternative"; "was as good as any detector".
**Problem:** Identical point estimates in 26 eyes are a fact about the data. "As good as" is an inferential claim, and it needs an equivalence margin and CI.
**Fix:** Use descriptive language ("not significantly different; 95% CI for the difference ...").

### 12. MINOR — The validity-rule description in the abstract contradicts the Methods
**Location:** Abstract: "while keeping false alarms at the nominal 5%".
**Problem:** The rule actually used tolerates an upper CI limit up to 10%, and D6 at k = 4 (5.1%) and D1 at k = 6 (5.1%) are "valid".
**Fix:** Describe the rule as actually applied.

### 13. MINOR — Secondary-reference results lack denominators and specificity
**Location:** "Against the secondary PoPLR reference, D1 detected 10.3% of progressors at three tests and 37.9% at six tests (58 progressors)."
**Fix:** Report the number of PoPLR-stable eyes, specificity, CIs and paired tests for the secondary reference. Note the circularity with D4 and D10, which are PoPLR-type statistics.

### 14. MINOR — The numbers I checked all transcribe correctly; no transcription mismatches were found
For the record, every Table 2/Table 3 value, the abstract numbers (19.2, 4.4, 56.9, 22.4, 27.7, 18.8, ρ = 0.65, 80%, 61.2, 95.3), the Holm-adjusted p-values (0.02, 0.72, 1.00, 0.04, 0.28, < 0.001), the Table 1 descriptives and the 69%/78%/77% time-to-detection figures match the JSON files after rounding. The problems above concern inference, not transcription, apart from the seed-mean/majority mismatch in Issue 6.
