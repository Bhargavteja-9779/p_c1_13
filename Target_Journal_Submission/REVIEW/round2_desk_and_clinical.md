# Round 2: desk screening and clinical review

**Journal:** Ophthalmology and Therapy (Springer/Adis)
**Manuscript:** "Apparent Gains in Detecting Glaucomatous Visual-Field Progression Disappear at Matched False-Alarm Rates: A Two-Stage Benchmark" (revised; `manuscript/manuscript_filled.md`)
**Reviewed on:** 2026-11-23
**Files read:** manuscript_filled.md, figure_legends.json, Figs 1–4 (fig1, fig2, fig5, fig6), cover_letter_filled.md, selected_journal.md, style_notes.md. Spot checks against `results/study2_metrics.json` and `results/metrics.json`, and one check of `code/study2.py`.

The author, affiliation, ORCID, funding, COI and author-contribution fields are placeholders. We know this and it is intentional. The editorial office will return the submission at the technical check until they are completed, together with line numbers and figures supplied as separate TIFF/JPG files. These items are not raised again below.

---

## Part 1. Desk decision (handling editor)

**Decision: borderline. As submitted, the more likely outcome is desk rejection on scope and fit.**
**Estimated probability of being sent to review: about 40% (desk reject about 60%).** If the changes in Part 2 are made, I estimate about 55%.

How I reached this: the journal makes most first decisions within days (median 2 days to first decision). Its content is mostly treatment, real-world and health-outcomes research. This manuscript is a statistical and methods benchmark of perimetry analysis rules. It uses only public data, and no therapy appears anywhere in the Methods or Results. The question matters clinically. The work is careful and openly reported, so it could be sent out. But an editor skimming the title, abstract and Fig. 1 will first think "TVST, Ophthalmology Glaucoma or Ophthalmology Science". That reaction has to be overcome on the first page.

### Three strongest reasons to desk-reject

1. **Scope and fit.** Nothing in the study is a therapy, device or surgical technique. Treatment escalation is named in the Introduction and the Plain Language Summary, but no outcome, analysis or figure relates to treatment. The title ("Two-Stage Benchmark"), the Fig. 1 boxes (E1–E4, "shuffle audit", "repeated-look control") and the Methods (D1–D10, S1–S7, B8, Q1–Q4, R1–R3, H6–H9, A1–A2) read like a biostatistics paper. Specialist journals that regularly publish PoPLR, ANSWERS and GPA comparisons (TVST, IOVS, Ophthalmology Glaucoma) are the natural home, and an editor may simply redirect.
2. **Length and density for the readership.** The main text (Introduction to Conclusions, excluding tables) is about 5,000 words, against a guide of about 4,000. Table 2 has 40 rows, and there are 4 tables, 4 figures and 21–22 detector variants. The design has two stages, with a second protocol written after the first study's results were known. Most of the journal's clinician readers will not get past the Methods.
3. **Credibility signals at triage.** The AI disclosure says an AI assistant "write[s] analysis code, run[s] the analyses, ... and draft[s] the text". Code and raw outputs are only "available on request". All data are public and retrospective. The headline result is negative, and it is measured against a reference (mean-deviation slope) that is structurally close to the winning detector. A cautious editor may see a high-risk, low-citation item for an APC journal.

### Three strongest reasons to send to review

1. **A clinically important question with a clear take-home message.** The paper asks whether claims of "earlier detection" by AI progression tools survive once false alarms are controlled. That question applies directly to software now being marketed for glaucoma monitoring, and to decisions to add drops, laser or surgery. The 22-point "gain" that comes with 15% false alarms makes a memorable, policy-relevant example.
2. **Methodological honesty and rigour that are uncommon in this literature.** The design uses a true no-change arm, a locked test split, cross-fitting, an external clinic, protocols time-stamped before analysis, labelled deviations, and Holm-adjusted paired tests. The negative result is expressed as an exclusion of gains of 8.4 points or more, rather than as "no difference".
3. **It complies with the journal format.** The structured abstract is 300 words. There are five Key Summary Points in the prescribed structure, a Plain Language Summary under 250 words, and an explicit hypothesis at the end of the Introduction. The ethics statements appear in Methods and in Declarations, reporting follows TRIPOD+AI, and the journal already publishes AI papers on glaucoma.

---

## Part 2. Changes that would most reduce desk-rejection risk

Listed in order of impact.

