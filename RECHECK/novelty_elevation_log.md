# Novelty elevation log (Prompt-2 run). Every idea tried is listed, including failures.
Count of ideas tried in this run is kept at the bottom for multiple-comparison reporting.
Development data: UWHVF TRAIN (fit) and VALIDATION (select) splits only; null proxy for development = shuffled VALIDATION
series (Artes true-null and UWHVF TEST are NOT used for selection). Final candidates are evaluated once on TEST + Artes + GRAPE.

## Starting point (re-scored honestly, see stage4_scorecard.md): 17/30
Weakest point: item 1 "distance from prior work" — evaluating progression methods on test-retest/no-change data is an
established idea (Artes et al. 2014 used the same retest data to estimate GPA specificity), so a benchmark with a
true-null arm is not by itself new. Item 4 (evidence) also weak: 26 progressors / 26 stable reference eyes.

## Round 1 (2026-11-23) — weakest point: distance from prior work + "why does it work/fail?"
Observation from run-1 results (TEST, already computed): LightGBM (D8) has 95% spec on reference-stable eyes but a 27.7%
false-alarm rate on true no-change series at k=3. Run 1 gave no explanation.

### Six candidate ideas from different families
1. (analysis / new insight) MECHANISM: the usual "reference-stable" definition (full-series one-sided slope p > 0.5) selects
   eyes whose long-run slope is POSITIVE (improving: learning effect / regression to mean). Thresholds set at 95%
   specificity on such eyes are calibrated against improving eyes, not against no-change eyes -> inflated true-null FPR.
   Reusable finding for every supervised VF-progression paper that uses this kind of stable reference.
2. (new inference idea / calibrated decision) NULL-CALIBRATED ML: keep the ML score, but choose its threshold from
   shuffled training series (conformal p-value, Mondrian strata by mean sensitivity) instead of from reference-stable eyes.
   Gives finite-sample FPR control under within-eye exchangeability for ANY learned score.
3. (new learning signal / representation) CHANGE-ONLY FEATURES: remove order-invariant features (level, variability,
   range) from the ML model, so that it can only use change; tests whether level confounding drives false alarms.
4. (new evaluation protocol) FUTURE-ONLY REFERENCE: define progression from tests AFTER the first k only, removing the
   shared-noise circularity between detector input and reference (run-1 reference used the full series incl. the first k).
5. (theory) A short formal result: (a) within-eye permutation cannot reject below 1/k!; (b) a shuffle-calibrated conformal
   threshold has FPR <= alpha for any score under exchangeability within eye and of eyes within stratum; (c) thresholds set
   on a reference-stable set selected by a positive full-series slope give no such guarantee.
6. (cost-sensitive / decision) CLINICAL UNITS: false escalations per 1,000 stable eyes and progressing eyes detected per
   extra false alarm (number-needed-to-false-alarm) at 3-6 tests.
7. (borrowed from another field) surrogate-data testing (physics/neuroscience: shuffled surrogates to test for structure)
   and negative-control outcomes (epidemiology) -> shuffle audit framed as a "surrogate-null audit" anyone can run without
   retest data.
Literature check: idea 2 (conformal/permutation calibration of an ML score) exists in statistics (classification permutation
test, conformal novelty detection) but no VF-progression paper found (prior-art agent: see close_calls.md); idea 1 not
found in VF literature (to confirm by Stage-3 search); idea 4 is a known concern (circular reference) but rarely fixed.

### Pre-stated hypotheses (written BEFORE running; falsifiers in brackets)
H1 (mechanism): reference-stable eyes have positive mean full-series slope and their first-k-test D8 scores are lower than
    those of shuffled validation series. [Wrong if the stable eyes' slope distribution is centred on 0, or if D8 scores of
    shuffled series are not higher than those of reference-stable eyes.]
H2 (null-calibrated ML): thresholding the D8 score with shuffled-train calibration brings the shuffled-validation FPR to
    <= 5% (CI) AND keeps validation sensitivity >= OLS-MD + 10 pp at k = 3 or 4. [Wrong if FPR > 5% or gain < 10 pp.]
H3 (change-only features): removing level/variability features cuts shuffled-validation FPR of D8 (standard threshold)
    by >= half. [Wrong if FPR falls by < half.]
Script: code/experiments/recheck_elev_r1.py -> results/recheck_elev_r1.json
