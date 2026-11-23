# Review 07: Research integrity

**Reviewer role:** research integrity. I compared the pre-registration claims with what happened, looked at how the Artes data were used during development, and checked for HARKing, selective reporting and the reporting of negative results.

## Summary

The authors deserve credit for publishing the full development log, including abandoned ideas and an unrelated nAMD pilot. They also report a failed pre-specified target (ρ < 0.70) and disclose that the Artes data were used in development. However, the git history and the supplement show three things:

- The study's central finding was observed on the same true no-change data before the "pre-registered" protocol was written. That finding is that the most sensitive pooled-detrended detector is invalid on Artes while OLS-MD is valid.
- The study question was then chosen because of that finding.
- The validity rule that classifies detectors was written after the final results.

The paper still describes the work as pre-specified and confirmatory. As written, it overstates its evidential status.

## Timeline reconstructed from `git log` (all on 2026‑11‑23, UTC)

| Time | Event |
|---|---|
| 08:11:48 | Repository initialised |
| 08:48–09:02 | Pilot rounds 0–4 (UWHVF validation split; nAMD) |
| 09:05:02 | Commit "Round 5: pooled-null gain at k=3 is a false-alarm artefact; pivot to true-null benchmark". Artes was already analysed at this point. |
| 09:05:51 | Commit "Pre-registered protocol" (49 s later) |
| 09:08:27 | Ten-detector implementation and Amendments A1–A2 (2 min 36 s later) |
| 09:33:48 | Full results committed |
| 10:22:55 | `fill_values.py` committed. This holds the validity rule and the claim checks. |

## Issues

**1. FATAL — The primary validity result for the two pivotal detectors was known before the protocol, and the paper still presents it as a pre-specified test.**
- Locations:
  - Abstract: "Ten pre-specified detectors". KSP: "We hypothesised that no detector would…".
  - Methods: "The analysis plan … was written down and time-stamped before the final test data were analysed".
  - Limitations: "the Artes data were used once during development, to check false alarms of a candidate method".
- Evidence:
  - Supplement S1, round 5, reports on Artes: "region-max detrended: sens 35.5%, FPR 20–22% → INVALID" and "OLS MD parametric: sens 3.2%, Artes FPR 4.0%" (k = 3), and "OLS MD … Artes FPR 2.6%" (k = 4).
  - So the Artes false-alarm rates of both the comparator (D1) and the precursor of D6 were seen before the protocol. The final values are 4.4%, 3.8% and 22.4%.
  - The S1 "Decision" paragraph then chose the paper's framing because of that observation: "The robust, generalisable finding is an EVALUATION finding: apparent early-detection gains … are explained by inflated false alarms that only a true-no-change check reveals."
  - Calling this "a candidate method" understates it: the comparator was checked too.
  - The protocol calls D6 the "development variant that looked more sensitive". It omits that the same log had already found it invalid on Artes.
- Fix:
  - Say plainly in the Abstract, Methods and Limitations that the Artes arm is **not independent confirmation** for D1 and D6. Both were evaluated on these data before the protocol, and the research question was formed after that evaluation.
  - Relabel RQ1 and H2 for D1 and D6 as exploratory, or replicate them on an independent short-term retest data set never touched in development.
  - Remove "pre-specified" from the Abstract, or qualify it.

**2. FATAL — The validity criterion used for every verdict is not the protocol's criterion, and the deviation is not reported.**
- Location: Methods: "A detector was considered valid … if … the lower limit … was at or below 5% … and the upper limit did not exceed 10%".
- Evidence:
  - The protocol says only "Validity: FPR CI upper bound vs 5%". It also promises: "No result-dependent change of thresholds … any deviation will be reported."
  - The two-sided 5%/10% rule first appears in `manuscript/fill_values.py`, committed 49 minutes after the results.
  - Under the most natural reading of the protocol (upper CI ≤ 5%), the comparator D1 fails at every k: its upper limits are 6.3%, 6.2%, 7.5% and 8.1%. The headline "trend test … as good as any valid alternative" then has no valid reference.
  - Under the other reading (invalid only if the lower CI > 5%), D9 at k = 5 and 6 and D6 at k = 6 become valid. That changes the RQ4 statement "supported … for D9 at three, five and six tests".
- Fix:
  - Add a "Deviations from protocol" table listing this rule, its date of creation, and the reason for it.
  - Report results under both protocol readings.
  - Remove any claim that the validity rule was pre-specified.

**3. MAJOR — The "pre-registration" is an internal git commit, not a registration.**
- Locations:
  - Protocol header: "Pre-registered protocol — written 2026‑11‑23, BEFORE any final-test result".
  - Cover letter: "The analysis plan was time-stamped before the final analysis".
  - Data Availability: "the pre-specified protocol".
- Evidence:
  - The protocol is a file in a repository that the study team controls. Commit dates are author-set and can be rewritten.
  - The full ten-detector implementation was committed 2.6 minutes after the protocol, so the code almost certainly existed when the protocol was written.
  - The whole project, from initialisation to filled manuscript, took about 2 h 15 min in one session.
