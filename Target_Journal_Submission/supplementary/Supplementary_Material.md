# Supplementary Material

How Early Can Glaucomatous Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm

## S1. Development history, including abandoned ideas

This section reproduces the development log kept during the study. All pilot numbers were computed on the training and validation splits of UWHVF (and, in round 5, on the Artes retest data), never on the locked test split. The benchmark reported in the main text was specified after round 5. Round 4 explored a different clinical problem (neovascular age-related macular degeneration) and was abandoned.

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

### Round 1 — population-calibrated null (shuffled series of TRAIN eyes, stratified by k and mean sensitivity)
Hypothesis H1: calibrating against shuffled series of other eyes gives valid FPR and higher power at small k.
Result (results/pilot_v1.json): k=3 real-positive 8.1% (MD) vs within-eye 0% (impossible); null FPR 4.3-5.5%.
k=4: 12.9% vs 9.3%; k>=5: no gain (16.8% vs 18.4% at k=5). Learned statistic again no better.
Conclusion: detection power is information-limited; gains are incremental (fails "remarkable" step-change).
DECISION: change angle (stop rule: no real gain) -> reformulate as a DECISION problem with real-world units.

### Round 2 — reformulation: risk-controlled DEFERRAL of VF tests (N1 formulation + N3 guarantee + N6 external)
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

### Round 3 — detection with population-calibrated null vs FUTURE reference (results/pilot_v2.json)
Val eyes with >= 8 tests (n=145; reference progressors 31, reference stable 39 by full-series MD slope).
Sensitivity / specificity at alpha 0.05:
 k=3: MD pop-detrended 19.4% / 94.9%; within-eye 0% / 100% (no valid test possible).
 k=4: MD pop-detrended 22.6% / 87.2%; MD within-eye 12.9% / 97.4%.
 k=5: all MD variants 41.9% / 92.3%.
Gain only at 3-4 tests; small sample. Not a step change at >= 5 tests.

### Round 4 — alternative problem: nAMD anti-VEGF (Moorfields CC0 data via Zenodo mirrors; Dryad file downloads
blocked by Dryad's anti-bot check). Tested whether year-1 injection rhythm adds prognostic value for 3-year VA
(n=2,664 eyes; 80/20 patient split): baseline-only R2 0.272; + year-1 VA R2 0.531 (AUROC >=15-letter loss 0.762);
+ rhythm R2 0.529 (0.760). -> rhythm adds nothing. REJECTED as a finding.

### Status after restart 1 (glaucoma detection/deferral) and part of restart 2
No "remarkable" candidate yet. Best methodological candidate: population-calibrated (conformal) progression
testing that is valid from the 3rd field (gain limited to 3-4 tests).

### Round 5 (validation + Artes true-null; results/d6_round5.json) — pre-stated hypotheses H5a (noise strata add
power) and H5b (weighted / regional statistics add power); falsifier: no sensitivity gain at matched specificity.
Key result (alpha 0.05):
 k=3: MD detrended-pooled sens 19.4% BUT false-alarm rate 13.2% on shuffled and 12.7% on TRUE no-change (Artes) data;
      region-max detrended: sens 35.5%, FPR 20-22% -> INVALID (anti-conservative). Valid pooled shuffle null: sens 3-6%.
      OLS MD parametric: sens 3.2%, Artes FPR 4.0%.
 k=4: OLS MD sens 22.6% / spec 87.2% / Artes FPR 2.6% == best valid conformal variants (19-26%).
 k=5: all valid methods ~41.9%.
 Weighted MD had a division-by-zero bug (zero variance at floor) -> results void; to fix in final code.
=> The earlier "valid from the 3rd test" gain was a false-alarm artefact of detrending with 1 residual df.
   H5a, H5b REJECTED. Population-calibrated testing gives NO gain over plain OLS-MD p-values.
Note: Artes data were used here during development (only to check FPR); disclosed in the paper.

### Decision after restart 1 exhausted (6 rounds, glaucoma) + restart 2 pilot (nAMD) failed
No method idea reached the "remarkable" bar. The robust, generalisable finding is an EVALUATION finding:
apparent early-detection gains of more complex methods are explained by inflated false alarms that only a
true-no-change check reveals. New topic framing (N4 benchmark + N5 protocol + N7 finding + N6 two clinics):
an open benchmark for glaucoma VF progression detection with a TRUE NO-CHANGE arm, testing classical, permutation,
pooled-null and machine-learning detectors at 3-6 tests. Honest label expected: NOT REMARKABLE (strongest honest result).

