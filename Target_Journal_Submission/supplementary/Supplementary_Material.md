# Supplementary Material

Apparent Gains in Detecting Glaucomatous Visual-Field Progression Disappear at Matched False-Alarm Rates: A Two-Stage Benchmark

## S1. Development history, including abandoned ideas

This section reproduces the development log kept before Study 1. Pilot numbers were computed on the training and validation splits of UWHVF (and, in round 5, on the Artes retest data), never on the locked test split. Study 1 was specified after round 5; Study 2 was specified after Study 1 (protocol_v2). Round 4 explored a different clinical problem and was abandoned.

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

## S2. Study 1 protocol amendments (made before any final result)

### Amendment A1 (2026-11-23, before any final result)
Artes tests are one week apart. Rate-based rules (D2, D3, D7, D8, D9) are not invariant to the time scale, so each
Artes window of k tests is assigned the test times of a randomly drawn UW-test eye with >= k tests (10 draws per
window). Under true no change the time labels carry no signal, so this keeps the arm a valid null at clinical spacing.

### Amendment A2 (2026-11-23, before any final result)
GRAPE was measured with a different perimeter (59 analysable points after removing points coded -1; dB scale differs
from Humphrey). Therefore on GRAPE: D5 calibration pool and D7 change limits come from GRAPE itself by 5-fold
patient-level cross-fitting ("own-clinic calibration"); D8 is the UWHVF-trained model applied unchanged (transfer
test, grid-agnostic features); D6, D9, D10 (24-2 specific) are not evaluated on GRAPE.


## S3. Study 1 statistical methods in full, including the validity-rule deviation

In Study 1, proportions are reported with 95% confidence intervals from 2,000 bootstrap resamples of patients, which accounts for two eyes per patient and repeated windows per patient. We compared each detector with D1 on the same eyes using the exact McNemar test and corrected p-values for the nine comparisons within each number of tests and endpoint with the Holm method. For stochastic detectors, the paired tests used each eye's majority flag across seeds. Confidence intervals for paired differences came from 2,000 bootstrap resamples of eyes. Because of the majority flag, paired differences can differ slightly from differences between the seed-averaged percentages in the tables. With 26 progressors and nine comparisons, a sensitivity gain over D1 could reach Holm-adjusted significance only if at least 9 more progressors were flagged (34.6 percentage points). The protocol stated that validity would be judged by comparing the upper confidence limit of the false-alarm rate on true no-change data with 5%. Read literally (upper limit at or below 5%), this rule could not be met even by D1, whose false-alarm rate was close to the nominal 5%, because the true no-change arm has only 30 patients. Before the final results were available, the analysis plan in our draft Methods specified a working rule: the upper limit must not exceed 10% and the point estimate must not exceed 5% by more than sampling error. After the results were available, we made the second part operational as "the lower confidence limit is at or below 5%". We call a detector valid under this rule, and we report the strict literal rule as a sensitivity analysis. This sequence is a deviation from the protocol. To express false alarms in clinical units, we report the expected number of false progression flags per 1,000 stable eyes at one review. We also report, among reference progressors, the share flagged at least once by the sixth test, and, as a matching measure, the share of true no-change series flagged at least once across the looks at three to six tests (window starting at the first test). These cumulative measures, the strict validity rule, a confidence interval for the shuffle-audit correlation (resampling detector–test-number cells) and the GRAPE results for the PLR labels were added after internal review and were not in the protocol. Agreement between the shuffle audit and the true no-change false-alarm rate was summarised by the Spearman correlation across detector–test-number cells and by their absolute difference. Analyses used Python 3.13 with NumPy, SciPy, pandas, scikit-learn, LightGBM and PyTorch. The Study 1 run took 24 minutes on a 4-core CPU without a graphics card.



Under the strict literal rule (upper 95% limit of the false-alarm rate at or below 5%), only the following detector–k cells were valid in Study 1: D10@3, D2@3, D3@3, D4@3, D7@3, D2@4, D3@4, D4@4, D7@4, D9@4, D2@5, D3@5, D7@5, D2@6, D3@6, D7@6; D1 failed it at every k (upper limits 6.3%, 6.2%, 7.5%, 8.1%), and no strict-valid detector was significantly more sensitive than D1. With 26 progressors, the smallest significant gain was 9 eyes (34.6 percentage points). Bootstrap 95% CI of the shuffle-audit Spearman correlation, resampling detector–k cells: 0.35 to 0.85.

## S4. Supplementary tables

Table S1. Study 1: all metrics by detector and number of tests (k). Seed SD across five seeds; FA, false-alarm rate; PoPLR ref, secondary reference; detector names are internal code names (D1 OLS-MD = trend test; D2 MD-rate = rate rule on mean sensitivity).

