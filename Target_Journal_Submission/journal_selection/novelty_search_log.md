# Novelty search log (prior-art search)

Run date: 2026-11-23 (all queries run on this date, in one session).
Output: `novelty_map.csv` (55 rows, every id checked against Crossref `api.crossref.org/works/<doi>` or the arXiv API; the title, year and venue columns are copied from those records). Crossref "year" is the print/online date it reports (for example, the MICCAI 2025 paper shows as 2026).

## Scope
- The first brief covered G1-G4: a self-supervised temporal-order statistic for visual-field (VF) progression, with per-eye permutation calibration.
- A scope update in mid-session added **G5**, which now takes priority: risk-controlled deferral of VF tests, with the deferral threshold calibrated by conformal risk control or Learn-then-Test.
- The `closeness` column (1-5) scores closeness to the **new G5 idea**.
- An extra column, `closeness_original_idea`, keeps the score against the original temporal-order/permutation idea.

## Databases and endpoints
| Database | Endpoint | Search scope | Status |
|---|---|---|---|
| OpenAlex | api.openalex.org/works?search=...&filter=from_publication_date:2008-01-01 | title/abstract/full-text where indexed | worked |
| PubMed | eutils esearch/esummary/efetch | default PubMed fields | worked |
| Europe PMC | REST search | includes full text of OA/PMC articles | worked, with intermittent HTTP 503 and timeouts (retried) |
| Semantic Scholar | graph/v1/paper/search | - | mostly HTTP 429 (rate limited, no API key): 1 of 4 queries returned |
| Crossref | /works/<doi> for verification; /works?query.bibliographic= for 3 lookups | - | worked (one 429, retried) |
| arXiv | export.arxiv.org/api/query?id_list= for verification | - | worked |
| medRxiv | full-text HTML for one paper (GEAR) | - | worked |
| PMC | efetch db=pmc, author manuscript for Si et al. 2025 | - | worked |

Hit counts are the totals each engine reported. OpenAlex counts for natural-language queries are very large because matching is loose; I screened only the top 15 results by relevance for each query. PubMed and Europe PMC returned at most the top 25 or 15 records per query, and I screened those.

