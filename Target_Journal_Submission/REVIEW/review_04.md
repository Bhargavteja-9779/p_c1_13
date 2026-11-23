# Review 04 — Handling editor desk check (Ophthalmology and Therapy, Adis/Springer)

## Summary

This is an Original Research submission reporting a retrospective benchmark of ten visual-field progression detectors on three public datasets. The main message is negative and methodological: apparent early-detection gains are false alarms, a simple trend test is a strong default, and a "shuffle audit" is offered as a practical check. I assessed scope, novelty, publishability of a negative result, compliance with the Adis author instructions (`journal_selection/author_guidelines/I4A.txt`), and internal consistency.

The manuscript is well organised and largely compliant in form:

- The structured abstract has 294 words, including headings, against a limit of 300.
- There are 5 Key Summary Points in the required two-part structure.
- There are 7 keywords, within the required 3–10.
- The main text is about 4,480 words, against a guide of about 4,000 that is "not limited to".

Its main desk-level weaknesses are scope fit (no therapy data at all), headline claims stronger than the design supports (see Reviews 01–03), undefined internal labels (RQ/H numbers), and incomplete declarations. A negative or benchmark result is publishable in this journal, which accepts "all scientifically sound research", but only if the negative claim is framed as an estimate with its uncertainty.

## Issues

### 1. MAJOR — Scope: no therapy, intervention or outcome data; the escalation framing is asserted, not studied
*Location:* Abstract Introduction: "which would allow earlier treatment escalation". Discussion: "a flag from it should not by itself trigger escalation of treatment". Conclusion: "before relying on its flags to escalate treatment."

*Problem:* The journal's scope is research "around the use of ophthalmological therapies, devices and surgical techniques" (`selected_journal.md`). None of the three datasets contains treatment, IOP or escalation information. The link to therapy rests entirely on rhetoric. Reviewers from a therapy readership will ask what changes in management. Clinical diagnostic-methods journals (Ophthalmology Glaucoma, TVST, IOVS, Ophthalmology Science) are more natural homes. If the authors stay here, the paper needs a concrete therapy-relevant quantity. For example: the expected number of unnecessary escalations per 1,000 stable patients per year under each detector at realistic testing frequency, with assumptions stated. The current "false flags per 1,000 stable eyes at one review" is a start, but it is per review and not per year of care.

*Fix:* Add the therapy-relevant translation described above, or consider transfer to a diagnostics journal. Tone down the escalation recommendations unless they are directly supported.

### 2. MAJOR — Headline claims exceed what the design supports; the abstract and Key Summary Points need rewriting
*Location:* Title: "…Without False Alarms". Key Summary Points: "No detector with a valid false-alarm rate beat the simple trend test significantly at any number of fields, so the evidence does not support replacing it in routine care." Abstract Conclusion: "the largest apparent early-detection gains were false alarms that standard specificity estimates missed."

*Problem:* The guidelines require that Key Summary Points "must purely reflect the content within the article" and that "Abstracts must reflect the content of the article accurately". As detailed in Reviews 01–03:

- (a) The primary comparison can only detect gains of about 35 points or more with 26 progressors, so "no detector beat" is absence of evidence.
- (b) The validity rule that defines "valid" was set after the results and differs from the protocol. Under the protocol wording, D1 itself is not valid.
- (c) The D6 false-alarm result had already been measured on the same Artes data before the protocol was written (`novelty_escalation_log.md`, round 5).
- (d) The external comparison is largely circular: 38% of GRAPE eyes have exactly the three fields used for both the label and D1.
- (e) The external ML result reflects an unscaled perimeter-unit mismatch.

*Fix:* Rewrite the abstract results and conclusion, the Key Summary Points and the title around estimates and CIs. Present D6 as a known-invalid positive control, and state the minimum detectable difference. A suggested title: "False-alarm rates of visual-field progression detectors with few fields: an open benchmark with a true no-change arm".