| Detector | k | Sens % (95% CI) | Seed SD | Spec % | FA true null % (95% CI) | FA shuffle % | Sens, PoPLR ref % | GRAPE sens % | GRAPE spec % |
|---|---|---|---|---|---|---|---|---|---|
| D1 OLS-MD | 3 | 19.2 (7.4–33.3) | 0.0 | 96.2 | 4.4 (2.8–6.3) | 4.8 | 10.3 | 44.4 | 95.3 |
| D2 MD-rate <= -1 dB/yr | 3 | 38.5 (20.0–56.5) | 0.0 | 92.3 | 2.6 (1.5–3.9) | 11.7 | 24.1 | 59.3 | 78.8 |
| D3 PLR >=3 points | 3 | 3.8 (0.0–12.5) | 0.0 | 96.2 | 1.4 (1.0–1.8) | 1.8 | 1.7 | 3.7 | 95.8 |
| D4 PoPLR (within-eye permutation) | 3 | 0.0 (0.0–0.0) | 0.0 | 100.0 | 0.0 (0.0–0.0) | 0.0 | 0.0 | 0.0 | 100.0 |
| D5 Pooled-shuffle conformal MD | 3 | 19.2 (7.4–33.3) | 0.0 | 96.2 | 4.0 (2.7–5.6) | 4.6 | 10.0 | 41.5 | 95.4 |
| D6 Pooled-detrended conformal region-max | 3 | 56.9 (37.0–76.2) | 1.7 | 96.2 | 22.4 (19.3–25.7) | 22.5 | 46.2 |  |  |
| D7 Event analysis (GPA-like) | 3 | 0.0 (0.0–0.0) | 0.0 | 100.0 | 0.0 (0.0–0.0) | 0.0 | 0.0 | 0.0 | 100.0 |
| D8 ML-tabular (LightGBM) | 3 | 26.2 (12.3–43.2) | 5.0 | 94.6 | 27.7 (22.7–32.9) | 17.3 | 24.1 | 65.9 | 61.2 |
| D9 ML-sequence (GRU) | 3 | 12.3 (2.4–24.8) | 5.0 | 95.4 | 12.7 (6.2–20.0) | 8.5 | 9.7 |  |  |
| D10 Self-supervised order net + permutation | 3 | 0.0 (0.0–0.0) | 0.0 | 100.0 | 0.0 (0.0–0.0) | 0.0 | 0.0 |  |  |
| D1 OLS-MD | 4 | 30.8 (14.3–48.1) | 0.0 | 100.0 | 3.8 (1.9–6.2) | 4.7 | 20.7 | 33.3 | 95.9 |
| D2 MD-rate <= -1 dB/yr | 4 | 23.1 (8.0–40.0) | 0.0 | 96.2 | 0.6 (0.4–0.9) | 6.4 | 12.1 | 55.6 | 86.2 |
| D3 PLR >=3 points | 4 | 15.4 (3.6–30.8) | 0.0 | 100.0 | 0.2 (0.0–0.3) | 1.5 | 10.3 | 11.1 | 97.9 |
| D4 PoPLR (within-eye permutation) | 4 | 3.8 (0.0–12.5) | 0.0 | 100.0 | 3.3 (1.8–4.9) | 4.1 | 8.6 | 22.2 | 95.2 |
| D5 Pooled-shuffle conformal MD | 4 | 30.8 (14.3–48.1) | 0.0 | 100.0 | 3.6 (1.8–5.9) | 4.9 | 20.7 | 33.3 | 94.5 |
| D6 Pooled-detrended conformal region-max | 4 | 25.4 (10.3–44.0) | 2.1 | 100.0 | 5.1 (3.4–7.2) | 5.5 | 16.6 |  |  |
| D7 Event analysis (GPA-like) | 4 | 23.1 (7.7–40.0) | 0.0 | 100.0 | 1.1 (0.0–2.6) | 5.2 | 13.8 | 16.7 | 95.9 |
| D8 ML-tabular (LightGBM) | 4 | 41.5 (23.7–59.2) | 5.0 | 99.2 | 9.4 (6.3–12.9) | 7.7 | 24.8 | 48.9 | 81.5 |
| D9 ML-sequence (GRU) | 4 | 11.5 (2.8–23.2) | 3.8 | 99.2 | 2.0 (0.6–3.7) | 4.7 | 7.2 |  |  |
| D10 Self-supervised order net + permutation | 4 | 20.0 (7.7–35.8) | 4.2 | 100.0 | 3.8 (2.5–5.1) | 4.1 | 12.1 |  |  |
| D1 OLS-MD | 5 | 42.3 (23.1–61.5) | 0.0 | 100.0 | 4.7 (2.2–7.5) | 5.1 | 27.6 |  |  |
| D2 MD-rate <= -1 dB/yr | 5 | 23.1 (7.7–41.4) | 0.0 | 100.0 | 0.8 (0.5–1.2) | 3.6 | 13.8 |  |  |
| D3 PLR >=3 points | 5 | 23.1 (8.0–40.0) | 0.0 | 100.0 | 0.5 (0.1–1.1) | 1.4 | 15.5 |  |  |
| D4 PoPLR (within-eye permutation) | 5 | 38.5 (20.0–57.7) | 0.0 | 100.0 | 3.9 (1.9–6.2) | 4.3 | 24.1 |  |  |
| D5 Pooled-shuffle conformal MD | 5 | 42.3 (23.1–61.5) | 0.0 | 100.0 | 4.3 (2.0–7.1) | 4.9 | 27.6 |  |  |
| D6 Pooled-detrended conformal region-max | 5 | 31.5 (16.0–48.5) | 1.7 | 100.0 | 6.2 (3.7–8.9) | 5.0 | 21.0 |  |  |
| D7 Event analysis (GPA-like) | 5 | 50.0 (30.4–69.6) | 0.0 | 100.0 | 1.2 (0.0–2.9) | 7.9 | 31.0 |  |  |
| D8 ML-tabular (LightGBM) | 5 | 56.2 (36.1–74.8) | 2.1 | 99.2 | 18.8 (13.1–24.9) | 16.1 | 38.3 |  |  |
| D9 ML-sequence (GRU) | 5 | 40.8 (22.8–59.2) | 8.9 | 93.8 | 7.5 (2.8–13.3) | 8.1 | 25.9 |  |  |
| D10 Self-supervised order net + permutation | 5 | 43.8 (28.0–60.0) | 3.4 | 100.0 | 5.1 (2.9–7.6) | 4.2 | 27.9 |  |  |
| D1 OLS-MD | 6 | 57.7 (38.4–76.9) | 0.0 | 100.0 | 5.1 (2.5–8.1) | 5.9 | 37.9 |  |  |
| D2 MD-rate <= -1 dB/yr | 6 | 23.1 (8.3–38.5) | 0.0 | 100.0 | 1.0 (0.6–1.5) | 2.8 | 15.5 |  |  |
| D3 PLR >=3 points | 6 | 23.1 (7.7–41.7) | 0.0 | 100.0 | 0.3 (0.0–0.8) | 1.2 | 15.5 |  |  |
| D4 PoPLR (within-eye permutation) | 6 | 50.0 (30.8–67.9) | 0.0 | 100.0 | 5.0 (2.4–8.4) | 4.8 | 36.2 |  |  |
| D5 Pooled-shuffle conformal MD | 6 | 56.9 (37.7–76.0) | 1.7 | 100.0 | 5.0 (2.4–7.9) | 5.0 | 37.6 |  |  |
| D6 Pooled-detrended conformal region-max | 6 | 53.8 (37.0–71.4) | 0.0 | 100.0 | 7.6 (4.5–11.1) | 4.9 | 43.1 |  |  |
| D7 Event analysis (GPA-like) | 6 | 57.7 (36.0–77.8) | 0.0 | 100.0 | 1.9 (0.5–3.8) | 11.7 | 39.7 |  |  |
| D8 ML-tabular (LightGBM) | 6 | 70.8 (51.7–88.8) | 3.4 | 100.0 | 3.6 (1.7–6.0) | 8.7 | 42.1 |  |  |
| D9 ML-sequence (GRU) | 6 | 37.7 (22.3–53.8) | 13.2 | 91.5 | 5.9 (2.3–10.0) | 8.6 | 21.0 |  |  |
| D10 Self-supervised order net + permutation | 6 | 54.6 (36.9–70.8) | 3.2 | 99.2 | 5.7 (3.0–9.2) | 4.7 | 43.1 |  |  |

