# Review 08: Epidemiology and diagnostic accuracy (TRIPOD+AI / STARD)

**Reviewer role:** clinical epidemiologist reviewing the study as a diagnostic-accuracy and prediction-model evaluation.

## Summary

The core design problem is the extreme-phenotype reference standard. Stable eyes are defined by a full-series MTD slope with one-sided p > 0.5, which in practice means eyes whose field *improved* over about 13 years. This case-control-like sampling, plus requiring ≥8 tests, inflates specificity and makes the 26/26 comparison of limited use for the intended clinical setting. Two further problems: the reference series includes the index-test data (incorporation bias), and repeated looks inflate the cumulative false-alarm rate, which the paper reports only for sensitivity. Several core STARD 2015 and TRIPOD+AI items are missing.

## Issues

**1. MAJOR — Spectrum bias: the "stable" reference eyes are improving eyes.**
- Location: Methods: "An eye was stable if the one-sided p was above 0.5."
- Evidence: in `deferral.ols` the one-sided p is `t.cdf(b/se)`. So p > 0.5 if and only if the full-series slope b > 0. Every one of the 26 "stable" eyes had a positive MTD slope over a median 12.7 years.
- This explains the result "Specificity … was at least 91.5% for every detector": an eye whose mean sensitivity is rising is unlikely to be flagged by any decline rule.
- It also biases the ML thresholds (D8 and D9), which are set on 39 validation eyes defined the same way.
- Fix:
  - State in the Methods text that "stable" means a non-negative long-term slope.
  - Add a clinically realistic non-progressor definition. One option is a slope between −0.3 and +0.3 dB/yr with a narrow CI; another is "not progressor", including the 80 excluded eyes.
  - Report specificity under that definition.

**2. MAJOR — The two-gate design with 61% of eligible eyes excluded overstates accuracy and is not representative.**
- Location: "Of 132 test-set eyes with at least eight tests, 26 were progressors, 26 were stable and 80 were excluded."
- Evidence:
  - Only 132 of 869 test eyes (15%) had ≥8 tests. Of those, 80 (61%) were indeterminate and dropped.
  - Accuracy estimated only in the clear extremes is systematically higher than in consecutive eyes (STARD 2015 item 20, spectrum).
  - The 50% prevalence also means no predictive value can be inferred.
- Fix:
  - Report a participant-flow diagram (STARD item 19) with counts at each step.
  - Report a 2 × 2 table per detector for all 132 eyes, with indeterminate eyes shown separately (item 24).
  - Run a sensitivity analysis that treats indeterminate eyes as non-progressors.
  - Discuss PPV at realistic progression prevalence.

**3. MAJOR — Selection bias from requiring ≥8 tests.**
- Location: "For eyes with at least eight tests, we defined a future-confirmed reference".
- Evidence:
  - Eyes followed for 8–12 tests over 13 years were tested roughly once a year. They differ from eyes that progressed fast and were escalated, operated on, or lost to follow-up.
  - Rapid progressors, the eyes where early detection matters most, are probably under-represented.
  - Ages also differ: median 63.3 years for progressors against 54.0 for stable eyes (Table 1).
- Fix:
  - Compare the 132 included eyes with the 737 excluded test eyes (age, baseline MTD, test frequency).
  - Discuss the direction of bias.
  - Consider inverse-probability weighting for having ≥8 tests.

**4. MAJOR — Incorporation bias (partial overlap of index test and reference) is not disclosed in the paper.**
- Location: Reference standard section; Limitations.
- Evidence:
  - The reference slope uses all tests, including tests 1…k, which D1 also analyses with the same statistic, on raw sensitivity rather than TD.
  - At k = 6, against a median 12 tests (progressors) or 9 tests (stable), half or more of the reference data are the index data.
  - `leakage_audit.md` marks this "DISCLOSED … stated as a limitation", but the manuscript Limitations paragraph does not mention it.
- Fix:
  - Define the reference only on tests k+1 onward, for example tests 7–N with N ≥ 12, or as confirmation on later tests.
  - At minimum, report this analysis as a sensitivity check and state the limitation explicitly.

**5. MAJOR — Repeated looks: cumulative sensitivity is reported, but not cumulative false alarms.**
- Locations:
  - Results: "By the sixth test, D1 had flagged 69% of reference progressors."
  - Discussion: "the trend test flagged only about 69% … by the sixth test".
  - Methods: "false progression flags per 1,000 stable eyes at one review".
- Evidence:
  - The 69% (`descriptives.json`, `detected_by6_mean` = 0.692) is "flagged at k = 3, 4, 5 *or* 6". That is higher than the single-look 57.7% at k = 6.
  - The matching false-alarm figure is not reported. From `raw_results.csv` I computed the share of Artes windows (start i, draw d) flagged by D1 at any of k = 3–6: about **12.6%**. This is approximate because donor dates are re-drawn for each k.
  - So the clinically relevant "any flag over 4 reviews" false-alarm rate for D1 is about 2.5 times the nominal 5%.
- Fix:
  - Report cumulative false-alarm rates on Artes alongside cumulative sensitivity for every detector.
  - Rephrase the "per 1,000 stable eyes" metric as per review, and add the per-patient figure over a monitoring period.