### 2.1 Re-frame around the therapeutic decision (highest impact)

The paper must make it obvious from the title onwards that the outcome is **the decision to escalate therapy**. The detector is the tool that triggers that decision.

**(a) Title.** The current title has 20 words, while the journal's titles run 13–16 (style_notes). It also contains "Disappear", which overclaims (see C4).
Replace with:

> **Calibrating Visual-Field Progression Detectors to a Stated False-Alarm Rate Before Escalating Glaucoma Therapy: A Retrospective Benchmark Study**

(18 words.) A shorter alternative (15 words):

> **False Alarms Explain Apparent Gains of a Machine-Learning Glaucoma Progression Detector: A Retrospective Benchmark**

**(b) Introduction, paragraph 1.** Replace the last two sentences ("The key clinical decision is when to escalate treatment. Clinicians make this decision mainly when standard automated perimetry shows that the visual field is getting worse.") with:

> "In practice, the decision to escalate therapy (adding a topical agent, laser trabeculoplasty or filtration surgery) is usually triggered when standard automated perimetry shows that the visual field is getting worse. Software that flags progression earlier therefore promises earlier treatment, but each false flag exposes a patient to the cost, side effects and surgical risk of a treatment that was not needed."

**(c) Add a short Discussion paragraph, "Implications for treatment decisions", placed after the main-finding paragraph.** Every number below is already in Table 3 or `study2_metrics.json`. The time values must be added to Results by script before they appear in Discussion.

> "For a clinician deciding whether to escalate therapy, these results translate as follows. If the trend test is re-applied at every visit, about one in seven eyes whose glaucoma has not changed (15.2%) will be flagged at least once by the sixth field. Requiring confirmation at a second visit lowers this to about one in twenty (5.0%), but 25 of the 97 progressing eyes that the unconfirmed test flagged were no longer flagged by the sixth field. A new detector that reports 'earlier detection' without a stated false-alarm rate cannot be placed on this trade-off, and should not by itself trigger escalation of therapy."

**(d) Report time, not only test number (see C6).** UWHVF clinicians reached the sixth field a median of 5.9 years after the first. "Detection by the sixth test" therefore means years of follow-up. The result file already contains time-to-first-flag values: D1 applied at every review, median 4.5 years among the 97 eyes it flagged; Q2, 5.6 years among 72. These are medians within different subsets and are not comparable as they stand. A properly estimated version, for example cumulative incidence of a first flag against years from the first field, would give a therapy journal its clinically legible outcome: "years until treatment would have been escalated".

### 2.2 Abstract (exact replacement; 300 words or fewer including headings; fixes C4, C5 and C1 wording)

> **Introduction:** Glaucoma therapy is usually escalated after visual-field progression. New detectors, including machine-learning models, report earlier detection, rarely at a stated false-alarm rate. We tested whether any detector beats a trend test of mean sensitivity when all are calibrated to one nominal false-alarm rate.
>
> **Methods:** In this retrospective benchmark of three public data sets, Study 1 evaluated ten detectors on a locked University of Washington test split, using the first 3–6 fields. False alarms were measured on weekly retest series (30 patients) in which glaucoma could not change. Study 2 (new protocol) used 5-fold cross-fitting; 150 progressing and 164 stable eyes, defined by the long-term slope of mean deviation, were evaluated. Seven detectors were calibrated to a nominal 5% false-alarm rate on randomly re-ordered ("shuffled") series from the clinic's own records. An external clinic (263 eyes) tested local recalibration.
>
> **Results:** A LightGBM model thresholded at 95% specificity on labelled stable eyes appeared 22.0 percentage points more sensitive than the trend test at six fields, but flagged 15.3% of no-change retest windows. After shuffle calibration it flagged 2.6% and gained 2.2 points (95% CI −2.9 to 7.1). No calibrated detector or event analysis was significantly more sensitive than the trend test at any number of fields (all upper 95% confidence limits ≤8.4 points). Re-applied at every visit, the trend test flagged 64.7% of progressors and 15.2% of no-change series by the sixth field; requiring confirmation limited false alarms to 5.0% but flagged 47.6%. Externally, local recalibration restored the transferred model's specificity (93.2%) but cut sensitivity to 7.4%.
>
> **Conclusion:** Against a mean-deviation reference, the apparent advantage of a machine-learning detector was explained by its higher false-alarm rate. Progression detectors used to guide escalation of therapy should be compared at a stated false-alarm rate, per visit and over repeated visits.