## Exact queries and hit counts
| DB | Query | Hits |
|---|---|---|
| OpenAlex | `visual field progression self-supervised` | 119382 |
| OpenAlex | `visual field contrastive learning glaucoma` | 14181 |
| OpenAlex | `visual field temporal order shuffle` | 31261 |
| OpenAlex | `visual field progression permutation machine learning` | 8387 |
| OpenAlex | `glaucoma visual field progression deep learning` | 7741 |
| OpenAlex | `UWHVF` | 31 |
| OpenAlex | `University of Washington Humphrey visual field dataset` | 1544 |
| OpenAlex | `self-supervised visual field glaucoma` | 8151 |
| OpenAlex | `visual field foundation model glaucoma` | 18200 |
| OpenAlex | `permutation of pointwise linear regression` | 6391 |
| OpenAlex | `PoPLR visual field` | 79 |
| OpenAlex | `transformer visual field progression glaucoma` | 1478 |
| OpenAlex | `arrow of time self-supervised medical longitudinal` | 20654 |
| OpenAlex | `temporal order prediction longitudinal medical images self-supervised` | 21612 |
| OpenAlex | `longitudinal self-supervised learning disease progression retina` | 2265 |
| OpenAlex | `temporally informed non-contrastive learning disease progression` | 61078 |
| OpenAlex | `sequence order verification self-supervised electronic health records` | 40697 |
| OpenAlex | `classification permutation test` | 233137 |
| OpenAlex | `classifier two-sample test` | 2032172 |
| OpenAlex | `learned test statistic permutation valid p-value` | 29628 |
| OpenAlex | `conformal change detection medical monitoring` | 90155 |
| OpenAlex | `DeepAtrophy temporal inference longitudinal MRI` | 14 |
| OpenAlex | `learning to compare longitudinal images` | 544800 |
| OpenAlex | `self-supervised scan temporal order progression atrophy` | 4175 |
| OpenAlex | `time-reversal self-supervised disease progression` | 18556 |
| OpenAlex | `within-subject permutation test trend detection longitudinal` | 15933 |
| OpenAlex | `self-supervised denoising visual field glaucoma progression` | 357 |
| OpenAlex | `conformal visual field glaucoma` | 3618 |
| OpenAlex | `number of visual field tests needed detect progression` | 200359 |
| OpenAlex | `recurrent neural network visual field prediction glaucoma Park` | 908 |
| OpenAlex | `convolutional long short-term memory visual field progression glaucoma` | 661 |
| OpenAlex | `Eslami visual field progression deep learning` | 1386 |
| OpenAlex | `Kalman filter personalized forecasting glaucoma visual field` | 58 |
| OpenAlex | `Rotterdam longitudinal glaucomatous visual field data` | 583 |
| OpenAlex | `learning and using the arrow of time` | 506791 |
| OpenAlex | `practical recommendations measuring rates of visual field change` | 325654 |
| OpenAlex | `false positive rate visual field progression stable glaucoma simulation` | 442 |
| OpenAlex | `visual field testing frequency glaucoma` | 25722 |
| OpenAlex | `personalized monitoring schedule glaucoma visual field` | 1140 |
| OpenAlex | `reduce visual field tests glaucoma OCT` | 19090 |
| OpenAlex | `glaucoma follow-up interval artificial intelligence` | 4192 |
| OpenAlex | `conformal risk control clinical` | 288883 |
| OpenAlex | `learn then test risk control` | 1643756 |
| OpenAlex | `conformal prediction follow-up interval surveillance` | 14138 |
| OpenAlex | `personalised screening interval diabetic retinopathy risk algorithm` | 484 |
| OpenAlex | `intervals between visual field tests wait-and-see glaucoma` | 1181 |
| OpenAlex | `surveillance of sight loss due to delay in ophthalmic treatment or review` | 1228 |
| OpenAlex | `conformal risk control triage deferral guarantee` | 752 |
| OpenAlex | `distribution-free guarantee skip test monitoring patients` | 9820 |
| OpenAlex | `risk-based follow-up interval machine learning surveillance guarantee` | 20527 |
| OpenAlex | `selective prediction deferral clinical monitoring false negative rate control` | 1780 |
| OpenAlex | `personalized prediction glaucoma progression target intraocular pressure Kazemian` | 49 |
| OpenAlex | `dynamic monitoring schedule chronic disease optimal testing glaucoma` | 1135 |
| OpenAlex | `conformal prediction screening interval personalized` | 5028 |
| OpenAlex | `risk-controlled screening schedule guarantee missed cancer` | 8654 |
| OpenAlex | `optimizing risk-based breast cancer screening policies reinforcement learning` | 3123 |
| OpenAlex | `conformal prediction time-to-event survival lower predictive bound` | 14592 |
| OpenAlex | `visual field OCT replace perimetry testing frequency reduce` | 599 |
| OpenAlex | `Erler longitudinal glaucomatous visual field Rotterdam dataset optimizing structure-function` | 12 |
| PubMed | `(visual field) AND (self-supervised OR contrastive OR "self supervised")` | 9940 |
| PubMed | `(visual field) AND (permutation) AND (progression)` | 39 |
| PubMed | `(visual field progression) AND (deep learning OR machine learning OR neural network)` | 490 |
| PubMed | `"UWHVF" OR ("University of Washington" AND "visual field" AND dataset)` | 8 |
| PubMed | `(temporal order OR shuffle OR "arrow of time") AND self-supervised AND (longitudinal) AND (disease OR medical)` | 4 |
| Europe PMC (full text) | `"PoPLR" AND ("deep learning" OR "neural network" OR "machine learning")` | 14 |
| Europe PMC (full text) | `"visual field" AND "permutation" AND ("deep learning" OR "neural network") AND glaucoma` | 71 |
| Europe PMC (full text) | `"visual field" AND ("self-supervised" OR "self supervised") AND (progression)` | 103 |
| Europe PMC (full text) | `("permutation" AND "exchangeab*") AND ("visual field")` | 0 |
| Europe PMC (full text) | `"visual field" AND ("temporal order" OR "chronological order" OR "shuffled order") AND ("deep learning" OR "neural network")` | 147 |
| Europe PMC (full text) | `"visual field" AND ("contrastive learning" OR "SimCLR" OR "masked autoencoder")` | 98 |
| Europe PMC (full text) | `("temporal order" OR "chronological order") AND ("self-supervised" OR "pretext task") AND (longitudinal) AND (MRI OR OCT OR fundus OR "medical")` | 64 |
| Europe PMC (full text) | `"classification permutation test"` | 10 |
| Europe PMC (full text) | `"permutation" AND "exchangeab*" AND "visual field"` | 0 |
| Europe PMC (full text) | `("visual field" OR perimetry) AND ("conformal" OR "learn then test" OR "learn-then-test") AND glaucoma` | 72 |
| Europe PMC (full text) | `("conformal risk control" OR "learn then test" OR "learn-then-test") AND (follow-up OR surveillance OR monitoring OR screening interval)` | 165 |
| Europe PMC (full text) | `glaucoma AND ("visual field") AND (defer* OR skip* OR omit*) AND (test* frequency OR "testing interval" OR "follow-up interval")` | 1741 |
| Europe PMC (full text) | `"diabetic retinopathy" AND ("conformal")` | 115 |
| Semantic Scholar | `self-supervised temporal order visual field glaucoma` | ERR HTTP Error 429:  |
| Semantic Scholar | `visual field test scheduling conformal risk control` | ERR HTTP Error 429:  |
| Semantic Scholar | `defer visual field test glaucoma risk` | 11357 |
| Semantic Scholar | `permutation test deep learning visual field progression` | ERR HTTP Error 429:  |