## S2. Protocol amendments (made before any final result)

### Amendment A1 (2026-11-23, before any final result)
Artes tests are one week apart. Rate-based rules (D2, D3, D7, D8, D9) are not invariant to the time scale, so each
Artes window of k tests is assigned the test times of a randomly drawn UW-test eye with >= k tests (10 draws per
window). Under true no change the time labels carry no signal, so this keeps the arm a valid null at clinical spacing.

### Amendment A2 (2026-11-23, before any final result)
GRAPE was measured with a different perimeter (59 analysable points after removing points coded -1; dB scale differs
from Humphrey). Therefore on GRAPE: D5 calibration pool and D7 change limits come from GRAPE itself by 5-fold
patient-level cross-fitting ("own-clinic calibration"); D8 is the UWHVF-trained model applied unchanged (transfer
test, grid-agnostic features); D6, D9, D10 (24-2 specific) are not evaluated on GRAPE.


## S3. Full results

Table S1. All metrics by detector and number of tests (k). Seed SD: standard deviation across five seeds (stochastic detectors only). FA, false-alarm rate; PoPLR ref, secondary reference standard; pp, percentage points.

| Detector | k | Sens % | Seed SD | Spec % | FA true null % | Seed SD | FA shuffle % | Sens, PoPLR ref % | GRAPE sens % | GRAPE spec % |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 OLS-MD | 3 | 19.2 | 0.0 | 96.2 | 4.4 | 0.0 | 4.8 | 10.3 | 44.4 | 95.3 |
| D2 MD-rate <= -1 dB/yr | 3 | 38.5 | 0.0 | 92.3 | 2.6 | 0.0 | 11.7 | 24.1 | 59.3 | 78.8 |
| D3 PLR >=3 points | 3 | 3.8 | 0.0 | 96.2 | 1.4 | 0.0 | 1.8 | 1.7 | 3.7 | 95.8 |
| D4 PoPLR (within-eye permutation) | 3 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
| D5 Pooled-shuffle conformal MD | 3 | 19.2 | 0.0 | 96.2 | 4.0 | 0.4 | 4.6 | 10.0 | 41.5 | 95.4 |
| D6 Pooled-detrended conformal region-max | 3 | 56.9 | 1.7 | 96.2 | 22.4 | 0.7 | 22.5 | 46.2 |  |  |
| D7 Event analysis (GPA-like) | 3 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 100.0 |
| D8 ML-tabular (LightGBM) | 3 | 26.2 | 5.0 | 94.6 | 27.7 | 5.1 | 17.3 | 24.1 | 65.9 | 61.2 |
| D9 ML-sequence (GRU) | 3 | 12.3 | 5.0 | 95.4 | 12.7 | 3.8 | 8.5 | 9.7 |  |  |
| D10 Self-supervised order net + permutation | 3 | 0.0 | 0.0 | 100.0 | 0.0 | 0.0 | 0.0 | 0.0 |  |  |
| D1 OLS-MD | 4 | 30.8 | 0.0 | 100.0 | 3.8 | 0.0 | 4.7 | 20.7 | 33.3 | 95.9 |
| D2 MD-rate <= -1 dB/yr | 4 | 23.1 | 0.0 | 96.2 | 0.6 | 0.0 | 6.4 | 12.1 | 55.6 | 86.2 |
| D3 PLR >=3 points | 4 | 15.4 | 0.0 | 100.0 | 0.2 | 0.0 | 1.5 | 10.3 | 11.1 | 97.9 |
| D4 PoPLR (within-eye permutation) | 4 | 3.8 | 0.0 | 100.0 | 3.3 | 0.2 | 4.1 | 8.6 | 22.2 | 95.2 |
| D5 Pooled-shuffle conformal MD | 4 | 30.8 | 0.0 | 100.0 | 3.6 | 0.3 | 4.9 | 20.7 | 33.3 | 94.5 |
| D6 Pooled-detrended conformal region-max | 4 | 25.4 | 2.1 | 100.0 | 5.1 | 0.4 | 5.5 | 16.6 |  |  |
| D7 Event analysis (GPA-like) | 4 | 23.1 | 0.0 | 100.0 | 1.1 | 0.0 | 5.2 | 13.8 | 16.7 | 95.9 |
| D8 ML-tabular (LightGBM) | 4 | 41.5 | 5.0 | 99.2 | 9.4 | 2.3 | 7.7 | 24.8 | 48.9 | 81.5 |
| D9 ML-sequence (GRU) | 4 | 11.5 | 3.8 | 99.2 | 2.0 | 1.5 | 4.7 | 7.2 |  |  |
| D10 Self-supervised order net + permutation | 4 | 20.0 | 4.2 | 100.0 | 3.8 | 0.6 | 4.1 | 12.1 |  |  |
| D1 OLS-MD | 5 | 42.3 | 0.0 | 100.0 | 4.7 | 0.0 | 5.1 | 27.6 |  |  |
| D2 MD-rate <= -1 dB/yr | 5 | 23.1 | 0.0 | 100.0 | 0.8 | 0.0 | 3.6 | 13.8 |  |  |
| D3 PLR >=3 points | 5 | 23.1 | 0.0 | 100.0 | 0.5 | 0.0 | 1.4 | 15.5 |  |  |
| D4 PoPLR (within-eye permutation) | 5 | 38.5 | 0.0 | 100.0 | 3.9 | 0.2 | 4.3 | 24.1 |  |  |
| D5 Pooled-shuffle conformal MD | 5 | 42.3 | 0.0 | 100.0 | 4.3 | 0.2 | 4.9 | 27.6 |  |  |
| D6 Pooled-detrended conformal region-max | 5 | 31.5 | 1.7 | 100.0 | 6.2 | 0.2 | 5.0 | 21.0 |  |  |
| D7 Event analysis (GPA-like) | 5 | 50.0 | 0.0 | 100.0 | 1.2 | 0.0 | 7.9 | 31.0 |  |  |
| D8 ML-tabular (LightGBM) | 5 | 56.2 | 2.1 | 99.2 | 18.8 | 2.2 | 16.1 | 38.3 |  |  |
| D9 ML-sequence (GRU) | 5 | 40.8 | 8.9 | 93.8 | 7.5 | 4.1 | 8.1 | 25.9 |  |  |
| D10 Self-supervised order net + permutation | 5 | 43.8 | 3.4 | 100.0 | 5.1 | 0.3 | 4.2 | 27.9 |  |  |
| D1 OLS-MD | 6 | 57.7 | 0.0 | 100.0 | 5.1 | 0.0 | 5.9 | 37.9 |  |  |
| D2 MD-rate <= -1 dB/yr | 6 | 23.1 | 0.0 | 100.0 | 1.0 | 0.0 | 2.8 | 15.5 |  |  |
| D3 PLR >=3 points | 6 | 23.1 | 0.0 | 100.0 | 0.3 | 0.0 | 1.2 | 15.5 |  |  |
| D4 PoPLR (within-eye permutation) | 6 | 50.0 | 0.0 | 100.0 | 5.0 | 0.2 | 4.8 | 36.2 |  |  |
| D5 Pooled-shuffle conformal MD | 6 | 56.9 | 1.7 | 100.0 | 5.0 | 0.2 | 5.0 | 37.6 |  |  |
| D6 Pooled-detrended conformal region-max | 6 | 53.8 | 0.0 | 100.0 | 7.6 | 0.4 | 4.9 | 43.1 |  |  |
| D7 Event analysis (GPA-like) | 6 | 57.7 | 0.0 | 100.0 | 1.9 | 0.0 | 11.7 | 39.7 |  |  |
| D8 ML-tabular (LightGBM) | 6 | 70.8 | 3.4 | 100.0 | 3.6 | 0.7 | 8.7 | 42.1 |  |  |
| D9 ML-sequence (GRU) | 6 | 37.7 | 13.2 | 91.5 | 5.9 | 4.2 | 8.6 | 21.0 |  |  |
| D10 Self-supervised order net + permutation | 6 | 54.6 | 3.2 | 99.2 | 5.7 | 0.5 | 4.7 | 43.1 |  |  |

