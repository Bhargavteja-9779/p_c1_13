# Review 01 — Glaucoma clinician-scientist

**Manuscript:** "How Early Can Glaucomatous Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm" (Ophthalmology and Therapy, Original Research)

**Recommendation:** Major revision. The paper has value if reframed. In its current form it is not a therapy paper, and its clinical conclusions go further than the data allow.

## Summary

The authors compare ten visual-field (VF) progression detectors on their first 3–6 tests. Sensitivity is measured against a full-series mean-total-deviation (MTD) slope reference in 26 progressing and 26 stable UWHVF eyes. False alarms are measured on the 30-patient Artes weekly retest series, and the authors also report agreement with algorithmic labels in GRAPE. They conclude that an ordinary least-squares trend of mean sensitivity is "as good as any valid alternative" and that new detectors should report true no-change false alarms "before they guide treatment escalation". The emphasis on false alarms is useful to clinicians. However, the reference standard is built in a way that favours the comparator, the stable class is defined as eyes whose slope was positive, the external "clinician labels" are computed from the same tests the detectors see, and the treatment-escalation framing is not supported by any treatment data.

## Issues

### 1. MAJOR — The "stable" reference class is eyes with an improving slope, not stable eyes
**Location:** Methods, Reference standard: "An eye was stable if the one-sided p was above 0.5." Discussion: "Reference-stable eyes are selected because their long-term course is flat".
**Problem:** In the code (`code/src/models/deferral.py::ols`, `p = stats.t.cdf(b / se)`), a one-sided p > 0.5 means the estimated full-series slope is **positive**. The negative class is therefore eyes that got better over 8–12+ years, typically through learning effects, cataract surgery or noise. These eyes are not representative of stable glaucoma, and an early trend detector will almost never flag them. This explains why specificity is ≥91.5% everywhere and 100% for most detectors from k = 4. It also means the specificity part of E1 says nothing about clinical specificity. The Discussion's "flat" description is wrong.
**Fix:** State plainly that "stable" means a non-negative estimated full-series slope. Add a sensitivity analysis with a clinically defined stable class, such as |slope| < 0.2 dB/yr with a narrow CI, or slope > −0.1 dB/yr. Change "flat" to "non-declining or improving" in the Discussion. Report how many stable eyes had a positive slope above +0.2 dB/yr.

### 2. MAJOR — Incorporation bias: the reference includes the very tests being judged and uses the same quantity as D1
**Location:** "For eyes with at least eight tests, we defined a future-confirmed reference from the whole series." Limitation: "Second, the primary reference was based on mean deviation, which may favour detectors based on mean sensitivity, such as D1."
**Problem:** The reference slope uses all tests, including tests 1..k. With a median of 9 tests in stable eyes and 12 in progressors, the first 6 tests make up half to two-thirds of the data that define the label at k = 6. Calling the reference "future-confirmed" is inaccurate. The limitation sentence understates the problem: the bias comes not only from the shared MD basis but from shared data points.
**Fix:** Define the reference on tests k+1..end only (a truly *future* reference) and rerun E1. At minimum, add that analysis as a sensitivity analysis and stop using the word "future-confirmed" unless the reference excludes the first k tests.

### 3. MAJOR — GRAPE labels are algorithmic criteria computed on the same short series, not clinicians' judgement
**Location:** Abstract: "agreement with clinician labels in an external clinic (263 eyes)". Results: "compared flags with the clinicians' labels"; "eyes labelled as progressing by the clinicians' mean-deviation criterion". Fig. 4 axis: "1 - specificity (clinician label)".
**Problem:** The Methods say that GRAPE labels were "assigned with three criteria (mean deviation, and two pointwise linear regression rules)". These are rule-based labels, not clinical decisions. GRAPE eyes have a median of 4 visits, and `descriptives.json` shows `eyes_ge3 = 263` but `eyes_ge4 = 163`. So 100 eyes have exactly 3 visits, and for them the k = 3 detectors see the **entire** series from which the MD label was computed. The external sensitivity and specificity of D1, D2 and D5 (all MD-slope rules) are therefore largely agreement between an MD slope and an MD-slope criterion on the same data. The headline external contrast, "gradient-boosted trees had a specificity of 61.2%, compared with 95.3% for the trend test", is confounded by this.
**Fix:** Replace "clinician labels" with "criterion-based labels" throughout, including in the abstract and figures. Restrict E4 to eyes with ≥ k+2 visits, so that the label depends on later tests, or recompute the MD criterion from tests after k. Report the 3-visit subgroup separately.

### 4. MAJOR — The treatment-escalation framing is not supported by the study, and scope fit with a therapy journal is weak
**Location:** Abstract Conclusion: "before they guide treatment escalation". KSP: "Escalating glaucoma treatment depends on detecting visual-field progression". Discussion: "For treatment decisions, these results matter in a direct way. A false progression flag can lead to additional drops, laser or surgery, with side effects and costs [2, 3]."
**Problem:** No treatment, IOP, target-pressure or structural (OCT) data were used. In practice, escalation is rarely triggered by a single unconfirmed VF flag: clinicians confirm progression, look at IOP and OCT, and weigh life expectancy. Treating each flag at one review as a potential escalation exaggerates the harm. The limitation "we did not measure the clinical consequences of false alarms" is correct, but the abstract and conclusion then assume those consequences.
**Fix:** Present the escalation link as motivation, not as a result. Add a paragraph on how detector flags enter escalation decisions (confirmation testing, structure–function concordance). Remove "in a direct way". In the cover letter, state the scope fit explicitly (monitoring that decides therapy), or consider a methods/diagnostics journal.

