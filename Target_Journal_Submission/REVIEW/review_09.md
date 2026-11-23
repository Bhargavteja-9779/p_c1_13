# Review 09 — "Reviewer 2" (hostile generalist)

Manuscript: *Detecting Glaucomatous Visual Field Progression From Few Tests Without False Alarms: An Open Benchmark With a True No-Change Arm* (target: Ophthalmology and Therapy)

Files checked: `manuscript/manuscript_filled.md`, `manuscript/figure_legends.json`, `figures/fig1–fig4`, `tables/*.csv`, `results/metrics.json`, `results/statistics.json`, `results/descriptives.json`, `results/raw_results.csv.gz`, `supplementary/Supplementary_Note_S1_development_history.md`, `journal_selection/{selected_journal,style_notes,journal_level_profile}.md`. Every number I criticise below was recomputed or looked up in these files. Where I computed something the authors did not report, I say so.

## Summary

The authors run ten progression detectors on the first 3–6 fields of a series. They score them in three ways: against a whole-series reference in 26 progressing and 26 stable UWHVF eyes, by false-alarm rate on 30 Artes weekly-retest patients, and by a "shuffle audit". They also use a Chinese Octopus data set (GRAPE). The headline is that the largest early gains are false alarms that reference-stable specificity misses, and that nothing valid beats an OLS trend of mean sensitivity.

The engineering is careful and transparent. Code, a protocol, seeds, bootstrap by patient, Holm correction and an honest development log are all above this journal's norm. But the paper's story is bigger than its evidence. The detectors whose "gains turn out to be false alarms" are mostly the authors' own in-house constructions. One of them (D6) was already known to be invalid on the same 30 Artes patients before the protocol was written. The null result for valid detectors rests on 26 progressors, so it cannot tell "no gain" apart from "a gain we could not detect". The Key Summary Points also contain a factual error about which detectors flagged the most progressors. All of this can be fixed, but only by reframing the paper downward.

## Issues

### 1. FATAL (as currently framed) — The headline generalises from in-house straw men to "new detectors" in the literature
- **Location:** Abstract, Introduction ("Many new detectors claim to find glaucomatous visual field progression earlier... but their false-alarm rates are rarely measured"); Abstract Conclusion ("the largest apparent early-detection gains were false alarms that standard specificity estimates missed"); Discussion para 3.
- **Problem:** None of the published detectors cited [15–22] is evaluated. D5, D6 and D10 are the authors' own abandoned development ideas (Supplementary Note S1, rounds 0, 1 and 5). D8 and D9 are generic in-house LightGBM/GRU models with a threshold rule the authors chose. Supplementary Note S1, round 5, says the D6 detrended pooled null was "Rejected: the apparent gain at 3 fields came with false-alarm rates of about 13–22% on true no-change data". That was measured on the same Artes data later used as the "true no-change arm". The paper's most striking result (D6: 57% sensitivity, 22.4% false alarms) is therefore a re-measurement of something already known, on the same 30 patients. It is not a held-out discovery. The main text says only that D6 "was the most sensitive approach during development" (Methods) and, in Limitations, that "the Artes data were used once during development to check false alarms".
- **Fix:** (a) State plainly in Methods, next to D6, that D6 was known before the protocol to have inflated false alarms on the Artes data, and that its E2 result is therefore not an independent test. (b) Change the Abstract and Conclusion claims to refer to "the detectors we evaluated, three of which were our own development methods". (c) Either add at least one published, independently specified detector, or remove the implied indictment of the literature ("Many new detectors claim..."). (d) Consider retitling. "Without False Alarms" promises a method; the paper delivers a negative benchmark.

### 2. MAJOR — Factual error in the Key Summary Points and Abstract about who "flagged the most progressors"
- **Location:** Key Summary Points ("With three fields, the two detectors that flagged the most progressors (57% and 26% versus 19% for the trend test) raised false alarms in 22.4% and 27.7%"); Abstract ("Two detectors flagged more progressors only with excess false alarms").
- **Verification:** `tables/table2_main.csv`, k = 3: D6 0.569, **D2 0.385**, D8 0.262, D1 0.192. D2 (MD-rate rule) had a *valid* false-alarm rate of 2.6% (95% CI 1.5–3.9). So the second-most-sensitive detector at three fields is a valid one, and the summary-point statement is false. The D8 "gain" over D1 is a paired difference of +7.7 points, about 2 eyes (`statistics.json`: only_det 4, only_D1 2; Holm p = 1.0). That is not evidence that D8 "flagged more progressors".
- **Fix:** Rewrite to: "With three fields, the most sensitive detector (57%) had 22.4% false alarms; a machine-learning model had 27.7% false alarms with no significant sensitivity gain; a simple rate rule reached 38% with valid false alarms, but this was not significant (adjusted p = 0.72)." Make the same correction in the Abstract.

