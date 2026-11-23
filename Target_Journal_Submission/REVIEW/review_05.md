# Review 05 — Editor desk-check (Ophthalmology and Therapy, Adis Rapid+)

**Desk decision as submitted:** Return to authors without review (incomplete submission). If it were complete: high risk of desk rejection on scope and novelty, but sendable if reframed.

## Summary

The format mostly complies:
- Abstract: 292 words (headings excluded), structured as Introduction/Methods/Results/Conclusion.
- Keywords: 8, in alphabetical order.
- Key Summary Points: 5, in the prescribed structure.
- Title: 19 words.
- Plain Language Summary: 215 words.

The submission is incomplete: authors, affiliations, conflicts of interest, funding, author contributions and the data repository URL are all placeholders. The scope fit with a therapy journal is weak, and the novelty claims ("true no-change arm", "shuffle audit") overlap with work the manuscript itself cites. The pre-registration claim and the post hoc validity rule (Review 02) are integrity-level concerns that an editor would raise before sending the paper out.

## Issues

### 1. FATAL — The submission is incomplete; the mandatory declarations are placeholders
**Location:** "**Authors:** [AUTHOR NAMES, DEGREES — to be completed by the authors]"; "## Conflict of Interest [TO BE COMPLETED BY THE AUTHORS for each author by name.]"; "[PUBLIC REPOSITORY URL — to be added by the authors before submission]"; "[TO BE CONFIRMED BY THE AUTHORS] No funding or sponsorship was received"; "Author Contributions [TO BE COMPLETED ...]".
**Problem:** Adis requires all of these at submission, as well as the Rapid Service Fee funding statement. The AI-use statement asserts that "The authors checked the code, the result files and every cited reference". With no authors named, this cannot yet be true.
**Fix:** Complete every declaration. Make the repository public with a DOI (Zenodo) before submission. Make sure the named authors actually performed the checks the AI statement attributes to them.

### 2. FATAL — "Pre-specified"/"time-stamped" claims coexist with an undisclosed post hoc change to the primary validity rule
**Location:** Abstract: "Ten pre-specified detectors"; Methods: "The analysis plan, including all ten detectors, thresholds, reference standards and statistical tests, was written down and time-stamped before the final test data were analysed ... Two amendments were made before any final result was seen; both are reported below."
**Problem:** The protocol's validity criterion ("FPR CI upper bound vs 5%") differs from the manuscript's ("lower limit ... at or below 5% ... and the upper limit did not exceed 10%"). The latter first appears in the manuscript-filling script after the results existed, and under the protocol rule D1 is invalid at every k (Review 02, Issue 1). The "pre-registration" is also a git commit in the authors' own repository, made 28 minutes before the full results commit, not a public registry entry.
**Fix:** Disclose the deviation and present both rules. Describe the protocol as "internally time-stamped (commit hash ...)" rather than implying registration. Cite the commit hash in the Methods.

### 3. MAJOR — Scope: no therapy, intervention or treatment outcome is studied
**Location:** Title, KSP 1 ("Escalating glaucoma treatment depends on detecting visual-field progression"), Conclusion ("before they guide treatment escalation").
**Problem:** The journal's scope covers "research around the use of ophthalmological therapies, devices and surgical techniques". This is a diagnostic-methods benchmark with no therapy data. The treatment link is asserted rather than studied (see Review 01, Issue 4), and a handling editor would likely suggest a diagnostics or methods journal (e.g., TVST, Ophthalmology Science, Ophthalmology Glaucoma).
**Fix:** Either make the treatment relevance concrete (for example, model the escalation decisions or treatment burden implied by each detector's false-alarm and miss rates under a realistic monitoring schedule), or retarget.

### 4. MAJOR — The novelty overlaps with prior work, including work cited in the paper
**Location:** Introduction: "Specificity is usually estimated indirectly: by shuffling test order"; "Only a few studies have measured false alarms on true no-change data ... [9]". Abstract/KSP: "Clinics and developers can check false alarms with a shuffle audit of their own records".
**Problem:** The paper's own Introduction says that shuffling test order is the *usual* way to estimate specificity, yet the "shuffle audit" is presented as a contribution, and its pre-specified agreement target was not met (ρ = 0.65 < 0.70). The true no-change arm is the published Artes 2014 dataset, which was originally used to estimate GPA specificity (reference 9's full title, truncated in the reference list, is "... What Is the Specificity of the Guided Progression Analysis?"). The incremental contributions are the open benchmark and the side-by-side comparison of ten detectors. Those are worthwhile, but they are not what the abstract sells.
**Fix:** Reposition the paper as an open benchmark/resource. Describe the shuffle audit as an existing technique evaluated against a true null. Put prior Artes-based specificity work up front.

