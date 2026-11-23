# Review 10 — "Reviewer Zero": novelty and publishability skeptic

## Summary
Strip away the framing and the paper shows that (a) an OLS trend of mean sensitivity keeps roughly its nominal false-alarm rate, and (b) three detectors that the authors built themselves (D6 from their own failed development, plus two small home-made ML models) have inflated false-alarm rates on a 30-patient retest set. That retest set was already used for exactly this purpose (specificity of progression criteria) by Artes et al. 2014 [11]. In addition:

- none of the "complex" detectors is a published, externally validated method;
- the confirmatory sample is 26 vs 26 eyes;
- the external data set cannot assess validity;
- the main inferential claim is non-rejection of a null that the design could not reject.

I doubt this clears the novelty bar of a Q1 clinical journal.

**Recommendation: Reject in current form (resubmission possible after substantial redesign).**

## Issues

1. **FATAL — The cautionary examples are straw men the authors built themselves (Methods D6, D8, D9; Discussion para 2 "Our own development history shows the risk").**
   - D6 is the authors' own abandoned development variant. Its true-null failure (20–22% on Artes) was already known from development Round 5 on the same data (`novelty_escalation_log.md`).
   - D8 and D9 are small in-house models trained on about 190 labelled eyes (see review 05).
   - The paper says "many new methods claim to detect ... earlier" (Introduction para 3; Abstract Introduction), yet it tests *none* of the published new methods it cites: ANSWERS [14], hierarchical Bayesian [16], smoothing [10], published ML models [17–22], the Si et al. diffusion/conformal model [24].
   - The general claim ("Apparent early-detection gains were explained by false alarms") is therefore supported only for the authors' own methods.

   *Fix:* evaluate at least two or three *published* detectors with code or re-implementations (e.g., ANSWERS, PoPLR with smoothing, a published ML model), or restrict every claim to "detectors of the type we built".

2. **MAJOR — The novelty over Artes et al. 2014 [11] is not shown (Introduction para 3 "Only a few studies have measured false alarms on true no-change data [11]").** Ref. 11 already used these 12-week retest series to estimate the specificity of GPA. Ref. 8 (PoPLR) relied on permutation, i.e., a shuffle-type null. I cannot verify from the manuscript exactly what refs 8, 11 and 12 reported, and I will not characterise them further. The authors, however, need to state explicitly what is new beyond (i) more detectors and (ii) a shuffle-audit correlation of 0.65 that missed its own pre-registered target. *Fix:* add a "what is known / what this adds" paragraph with specific quantitative comparisons to [11], and cite any other retest-based specificity studies.

3. **MAJOR — The sample size makes the main result uninformative (Results RQ2; Limitations "First").** With 26 progressors and Holm over 9 comparisons, only a gain of ≥ 9 more progressors (≈ 35 pp) with no reverse discordance could reach significance (review 04 #3). The conclusion "no valid detector flagged significantly more" was close to guaranteed before the data were seen. A Q1 journal would expect an adequately powered comparison, or an explicit equivalence framing. *Fix:* use all UWHVF eyes with ≥ 8 tests for the untrained detectors (n ≈ 314 reference eyes), and train ML with cross-fitting.

4. **MAJOR — The headline claim does not follow from the evidence (Abstract Conclusion; Conclusions).** "Apparent early-detection gains were explained by false alarms that only a true no-change check revealed" overreaches:
   - D2 at k = 3 (valid, +19 pp) and D8 at k = 6 (valid, +11.5 to +13 pp) are gains that the true-null check did *not* explain away.
   - The shuffle audit, which needs no retest data, also flagged D6 and D8 at k = 3 (22.5% and 17.3%). So "only a true no-change check revealed" is contradicted by the authors' own RQ3.

   *Fix:* rewrite the conclusion to match the evidence. Acknowledge that the shuffle audit caught the same failures.

5. **MAJOR — Desk-reject risks for this journal.**
   - (a) Scope: the paper is about methods and perimetry statistics, with no therapy outcome.
   - (b) Placeholders throughout the Declarations.
   - (c) An AI-generated study design, code and manuscript with no human commit in the repository.
   - (d) "Pre-registration" in a private repository 3 minutes before implementation.
   - (e) The decisive validity rule deviates from the protocol (review 09 #1).

   Any one of (c)–(e), raised by a referee, can sink the paper. *Fix:* resolve them before submission (see reviews 01 and 09).

6. **MODERATE — The real-world translation is hypothetical (Results "Real-World Measures"; Table 3).** "224 and 277 unnecessary escalation discussions" per 1,000 eyes is 1,000 × a retest false-alarm rate under borrowed time labels. There are no clinic data on escalations. *Fix:* present it as a scenario, or drop it.

7. **MODERATE — The shuffle-audit contribution is weak (RQ3).** ρ = 0.65 missed the pre-registered ≥ 0.7, and the audit over-estimated rate and event rules by up to 10 pp. Agreement is partly built in for permutation-calibrated detectors (D4, D5, D10). The paper nonetheless recommends it to clinics (Key Summary Points bullet 5; Discussion para 3). *Fix:* recommend it only as a screen for *pooled or learned* detectors, with the over-estimation caveat stated in the Key Summary Points.

8. **MINOR — The title promises "how early".** The answer, a median of 5 tests (about 5 years) for D1, appears only in Table 3 and Results. *Fix:* put the number in the Abstract, or change the title to describe the benchmark.

## What would make it publishable
- Include published comparator methods.
- Use all eligible reference eyes for the non-learned detectors.
- Use a future-only, non-MD reference (or several).
- Report the pre-registered GRAPE labels.
- Run an honest protocol-deviation table.
- Frame the paper as an estimation or equivalence study.

A TVST-type perimetry methods journal may be a better fit than Ophthalmology and Therapy.
