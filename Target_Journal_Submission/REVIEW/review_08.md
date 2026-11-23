# Review 08 — External-validity reviewer (GRAPE; Artes time-label amendment)

## Summary
The paper claims external support from GRAPE (263 eyes, Hangzhou) and validity judgments from the Artes retest data, after amendment A1 re-labels its time axis. Both pieces are weaker than the text suggests:

- GRAPE has no true-null arm, so "valid" has no meaning there.
- Only 27 (k = 3) and 18 (k = 4) progressors are available.
- Three of the most interesting detectors (D6, D9, D10) were not run on GRAPE.
- The ML model was transferred across perimeters without recalibration.
- The pre-registered secondary labels were not reported.

For Artes, borrowing time labels makes rate rules look valid in a way that may not carry over to clinics.

**Recommendation: Major revision.**

## Issues

1. **MAJOR — "In Seattle or in an external clinic in China" (Key Summary Points, bullet 4; Abstract Results last sentence; Discussion para 1 "in two clinics").** In GRAPE, validity is undefined because there is no no-change data for that perimeter. The GRAPE result shows that D2 and D8 flag more MD-label non-progressors. It does not show that "no valid detector beat D1". *Fix:* reword. Something like: "In GRAPE, detectors that flagged more MD-label progressors than D1 also flagged significantly more MD-label non-progressors". Drop "valid" from GRAPE statements.

2. **MAJOR — The pre-registered secondary GRAPE labels are not reported, and they change the picture (Protocol "Data": "primary: MD label; secondary: PLR2, PLR3, any").**
   - My computation from `raw_results.csv.gz` (seed-averaged, no CIs; authors to verify): at 3 tests against PLR2 (40 progressors), D1 detects 17.5%, D2 45.0% and D8 61.0%.
   - Against PLR3 at 4 tests (12 progressors), D3, D4 and D7 each reach 33.3% vs 16.7% for D1.
   - These are unreported pre-specified outcomes.

   *Fix:* add them (main text or Supplement), with tests vs D1. State in the Results that conclusions depend on the label.

3. **MAJOR — Amendment A1 (borrowing UWHVF dates for Artes windows) has consequences that are not examined (Methods E2; Limitations "Second").**
   - (a) Donors are drawn from *all* UWHVF test eyes with ≥ k tests (`donors = {k: [s['t'][:k] for s in test ...]}`), not from the reference cohort. Their spacing differs from that of the reference eyes (see review 05).
   - (b) Short-term (weekly) noise is placed on a multi-year time axis, so slope-magnitude rules (D2, D3) see very small slopes. D2's 2.6% at k = 3 contrasts with an 11.7% shuffle-audit rate and with the 16.5-pp excess of flags in GRAPE.
   - (c) A1 was written after a "quick" run that had already processed the Artes and GRAPE data (see issue 5).

   *Fix:* report results under the unmodified weekly spacing (in an appendix) and under donor spacing drawn from reference-stable eyes. Report a variance-inflated sensitivity analysis. Discuss the clinic-noise gap explicitly as a threat to the "valid" verdict for D2, D3 and D7.

4. **MAJOR — GRAPE coverage and power (Results RQ5; Table 2).**
   - D6, D9 and D10 are not evaluated: D6 is the headline detector, and D9/D10 are ML/self-supervised.
   - With 27/18 progressors, the sensitivity CIs span 30–40 points.
   - The conclusion "the pattern was the same" rests on false-positive differences, not on sensitivity.

   *Fix:* implement a grid-agnostic D6 (the code already has a quarter-split fallback in `make_regions`). Run it with GRAPE-internal cross-fitting. Present the GRAPE sensitivity results as exploratory.

5. **MAJOR — The GRAPE data were processed before amendment A2 was written (`run_all.py` quick mode; commit 60ba7b2).** Quick mode evaluates E2 (Artes) and E4 (GRAPE, with labels) at k = 4. `results/run_meta_quick.json` (n_grape = 263, n_artes = 30) was committed together with amendments A1 and A2. The Methods state that "GRAPE [was] not used before the final run". The quick output file (`raw_results_quick.csv`) is not in the repository, so it cannot be checked whether its results were inspected. *Fix:* disclose that the quick run touched GRAPE and Artes. State what output was produced and whether anyone viewed it. Provide the file if it exists.

6. **MODERATE — GRAPE time axis and intervals.** GRAPE follow-up spans 0–4.8 years (column 3 of the follow-up sheet; median visit time 1.1 years). With 3 visits over about 1 year, a −1 dB/yr rule (D2) is very noisy. *Fix:* report the GRAPE inter-visit intervals in Results "Study Data". Discuss how rate rules depend on spacing.

7. **MODERATE — Generalisability of the UWHVF reference cohort.** The reference eyes are those with ≥ 8 tests over a median of 12.9 years, a highly selected long-follow-up population. *Fix:* compare the baseline characteristics of reference vs non-reference test eyes.

8. **MODERATE — The GRAPE baseline visit may be excluded.** The loader reads only the "Follow-up" sheet. It is unclear whether "visit 1" there is the baseline examination used in the GRAPE labels. *Fix:* clarify and confirm with the data descriptor [29].

9. **MINOR — Ethnic and device generalisability.** The paper covers one US academic centre, one Canadian research cohort and one Chinese centre, and no commercial GPA. *Fix:* temper "in two clinics" to "in one development clinic and one external data set".