(Counted at 297 words including headings by our script. The authors must recount after editing. "≤8.4" keeps the manuscript's figure; the result file's maximum is 8.33, so "≤8.4" is true. See C10.)

### 2.3 Key Summary Points (exact replacement; 5 bullets)

**Why carry out this study?**
- Escalation of glaucoma therapy usually follows detection of visual-field progression, and new detectors, including machine-learning models, often report earlier detection than trend analysis.
- These comparisons rarely fix the false-alarm rate, although a false alarm can lead to unnecessary drops, laser or surgery.

**What was learned from the study?**
- A machine-learning detector thresholded on labelled stable eyes appeared 22.0 percentage points more sensitive than a trend test of mean sensitivity at six fields, but flagged 15.3% of retest windows in which glaucoma could not have changed.
- When detectors were calibrated to a nominal 5% false-alarm rate on shuffled series from the clinic's own records, none was significantly more sensitive than the trend test against a mean-deviation reference.
- Reports of earlier progression detection, and software used to guide therapy, should state the false-alarm rate per visit and over repeated visits.

### 2.4 Length: from about 5,000 to about 4,000 words

| Cut | Saving (approx.) |
|---|---|
| Move the D2–D10 definitions to a Supplementary table. Keep one sentence per detector family in the main text. | 350 |
| Move "Study 1 evaluation" E1–E4, amendment A1/A2 detail and the PoPLR secondary-reference detail to the Supplement. Keep two sentences. | 200 |
| Move Table 4 (GRAPE, 16 rows) to the Supplement. Keep 3 numbers in the text. | (table) |
| Cut Table 2 to the four rows clinicians need (D1, S1, S5, B8) at k = 3 and 6, plus a gain-CI column. Move the full 40 rows to the Supplement. | (table) |
| Discussion paragraph 6 (PoPLR pooling, D6 "confirmation rather than discovery"). Condense to two sentences. | 120 |
| Methods "Use of AI tools" repeats Declarations. Keep one full version and cross-reference it. | 60 |
| Statistical analysis: move the validity-rule deviation history to the Supplement. Keep one sentence plus a pointer. | 90 |
| Introduction paragraph 3 (the catalogue of detector families). Halve it. | 90 |

Also rename the hypotheses H6–H9 to H1–H4. Numbering that starts at H6 tells the editor that earlier hypotheses are hidden somewhere.

### 2.5 Figures

- **Fig. 2 (Study 1) → Supplement.** It is the least clinical figure. The point labels overlap ("D5/D1", "D3/D2", and the clipped "0"/"10" at the origin in the 3-test panel). It also shows that the Study 1 LightGBM (D8) at six tests had **3.6% false alarms and 70.8% sensitivity**, better than D1 on both axes (C2). That undercuts the section heading it illustrates.
- **New Fig. 2:** cumulative proportion of eyes flagged against **years** from the first field, for D1 at every visit, Q2 (confirmed), D7 at every visit and B8. One panel for progressors and one for true no-change series. This is the "time to escalation" figure that a therapy journal wants.
- **Fig. 3 (fig5):** the four panels use different x-axis scales (0–0.15, 0–0.25, 0–0.30, 0–0.20). Either use a common axis or state in the legend that the scales differ, as the Fig. 2 legend already does. The phrase "At matched false alarms (shaded band)" is inaccurate, because the band is the nominal ≤5% region and several calibrated detectors sit at about 0% (C1). Change it to "Shaded band: false-alarm rate at or below the nominal 5%."
- **Fig. 4 (fig6):** the legend reads "D1-repeated/D7-repeated", but the text says "applied at every review". Use the text's wording. The Q3 marker at (0.00, 0.13) is clipped by both axes; extend the axes slightly below 0.
- **Fig. 1:** replace "repeated-look" with "repeated reviews" (or "repeated visits"). Replace "E1 reference, E2 true no-change, E3 shuffle audit, E4 external" with plain words. Add the therapy-decision framing: a final box reading "Implication: state the false-alarm rate before a flag triggers escalation of therapy".
- All figures must be supplied as separate TIFF or JPG files at 300 dpi or more (currently PNG).

### 2.6 Cover letter (`cover_letter_filled.md`)