Table S2. All paired comparisons with D1 (exact McNemar test; Holm correction within each k and endpoint).

| k | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Only detector | Only D1 | p | Holm p |
|---|---|---|---|---|---|---|---|---|
| 3 | sensitivity | D10 Self-supervised order net + permutation | 26 | -19.2 (-34.6 to -3.8) | 0 | 5 | 0.0625 | 0.5 |
| 3 | sensitivity | D2 MD-rate <= -1 dB/yr | 26 | 19.2 (0.0 to 42.3) | 7 | 2 | 0.18 | 0.719 |
| 3 | sensitivity | D3 PLR >=3 points | 26 | -15.4 (-30.8 to -3.8) | 0 | 4 | 0.125 | 0.625 |
| 3 | sensitivity | D4 PoPLR (within-eye permutation) | 26 | -19.2 (-34.6 to -3.8) | 0 | 5 | 0.0625 | 0.5 |
| 3 | sensitivity | D5 Pooled-shuffle conformal MD | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 3 | sensitivity | D6 Pooled-detrended conformal region-max | 26 | 38.5 (19.2 to 57.7) | 10 | 0 | 0.00195 | 0.0176 |
| 3 | sensitivity | D7 Event analysis (GPA-like) | 26 | -19.2 (-34.6 to -3.8) | 0 | 5 | 0.0625 | 0.5 |
| 3 | sensitivity | D8 ML-tabular (LightGBM) | 26 | 7.7 (-11.5 to 26.9) | 4 | 2 | 0.688 | 1 |
| 3 | sensitivity | D9 ML-sequence (GRU) | 26 | -3.8 (-23.1 to 15.4) | 3 | 4 | 1 | 1 |
| 3 | false positives (1-spec) | D10 Self-supervised order net + permutation | 26 | -3.8 (-11.5 to 0.0) | 0 | 1 | 1 | 1 |
| 3 | false positives (1-spec) | D2 MD-rate <= -1 dB/yr | 26 | 3.8 (0.0 to 11.5) | 1 | 0 | 1 | 1 |
| 3 | false positives (1-spec) | D3 PLR >=3 points | 26 | 0.0 (-11.5 to 11.5) | 1 | 1 | 1 | 1 |
| 3 | false positives (1-spec) | D4 PoPLR (within-eye permutation) | 26 | -3.8 (-11.5 to 0.0) | 0 | 1 | 1 | 1 |
| 3 | false positives (1-spec) | D5 Pooled-shuffle conformal MD | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 3 | false positives (1-spec) | D6 Pooled-detrended conformal region-max | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 3 | false positives (1-spec) | D7 Event analysis (GPA-like) | 26 | -3.8 (-11.5 to 0.0) | 0 | 1 | 1 | 1 |
| 3 | false positives (1-spec) | D8 ML-tabular (LightGBM) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 3 | false positives (1-spec) | D9 ML-sequence (GRU) | 26 | -3.8 (-11.5 to 0.0) | 0 | 1 | 1 | 1 |
| 3 | GRAPE sensitivity | D2 MD-rate <= -1 dB/yr | 27 | 14.8 (-11.1 to 37.0) | 8 | 4 | 0.388 | 0.775 |
| 3 | GRAPE sensitivity | D3 PLR >=3 points | 27 | -40.7 (-63.0 to -18.5) | 1 | 12 | 0.00342 | 0.0137 |
| 3 | GRAPE sensitivity | D4 PoPLR (within-eye permutation) | 27 | -44.4 (-63.0 to -25.9) | 0 | 12 | 0.000488 | 0.00293 |
| 3 | GRAPE sensitivity | D5 Pooled-shuffle conformal MD | 27 | -3.7 (-11.1 to 0.0) | 0 | 1 | 1 | 1 |
| 3 | GRAPE sensitivity | D7 Event analysis (GPA-like) | 27 | -44.4 (-63.0 to -25.9) | 0 | 12 | 0.000488 | 0.00293 |
| 3 | GRAPE sensitivity | D8 ML-tabular (LightGBM) | 27 | 25.9 (0.0 to 48.1) | 10 | 3 | 0.0923 | 0.277 |
| 3 | GRAPE false positives | D2 MD-rate <= -1 dB/yr | 236 | 16.5 (11.0 to 22.0) | 44 | 5 | 7.6e-09 | 3.8e-08 |
| 3 | GRAPE false positives | D3 PLR >=3 points | 236 | -0.4 (-3.8 to 2.5) | 7 | 8 | 1 | 1 |
| 3 | GRAPE false positives | D4 PoPLR (within-eye permutation) | 236 | -4.7 (-7.6 to -2.1) | 0 | 11 | 0.000977 | 0.00391 |
| 3 | GRAPE false positives | D5 Pooled-shuffle conformal MD | 236 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 3 | GRAPE false positives | D7 Event analysis (GPA-like) | 236 | -4.7 (-7.6 to -2.1) | 0 | 11 | 0.000977 | 0.00391 |
| 3 | GRAPE false positives | D8 ML-tabular (LightGBM) | 236 | 33.5 (27.5 to 39.4) | 79 | 0 | 3.31e-24 | 1.99e-23 |
| 4 | sensitivity | D10 Self-supervised order net + permutation | 26 | -11.5 (-30.8 to 3.8) | 1 | 4 | 0.375 | 1 |
| 4 | sensitivity | D2 MD-rate <= -1 dB/yr | 26 | -7.7 (-23.1 to 7.7) | 1 | 3 | 0.625 | 1 |
| 4 | sensitivity | D3 PLR >=3 points | 26 | -15.4 (-34.6 to 0.0) | 1 | 5 | 0.219 | 1 |
| 4 | sensitivity | D4 PoPLR (within-eye permutation) | 26 | -26.9 (-46.2 to -11.5) | 0 | 7 | 0.0156 | 0.141 |
| 4 | sensitivity | D5 Pooled-shuffle conformal MD | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | sensitivity | D6 Pooled-detrended conformal region-max | 26 | -3.8 (-19.2 to 7.7) | 1 | 2 | 1 | 1 |
| 4 | sensitivity | D7 Event analysis (GPA-like) | 26 | -7.7 (-26.9 to 11.5) | 2 | 4 | 0.688 | 1 |
| 4 | sensitivity | D8 ML-tabular (LightGBM) | 26 | 11.5 (-3.8 to 30.8) | 4 | 1 | 0.375 | 1 |
| 4 | sensitivity | D9 ML-sequence (GRU) | 26 | -19.2 (-38.5 to 3.8) | 2 | 7 | 0.18 | 1 |
| 4 | false positives (1-spec) | D10 Self-supervised order net + permutation | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | false positives (1-spec) | D2 MD-rate <= -1 dB/yr | 26 | 3.8 (0.0 to 11.5) | 1 | 0 | 1 | 1 |
| 4 | false positives (1-spec) | D3 PLR >=3 points | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | false positives (1-spec) | D4 PoPLR (within-eye permutation) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | false positives (1-spec) | D5 Pooled-shuffle conformal MD | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | false positives (1-spec) | D6 Pooled-detrended conformal region-max | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | false positives (1-spec) | D7 Event analysis (GPA-like) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | false positives (1-spec) | D8 ML-tabular (LightGBM) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | false positives (1-spec) | D9 ML-sequence (GRU) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | GRAPE sensitivity | D2 MD-rate <= -1 dB/yr | 18 | 22.2 (-5.6 to 50.0) | 6 | 2 | 0.289 | 1 |
| 4 | GRAPE sensitivity | D3 PLR >=3 points | 18 | -22.2 (-38.9 to -5.6) | 0 | 4 | 0.125 | 0.75 |
| 4 | GRAPE sensitivity | D4 PoPLR (within-eye permutation) | 18 | -11.1 (-27.8 to 0.0) | 0 | 2 | 0.5 | 1 |
| 4 | GRAPE sensitivity | D5 Pooled-shuffle conformal MD | 18 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 4 | GRAPE sensitivity | D7 Event analysis (GPA-like) | 18 | -16.7 (-44.4 to 11.1) | 2 | 5 | 0.453 | 1 |
| 4 | GRAPE sensitivity | D8 ML-tabular (LightGBM) | 18 | 16.7 (-5.6 to 38.9) | 4 | 1 | 0.375 | 1 |
| 4 | GRAPE false positives | D2 MD-rate <= -1 dB/yr | 145 | 9.7 (4.8 to 15.2) | 16 | 2 | 0.00131 | 0.00656 |
| 4 | GRAPE false positives | D3 PLR >=3 points | 145 | -2.1 (-6.2 to 2.1) | 3 | 6 | 0.508 | 1 |
| 4 | GRAPE false positives | D4 PoPLR (within-eye permutation) | 145 | 0.7 (-4.1 to 5.5) | 6 | 5 | 1 | 1 |
| 4 | GRAPE false positives | D5 Pooled-shuffle conformal MD | 145 | 1.4 (0.0 to 3.4) | 2 | 0 | 0.5 | 1 |
| 4 | GRAPE false positives | D7 Event analysis (GPA-like) | 145 | 0.0 (-4.8 to 4.8) | 6 | 6 | 1 | 1 |
| 4 | GRAPE false positives | D8 ML-tabular (LightGBM) | 145 | 14.5 (9.0 to 20.7) | 21 | 0 | 9.54e-07 | 5.72e-06 |
| 5 | sensitivity | D10 Self-supervised order net + permutation | 26 | 7.7 (-7.7 to 23.1) | 3 | 1 | 0.625 | 1 |
| 5 | sensitivity | D2 MD-rate <= -1 dB/yr | 26 | -19.2 (-38.5 to 0.0) | 1 | 6 | 0.125 | 1 |
| 5 | sensitivity | D3 PLR >=3 points | 26 | -19.2 (-34.6 to -3.8) | 0 | 5 | 0.0625 | 0.562 |
| 5 | sensitivity | D4 PoPLR (within-eye permutation) | 26 | -3.8 (-11.5 to 0.0) | 0 | 1 | 1 | 1 |
| 5 | sensitivity | D5 Pooled-shuffle conformal MD | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | sensitivity | D6 Pooled-detrended conformal region-max | 26 | -11.5 (-30.8 to 7.7) | 2 | 5 | 0.453 | 1 |
| 5 | sensitivity | D7 Event analysis (GPA-like) | 26 | 7.7 (-11.5 to 26.9) | 4 | 2 | 0.688 | 1 |
| 5 | sensitivity | D8 ML-tabular (LightGBM) | 26 | 11.5 (0.0 to 26.9) | 3 | 0 | 0.25 | 1 |
| 5 | sensitivity | D9 ML-sequence (GRU) | 26 | 0.0 (-23.1 to 23.1) | 5 | 5 | 1 | 1 |
| 5 | false positives (1-spec) | D10 Self-supervised order net + permutation | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | false positives (1-spec) | D2 MD-rate <= -1 dB/yr | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | false positives (1-spec) | D3 PLR >=3 points | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | false positives (1-spec) | D4 PoPLR (within-eye permutation) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | false positives (1-spec) | D5 Pooled-shuffle conformal MD | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | false positives (1-spec) | D6 Pooled-detrended conformal region-max | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | false positives (1-spec) | D7 Event analysis (GPA-like) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | false positives (1-spec) | D8 ML-tabular (LightGBM) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 5 | false positives (1-spec) | D9 ML-sequence (GRU) | 26 | 7.7 (0.0 to 19.2) | 2 | 0 | 0.5 | 1 |
| 6 | sensitivity | D10 Self-supervised order net + permutation | 26 | 0.0 (-19.2 to 19.2) | 3 | 3 | 1 | 1 |
| 6 | sensitivity | D2 MD-rate <= -1 dB/yr | 26 | -34.6 (-57.7 to -15.4) | 1 | 10 | 0.0117 | 0.0938 |
| 6 | sensitivity | D3 PLR >=3 points | 26 | -34.6 (-53.8 to -19.2) | 0 | 9 | 0.00391 | 0.0352 |
| 6 | sensitivity | D4 PoPLR (within-eye permutation) | 26 | -7.7 (-26.9 to 11.5) | 2 | 4 | 0.688 | 1 |
| 6 | sensitivity | D5 Pooled-shuffle conformal MD | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | sensitivity | D6 Pooled-detrended conformal region-max | 26 | -3.8 (-19.2 to 11.5) | 2 | 3 | 1 | 1 |
| 6 | sensitivity | D7 Event analysis (GPA-like) | 26 | 0.0 (-19.2 to 15.4) | 3 | 3 | 1 | 1 |
| 6 | sensitivity | D8 ML-tabular (LightGBM) | 26 | 11.5 (-7.7 to 30.8) | 5 | 2 | 0.453 | 1 |
| 6 | sensitivity | D9 ML-sequence (GRU) | 26 | -11.5 (-38.5 to 11.5) | 4 | 7 | 0.549 | 1 |
| 6 | false positives (1-spec) | D10 Self-supervised order net + permutation | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | false positives (1-spec) | D2 MD-rate <= -1 dB/yr | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | false positives (1-spec) | D3 PLR >=3 points | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | false positives (1-spec) | D4 PoPLR (within-eye permutation) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | false positives (1-spec) | D5 Pooled-shuffle conformal MD | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | false positives (1-spec) | D6 Pooled-detrended conformal region-max | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | false positives (1-spec) | D7 Event analysis (GPA-like) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | false positives (1-spec) | D8 ML-tabular (LightGBM) | 26 | 0.0 (0.0 to 0.0) | 0 | 0 | 1 | 1 |
| 6 | false positives (1-spec) | D9 ML-sequence (GRU) | 26 | 7.7 (0.0 to 19.2) | 2 | 0 | 0.5 | 1 |

