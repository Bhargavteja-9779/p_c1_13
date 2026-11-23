# Review 09: Reporting (TRIPOD+AI) and research-integrity reviewer

## Summary
I compared claims with evidence, the protocol with the manuscript, and the repository history with the disclosures. The authors deserve credit: they keep a development log, disclose the round-5 use of Artes, and list a deviation in S2. Even so, there are:

- undisclosed or under-disclosed deviations;
- statements in the leakage audit that the manuscript does not honour;
- several over-claims in the Abstract and Key Summary Points;
- an incomplete TRIPOD+AI report.

## Recommendation
**Major revision.**

## Issues

1. **FATAL – A result-relevant protocol deviation is reported only in the Supplement, and its timing is not independently verifiable.**
   - *Location:* Methods, Statistical analysis; S2; git history.
   - *Problem:* The validity rule changed from "upper bound vs 5%" (protocol, commit c0dedb5, 09:05) to "lower ≤ 5% and upper ≤ 10%" (draft, commit bd2c2e2, 09:14). In between, a quick run that evaluated Artes and GRAPE was committed (60ba7b2, 09:08; `run_meta_quick.json`). The S2 statement that the rule was set "before the final results" is true, but it omits that preliminary Artes/GRAPE outputs existed. The new rule rescues the comparator: D1 fails the protocol rule at every k.
   - *Fix:*
     - Move the deviation into the main Methods and into the Abstract's Results.
     - Make the protocol rule primary.
     - Disclose the quick run and deposit its output.

2. **MAJOR – The leakage audit claims a limitation that the manuscript does not state.**
   - *Location:* `leakage_audit.md` ("Reference overlap … stated as a limitation"); manuscript Limitations.
   - *Problem:* The Limitations do not mention that the reference uses the same first k tests (incorporation bias). The same applies to GRAPE, where many eyes have only 3–4 visits.
   - *Fix:* Add this limitation explicitly.

3. **MAJOR – Other undisclosed deviations from the protocol.**
   - *Location:* S2 ("No other deviations").
   - *Problem:* I found the following:
     - (a) H2's 10-percentage-point margin is not used; the manuscript says "substantially".
     - (b) Paired-difference CIs are eye-level, not patient-cluster bootstrap as the protocol requires (`summarise.py`).
     - (c) GRAPE D5 calibration is 5-fold, not leave-one-patient-out (D5 protocol text). A2 changes this, but S2 does not list it as a change to the D5 specification.
     - (d) The D8 features differ from the protocol list (no PoPLR S, no regional slope).
     - (e) Secondary GRAPE labels (PLR2, PLR3, any) are pre-specified but not reported.
     - (f) Specificity under the secondary reference is not reported.
     - (g) "All seeds reported (mean ± SD)" is met only for sensitivity and false alarms.
   - *Fix:* List all of these in S2, and report the missing pre-specified analyses.

4. **MAJOR – The Abstract and Key Summary Points overclaim.**
   - *Location and problems:*
     - Abstract Conclusion: "apparent gains in early progression detection were explained by false alarms that standard specificity estimates missed". This generalises from one in-house detector whose failure was known before the analysis plan.
     - Abstract: "A shuffle audit … tracked true false-alarm rates (ρ = 0.65)". It omits that the pre-specified target (ρ ≥ 0.7) failed.
     - Key point 2: "a shuffle audit … identified the invalid detectors". The audit missed D6 at 6 tests (4.9% vs 7.6%) and flagged valid detectors (D2 k = 3; D7 k = 5, 6; D8 k = 6).
     - Discussion: "A shuffle audit did [reveal the problem]" and "gave the best balance … in both clinics". The latter is not tested.
     - Discussion: "In our data that practice gave false-alarm rates several times higher than intended". True for D8 at k = 3 and 5 only. D8 at k = 6 is 3.6%, and D9 at k = 4 is 2.0%.
   - *Fix:* Rewrite each sentence to match the evidence.

5. **MAJOR – "Pre-registered" and "time-stamped" overstate independence.**
   - *Location:* Methods ("written down and time-stamped before the final test data were analysed"); Data Availability ("the pre-registered protocol").
   - *Problem:* The plan is a commit in the authors' own repository. Commit timestamps are author-controlled. The plan was written 28 minutes before the full results.
   - *Fix:* Describe it as a "version-controlled analysis plan (commit c0dedb5)". Do not call it pre-registered unless it was deposited in a public registry.

6. **MAJOR – Development history and the D6 selection need main-text disclosure.**
   - *Location:* Methods D6 ("This variant was the most sensitive approach during development"); S1.
   - *Problem:* The Methods should say, at the point where D6 is defined, that D6 was already known to be anti-conservative on the Artes data at k = 3 (Round 5: 20–22%). Otherwise the reader takes the RQ1/RQ2 result for D6 as new. The project's own log also records a selection process across six failed ideas and two disease areas ("Honest label expected: NOT REMARKABLE"). A sentence on this researcher-degrees-of-freedom history belongs in the Limitations, not only in S1.
   - *Fix:* Disclose both points in the main text.

