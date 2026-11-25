# Review 09 — Research-integrity reviewer

## Summary
I checked pre-registration timing (git history), deviations from protocol, the development use of the Artes data, selective reporting and number provenance. Number provenance is good: every number I checked matches the JSON. The summary statistics also reproduce exactly from `raw_results.csv.gz` (I re-ran `src.statistics.summarise` in a scratch copy). However:

- the key validity rule is an unreported deviation;
- the "pre-registered" claim is overstated;
- the development use of Artes is more consequential than disclosed;
- the quick run processed GRAPE and Artes before the amendments;
- several pre-registered outcomes are missing.

**Recommendation: Major revision (integrity clarifications are a condition for further review).**

## Number provenance spot-check (manuscript vs JSON)

| # | Manuscript location | Manuscript value | JSON source | JSON value | Match |
|---|---|---|---|---|---|
| 1 | Abstract/Results RQ2 | D1 k=3 sensitivity 19.2% (7.4–33.3) | metrics.json D1 k3 sens | 0.1923 (0.0740–0.3333) | Yes |
| 2 | Abstract/RQ1 | D1 k=3 true-null 4.4% (2.8–6.3) | fpr_true_null | 0.04433 (0.02833–0.06267) | Yes |
| 3 | Abstract | D6 k=3 56.9%; +38.5 pp (19.2 to 57.7); Holm p = 0.018 | metrics D6 sens; statistics paired D6 k3 | 0.5692; diff 0.3846 (0.1923–0.5769); p_holm 0.01758 | Yes, but **internally inconsistent**: 56.9 − 19.2 = 37.7 (majority-vote vs seed-mean; see issue 3) |
| 4 | Abstract/RQ1 | D6 22.4% (19.3–25.7); D8 27.7% (22.7–32.9) | fpr_true_null | 0.2235 (0.1933–0.2573); 0.2773 (0.2273–0.3293) | Yes |
| 5 | Abstract | Specificity 96.2% and 94.6% vs 96.2% | spec D6/D8/D1 k3 | 0.9615/0.9462/0.9615 | Yes (but the McNemar table shows 0/0 discordant pairs for D8, issue 3) |
| 6 | Abstract/RQ3 | Spearman ρ 0.65; 80% within 3 pp; max 10.4; median 1.0 | rq3_audit_concordance | 0.6483; 0.80; 0.1039; 0.00956 | Yes |
| 7 | Abstract/RQ5 | GRAPE +16.5 and +33.5 pp false positives, p < 0.001 | paired GRAPE FP k3 D2/D8 | 0.1653/0.3347; p_holm ≈ 0 | Yes |
| 8 | Results Study Data | 132 / 26 / 26 / 80 / 41 patients | dataset_counts | 132/26/26/80/41 | Yes |
| 9 | Results Study Data | Age 58.8 (50.3–64.4); MD −4.4 (−6.0 to −3.2); FU 12.9 y; 11 tests; interval 1.0 y | dataset_counts | 58.81 (50.34–64.38); −4.358 (−6.036 to −3.160); 12.94; 11; 1.016 | Yes |
| 10 | Results Study Data | 3,000 windows; 263 / 163 GRAPE eyes; 1,458 s | metrics fpr_true_null_n; counts; run_meta_full | 3000; 263/163; 1458.28 | Yes ("four-core CPU" is not recorded in any JSON) |
| 11 | RQ1 | D9 k=6 5.9% (2.3–10.0), "failed narrowly" | fpr_true_null_hi | 0.100002 | Yes, but the classification depends on the 6th decimal place |
| 12 | RQ2 | D8 k=6 70.8%, +11.5 (−7.7 to 30.8), p = 1.00 | metrics / paired | 0.7077; diff 0.1154 | Yes, but 70.8 − 57.7 = 13.1 (issue 3) |
| 13 | RQ5 | GRAPE D8 65.9%, +25.9 (0.0 to 48.1), p = 0.28 | grape_sens / paired | 0.6593; 0.2593; p_holm 0.2769 | Yes, but 65.9 − 44.4 = 21.5 (issue 3) |
| 14 | Real-world | 38/54/69%; median 5; 224 and 277 per 1,000 | realworld.json | 0.385/0.538/0.692; 5.0; 223.5; 277.3 | Yes |
| 15 | Table S2 | D1 27.6%, D7 31.0% of 58 at k=5 | sens_ref2 | 0.2759; 0.3103; n 58 | Yes |
| 16 | Discussion | "raised sensitivity 3.0-fold"; "5.0 and 6.3 times" | derived | 56.9/19.2 = 2.96; 22.4/4.4 = 5.04; 27.7/4.4 = 6.26 | Yes |

No number was found that departs from the JSON. The problems are internal inconsistencies (items 3, 5, 12, 13) and the validity classification (item 11).

## Issues

1. **FATAL — The validity rule is an undeclared protocol deviation that decides the primary results (Methods "Statistical Analysis": "Before the results were seen, we made this rule operational...").**
   - The time-stamped protocol (commit c0dedb5, 09:05:51) says "Validity: FPR CI upper bound vs 5%". Amendments A1 and A2 (commit 60ba7b2, 09:08:27) do not change this.
   - The "upper ≤ 10% and lower ≤ 5%" rule appears first in a Methods draft (commit bd2c2e2, 09:14:18), worded differently, and in final form only in `manuscript/fill_values.py` (commit 53896c1, 19:32).
   - The full run lasted 1,458 s and was committed at 09:33:48, so it most likely began around 09:09. The rule was therefore written *during* the final run. This cannot be shown to be "before the results were seen".
   - Under the protocol's literal rule, D1 is invalid at every k (upper limits 6.3–8.1%).
   - The manuscript says "Two amendments were made"; in fact there were three changes.

   *Fix:* declare it as amendment A3 with its real timestamp. Present the results under both rules. Remove the "before results were seen" claim unless it can be evidenced, for example with run logs showing no output was viewed.