### 3. MAJOR — Novelty relative to prior work is not established
*Location:* Introduction: "Only a few studies have measured false alarms on true no-change data … [9]". Discussion: "We extend this approach to ten detectors and four series lengths".

*Problem:* Measuring specificity on retest data (Artes 2014 [9], on the same dataset) and on permuted or shuffled series (the logic of PoPLR [7]; several prior permutation-based specificity analyses) is established methodology. The "shuffle audit" is the standard permutation-specificity estimate that has long been used for PoPLR, reframed as a clinic tool. The novelty therefore lies in the combination and in the open benchmark. That is legitimate, but the paper needs a short, referenced paragraph on what earlier specificity-estimation studies did and what this study adds. The Introduction also says "most new detectors are judged by how many eyes they flag" without a systematic basis (the novelty search in `journal_selection/` is not reported).

*Fix:* Add a related-work paragraph with specific prior specificity-estimation studies. Either support "most new detectors…" with the search or soften it.

### 4. MAJOR — Undefined internal labels and protocol cross-references
*Location:* Results headings: "False alarms on true no-change data (RQ1 and RQ4)", "(RQ2)", "(RQ3)", "(RQ5)". Text: "the pre-specified hypothesis H2 was not falsified", "Hypothesis H3 was therefore partly met".

*Problem:* RQ1–RQ5 and H2–H4 are defined only in `code/experiments/protocol.md`, not in the manuscript. The Introduction states a single, differently worded hypothesis ("no detector would flag substantially more…"). The protocol's H2 uses a ≥ 10-point margin, and H3 has two criteria, ρ ≥ 0.7 and "most cells within 3 points". H4 is never adjudicated in the text. Also, protocol RQ5 refers to "clinician-applied criteria", whereas GRAPE labels are rule-based. The manuscript corrects this silently. It should be listed as a deviation.

*Fix:* List RQ1–RQ5 and H2–H4 verbatim in Methods, with their decision rules. Report each as met or not met. H3 should be reported as not met, since ρ = 0.65 < 0.7. List all deviations from the protocol in one table: the validity rule; the time-to-detection definition (protocol "followed to 8 tests" versus manuscript "until six fields … counted as seven"); the D8 feature set; GRAPE D5 calibration (LOPO → 5-fold, which is covered by A2); and the GRAPE label description.

### 5. MODERATE — The pre-registration claim needs qualification
*Location:* Methods: "The analysis plan … was written down and time-stamped before the final test data were analysed … Two amendments were made before any final result was seen".

*Problem:* The plan is time-stamped only by a git commit in a private repository, made the same day as the analysis (commit c0dedb5, 09:05, with full results at 09:33). There is no external registry (OSF/Zenodo). The validity operationalisation was added later (see issue 4). Editors and readers cannot verify the time stamps independently.

*Fix:* Archive the protocol commit with a DOI (Zenodo) before submission, and cite the archived commit hash. Do not call the plan "pre-registered" unless it is in an external registry. Use "pre-specified (internally time-stamped)".

### 6. MODERATE — Declarations incomplete; mandatory items are placeholders
*Location:* Authors, Corresponding author, Funding, Author Contributions, Conflict of Interest, Code Availability ("[REPOSITORY URL — TO BE INSERTED …]"), Acknowledgements, Prior presentation.

*Problem:* The manuscript cannot be sent out in this state. Adis also requires a statement of who paid the Rapid Service Fee in the Funding section, line numbers in the manuscript, and figures as separate JPG/TIFF files.

*Fix:* Complete all declarations, add line numbers, and supply TIFF figures. Make sure the AI-assistance statement meets Springer Nature's AI policy: AI use described in Methods and not listed as an author. The current wording is acceptable once the authors confirm it.

### 7. MODERATE — The structured abstract Introduction lacks the research hypothesis
*Location:* Abstract, Introduction: "We asked how early progression can be detected from the first few fields without raising false alarms."