Table S2. Study 2: all per-review metrics. R1, primary reference; R2, flat-stable reference; R3, future-only reference (n shown); FA, false-alarm rate on true no-change series; strict valid, upper 95% limit at or below 5%.

| Detector | k | Sens R1 % (95% CI) | Seed SD | Spec R1 % | Spec R2 % | Sens R3 % (n) | Spec R3 % (n) | FA true null % (95% CI) | Valid | Strict valid |
|---|---|---|---|---|---|---|---|---|---|---|
| D1 OLS-MD | 3 | 14.7 (9.3–20.5) | 0.0 | 96.3 | 95.2 | 8.4 (95) | 93.0 (187) | 4.2 (2.8–5.7) | yes | no |
| D1 OLS-MD | 4 | 26.7 (19.7–34.0) | 0.0 | 95.7 | 93.2 | 13.4 (67) | 89.1 (119) | 3.9 (2.1–6.2) | yes | no |
| D1 OLS-MD | 5 | 40.0 (32.2–47.9) | 0.0 | 97.6 | 94.5 | 27.9 (43) | 89.0 (91) | 4.5 (2.0–7.2) | yes | no |
| D1 OLS-MD | 6 | 57.3 (49.0–66.4) | 0.0 | 99.4 | 94.8 | 32.4 (34) | 82.2 (73) | 5.5 (2.9–8.4) | yes | no |
| D7 Event | 3 | 0.0 (0.0–0.0) | 0.0 | 100.0 | 100.0 | 0.0 (95) | 100.0 (187) | 0.0 (0.0–0.0) | yes | yes |
| D7 Event | 4 | 16.0 (10.3–22.7) | 0.0 | 93.3 | 96.1 | 1.5 (67) | 90.8 (119) | 0.8 (0.0–1.9) | yes | yes |
| D7 Event | 5 | 32.7 (24.8–41.4) | 0.0 | 90.9 | 93.9 | 16.3 (43) | 90.1 (91) | 0.9 (0.0–2.1) | yes | yes |
| D7 Event | 6 | 46.0 (37.8–54.7) | 0.0 | 89.0 | 91.0 | 26.5 (34) | 84.9 (73) | 1.5 (0.3–3.1) | yes | yes |
| S1 SC-Trend | 3 | 15.3 (9.9–21.4) | 0.0 | 96.3 | 95.2 | 8.4 (95) | 92.5 (187) | 4.6 (3.1–6.2) | yes | no |
| S1 SC-Trend | 4 | 29.3 (22.1–36.9) | 0.7 | 95.3 | 92.9 | 16.9 (67) | 87.7 (119) | 4.2 (2.2–6.6) | yes | no |
| S1 SC-Trend | 5 | 40.4 (32.4–48.4) | 0.4 | 97.6 | 94.5 | 27.9 (43) | 89.0 (91) | 4.6 (2.1–7.4) | yes | no |
| S1 SC-Trend | 6 | 56.7 (48.4–65.6) | 0.7 | 99.4 | 95.1 | 30.4 (34) | 83.6 (73) | 5.5 (2.9–8.4) | yes | no |
| S2 SC-Rate | 3 | 5.3 (1.9–9.7) | 0.0 | 89.6 | 96.1 | 4.2 (95) | 90.7 (187) | 0.7 (0.4–0.9) | yes | yes |
| S2 SC-Rate | 4 | 16.0 (10.7–21.6) | 0.0 | 93.3 | 97.1 | 4.5 (67) | 89.1 (119) | 0.6 (0.4–0.8) | yes | yes |
| S2 SC-Rate | 5 | 24.7 (18.1–32.4) | 0.0 | 94.5 | 96.9 | 18.6 (43) | 92.3 (91) | 0.6 (0.4–0.8) | yes | yes |
| S2 SC-Rate | 6 | 34.0 (26.7–41.9) | 0.0 | 97.0 | 97.7 | 14.7 (34) | 87.7 (73) | 0.5 (0.4–0.7) | yes | yes |
| S3 SC-PoPLR | 3 | 16.0 (9.7–22.6) | 0.0 | 91.5 | 91.6 | 8.4 (95) | 87.2 (187) | 0.1 (0.0–0.2) | yes | yes |
| S3 SC-PoPLR | 4 | 27.3 (20.7–34.7) | 0.0 | 89.8 | 88.5 | 14.9 (67) | 83.2 (119) | 0.2 (0.0–0.4) | yes | yes |
| S3 SC-PoPLR | 5 | 39.6 (31.3–47.8) | 0.4 | 96.1 | 92.3 | 35.7 (43) | 84.2 (91) | 0.5 (0.0–1.3) | yes | yes |
| S3 SC-PoPLR | 6 | 47.8 (39.1–56.9) | 0.4 | 97.4 | 90.6 | 26.5 (34) | 75.3 (73) | 0.1 (0.0–0.3) | yes | yes |
| S4 SC-Event | 3 | 5.3 (2.0–9.6) | 0.0 | 95.7 | 98.1 | 3.2 (95) | 95.7 (187) | 0.0 (0.0–0.0) | yes | yes |
| S4 SC-Event | 4 | 13.3 (8.0–19.4) | 0.0 | 95.1 | 97.4 | 0.0 (67) | 91.6 (119) | 0.2 (0.0–0.7) | yes | yes |
| S4 SC-Event | 5 | 18.7 (12.4–25.2) | 0.0 | 95.7 | 97.1 | 9.3 (43) | 93.4 (91) | 0.0 (0.0–0.0) | yes | yes |
| S4 SC-Event | 6 | 22.2 (15.8–29.2) | 1.4 | 99.0 | 99.1 | 1.0 (34) | 92.7 (73) | 0.0 (0.0–0.0) | yes | yes |
| S5 SC-LightGBM | 3 | 14.2 (9.3–19.7) | 1.5 | 97.4 | 95.6 | 8.8 (95) | 95.9 (187) | 8.1 (6.2–10.1) | no | no |
| S5 SC-LightGBM | 4 | 18.0 (12.6–24.0) | 1.3 | 97.8 | 95.9 | 12.9 (67) | 94.7 (119) | 7.0 (4.8–9.5) | yes | no |
| S5 SC-LightGBM | 5 | 28.9 (22.3–36.1) | 2.0 | 98.2 | 94.8 | 23.3 (43) | 89.7 (91) | 7.6 (5.0–10.5) | no | no |
| S5 SC-LightGBM | 6 | 59.6 (51.1–68.5) | 0.4 | 99.0 | 94.5 | 34.3 (34) | 79.5 (73) | 2.6 (1.1–4.4) | yes | yes |
| S6 Order-LightGBM | 3 | 15.3 (10.7–20.5) | 2.0 | 90.9 | 92.6 | 6.0 (95) | 88.1 (187) | 2.2 (1.6–2.8) | yes | yes |
| S6 Order-LightGBM | 4 | 20.2 (14.9–26.0) | 3.3 | 93.7 | 92.3 | 11.4 (67) | 90.5 (119) | 2.3 (1.5–3.2) | yes | yes |
| S6 Order-LightGBM | 5 | 35.1 (28.6–42.2) | 1.0 | 96.3 | 92.7 | 22.5 (43) | 84.6 (91) | 2.8 (1.8–4.0) | yes | yes |
| S6 Order-LightGBM | 6 | 54.2 (46.5–62.4) | 0.8 | 97.0 | 91.2 | 33.3 (34) | 78.1 (73) | 4.4 (2.8–6.4) | yes | no |
| S7 SC-GRU | 3 | 6.9 (3.5–10.9) | 1.4 | 94.5 | 96.0 | 3.5 (95) | 94.7 (187) | 2.9 (1.1–5.3) | yes | no |
| S7 SC-GRU | 4 | 8.0 (4.4–12.2) | 0.0 | 93.9 | 96.2 | 1.5 (67) | 93.8 (119) | 1.5 (0.5–2.6) | yes | yes |
| S7 SC-GRU | 5 | 18.2 (12.6–24.7) | 2.1 | 95.9 | 96.3 | 10.9 (43) | 91.2 (91) | 2.2 (0.9–3.8) | yes | yes |
| S7 SC-GRU | 6 | 20.7 (14.8–27.4) | 2.3 | 95.7 | 96.3 | 5.9 (34) | 90.4 (73) | 1.6 (0.5–2.9) | yes | yes |
| B8 LightGBM-95spec | 3 | 18.7 (12.7–25.4) | 1.2 | 94.7 | 91.8 | 11.2 (95) | 92.0 (187) | 13.9 (10.9–17.1) | no | no |
| B8 LightGBM-95spec | 4 | 44.9 (36.6–53.2) | 1.0 | 90.0 | 86.9 | 26.4 (67) | 77.3 (119) | 21.7 (17.3–26.1) | no | no |
| B8 LightGBM-95spec | 5 | 58.9 (51.7–66.4) | 1.7 | 90.9 | 86.1 | 53.5 (43) | 72.2 (91) | 26.4 (20.9–31.8) | no | no |
| B8 LightGBM-95spec | 6 | 79.3 (72.7–86.2) | 0.0 | 88.8 | 79.0 | 60.8 (34) | 60.3 (73) | 15.3 (11.5–19.1) | no | no |

