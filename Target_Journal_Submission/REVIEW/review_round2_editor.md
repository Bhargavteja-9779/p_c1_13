# Editor desk check, round 2: *Ophthalmology and Therapy*

**Manuscript:** "Shuffle Calibration Controls False Alarms of Glaucoma Visual Field Progression Detectors: A Benchmark With a True No-Change Arm" (Original Research)
**Checked:** manuscript_filled.md, cover_letter_filled.md, fig1–fig5 (PNG), results/metrics.json, statistics.json, a3_summary.json, posthoc.json, descriptives.json, code/experiments/protocol.md, journal_level_profile.md and journal_benchmark.csv. Five DOIs were checked on Crossref (refs 9, 22, 24, 33 and 35).

---

## 1. Desk decision

**Decision: SEND TO REVIEW, but only after a pre-review technical revision (items R1–R5 below). If the editorial office must send it out as submitted, my decision is DESK REJECT.**

The science is acceptable for this journal. It uses public data with a held-out split, a true no-change arm, an external data set and paired tests with confidence intervals, and its clinical message (with few fields every detector misses most progression, and ML flags should not trigger escalation unchecked) is relevant to treatment decisions. Four things would make a reviewer, or me, reject it now:
- The headline is causally overclaimed.
- An exploratory post-review analysis is called "pre-specified".
- The abstract leaves out the cost of the proposed fix.
- The paper reads as a statistics-methods paper rather than a paper about therapy decisions.

All four can be fixed by rewording and restructuring. No new data are needed.

**The three sentences to the authors:**

> Your benchmark asks a question that matters for treatment escalation in glaucoma, and the true no-change arm with external testing is a strength we rarely see in this journal; however, in its present form the manuscript overstates its central claim ("the apparent early-detection gains were false alarms", "direct evidence"), describes the post-review amendment A3 as "pre-specified" although your own protocol labels it exploratory and post-review, and omits from the Abstract that shuffle calibration made the calibrated detectors significantly *less* sensitive than the trend test in the external data set. Before we invite reviewers, please reframe the paper around the clinical decision (title, research questions and a clinical-implication table), report the calibration results as exploratory with their sensitivity cost, apply one validity rule throughout, and bring the main text to about 4,000 words with at most four figures and three to four tables. With these changes, which need no new data, we will send the manuscript to review promptly.

---

## 2. Desk-rejection risks, ranked, with fixes that need no new data

### R1. The paper reads as a methods paper, outside the journal's applied and therapy scope (highest risk)
The title leads with a statistical technique ("Shuffle Calibration Controls False Alarms…"). The text uses RQ1–RQ6, H2–H8, D1–D10, E1–E4 and A1–A3 codes. The journal profile itself warns: "Rarely new methodology… the risk is scope (must be framed around therapy/monitoring decisions, not as pure methods)."
**Fix:**
- Retitle around the decision. Example: *"How Early Can Visual Field Progression Be Flagged Before Escalating Glaucoma Treatment? False Alarms of Ten Detectors in a Benchmark With a True No-Change Arm and External Validation."*
- In the main text, replace detector codes with short names (trend test, MD-rate rule, ML model and so on) and keep the codes only in tables. Replace the six RQs and seven hypotheses with three plain questions: (i) false alarms, (ii) sensitivity at equal false alarms, (iii) can a clinic set thresholds locally. Move the hypothesis bookkeeping to the supplement.
- Add **Table 4, "Clinical implications at 3 fields"**. One row per detector, with columns for:
  - progressors flagged per 100;
  - false flags per 1,000 stable eyes (from false_flags_per_1000);
  - share of no-change series flagged at least once across 3–6 reviews (posthoc P2);
  - PPV at 10% prevalence (posthoc P3);
  - real elapsed time to the 3rd field in UWHVF (about 2.6 years at a median 1.3-year interval);
  - a one-line "use before escalation?" verdict.
  All of these values already exist in the result files.

