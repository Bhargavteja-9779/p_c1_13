# Prior-art search log (v2) - hostile recheck

Date of all searches: 2026-11-23 (system date). Run from Bash with python urllib (scripts in session scratchpad).
Framing searched: open benchmark of 10 VF progression detectors at 3-6 tests, true no-change arm (Artes 2014 retest), shuffle audit, ML miscalibration, UWHVF/GRAPE.

## Sources reached
- Europe PMC REST (search, resultType=core; abstracts read from API) - OK. Note: adding sort=RELEVANCE returned HTTP 503 twice (logged as ERROR); queries re-run without sort.
- OpenAlex API (works search, with/without publication-date filters) - OK.
- NCBI E-utilities (PubMed esearch/esummary) - OK.
- Crossref REST (query.bibliographic) - OK, used for verifying DOIs of non-biomedical items.
- arXiv API (https://export.arxiv.org) - OK (http:// returned 301; switched to https).
- medRxiv/bioRxiv API (api.biorxiv.org) - reachable (HTTP 200) but has no keyword search; medRxiv/Research Square preprints were found through Europe PMC (SRC:PPR) and OpenAlex instead.

## Sources NOT reached / not used
- Semantic Scholar Graph API: HTTP 429 (rate-limited) on two attempts; not used.
- Google Scholar: HTTP 403; not used (no bypass attempted).
- Publisher full-text pages (ScienceDirect, Wiley, IEEE, ARVO full text): not attempted per instructions; ALL assessments below are from API abstracts only. Full texts were NOT read, so methods details not stated in abstracts (e.g., whether a paper also compared shuffled-clinic FAR with retest FAR inside its results) are UNVERIFIED.
- Scopus / Web of Science / Embase: no access.

## Queries (source, query, hit count as reported by the API)

| # | date | source | query | hits |
|---|---|---|---|---|
| 1 | 2026-11-23 | EuropePMC | `"visual field" progression (specificity OR "false positive") (retest OR "test-retest" OR stable)` | 3376 |
| 2 | 2026-11-23 | EuropePMC | `TITLE_ABS:"visual field" AND TITLE_ABS:progression AND (TITLE_ABS:"test-retest" OR TITLE_ABS:"retest") AND (TITLE_ABS:specificity OR TITLE_ABS:"false positive" OR TITLE_ABS:"false-positive")` | ERROR HTTP Error 503:  |
| 3 | 2026-11-23 | EuropePMC | `TITLE_ABS:"visual field" AND TITLE_ABS:progression AND (TITLE_ABS:permutation OR TITLE_ABS:permuted OR TITLE_ABS:shuffled OR TITLE_ABS:"reordered" OR TITLE_ABS:"re-ordered")` | ERROR HTTP Error 503:  |
| 4 | 2026-11-23 | EuropePMC | `TITLE_ABS:"visual field" AND TITLE_ABS:progression AND (TITLE_ABS:"test-retest" OR TITLE_ABS:"retest") AND (TITLE_ABS:specificity OR TITLE_ABS:"false positive" OR TITLE_ABS:"false-positive")` | 26 |
| 5 | 2026-11-23 | EuropePMC | `TITLE_ABS:"visual field" AND TITLE_ABS:progression AND (TITLE_ABS:permutation OR TITLE_ABS:permuted OR TITLE_ABS:shuffled OR TITLE_ABS:"reordered" OR TITLE_ABS:"re-ordered")` | 29 |
| 6 | 2026-11-23 | EuropePMC | `TITLE_ABS:"visual field" AND TITLE_ABS:progression AND (TITLE_ABS:"stable glaucoma" OR TITLE_ABS:"stable eyes" OR TITLE_ABS:"no change" OR TITLE_ABS:"short-term" OR TITLE_ABS:"weekly") AND (TITLE_ABS:specificity OR TITLE_ABS:"false positive" OR TITLE_ABS:"false-positive" OR TITLE_ABS:"false progression")` | 60 |
| 7 | 2026-11-23 | EuropePMC | `TITLE_ABS:"visual field" AND TITLE_ABS:progression AND (TITLE_ABS:"number of visual fields" OR TITLE_ABS:"number of tests" OR TITLE_ABS:"how many" OR TITLE_ABS:"frequency of testing" OR TITLE_ABS:"time to detect")` | 34 |
| 8 | 2026-11-23 | EuropePMC | `TITLE_ABS:"visual field" AND TITLE_ABS:progression AND (TITLE_ABS:"deep learning" OR TITLE_ABS:"machine learning" OR TITLE_ABS:"artificial intelligence" OR TITLE_ABS:"neural network") AND (TITLE_ABS:detect OR TITLE_ABS:detection OR TITLE_ABS:identify)` | 73 |
| 9 | 2026-11-23 | OpenAlex | `Chauhan practical recommendations measuring rates of visual field change glaucoma` | 529 |
| 10 | 2026-11-23 | OpenAlex | `Montesano open source dataset perimetry university of washington` | 26 |
| 11 | 2026-11-23 | OpenAlex | `GRAPE multi-modal dataset longitudinal follow-up visual field glaucoma` | 48 |
| 12 | 2026-11-23 | OpenAlex | `Nouri-Mahdavi comparison methods detect visual field progression glaucoma` | 821 |
| 13 | 2026-11-23 | OpenAlex | `Nouri-Mahdavi influence visual field testing frequency detection glaucoma progression` | 282 |
| 14 | 2026-11-23 | EuropePMC | `AUTH:"Nouri-Mahdavi K" AND TITLE:"visual field" AND (TITLE:progression OR TITLE:frequency OR TITLE:detect*)` | 21 |
| 15 | 2026-11-23 | EuropePMC | `AUTH:"Artes PH" AND (TITLE:retest OR TITLE:variability OR TITLE:specificity OR TITLE:"false")` | 4 |
| 16 | 2026-11-23 | arXiv | `all:"visual field" AND all:glaucoma AND all:progression` | 16 |
| 17 | 2026-11-23 | arXiv | `abs:perimetry AND abs:progression` | 4 |
| 18 | 2026-11-23 | EuropePMC | `SRC:PPR AND (TITLE_ABS:"visual field" OR TITLE_ABS:perimetry) AND TITLE_ABS:glaucoma AND (TITLE_ABS:progression OR TITLE_ABS:worsening) AND FIRST_PDATE:[2024-06-01 TO 2026-12-31]` | 29 |
| 19 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"visual field" OR TITLE_ABS:perimetry) AND TITLE_ABS:glaucoma AND (TITLE_ABS:progression OR TITLE_ABS:worsening) AND (TITLE_ABS:"deep learning" OR TITLE_ABS:"machine learning" OR TITLE_ABS:transformer OR TITLE_ABS:"recurrent") AND FIRST_PDATE:[2025-05-01 TO 2026-12-31]` | 24 |
| 20 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"visual field" OR TITLE_ABS:perimetry) AND (TITLE_ABS:"random order" OR TITLE_ABS:"randomly reordered" OR TITLE_ABS:"re-ordered" OR TITLE_ABS:"reorderings" OR TITLE_ABS:"permutation distribution" OR TITLE_ABS:"permutations of")` | 93 |
| 21 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"visual field" OR TITLE_ABS:perimetry) AND (TITLE_ABS:"global visit effect" OR TITLE_ABS:"global visit effects" OR TITLE_ABS:"correlated noise" OR TITLE_ABS:"spatially correlated")` | 17 |
| 22 | 2026-11-23 | EuropePMC | `TITLE_ABS:"optical coherence tomography" AND TITLE_ABS:glaucoma AND TITLE_ABS:progression AND (TITLE_ABS:"false positive" OR TITLE_ABS:"false-positive" OR TITLE_ABS:specificity) AND (TITLE_ABS:permutation OR TITLE_ABS:"test-retest" OR TITLE_ABS:"healthy eyes" OR TITLE_ABS:"stable")` | 19 |
| 23 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"eGFR slope" OR TITLE_ABS:"GFR slope") AND (TITLE_ABS:"false positive" OR TITLE_ABS:"type I error" OR TITLE_ABS:noise OR TITLE_ABS:"measurement error") AND (TITLE_ABS:"number of measurements" OR TITLE_ABS:"short-term" OR TITLE_ABS:variability)` | 1 |
| 24 | 2026-11-23 | OpenAlex | `MIRIAD atrophy challenge assessing atrophy measurement techniques same-day repeat scans` | 18 |
| 25 | 2026-11-23 | OpenAlex | `testing for nonlinearity in time series method of surrogate data` | 74834 |
| 26 | 2026-11-23 | OpenAlex | `surrogate time series Schreiber Schmitz` | 1809 |
| 27 | 2026-11-23 | OpenAlex | `interpreting observational studies why empirical calibration is needed negative controls` | 59413 |
| 28 | 2026-11-23 | OpenAlex | `negative controls a tool for detecting confounding and bias in observational studies` | 122462 |
| 29 | 2026-11-23 | OpenAlex | `evaluation of change point detection algorithms benchmark` | 405573 |
| 30 | 2026-11-23 | OpenAlex | `Landsat time series change detection algorithm accuracy stable no-change false positive commission error comparison` | 1275 |
| 31 | 2026-11-23 | OpenAlex | `BFAST breaks detection simulated time series false detection no change` | 87 |
| 32 | 2026-11-23 | OpenAlex | `reliable change index false positive rate stable patients test-retest methods comparison` | 6540 |
| 33 | 2026-11-23 | OpenAlex | `Jacobson Truax clinical significance statistical approach defining meaningful change psychotherapy research` | 4565 |
| 34 | 2026-11-23 | arXiv | `abs:"temporal order" AND abs:shuffled AND abs:"time series" AND abs:clinical` | 0 |
| 35 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"visual field" OR TITLE_ABS:perimetry) AND (TITLE_ABS:"12 times" OR TITLE_ABS:"twelve" OR TITLE_ABS:"weekly" OR TITLE_ABS:"10 weeks" OR TITLE_ABS:"within a short" OR TITLE_ABS:"short period") AND (TITLE_ABS:progression) AND TITLE_ABS:glaucoma` | 43 |
| 36 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"visual field" OR TITLE_ABS:perimetry) AND TITLE_ABS:glaucoma AND (TITLE_ABS:"test-retest") AND (TITLE_ABS:"machine learning" OR TITLE_ABS:"deep learning" OR TITLE_ABS:"artificial intelligence")` | 8 |
| 37 | 2026-11-23 | EuropePMC | `AUTH:"Shuldiner SR" AND TITLE:glaucoma` | 1 |
| 38 | 2026-11-23 | EuropePMC | `AUTH:"Yousefi S" AND TITLE:"visual field" AND (TITLE:progression OR TITLE:worsening OR TITLE:deep) AND FIRST_PDATE:[2022-01-01 TO 2026-12-31]` | 3 |
| 39 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"visual field") AND TITLE_ABS:glaucoma AND (TITLE_ABS:"reference standard" OR TITLE_ABS:"ground truth") AND (TITLE_ABS:progression) AND (TITLE_ABS:"specificity" OR TITLE_ABS:"false positive")` | 11 |
| 40 | 2026-11-23 | EuropePMC | `AUTH:"Gardiner SK" AND (TITLE_ABS:specificity OR TITLE_ABS:"false positive" OR TITLE_ABS:permutation OR TITLE_ABS:"test-retest") AND (TITLE_ABS:progression OR TITLE_ABS:deterioration OR TITLE_ABS:change)` | 13 |
| 41 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"visual field" OR TITLE_ABS:perimetry) AND TITLE_ABS:progression AND TITLE_ABS:"false-positive rate" AND (TITLE_ABS:"matched" OR TITLE_ABS:"equated" OR TITLE_ABS:"equalized" OR TITLE_ABS:"fixed specificity")` | 3 |
| 42 | 2026-11-23 | EuropePMC | `(TITLE_ABS:"visual field") AND TITLE_ABS:glaucoma AND TITLE_ABS:progression AND (TITLE_ABS:"short series" OR TITLE_ABS:"shorter series" OR TITLE_ABS:"first three" OR TITLE_ABS:"three visual fields" OR TITLE_ABS:"few visual fields" OR TITLE_ABS:"early in follow-up" OR TITLE_ABS:"limited number of")` | 18 |
| 43 | 2026-11-23 | OpenAlex | `benchmark visual field progression detection methods open dataset reproducible comparison` | 14175 |
| 44 | 2026-11-23 | EuropePMC | `(UWHVF OR "University of Washington Humphrey Visual Field" OR "UW Humphrey") AND (progression OR worsening)` | 11 |
| 45 | 2026-11-23 | EuropePMC | `(GRAPE) AND glaucoma AND ("visual field") AND (progression)` | 59 |
| 46 | 2026-11-23 | EuropePMC | `TITLE_ABS:glaucoma AND (TITLE_ABS:scrambled OR TITLE_ABS:shuffled OR TITLE_ABS:"randomly permuted" OR TITLE_ABS:"permuted series" OR TITLE_ABS:"permutated") AND (TITLE_ABS:progression OR TITLE_ABS:change)` | 4 |
| 47 | 2026-11-23 | EuropePMC | `TITLE_ABS:glaucoma AND (TITLE_ABS:"positive-unlabeled" OR TITLE_ABS:"self-supervised" OR TITLE_ABS:"weakly supervised") AND (TITLE_ABS:progression)` | 3 |
| 48 | 2026-11-23 | EuropePMC | `(AUTH:"Mandal S" OR AUTH:"Mariottoni EB") AND TITLE_ABS:glaucoma AND TITLE_ABS:progression` | 11 |
| 49 | 2026-11-23 | EuropePMC | `TITLE_ABS:glaucoma AND TITLE_ABS:"deep learning" AND TITLE_ABS:progression AND (TITLE_ABS:"specificity" ) AND (TITLE_ABS:"matched" OR TITLE_ABS:"equalized" OR TITLE_ABS:"95% specificity" OR TITLE_ABS:"fixed specificity")` | 3 |
| 50 | 2026-11-23 | OpenAlex | `surrogate data for hypothesis testing of physical systems` | 105773 |
| 51 | 2026-11-23 | OpenAlex | `review of solutions for diagnostic accuracy studies with an imperfect or missing reference standard` | 12734 |
| 52 | 2026-11-23 | OpenAlex | `eGFR slope estimation number of measurements variability false progression chronic kidney disease` | 887 |
| 53 | 2026-11-23 | OpenAlex | `scan-rescan reproducibility longitudinal brain atrophy SIENA false positive zero change` | 5 |
| 54 | 2026-11-23 | OpenAlex | `how similar are forest disturbance maps derived from different Landsat time series algorithms` | 10168 |
| 55 | 2026-11-23 | OpenAlex | `detecting significant change in neuropsychological test performance comparison of four models` | 66929 |
| 56 | 2026-11-23 | Crossref | `Jacobson Truax 1991 Clinical significance: a statistical approach to defining meaningful change in psychotherapy research` | 972087 |
| 57 | 2026-11-23 | Crossref | `Bates Candes Lei Romano Sesia Testing for outliers with conformal p-values` | 1261244 |
| 58 | 2026-11-23 | Crossref | `Altangerel knowledge of chronology of optic disc stereophotographs influences the determination of glaucomatous change` | 25994 |
| 59 | 2026-11-23 | arXiv | `ti:"Are Transformers Effective for Time Series Forecasting"` | 1 |
| 60 | 2026-11-23 | OpenAlex | `visual field progression glaucoma specificity false positive /from_publication_date:2025-11-01` | 968 |
| 61 | 2026-11-23 | OpenAlex | `glaucoma progression deep learning visual field detection /from_publication_date:2026-05-01` | 695 |
| 62 | 2026-11-23 | PubMed | `"visual field"[tiab] AND progression[tiab] AND (permutation[tiab] OR permuted[tiab] OR reordered[tiab] OR "re-ordered"[tiab] OR shuffled[tiab])` | 29 |
| 63 | 2026-11-23 | PubMed | `"visual field"[tiab] AND progression[tiab] AND ("machine learning"[tiab] OR "deep learning"[tiab]) AND ("false positive"[tiab] OR "false-positive"[tiab] OR specificity[tiab]) AND ("test-retest"[tiab] OR stable[tiab])` | 8 |
| 64 | 2026-11-23 | EuropePMC | `TITLE_ABS:RAPID AND TITLE_ABS:"visual field" AND TITLE_ABS:glaucoma AND (TITLE_ABS:"stable" OR TITLE_ABS:"specificity")` | 47 |