Table S3. Study 1: paired comparisons with D1 (exact McNemar; Holm within k and endpoint).

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

Table S4. Study 2: paired comparisons with D1 (sensitivity R1, specificity R1 and R2; Holm across D7 and S1–S7 within k; B8 unadjusted).

| k | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Only detector | Only D1 | p | Holm p |
|---|---|---|---|---|---|---|---|---|
| 3 | sens | D7 Event | 150 | -14.7 (-20.5 to -9.3) | 0 | 22 | 4.77e-07 | 3.81e-06 |
| 3 | sens | S1 SC-Trend | 150 | 0.7 (0.0 to 2.1) | 1 | 0 | 1 | 1 |
| 3 | sens | S2 SC-Rate | 150 | -9.3 (-16.0 to -3.3) | 6 | 20 | 0.00936 | 0.0561 |
| 3 | sens | S3 SC-PoPLR | 150 | 1.3 (-4.5 to 7.1) | 12 | 10 | 0.832 | 1 |
| 3 | sens | S4 SC-Event | 150 | -9.3 (-15.5 to -3.4) | 4 | 18 | 0.00434 | 0.0304 |
| 3 | sens | S5 SC-LightGBM | 150 | -0.4 (-7.4 to 6.4) | 14 | 14 | 1 | 1 |
| 3 | sens | S6 Order-LightGBM | 150 | 0.7 (-5.0 to 5.8) | 12 | 11 | 1 | 1 |
| 3 | sens | S7 SC-GRU | 150 | -7.8 (-14.4 to -1.5) | 8 | 20 | 0.0357 | 0.178 |
| 3 | sens | B8 LightGBM-95spec | 150 | 4.0 (-3.4 to 11.0) | 18 | 13 | 0.473 |  |
| 3 | spec_R1 | D7 Event | 164 | 3.7 (1.2 to 6.7) | 0 | 6 | 0.0312 | 0.188 |
| 3 | spec_R1 | S1 SC-Trend | 164 | -0.0 (-0.0 to -0.0) | 0 | 0 | 1 | 1 |
| 3 | spec_R1 | S2 SC-Rate | 164 | -6.7 (-11.7 to -1.8) | 13 | 2 | 0.00739 | 0.0591 |
| 3 | spec_R1 | S3 SC-PoPLR | 164 | -4.9 (-9.4 to -1.2) | 9 | 1 | 0.0215 | 0.15 |
| 3 | spec_R1 | S4 SC-Event | 164 | -0.6 (-5.3 to 3.8) | 6 | 5 | 1 | 1 |
| 3 | spec_R1 | S5 SC-LightGBM | 164 | 1.0 (-2.7 to 4.9) | 4 | 6 | 0.754 | 1 |
| 3 | spec_R1 | S6 Order-LightGBM | 164 | -5.5 (-9.2 to -1.9) | 12 | 3 | 0.0352 | 0.188 |
| 3 | spec_R1 | S7 SC-GRU | 164 | -1.8 (-6.1 to 2.6) | 7 | 5 | 0.774 | 1 |
| 3 | spec_R1 | B8 LightGBM-95spec | 164 | -1.6 (-6.0 to 2.4) | 8 | 6 | 0.791 |  |
| 3 | spec_R2 | D7 Event | 310 | 4.8 (2.6 to 7.1) | 0 | 15 | 6.1e-05 | 0.000488 |
| 3 | spec_R2 | S1 SC-Trend | 310 | -0.0 (-0.0 to -0.0) | 0 | 0 | 1 | 1 |
| 3 | spec_R2 | S2 SC-Rate | 310 | 1.0 (-1.6 to 3.5) | 7 | 10 | 0.629 | 1 |
| 3 | spec_R2 | S3 SC-PoPLR | 310 | -3.5 (-7.1 to -0.0) | 19 | 8 | 0.0522 | 0.366 |
| 3 | spec_R2 | S4 SC-Event | 310 | 2.9 (-0.0 to 5.7) | 5 | 14 | 0.0636 | 0.381 |
| 3 | spec_R2 | S5 SC-LightGBM | 310 | 0.4 (-2.5 to 3.3) | 11 | 13 | 0.839 | 1 |
| 3 | spec_R2 | S6 Order-LightGBM | 310 | -2.6 (-5.8 to 0.6) | 19 | 12 | 0.281 | 1 |
| 3 | spec_R2 | S7 SC-GRU | 310 | 0.9 (-2.6 to 4.0) | 11 | 14 | 0.69 | 1 |
| 3 | spec_R2 | B8 LightGBM-95spec | 310 | -3.3 (-6.7 to -0.1) | 19 | 11 | 0.2 |  |
| 4 | sens | D7 Event | 150 | -10.7 (-17.9 to -3.3) | 10 | 26 | 0.0113 | 0.0567 |
| 4 | sens | S1 SC-Trend | 150 | 2.7 (0.7 to 5.3) | 5 | 0 | 0.0625 | 0.125 |
| 4 | sens | S2 SC-Rate | 150 | -10.7 (-18.0 to -3.8) | 10 | 26 | 0.0113 | 0.0567 |
| 4 | sens | S3 SC-PoPLR | 150 | 0.7 (-6.3 to 8.3) | 15 | 14 | 1 | 1 |
| 4 | sens | S4 SC-Event | 150 | -13.3 (-20.1 to -6.8) | 7 | 27 | 0.000821 | 0.00493 |
| 4 | sens | S5 SC-LightGBM | 150 | -8.7 (-16.3 to -0.7) | 13 | 27 | 0.0385 | 0.115 |
| 4 | sens | S6 Order-LightGBM | 150 | -6.4 (-11.4 to -1.4) | 2 | 18 | 0.000402 | 0.00282 |
| 4 | sens | S7 SC-GRU | 150 | -18.7 (-26.2 to -11.6) | 5 | 34 | 2.43e-06 | 1.94e-05 |
| 4 | sens | B8 LightGBM-95spec | 150 | 18.2 (9.7 to 26.8) | 38 | 11 | 0.000142 |  |
| 4 | spec_R1 | D7 Event | 164 | -2.4 (-7.9 to 2.5) | 9 | 5 | 0.424 | 1 |
| 4 | spec_R1 | S1 SC-Trend | 164 | -0.4 (-1.3 to -0.0) | 1 | 0 | 1 | 1 |
| 4 | spec_R1 | S2 SC-Rate | 164 | -2.4 (-7.7 to 2.4) | 9 | 5 | 0.424 | 1 |
| 4 | spec_R1 | S3 SC-PoPLR | 164 | -5.9 (-9.5 to -2.6) | 10 | 0 | 0.00195 | 0.0156 |
| 4 | spec_R1 | S4 SC-Event | 164 | -0.6 (-5.1 to 3.7) | 6 | 5 | 1 | 1 |
| 4 | spec_R1 | S5 SC-LightGBM | 164 | 2.0 (-1.0 to 5.2) | 2 | 5 | 0.453 | 1 |
| 4 | spec_R1 | S6 Order-LightGBM | 164 | -2.0 (-5.2 to 1.4) | 5 | 5 | 1 | 1 |
| 4 | spec_R1 | S7 SC-GRU | 164 | -1.8 (-7.0 to 2.7) | 9 | 7 | 0.804 | 1 |
| 4 | spec_R1 | B8 LightGBM-95spec | 164 | -5.7 (-10.5 to -1.2) | 12 | 3 | 0.0352 |  |
| 4 | spec_R2 | D7 Event | 310 | 2.9 (-0.3 to 6.3) | 8 | 17 | 0.108 | 0.539 |
| 4 | spec_R2 | S1 SC-Trend | 310 | -0.3 (-1.0 to -0.0) | 1 | 0 | 1 | 1 |
| 4 | spec_R2 | S2 SC-Rate | 310 | 3.9 (1.0 to 6.8) | 5 | 17 | 0.0169 | 0.101 |
| 4 | spec_R2 | S3 SC-PoPLR | 310 | -4.7 (-8.0 to -1.6) | 22 | 7 | 0.00813 | 0.0576 |
| 4 | spec_R2 | S4 SC-Event | 310 | 4.2 (1.5 to 7.2) | 4 | 17 | 0.0072 | 0.0576 |
| 4 | spec_R2 | S5 SC-LightGBM | 310 | 2.7 (-0.4 to 5.8) | 9 | 17 | 0.169 | 0.598 |
| 4 | spec_R2 | S6 Order-LightGBM | 310 | -1.0 (-3.4 to 1.6) | 10 | 11 | 1 | 1 |
| 4 | spec_R2 | S7 SC-GRU | 310 | 3.0 (-0.4 to 6.4) | 11 | 20 | 0.15 | 0.598 |
| 4 | spec_R2 | B8 LightGBM-95spec | 310 | -6.3 (-10.6 to -2.6) | 32 | 12 | 0.00366 |  |
| 5 | sens | D7 Event | 150 | -7.3 (-15.0 to 0.0) | 12 | 23 | 0.0895 | 0.358 |
| 5 | sens | S1 SC-Trend | 150 | 0.4 (0.0 to 1.4) | 1 | 0 | 1 | 1 |
| 5 | sens | S2 SC-Rate | 150 | -15.3 (-23.0 to -8.1) | 8 | 31 | 0.000294 | 0.00176 |
| 5 | sens | S3 SC-PoPLR | 150 | -0.4 (-8.1 to 6.9) | 16 | 17 | 1 | 1 |
| 5 | sens | S4 SC-Event | 150 | -21.3 (-29.8 to -13.7) | 7 | 39 | 1.83e-06 | 1.47e-05 |
| 5 | sens | S5 SC-LightGBM | 150 | -11.1 (-18.5 to -3.7) | 11 | 28 | 0.00948 | 0.0474 |
| 5 | sens | S6 Order-LightGBM | 150 | -4.9 (-10.7 to 0.5) | 10 | 19 | 0.136 | 0.408 |
| 5 | sens | S7 SC-GRU | 150 | -21.8 (-29.8 to -13.7) | 9 | 42 | 3.39e-06 | 2.37e-05 |
| 5 | sens | B8 LightGBM-95spec | 150 | 18.9 (12.0 to 25.6) | 34 | 5 | 2.43e-06 |  |
| 5 | spec_R1 | D7 Event | 164 | -6.7 (-12.6 to -1.3) | 13 | 2 | 0.00739 | 0.0591 |
| 5 | spec_R1 | S1 SC-Trend | 164 | -0.0 (-0.0 to -0.0) | 0 | 0 | 1 | 1 |
| 5 | spec_R1 | S2 SC-Rate | 164 | -3.0 (-7.6 to 1.2) | 7 | 2 | 0.18 | 1 |
| 5 | spec_R1 | S3 SC-PoPLR | 164 | -1.4 (-4.0 to 0.8) | 3 | 1 | 0.625 | 1 |
| 5 | spec_R1 | S4 SC-Event | 164 | -1.8 (-5.8 to 1.9) | 6 | 3 | 0.508 | 1 |
| 5 | spec_R1 | S5 SC-LightGBM | 164 | 0.6 (-2.4 to 3.7) | 3 | 4 | 1 | 1 |
| 5 | spec_R1 | S6 Order-LightGBM | 164 | -1.2 (-3.5 to 1.0) | 3 | 1 | 0.625 | 1 |
| 5 | spec_R1 | S7 SC-GRU | 164 | -1.6 (-5.2 to 1.4) | 4 | 2 | 0.688 | 1 |
| 5 | spec_R1 | B8 LightGBM-95spec | 164 | -6.7 (-11.4 to -2.2) | 12 | 2 | 0.0129 |  |
| 5 | spec_R2 | D7 Event | 310 | -0.6 (-4.4 to 3.1) | 16 | 14 | 0.856 | 1 |
| 5 | spec_R2 | S1 SC-Trend | 310 | -0.0 (-0.0 to -0.0) | 0 | 0 | 1 | 1 |
| 5 | spec_R2 | S2 SC-Rate | 310 | 2.4 (-0.7 to 5.5) | 8 | 15 | 0.21 | 1 |
| 5 | spec_R2 | S3 SC-PoPLR | 310 | -2.3 (-4.8 to 0.3) | 13 | 6 | 0.167 | 1 |
| 5 | spec_R2 | S4 SC-Event | 310 | 2.6 (-0.3 to 6.0) | 7 | 15 | 0.134 | 1 |
| 5 | spec_R2 | S5 SC-LightGBM | 310 | 0.3 (-2.4 to 3.2) | 10 | 10 | 1 | 1 |
| 5 | spec_R2 | S6 Order-LightGBM | 310 | -1.8 (-4.2 to 0.4) | 11 | 6 | 0.332 | 1 |
| 5 | spec_R2 | S7 SC-GRU | 310 | 1.8 (-1.4 to 4.9) | 7 | 14 | 0.189 | 1 |
| 5 | spec_R2 | B8 LightGBM-95spec | 310 | -8.4 (-12.2 to -4.8) | 32 | 8 | 0.000182 |  |
| 6 | sens | D7 Event | 150 | -11.3 (-18.5 to -4.1) | 8 | 25 | 0.00455 | 0.0228 |
| 6 | sens | S1 SC-Trend | 150 | -0.7 (-1.8 to 0.0) | 0 | 1 | 1 | 1 |
| 6 | sens | S2 SC-Rate | 150 | -23.3 (-31.4 to -15.8) | 4 | 39 | 3.11e-08 | 1.86e-07 |
| 6 | sens | S3 SC-PoPLR | 150 | -9.6 (-17.9 to -1.8) | 9 | 23 | 0.0201 | 0.0802 |
| 6 | sens | S4 SC-Event | 150 | -35.1 (-43.4 to -27.3) | 2 | 54 | 4.43e-14 | 3.55e-13 |
| 6 | sens | S5 SC-LightGBM | 150 | 2.2 (-2.9 to 7.1) | 10 | 7 | 0.629 | 1 |
| 6 | sens | S6 Order-LightGBM | 150 | -3.1 (-9.2 to 2.7) | 10 | 14 | 0.541 | 1 |
| 6 | sens | S7 SC-GRU | 150 | -36.7 (-45.7 to -27.5) | 7 | 62 | 4.1e-12 | 2.87e-11 |
| 6 | sens | B8 LightGBM-95spec | 150 | 22.0 (15.3 to 28.5) | 35 | 1 | 1.08e-09 |  |
| 6 | spec_R1 | D7 Event | 164 | -10.4 (-16.2 to -5.1) | 17 | 0 | 1.53e-05 | 0.000122 |
| 6 | spec_R1 | S1 SC-Trend | 164 | -0.0 (-0.0 to -0.0) | 0 | 0 | 1 | 1 |
| 6 | spec_R1 | S2 SC-Rate | 164 | -2.4 (-6.0 to 0.6) | 5 | 1 | 0.219 | 1 |
| 6 | spec_R1 | S3 SC-PoPLR | 164 | -2.0 (-4.4 to -0.2) | 3 | 0 | 0.25 | 1 |
| 6 | spec_R1 | S4 SC-Event | 164 | -0.4 (-1.9 to 0.6) | 1 | 0 | 1 | 1 |
| 6 | spec_R1 | S5 SC-LightGBM | 164 | -0.4 (-1.3 to -0.0) | 1 | 0 | 1 | 1 |
| 6 | spec_R1 | S6 Order-LightGBM | 164 | -2.4 (-4.4 to -0.8) | 2 | 0 | 0.5 | 1 |
| 6 | spec_R1 | S7 SC-GRU | 164 | -3.7 (-7.1 to -0.6) | 6 | 1 | 0.125 | 0.875 |
| 6 | spec_R1 | B8 LightGBM-95spec | 164 | -10.6 (-15.1 to -6.4) | 17 | 0 | 1.53e-05 |  |
| 6 | spec_R2 | D7 Event | 310 | -3.9 (-7.7 to -0.0) | 24 | 12 | 0.0652 | 0.391 |
| 6 | spec_R2 | S1 SC-Trend | 310 | 0.2 (-0.0 to 0.7) | 0 | 1 | 1 | 1 |
| 6 | spec_R2 | S2 SC-Rate | 310 | 2.9 (-0.0 to 6.0) | 7 | 16 | 0.0931 | 0.466 |
| 6 | spec_R2 | S3 SC-PoPLR | 310 | -4.2 (-6.9 to -1.5) | 17 | 4 | 0.0072 | 0.0504 |
| 6 | spec_R2 | S4 SC-Event | 310 | 4.3 (1.9 to 7.1) | 2 | 15 | 0.00235 | 0.0188 |
| 6 | spec_R2 | S5 SC-LightGBM | 310 | -0.3 (-2.7 to 2.2) | 8 | 7 | 1 | 1 |
| 6 | spec_R2 | S6 Order-LightGBM | 310 | -3.7 (-6.0 to -1.2) | 12 | 5 | 0.143 | 0.574 |
| 6 | spec_R2 | S7 SC-GRU | 310 | 1.5 (-1.5 to 4.8) | 8 | 14 | 0.286 | 0.859 |
| 6 | spec_R2 | B8 LightGBM-95spec | 310 | -15.8 (-20.0 to -11.7) | 50 | 1 | 4.62e-14 |  |