### 3. MAJOR — The conclusion "no valid detector beat the trend test" is absence of evidence from 26 progressors
- **Location:** Abstract ("No detector with a valid false-alarm rate flagged significantly more progressors than the trend test"); Key Summary Points ("so the evidence does not support replacing it in routine care"); Abstract Conclusion ("a simple trend test remains a strong default"); Discussion ("no detector with a valid false-alarm rate beat the plain trend test").
- **Verification:** Valid detectors had point gains of +19 points (D2, k = 3; CI 0 to 42, Holm p = 0.72) and +12 points (D8, k = 6, valid FA 3.6%; CI −8 to 31). The lower CI of the D2 difference touches zero. With 26 progressors from 41 patients, the study can only detect very large differences. The authors concede this in Limitations ("moderate gains (around 10 points) cannot be excluded"), but the Abstract and Key Summary Points do not.
- **Fix:** Add a power or minimum-detectable-difference statement to Methods (for example, the paired difference detectable with 80% power at n = 26). Put "differences of up to ~X points cannot be excluded" in the Abstract Results. Replace "strong default" with "a well-calibrated default that was not beaten in this small sample". With 19% sensitivity at three fields and 58% at six, D1 is calibrated, but it is not "strong".

### 4. MAJOR — Spectrum and incorporation bias in the 26 + 26 reference; 61% of eligible eyes discarded
- **Location:** Methods, Reference standard; Results, Study data ("132 had at least eight fields, of which 26 were reference progressors, 26 reference stable and 80 indeterminate").
- **Problem:** (a) Sensitivity and specificity are estimated only at the extremes (p < 0.01 with slope < −0.3 dB/yr, versus p > 0.5). 80 of 132 eyes (61%) were excluded. Clinic eyes are mostly in the indeterminate middle. (b) The reference slope is computed on *all* fields, including the first k that the detectors see. This is incorporation bias, and it favours D1 most because D1 is the same statistic on a subset. (c) Stable eyes needed a whole-series p > 0.5, which selects eyes whose early fields were not falling. The authors use this to explain why specificity misses false alarms (good), but it also means the specificity column of Table 2 has little meaning in any setting. 100% specificity with a bootstrap CI of 100–100 at k ≥ 4 for most detectors reflects this selection, not accuracy.
- **Fix:** Name incorporation and spectrum bias explicitly in Limitations. Add a sensitivity analysis that computes the reference only from fields k+1 onward (non-overlapping). Report how detectors classify the 80 indeterminate eyes (flag rate), so readers see behaviour in the realistic middle.

### 5. MAJOR — The GRAPE "external" comparison is near-circular for D1, so it cannot support "in a second clinic"
- **Location:** Discussion para 1 ("no detector with a valid false-alarm rate beat the plain trend test significantly at any number of fields, in one clinic or in a second clinic using a different perimeter"); Results, External data set.
- **Problem:** The GRAPE MD label is "a negative slope of mean deviation with p < 0.05" over a median of 4 visits. D1 is a one-sided OLS slope test of mean sensitivity, p < 0.05, on the first 3–4 of those same visits. For a 4-visit eye at k = 4, D1 and the label are almost the same test, so D1's 95% specificity is close to automatic. The manuscript also defines no "valid false-alarm rate" in GRAPE, because there is no no-change arm there, so the "valid" qualifier in the Discussion sentence does not apply to GRAPE. Finally, D8 was trained on Humphrey 24-2 data and applied unchanged to an Octopus G1 perimeter. Nobody would deploy a model that way, so its 61% specificity is unsurprising.
- **Fix:** Delete "or in a second clinic" from the Discussion sentence. State in Results that the GRAPE MD label and D1 share their statistic and data. Report GRAPE results against PLR2/PLR3 labels as well (Table 1 lists them: 40 and 14 eyes). Present GRAPE strictly as a transfer and false-flag stress test, as the Limitations paragraph already says.