- Paragraph 2: add one sentence on therapy. "Visual-field progression is the usual trigger for escalating glaucoma therapy, so a detector's false-alarm rate translates directly into unnecessary treatment."
- "In two pre-specified studies": Study 2's protocol was written after Study 1's results were known. Say "two studies, each with an analysis plan time-stamped before analysis".
- "a trade-off that clinicians can now choose explicitly" overclaims. Replace with "a trade-off that should be reported for every detector".
- "code and raw outputs are available on request": deposit them (Zenodo/OSF with a DOI) and say so. At triage this one change does more for credibility than anything else in the letter.
- Add a sentence explaining why this journal rather than TVST or Ophthalmology Glaucoma. For example: "Ophthalmology and Therapy readers decide on and evaluate glaucoma treatment, and are the audience most affected by false progression flags from commercial or AI software."
- Add up to three suggested reviewer fields (glaucoma perimetry, biostatistics of progression, ophthalmic AI evaluation), as the guidelines allow.

---

## Part 3. Clinical review (glaucoma clinician-scientist)

### Summary for the editor

The authors compare 10 (Study 1) and 10+4 (Study 2) rules for detecting visual-field progression from the first 3–6 fields. In Study 2 they calibrate each rule's threshold so that it flags 5% of shuffled series, then compare sensitivity against a mean-deviation-slope reference with the trend test of mean sensitivity (D1). The central demonstration is convincing and useful: a LightGBM model with a "95% specificity on stable eyes" threshold looks 18–22 points better at four to six fields while flagging 14–26% of no-change retest windows. The broader claim that "no detector beats the trend test at matched false alarms" is less secure than the abstract implies, for two reasons. First, the false-alarm rates were not actually matched on the data used to judge them (C1). Second, the reference standard is built from the same global trend that D1 measures (C2). There are no fatal flaws, but C1–C6 need to be addressed, and the headline claims need narrowing.

### Claim-by-claim support check (Abstract, KSP, Discussion, Conclusions)