### R2. Central claim overclaimed: "The apparent early-detection gains were false alarms"
These phrases appear in the Abstract, the Conclusion, Discussion paragraph 1 ("This is direct evidence that…") and the cover letter. The data do not support them as written:
- Only one nominal gain was statistically significant: D6 at 3 fields (+38 pts, Holm p = 0.018 within k, 0.070 across k). D6's Artes false-alarm rate is also not independent, because it was measured during development.
- D8's gain at 3 fields was +7.7 pts (95% CI −10 to +27, p = 0.69). It was never a demonstrated gain.
- D2 (MD-rate rule) gained +19 pts at 3 fields with a **valid** true no-change false-alarm rate of 2.6% (CI 1.5–3.9). Its posthoc PPV at 10% prevalence is the highest of any detector (62% vs 33% for D1; posthoc.json P3). Calibration removed that gain by pushing D2's false-alarm rate to **0.3%** (threshold slope of about −2.4 dB/yr) and its sensitivity to **4%**. That is over-conservative calibration, not removal of false alarms.
- Calibration also left D8 at 6 fields with 2.2% false alarms and D6 at 6 fields essentially unchanged (7.6% nominal, 7.7% calibrated).

**Fix:** Replace the claim with: *"Once every detector was held to the same false-alarm level, none showed a significant sensitivity advantage over the trend test; the largest nominal gains came with false-alarm rates of 22–28% on no-change series."* Delete "direct evidence". Add one sentence acknowledging that shuffled clinic series contain real progressors and long-term fluctuation, so shuffle calibration can be conservative (D2: 0.3%).

### R3. Provenance of amendment A3 is misdescribed
- The Abstract says "In a **pre-specified** amendment". The Introduction says "we added a pre-specified amendment". The Methods say "pre-specified post-review analyses".
- protocol.md says: *"Status: exploratory, post-review… prompted by simulated review."* The manuscript calls this an "internal review".
- The detectors chosen for calibration (D2, D6, D8, D9) were selected *because* their nominal results "proved invalid". That selection depends on the results.
- The whole protocol and all three amendments carry the same date (2026-11-23).

**Fix:**
- Use "exploratory analysis, specified in writing before it was run, after review of the main results" everywhere, and drop "pre-specified" from the Abstract and the Introduction.
- Describe the nature of the review truthfully and in the same words as the protocol. If it was an AI-simulated review, say so.
- State that the choice of detectors depended on the results.
- Give the protocol dates in the Methods.
- Restructure the Results so that the confirmatory analyses (RQ1–RQ5) come first, under a clear "Exploratory analyses" heading for A3.

### R4. Calibration's sensitivity cost is hidden, and "near the nominal level" is untrue for several cells
The Abstract and the cover letter report only "external specificity 61% to 95%". In GRAPE, calibrated D8 sensitivity fell to **10%** against 44% for D1 (paired −33 pts, 95% CI −52 to −17, Holm p = 0.008, a significant *loss*), and calibrated D2 fell to 19% (−26 pts, p = 0.09). The Abstract's "keep false alarms near the nominal level" does not hold for D2 (0.3–0.7%) or D8 at 6 fields (2.2%).
**Fix:**
- Say "at or below 5%" instead of "near the nominal level".
- Add to the Abstract: *"…but calibrated detectors flagged fewer labelled progressors than the trend test (machine learning 10% vs 44%)."*
- Make the same changes in the Key Summary Points, the Plain Language Summary and the cover letter.
- Replace or extend the Fig. 5 GRAPE panel so that it shows sensitivity next to specificity.

### R5. Non-significance presented as equivalence
With 26 progressors, the CIs include large gains (calibrated D8 at 6 fields: +8 pts, 95% CI −13 to +28). The Key Summary Point "no detector was significantly more sensitive than the simple trend test" will be read as "no better".
**Fix:**
- Report the paired difference and CI wherever a gain is denied.
- Add: "the study could not exclude gains of up to about 25–40 points".
- In the Key Summary Points, change the wording to "showed no significant advantage (small reference set)".

