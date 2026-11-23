# Review 10: Plain English and internal consistency

**Reviewer role:** copy-editor. I checked internal contradictions across the Abstract, KSP, PLS, Results, tables, Discussion, Conclusions, Supplement and cover letter; undefined abbreviations; sentences over 25 words; and detector naming.

## Summary

The prose is mostly clear and the British spelling is consistent. However, several statements contradict the paper's own tables:

- The shuffle audit "identified the same invalid detectors".
- Two machine-learning methods "found more worsening".
- The paired differences do not equal the difference of the tabulated percentages.
- 69% against 57.7% "by" or "at" the sixth test.

Detector names change across sections, and "MD" is used for two different quantities. Forty-nine sentences in the main text exceed 25 words.

## A. Internal contradictions

**1. MAJOR — The shuffle audit is said to have "identified the same invalid detectors", which the Results contradict.**
- Locations:
  - Discussion, paragraph 2: "In our study, both identified the same invalid detectors."
  - Cover letter: "A simple 'shuffle audit' … flagged the same invalid detectors."
  - Results: "it underestimated the false alarms of D9 at three tests (8.5% versus 12.7%)".
  - Table 2: D6 at k = 6 has an audit rate of 4.9%, but true no-change 7.6% ("no"). D2 at k = 3 (11.7%) and D7 at k = 6 (11.7%) are valid but flagged by the audit.
- Fix: "ranked detectors broadly as the true no-change data did, but missed or wrongly flagged several detector–test-number cells."

**2. MAJOR — The PLS says two ML methods found more worsening; Table 2 shows the GRU never did.**
- Location: PLS: "Methods that found more worsening, including two machine-learning methods, also gave many more false alarms."
- Evidence: Table 2 shows D9 (GRU) below D1 at every k (12.3 against 19.2; 11.5 against 30.8; 40.8 against 42.3; 37.7 against 57.7).
- Fix: "including one machine-learning method".

**3. MAJOR — Stated differences do not equal the difference of the stated percentages.**
- Locations:
  - Results: "D8 … flagged more labelled progressors (65.9%; +25.9 percentage points …)". 65.9 − 44.4 = 21.5.
  - "D6 … sensitivity of 56.9% … a difference of +38.5 percentage points". 56.9 − 19.2 = 37.7.
  - "D8 detected 70.8% … (+11.5 percentage points …)". 70.8 − 57.7 = 13.1.
  - "specificity fell to 61.2% (+33.5 percentage points … in false positives)". 95.3 − 61.2 = 34.1.
- Cause: differences use majority-over-seeds flags, while the percentages are seed means.
- Fix: add to Methods and the Table 2 and Table S2 notes: "Differences and McNemar tests use each eye's majority flag across seeds; percentages are seed means, so the two may differ by up to a few points." Alternatively, report the majority-flag percentage next to each difference.

**4. MAJOR — The sixth-test sensitivity is given as 69% in some places and 57.7% in others.**
- Locations:
  - Results: "By the sixth test, D1 had flagged 69% of reference progressors."
  - Discussion: "the trend test flagged only about 69% of reference progressors by the sixth test".
  - Table 2 and Results: D1 sensitivity "57.7% … at six tests".
- Cause: 69% means "flagged at any of reviews 3–6"; 57.7% is the flag at the sixth-test review only. The reader is not told this.
- Fix: define it on first use ("flagged at least once at reviews based on 3, 4, 5 or 6 tests") and give the matching cumulative false-alarm rate.

**5. MODERATE — The D9 k = 6 validity wording contradicts the displayed CI and the rule.**
- Location: Results: "D9 had 5.9% (95% CI 2.3–10.0%), so both were again not valid; D9 only just exceeded the 10% upper limit."
- Problem: the rule says invalid if the upper limit "did not exceed 10%" fails. The printed 10.0% reads as not exceeding.
- Fix: print two decimals for this cell (10.00% → "10.0002%"), or call the cell borderline.

**6. MODERATE — "Exceeded the validity limits" is used for a value inside the 10% ceiling.**
- Location: Results: "D8 also exceeded the validity limits at four tests (9.4%)".
- Problem: 9.4% is below the 10% ceiling. The failure is the *lower* limit (6.3% > 5%), but the reader sees only 9.4%.
- Fix: "D8 at four tests (9.4%; lower 95% limit 6.3%, above 5%)".