7. **MAJOR – Authorship, accountability and AI use.**
   - *Location:* Title page; Declarations ("An AI assistant (Claude, Anthropic) was used for code, analysis and drafting under author supervision").
   - *Problem:*
     - Authors are placeholders, so no named person currently takes responsibility for the analysis.
     - Under Springer Nature policy, use of an LLM for analysis and drafting must be described in the Methods, and the authors must be able to vouch for every result.
     - The repository history shows the protocol, code, full run and manuscript were all produced on one day. Human verification of the data handling should be documented.
   - *Fix:*
     - Name accountable authors.
     - Describe the AI's role in the Methods.
     - State which analyses a named author independently re-ran or checked.

8. **MODERATE – The TRIPOD+AI checklist is missing and several items are absent.**
   - *Location:* Methods, Study design ("We followed the TRIPOD+AI reporting guidance where it applies").
   - *Problem:* There is no checklist. Missing items include:
     - sample-size rationale;
     - participant flow diagram (7,428 eyes → 1,489 test eyes → 869 with ≥3 tests → 132 with ≥8 → 52 reference);
     - handling of missing points (GRAPE −1 codes, per-eye removal);
     - full model specification and hyperparameters chosen;
     - ML calibration;
     - fairness and subgroup reporting (age, sex, severity);
     - demographics of the Artes and GRAPE cohorts.
   - *Fix:* Add a completed TRIPOD+AI checklist and a descriptive table. Consider STARD 2015 for the accuracy parts.

9. **MODERATE – Citation accuracy.**
   - *Location:* References.
   - *Problems:*
     - [28] Freedman & Lane is cited for a claim it does not make (fragility with 1 df).
     - [25] UWHVF: the DOI ends `tvst.11.1.1` but the citation says "11(1):2". These are inconsistent.
     - [22] Si et al.: the reference list says 2025, while the novelty map records the 2026 MICCAI LNCS volume.
     - [21] Chen et al.: a medRxiv preprint dated November 2026 with DOI prefix 10.64898, which differs from the long-standing medRxiv prefix 10.1101.
     - [15, 16, 23] are cited for "usually set the threshold at a fixed specificity in reference-stable eyes" without evidence that they did.
   - *Fix:* Re-verify [21, 22, 25] against Crossref, and mark any item that cannot be verified as UNVERIFIED. Replace or remove the [28] attribution. Support or remove the [15, 16, 23] claim.

10. **MINOR – Licensing statement.**
    - *Location:* Ethics; Data Availability.
    - *Problem:* The `visualFields` data are distributed under GPL-3 (`artes_retest.py` docstring). "Open licences" is fine, but name it.
    - *Fix:* State the licence for each data set.

11. **MINOR – Journal format.**
    - *Location:* Declarations.
    - *Problem:* The headings "Conflict of Interest" and "Ethical Approval" should be "Disclosures" and "Compliance with Ethics Guidelines". The ethics text is duplicated verbatim in the Methods and the Declarations.
    - *Fix:* Rename the headings and remove the duplicate.

12. **MINOR – Figures do not match the text, and labels overlap.**
    - *Location:* Figs. 1–4.
    - *Problems:*
      - Fig. 2: the shaded "valid" zone is drawn at ≤5%, while validity in the text uses an upper limit ≤10%. D1 at 6 tests (5.1%) and D6 at 4 tests (5.1%, "valid") both sit outside the shaded zone. The legend sentence "Detectors to the right of the shaded area gain sensitivity by raising false alarms" therefore indicts D1.
      - Labels overlap in several places: Fig. 2 (D1/D5; D4/D7/D10 at the origin) and Fig. 4 (D4/D7).
      - The x-axis scales differ across the Fig. 2 panels.
      - Fig. 1: the arrow from Artes points into the detector-development box, which implies Artes was used to build the detectors. The E3/E4 box text overflows.
    - *Fix:* Align the shaded zone with the validity rule (or show both thresholds), de-overlap the labels, use a common x-axis, and redraw Fig. 1 so Artes feeds only E2.

13. **MINOR – Textual errors.**
    - *Problems:*
      - "kept false alarms close to the nominal 5%" for D2 and D3, which are at 0.2–2.6%.
      - "was therefore not met, In a post hoc look": a typo.
      - D9 at 5 tests is invalid (7.5% [2.8–13.3]) but is omitted from the RQ1 paragraph.
      - "D5 flagged exactly the same reference eyes" holds only for the seed-majority flags.
    - *Fix:* Correct each of these.