### R6. Two validity rules give inconsistent counts
- The text says false alarms were "clearly above 5%" in 5 combinations and that "machine-learning models exceeded 5% clearly in 4 of 8".
- The Table 2 daggers ("upper >10% or lower >5%") mark **8** invalid combinations, **6** of them ML: D8 at 3/4/5 fields and D9 at 3/5/6 fields.
- The audit section uses the dagger rule ("7 of 8 invalid combinations").
- The rule was "made exact after the main results were available".

The results sentence "False alarms were clearly above 5% for D6 (3 fields), D8 (3 fields), D9 (3 fields), D8 (4 fields), D8 (5 fields)" also reads like unedited script output.
**Fix:** Use one rule (the dagger rule) throughout the main text, rewrite that sentence in prose, and put the strict rule (16/40 qualified) in the supplement.

### R7. A non-independent result headlines the Abstract
D6's 22.4% Artes false-alarm rate was already known from development (Methods and leakage audit). Yet "22.4%" is the first number in the Abstract, the Key Summary Points and the cover letter.
**Fix:** Lead with D8's 27.7% (an independent result). Mention D6 with "(known from development)", or drop it from the Abstract.

### R8. Length and display items exceed the journal norm
Main text prose, from the Introduction to the Conclusion and excluding tables, is about **4,260 words**, or about 4,800 with tables. The submission has 5 figures and 3 tables, against a journal median of about 3,900 words and 3 figures and 3 tables (ML subgroup 3,949 words, 3.5 / 3.5).
**Fix:** Make the cuts in section 4 below. Move Fig. 3 (audit) and Table 3 (GRAPE) to the supplement and add the clinical table (Table 4).

### R9. The clinical time scale is missing from the Abstract and Key Summary Points
"Three fields" sounds like months, but in UWHVF it is a median of about 2.6 years (interval 1.3 years; six fields took 6.5 years).
**Fix:** Add "(UWHVF median 1.3 years between fields)" to the Abstract Methods. Express the key result in years in one Key Summary Point.

### R10. Code "on request" for a benchmark paper
The journal profile's own target was "full repository". Reviewers of a benchmark will ask for the code.
**Fix:** Deposit the code, the protocol with its dated amendments, and the per-eye flag files in a public archive with a DOI, and change the Code and Data Availability statements. This needs no new data.

### R11. Minor factual inconsistencies in the lay texts
- The Plain Language Summary and cover letter say patients were "tested every week for 12 weeks", but one series spanned 524 days (Methods). Say "about weekly (median span 84 days)".
- The Plain Language Summary claims data "from the USA, Canada and China". That is correct, but it also says the fix worked "in a clinic using a different machine" without saying that sensitivity fell there.

---

## 3. Numbers, claims and citation contexts checked against the result files

### Numbers verified correct
I recomputed or read the following from the JSON files and found them consistent with the text:
- **Table 2 and nominal metrics:** every cell in Table 2; D1 false-alarm rates of 4.4/3.8/4.7/5.1%; D6 22.4% (19.3–25.7); D8 27.7% (22.7–32.9); D9 12.7% (6.2–20.0); specificity 96/96/95%; strict rule 16/40; false flags 44/224/277 per 1,000; cumulative flags 13/30/44% (posthoc P2: 12.6/29.8/43.9%); D6 +38 pts (19–58), Holm 0.018 and 0.070 across k.
- **Calibration (A3a):** D6 4.7% (3.7–5.9); D8 6.6% (4.7–8.9); D9 4.2% (1.5–7.5); 15/16 valid, D6 at 6 fields 7.7% (4.6–11.0); D2 0.3%; calibrated sensitivities 15/15 vs 19, diff −4/−4, Holm 1.00; D8 at 6 fields 64% / 2.2%, +8 (−13 to 28).
- **GRAPE:** D8 specificity 61→95 (92–97); D2 79→95; sensitivity 10 and 19 vs 44; PPV 52% and 16%; D1 8/9 and 4/18.
- **Confirmation and enlarged reference:** confirmation 3.7/4.0/2.0 (D8) and 2.8/1.6/2.5 (D6), sensitivity 52/35 vs 58; enlarged reference D1 15% (9–21), 27, 40, 57; D2 +9 (1–16), Holm p = 0.047, stable eyes +11 (5–17).
- **Audit:** Spearman ρ 0.65 (0.35–0.85), 80% within 3 points, audit 7/8 detected with 7 false warnings.
- **Descriptives:** 132 / 26 / 26 / 80 / 41 patients; MD −4.4 (−6.0 to −3.2); 12.9 years; interval 1.3 years; 6.5 years to the 6th field.