**7. MODERATE — "The hypothesis … was supported" contradicts the CIs.**
- Location: Results: "the hypothesis that these detectors exceed the nominal 5% was supported for D8 at three to five tests and for D9 at three, five and six tests".
- Problem: D9's CIs at k = 5 (2.8–13.3%) and k = 6 (2.3–10.0%) include 5%, so there is no evidence that they exceed 5%. They were "not valid" only because of the 10% ceiling.
- Fix: "D9 at three tests exceeded 5%; at five and six tests its upper limit exceeded 10%, so validity could not be confirmed."

**8. MODERATE — GRAPE labels are called "clinician labels" in some places and criterion labels in others.**
- Locations: Abstract, "agreement with clinician labels"; Results, "the clinicians' mean-deviation criterion"; Limitations, "its labels came from criteria applied to the full series".
- Fix: use "criterion-based progression labels" throughout.

**9. MODERATE — Table 3 denominators are wrong for the k = 4 rows.**
- Location: Table 3 legend: "27 labelled progressors and 236 non-progressors with at least three tests".
- Problem: the k = 4 rows use 18 progressors and 145 non-progressors (Table S2; 163 eyes with ≥4 visits).
- Fix: add "k = 4: 18 and 145 eyes with at least four tests".

**10. MODERATE — The Artes test schedule is described inconsistently.**
- Locations: Methods: "had 12 visual fields in 12 consecutive weeks"; PLS: "tested every week for 12 weeks"; Table 1: "Time from first to third test … 2 weeks by design".
- Problems:
  - One series spans 524 days.
  - The analysis replaces the real dates with routine-care donor dates (about 2.2 years to the third test), which Table 1 does not say.
- Fix: correct the description and footnote Table 1: "analysed with donor test dates (Amendment A1)".

**11. MODERATE — D4 is listed as stochastic but is deterministic.**
- Location: Methods: "Stochastic detectors (D4–D6, D8–D10) were run with five seeds".
- Problem: D4 uses exact enumeration and is deterministic. Table S1 shows a seed SD of 0.0 for D4 sensitivity at all k.
- Fix: "D5, D6 and D8–D10 have random components. D4 was re-run with five sets of donor dates."

**12. MODERATE — The Holm family size is wrong for GRAPE.**
- Location: Methods: "corrected p-values for the nine comparisons within each number of tests and endpoint".
- Problem: GRAPE endpoints have six comparisons.
- Fix: "nine (UWHVF) or six (GRAPE) comparisons".

**13. MINOR — Amendments are said to be "reported below", but they appear only as parenthetical tags.**
- Location: Methods: "Two amendments were made before any final result was seen; both are reported below."
- Problem: the amendments appear only as "(amendment A1)" and "(amendment A2)" tags and in Supplement S2.
- Fix: "both are described in Evaluation and in Supplementary S2".

**14. MINOR — The test-set size is ambiguous.**
- Location: "The test set (777 patients, 869 eyes with at least three tests)".
- Problem: the 777 patients include patients without eligible eyes.
- Fix: "777 patients (1,489 eyes), of whom 869 eyes had at least three tests".

## B. Detector names and abbreviations

**15. MAJOR — "MD" refers to two different quantities, and detector labels change across sections.**
- MD conflict:
  - Table 1 note defines "MD, mean deviation", and the reference uses "mean total deviation".
  - D1 and D2 use *mean sensitivity* but are labelled "D1 Trend, MD", "D1 OLS-MD", "D2 MD rate" and "MD-rate <= -1 dB/yr".
- Naming used in each source:

| Detector | Methods list | Table 2/3 | Supplement/JSON | Running text |
|---|---|---|---|---|
| D1 | OLS-MD | Trend, MD | OLS-MD | trend test of mean sensitivity |
| D2 | MD rate | MD rate | MD-rate <= -1 dB/yr | rate rule |
| D3 | PLR-3 | PLR-3 | PLR >=3 points | pointwise rule |
| D5 | pooled-shuffle conformal test | Pooled conformal | Pooled-shuffle conformal MD | pooled test without detrending |
| D6 | pooled-detrended conformal regional test | Pooled-detrended | … region-max | conformal test with a pooled and detrended reference |
| D7 | event analysis | Event | Event analysis (GPA-like) | event analysis |
| D8 | machine learning, tabular | LightGBM | ML-tabular (LightGBM) | gradient-boosted trees |
| D9 | machine learning, sequence | GRU | ML-sequence (GRU) | recurrent network |
| D10 | self-supervised order network | Order net | … + permutation | order network |

- Fix: choose one short name per detector and use it everywhere, with the D-number:
  - D1 trend (MS), where MS means mean sensitivity, and D2 rate (MS);
  - D3 pointwise (PLR-3), D5 pooled conformal, D6 pooled-detrended conformal, D7 event, D8 boosted trees, D9 GRU, D10 order net.
  
  Reserve "MD" for mean deviation only.