**6. MODERATE — Clustering of eyes within patients is ignored in the paired analyses.**
- Location: "Confidence intervals for paired differences came from 2,000 bootstrap resamples of eyes."
- Evidence:
  - Progressors: 26 eyes from 23 patients. Stable: 26 eyes from 20 patients.
  - McNemar tests and the difference CIs treat eyes as independent (`summarise.py` lines 63–67).
  - The protocol said: "Unit of analysis = eye … with patient-cluster bootstrap".
- Fix: use a cluster bootstrap for the paired differences, or a clustered McNemar test (for example Obuchowski's or Durkalski's method), and state the patient counts in Table 2.

**7. MODERATE — The confidence-interval method fails at the boundaries and with few clusters.**
- Locations: Table 2, "0.0 (0.0–0.0)" and "100.0"; Table 3, "100.0 (100.0–100.0)".
- Evidence:
  - Percentile bootstrap CIs collapse to zero width at 0/26 or 26/26. The exact 95% upper bound for 0/26 is 13.2%.
  - E2 has only 30 patient clusters, and its 210–300 windows overlap heavily within each patient. Percentile cluster-bootstrap CIs with 30 clusters tend to under-cover.
- Fix: use Wilson or Clopper–Pearson intervals with a design-effect adjustment, or a BCa or studentised cluster bootstrap. Never report zero-width CIs.

**8. MODERATE — The true no-change arm has narrow spectrum and limited generalisability.**
- Location: "Thirty patients with glaucoma from Halifax, Canada, had 12 visual fields in 12 consecutive weeks".
- Evidence:
  - Median mean sensitivity is 26.9 dB (Table 1), which is early disease.
  - Test–retest variability rises steeply with damage, so false-alarm rates in moderate to advanced eyes are unknown. The authors note this in the third limitation.
  - The arm has 30 patients, one eye each, from a single centre with experienced patients.
  - One series spans 524 days, with first gaps of 116, 175 and 156 days (my check with `load_artes()`), so it was not 12 consecutive weeks.
- Fix:
  - Report false-alarm rates by baseline sensitivity tertile, at least D1 against the others.
  - Correct the description, and handle the long series with exclusion plus a sensitivity analysis.
  - Temper the claim that D1 is "valid at every number of tests" to "in early glaucoma".

**9. MODERATE — The external "clinician labels" are criterion labels with incorporation bias.**
- Locations:
  - Abstract: "agreement with clinician labels".
  - Results: "the clinicians' mean-deviation criterion".
  - Limitations: "its labels came from criteria applied to the full series".
- Evidence:
  - The GRAPE MD label is an algorithmic MD criterion applied to the full series. The median series has 4 visits, so at k = 3 the index data are three-quarters of the reference data.
  - D1 is essentially the same statistic, which favours D1 and D5.
  - The GRAPE cohort is also unusual for glaucoma (median age 41 years, `descriptives.json`) and uses a different perimeter.
- Fix:
  - Call them "criterion-based labels", not clinician labels.
  - Report all three GRAPE labels, as the protocol requires.
  - Interpret E4 as concordance with an MD-based rule, not accuracy.

**10. MODERATE — Reporting-guideline choice and missing items.**
- This is a comparative diagnostic-accuracy study of detection rules against a reference standard. STARD 2015 is the primary guideline, with TRIPOD+AI for the ML models (D8 and D9).
- Missing STARD items:
  - 3: intended use and clinical role. The setting is the routine review visit; this should be stated.
  - 5 and 9: eligibility and data-collection period of UWHVF.
  - 15: handling of indeterminate results.
  - 16: missing data and unreliable tests; there are no reliability indices.
  - 18: sample-size rationale.
  - 19: flow diagram with numbers.
  - 23: cross-tabulation.
  - 24: estimates for indeterminate results.
- Missing TRIPOD+AI items:
  - Model specification and hyperparameters selected.
  - Calibration of D8 and D9 (no calibration plot or intercept/slope).
  - Training sample size: 93 progressors and 99 stable eyes (my count).
  - Threshold sample: 39 validation stable eyes.
  - Fairness and subgroups (age, sex, severity).
  - Code availability.
- Fix: add a completed STARD 2015 checklist and a TRIPOD+AI checklist as supplements, and cite STARD.

**11. MODERATE — There is no sample-size or precision justification.**
- Location: Limitations: "The study could miss real differences of about 10–20 percentage points."
- Evidence:
  - With 26 paired eyes and Holm correction across 9 comparisons, the smallest significant gain is about 9 extra eyes with no reverse discordance: 34.6 pp (exact McNemar 9:0, p = 0.0039 < 0.05/9).
  - The real minimum detectable difference is therefore about 35 pp, not "10–20".
- Fix: report the minimum detectable difference or power for H2 explicitly, and correct the Limitations sentence.

**12. MINOR — The index test and reference use different scales and age adjustment.**
- Evidence: D1 uses raw mean sensitivity, which is not age-corrected. The reference uses mean TD, which is age-corrected. With progressors about 9 years older at baseline than stable eyes, age-related decline adds slightly to D1's apparent signal.
- Fix: state this, or run D1 on mean TD as a sensitivity analysis.

**13. MINOR — The shuffle audit is not a pure null.**
- Evidence: it uses all 869 test eyes, including real progressors, and includes the identity order in 1/k! of the draws (see Review 06, item 4). Real progressors inflate the variance of rate-based statistics after shuffling, which is the likely reason D2 and D7 have higher audit rates.
- Fix: exclude identity permutations. Report the audit separately in eyes without evidence of progression.