### Claims that are wrong, misleading or overclaimed
1. **"In a pre-specified amendment…" (Abstract, Introduction, Methods).** The protocol says "exploratory, post-review… prompted by simulated review". Fix as in R3.
2. **"The apparent early-detection gains were false alarms." (Abstract, Conclusion, Key Summary Points); "This is direct evidence that…" (Discussion).** Overclaim: see R2. D2's +19-point gain had a valid false-alarm rate of 2.6%, and D8's gain was never significant (p = 0.69).
3. **"Calibrating … keep[s] false alarms near the nominal level, including after transfer to another perimeter." (Abstract Conclusion).** a3_summary.json gives D2-calibrated 0.3/0.5/0.7/0.7% and D8 at 6 fields 2.2%. In GRAPE, specificity was restored but sensitivity fell to 10% (paired −33 pts vs D1, Holm p = 0.008). The Abstract omits this; the Results state it only without the test.
4. **"Shuffle calibration removed every clear excess (H5 supported)."** a3_summary.json has `H5_all_valid: false` (D6 at 6 fields: upper limit 11.0%, and its value is unchanged from nominal 7.6%). The protocol's H5 wording ("valid … at every k") is therefore **not** met. Only its falsification clause (lower CI > 5%) passes. Say "H5 met by its falsification criterion; one cell (D6, 6 fields) remained invalid".
5. **"The machine-learning models exceeded 5% clearly in 4 of 8 combinations (H4 supported)."** By the paper's own dagger rule, 6 of 8 ML cells are invalid, and all 6 have point estimates above 5%. The count is inconsistent with Table 2 (R6).
6. **"False alarms were clearly above 5% for D6 (3 fields), D8 (3 fields), D9 (3 fields), D8 (4 fields), D8 (5 fields)".** These are 5 cells, but Table 2 daggers 8. Unify the rule.
7. **"D1 flagged 69% of progressors by the sixth field".** Correct (descriptives `flagged_by6` = 0.692), but it sits next to Table 2's 58% at 6 fields. Readers will think one is an error. Say "flagged at any of fields 3–6 (69%) vs at field 6 alone (58%)".
8. **Methods promise "positive predictive value at 10% prevalence and at the GRAPE prevalence", but the Results report only the GRAPE PPV.** The omitted UWHVF 10%-prevalence PPVs (posthoc P3) are D1 33%, D2 **62%**, D6 22% and D8 9%. D2's value runs against the narrative. Report it (in the proposed Table 4) or remove the promise. Leaving it out selectively is not acceptable.
9. **"D8 transferred from UWHVF flagged more labelled progressors than D1 (66% versus 44%)."** Add that this was not significant (paired +26 pts, 95% CI 0 to 50, Holm p = 0.28).
10. **"With the secondary PoPLR-based reference and the post-hoc later-field reference, sensitivities were lower and the pattern was similar."** In the later-field reference at 3 fields, D6 stays at 53% vs D1 6% (n = 17, Holm p = 0.07) with specificity 83%. "Similar" is fine, but give the number, because it supports the claim that D6 "flags more of everything".
11. **"In 150 progressors … H8 supported" (adjusted p = 0.047).** Correct, but fragile. Holm p sits exactly at the margin and the protocol's pilot estimate was +19 pts against an observed +8.7. Say "marginally".
12. **Key Summary Point: "Shuffle calibration brought every detector's false-alarm rate close to 5%".** False for D2 (≤0.7%), D8 at 6 fields (2.2%) and D9 at 6 fields (1.3%). Change to "to 5% or below (one exception)".
13. **Novelty sentence: "To our knowledge … this has not been used to set the thresholds of visual field progression detectors."** Your own D5 (pooled-shuffle conformal) uses the same mechanism for the trend statistic. Soften to "as a general recalibration of arbitrary detector scores, including ML outputs".
14. **Fig. 5, GRAPE bar panel.** It shows only specificity, so the 10% sensitivity of calibrated D8 is invisible. This is misleading by omission.