| # | Claim (location) | Supported by Results/Tables? | Verdict |
|---|---|---|---|
| 1 | "Every detector's threshold was set to 5% false alarms on shuffled series" (Abstract, Methods) | No. D1 (p < 0.05), D7 (Study 1 event rule) and B8 (95% spec) were not shuffle-calibrated. | **Incorrect.** C5 |
| 2 | "Across eight shuffle-calibrated detectors" (Abstract) | No. Seven are shuffle-calibrated (S1–S7). The "eight" in Methods are D7 + S1–S7. | **Incorrect.** C5 |
| 3 | B8 +22.0 pp, 15.3% false alarms, k = 6 (Abstract, KSP, Cover) | Table 2 | Supported |
| 4 | S5 calibrated: 2.6% false alarms, +2.2 pp (−2.9 to 7.1) (Abstract) | Table 2 / text, k = 6 | Supported, but **selective**. At k = 3 and 5, S5 was invalid (8.1%, 7.6%), and at k = 5 it was −11.1 pp. C5 |
| 5 | "all upper confidence limits for the gain were below 8.4 points" / "gains of 8.4 pp or more were excluded" (Abstract, KSP, Discussion) | Not shown in any main table: Table 2 has no gain CIs. The result file gives a maximum of 8.33 (S3, k = 4). | Numerically supported. Not verifiable from the paper. Unadjusted CIs across 32 comparisons. C10 |
| 6 | "At matched false alarms, a plain trend test was as sensitive as ML and permutation detectors" (Abstract Conclusion, Conclusions) | Table 2. Realised false alarms of the calibrated detectors were 0.0–8.1% (not matched). No equivalence test was done. S7 was significantly *less* sensitive. | **Overclaim.** C1, C4 |
| 7 | "Apparent gains ... can be explained by higher false-alarm rates" (Abstract), "Disappear" (Title) | Shown for one in-house LightGBM (B8) and for D6 in Study 1. No published detector was re-evaluated. | **Overgeneralised.** C4 |
| 8 | "Controlling cumulative false alarms to 5% reduced detection by the sixth test from 64.7% to 47.6%" (Abstract, Cover) | Table 3 | Supported. Q2's false-alarm CI is 1.0–10.0%. |
| 9 | "local recalibration restored specificity (93.2%) but reduced its sensitivity" (Abstract) | Table 4 | Supported (sensitivity 7.4%, 27 progressors) |
| 10 | "detectors that flagged more eyes raised more false alarms" (Study 1 heading, Fig. 1 Finding 1) | Partly. At k = 6, Study 1 D8 flagged more progressors than D1 (70.8% vs 57.7%) with *fewer* true no-change false alarms (3.6% vs 5.1%; `results/metrics.json`). | **Partly contradicted.** C2, C9 |
| 11 | "The apparent advantage was a choice of operating point, not a better detector" (Discussion paragraph 1) | Consistent with B8 vs S5 at k = 6 only | Overclaim. Rephrase as "in our data, largely". C4 |
| 12 | "Shuffle calibration ... brought ML false alarms close to the target ... simple enough for any clinic or software vendor to apply" (Discussion paragraph 2) | S5 exceeded the validity rule at k = 3 and 5. The shuffle audit tracked true false alarms only moderately (ρ = 0.65). In GRAPE, local calibration with 263 eyes cut ML sensitivity to 7.4%. | **Overclaim.** C7 |
| 13 | "a well-calibrated linear trend appears to capture most of the available signal" (Discussion paragraph 3) | Only against a mean-deviation-slope reference. | Conditional. C2 |
| 14 | "More tests early ... or risk-guided scheduling ... are therefore more promising" (Discussion paragraph 3) | Not tested. The authors say so, but "therefore" implies it follows from their results. | Mild overclaim. Change to "may be more promising". |
| 15 | "missed 25 of the 97 progressors that the unconfirmed test found" (Discussion paragraph 4) | Not in any table. The result file gives Q2 flagging 72 eyes, all of them also flagged by D1 (only_D1 = 25), which is 48.0%. Table 3 says 47.6% / −17.1 pp. | Supported by the data file but inconsistent with Table 3 rounding. C13 |
| 16 | "the plain trend test kept its performance without any recalibration" (Discussion paragraph 5) | Table 4: D1 44.4% (k = 3), 33.3% (k = 4) against a label partly built from the same tests | Weakly supported. C8 |
| 17 | "Transferring a complex detector is therefore riskier than transferring a simple one" (Discussion paragraph 5) | One model, one external site, 27 progressors | Overgeneralised. C8 |
| 18 | "the conclusions hold under the strict rule" (Limitations) | Supplement only | Not checkable in main text. Acceptable if the Supplement shows it. |
| 19 | "Across two studies, three data sources and 21 detector variants" (Conclusions) | Count is 10 (Study 1) + 7 (S1–S7) + B8 + 4 (Q1–Q4) = 22, or 21 if B8 is counted as D8 | Clarify. C14 |
| 20 | "mostly with early to moderate damage" (Limitations, Artes) | Table 1 gives only mean sensitivity (26.9 dB). Mean deviation is "not available". | Unsupported in the paper. Cite [11] or remove. C11 |

### Numbered issues

**C1. MAJOR: "Matched false alarms" were nominal, not achieved, so the main comparison is not at a common operating point.**
Quote: "At matched false alarms, no detector was significantly more sensitive than D1 at any number of tests."
Calibration matched *shuffled-series* flag rates in the calibration eyes. On the two data sets that judge specificity, the calibrated detectors were far from matched. True no-change false alarms ranged from 0.0% (S4) and 0.1–0.5% (S3) to 8.1% (S5, k = 3). Flat-stable (R2) specificity ranged from 88.5% (S3, k = 4) to 99.1% (S4, k = 6). Many of the "significantly less sensitive" results (S2, S4, S7) are therefore partly the result of conservative operating points, not weaker detectors. The opposite reading is also possible: S3 (pooled PoPLR) matched D1's sensitivity at k = 3–5 while raising 0.1–0.5% false alarms on true no-change data against D1's 3.9–4.5%. On that axis S3 arguably *beats* D1, yet its R2 specificity was lower (88.5–92.3%). The paper does not discuss this disagreement between its two specificity yardsticks, and it bears directly on which detector a clinic should use.
Fix: (i) Throughout, replace "matched false alarms" with "calibrated to a nominal 5% false-alarm rate". (ii) Add a sensitivity analysis at a truly common operating point, for example sensitivity at R2 specificity fixed at 95% for score-based detectors (the scores exist), or partial ROC curves on R2. Report whether H7 still fails. (iii) Discuss the S3 discrepancy in one paragraph.

