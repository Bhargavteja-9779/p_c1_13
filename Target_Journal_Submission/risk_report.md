# Risk report and final decision (2026-11-23)

## Final decision
**NOT READY FOR SUBMISSION** — the scientific package is complete and internally audited, but submission is blocked by
items only the authors can supply (below).
**Novelty label: NOT REMARKABLE — honest strongest result** (see journal_selection/novelty_escalation_log.md: two
restarts and 6+ rounds produced no method that met the "remarkable" bar; the paper reports an evaluation finding).

## Blocking items (authors only)
1. Author names, degrees, affiliations, corresponding author, ORCID iDs (title page).
2. Funding statement, author contributions, conflict-of-interest statement for each author, prior presentation.
3. Public code/data repository URL (the GitHub repo used here is private; make it public or deposit on Zenodo).
4. Confirm APC (USD 8,050 / GBP 5,370; mandatory open access) is acceptable.
5. Verify JCR 2025 quartile of Ophthalmology and Therapy directly in JCR (secondary sources say Q1; UNVERIFIED).
6. Authors must read and approve the full text, check the AI-use disclosure, and take responsibility for it.

## Residual scientific risks (after revision 1)
| Risk | Likelihood | Mitigation in paper |
|---|---|---|
| Desk rejection for limited novelty / methods paper in a therapy journal | High | framed on treatment-escalation decisions; honest negative result; true no-change + repeated-looks + external clinic |
| Small reference set (26/26): only >= 34.6 pp gains detectable | Certain | stated in Abstract, Results, Limitations |
| Validity rule applied after results (deviation) and development knowledge of D6 failure | Certain (disclosed) | disclosed in Methods/Limitations; strict-rule sensitivity analysis; conclusions unchanged |
| Protocol only time-stamped in own repository | Certain | stated explicitly |
| True no-change arm small (30 pts), early glaucoma, short span | Certain | Limitation 4 |
| ML baselines modest (few labelled eyes, 12-config budget); no shuffle-calibrated ML variant | Medium | Limitation 8; reviewers may ask for more |
| GRAPE perimeter/dB scale confound; labels criterion-based; 100 eyes with only 3 visits | Certain | disclosed |
| No STARD flow diagram | Medium | counts in text; could add a figure |
| Main text ~5,100 words (guide ~4,000) | Low-medium | journal says guide, not limit; could move secondary reference / ML section to Supplement |
| Cites a medRxiv preprint (risk-weighted scheduling, Nov 2026) | Low | check journal preprint-citation policy |
| Fresh full re-run not repeated (bit-identity UNVERIFIED) | Low | statistics re-derived exactly from committed raw outputs |
| Acceptance-time margin: p75 70.25 d vs 72-d rule | Medium | timeline risk, not controllable |

## Rescored novelty scorecard (honest, after final results)
| Item | Score | Note |
|---|---|---|
| Distance from closest papers | 3 | true no-change benchmarking exists (Artes 2014 for GPA); new: 10 detectors, ML, shuffle-audit check, repeated looks, external clinic |
| Strength of problem | 4 | false escalation vs delayed detection |
| Depth of idea | 3 | evaluation protocol, not a new method |
| Strength of evidence | 3 | locked test set, 3 data sources, but n = 26/26 and post-hoc deviations disclosed |
| Generality | 3 | applies to any progression detector; arms small |
| Journal level match | 3 | above journal median evidence (3 datasets, 10 comparators, code), scope fit moderate |
| **Total** | **19/30** | below the 22 start gate and far below 26: consistent with NOT REMARKABLE |

## Audits completed
- Claim–evidence: 49 automated checks (manuscript/claim_checks.json); every number script-inserted.
- Citation: REVIEW/citation_audit.md (36 refs; all NOT SUPPORTED / PARTLY items fixed).
- Reproducibility: REVIEW/reproducibility_audit.md.
- Reviews: REVIEW/review_01..10.md, review_stakeholder.md; responses in REVIEW/response_to_reviews.md.
- Plagiarism: all text written for this project; no external text copied (no plagiarism-detection software available here: UNVERIFIED by tool).
