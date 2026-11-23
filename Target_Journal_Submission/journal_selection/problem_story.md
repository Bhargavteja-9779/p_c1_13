# STEP 2 — Problem story and Real-Problem Test (selected topic)

## One-sentence story
Glaucoma clinicians must decide whether to escalate treatment, but standard trend tests cannot give a valid
progression verdict until an eye has about five visual-field tests (often four to five years in routine care), because
with few tests an eye's own data cannot separate true loss from test noise; we calibrate each eye's test against
shuffled test series from the clinic's other patients, which gives a valid false-alarm rate from the third test, and we
measure how many progressing eyes are then flagged earlier, how often stable eyes are falsely flagged (including on true
no-change data), and whether this holds in an independent clinic.

## Real-Problem Test
1. Stakeholder: glaucoma specialists and optometrists who decide treatment escalation; patients with glaucoma.
2. Cost (to cite, DOIs verified in citation audit): glaucoma is a leading cause of irreversible blindness (Tham et al.
   2014 Ophthalmology; GRAPE abstract); progression detection needs many tests (Chauhan et al. 2008 BJO recommend 6 tests
   in the first 2 years, rarely achieved in practice); delayed follow-up causes sight loss (Foot & MacEwen 2017 Eye).
3. Documented failure: within-eye permutation (PoPLR, O'Leary et al. 2012) cannot reach p < 0.05 with 3 tests (only 6
   orderings, minimum p = 1/6) and is coarse with 4 (24 orderings); OLS trend p-values assume Gaussian, homoscedastic
   noise that perimetry violates (variability rises as sensitivity falls; Artes et al. 2002; Gardiner et al.);
   event analysis (GPA) needs a dedicated test-retest cohort and >= 4 tests, and its real specificity is lower than
   nominal (Artes et al. 2014 Ophthalmology).
   Our pilot (validation split): within-eye tests flag 0% of eyes at 3 tests by construction.
4. Data: UWHVF (BSD-3, 28,943 fields); GRAPE (CC0, 263 eyes, clinical progression labels); Artes 2014 12-week retest
   data (30 glaucoma patients x 12 fields; distributed with the visualFields R package, GPL-3) = true no-change data.
5. Real-world measure: proportion of progressing eyes flagged at test 3/4 (one or two tests earlier = about 1-2 years
   earlier at UW testing intervals), false-alarm rate on true no-change series, number of tests to first detection.
6. Journal fit: monitoring of glaucoma therapy (escalation decisions) with a device (perimetry); journal publishes
   glaucoma management and AI papers.

## Desk-rejection stress test (editor's view)
- Incremental? The core is a new inference principle for this field (clinic-calibrated conformal null from shuffled
  routine data), with a validity argument; not a new network on a known dataset.
- Simpler method does the same? Compared directly with OLS p, within-eye permutation, GPA-like event analysis.
- Gain vanishes under statistics? Pilot gain is concentrated at 3-4 tests; CIs from patient bootstrap will show it.
  RISK: gains are moderate; we will not oversell.
- Dataset too easy / leakage? Patient-level splits; calibration pool disjoint from evaluation patients; external clinic
  calibrated on its own data with leave-one-patient-out.
- Depth: theory (exchangeability), method variants (detrended residual shuffles, Mondrian strata), 3 datasets.