**C2. MAJOR: The reference standard favours the trend test, and the one non-mean-deviation reference was dropped in Study 2.**
Quote: "An eye was a progressor if the slope of mean total deviation over all its tests was worse than −0.3 dB per year with a one-sided p < 0.01."
D1 is the slope of mean sensitivity over the first k of the same fields. The reference is therefore essentially D1 run on the full series, so incorporation and construct overlap favour D1. The R3 future-only reference reduces this but has 95 progressors at k = 3 and only 34 at k = 6. Its specificities are also low for everyone: 82.2% for D1 at k = 6 and 60.3% for B8 (`study2_metrics.json`). In Study 1, under the PoPLR (pointwise) reference at k = 6, D8 (42.1%) and D10 (43.1%) were numerically above D1 (37.9%) (`metrics.json`). Localised progression is exactly where pointwise and ML methods are expected to help, and Study 2 does not test it. The Limitations paragraph acknowledges the bias but asserts that the conclusions are unchanged, which cannot be checked for a pointwise reference in Study 2.
Fix: compute the PoPLR whole-series reference (already implemented for Study 1) in the Study 2 cross-fitted eyes, and report Table 2's key rows against it. Restrict the Title, Abstract and Conclusions to "progression defined by the mean-deviation slope" unless that analysis agrees.

**C3. MAJOR: Spectrum bias. More than half of the eligible eyes were excluded from the accuracy analysis.**
Quote: "Of 690 eyes of 379 patients with at least eight tests, 150 were progressors and 164 were stable."
376 of 690 eyes (54%) were "indeterminate" and were not evaluated. The progressors had strong evidence (p < 0.01), and the R1-stable eyes had flat or improving slopes. Early detection matters most in exactly the excluded middle group, where a better detector could separate slow from fast progressors. A two-extremes design usually inflates sensitivity and specificity for every detector, and can hide differences between them.
Fix: report flag rates in indeterminate eyes, stratified by full-series slope (for example < −0.3, −0.3 to 0, > 0 dB/yr), or use a continuous reference (correlation of the k-test score with the full-series slope). Add spectrum bias to the Limitations.

**C4. MAJOR: The headline claims overgeneralise from a single in-house model to "new detectors" in general.**
Quotes: Title "Apparent Gains ... Disappear"; Abstract "Apparent gains in early detection ... can be explained by higher false-alarm rates"; Discussion "The apparent advantage was a choice of operating point, not a better detector"; Limitations "our results predict that their advantages will shrink at matched false alarms".
The paper re-evaluates no published detector. The inflation is shown for one LightGBM with one thresholding rule (B8) and one conformal variant (D6). Moreover, in Study 1 the same LightGBM rule at k = 6 had 3.6% false alarms (C9), so the inflation is not even stable across training runs. "As sensitive as" asserts equivalence that was not tested: the confidence intervals go down to −36.7 pp, and S7 was significantly worse.
Fix: use the title in 2.1(a). Replace "as sensitive as" with "no more sensitive than". Change the Limitations sentence to: "Shuffle calibration can be applied to any of them; whether their advantages persist at a stated false-alarm rate is untested."

**C5. MAJOR: The Abstract contains factual errors and a selective example.**
(a) "Every detector's threshold was set to 5% false alarms on shuffled series" is wrong for D1, D7 and B8. (b) "eight shuffle-calibrated detectors" should be seven calibrated detectors plus event analysis. (c) The calibrated-LightGBM example uses k = 6, its best case. At k = 3 and 5 it failed the validity rule (8.1%, 7.6%), and at k = 5 it was 11.1 points *less* sensitive than D1.
Fix: the replacement Abstract in 2.2 corrects (a) and (b). For (c), add to Results: "At three and five tests, calibrated LightGBM exceeded the validity rule (8.1% and 7.6%)."

**C6. MAJOR (clinical relevance): The outcome is counted in tests, not time, and the link to treatment is not analysed.**
Quote: "In routine care, the third test came a median of 2.1 years after the first, and the sixth a median of 5.9 years after the first."
"Detection at six tests" in this cohort means roughly six years. A trade-off stated in test numbers (64.7% vs 47.6%) cannot be translated into "how much later would I escalate therapy". The time-to-first-flag analysis is in the result files but not reported (D1 at every review: median 4.5 y among 97 flagged; Q2: 5.6 y among 72). There is also no estimate of what a false alarm costs (extra visits, escalation), which is the whole rationale given in the Introduction.
Fix: add time-to-first-flag as cumulative incidence against years, for progressors and for no-change series (Fig. suggestion in 2.5). Add the "implications for treatment decisions" paragraph (2.1c). State in the Limitations that the consequences of treatment were not modelled; this is already there, so keep it.