## Other lookups
- **Abstracts:** fetched from OpenAlex `abstract_inverted_index`, or from PubMed efetch when OpenAlex had none.
- **GEAR (medRxiv 10.64898/2026.11.16.26368187):** I read the full text and screened its reference list, which led to Jansonius 2007, Kazemian 2019, Phu 2026 and Yala 2022.
- **Si et al. 2025 (MICCAI, PMC13348073):** I read the abstract, introduction and datasets sections.

## Screening outcome for the key questions
**G5:** has anyone combined (i) per-visit deferral of VF or other monitoring tests with (ii) a distribution-free guarantee on delayed or missed progression?
- I found no paper that does both.
- The closest papers do one half each:
  - GEAR (2026, medRxiv) does risk-based deferral and rescheduling of VF/OCT, with UWHVF as external data, but gives no guarantee.
  - Si et al. 2025 uses conformal risk control on UWHVF, but for forecast intervals, not for deferral decisions.
  - RetinaGuard (2026) and Kwon & Kim (2026) use conformal/risk-controlled deferral, but for cross-sectional triage.
  - Sesia & Svetnik 2025 build conformal survival bands for low-risk screening, but not for repeat-test scheduling.
- Schell 2014 and Kazemian 2019 use model-based (Kalman/LQG) personalised schedules, with no distribution-free guarantee.

**Original idea:**
- (a) Self-supervised temporal-order learning on VFs: none found. VF self-supervision so far is masked-autoencoder or VAE reconstruction (Wu et al. 2024 arXiv; CHIASM 2026).
- (b) A learned statistic combined with within-eye permutation calibration for VF: none found.
- Temporal-order self-supervision does exist on longitudinal MRI and images: DeepAtrophy 2021, the NEJM AI 2025 glioma paper, LILAC/PaIRNet. None of these uses per-subject permutation p-values.

## Limitations
- Google Scholar, Web of Science, Scopus, IEEE Xplore, the ACM DL and Embase were not queried; no interface to them was available.
- Semantic Scholar was largely unavailable (rate limit). Conference-only ML work (NeurIPS/ICML/MICCAI workshops, ARVO abstracts) may be under-covered.
- ARVO meeting abstracts, which IOVS publishes as supplements, were not searched systematically.
- OpenAlex relevance ranking is loose; I screened only the top 15 per query.
- Europe PMC full-text queries were intermittently unavailable (503s, retried); one early run lost two queries, which were re-run successfully.
- For most papers only the abstract was read (`access` = "abstract only"). Full text was read only for GEAR and, partly, for Si et al. 2025.
- Preprints from 2026 (medRxiv/arXiv) are not peer-reviewed and may change.
- Records dated after the model's knowledge cutoff were checked only through Crossref/arXiv metadata and the abstracts.
