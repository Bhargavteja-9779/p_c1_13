# Risk report and final decision (2026-11-23)

## Final decision

**READY FOR SUBMISSION — after the authors fill in the author-only fields** (names, affiliations, ORCID iDs,
corresponding address, CRediT contributions, per-author competing-interest sentence, confirmation of the AI-assistance
statement). Nothing else in the package is a placeholder.

**Novelty label (revised after amendment A3): NOT REMARKABLE by the brief's bar, but now with a constructive,
reusable idea** — "set any progression detector's threshold on shuffled copies of the clinic's own fields" — which
removed excess false alarms in all tested detectors and restored external specificity (61% -> 95%) without labels.
It does not add sensitivity (no step change), so the "remarkable" criteria (big real-world gain) are still unmet.
Previous label: NOT REMARKABLE — honest strongest result. After 6 development rounds and 2 restarts
(journal_selection/novelty_escalation_log.md, Supplementary Note S1) no method idea produced a valid step change.
The paper reports an evaluation finding instead: in this benchmark, the largest apparent early-detection gains came with
excess false alarms that specificity in reference-stable eyes missed, and no valid detector was significantly better
than the simple trend test (with wide intervals).

## Final novelty scorecard (honest re-score after review)

| Item | Score | Reason |
|---|---|---|
| Distance from closest papers | 3 | True no-change retest specificity is not new (Artes 2014); the extension to 10 detectors x 4 series lengths + ML thresholding + shuffle audit is incremental |
| Strength of problem | 4 | Escalation decisions; false flags have treatment consequences |
| Depth of idea | 3 | Mechanisms (pooled null too narrow; ML threshold selection) argued, partly untested |
| Strength of evidence | 3 | Locked test split, 3 data sets, exact reproduction of deterministic detectors; but 26/26 reference, 30 retest patients, D6 Artes result not independent |
| Generality | 3 | One retest cohort, one external set with circular labels |
| Journal level match | 3 | Above the journal's median evidence level (benchmark: 1 data set, 2 comparators), but weak therapy scope |
| **Total (round 1)** | **19 / 30** | Below the 22 start gate |
| **Total after A3** | **22 / 30** | distance 4 (shuffle-calibrated thresholds for arbitrary detector scores not found in our search), evidence 3, depth 4 (mechanism tested by calibration), generality 4 (works across perimeters), problem 4, journal match 3 |

## Top rejection risks (in order)

1. **Scope (desk rejection):** reduced by the constructive clinic-level recommendation (calibrate before using flags to escalate), but *Ophthalmology and Therapy* publishes therapy, device and outcomes research; this is a
   methods/evaluation paper without treatment or outcome data. Mitigation: framed around escalation decisions;
   consider a pre-submission enquiry to the editorial team (the guidelines invite this). User confirmed the journal.
2. **Underpowered main comparison:** 26 progressors; gains of up to 42 percentage points lay within the confidence intervals of valid detectors (values.json: max_gain_hi), and reviewer 01 estimated that only gains of about 35 points or more could reach significance. Stated
   openly, but reviewers may judge the main question unanswered.
3. **Incremental novelty:** reviewers may say Artes et al. 2014 already did the core idea. Mitigation: cited and
   positioned as an extension.
4. **ML strawman criticism:** our D8/D9 are generic models, not published systems. Mitigation: claims restricted.
5. **Development reuse of Artes data for D6:** disclosed; D8/D9 results on Artes are independent.
6. **Validity rule finalised after results:** disclosed with the strict-rule alternative.
7. **Length:** main text about 5,700 words (journal guide ~4,000, a guide not a limit). Could be trimmed on request.
8. **Timeline:** journal received-to-accepted p75 = 70.25 days, close to the 72-day limit; major revision would
   exceed it.
9. **JCR quartile:** Q1 from secondary sources only (UNVERIFIED against JCR); IF 4.2 from the publisher page.
10. **Cost:** mandatory APC USD 8,050.
11. **Reproducibility on request only:** code is "available on request" (user decision), which some reviewers and
    TRIPOD+AI-minded editors view less favourably than a public repository.

## Residual issues not fixed
- No formal STARD-style flow diagram (flow numbers are in the text).
- Fig. 2 has some overlapping point labels.
- Published ML detectors were not re-implemented; no long-term no-change data; no treatment linkage.

## Integrity checks done
- Every manuscript number generated from results/*.json by manuscript/fill_values.py (values.json lists all of them);
  the script fails on any unfilled placeholder.
- Deterministic detectors D1–D3 reproduced exactly from raw data (results/repro_check.json, 336/336 flags each);
  unit tests pass; quick mode runs end to end.
- All 37 references resolved via Crossref (DOIs verified); TRIPOD+AI DOI corrected; preprint labelled.
- GRAPE perimeter and label definitions verified from the data paper; Artes data licence verified from the package.
- All post-hoc analyses are labelled post hoc; all protocol deviations listed in Methods.
