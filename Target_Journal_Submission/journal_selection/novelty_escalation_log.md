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
