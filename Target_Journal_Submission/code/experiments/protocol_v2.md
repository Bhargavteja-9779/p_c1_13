# Protocol v2 (Study 2) — written 2026-11-23, BEFORE any Study 2 code was run on outcome data

Context. Study 1 (protocol.md) found that no valid detector beat the OLS mean-sensitivity trend test (D1), but it had
only 26 progressing / 26 stable reference eyes (smallest significant gain 34.6 pp), the ML detectors were thresholded
on labelled stable eyes (and were not valid on true no-change data), and validity was judged per look only.
Study 2 asks the question that Study 1 could not answer: **when every detector is held to the same false-alarm rate,
does any detector find more progression than D1, and how should repeated looks be controlled?**
Study 1 results are known to the authors; Study 2 is therefore a new, separately specified analysis. Everything below is
fixed before running. All results will be reported, whatever they show.

## Data and design
- UWHVF, all patients. 5-fold patient-level cross-fitting: fold = salted SHA-256 of patient id ("uwhvf-cv-v2") mod 5.
  For each fold f: detectors are fitted / calibrated on the other 4 folds (for ML: inner split of those patients,
  75% fit / 25% model selection, by hash "uwhvf-inner-v2"), and evaluated on fold f. Every eye is evaluated exactly once,
  out of fold. Study 1's locked test split is reported as a subset analysis for consistency.
- Artes retest (true no-change): every fold's fitted detector is applied to all Artes windows (k = 3..6, donor dates
  from the held-out fold's eyes with >= k tests, 10 draws per window, as amendment A1). False-alarm rate = mean over folds.
- GRAPE (external): see H9.
- k = 3, 4, 5, 6 tests; blind spots removed; sensitivities in dB.

## Reference standards (UWHVF eyes with >= 8 tests)
- R1 (primary, as Study 1): full-series slope of mean total deviation < -0.3 dB/yr and one-sided p < 0.01 -> progressor;
  one-sided p > 0.5 -> stable.
- R2 (flat stable): progressors as R1; stable = full-series slope between -0.3 and +0.3 dB/yr and one-sided p > 0.1
  (removes the "improving eyes only" spectrum problem of R1).
- R3 (future-only, removes incorporation bias): uses only tests k+1..n, requires n - k >= 5; same rule as R1.

## Shuffle calibration (the method under test)
For a detector score s(t, Y) (larger = more progression), its threshold at k tests is the (1 - 0.05) quantile of s over
shuffled first-k series of the calibration eyes: each calibration eye with >= k tests contributes 20 random
permutations of its first k fields, excluding the identity order, keeping its own test dates. This targets a 5%
false-alarm rate per look under "no change in order". Discrete scores: the most liberal threshold with calibrated rate
<= 5% (ties broken by randomisation with a fixed seed is NOT used; conservative rounding instead).

## Detectors (all fitted on calibration folds only)
Per-look detectors (target 5% per look):
- D1 OLS-MD t-test p < 0.05 (reference comparator; not shuffle-calibrated).
- D7 Event analysis (Study 1 definition, 5th percentile limits, 3 points on 2 consecutive follow-ups).
- S1 SC-Trend: score = -t statistic of mean-sensitivity slope, shuffle-calibrated (= D5 without strata).
- S2 SC-Rate: score = -(mean-sensitivity slope in dB/yr), shuffle-calibrated.
- S3 SC-PoPLR: score = PoPLR combined statistic, shuffle-calibrated (pooled, so it can flag at k = 3).
- S4 SC-Event: event analysis with change-limit percentile q in {1, 2.5, 5, 10, 15, 20}% and required points m in
  {2, 3, 4} on 2 consecutive follow-ups (k >= 4); choose the (q, m) with the largest shuffle-calibrated rate <= 5%
  (ties: larger q). For k = 3: single follow-up version (m points beyond q on test 3).
- S5 SC-LightGBM: Study 1 D8 model (labels R1, 12-config grid, inner model selection by AUC) with the threshold from
  shuffle calibration instead of 95% specificity on stable eyes.
