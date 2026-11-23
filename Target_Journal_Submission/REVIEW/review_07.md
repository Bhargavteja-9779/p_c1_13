# Review 07 — Reference-standard / circularity skeptic

## Summary
Every sensitivity and specificity in E1 depends on a reference built from the slope of mean total deviation over the full series. That series includes the first k tests the detectors see. The reference is then compared with a detector (D1) that is a one-sided t-test of the slope of mean sensitivity on those same first tests. The "stable" class consists only of eyes whose full-series slope is positive. The external labels (GRAPE "MD" criterion) are again MD-based. When I re-analysed the unreported PLR labels in GRAPE, D1's apparent advantage largely disappeared. The headline that the MD trend is "hard to beat" may therefore partly reflect the reference definition rather than the detectors.

**Recommendation: Major revision.**

## Issues

1. **FATAL (as currently interpreted) — Incorporation bias and shared measurement between the reference and D1 (Methods "Reference Standard"; Results RQ2; Discussion para 1).**
   - The progressor label requires a full-series MD slope < −0.3 dB/yr with p < 0.01, and that series *includes* tests 1..k.
   - D1 flags when the slope of mean sensitivity over tests 1..k has p < 0.05. Mean sensitivity and unweighted mean TD differ only by age-normal values, so their slopes differ by an approximately constant age term.
   - The first k tests therefore enter both the index test and the reference with the same summary statistic. Eyes with an early MD drop are more likely to be reference positive *and* D1 positive.
   - The repository's own leakage audit (`experiments/leakage_audit.md`, "Reference overlap") says this is "stated as a limitation". It is not stated in the manuscript's Limitations. The third limitation mentions only that the reference "may favour detectors based on mean sensitivity".

   *Fix:* (a) define the reference on tests k+1..end only (a "future-only" reference), or at minimum on tests ≥ 4..end; (b) disclose the overlap in Limitations; (c) report how much the D1-vs-others comparisons change.

2. **MAJOR — The "stable" class is "improving" (Methods: "stable if the one-sided p was above 0.5").** One-sided p > 0.5 means a positive slope estimate. I re-ran the reference on all UWHVF eyes with ≥ 8 tests: 164/164 stable eyes had slopes > 0 (median +0.10 dB/yr). Specificity measured on improving eyes is close to 100% by construction. Table 1 shows 100% for most detectors at k ≥ 4. The section heading "Specificity on Reference-Stable Eyes Hid These False Alarms" is then almost a tautology: any eye selected for improvement will rarely be flagged. *Fix:* state the definition plainly. Add a stable class of "|slope| < 0.2 dB/yr with p > 0.1" or similar. Report the specificity of every detector in the 80 indeterminate eyes, stratified by slope.

3. **MAJOR — 61% of eligible eyes are excluded as "indeterminate" (Results "Study Data": 80 of 132).** This is extreme-group (spectrum) selection. Sensitivity and specificity in the clear extremes overstate performance relative to the clinical population. More importantly, the selection changes the relative ranking of detectors that use different signals (PLR, events, ML). *Fix:* report performance as a function of the full-series slope (e.g., flag rate vs slope decile) for all 132 eyes, or use a three-level reference.

4. **MAJOR — The secondary reference is not independent of the primary (Results "The secondary, PoPLR-based reference gave the same ranking"; Table S2).**
   - From `raw_results.csv.gz`: all 26 primary progressors are among the 58 secondary progressors. The other 32 are primary-indeterminate eyes. All 17 secondary-stable eyes are primary-stable.
   - Secondary-reference specificity is not reported at all.
   - The ranking is *not* the same. At k = 6, D1 (37.9%) ranks behind D6 (43.1%), D10 (43.1%), D8 (42.1%) and D7 (39.7%) on the secondary reference. On the primary reference, D1 (57.7%) is tied with D7 and behind only D8.
   - The PoPLR reference is in turn circular with D4 and D10.

   *Fix:* correct the "same ranking" sentence. Report secondary specificity (n = 17) and paired tests. Add a reference that is not built from the same trend statistics, e.g., a GPA-like event reference on future tests, or agreement among several criteria.

5. **MAJOR — GRAPE "clinician labels" are MD-criterion labels, and the pre-registered PLR labels were not reported (Methods "GRAPE"; Results RQ5; Table 2).**
   - The protocol lists PLR2, PLR3 and "any" as secondary GRAPE labels. None appears in the paper, although `raw_results.csv.gz` stores them.
   - I computed seed-averaged flag rates from the raw file. These are the reviewer's own computation without CIs, and the authors should verify them.
   - Against PLR2 (40 progressors) at 3 tests: D1 sensitivity 17.5% (false positives in non-progressors 7.2%); D2 45.0% (21.5%); D8 61.0% (38.1%).
   - Against PLR3 (14 progressors): D1 21.4%, D2 57.1%, D3 28.6%. At 4 tests: D3, D4 and D7 at 33.3% each vs D1 16.7%.
   - So D1's GRAPE sensitivity of 44.4% under the MD label falls to 17.5–21% under non-MD labels. That is what MD-on-MD circularity predicts.
   - "Clinician-labelled" also appears to overstate how the labels were made. The manuscript itself says the labels were "assigned with three criteria". I could not verify from the GRAPE paper whether clinicians adjudicated them.

   *Fix:* report all pre-registered GRAPE labels with CIs and tests. Call them "criterion-based labels". Discuss the circularity explicitly.

6. **MODERATE — The GRAPE labels also use the full follow-up (incorporation), and GRAPE "false positives" are not false alarms (Results RQ5; Abstract "more false positives").** A non-progressor by the MD criterion can be a PLR progressor. Calling D2's and D8's extra flags "false positives" therefore assumes the MD criterion is truth. *Fix:* use "flags in MD-label non-progressors" and show the cross-tabulation with the PLR labels.

7. **MODERATE — The reference thresholds are arbitrary and not justified (Methods: −0.3 dB/yr, p < 0.01, p > 0.5).** *Fix:* cite a source for these cut-offs or give a rationale. Show sensitivity to −0.5 and −1.0 dB/yr thresholds.

8. **MINOR — "Future-confirmed" is a misnomer.** The reference is not future-only (see issue 1). *Fix:* use "whole-series reference" until issue 1 is fixed.