### 6. MAJOR — The shuffle-audit result is oversold in the Abstract
- **Location:** Abstract ("The shuffle audit tracked the true false-alarm rate (Spearman ρ = 0.65; 80% of combinations within 3 percentage points)"); Conclusion ("clinics can check a detector on their own records with a shuffle audit").
- **Verification:** `statistics.json`: ρ = 0.648, 80% within 3 points, maximum difference 10.4 points (D8, k = 3: audit 17.3% versus true 27.7%). The pre-specified criterion was ρ ≥ 0.7, which was not met (the Results admit "partly met"; the Abstract does not). Three of the 40 cells (D4, D7 and D10 at k = 3) are structural zeros where both rates are 0 by construction, which inflates agreement. In my recomputation excluding these three cells (37 cells), ρ = 0.56 and 78% were within 3 points. The audit also missed an invalid cell (D6, k = 6: audit 4.9%, true 7.6%, CI upper 11.1%). It raised false audit alarms on valid rules: D2 k = 3 (11.7% versus 2.6%), D7 k = 6 (11.7% versus 1.9%) and D8 k = 6 (8.7% versus 3.6%).
- **Fix:** In the Abstract, say "partly met the pre-specified agreement criterion (ρ = 0.65 versus ≥ 0.7)". Report agreement excluding structural zeros. Report the audit's ability to classify valid versus invalid cells (a 2×2 table at a stated audit cut-off).

### 7. MODERATE — The validity rule is inconsistently defined and knife-edge for at least one cell
- **Location:** Methods, Statistical analysis ("its point estimate did not exceed 5% by more than sampling error") versus Table 2 footnote ("95% CI upper limit above 10% or lower limit above 5%").
- **Verification:** D9 at k = 6 is declared invalid with a CI upper limit of 0.100002 (`metrics.json`), i.e. 10.0002%. A bootstrap Monte-Carlo fluctuation decides this classification. Meanwhile D6 at k = 5 (6.2%, CI 3.7–8.9) counts as valid.
- **Fix:** Use one operational definition everywhere. Report validity counts under a slightly different rule (e.g. upper limit ≤ 8% or ≤ 12%) to show robustness. Mark D9 k = 6 as borderline.

### 8. MODERATE — Erratic, non-monotone sensitivity is not discussed
- **Location:** Table 2.
- **Verification:** D6 sensitivity is 57%, 25%, 32% and 54% for k = 3–6. D2 is 38%, then 23% at k = 4–6. D9 is 12%, 12%, 41% and 38%. More data should not make a well-behaved detector flag fewer true progressors. This shows that the three-field "gains" were mostly flags that disappeared at the next field.
- **Fix:** Add a "flag persistence" analysis (the share of k = 3 flags still present at k = 4 and 5) for both reference progressors and Artes windows. This directly answers the clinical question of whether an early flag holds up.

### 9. MODERATE — The "so what?" for an Ophthalmology and Therapy reader is thin
- **Location:** Introduction last paragraph; Discussion para 5.
- **Problem:** The two actionable messages are "report false alarms on true no-change data" and "test more often". The first was already done for GPA by Artes et al. [9]. The second is the conclusion of [5, 32–35]. The paper's real contribution is a reusable open benchmark with a no-change arm, and that is under-sold relative to the clinical claims. The journal's scope (`selected_journal.md`) flags "methods-heavy AI paper in a therapy-oriented journal" as the top rejection risk, and the escalation framing is asserted rather than measured.
- **Fix:** Lead with the benchmark as a resource (what anyone can now run against it). Cut the clinical-recommendation sentences back to what the data show.

### 10. MODERATE — Figure 2 readability
- **Location:** Fig. 2 (`fig2_validity_vs_power.png`).
- **Problems:** (a) Overlapping labels. At 3 tests "D1"/"D5" overprint, and "D4/D7/D10" at the origin reads as a single illegible "0". At 4 tests "D1"/"D5" overprint. At 5 tests D1, D4, D5 and D10 form an unreadable cluster, and "D2"/"D3" overprint. At 6 tests "D1"/"D5"/"D4" overprint ("D" fragments). (b) Each panel has a different x-axis range (0–0.33, 0–0.125, 0–0.25, 0–0.10). The legend notes this, but readers will compare positions across panels. (c) The shaded band marks FA ≤ 5%, but the paper's validity rule is CI upper ≤ 10%, so the shading does not show which points are valid (D6 at k = 5, plotted outside the band, is "valid"). (d) The x-axis is in proportions while all text uses percentages. (e) D1, D2 and D3 share colour and marker. In grayscale only marker shape separates families, and individual detectors depend entirely on the overlapping labels.
- **Fix:** Use a common x-axis (or a log scale) across panels. Mark invalid points with open markers or a dagger, matching Table 2. Use leader lines or a repel algorithm for labels, or replace the scatter with a dot-and-interval "forest" layout (one row per detector, two columns: sensitivity and FA). Use percent axes. Add panel letters (a–d).