## Additional targeted verification lookups
Specific known candidates (Artes 2014, Rabiolo 2019, Saeedi 2019/2021, Wu & Medeiros 2018, Chauhan 2008, Nouri-Mahdavi 1997/2007/2011, Vesti 2003, Gardiner & Crabb 2002, Bryan 2013/2015, O'Leary 2012, Montesano 2021/2022/2023, Huang 2023 GRAPE, Yousefi 2016/2018, Wang M 2019, Dixit 2021, Shuldiner 2021, Mohammadzadeh 2024, Eslami-related preprints) were each found in at least one API record above; abstracts were read from Europe PMC/OpenAlex.
Note: Chauhan 2008 BJO abstract available only via OpenAlex inverted index.

## Known candidates: outcome
- Artes 2014 Ophthalmology: VERIFIED (10.1016/j.ophtha.2014.04.015). Also used 1000 permutations of the 12-test retest order.
- Rabiolo 2019 TVST: VERIFIED (10.1167/tvst.8.5.2). Abstract describes simulated series for pAUC; no permutation-based specificity stated in abstract (full text not read - UNVERIFIED whether permutations used).
- Saeedi 2019 Ophthalmology: VERIFIED (10.1016/j.ophtha.2019.01.029). Saeedi 2021 TVST ML: VERIFIED (10.1167/tvst.10.7.27).
- Wu & Medeiros 2018 TVST: VERIFIED (10.1167/tvst.7.4.20); specificity matched on SIMULATED stable eyes (not real test-retest series, per abstract).
- Chauhan 2008 BJO: VERIFIED (10.1136/bjo.2007.135012).
- Nouri-Mahdavi: 1997 Ophthalmology (10.1016/s0161-6420(97)30153-5), 2011 Arch Ophthalmol (10.1001/archophthalmol.2011.224), Brigatti/Nouri-Mahdavi 1997 NN (10.1001/archopht.1997.01100150727005) VERIFIED.
- Vesti 2003 IOVS: VERIFIED (10.1167/iovs.02-1171). Gardiner & Crabb 2002 BJO: VERIFIED (10.1136/bjo.86.5.560). Bryan 2013 IOVS: VERIFIED (10.1167/iovs.12-11185). O'Leary 2012: VERIFIED (10.1167/iovs.12-10049). Montesano 2022 UWHVF: VERIFIED (10.1167/tvst.11.1.1). Huang 2023 GRAPE: VERIFIED (10.1038/s41597-023-02424-4).
- 2025-2026 DL/VF progression preprints and papers: see map (arXiv:2609.29256, arXiv:2606.30417, arXiv:2411.12146, medRxiv 10.1101/2025.10.31.25339266, medRxiv 10.64898/2026.11.16.26368187, Research Square 10.21203/rs.3.rs-10009600/v1 [not put in map; prognosis only], PLoS One 10.1371/journal.pone.0357179, Ophthalmol Glaucoma 10.1016/j.ogla.2026.01.004). None found that tests ML VF detectors on true no-change retest data.