Table S3. External clinic (GRAPE): agreement with the secondary PLR2 and PLR3 progression labels (point estimates; seed means for D8).

| Detector | k | PLR2 sens % (n+) | PLR2 spec % (n−) | PLR3 sens % (n+) | PLR3 spec % (n−) |
|---|---|---|---|---|---|
| D1 | 3 | 17.5 (40) | 92.8 (223) | 21.4 (14) | 92.0 (249) |
| D2 | 3 | 45.0 (40) | 78.5 (223) | 57.1 (14) | 76.7 (249) |
| D3 | 3 | 17.5 (40) | 98.2 (223) | 28.6 (14) | 97.2 (249) |
| D4 | 3 | 0.0 (40) | 100.0 (223) | 0.0 (14) | 100.0 (249) |
| D5 | 3 | 17.5 (40) | 93.3 (223) | 21.4 (14) | 92.4 (249) |
| D7 | 3 | 0.0 (40) | 100.0 (223) | 0.0 (14) | 100.0 (249) |
| D8 | 3 | 61.0 (40) | 61.9 (223) | 72.9 (14) | 60.2 (249) |
| D1 | 4 | 16.1 (31) | 94.7 (132) | 16.7 (12) | 93.4 (151) |
| D2 | 4 | 38.7 (31) | 86.4 (132) | 50.0 (12) | 84.1 (151) |
| D3 | 4 | 16.1 (31) | 100.0 (132) | 33.3 (12) | 99.3 (151) |
| D4 | 4 | 22.6 (31) | 97.0 (132) | 33.3 (12) | 95.4 (151) |
| D5 | 4 | 20.6 (31) | 94.2 (132) | 23.3 (12) | 92.6 (151) |
| D7 | 4 | 16.1 (31) | 97.0 (132) | 33.3 (12) | 96.7 (151) |
| D8 | 4 | 43.9 (31) | 83.3 (132) | 53.3 (12) | 80.7 (151) |

