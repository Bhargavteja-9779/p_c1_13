# STAGE 2 — Problem story re-check

## 1. Is the problem real? (person, setting, cost) — with citation status
| Element | Statement | Evidence | Status |
|---|---|---|---|
| Person | Glaucoma specialist / optometrist deciding whether to escalate therapy | Weinreb 2014 JAMA (treatment = IOP lowering; monitoring by VF) [ref 2]; Heijl 2002 EMGT (IOP lowering slows progression) [ref 3] | DOIs verified (Crossref) run 1; content re-checked from abstracts in Stage 6 |
| Setting | Routine glaucoma follow-up with standard automated perimetry, ~1 test/yr | Chauhan 2008 BJO recommends 6 tests in 2 yrs [4]; 2026 Ophthalmol Glaucoma nationwide-insured study of time to identify progression at typical testing frequency [27] | verified DOIs; [27] abstract to re-read in Stage 6 |
| Harm of late detection | Delayed review/treatment causes avoidable sight loss | Foot & MacEwen 2017 Eye (BOSU surveillance) [5] | verified DOI |
| Harm of false alarms | Unneeded escalation (more drops, laser, surgery; side effects, cost) | NO verified citation in run 1 -> must add one (Stage 6) or soften to a plain logical statement without a cost number | UNVERIFIED -> fix |
| Size | ~76 M with glaucoma in 2020, ~112 M by 2040 | Tham 2014 [1] | verified |

## 2. Field changes since run 1 (to be completed by Stage 3 hostile search; preliminary)
- 2026 PLoS One "Labeling matters" (multicentre ML on VF progression; label definitions change model results) [22]:
  directly relevant to our reference-definition finding -> must be engaged in Introduction and Discussion.
- 2026 medRxiv GEAR (risk-weighted VF/OCT scheduling, uses UWHVF externally) [23].
- 2025 MICCAI conformal risk control for VF forecasting [24].

## 3. One-paragraph story (draft; final version after Stage 4 results, see stage2_story_final.md)
"Glaucoma clinicians must decide early whether a patient's visual field is getting worse, because waiting for five or six
tests delays treatment, while acting on a false alarm adds treatment that is not needed. New detection methods,
including machine-learning models, report earlier detection, but they are usually checked against eyes labelled
'stable' by the same kind of trend analysis rather than against eyes that truly did not change. We test ten detectors on
true no-change retest data, a future reference and an external clinic, and show [result of Stage 4/5]."
The cost/harm sentence for false alarms needs a verified source (Stage 6).

## 4. First-page check (run-1 draft intro): tells the escalation story in plain English (para 1-2), names the gap
(para 4). Weakness: the abstract/title did not exist yet; the gap statement "only a few studies have measured false alarms
on true no-change data [7]" must be checked against Stage-3 close calls (Wu & Medeiros 2018 and others also used
test-retest data).