- S6 Order-LightGBM (self-supervised, no labels): LightGBM trained to separate real-order first-k series from shuffled
  versions of the same series, using all calibration eyes with >= k tests (features: Study 1 tab_features; 1 real + 3
  shuffles per eye; fixed config n_estimators=400, learning_rate=0.05, num_leaves=15). Score = predicted P(real order);
  threshold by shuffle calibration on the inner model-selection eyes (not used for fitting).
- S7 SC-GRU: Study 1 D9 model with shuffle-calibrated threshold (seeds as below).
- B8 LightGBM-95spec: Study 1 D8 as is (threshold = 95% specificity on stable eyes), kept as the "usual practice" arm.

Repeated-look detectors (target 5% CUMULATIVE false alarms over looks k = 3, 4, 5, 6 on the same eye):
- Q1 Sequential trend: S1 score with one common per-look level a chosen so that, on shuffled calibration series
  (one random permutation of the first 6 tests per eye with >= 6 tests, 20 per eye; looks = prefixes of length 3..6),
  the share flagged at least once is <= 5%.
- Q2 Confirmed trend: flag at look k only if the S1 score exceeds its per-look threshold at looks k-1 and k (k >= 4);
  common level a chosen as in Q1.
- Q3 Confirmed SC-Event: S4 family re-calibrated for 5% cumulative (choose (q, m) as in S4 but on cumulative rate).
- Q4 Sequential Order-LightGBM: S6 score, common quantile level chosen as in Q1.
- D1-repeated: D1 applied at every look (uncontrolled; comparator).

Seeds: stochastic detectors (S5, S6, S7, B8, shuffle draws) use seeds 0, 1, 2; results averaged; SD reported.

## Hypotheses (each with its test; alpha 0.05)
H6 (validity of shuffle calibration): every shuffle-calibrated per-look detector has a true no-change (Artes)
    false-alarm rate with 95% CI lower limit <= 5% and upper limit <= 10% at every k; B8 does not (replication of Study 1).
H7 (matched false alarms): at least one shuffle-calibrated detector has higher sensitivity (R1) than D1 by >= 10 pp at
    some k with Holm-adjusted exact McNemar p < 0.05 (Holm over the 7 S/D7 detectors within k). Falsified otherwise.
    Specificity (R1, R2) reported with McNemar vs D1.
H8 (repeated looks): with cumulative false alarms on Artes <= ~5%, the best Q detector detects (by the 6th test) at
    least as many R1 progressors as D1-repeated, whose cumulative false alarms are ~15% (non-inferiority margin 10 pp,
    one-sided 95% bootstrap CI of the difference > -10 pp).
H9 (local recalibration in a new clinic): in GRAPE, S5 (UWHVF-trained LightGBM) re-thresholded by shuffle calibration on
    GRAPE's own series (5-fold patient-level cross-fitting) has specificity >= 90% against the MD label at k = 3, whereas
    the UWHVF threshold does not (Study 1: 61%). S1 and S6 are also cross-fitted on GRAPE.

## Statistics
Patient-cluster bootstrap (2,000) for all proportions; exact McNemar on majority-vote flags over seeds; Holm within k.
Cumulative measures: eye-level "flagged at any look 3..6" for progressors with >= 8 tests (R1) and for Artes series
(window start = first test; donor dates drawn once per series and draw index, and reused across looks — an improvement
over Study 1's approximation). Real-world units: false flags per 1,000 stable eyes; months of follow-up gained at the
first flag among detected progressors (median time of first flag, from test dates).
Secondary: R2, R3 results; locked-test-split subset; GRAPE PLR2/PLR3 labels.

## What would change our conclusions
If H7 is supported, the paper's message becomes "under matched false alarms, detector X finds more progression";
if not, "with ~150 progressors, no detector beats D1 by >= 10 pp at matched false alarms". Both will be reported.