Table S5. Study 1: false alarms over repeated reviews on true no-change series (approximate; analysis added after internal review).

| Detector | Flagged at least once, k = 3–6, % | Mean per-review false-alarm rate, % |
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

Table S6. Study 2, external clinic (GRAPE): agreement with the mean-deviation, PLR2 and PLR3 labels.

| Detector | k | Sens MD % | Spec MD % | Sens PLR2 % | Spec PLR2 % | Sens PLR3 % | Spec PLR3 % |
|---|---|---|---|---|---|---|---|
| B8 LightGBM-95spec | 3 | 36.5 | 74.1 | 25.8 | 72.8 | 38.1 | 73.6 |
| D1 OLS-MD | 3 | 44.4 | 95.3 | 17.5 | 92.8 | 21.4 | 92.0 |
| S1 SC-Trend (UW threshold) | 3 | 46.4 | 95.3 | 18.8 | 92.8 | 25.2 | 92.0 |
| S1 SC-Trend (local threshold) | 3 | 44.4 | 95.2 | 17.5 | 92.7 | 21.4 | 91.9 |
| S5 SC-LightGBM (UW threshold) | 3 | 24.0 | 83.5 | 15.7 | 82.5 | 23.8 | 83.1 |
| S5 SC-LightGBM (local threshold) | 3 | 7.4 | 93.2 | 6.5 | 93.1 | 11.0 | 93.4 |
| S6 Order-LightGBM (UW threshold) | 3 | 13.1 | 96.7 | 9.0 | 96.6 | 15.2 | 96.3 |
| S6 Order-LightGBM (local threshold) | 3 | 18.5 | 95.0 | 13.5 | 94.9 | 19.0 | 94.4 |
| B8 LightGBM-95spec | 4 | 70.4 | 60.0 | 58.9 | 60.3 | 66.7 | 58.5 |
| D1 OLS-MD | 4 | 33.3 | 95.9 | 16.1 | 94.7 | 16.7 | 93.4 |
| S1 SC-Trend (UW threshold) | 4 | 33.3 | 94.9 | 18.5 | 94.2 | 21.7 | 92.8 |
| S1 SC-Trend (local threshold) | 4 | 33.3 | 94.6 | 18.7 | 93.9 | 23.3 | 92.7 |
| S5 SC-LightGBM (UW threshold) | 4 | 36.3 | 82.7 | 34.4 | 84.1 | 37.8 | 82.1 |
| S5 SC-LightGBM (local threshold) | 4 | 16.7 | 92.2 | 15.1 | 92.7 | 10.0 | 91.3 |
| S6 Order-LightGBM (UW threshold) | 4 | 22.2 | 94.0 | 15.5 | 94.0 | 20.0 | 93.2 |
| S6 Order-LightGBM (local threshold) | 4 | 23.0 | 93.1 | 16.3 | 93.1 | 20.0 | 92.2 |

Table S7. Study 2: time of first flag among R1 progressors flagged by the sixth test (detectors applied at every review). Groups differ between detectors, so medians are descriptive only.

| Detector (every review) | Progressors flagged by test 6, n / N | Median review of first flag (test number) | Median years from first test to first flag |
|---|---|---|---|
| D1-repeated | 97 / 150 | 4 | 4.5 |
| D7-repeated | 69 / 150 | 5 | 5.4 |
| Q1 Sequential trend | 62 / 150 | 5 | 5.8 |
| Q2 Confirmed trend | 72 / 150 | 5 | 5.6 |
| Q3 Confirmed SC-Event | 19 / 150 | 5 | 6.7 |
| Q4 Sequential Order-LightGBM | 55 / 150 | 5 | 6.5 |

## S5. Supplementary figures