### Citation contexts
- **Crossref check.** Refs 9, 22, 24, 33 and 35 resolve to the cited titles, journals and volumes. Ref 24's DOI (`tvst.11.1.1` with article number 2) looks inconsistent, but Crossref confirms it resolves to the UWHVF paper, so it is correct.
- **Ref 9 (Artes 2014).** The reference list gives only "Visual Field Progression in Glaucoma". The authors should check whether the published title has a subtitle (it is a GPA-specificity paper). The citation context ("true no-change data", event-method limits) is appropriate. Title completeness is **UNVERIFIED**.
- **Ref 30 (Gagnon-Bartsch & Shem-Tov, classification permutation test).** It is a covariate-balance method, cited as the basis for D10 and for "pooling shuffles". Present it as an analogy ("a classifier score used as a permutation statistic, as in [30]"), not as precedent.
- **Ref 35 (medRxiv preprint dated 16 Nov 2026, one week before submission).** It is not peer reviewed and is cited as evidence for personalised schedules. Label it as a preprint in the text, or replace it with ref 36 alone.
- **Ref 11 (Heijl 2008, EMGT criteria) for "commercial Guided Progression Analysis".** Acceptable, but a primary GPA description would be the more accurate citation.
- **Ref 23 (TRIPOD+AI).** This is a benchmark of detectors, not a prediction-model development study. "Following TRIPOD+AI where it applies" is acceptable, but attach the checklist with "N/A" items, or reviewers will ask for it.

### Figures (each image inspected)
- **Fig. 1:** clear. The E3 box merges "shuffle audit & calibration" with "E4 external". Split it, or label calibration as exploratory.
- **Fig. 2:**
  - Labels overlap (D1/D5 at 3, 4 and 6 fields; D4/D10/D7 stacked at the origin at 3 fields; "D2D3" at 5 fields).
  - The x-axis scale differs per panel (0–0.3 vs 0–0.1), which visually shrinks the 3-field excess against the others.
  - The axes are in proportions while the text uses %.
  - **Fix:** use a common x-axis or state the difference in the legend, convert to %, and use leader lines or offsets for labels.
- **Fig. 3:** acceptable. Move it to the supplement (secondary, negative result).
- **Fig. 4:** "D7/D4" labels overlap at the origin. Merge it into the supplement with Table 3, or keep only Fig. 4 and move Table 3.
- **Fig. 5:**
  - Labels overlap (D1/D6 at 4 fields, D1/D9 at 5 fields).
  - D1 is drawn as a filled "calibrated" marker although it was not calibrated.
  - The GRAPE panel omits sensitivity (see item 14).
  - **Fix:** use a distinct D1 reference marker and add the GRAPE sensitivity bars.

---

## 4. Cuts to reach about 4,000 words of main text

These figures are approximate prose word counts (current about 4,260). The cuts listed total about 600–700 words, which leaves room for the new Table 4 legend and the caveat sentences demanded above.