### 11. MODERATE — Figures 3 and 4 readability
- **Fig. 3:** No point is labelled, so the reader cannot find the outliers the text discusses (D2 k = 3, D7 k = 6, D8 k = 3). Structural zeros are hidden under the origin. There is no ±3-point band, even though the text's main agreement metric is "within 3 points". Invalid cells are not distinguished. Fix: label the 5–6 discussed points, add a shaded ±3 pp band, use open markers for invalid cells, and note the overplotted zeros in the legend.
- **Fig. 4:** At 3 tests "D4"/"D7" overprint at the origin ("D7/4"), and "D1"/"D5" labels overlap. The left and right x-axes differ (0–0.45 versus 0–0.25). Fix: common axes, label repel, and the same marker scheme as Fig. 2.
- **Fig. 1:** The text "E3 shuffle audit │ E4 external" touches the box border. The box says "first 3-6 tests only", but E4 uses only 3–4 tests. Artes feeds the "detectors" box rather than E2, and UWHVF does not feed E3, so the data-to-evaluation mapping is not shown. Key counts are missing (869 test eyes, 26/26/80 reference, 300–210 windows, 263 eyes). Fix: redraw as a flow with one arrow per data set to its evaluation and put the counts on the arrows.

### 12. MODERATE — Table clarity
- **Table 2:** "Sens / FA" in one cell with no CIs makes the key comparison hard to read. Sensitivities are seed means over 26 eyes (e.g. 57 = 14.8/26), so readers cannot map them to eye counts. Fix: split into two sub-tables or add an "n flagged/26" column, and give FA CIs in the main table (they are the paper's primary endpoint).
- **Table 3 and Supplementary Table S1:** Degenerate bootstrap CIs ("0 (0–0)", "100 (100–100)") should be replaced by exact (Clopper–Pearson or Wilson) intervals. For 0/26 the exact upper bound is about 13%, which is not 0.
- **Table 1:** "30 / 30 / 360" (Artes) should say one eye per patient. "Interval 1.3 years" should say "median interval between first six fields".

### 13. MODERATE — Abstract Conclusion over-reaches on "largest apparent gains were false alarms"
- **Location:** Abstract Conclusion and Conclusion ("the largest apparent gains in early detection ... came with false-alarm rates far above the nominal level").
- **Verification:** True at k = 3 (D6). At k = 6 the largest gain (D8, 71% versus 58%) had a valid FA of 3.6%. At k = 5 the largest valid gain was D7 (+8 points, valid FA 1.2%).
- **Fix:** "With three fields, the largest apparent gain came with ..." Do not generalise across k.

### 14. MINOR — Reference list problems (verify; do not trust my memory)
- Ref 24 has no authors (". TRIPOD+AI statement ..."). Add the author group.
- Ref 9 title appears truncated ("Visual Field Progression in Glaucoma."). Check the full title in PubMed.
- Ref 25: the DOI ends in "tvst.11.1.1" but the citation gives article "2". Check which is correct.
- Ref 21: a medRxiv preprint dated 16 Nov 2026 with DOI prefix 10.64898. Confirm the DOI resolves, and note that it is a non-peer-reviewed preprint.
- Ref 29 (Freedman & Lane 1983) is cited for "detrended, shuffled" null construction. Make sure it supports that specific use.

### 15. MINOR — Wording and hygiene
- "PLR-3: at least three locations with a slope of −1 dB per year or worse and p < 0.01". State whether this is per location and whether locations must be contiguous.
- "eyes not flagged by six fields were counted as seven". Report the share censored (D1 31%, D3 62%; `descriptives.json`) next to every median.
- The Abstract says "University of Washington data set". Say Humphrey 24-2 there, since generalisability hinges on it.
- Placeholders ([AUTHORS TO COMPLETE], [REPOSITORY URL]) must be resolved. Without a DOI-archived repository, the "open benchmark" claim cannot be checked.
- Figure legends live in `figure_legends.json` but are not in `manuscript_filled.md`. Make sure they appear in the submitted file after the references, as the journal requires.

## Recommendation

**Major revision.** The analysis is honest and the benchmark is useful. But the Abstract and Key Summary Points currently (i) contain a factual error about which detectors were most sensitive, (ii) present a known-in-advance failure of the authors' own method as a discovery about "new detectors", and (iii) turn a 26-progressor null into "the trend test remains a strong default". With the reframing, the near-circular GRAPE caveat, a power statement, flag-persistence analysis and redrawn figures, this would be a solid, modest contribution.