2. **MAJOR — "Pre-registered" overstates what was done (Abstract Methods; Methods "Study Design").**
   - The protocol is a file in the authors' private repository, committed by the same AI session 3 minutes before the 218-line detector implementation. The implementation was very probably written before or alongside the protocol.
   - There is no public registry entry and no third-party timestamp.

   *Fix:* use "analysis plan committed to version control before the final run (commit c0dedb5)". Make the repository public with its full history. Do not use "pre-registered" without a registry.

3. **MAJOR — The test procedure is not disclosed in Methods, and its estimand differs from the reported proportions (Methods "Statistical Analysis"; Abstract).** The McNemar tests and paired differences use a majority vote over seeds; the proportions use seed means. Only the Table S3 footnote says so. This produces the inconsistencies in items 3, 5, 12 and 13. *Fix:* disclose the procedure in Methods and harmonise the estimands (see review 04 #2).

4. **MAJOR — Development use of the Artes data is under-disclosed (Methods "Disclosure of Development Use of Data"; Supplement S1 Round 5).**
   - The development log (`novelty_escalation_log.md`, Round 5) shows that the Artes data were used to find that the region-max detrended pooled null gives "FPR 20–22%" at k = 3. That is essentially the headline result for D6 (22.4%).
   - The same round gave the OLS-MD Artes false-alarm rate (4.0%).
   - The paper's framing, the inclusion of D6, and hypotheses H2/RQ4 were chosen *after* this observation. The log says so: "New topic framing ... apparent early-detection gains ... are explained by inflated false alarms that only a true-no-change check reveals."
   - The manuscript says the check "did not change any detector, threshold or reference". It did determine the research question and which detector became the cautionary example. The D6 result on Artes is therefore a replication on the *same data*, not a confirmatory test.

   *Fix:* state explicitly that the D6 true-null finding was known from development on the same Artes data and is not confirmatory. Report the D6 development result alongside the final one. Restrict confirmatory language to outcomes not seen in development (e.g., D8, D9, GRAPE).

5. **MAJOR — The quick run processed GRAPE and Artes before A1 and A2 were written (`run_all.py` quick branch; commit 60ba7b2; Methods "The UWHVF test set and GRAPE were not used before the final run").** The quick mode computes E2 and E4 flags with GRAPE labels. `run_meta_quick.json` (n_grape = 263) was committed in the same commit as A1 and A2. The leakage audit says quick mode "never touches the test split", which is true for UWHVF only. The quick raw output is not in the repository. *Fix:* correct the statement. Disclose the quick run. Provide its output or a statement of what was seen.

6. **MAJOR — Selective reporting of pre-registered outcomes.** Not reported:
   - GRAPE secondary labels PLR2, PLR3 and "any" (protocol "Data"), which the raw file contains and which are less favourable to D1 (review 07 #5);
   - secondary-reference specificity;
   - the bootstrap CI for Spearman ρ;
   - per-seed SD ("All seeds reported (mean ± SD)").

   *Fix:* report all of them, or explain each omission in a "Deviations from protocol" table.

7. **MAJOR — A limitation is claimed as disclosed but is not.** `experiments/leakage_audit.md` says the overlap between the reference and the first k tests is "stated as a limitation". The manuscript's Limitations do not mention it. *Fix:* add it.

8. **MODERATE — The development history (Supplement S1) is incomplete as a multiplicity record.** It omits Round 3's result details (sensitivity 19.4% vs 0% at k = 3), the Round 5 weighted-MD bug ("results void"), and the fact that the protocol was written after six failed rounds aimed at a "remarkable" result. S1 also says "All development used the UWHVF training and validation sets only", which is contradicted by Round 4 (Moorfields) and Round 5 (Artes). *Fix:* correct that sentence. Link the full log in the Supplement.

9. **MODERATE — The pipeline claim "One command (`run_all.py --mode full`) reproduces every number, table and figure" (Methods, last sentence of "Statistical Analysis") is inaccurate.** `run_all.py` only writes raw results; `summarise.py`, `describe.py`, `figures.py` and `fill_values.py` must be run separately, and the validity rule lives in `fill_values.py`. *Fix:* provide a single driver script, or correct the sentence.

10. **MODERATE — AI authorship and accountability.** The git history shows every commit authored by "Claude", including protocol, code, results and manuscript, with no human commits. The Declarations say the authors "checked all content". *Fix:* the authors should document what human verification was done (e.g., independent re-run, code review), in line with ICMJE and Springer Nature AI policy.

11. **MINOR — Reference verification.** Refs 6, 23 and 26 are 2026 publications that I could not verify. The ref. 23 DOI prefix (10.64898) is atypical. Ref. 28 has an article-number/DOI mismatch (":2" vs ".1.1"). *Fix:* re-verify. Note that the repository contains a PubMed/Crossref check file (`manuscript/pubmed_check.json`); please include its outcome.