**16. MODERATE — Abbreviations are undefined or defined only implicitly.**
- Main text:
  - GRAPE is never expanded.
  - TRIPOD+AI is not expanded.
  - GRU appears in tables without "(GRU)" after "gated recurrent unit".
  - LightGBM appears in tables and software without being linked to "gradient-boosted trees".
  - OLS is not introduced as an abbreviation.
  - PLR (in "PLR-3") is introduced only inside "PoPLR".
  - E1–E4 are introduced as labels without a definition sentence.
  - UWHVF is defined.
- Supplement: FA, FPR, pp, Sens, Spec, VF, nAMD, VA, AUROC, R2, GPA, "N1/N3/N4–N7", "eps" and "lambda" are undefined.
- Fix: add an abbreviation list, or expand each abbreviation at first use in each section and table legend.

## C. Plain English and long sentences

**17. MODERATE — Forty-nine main-text sentences exceed 25 words (automated count, Abstract to Conclusions, table rows excluded but table captions included).**
- Worst cases, with line numbers in `manuscript_filled.md`:
  - L88 (55 words), D7 definition: split into "A location is deteriorated if … . Progression requires … . D7 needs at least four tests."
  - L19 (46 words), Abstract Methods: split the three data sets into separate sentences.
  - L97 (45 words), timing of tests: give progressors and stable eyes in separate sentences.
  - L209 (44 words), D8 in GRAPE: separate the sensitivity sentence from the specificity sentence.
  - L193 (42 words), D6 significance; L109 (41 words), validity rule; L86 (39 words), D5 definition.
  - L39 (36 words), KSP bullet; L144 (36 words); L244 (37 words); L250 (37 words); L189 (two caption sentences, 33 and 37 words).
  - L254 (34 words), the first Conclusions sentence.
- Fix: aim for 20 words or fewer per sentence in the Abstract, KSP and PLS, and 25 or fewer elsewhere.

**18. MINOR — The Supplement S1 log is not written in journal register.**
- Location: Supplement S1.
- Problems:
  - It uses capitals and arrows ("REJECTED", "BUT", "->", "=>"), internal jargon ("restart 1", "remarkable bar", "N4 benchmark + N5 protocol + N7 finding + N6 two clinics", "Honest label expected: NOT REMARKABLE") and internal file paths.
  - Round 4 (nAMD, Moorfields) is unrelated to this article.
- Fix: rewrite as a dated table (round, hypothesis, data split, result, decision). Keep all facts and the disclosure of Artes use. Move nAMD to one sentence.

**19. MINOR — Wording overreaches in summary sections.**
- Locations:
  - Abstract Conclusion: "remained as good as any valid alternative".
  - Conclusions: "In three independent data sources …".
  - PLS: "This check gave a fair estimate of the false-alarm rate."
- Fix: see Review 09. Suggested wording: "no valid alternative was shown to be more sensitive"; "in one data set with a true no-change arm, supported by one external data set"; "gave a rough estimate".

**20. MINOR — The Abstract Results sentence about D6 needs its k.**
- Location: "The only detector significantly more sensitive than the trend test, a pooled-detrended conformal test (sensitivity 56.9%), had a false-alarm rate of 22.4%."
- Fix: add "at three tests" inside the sentence.

## D. Formatting and submission completeness

**21. MINOR — Table 2 gives no CI for specificity.**
- Location: Table 2 header "Specificity, %".
- Problem: sensitivity and false alarms have CIs; specificity does not.
- Fix: add specificity CIs; they are already in `metrics.json` as `spec_lo` and `spec_hi`.

**22. MINOR — Figure legends are missing from the manuscript file.**
- Problem: they exist only in `figure_legends.json`, and the journal expects them after the references.
- Fix: insert them.

**23. MINOR — The ethics text appears twice.**
- Location: the "Ethics" subsection (Methods) and "Ethical Approval" (Declarations) are identical.
- Fix: keep one, in Declarations, as the journal's template requires, and cross-reference it from the other.

**24. MINOR — Placeholders and tense need finishing.**
- Placeholders remain for authors, affiliations, ORCID, prior presentation, funding, contributions, conflicts of interest and the repository URL.
- Data Availability says code "are available at [URL]", while the cover letter says it "will be released".
- Fix: complete the placeholders and use the same tense in both documents.

**25. MINOR — The cover letter's "pre-specified" contradicts the Supplement.**
- Location: cover letter: "We compared ten pre-specified detectors".
- Problem: Supplement S1 says "The benchmark reported in the main text was specified after round 5".
- Fix: say "detectors specified in a time-stamped protocol after the development rounds".
