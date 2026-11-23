# Review 08 — Literature and novelty review

Reviewer role: literature and novelty reviewer (adversarial).

Sources:
- `manuscript/manuscript_filled.md` (numbered reference list), `manuscript/references.json`.
- `journal_selection/novelty_map.csv`, `journal_selection/novelty_escalation_log.md`, `journal_selection/novelty_scorecard.md`.
- Crossref REST API queries made on 2026-11-23 for the metadata or abstracts of [9], [11], [13], [21]–[25], [32],
  [34], [35], [37], [30], [17]–[20] and for candidate missing works. Crossref returned abstracts only for [19], [21],
  [23] and [30]. For the other cited works I judged support from the title, the venue and the authors' own
  `novelty_map.csv` notes. Where that was insufficient, I mark the item UNVERIFIED.
- The visualFields 1.0.7 package documentation in `data_raw/ext/visualFields`.

## Summary

The core contribution is new as far as I can tell. I know of no prior paper that benchmarks a broad panel of
visual-field progression detectors on true no-change retest data, a future-confirmed reference and an external clinic
together, at 3–6 fields. The authors' own novelty map supports this, and the manuscript does not use the word "first".

The novelty *framing* has four problems:

- **Prior shuffle-based work is under-acknowledged.** The paper presents the shuffle audit as something it adds. Random
  re-ordering of series to estimate specificity is long established (Artes 2014 [9] used 1,000 random reorderings of
  the same retest series, per the authors' novelty map; [13] and [14] matched false-positive rates by permutation). The
  genuinely new piece is the *calibration of the shuffle estimate against a true null*.
- **"Standard specificity estimates" is too broad.** The paper's own RQ3 shows that the classical permutation approach
  largely *worked*. The method that failed was specificity in label-defined stable eyes, the approach typical of
  supervised ML papers. The Abstract and Conclusion blur this distinction.
- **The tested detectors are not the published ones.** The generalisation "many new detectors claim earlier detection
  ... their gains are false alarms" is not tested on the published detectors the Introduction cites ([12]–[22]). The
  "new" detectors that failed are the authors' own D6 (known to be invalid in development), a generic LightGBM and a
  GRU. None of ANSWERS, the hierarchical Bayesian model, the VAE, the ConvLSTM or the archetype method was evaluated.
- **Several citations are mis-characterised, and the TRIPOD+AI reference points to a correction notice.** These are
  [29] (Freedman–Lane), [15]–[20] ("supervised"), [23] ("may not transfer") and [24].

Important prior comparative work on progression criteria and their specificity is missing.

## A. Citation-by-citation check

| Location (quote) | Ref(s) | Supports? | Comment |
|---|---|---|---|
| "About 76 million ... 2020 ... about 112 million by 2040" | [1] Tham 2014 | Yes | Standard source |
| "Treatment lowers intraocular pressure and slows visual loss" | [2] Weinreb 2014; [3] Heijl 2002 (EMGT) | Yes | |
| "the noise grows as sensitivity falls" | [4] Gardiner 2014 | Yes (title: reliability of SAP in regions of damage) | |
| "Expert guidance suggests six tests in the first two years" | [5] Chauhan 2008 | Yes | |
| "Delays in follow-up are a documented cause of avoidable sight loss" | [6] Foot & MacEwen 2017 | Yes (title) | |
| "Trend methods fit a line through the mean deviation or through each test location" | [7] PoPLR; [8] VFI | Partly | [8] regresses VFI, not MD. [7] is a permutation method built on pointwise regression. A classical MD/PLR source would fit better (e.g. McNaught 1996, see C). |
| "Event methods compare each follow-up test with a baseline, using limits taken from stable patients" | [9]–[11] | Yes | [11] compares EMGT/AGIS/CIGTS criteria. Acceptable. |
| "Permutation methods, such as PoPLR, compare the eye's real test order with shuffled orders" | [7] | Yes | |
| "Bayesian and spatial models share information across locations or patients" | [12] ANSWERS; [13] PoPLR vs ANSWERS; [14] hierarchical Bayesian | Mostly | [13] is a comparison study, not a model paper. Per `novelty_map.csv` it estimated false-positive rates "by permuting the same series", which is prior art relevant to the shuffle audit and should be cited for that too. |
| "machine-learning models have been trained to classify or forecast progression" | [15]–[20] | Yes | |
| "some newer studies use deep generative models or risk-based test scheduling" | [21] Chen 2026 (medRxiv); [22] Si 2025 (MICCAI) | Yes | [21] is a **preprint posted 2026-11-18** (Crossref `posted-content`). Label it "[Preprint]" and check whether a peer-reviewed version exists at submission. [22] is missing the conference/volume name. |
| "Only a few studies have measured false alarms on true no-change data ... [9]" | [9] Artes 2014 | Yes | The full title is "Visual field progression in glaucoma: what is the specificity of the Guided Progression Analysis?" (visualFields documentation); the reference list truncates it to "Visual Field Progression in Glaucoma". The text should also report what [9] found. Per the authors' novelty map it found mean false-positive rates of 2.6% ("likely") and 18.5% ("possible") after 10 tests, so the *problem* of false alarms under no change was already shown. |
| "labels for 'progression' differ ..., and models trained on one label may not transfer" | [23] Kim 2026 | Partly | Its abstract shows that ML performance depends strongly on the labeling strategy (Consensus vs Wiggs' label) and that differences "reflect model-label compatibility". Per the abstract, it does not test cross-label *transfer*. Reword to "performance depends strongly on the label definition". |
| "We followed the TRIPOD+AI reporting guidance" | [24] | **Wrong DOI** | 10.1136/bmj.q902 is, per Crossref, a *correction* notice (`update-to` → 10.1136/bmj-2023-078378, type "correction"), and the reference has no authors. Cite Collins GS, Moons KGM, Dhiman P, et al. BMJ 2024;385:e078378, doi 10.1136/bmj-2023-078378 (verified via Crossref). |
| UWHVF description | [25] Montesano 2022 | Yes | Crossref lists DOI tvst.11.1.1 with article number 2. This is consistent with Crossref, so it is not an error by the authors. |
| Artes data distributed with visualFields | [26] Marín-Franch & Swanson 2013 | Yes, for the package | Licence error elsewhere (see review 06): visualFields 1.0.7 is Apache-2.0, not GPL-3. |
| GRAPE labels: "MD slope p < 0.05 ... PLR2, PLR3" | [27] Huang 2023 | UNVERIFIED in detail | Crossref has no abstract. The authors' protocol originally called these "clinician-applied criteria". Check the label definitions against the data descriptor's text. |
| D4 PoPLR | [7] | Yes | |
| D5 "a conformal p-value" | [28] Angelopoulos & Bates | Yes (general) | |
| D6 "builds the reference from detrended, shuffled series"; Discussion "borrowed its null distribution from other patients' detrended and shuffled series [28, 29]" | [29] Freedman & Lane 1983 | **Mis-characterised** | Freedman–Lane permutes the residuals of the *reduced* (null) model, which here is mean only, i.e. a plain shuffle. D6 removes each eye's *own fitted trend* (full-model residuals), which is closer to ter Braak's method. That difference is exactly why D6 is anti-conservative with one residual df. Cite a source that describes the method actually used, e.g. Anderson & Legendre 1999 (doi 10.1080/00949659908811936, verified), which compares Freedman–Lane, ter Braak and others, and call the D6 null "full-model residual permutation". |
| D7 "similar in spirit to Guided Progression Analysis" | [11] | Weak | [11] is a comparison of trial criteria. Cite a GPA-specific description, or [9], which evaluated GPA. |
| D10 permutation with a learned statistic | [30] Gagnon-Bartsch & Shem-Tov 2019 | Yes (analogy) | The abstract confirms a classifier-based permutation test. |
| "The permutation p-values included the observed order, so they are never zero" | [31] Phipson & Smyth | Yes | For k ≤ 6 the code uses exact enumeration, so [31]'s random-permutation argument applies only to the secondary reference (2,000 random permutations). |
| "Methods that pool information ... can add power" | [12]–[14] | Yes | |
| "supervised models are increasingly proposed for this task" | [15]–[20] | **Partly wrong** | [19] (VAE) and [20] (Gaussian mixture, "Unsupervised" in the title) are unsupervised. [18] is forecasting. Cite only [15]–[17] here, or say "machine-learning models". |
| "Artes and colleagues previously used the same retest series to estimate the specificity of the Guided Progression Analysis" | [9] | Yes | The novelty map records that [9] also used random reorderings. The next sentence, "add a check that any clinic can run without retest data", should acknowledge that reordering-based specificity is established practice ([9], [13], [14]). |
| "routine testing frequencies delay the identification of progression" | [32] Wu 2017; [33] Crabb & Garway-Heath 2012; [34] Stagg 2026 | Yes (titles) | |
| "Testing more often early in follow-up [5], clustering tests [35], personalised schedules [21, 36] or smoothing [37]" | | Yes | [21] is a preprint (see above). |

## B. Novelty assessment

**What is new, based on the novelty map and my searches:** a single open benchmark with all of the following:
- a true no-change arm, time-rescaled to clinical spacing (amendment A1);
- a future-confirmed reference;
- an external perimeter;
- ten detectors at 3–6 fields;
- an empirical calibration of the shuffle estimate against the true no-change estimate.

**What is not new:**
- Measuring GPA specificity on these retest data, which is [9].
- Estimating specificity by reordering series ([9]; [13] and [14] per the novelty map; Wu & Medeiros [10] matched
  specificity by simulation).
- The PoPLR floor at k=3, which follows directly from [7].
- The observation that progression definitions disagree ([11], [23], and the method-comparison literature in C).

## C. Important missing prior work

DOIs listed were confirmed to exist with matching title, authors and venue via Crossref on 2026-11-23. Crossref
returned no abstracts for them, so the **content relevance** stated is based on title or common knowledge and is marked
UNVERIFIED where it is a specific claim. The authors must read each before citing. Crossref confirmed the surnames of the first three
authors only; the initials below are from memory and must be checked.

1. Nouri-Mahdavi K, Brigatti L, Weitzman M, et al. Comparison of methods to detect visual field progression in
   glaucoma. *Ophthalmology* 1997;104:1228–1236. doi 10.1016/s0161-6420(97)30153-5. This is a classical comparison of
   progression criteria showing that they disagree.
2. Vesti E, Johnson CA, Chauhan BC. Comparison of different methods for detecting glaucomatous visual field
   progression. *IOVS* 2003;44:3873. doi 10.1167/iovs.02-1171. A comparison of methods, including specificity
   (UNVERIFIED detail).
3. Rabiolo A, Morales E, Mohamed L, et al. Comparison of methods to detect and measure glaucomatous visual field
   progression. *TVST* 2019;8(5):2. doi 10.1167/tvst.8.5.2. A modern multi-method comparison. Whether it matched
   specificity by permutation is UNVERIFIED.
4. Artes PH, Nicolela MT, LeBlanc RP, Chauhan BC. Visual field progression in glaucoma: total versus pattern deviation
   analyses. *IOVS* 2005;46:4600. doi 10.1167/iovs.05-0827. From the same group as the retest data; relevant to
   whether D1–D3 should use sensitivity, TD or PD.
5. Bryan SR, Eilers PHC, Lesaffre EMEH, et al. Global visit effects in point-wise longitudinal modeling of
   glaucomatous visual fields. *IOVS* 2015;56:4283. doi 10.1167/iovs.15-16691. Relevant because visit-level shared
   fluctuation is a mechanism for false alarms that pooled or pointwise nulls ignore (UNVERIFIED detail).
6. Turpin A, McKendrick AM. What reduction in standard automated perimetry variability would improve the detection of
   visual field progression? *IOVS* 2011;52:3237. doi 10.1167/iovs.10-6255. Supports "the limit is information, not
   the detector", which is the paper's Discussion claim.
7. Yousefi S, Kiwaki T, Zheng Y, et al. Detection of longitudinal visual field progression in glaucoma using machine
   learning. *Am J Ophthalmol* 2018;193:71–79. doi 10.1016/j.ajo.2018.06.007. An ML progression detector. Whether
   it estimated specificity on a short-interval stable/retest cohort is **UNVERIFIED**. If it did, it directly
   qualifies the claim "Only a few studies have measured false alarms on true no-change data".
8. Wu Z, Crabb DP, Chauhan BC, et al. Improving the feasibility of glaucoma clinical trials using trend-based visual
   field progression end points. *Ophthalmol Glaucoma* 2019;2:72–77. doi 10.1016/j.ogla.2019.01.004. Trend versus
   event end points, with specificity considerations (UNVERIFIED detail).
9. Tan, Montesano, Bell, et al. Refining visual field trend progression criteria in glaucoma. *Ophthalmol Glaucoma*
   2026;9:372–379. doi 10.1016/j.ogla.2026.01.004. Very recent and directly on trend criteria; it must be read
   and likely cited. Content UNVERIFIED.
10. McNaught AI, Crabb DP, Fitzke FW, et al. Visual field progression: comparison of Humphrey Statpac and pointwise
    linear regression analysis. *Graefe's Arch Clin Exp Ophthalmol* 1996;234:411–418. doi 10.1007/bf02539406. A
    classical PLR source for the "trend methods" sentence.
11. Kummet CM, Zamba KD, et al. Refinement of pointwise linear regression criteria for determining glaucoma
    progression. *IOVS* 2013. doi 10.1167/iovs.13-11680. Also De Moraes CG, Liebmann JM, et al., *Clin Exp
    Ophthalmol* 2011, doi 10.1111/j.1442-9071.2011.02680.x. Both concern PLR criteria and their false-positive
    behaviour (UNVERIFIED detail). They are relevant to D3.
12. Anderson MJ, Legendre P. An empirical comparison of permutation methods for tests of partial regression
    coefficients in a linear model. *J Stat Comput Simul* 1999;62:271–303. doi 10.1080/00949659908811936. This is the
    correct statistical source for the D6 residual-permutation discussion.
13. Gardiner SK, Crabb DP (2002, IOVS), on pointwise linear regression criteria with specificity estimated from
    reordered series: **UNVERIFIED**. A Crossref search did not return it. Locate it and verify before citing.
14. STARD 2015 (Bossuyt et al., BMJ 2015): its DOI was not verified by my query (**UNVERIFIED**). It is needed if the
    paper reports diagnostic accuracy (review 07).

## D. Issues

**1. MAJOR — The generalisation goes beyond the detectors tested.**
- Location: Abstract Introduction ("Many new detectors claim to find ... earlier"); Conclusion ("the largest apparent
  gains in early detection ... came with false-alarm rates far above the nominal level"); Key Summary Points.
- Problem: none of the published detectors in [12]–[22] was re-implemented. The failing "new" detectors are a
  home-made conformal variant already known to be invalid (D6; review 06, issue 1), a generic LightGBM and a GRU
  trained on 192 eyes.
- Fix: state explicitly that D5, D6 and D10 are the authors' constructions and D8/D9 are generic re-implementations
  of the *training-and-thresholding practice*, not of any published model. Restrict the conclusion to "detectors
  thresholded on label-defined stable eyes" and "pooled nulls with few residual degrees of freedom". Ideally, add at
  least one published, open detector (for example, a public implementation of ANSWERS or the hierarchical Bayesian
  model, if available).

**2. MAJOR — "Standard specificity estimates" is over-broad, and the shuffle audit's novelty is overstated.**
- Location: Abstract ("false alarms that standard specificity estimates missed"); Discussion ("add a check that any
  clinic can run without retest data"); Key Summary Point 1 ("most are judged by how many eyes they flag").
- Problem: the paper's own data show that the reorder/permutation approach used in the classical literature ([9],
  [13], [14]) tracked the true null reasonably well. Only label-defined stable-eye specificity failed. The Key Summary
  Point that "most are judged by how many eyes they flag" is uncited, and the authors' novelty map contradicts it.
- Fix:
  - Write "specificity in reference-stable eyes" instead of "standard specificity estimates".
  - Credit [9], [13] and [14] for reordering-based specificity.
  - Describe the contribution as "the first comparison of reordering-based against true no-change false-alarm rates
    across many detectors". Verify that no such comparison exists, e.g. in [9] itself.
  - Either delete Key Summary Point 1 or support it with a citation.

**3. MODERATE — The TRIPOD+AI citation [24] points to a correction notice and has no authors.**
- Fix: use doi 10.1136/bmj-2023-078378 (Collins GS, Moons KGM, Dhiman P, et al. BMJ 2024;385:e078378).

**4. MODERATE — [29] Freedman & Lane is mis-characterised for D6.**
- Fix: as in the table above. Also correct the code docstring.

**5. MODERATE — [15]–[20] are called "supervised" and [23] is said to show "may not transfer".**
- Fix: reword both, as in the table above.

**6. MODERATE — [9] is cited without its key finding.**
- Problem: [9] already showed high false-positive rates for GPA "possible progression" on these no-change data (per
  the authors' own novelty map; confirm against the paper). Omitting this makes the problem look newer than it is.
- Fix: state [9]'s finding in the Introduction.

**7. MODERATE — Missing prior comparative and specificity literature (section C).**
- Fix: add at least items 1–3, 6, 9 and 12, after reading them.

**8. MINOR — Reference-list quality.**
- [9]'s title is truncated.
- [21] is not marked as a preprint, and it was posted 5 days before this review. Re-check its status at submission.
- [22] is missing the proceedings volume.
- There are double periods ("Trans. Vis. Sci. Tech..", "Invest. Ophthalmol. Vis. Sci..").
- [24] has no authors.
- Page ranges are incomplete in [2], [3], [7] and others. Use the journal's (Springer/Adis) reference style.

**9. MINOR — Possible author overlap with the GEAR preprint.**
- [21] describes a scheduling policy (GEAR) evaluated with a VF-only adaptation on UWHVF. If any author of this
  manuscript is an author of [21], declare it. I could not determine authorship overlap because the author fields are
  placeholders.

## Recommendation

**Major revision (framing).** The benchmark is a useful and, to my knowledge, novel combination. However, the claims
need to be narrowed to what was tested: in-house and generic detectors, and specificity in label-defined stable eyes.
Prior reordering-based specificity work must be credited, the shuffle audit presented as a calibration study rather
than a new tool, the wrong TRIPOD+AI DOI and the Freedman–Lane mischaracterisation corrected, and the missing
comparative literature engaged.
