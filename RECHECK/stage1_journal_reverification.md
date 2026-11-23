# STAGE 1 — Journal re-verification (2026-11-23, second run; nothing from run 1 trusted)

## 1. Ophthalmology and Therapy (ISSN 2193-8245 / 2193-6528), Springer Nature (Adis)
| Item | Re-check result | Status |
|---|---|---|
| Publisher / legitimacy | Springer Nature (Adis); DOIs 10.1007/s40123-*; not MDPI | VERIFIED (Crossref) |
| JCR IF | Run 1 read "4.2 (2025)" from the Springer page. In run 2 the Springer page is behind a JavaScript bot challenge (curl gets "Client Challenge"; WebFetch is redirected to idp.springer.com). A headless-browser fetch was blocked by this session's permission policy. Aggregator (scijournal.org) lists 4.22 (2025) — not an official source. | **UNVERIFIED in run 2** (consistent secondary evidence only) |
| JCR quartile / category | Ophthalmology, Q1 per aggregators (Resurchify = Scopus-based; journalmetrics = OpenAlex-based). No JCR access. | **UNVERIFIED** |
| Scope | Run-1 copy of aims & scope (author_guidelines/) says clinical, observational, real-world and health-outcomes research on ophthalmological therapies, devices and surgical techniques. Not re-fetched (bot challenge). | Run-1 copy; UNVERIFIED live |
| APC | Run-1 value USD 8,050 / GBP 5,370 / EUR 6,250 | UNVERIFIED live in run 2 |
| Author guidelines | Run-1 PDF author_guidelines/adis_rapid_I4A.pdf (V15.1) still in repo; used for formatting. | Local copy (date of fetch: 2026-11-23, run 1) |
| Integrity | Crossref: 1 retraction notice in the journal ever (10.1007/s40123-024-00911-4, a case report). Web search: no delisting, no expression-of-concern cluster, no publisher warning found. Clarivate MJL needs JavaScript -> not checked. | "No concern found" (not proof) |

## 2. Received -> accepted re-computation (Crossref assertions, script code/scripts/full_journal_dates.py)
File: RECHECK/journal/ophthalmol_ther_last12m.csv (257 records, published 2025-11-23..2026-11-23; research articles = OpenAlex type
"article" with letters/reviews/editorials removed by title regex).

| Window | n research articles | median (d) | p75 (d) | share <= 72 d |
|---|---|---|---|---|
| Last 12 months | 180 | 54.5 | **74.0** | 0.74 |
| Last 6 months (published >= 2026-05-23) | 105 | 56.0 | **78.0** | 0.70 |
| Last 3 months | 45 | 56.0 | **74.0** | 0.73 |
| Run 1 (2025-06-01..2026-11-23) | 266 | 52.5 | 70.25 | 0.77 |

**Finding: run 1's "p75 <= 72" passed only because its window started in June 2025. On the most recent 12 months the
75th percentile is 74 d (6 months: 78 d). The 72-day rule (median well under 72 AND p75 <= 72) is NOT MET; it fails by 2-6 days.**
The median (54-56 d) is well under 72. Survivorship limitation: only accepted papers are visible.

## 3. Search for a better journal (same 12-month window, same script) — RECHECK/journal/alt/*.log
| Journal | Publisher | median / p75 (d) | Verdict |
|---|---|---|---|
| Eye | Springer Nature | 64 / 188 (n=718) | fails p75 |
| Eye and Vision | Springer (BMC) | 157 / 186.5 | fails |
| Graefe's Arch Clin Exp Ophthalmol | Springer | 141 / 187.5 | fails |
| Seminars in Ophthalmology | T&F | 71.5 / 112.8 | fails |
| Expert Review of Ophthalmology | T&F | 152 / 218.5 | fails |
| Advances in Therapy (Adis) | Springer | 78.5 / 104 | fails, scope |
| Journal of Medical Systems | Springer | 125 / 199 | fails |
| BMC Med Res Methodology | Springer (BMC) | 159 / 271 | fails |
| Diagnostic and Prognostic Research | Springer (BMC) | 200.5 / 277 | fails |
| BMC Med Inform Decis Mak | Springer (BMC) | 167.5 / 309 | fails |
| Health Inf Sci Syst | Springer | 192.5 / 346 | fails |
| Current Eye Research | T&F | 174 / 260.5 | fails |
| Clinical Ophthalmology (Dove/T&F) | T&F | no dates deposited in Crossref | UNVERIFIABLE (and Q2/Q3 by aggregators) |
| npj Digital Medicine | Springer Nature | run 1: median >= 134 | fails |
Journals of Elsevier, Wiley, OUP, SAGE, IEEE, Wolters Kluwer (e.g., Ophthalmology Science, AJO, Acta Ophthalmol, Clin Exp
Ophthalmol, TVST, J Glaucoma) do not deposit received/accepted dates in Crossref and their pages are blocked here (run 1) ->
their acceptance times are UNVERIFIABLE, so they cannot pass the evidence rule. Run 1 also screened 740 Springer/T&F journals;
the only ones passing p75 <= 72 had no scope fit.

## Decision
**Keep Ophthalmology and Therapy**: it remains the only verifiable Q1-candidate ophthalmology journal with a median well under
72 d, and no journal with equal or better IF and scope passes the 72-day test. **Unmet rule, stated openly: the recent p75 is
74 d (12 m) / 78 d (6 m), i.e. about 1 in 4 accepted papers took longer than 72 days.** Expected time to acceptance for a
typical paper: ~55 d; a 72-day acceptance is likely (~70-74%) but not assured. JCR IF/quartile remain UNVERIFIED in this run.

## 5. Ten newest research papers (Oct-Nov 2026; list from Crossref, titles only — full texts not re-read: Springer pages blocked)
Newest 25 printed in stage log; 10 newest: aflibercept biosimilar real-world outcomes; bio-interventional cyclodialysis
real-world; cyclosporine after vitrectomy RCT; retinoblastoma chemotherapy comparison; cyclosporine dry eye RCT; IOL constant
optimization; supplemental IOL outcomes; aflibercept 8 mg real-world; polihexanide Acanthamoeba keratitis; avacincaptad pegol
IRIS Registry. Other recent: "An Agentic AI Workflow for Automated Macular Hole Diagnosis" (AI), "Characterizing the Modern
Interventional Glaucoma Treatment Paradigm: The Newton Registry" (glaucoma).
**Updated Journal Level Profile:** the journal's centre of gravity is even more clearly *therapy outcomes / real-world
evidence / registries*; methods papers are rare (about 1 AI paper per month). Evidence level per paper has not visibly moved
up (multicentre real-world cohorts, RCTs). Implication: our paper must be framed as evidence about *monitoring glaucoma
therapy* (when to escalate) with clinical units, not as a statistics-methods paper. Scope remains the top desk-reject risk.