### 5. MAJOR — The abstract and KSPs omit unfavourable or qualifying results
**Location:** Abstract Results: "Gradient-boosted trees, thresholded at 95% specificity, had false-alarm rates of 27.7% at three tests and 18.8% at five tests." "The shuffle audit agreed with true false alarms within 3 percentage points in 80% of detector–test-number cells (Spearman ρ = 0.65)."
**Problem:** The abstract omits that D8 was valid at six tests with the highest point sensitivity (70.8%; 3.6% false alarms), and that the pre-specified H3 target (ρ ≥ 0.70) was not met. The guidelines say "Abstracts must reflect the content of the article accurately", and the KSPs "must purely reflect the content within the article".
**Fix:** Add "the pre-specified agreement target (ρ ≥ 0.70) was not met" and D8's six-test result. Add CIs for the main abstract figures.

### 6. MAJOR — The Conclusion overclaims beyond the design
**Location:** Abstract Conclusion: "A plain trend test of mean sensitivity remained as good as any valid alternative." Main Conclusions: "In three independent data sources, a plain trend test ... was as good as any detector that kept false alarms at the nominal level ... Faster confirmation of progression will more likely come from better-timed testing than from more aggressive analysis."
**Problem:** These are equivalence claims from an underpowered study (a difference of ≥ 35 pp is needed for significance; Review 02, Issue 2). Sensitivity was measured in only one source. Test scheduling was not studied, so the "better-timed testing" sentence is not an inference from this study. Adis asks that "The conclusion should be an inference, not a summary". The inference must also be supported.
**Fix:** Limit the conclusion to what was shown: no significant gain at valid false-alarm rates; large false-alarm excess for the specific detectors tested; the audit is useful but imperfect. Move the scheduling point to the Discussion as a hypothesis.

### 7. MODERATE — Sex/gender reporting (SAGER) is missing
**Location:** Abstract and Table 1.
**Problem:** The author instructions say "Article titles and/or abstracts should indicate what sex(es) the study applies to" and ask for disaggregated data or a rationale. UWHVF contains a gender field (`load_series` reads it), but neither the abstract nor Table 1 reports sex.
**Fix:** Add sex distribution to Table 1 and one sentence to the abstract or Methods. Give a rationale for not doing a sex-stratified analysis.

### 8. MODERATE — The Introduction does not end with the hypothesis
**Location:** The last sentence of the Introduction is "We also tested whether a simple "shuffle audit", which any clinic can run on its own records, estimates the true false-alarm rate."
**Problem:** The guidelines require the Introduction to include the research hypothesis, and the house style favours ending with it. The hypothesis is in the penultimate sentence and is phrased as a null ("no detector would ..."), which reads oddly as a research hypothesis.
**Fix:** End with an explicit, testable hypothesis, including H3 for the audit, e.g. "We hypothesised that ... and that the shuffle audit would agree with true no-change false-alarm rates (Spearman ρ ≥ 0.70)."

### 9. MODERATE — Reference-list quality
**Location:** Reference 24: ". TRIPOD+AI statement: ..." (no authors). Reference 9 and reference 3 have truncated titles. Reference 25: "2022;11(1):2. https://doi.org/10.1167/tvst.11.1.1" (the page number and DOI suffix disagree; please verify). Reference 21 is a medRxiv preprint dated "2026.11.16", one week before the protocol date, and is cited as support for the clinical recommendation ("scheduling guided by risk [21, 35]").
**Fix:** Correct the authors and titles and verify the DOI of reference 25 against the publisher. Mark reference 21 as a non-peer-reviewed preprint, or replace it.

### 10. MINOR — The title is long and does not state the design succinctly
**Location:** "How Early Can Glaucomatous Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm" (19 words; the limit is ≤ 20).
**Fix:** This is acceptable as is. Consider e.g. "False Alarms in Early Detection of Visual-Field Progression: An Open Benchmark of Ten Detectors With a Retest Null Arm" (no "glaucomatous"; see Review 01, Issue 7).

### 11. MINOR — The PLS overstates the findings
**Location:** "This check gave a fair estimate of the false-alarm rate." "Methods that found more worsening, including two machine-learning methods, also gave many more false alarms."
**Fix:** H3 failed, and D9 did not find more worsening (Review 04, Issue 4). Revise both sentences.

### 12. MINOR — The ethics statement is duplicated verbatim
**Location:** The "Ethics" section in the Methods and the "Ethical Approval" section in the Declarations.
**Fix:** This is acceptable under Adis rules (the statement is needed in both places), but shorten one of them.

### 13. MINOR — Figure quality
**Location:** Fig. 2 (overlapping labels "D1/D5" and "D4/D7/D10" at the origin of the 3-test panel are illegible; the shaded "≤ 5%" band does not match the validity rule actually used, so D1 at k = 6 (5.1%) sits outside the band but is labelled valid). Fig. 1 (the Artes arrow points into the "10 detectors" box, implying training use). Fig. 2 legend: "Detectors far to the right of the band appear sensitive only because they raise more false alarms" (a causal claim in a legend).
**Fix:** De-clutter the labels and mark invalid cells explicitly in Fig. 2. Redraw the Fig. 1 arrows. Make the legend descriptive.
