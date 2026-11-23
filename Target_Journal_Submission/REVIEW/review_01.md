# Review 01: Handling editor desk check (Ophthalmology and Therapy)

**Manuscript:** "Early Detection of Glaucomatous Visual Field Progression Without False Alarms: A Benchmark With True No-Change Data"

## Summary
The authors compare ten progression detectors (trend, event, permutation, conformal and ML) on the first 3–6 visual fields. They use three public data sets: UWHVF (future reference, 26 progressors and 26 stable eyes), the Artes 12-week retest data (30 patients, the "true no-change" arm) and GRAPE (263 eyes, external). The main message is that the one significant sensitivity gain over an OLS mean-sensitivity trend (D6) came with false alarms of 22.4% on retest data, and that a "shuffle audit" approximates true false-alarm rates.

The paper is clearly written, short and openly documented. Abstract (278 words), Key Summary Points and the hypothesis at the end of the Introduction follow the journal format. My concern is whether the evidence matches the strength of the conclusions, and whether the advance is enough for this journal:

- The headline finding concerns D6, a variant the authors built themselves. Its invalidity on the same Artes data was already known before the protocol was written (`novelty_escalation_log.md`, Round 5: "region-max detrended: sens 35.5%, FPR 20–22% -> INVALID").
- The final validity definition differs from the protocol. Under the protocol's own rule, the comparator D1 is itself "invalid" at every number of tests (Supplementary Table S1).
- The reference set is very small, so the trial is underpowered.

## Recommendation
**Major revision.** I would send this for external review, but I warn the authors now that the framing must change before it can be considered.

## Issues

1. **FATAL – The headline result was known before the analysis plan.**
   - *Location:* Abstract Results ("The only detector with significantly higher sensitivity … raised 22.4% false alarms"); Conclusion ("apparent gains in early progression detection were explained by false alarms"); Key Summary Points bullet 1.
   - *Problem:* D6 is not a published method. The authors developed it, found it anti-conservative on the same Artes data (Round 5), and only then pre-specified the benchmark. The general claim that "apparent gains … were explained by false alarms" therefore rests on one in-house detector whose failure was known in advance. The final Artes result (22.4%) re-measures the development result (20–22%) on the same 30 patients. It is not an independent confirmation.
   - *Fix:* Present D6 explicitly as a known-invalid positive control for the evaluation framework, both in the Methods (D6 bullet) and in the Abstract. Delete the general claim about "apparent gains" in the literature, or support it with published detectors evaluated on independent no-change data.

2. **FATAL – The validity rule departs from the protocol, and the departure changes the conclusion.**
   - *Location:* Methods, Statistical analysis ("valid … lower limit … ≤5% … upper limit ≤10%"); Supplement S2; Table S1.
   - *Problem:* The protocol says "Validity: FPR CI upper bound vs 5%". Under that rule, D1 is not valid at any k: its upper limits are 6.3, 6.2, 7.5 and 8.1% (`metrics.json`). The central sentence "No detector with valid false alarms beat OLS-MD" then has no valid comparator.
   - *Fix:* Make the protocol rule primary in the main text, or show both rules side by side in Table 1. Rewrite RQ2 so it does not depend on a rule chosen after the protocol.

3. **MAJOR – Scope and fit for a therapy journal.**
   - *Location:* whole paper.
   - *Problem:* This is a statistical and methodological benchmark with no treatment, outcome or patient-level management component. It suits *Ophthalmology and Therapy* only if the clinical message is concrete and supported. At present that message ("a simple trend test is hard to beat; run a shuffle audit") is partly unsupported (see issue 5).
   - *Fix:* Strengthen the clinical translation: cumulative false alarms per patient-year, consequences for escalation, and a confirmation-test strategy. Alternatively, consider a methods journal.

4. **MAJOR – The sample is too small for a negative conclusion.**
   - *Location:* Results RQ2; Abstract ("No detector with valid false alarms beat OLS-MD significantly").
   - *Problem:* There are 26 progressors. With exact McNemar and Holm over 9 comparisons, a detector needs at least 9 discordant eyes, all in its favour, to reach significance, which is about a 35-percentage-point gain. The protocol's 10-pp margin (H2) was silently dropped.
   - *Fix:* State the minimum detectable difference. Reframe RQ2 as estimation, using the protocol's 10-pp margin and confidence intervals.

5. **MAJOR – The shuffle-audit claim goes beyond the data.**
   - *Location:* Key Summary Points bullet 2 ("identified the invalid detectors"); Abstract ("tracked true false-alarm rates").
   - *Problem:* The pre-specified target ρ ≥ 0.7 was not met (0.65), and the Abstract does not say so. The audit missed D6 at six tests (shuffle 4.9% vs true 7.6%). It also flagged valid detectors: D2 at 3 tests (11.7%), D7 at 5 and 6 tests (7.9%, 11.7%) and D8 at 6 tests (8.7%).
   - *Fix:* Report in the Abstract that H3 was not supported, and soften the Key Summary Points.

6. **MAJOR – Novelty relative to existing literature.**
   - *Location:* Introduction paragraph 4; Discussion.
   - *Problem:* False-positive rates measured on retest data or by re-ordering test series are established. Examples: Artes 2014 [9] (GPA on 12 retest tests with 1,000 re-orderings), O'Leary 2012 [7], Marín-Franch 2021 [13], Montesano 2021 [14] (permutations of a test–retest cohort). The paper reads as if the shuffle audit were new, yet the Introduction itself says specificity is "usually estimated … by shuffling test order".
   - *Fix:* Add an explicit paragraph on how this work differs from [7, 9, 13, 14], and drop the implied novelty of the shuffle audit.

7. **MODERATE – "Pre-registered" wording.**
   - *Location:* Methods, Study design ("written down and time-stamped"); Data Availability ("pre-registered protocol").
   - *Problem:* The protocol is a commit in the authors' own repository, not an entry in a public registry.
   - *Fix:* Use "time-stamped analysis plan (commit hash …)". If possible, deposit a frozen copy on OSF and give the link.

8. **MINOR – Submission completeness.**
   - *Location:* title page; Declarations; Data Availability.
   - *Problem:* Authors, affiliations, funding, conflicts and the repository URL are placeholders. The headings "Conflict of Interest" and "Ethical Approval" do not match the journal's "Disclosures" and "Compliance with Ethics Guidelines". The AI-assistance statement is inside a placeholder.
   - *Fix:* Complete all of these before resubmission. Springer Nature policy expects AI/LLM use to be documented in the Methods.