- Fix:
  - Describe the protocol as "internally time-stamped (git commit `c0dedb5`), not externally registered".
  - Publish the complete, unsquashed git history with the code release.
  - For future work, register on an external registry such as OSF before data access.

**4. MAJOR — Results are reported selectively in the Abstract, Conclusions and cover letter.**
- The Abstract reports D8's false alarms at k = 3 and 5 (27.7% and 18.8%). It omits two facts:
  - D8 was valid at k = 6.
  - At k = 6, D8 had the highest sensitivity of any detector: 70.8% against 57.7%, +11.5 pp. That exceeds the paper's own 10-pp margin, although it was not significant.
- The Abstract and Conclusions omit that the pre-specified H3 target (ρ ≥ 0.70) was **not met**. Both still recommend the shuffle audit.
- Pre-specified analyses that were not reported: GRAPE secondary labels (PLR2, PLR3, any); the bootstrap CI for ρ; tests to first detection. The code computes `mean_first_k_detected` but the paper never reports it.
- Specificity CIs are computed but omitted from Table 2. Specificity against the secondary reference (17 stable eyes) is never computed.
- Fix:
  - Add the D8 k = 6 result and the H3 failure to the Abstract.
  - Report every protocol-listed outcome, or list it as not done, with the reason.

**5. MAJOR — The Discussion and cover letter claim the shuffle audit "identified the same invalid detectors", but the paper's own Results contradict this.**
- Locations:
  - Discussion: "In our study, both identified the same invalid detectors."
  - Cover letter: "A simple 'shuffle audit' … flagged the same invalid detectors."
- Contradicting evidence from the Results and Table 2:
  - The audit underestimated D9 at k = 3 (8.5% against 12.7%).
  - It missed D6 at k = 6 (4.9% against 7.6%).
  - It falsely implicated valid detectors: D2 at k = 3 (11.7%) and D7 at k = 6 (11.7%).
  - Its largest error, 10.4 pp, was the invalid D8 at k = 3 (17.3% against 27.7%).
- Fix: reword both passages to "ranked detectors broadly similarly, with errors of up to 10 pp in both directions".

**6. MAJOR — A disclosure promised by the leakage audit is missing from the manuscript.**
- Location: `leakage_audit.md`: "Reference overlap | future reference uses the full series, which includes the first k tests (partial verification); stated as a limitation".
- Evidence: the manuscript's Limitations paragraph never mentions that the reference series contains the index-test data. The only overlap-related limitation concerns the MD basis.
- Fix: add the limitation and quantify it. At k = 6 the index tests are about half of a median 12-test reference series.

**7. MODERATE — The study used many development analyses (a garden of forking paths).**
- Evidence:
  - S1 documents six glaucoma rounds plus an nAMD restart, with explicit selection for a "remarkable" result: "No method idea reached the 'remarkable' bar", "Honest label expected: NOT REMARKABLE".
  - The benchmark question was the residual finding after the method hypotheses failed.
- Disclosing this is good practice, but readers need it in the main text.
- Fix:
  - Add one sentence to Methods. For example: "The benchmark question was formulated after six development rounds in which proposed methods did not outperform OLS-MD; see Supplementary S1."
  - Rewrite S1 in neutral scientific language, keeping the facts.

**8. MODERATE — D6 is a known-invalid comparator presented as a contender.**
- Location: Methods: "This variant was the most sensitive approach during development."
- Evidence: round 5 had already found it anti-conservative on Artes (FPR 20–22%). Including a detector already known to fail makes "the only significantly more sensitive detector was invalid" close to guaranteed.
- Fix: say that D6 was included as a known-invalid positive control for the validity check, not as a candidate method.

**9. MODERATE — Amendment A1 changed the time scale of the Artes arm after Artes results had been seen.**
- Evidence:
  - Round 5 evaluated Artes with weekly times rescaled ×52 (`d6_round5.py` line 55).
  - A1 replaces the real times with UWHVF donor dates.
  - A1 matters mainly for the rate-based rules (D2, D3, D7–D9). Those were not checked on Artes in round 5, so the risk is limited, but readers should know the scale was changed after a look.
- Fix: state when A1 was made relative to round 5, and give round-5-style (rescaled weekly) results for the rate rules as a sensitivity analysis.

**10. MODERATE — Accountability statements cannot yet be true.**
- Locations:
  - Methods, AI use: "The authors checked the code, the result files and every cited reference".
  - Cover letter: "All authors approved the submission."
- Evidence: authors, contributions, funding and conflicts of interest are all placeholders.
- Fix: do not submit until named authors have actually done and documented these checks. Keep the AI-use statement, and give the tool version and the tasks performed.

**11. MINOR — Ethics claims are unsourced.**
- Location: "The original studies obtained ethical approval."
- Evidence: no source is given for each data set. Also, the Artes file is distributed under the visualFields package licence (GPL‑3, per `artes_retest.py`); "open licences" is acceptable but vague.
- Fix: cite the ethics statement for each source paper and name each licence.

**12. MINOR (positive) — Negative results are reported.**
- The failed H3 target, the absence of any valid improvement over D1, and all abandoned ideas are reported.
- The claim-check assertions in `fill_values.py` are a good safeguard. Their output, `claim_checks.json`, should be released with the code.