**C7. MODERATE: Shuffle calibration is presented as more validated and portable than the data show.**
Quote: "It is simple enough for any clinic or software vendor to apply."
The shuffle audit tracked true false alarms only moderately (ρ = 0.65; 80% of cells within 3 pp). Calibrated LightGBM still exceeded the validity rule at two of four k values. Shuffling breaks real-world non-stationarity: learning effects, cataract and changes in reliability all produce real trends that are not progression, so shuffled-series false alarms are likely to underestimate clinic false alarms. In GRAPE, local recalibration on 263 eyes left calibrated LightGBM with 7.4% sensitivity.
Fix: change to "It needs no retest study or labels and can be applied to a clinic's existing records, although its accuracy depends on the number of eyes available and was imperfect in our data (ρ = 0.65)." Add the learning-effect and cataract point to the Limitations.

**C8. MODERATE: External-clinic inferences rest on 27 progressors and a label built from the same fields.**
Quote: "For 100 GRAPE eyes with only three visits, the labels were based on the same tests that the detectors saw."
D1's sensitivity *falls* from 44.4% at k = 3 to 33.3% at k = 4. That pattern is consistent with incorporation bias at k = 3. Table 4 does not give the denominators at k = 4. "Transferring a complex detector is therefore riskier than transferring a simple one" generalises from one model and one site.
Fix: give n (progressors/non-progressors) for each k in Table 4. Repeat Table 4 for the eyes with at least 4 visits only. Soften to "In our data, the transferred machine-learning model needed local recalibration and then lost sensitivity, whereas the trend test did not."

**C9. MODERATE: The Study 1 results are not fully described, and they conflict with the Study 2 instability of B8.**
Quote: "LightGBM thresholded at 95% specificity raised false alarms in 27.7% at three tests and 18.8% at five tests."
At six tests the same Study 1 model had 3.6% true no-change false alarms and 70.8% sensitivity (vs D1 5.1% / 57.7%). The heading "detectors that flagged more eyes raised more false alarms" omits this. The large swing in B8's false-alarm rate (3.6% in Study 1 vs 15.3% in Study 2 at k = 6) is itself an argument for the paper's thesis: a labelled-stable threshold does not control false alarms reliably. But the swing has to be reported, not left out.
Fix: report all four k values for D8 in the text, and add: "The false-alarm rate of the usual-threshold model was unstable across training sets (3.6% in Study 1 and 15.3% in Study 2 at six tests)."

**C10. MODERATE: The gain CIs and multiplicity are not shown or reconciled.**
Table 2 gives CIs for sensitivity but not for the paired gain. Readers therefore cannot check "upper limits ≤ 8.4 pp". The S1 gain at k = 4 has a 95% CI of 0.7 to 5.3, which excludes zero, yet its Holm p = 0.12. The paper does not explain the difference between the bootstrap CI and the McNemar test (majority flag across seeds vs means over seeds). The "8.4 excluded" statement uses 32 unadjusted 95% CIs.
Fix: add a "Gain, pp (95% CI)" column. Explain the CI/p discrepancy in a footnote. Either describe the exclusion as per-comparison or give simultaneous (for example Bonferroni-adjusted) limits.

**C11. MODERATE: The true no-change arm is small, short-term, and its unit is described inconsistently.**
Quotes: "raised false alarms in 15.3% of true no-change series"; "30 patients, mostly with early to moderate damage".
The per-review false-alarm rates are shares of overlapping k-test *windows* with borrowed test dates (ten draws each), not of series. The CIs look narrow for 30 clusters (for example D1 k = 3, 4.2%, 2.8–5.7). Please confirm that the bootstrap resampled the 30 patients with all their windows and date draws. "Early to moderate damage" is not supported in the paper (Table 1: mean deviation not available).
Fix: use "retest windows" for per-review results and keep "series" for repeated-review results. State the severity of the Artes cohort with a citation to [11], or delete the phrase.