*Problem:* The guidelines require "Introduction (including the research hypothesis)" for both the abstract and the main text. The abstract states a question, not a hypothesis. It is also at 294 of 300 words, which leaves no room to add caveats.

*Fix:* Add a one-clause hypothesis and cut elsewhere. For example, the Methods sentence listing evaluation sets can be compressed, and "(30 patients tested weekly for 12 weeks)" could become "(weekly retests)".

### 8. MODERATE — SAGER and reporting checklist
*Location:* Throughout.

*Problem:* The journal encourages SAGER reporting. UWHVF provides gender, which is not reported or discussed. The paper claims TRIPOD+AI adherence, but no checklist is supplied. The benchmark is closer to diagnostic accuracy, where STARD 2015 applies.

*Fix:* Report sex distribution for each dataset, or the reason it is unavailable. Supply a completed TRIPOD+AI or STARD checklist as supplementary material.

### 9. MODERATE — Reference list problems (verify before submission; integrity)
- Ref 24 has no authors: ". TRIPOD+AI statement…". Add Collins GS, Moons KGM, Dhiman P, et al.
- Ref 25: "Trans. Vis. Sci. Tech.. 2022;11(1):2. https://doi.org/10.1167/tvst.11.1.1". The article number (2) and DOI suffix (.1) disagree. Verify against Crossref.
- Ref 21: a medRxiv preprint dated 2026 with DOI prefix "10.64898" and posting date 2026-11-16, one week before this draft. The prefix differs from medRxiv's usual 10.1101. UNVERIFIED by this reviewer; confirm it resolves to the stated preprint, and check that citing a non-peer-reviewed preprint for "risk-based test scheduling" is appropriate.
- Ref 9: the title is truncated.
- Double periods throughout ("Invest. Ophthalmol. Vis. Sci.."; "Trans. Vis. Sci. Tech.."). Use the Adis reference style with NLM abbreviations.

### 10. MINOR — Supplementary material consistency
*Location:* Supplementary Material paragraph lists S1, S2 and Note S1. The repository's `supplementary/` folder contains S1–S3, including Table S3 (tests to first detection). S3 is not cited in the text, though the time-to-first-detection results are reported in Results. Supplementary Note S1 says "All pilot analyses below used only the UWHVF training and validation sets", yet round 4 used Moorfields nAMD data.

*Fix:* Cite S3 where the time-to-detection results appear, and correct the Note S1 sentence.

### 11. MINOR — Figures
*Location:* Fig. 2.

*Problem:* The shaded band in Fig. 2 marks FPR ≤ 5%, but the text's validity rule allows CI upper limits up to 10%, so the figure and the rule disagree visually. Labels overlap (D1/D5, D2/D3) and are illegible. The x-axis scales differ between panels without comment. Fig. 3 has no CIs.

*Fix:* Harmonise the shading with the stated rule, de-overlap the labels (offset or leader lines), use a common x-axis or flag the differing scales, and add CIs to Fig. 3.

### 12. MINOR — Table 3 denominators
*Location:* Table 3.

*Problem:* At k = 4, only 163 eyes (18 progressors) are analysable, but the table does not show this. D1 sensitivity falls from 44% (k = 3) to 33% (k = 4) because the eye set changes, which readers will misread as a paradox.

*Fix:* Add n (progressors/non-progressors) for each k and footnote the change in eye set.

## Is a negative or benchmark result publishable here?

Yes, in principle. The journal's scope statement ("all scientifically sound research") and its open-science stance support well-conducted negative benchmarks. For this paper, it depends on (i) reframing the claims as estimates with explicit minimum detectable differences, (ii) transparently listing deviations from the protocol and using the protocol's validity rule (or reporting both), and (iii) fixing the circular external validation. Without these, the "negative" result is partly built into the design.

## Recommendation

**Major revision** (send to review after the authors complete the declarations and the hypothesis/deviation table). Scope fit is weak but defensible if the therapy-relevant translation is strengthened. The headline claims must be brought in line with the evidence before peer review can assess the contribution fairly.
