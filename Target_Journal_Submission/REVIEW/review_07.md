# Review 07 — Reporting-guideline review (TRIPOD+AI; STARD 2015 for diagnostic accuracy)

Reviewer role: reporting-guideline reviewer.
Scope: the study is a benchmark of ten binary "progression" classifiers (index tests), evaluated against a
future-confirmed reference standard (E1), a true no-change arm (E2), a shuffle audit (E3) and an external data set
with rule-based labels (E4). Three of the detectors (D8–D10) are developed ML models. Accordingly, TRIPOD+AI (Collins
et al., BMJ 2024;385:e078378, doi 10.1136/bmj-2023-078378, verified via Crossref) applies to the development and evaluation of D8–D10. STARD 2015 applies to
the accuracy evaluation of all detectors against the reference standards.

Item numbers below follow the published checklists as I recall them. Note that the manuscript's reference [24] points to
10.1136/bmj.q902, which Crossref marks as a *correction* to the TRIPOD+AI article (see review 08). The authors should check the numbering against
the official PDF checklists, which I did not have in the repository. I also checked the journal's instructions
(`journal_selection/author_guidelines/I4A.txt`).

## Summary

The manuscript reports the core accuracy estimates with 95% CIs, uses public data and states that its code is
available. Many items expected by both guidelines are nevertheless missing or incomplete:

- No participant flow diagram with exclusions.
- No 2×2 cross-tabulations.
- No baseline characteristics by reference status.
- No sample-size rationale.
- No description of how indeterminate reference results and missing or unreliable test points were handled.
- No calibration or model-specification details for the ML detectors.
- No subgroup, fairness or sex/gender reporting (the journal asks for SAGER).
- No dates of data collection.
- No registration or protocol-access statement beyond a placeholder repository URL.
- No completed checklist, although the Methods say "We followed the TRIPOD+AI reporting guidance".

Journal-level formalities are also open. The main text is about 4,490 words, against "around 4,000". Line numbers,
author details, funding and competing interests are missing, and the promised supplementary files are absent.

## Missing or incomplete items

### Title and abstract

**1. MODERATE — The title and abstract do not fully identify the design.**
- Applicable items: TRIPOD+AI 1–2; STARD 1–2.
- What is missing: the title does not state "diagnostic accuracy" or "retrospective". The abstract omits:
  - the reference-standard definition (mean-TD slope < −0.3 dB/yr, p < 0.01, over ≥8 fields);
  - that "stable" means a full-series one-sided p > 0.5, i.e. a non-negative slope;
  - the number of patients behind the 26+26 eyes (41);
  - the specificity CIs.
- The abstract also does not state what sex(es) the study covers. The journal's SAGER requirement says: "Article
  titles and/or abstracts should indicate what sex(es) the study applies to".
- Fix: add "retrospective diagnostic-accuracy benchmark" to the title or subtitle. In the abstract, add one clause
  each defining the reference standard, the stable class, the patient counts and the sex distribution.

### Introduction

**2. MINOR — The intended clinical role of the index tests is not stated.**
- Applicable items: STARD 3–4; TRIPOD+AI 3a–c.
- What is missing: the intended use is implied (escalation decisions) but not stated. Readers are not told whether a
  flag is meant to be a triage, add-on or replacement test, at which visit, or in which population (suspects versus
  manifest glaucoma).
- TRIPOD+AI also asks whether health inequalities are known for the target population; this is not addressed.
- Fix: add one sentence defining the clinical role and target population.

### Methods: sources, participants, eligibility