**C12. MODERATE: H8 is designed to fail, and the event-analysis result goes undiscussed.**
H8 asks whether detectors held to about 5% cumulative false alarms are non-inferior to D1 running at about 15% cumulative false alarms. Rejecting it is close to inevitable and says little. The informative comparison is between detectors at similar cumulative false-alarm rates. Here, D7 applied at every review flagged 46.0% of progressors with 2.0% false alarms, against Q2's 47.6% with 5.0%. The (simplified) event analysis was thus at least as good as the confirmed trend test for repeated reviews. That sits awkwardly with the "plain trend test" message and deserves a sentence. The authors rightly note that D7 is not GPA, which is the event analysis clinicians actually use.
Fix: rephrase H8 in the Discussion as a trade-off, not a test. Add the D7-versus-Q2 comparison. Recommend GPA validation explicitly.

**C13. MINOR: Rounding inconsistencies in the repeated-review results.**
Table 3 reports Q2 at 47.6% and −17.1 pp. The result file has 72/150 flagged, which is 48.0%; the 97 − 72 = 25 eyes cited in the Discussion corresponds to −16.7 pp. The table values appear to be means over folds rather than pooled proportions. State this in the Table 3 footnote, or report pooled proportions, so that "25 of the 97" matches the table.

**C14. MINOR: The detector count is unclear.**
"21 detector variants" (Conclusions): list them in the Supplement, or say "ten Study 1 and twelve Study 2 detectors".

**C15. MINOR: The Study 2 LightGBM is described as "the Study 1 ... model" but is refit.**
Quote: "S5, the Study 1 gradient-boosted-tree model (LightGBM)". In `code/study2.py` the model is re-fitted within each fold (`LGBLabel(seed).fit(fit_e, sel_e)`), which is correct for leakage. Say "the Study 1 LightGBM specification, re-fitted within each fold". The same applies to S7 and B8.

**C16. MINOR: The trend test uses uncorrected mean sensitivity, while the reference uses total deviation.**
D1 regresses raw mean sensitivity, which includes normal ageing of about −0.1 dB/yr, whereas the reference uses the age-corrected mean TD. State why. Clinicians will ask why MD or VFI was not used, since those are what perimeter software shows. One sentence plus a supplementary check with mean TD would settle it.

**C17. MINOR: Table formatting.**
- Table 2: Holm p shown as "0.00" (S4 k = 4, S6 k = 4, S2 k = 5). Use "<0.01" or three decimals.
- Table 1: the rows "Mean sensitivity ... not shown" are confusing. Drop the row or fill it.
- Table 4 footnote: "Means over UWHVF folds and seeds" does not apply to the deterministic D1.

**C18. MINOR: Nomenclature overload.**
D1–D10, S1–S7, B8, Q1–Q4, R1–R3, E1–E4, A1–A2 and H6–H9 appear together. Use descriptive names in the main text ("trend test", "calibrated LightGBM", "usual-threshold LightGBM", "confirmed trend test") and keep codes for the tables.

**C19. MINOR: Reference details.**
- Ref 22 is a medRxiv preprint posted about a week before submission. Label it as a non-peer-reviewed preprint in the text, or drop it; ref 35 supports the same point.
- Journal abbreviations end in a double period ("Trans. Vis. Sci. Tech..", "Invest. Ophthalmol. Vis. Sci..", "Ann. Appl. Stat.."). Use NLM abbreviations without punctuation, per Vancouver style.
- The UWHVF eye-count discrepancy (7,428 counted vs 7,248 reported) is correctly flagged in the text. Keep it.

**C20. MINOR: Plain Language Summary.**
"Once false alarms were matched, no method found more worsening than the simplest one" repeats the C1/C4 overclaim. Change to "Once every method was set to the same target number of false alarms, none found clearly more worsening than the simplest one." Also, "more than 300 eyes" should say "314 eyes".

**C21. MINOR: Data availability.**
"available from the corresponding author on reasonable request" is weak for a fully public-data, scripted analysis. Deposit the code, protocols, split files and raw detector outputs with a DOI. This also addresses desk-reason 3.

### Recommendation (as reviewer)

**Major revision.** The central lesson is sound and clinically useful: thresholds set on labelled stable eyes can produce false-alarm-driven "gains", and detectors should be reported at a stated false-alarm rate, per visit and cumulatively. The broader claim that a plain trend test is as good as everything else needs either a truly matched operating point (C1) and a non-mean-deviation reference in Study 2 (C2), or narrower wording throughout (C4). The paper would also be much more relevant to this journal if detection were expressed in years and tied to the decision to escalate therapy (C6).