### 5. MAJOR — "As good as any valid alternative" ignores that event analysis had a much lower false-alarm rate at similar sensitivity
**Location:** Abstract Conclusion: "A plain trend test of mean sensitivity remained as good as any valid alternative." Conclusions: "a plain trend test of mean sensitivity was as good as any detector that kept false alarms at the nominal level".
**Problem:** Table 2 shows D7 (event analysis) at k = 5: sensitivity 50.0% vs 42.3% for D1, with true no-change false alarms of 1.2% vs 4.7%. At k = 6: 57.7% vs 57.7%, with 1.9% vs 5.1%. In clinical units that is about 19 vs 51 false flags per 1,000 stable eyes at equal sensitivity. On both axes the GPA-like rule is at least as good as D1 from k ≥ 5, and the paper's own framing values false alarms. D2 at k = 3 (38.5% vs 19.2%, false alarms 2.6% vs 4.4%) points the same way. The "as good as" claim is also an equivalence claim drawn from non-significant tests in 26 eyes (see Review 02).
**Fix:** Replace the claim with something the data support, for example: "No detector with a valid false-alarm rate was significantly more sensitive than the trend test; event analysis had similar sensitivity with fewer false alarms from five tests." Discuss D7's lower false-alarm rate as a clinically relevant trade-off.

### 6. MAJOR — The cumulative (multi-review) false-alarm burden is not reported, yet the paper reports cumulative sensitivity
**Location:** "In clinical units, D1 raised about 44 false progression flags per 1,000 stable eyes at a review based on three tests." "By the sixth test, D1 had flagged 69% of reference progressors."
**Problem:** The 69% figure is cumulative over reviews at k = 3, 4, 5 and 6 (`detected_by6_mean = 0.692`), while every false-alarm figure is per single review. In a clinic, a stable patient is reviewed at every visit, so the cumulative false-alarm probability over four looks is the number that matters for escalation, and for D1 it could be about 10–15%. The comparison as presented is lopsided, and it favours "more tests" messaging.
**Fix:** Compute the cumulative probability of at least one false flag across k = 3..6 on the Artes windows (consecutive windows within one series) for each detector. Report it next to the 69%, 78% and 77% figures.

### 7. MODERATE — The title says "glaucomatous", but UWHVF has no diagnoses and the reference uses non-specific global loss
**Location:** Title: "How Early Can Glaucomatous Visual-Field Progression Be Detected". Limitation: "Fourth, UWHVF does not include diagnoses or reliability indices, so some eyes may not have glaucoma".
**Problem:** The reference is the slope of unweighted mean TD. That slope is driven by diffuse loss (cataract, media opacity) as much as by glaucoma, and GPA-style pattern-deviation methods were designed to exclude exactly this. Progressors may include cataract and neurological cases. The title and the KSPs assert glaucoma throughout.
**Fix:** Change the title to "visual-field progression in a glaucoma clinic population" or similar. Add a sensitivity analysis using a pattern-deviation (PD) or PSD-based reference, or require concordant local loss.

### 8. MODERATE — The time scale of "early" detection is not clinically early, and the message should say so
**Location:** "With routine spacing in UWHVF, the third test of reference eyes was done a median of 2.3 years (progressors) ... and the sixth test a median of 6.3 and 7.3 years after the first."
**Problem:** "Three tests" here means about 2.3 years, and "six tests" means about 6–7 years. D1 sensitivity of 57.7% at about 6.3 years means 42% of eventual fast progressors are still unflagged after more than 6 years. That is a key clinical message (missed progression), and the paper underplays it because it focuses on false alarms.
**Fix:** Report sensitivity against time from baseline as well as k, and state the missed-progression burden explicitly in the Discussion and the KSPs.

### 9. MODERATE — The Artes cohort has early damage, which limits what the false-alarm rates mean clinically
**Location:** "the true no-change arm had only 30 patients, mostly with early to moderate damage".
**Problem:** The median mean sensitivity is 26.9 dB, which is early disease. False alarms per 1,000 "stable eyes" are extrapolated to all stable eyes, including advanced eyes, where variability is much higher [4]. The statement "mostly with early to moderate damage" is stronger than the data, because no MD or stage distribution is reported.
**Fix:** Report Artes MD (with normative TD) and a stage distribution. Qualify the per-1,000 numbers as applying to early glaucoma.

### 10. MINOR — "Expert guidance suggests six tests in the first two years [5]" is presented as current standard care
**Location:** Introduction paragraph 2.
**Fix:** Note that this is the 2008 Chauhan et al. recommendation and is rarely met. Cite contemporary data (e.g., [33]) for actual testing frequency.

### 11. MINOR — The D2 "fast progression" rule is presented without clinical context
**Location:** "D2 MD rate: slope of mean sensitivity of −1 dB per year or worse (a common "fast progression" rule, no p-value)."
**Fix:** Cite a source for the −1 dB/yr threshold. Also note that clinicians usually apply it to longer series (≥5 tests), which explains its high shuffle-audit rate at k = 3.

### 12. MINOR — Fig. 1 misrepresents the flow of data
**Location:** Fig. 1 (arrow from "Artes retest (Halifax)" into the "10 detectors" box).
**Problem:** The arrow implies that the Artes data were used to develop or fit detectors. Under the stated design they are evaluation-only, although see Review 02 on their development use.
**Fix:** Point the Artes arrow to E2 only, and give E3 and E4 separate boxes.
