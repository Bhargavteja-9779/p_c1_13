# Pre-registered protocol — written 2026-11-23, BEFORE any final-test result
(Development history, including every failed idea, is in journal_selection/novelty_escalation_log.md.)

## Title (working)
How early can glaucomatous visual-field progression be detected without false alarms? An open benchmark of
classical, permutation and machine-learning detectors with a true no-change arm, in two clinics.

## Hypotheses / research questions (each maps to one analysis)
RQ1 (validity): Which detectors keep the false-alarm rate on TRUE no-change series (Artes 12-week retest) at or
     below the nominal 5% at 3, 4, 5 and 6 tests?
RQ2 (power): At each number of tests k, does any detector flag more future-confirmed progressors than the simple
     OLS mean-sensitivity trend test (OLS-MD) while keeping a valid true-no-change false-alarm rate?
     H2: no detector beats OLS-MD by >= 10 percentage points sensitivity with valid FPR (falsified if one does,
     with Holm-adjusted McNemar p < 0.05).
RQ3 (audit): Does the "shuffle audit" (re-run the detector on each eye's randomly re-ordered tests) estimate the
     true-no-change false-alarm rate? H3: absolute difference <= 3 percentage points for most detector x k cells and
     Spearman rho >= 0.7 across cells.
RQ4 (common ML practice): Do supervised ML detectors, thresholded at 95% specificity against reference-stable eyes
     (the usual practice), have true-no-change false-alarm rates above 5%? H4: yes.
RQ5 (external): Do RQ1-RQ2 conclusions hold in an independent clinic (GRAPE, China) with clinician-applied criteria?

## Data
- UWHVF (Montesano et al. 2022; BSD-3): 24-2 fields; locked patient-level split by salted SHA-256 of patient id
  (60% train / 20% val / 20% test; salt "uwhvf-split-v1"). Test split never used before final run.
- Artes 2014 retest (visualFields R package 1.0.7, vfpwgRetest24d2): 30 patients x 12 weekly tests. Used during
  development for one FPR check (round 5); disclosed. Final evaluation: all consecutive windows of k tests.
- GRAPE (Huang et al. 2023 Sci Data; CC0): 263 eyes, labels "Progression Status" PLR2, PLR3, MD (primary: MD label;
  secondary: PLR2, PLR3, any). Points coded -1 excluded. Never used before the final run.
Blind-spot points (24-2 indices 25, 34) excluded. Sensitivities (dB) are the input for all detectors.

## Reference standard (UWHVF)
Eyes with >= 8 tests. Progressor: full-series slope of mean total deviation < -0.3 dB/yr with one-sided p < 0.01.
Stable: full-series one-sided p > 0.5. Others excluded. Secondary reference: full-series PoPLR p < 0.01 (2,000 random
permutations) vs PoPLR p > 0.5 (reduces circularity with MD-based detectors).

## Detectors (fixed now; tuned only on train/val)
D1 OLS-MD: one-sided t-test of the slope of mean sensitivity, p < 0.05.
D2 MD-rate: MD slope <= -1.0 dB/yr (fast-progression rule, no p-value).
D3 PLR-3: >= 3 locations with slope <= -1 dB/yr and one-sided p < 0.01.
D4 PoPLR within-eye permutation (O'Leary 2012), p < 0.05 (exact enumeration k <= 7).
D5 Pooled-shuffle conformal OLS-MD: calibration pool = 20 shuffles of each TRAIN eye's first k tests, strata = mean
   sensitivity tertile (<20, 20-26, >=26 dB); p < 0.05. (GRAPE: leave-one-patient-out pool from GRAPE itself.)
D6 Pooled-detrended conformal region-max (development variant that looked more sensitive): 4 regions
   (superior/inferior x central/peripheral), detrended residual shuffles; p < 0.05.
D7 Event analysis (GPA-like): point deteriorated if the decrease from the mean of tests 1-2 is below the 5th
   percentile of short-interval (<= 0.5 yr) test-pair differences in TRAIN eyes, binned by baseline sensitivity
   (2-dB bins); flag if >= 3 deteriorated points on 2 consecutive follow-ups (needs k >= 4).
D8 ML-tabular: LightGBM on grid-agnostic features of the first k tests (MD level/slope/z, PLR counts, PoPLR S, worst
   region slope, range, SD); trained on TRAIN reference labels; threshold = 95% specificity on VAL reference-stable eyes.
   5 seeds; tuning budget: same 12-configuration grid for D8 and D9.
D9 ML-sequence: GRU over the k x 52 fields + time gaps; same labels/threshold/seeds/budget as D8 (24-2 only).
D10 Self-supervised order network + within-eye permutation (round-0 idea), p < 0.05; 5 seeds.

## Evaluation sets and metrics (k = 3, 4, 5, 6 tests)
E1 UW-test future reference: sensitivity, specificity (95% CI: patient bootstrap, 2,000 resamples).
E2 Artes true no-change: false-alarm rate over windows (95% CI: patient-cluster bootstrap).
E3 Shuffle audit on UW-test (first k tests re-ordered, 10 seeds): false-alarm rate.
E4 GRAPE: sensitivity/specificity vs clinician labels, first k tests (k = 3, 4).
Real-world measures: expected false progression flags per 1,000 stable eyes per detection opportunity; number of
tests to first detection among reference progressors (eyes followed to 8 tests).

## Statistics
Paired comparisons with D1 (sensitivity, specificity): exact McNemar, Holm correction across detectors within each k
and endpoint. Effect: difference in proportions with paired bootstrap 95% CI. Validity: FPR CI upper bound vs 5%.
RQ3: per-cell absolute difference E3-E2 and Spearman rho across cells (bootstrap CI). Unit of analysis = eye for
E1/E4 with patient-cluster bootstrap; window clusters within patient for E2. All seeds reported (mean +- SD).
No result-dependent change of thresholds, references or detectors after this date; any deviation will be reported.

## Amendment A1 (2026-11-23, before any final result)
Artes tests are one week apart. Rate-based rules (D2, D3, D7, D8, D9) are not invariant to the time scale, so each
Artes window of k tests is assigned the test times of a randomly drawn UW-test eye with >= k tests (10 draws per
window). Under true no change the time labels carry no signal, so this keeps the arm a valid null at clinical spacing.

## Amendment A2 (2026-11-23, before any final result)
GRAPE was measured with a different perimeter (59 analysable points after removing points coded -1; dB scale differs
from Humphrey). Therefore on GRAPE: D5 calibration pool and D7 change limits come from GRAPE itself by 5-fold
patient-level cross-fitting ("own-clinic calibration"); D8 is the UWHVF-trained model applied unchanged (transfer
test, grid-agnostic features); D6, D9, D10 (24-2 specific) are not evaluated on GRAPE.

## Amendment B (2026-11-23, written and committed BEFORE any of the analyses below were run)
Motivation: round-1 results showed that detectors thresholded on reference-stable eyes (D6, D8, D9) have excess false
alarms on true no-change data, and that comparisons at unequal false-alarm rates are uninformative. Amendment B tests a
remedy and a fair comparison. All analyses below are NEW and labelled as such in the paper.

B1 No-change calibration (NCC). For each continuous-score detector — D1 (trend z statistic), D2 (minus MD slope),
   D6 (raw worst-region trend statistic, no pooled p-value), D8 (LightGBM probability), D9 (GRU output) — replace the
   original threshold by the 95th percentile of the detector's score on no-change series, from two label-free sources:
   (a) SHUFFLE calibration (SC): scores on the clinic's own TRAIN eyes with their first k tests randomly re-ordered
       (5 shuffles per eye); needs no retest data and no labels;
   (b) RETEST calibration (RC): scores on Artes windows (same 10 donor time-label draws per window as E2), with 5-fold
       patient-level cross-fitting so that every Artes window is evaluated with a threshold from other patients.
   Seeds: D6, D8, D9 seeds 0-4 (models re-fitted with the same code/seeds as the main run); D1, D2 deterministic.
B2 Outcomes (k = 3..6): true no-change false-alarm rate (Artes; for RC the cross-fitted rate), sensitivity and
   specificity on UW-test reference eyes (E1); RC threshold for E1 = 95th percentile over ALL Artes windows.
Hypotheses (pre-stated):
   HB1: after RC, every detector's Artes false-alarm 95% CI includes 5% (no excess false alarms) at every k.
   HB2: after SC, false-alarm rates are within 3 percentage points of 5% for most detector x k cells (>= 75%).
   HB3 (matched-false-alarm comparison, the main new test): at RC thresholds, no detector flags >= 10 percentage points
        more reference progressors than RC-calibrated D1 with Holm-adjusted exact McNemar p < 0.05 (Holm within k over
        D2, D6, D8, D9). Falsified if one does.
B3 All eligible eyes (precision for untrained detectors): D1, D2, D3, D4 need no training, so their sensitivity and
   specificity are also computed on ALL UWHVF eyes with >= 8 tests (train + val + test), same reference; paired
   comparisons vs D1 as in the main analysis. Exploratory.
B4 Time-label sensitivity analysis (A1): Artes false-alarm rates for D1, D2, D3, D7 recomputed with (i) the real weekly
   Artes dates rescaled to annual spacing (test i at year i-1) and (ii) donors restricted to reference-stable eyes.
   Exploratory.
Statistics as in the main analysis (patient-cluster bootstrap 2,000; seed-averaged flags; McNemar on majority flags).
No threshold, reference, detector or seed will be changed after seeing B results.
