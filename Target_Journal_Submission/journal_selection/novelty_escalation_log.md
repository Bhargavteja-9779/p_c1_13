# Novelty escalation log (D6) — every idea tried, including failures

## Round 0 (2026-11-23) — topic: glaucoma visual-field (VF) progression DETECTION with fewer tests
Data: UWHVF (28,943 24-2 VFs, 7,428 eyes, 3,871 patients). Locked patient-level split by salted hash (60/20/20),
test split untouched. All pilot numbers below are on the VALIDATION split only.
Hypothesis H0a: a self-supervised "true order vs shuffled order" network used as a test statistic with within-eye
permutation calibration detects more eyes at alpha = 0.05 than PoPLR or MD-slope permutation tests.
Falsifier: positive rate on real series not higher than PoPLR at matched alpha.
Result (results/pilot_v0.json): k=4: MD 9.3%, PoPLR 11.2%, learned 10.5%; k=5: 18.4% all three; k=6: 22.1/23.1/23.1%;
k=8: 37.2/38.6/37.2%. -> H0a REJECTED (no gain). Self-supervised loss fell only from 3.466 (chance) to ~3.33.
Diagnosis: within-eye permutation p-values are coarse for short series (k=3: 6 orderings, min p = 0.167), and
all methods detect the same strongly progressing eyes.

## Round 1 — population-calibrated null (shuffled series of TRAIN eyes, stratified by k and mean sensitivity)
Hypothesis H1: calibrating against shuffled series of other eyes gives valid FPR and higher power at small k.
Result (results/pilot_v1.json): k=3 real-positive 8.1% (MD) vs within-eye 0% (impossible); null FPR 4.3-5.5%.
k=4: 12.9% vs 9.3%; k>=5: no gain (16.8% vs 18.4% at k=5). Learned statistic again no better.
Conclusion: detection power is information-limited; gains are incremental (fails "remarkable" step-change).
DECISION: change angle (stop rule: no real gain) -> reformulate as a DECISION problem with real-world units.

## Round 2 — reformulation: risk-controlled DEFERRAL of VF tests (N1 formulation + N3 guarantee + N6 external)
Real problem: glaucoma clinics are over capacity; delayed follow-up causes sight loss; VF tests are burdensome.
Most eyes are stable at any given visit -> the information value of many tests is low.
Idea: after each test, a calibrated risk model estimates the chance that progression would be detected at the next
scheduled test; defer that test when the risk is low; choose the deferral threshold with a distribution-free
risk-control procedure (Learn-then-Test / conformal risk control) so the share of progressing eyes whose detection is
delayed stays below a pre-set level with high probability. Outcome: % VF tests avoided at a guaranteed delay risk.
Status: pilot pending.
Pilot (results/pilot_deferral.json, experiments/pilot_deferral_curve.py, VALIDATION halves): rules that need >= 5
tests make almost every early deferral delay detection. Full-schedule event rate 20%. Severity rule MD > -10 dB:
18.7% tests saved, 55% of progressing eyes delayed; risk model (LightGBM, 15 history features) at lambda 0.04:
18.8% saved, 60% delayed -> no gain over a simple rule. Learn-then-Test could not certify any lambda at eps <= 0.2
(31 event eyes in calibration half). -> REJECTED (structural: fewer tests = slower count-based detection).

## Round 3 — detection with population-calibrated null vs FUTURE reference (results/pilot_v2.json)
Val eyes with >= 8 tests (n=145; reference progressors 31, reference stable 39 by full-series MD slope).
Sensitivity / specificity at alpha 0.05:
 k=3: MD pop-detrended 19.4% / 94.9%; within-eye 0% / 100% (no valid test possible).
 k=4: MD pop-detrended 22.6% / 87.2%; MD within-eye 12.9% / 97.4%.
 k=5: all MD variants 41.9% / 92.3%.
Gain only at 3-4 tests; small sample. Not a step change at >= 5 tests.

## Round 4 — alternative problem: nAMD anti-VEGF (Moorfields CC0 data via Zenodo mirrors; Dryad file downloads
blocked by Dryad's anti-bot check). Tested whether year-1 injection rhythm adds prognostic value for 3-year VA
(n=2,664 eyes; 80/20 patient split): baseline-only R2 0.272; + year-1 VA R2 0.531 (AUROC >=15-letter loss 0.762);
+ rhythm R2 0.529 (0.760). -> rhythm adds nothing. REJECTED as a finding.

## Status after restart 1 (glaucoma detection/deferral) and part of restart 2
No "remarkable" candidate yet. Best methodological candidate: population-calibrated (conformal) progression
testing that is valid from the 3rd field (gain limited to 3-4 tests).