## S4. Analyses added after internal review (not in the protocol)

Table S4. Cumulative false alarms on true no-change series (Artes windows starting at the first test; same donor-date draw index across k, donor dates redrawn for each k, so the estimate is approximate).

| Detector | Flagged at least once, k = 3–6, % | Mean per-look false-alarm rate, % |
|---|---|---|
| D1 | 15.3 | 5.2 |
| D2 | 6.7 | 1.7 |
| D3 | 2.3 | 0.7 |
| D4 | 14.5 | 4.9 |
| D5 | 15.0 | 4.7 |
| D6 | 39.4 | 11.4 |
| D7 | 3.3 | 2.5 |
| D8 | 50.8 | 17.2 |
| D9 | 22.9 | 8.1 |
| D10 | 11.6 | 3.5 |

Validity under the strict literal protocol rule (upper 95% CI limit of the false-alarm rate at or below 5%) was met only by: D10@3, D2@3, D3@3, D4@3, D7@3, D2@4, D3@4, D4@4, D7@4, D9@4, D2@5, D3@5, D7@5, D2@6, D3@6, D7@6. The smallest sensitivity gain over D1 that could reach Holm-adjusted significance was 9 of 26 progressors (34.6 percentage points). Bootstrap 95% CI for the shuffle-audit Spearman correlation, resampling detector–k cells: 0.35 to 0.85.