| # | Where (current words) | Cut | Saves |
|---|---|---|---|
| 1 | Methods, "Ethics" (60) | Delete. It duplicates Declarations, "Ethical Approval". | ~60 |
| 2 | Methods, "Use of software assistance" (62) | Keep one sentence and refer to Declarations. | ~40 |
| 3 | Methods, "Deviations from the protocol" (97) | Move the list to the supplement and keep one sentence pointing to it. | ~70 |
| 4 | Methods, Statistical analysis (203) | Drop the runtime and core counts, the software list (move to supplement) and the audit-accuracy detail. | ~50 |
| 5 | Methods, Detectors D6–D9 (about 220) | Move the D6 development note, the D7 comparison with commercial GPA and the D8/D9 tuning details to Supplementary Methods. Keep one line per detector. | ~90 |
| 6 | Methods, A3 paragraph (206) | Move the H5–H8 statements to the supplement. Keep the procedure in three sentences, labelled exploratory. | ~70 |
| 7 | Introduction, para 2 (149) | Collapse the trend/event/permutation/Bayesian/ML taxonomy into one sentence with the citations. | ~60 |
| 8 | Introduction, para 4 (166) | Replace RQ1–RQ6 and H2–H6 with three plain questions. | ~70 |
| 9 | Results, strict-rule paragraph (119) | Move the strict-rule sentence and the D4/D10/D7 "cannot flag with three fields" explanation to the table legend or supplement. | ~50 |
| 10 | Results, shuffle audit (111) | Two sentences. Fig. 3 goes to the supplement. | ~50 |
| 11 | Results, confirmation (62) | One sentence. Details go to Table S7. | ~30 |
| 12 | Discussion, mechanism paragraph (232) | Halve it. Keep the one-sentence intuition per detector type and cut the conformal/CPT exposition. | ~110 |
| 13 | Discussion, limitations (211) | Merge the GRAPE caveats (already in Methods) and the duplicate circularity sentence. | ~40 |
| 14 | Display items | Move Table 3 (GRAPE) and Fig. 3 to the supplement. Add Table 4 (clinical implications). End with 4 figures (1, 2, 4 or 5 merged with the GRAPE panel) and 3 tables (1, 2, 4). | table words |

Do **not** cut:
- the 69% vs 58% clarification;
- the GRAPE sensitivity-cost sentence;
- the D2 over-conservatism caveat;
- the provenance wording for A3.

These are the honesty fixes that keep the paper from being rejected at review.

---

## One-line summary of the ranked fixes
1. Reframe it as a paper about the decision to escalate treatment: new title, plain detector names, three questions, and a new Table 4 of clinical implications built from existing outputs.
2. Replace "gains were false alarms / direct evidence" with "no significant advantage once detectors are held to the same false-alarm level". Acknowledge D2 (+19 pts at a valid 2.6% false-alarm rate, removed by over-conservative calibration).
3. Stop calling A3 "pre-specified". Label it exploratory and post-review, describe the review truthfully, and say that the choice of detectors depended on the results.
4. State the cost of calibration in the Abstract, Key Summary Points and cover letter: in GRAPE, calibrated ML sensitivity was 10% vs 44% (p = 0.008). Change "near nominal" to "at or below 5%".
5. Report CIs for every denied gain and say that large gains cannot be excluded with 26 progressors.
6. Use one validity rule throughout, fix the "4 of 8" vs 6-of-8 ML inconsistency, and rewrite the script-like list sentence.
7. Lead the Abstract with D8's 27.7% (independent), not D6's 22.4% (seen in development).
8. Cut about 600 words. Move Fig. 3 and Table 3 to the supplement. End with 4 figures and 3 tables.
9. Put the time scale in the Abstract: 3 fields is about 2.6 years at UWHVF intervals.
10. Report the promised UWHVF 10%-prevalence PPVs or remove the promise.
11. Deposit the code and flag files publicly with a DOI.
12. Fix the figures (overlapping labels, panel axis scales, a GRAPE sensitivity panel in Fig. 5), correct "weekly for 12 weeks", label ref 35 as a preprint, present ref 30 as an analogy, and check the full title of ref 9.
