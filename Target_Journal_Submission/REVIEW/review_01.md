# Review 01 — Handling editor desk check (Ophthalmology and Therapy)

**Manuscript:** "How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm"
**Reviewer persona:** handling editor. I check scope, novelty at a glance, and compliance with the Adis author rules summarised in `journal_selection/selected_journal.md` (V15.1 guide).

## Summary
This is a methods benchmark of ten visual-field (VF) progression detectors. It uses public data: UWHVF (26 progressors and 26 stable eyes in the test set), a 30-patient weekly retest set (Artes), and GRAPE (263 eyes). The main message is evaluative: on true no-change data, the apparent gains of complex detectors come with false alarms. The writing is clear. The abstract is within the word limit (286 words, counted with headings). Key Summary Points are present.

Scope fit is weak. The journal's aims cover the use of ophthalmological therapies, devices and surgery. This paper concerns diagnostic and statistical methods for perimetry, and its link to therapy is one sentence about "treatment escalation". The paper is also not ready for submission. Several mandatory declarations are placeholders, and several integrity statements need checking (see reviews 04 and 09). I would not send it out for review in its present form.

**Recommendation: Major revision before external review (return to authors; not desk-rejected outright).**

## Issues

1. **MAJOR — Scope / framing (Introduction paras 1 and 4; Key Summary Points).** The therapy link is asserted ("A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery"), but no outcome in the study is a therapy outcome. The "unnecessary escalation discussions" in Results ("Real-World Measures", last sentence) are 1,000 × a retest false-alarm rate, not observed escalations. *Fix:* reframe the paper explicitly as decision support for escalation. Either add an analysis that connects to treatment (for example, the expected number of escalations per 1,000 eyes under each detector, with the stated assumptions shown in a table), or justify the scope fit in the cover letter. Otherwise consider a methods or perimetry journal (e.g., TVST).

2. **MAJOR — Declarations incomplete (Declarations: Funding, Author Contributions, Disclosures; title page).** These contain placeholders: "[AUTHORS TO CONFIRM...]", "[AUTHORS TO ADD...]", "[CODE REPOSITORY URL TO BE ADDED]", and there are no authors or ORCIDs. Adis requires a Rapid Service Fee statement, CRediT contributions and individual disclosures. *Fix:* complete all of them before submission. A submission with placeholders would be returned unread.

3. **MAJOR — "Pre-registered" claim (Abstract Methods last sentence; Methods "Study Design").** The protocol is a file in the authors' own git repository. It was committed about 3 minutes before the implementation commit and about 30 minutes before the results commit, all on the same day. It is not registered with a third party (OSF, AsPredicted, PROSPERO-like). Editors will read "pre-registered" as public registration. *Fix:* say "analysis plan time-stamped in the project repository (commit hash X) before the final run". Alternatively, deposit the protocol on OSF now and describe it honestly as retrospective deposit.

4. **MAJOR — Artificial-intelligence use (Declarations, "Medical Writing...").** The statement says an AI assistant wrote the analysis code and drafted the manuscript. Springer Nature policy asks for documentation of LLM use, typically in Methods. The repository history shows the AI also designed the study, wrote the protocol and ran every analysis. *Fix:* move a precise statement into Methods. Say which steps were AI-performed: design, protocol, code, analysis, drafting. Confirm human verification of each. Name the human guarantor.

5. **MODERATE — Ethics statement placement and licence claims (Methods "Ethics"; "Compliance With Ethics Guidelines").** These sections repeat each other. The licence claims (UWHVF BSD-3, GRAPE CC0, visualFields Apache-2.0) need verifying against the sources. I could not verify them from the manuscript, and the visualFields licence in particular should be checked on CRAN. *Fix:* cite the licence URLs. Keep one full statement in Methods, as the guide requires, and a short one in Declarations.

6. **MODERATE — Figure legends and figures missing from the manuscript file.** Figures 1–4 are cited, but there are no legends in the manuscript (they sit in `figure_legends.json`). *Fix:* add a "Figure Legends" section after the references, as Adis requires. Upload the figures as separate files.

7. **MODERATE — Reference hygiene.** Ref. 23 has a DOI prefix (10.64898) that is unusual for medRxiv (historically 10.1101). Ref. 28 is cited as 11(1):2 but its DOI ends ".1.1". Refs 6, 23 and 26 are 2026 items that I could not verify. *Fix:* re-verify each against Crossref or PubMed, and correct the article number or DOI mismatch in ref. 28.

8. **MINOR — Key Summary Points (KSP bullet 3 of "What was learned").** The bullet "in Seattle or in an external clinic in China" implies validity was assessed in GRAPE. It was not, because there is no true-null arm for that perimeter. *Fix:* reword as "in the external clinic, gains in sensitivity came with significantly more false positives against the clinic labels".

9. **MINOR — Hypothesis statement.** The guide asks that the Introduction end with a testable hypothesis. The hypothesis given is a "no difference" hypothesis that cannot be confirmed with n = 26 (see review 04). *Fix:* reformulate as an estimation aim, or as a non-inferiority or equivalence hypothesis with a margin.

10. **MINOR — Line numbers and a plain-language summary are absent.** *Fix:* add both (the plain-language summary is optional but encouraged).

## Editor's note to authors
Before external review, please address items 1–4 and the integrity items raised in reviews 04 and 09: the validity rule absent from the protocol, the majority-vote versus seed-mean mismatch, and the quick-mode run on GRAPE/Artes before amendments A1 and A2.