**3. MAJOR — Dates, settings and eligibility are incompletely reported.**
- Applicable items: STARD 5–9; TRIPOD+AI 5a–b, 6a–c.
- What is missing:
  - (a) The calendar periods of data collection for UWHVF, Artes and GRAPE.
  - (b) The care setting and inclusion criteria of each source (UWHVF has no diagnosis, so the population is "all
    patients with 24-2 tests", not "glaucoma"). The Methods say this, but the Abstract and Introduction present the
    study as glaucoma progression.
  - (c) How eyes were sampled: consecutive versus convenience; Artes recruitment criteria.
  - (d) Whether any reliability filtering was applied. None was possible for UWHVF. Artes provides FP/FN/fixation
    losses (`load_artes` reads `fpr`, `fnr`, `fl`) but they were not used or reported. For GRAPE, reliability was not
    reported.
  - (e) The eligibility rule "≥3 fields" (E2–E4) and "≥8 fields" (E1).
- Fix: add a "Participants" paragraph per data set covering items (a)–(e), and report reliability distributions for
  Artes and GRAPE.

**4. MAJOR — There is no flow diagram with numbers at each step.**
- Applicable items: STARD 19; TRIPOD+AI 20a.
- What is missing: Fig. 1 is a design schematic. Required numbers include:
  - UWHVF: 3,871 patients / 7,428 eyes → split → test 869 eyes with ≥3 fields → 132 with ≥8 → 26 progressors,
    26 stable, 80 indeterminate.
  - The PoPLR secondary reference (58 progressors; stable count not reported).
  - Artes: 30 eyes → 300/270/240/210 windows × 10 draws.
  - GRAPE: 263 eyes → 163 with ≥4 fields; 27 / 18 MD-label progressors.
  - Per-eye exclusions of GRAPE points: 86 eyes lost at least one point; the minimum is 10 of 59 points.
- Fix: add a STARD-style flow diagram, as a separate figure or in the supplement.

**5. MAJOR — There is no sample-size or precision rationale.**
- Applicable items: STARD 18; TRIPOD+AI 9.
- What is missing: the protocol contains no power calculation. With 26 progressors, the McNemar comparison can detect
  only differences of about 35 points or more, and CIs on sensitivity span about ±20 points. For D8/D9 development,
  the number of events (93 progressors and 99 stable train eyes) and the 39 validation-stable eyes used to set the
  95%-specificity threshold are not reported.
- Fix: report all of these counts. Add a sentence stating that the sample size was fixed by data availability, and
  give the minimum detectable difference.

### Methods: reference standard and index tests

**6. MAJOR — The rationale for the reference standard, the handling of indeterminate cases and verification bias are
not reported.**
- Applicable items: STARD 10b, 11, 13b, 15, 16; TRIPOD+AI 7a–b (outcome).
- What is missing:
  - (a) The rationale for the −0.3 dB/yr, p < 0.01, p > 0.5 cut-offs, and a citation.
  - (b) A plain statement that "stable" eyes have a positive full-series slope.
  - (c) The fact that the reference is computed on data that include the index-test fields (incorporation bias).
    This is disclosed in `leakage_audit.md` ("partial verification") but only obliquely in the paper.
  - (d) How the 80 indeterminate eyes (61% of eligible eyes) were handled, and the resulting spectrum bias:
    sensitivity and specificity are estimated on extreme cases only.
  - (e) Partial verification: only eyes with ≥8 fields could be verified, so the population with short follow-up
    (the actual target of "few tests") is not represented in E1.
  - (f) Reference-standard readers and blinding are not applicable (algorithmic), and the paper should say so.
- Fix: add these points to "Reference standard" and Limitations. Report sensitivity and specificity with
  indeterminates assigned in both directions as a sensitivity analysis.

**7. MODERATE — The index tests are not specified precisely enough to reproduce.**
- Applicable items: STARD 10a, 12a–b; TRIPOD+AI 8, 12a–e.
- What is missing:
  - D7: the definition of the "short interval" (≤0.5 years), the binning by single-test sensitivity, the ≥200-pair
    rule and the interpolation.
  - D5: the strata cut-offs (<20, 20–26, ≥26 dB) and the fallback to the pooled reference when a stratum has <50
    values.
  - D6: the region definitions.
  - D8: the 14 features are not listed; the 12-configuration grid is not given; there is no statement that
    selection used validation AUC.
  - D9: architecture, loss weighting (`pos_weight`), epochs and input scaling.
  - D10: architecture and training objective (contrastive versus 31 shuffles; training windows of 3–8 tests).
- Positivity thresholds are given for most detectors. For D8/D9 the numeric threshold per k is not reported.
- Fix: add a supplementary table giving the exact rule, threshold and parameters for each detector, including the D8
  feature list and the hyperparameter grids.

**8. MODERATE — Missing data and handling of predictors are not described.**
- Applicable items: TRIPOD+AI 10 and 13; STARD 16.
- What is missing:
  - GRAPE points coded −1 are dropped per eye if missing at any visit, so eyes have from 10 to 59 points. This is not
    reported; Table 1 says "59 analysable points".
  - UWHVF masked values: `MASK_VALUE = 100` is defined in the loader but its handling is not reported.
  - The handling of same-day or near-duplicate tests (159 intervals of less than 0.05 years in UWHVF) is not reported.
- Fix: report each of these and how it was handled.

**9. MODERATE — Model specification and the ML development process are incompletely reported.**
- Applicable items: TRIPOD+AI 12a–g (analysis), 15 (model output), 16 (class imbalance), 17 (fairness), 18 (model
  output).
- What is missing:
  - No calibration assessment for D8/D9. Probabilities are thresholded, but calibration-in-the-large or a calibration
    plot on validation/test data is not reported.
  - The handling of class imbalance is not reported (D9 uses `pos_weight`; D8 has none).
  - No fairness or subgroup assessment by sex, age or baseline severity. UWHVF provides gender.
  - No statement on how the model output is turned into a flag at the point of care.
  - The trained D8/D9/D10 models are not released.
- Fix: add calibration on the validation set and per k. Report imbalance handling. Add subgroup sensitivity,
  specificity and false-alarm rates by sex and baseline MD tertile (where n permits). Release the models.

### Methods: analysis

**10. MODERATE — The statistical methods do not match the code, and the validity rule is not pre-specified.**
- Applicable items: STARD 14–15; TRIPOD+AI 12.
- What is missing:
  - The paired CIs use an eye-level bootstrap and the McNemar tests are not clustered, while the text implies patient
    clustering.
  - Majority vote across seeds is used for the paired tests.
  - The validity rule differs from the protocol (see reviews 05 and 06).
  - No measures of uncertainty are given for the Spearman ρ (the protocol promised a bootstrap CI).
- Fix: correct the descriptions and analyses.

**11. MINOR — Registration and protocol access are inadequate.**
- Applicable items: STARD 28–29; TRIPOD+AI 4 (protocol), 18c (registration).
- What is missing: the protocol is an internal repository file. The repository URL is "[TO BE INSERTED]". There is
  no registration.
- Fix: deposit the protocol with a DOI (OSF / Zenodo) and state "not registered; protocol time-stamped at <commit
  hash>".

### Results

**12. MAJOR — There are no cross-tabulations and no baseline characteristics by reference status.**
- Applicable items: STARD 20, 23; TRIPOD+AI 20b.
- What is missing:
  - 2×2 tables (index result × reference result) for each detector at each k. They are simple to derive from
    `raw_results.csv.gz`.
  - Baseline characteristics (age, sex, baseline MD, number of fields, follow-up) of progressors versus stable versus
    indeterminate eyes. They are computed in `descriptives.json` (`ref_prog_*`, `ref_stable_*`) but not reported.
  - The distribution of severity in the target condition.
- Fix: add a Table 1b with characteristics by reference class, and supplementary 2×2 tables.

**13. MODERATE — Some accuracy estimates and uncertainty measures are missing.**
- Applicable items: STARD 24; TRIPOD+AI 23a.
- What is missing:
  - Specificity CIs are not shown in Table 2. The table reports sensitivity / false-alarm rate without CIs, which are
    only in a Supplementary Table S1 that does not exist as a file in the repository (only
    `tables/table_metrics_all.csv`).
  - Secondary-reference specificity and n.
  - Seed SDs per cell.
  - Likelihood ratios or predictive values at realistic prevalence would help clinical readers.
- Fix: put CIs in the main table or ship the supplementary tables. Add PPV/NPV at an assumed prevalence of
  progression per review.

**14. MODERATE — Indeterminate or structurally impossible index results are not reported as such.**
- Applicable item: STARD 24/25.
- What is missing: D4, D7 and D10 cannot return a positive result at k=3, and D7 cannot at k<4. Their "0% sensitivity
  / 100% specificity" is reported as if it were an accuracy estimate.
- Fix: report these cells as "not applicable / structurally negative" and exclude them from summaries such as the RQ3
  agreement statistics.

**15. MODERATE — Sex/gender (SAGER, journal requirement) is not addressed.**
- Applicable items: journal instructions; TRIPOD+AI 14 and 20b.
- What is missing: the sex distribution of any data set, sex-disaggregated results, or a rationale for not reporting
  them.
- Fix: report the sex distribution for UWHVF reference eyes (the `gender` field exists) and for GRAPE (if available),
  and state the reason if Artes sex data are unavailable. Add a sentence to the Discussion.

### Discussion and other information

**16. MODERATE — The limitations are incomplete.**
- Applicable items: STARD 26–27; TRIPOD+AI 24–26.
- Missing limitations:
  - Spectrum bias from excluding 61% of eligible eyes as indeterminate.
  - The positive-slope definition of "stable".
  - Short-term-only noise in the no-change arm, and its specific consequence for rate-based rules.
  - The perimeter-scale shift in GRAPE for D8.
  - Development-phase knowledge of D6's invalidity.
  - Underpowered comparisons, with gains of up to 30–40 points not excluded.
- Fix: add each to Limitations.

**17. MINOR — Declarations, AI-use statement and journal formalities are incomplete.**
- Applicable items: TRIPOD+AI 3–5 (other information: funding, conflicts, data/code availability, patient and public
  involvement); journal file checklist.
- What is missing:
  - Funding, conflicts of interest and author contributions are placeholders.
  - There is no patient and public involvement statement (TRIPOD+AI asks for one).
  - The AI-use statement exists but needs author confirmation. The journal requires a description of AI use "including
    ... drafting ... data analysis".
  - There are no line numbers (required by the file checklist).
  - The main text is about 4,490 words (guide "around 4,000").
  - Supplementary Tables S1/S2 and Note S1 are referenced but not provided as files.
  - The code URL is a placeholder.
- Fix: complete these before submission.

**18. MINOR — No completed checklists.**
- What is missing: the Methods claim adherence to TRIPOD+AI, but no checklist with page or line numbers is provided,
  and STARD is not mentioned.
- Fix: provide completed TRIPOD+AI and STARD 2015 checklists as supplementary files, and cite STARD (Bossuyt et al.,
  BMJ 2015). Verify the DOI before citing; I did not query it.

## Recommendation

**Major revision for reporting.** None of these items requires new data. Several require modest new analyses from
existing outputs: the flow diagram, 2×2 tables, characteristics by reference status, calibration for D8/D9, sex
distribution, and indeterminate-handling sensitivity analyses. The most important omissions for a diagnostic-accuracy
reader are the flow diagram (item 4), the reference-standard and spectrum issues (item 6), the cross-tabulations and
characteristics by reference status (item 12), and the sample-size rationale (item 5).
