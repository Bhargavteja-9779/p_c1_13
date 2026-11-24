# Adversarial review, round 2: Amendment B (no-change calibration)

Reviewer role: adversarial peer reviewer. Scope: Amendment B text (Abstract, Key Summary Points, Methods/Results subsections, Discussion paragraph "The calibration extension", Conclusions), Table 5, Supplementary Table S6, Fig. 5, `code/experiments/amendment_b.py`, `code/src/statistics/amendment_b_stats.py`, `results/amendB/amendB.json`, and the protocol's Amendment B section.

## 1. Number check (manuscript vs amendB.json)

The check was done with a script for Table 5 (20 rows x 6 numeric cells) and Table S6 (15 rows), and by hand for the prose.

**Result: no numeric mismatches.** Every value in Table 5 and Table S6 matches amendB.json after rounding. The prose values checked were:

| Claim | JSON | OK |
|---|---|---|
| HB1: 20/20 RC cells with no excess false alarms | HB1_RC_cells_no_excess = 20/20 | yes |
| HB2: 70% of SC cells within 3 pp | HB2_SC_share_within_3pp = 0.70 | yes |
| SC D2 false alarms 0.4–1.0% | 0.0040–0.0105 | yes |
| D6/D8/D9 RC differences −19.2 to +19.2 pp; smallest Holm p = 0.38 | min −0.192 (D6 k5, D9 k4), max +0.192 (D8 k6); p_holm 0.375 | yes |
| D8 k3 RC: false alarms 5.2% (3.5–7.1), sensitivity 14.6% vs D1 19.2% | 0.0517 (0.0351–0.0715), 0.146, 0.192 | yes |
| D2 RC k5: 73.1%, +30.8 (14.8 to 50.0), p = 0.031, false alarms 5.5% | 0.731, 0.308 (0.148–0.500), 0.031, 0.055 | yes |
| D2 RC k6: 84.6%, +30.8 (15.4 to 48.0), p = 0.031, false alarms 5.2% | 0.846, 0.308 (0.154–0.480), 0.031, 0.0519 | yes |
| PoPLR reference: 46.6% vs 27.6% (k5) | 0.466 / 0.276 | yes |
| RC slope threshold 0.30 dB/yr (k5) | 0.298 | yes |
| SC/RC threshold ratio for D2 "about 3.0 at every k" | 2.97–3.02 | yes |
| SC D2 vs D1: −30.8 to −15.4 pp | −0.308 to −0.154 | yes |
| Other detectors' ratios 0.90–1.27 | 0.896–1.275 | yes |
| D1 time-label false alarms 3.3–5.8% | B4 range 0.033–0.058; main-run clinic dates 3.8–5.1% | yes |
| D3 annual k3: 18.3% | 0.183 | yes |
| B3: 314 eyes / 150 / 164 / 236 patients | B3_counts | yes |
| B3 D2 k3: +8.7 (0.7 to 16.4), p = 0.047; specificity 85.4 vs 96.3 | matches | yes |
| HB3 falsified | HB3_falsified = true | yes (reported honestly) |

The numbers are right, but some of the words describing them are wrong or too strong (see Section 3).

## 2. Code audit

| # | Item | Finding | Severity |
|---|---|---|---|
| C1 | Cross-fitted RC false-alarm rate | Correct. Folds are a SHA-256 hash of the Artes patient id, thresholds are recomputed per seed from the other four folds, and flags are seed-averaged. Clustering is by Artes patient. | OK |
| C2 | RC threshold for E1 | Uses the 95th percentile over all Artes windows (`thr_all`), as in the protocol. There is no label leakage, because Artes has no UWHVF labels. | OK |
| C3 | Leakage between calibration and evaluation | There is no label leakage. However, the E2 donor time labels come from the UWHVF test eyes, which are also the E1 evaluation eyes. The RC threshold for D2 (dB/yr) therefore depends directly on the test cohort's test intervals. This is label-free, so it is allowed, but it is not disclosed. | MINOR (disclose) |
| C4 | Donor time-label reuse | `default_rng(1000+seed)` reproduces the main-run E2 draws and consumes the E3 draws. This matches `run_all.py` lines 64–82. Each Artes window is reused with 10 donor draws, and the bootstrap clusters by Artes patient, so the CIs are not falsely narrow. | OK |
| C5 | SC uses training eyes only | Yes (`for s in train`). Two caveats: (a) the training eyes include progressors, so shuffling spreads true progression into the null and the raw-slope thresholds are biased upward (this is acknowledged in the Discussion); (b) D6, D8 and D9 were fitted on the same training eyes, so SC scores for D8/D9 are in-sample model outputs on permuted training sequences. This likely explains the erratic SC false-alarm rates for D8/D9 (1.6–7.0%). Fix: run SC on the validation eyes, or cross-fit SC, and disclose. | MODERATE |
| C6 | McNemar/Holm family | Holm is applied within each k and endpoint over D2/D6/D8/D9, as the protocol says. However, the HB3 falsification rests on k = 5 and k = 6, which reuse the same 26 eyes, and the family excludes the other k values and calibrations. Holm over all 16 RC sensitivity tests gives the smallest adjusted p = 16 × 0.0078 = 0.125, so HB3 would not be falsified. The protocol's choice stands, but the dependence of the conclusion on the family definition should be stated. | MODERATE |
| C7 | Seed-mean difference vs majority-flag McNemar | This is as specified. Note that the D8 k6 bootstrap CI excludes 0 (+19.2, 0.8 to 37.1) while the McNemar test is non-significant (p_holm 0.54). The same applies to D8 k5 in the other direction (−8.5, −17.8 to −0.8). Text built only on Holm p hides this. | MODERATE (see claim a) |
| C8 | B3 family | D4 at k3 is silently dropped from the Holm family. It cannot flag with exact enumeration at k = 3, which matches the main rule "detectors that can flag", but the drop should be noted under S6. | MINOR |
| C9 | `no_excess` rule | `lo <= .05 <= hi or hi < .05` is consistent with the main "excess" rule. Because RC is fitted on the same 30 patients (cross-fitting only holds out patients), HB1 is close to guaranteed by construction. It shows the code works; it is weak evidence about the detectors. Say so. | MODERATE |
| C10 | Labelling | D2 is still labelled "MD-rate <= -1 dB/yr" in the JSON, tables and code after recalibration. In Table 5 the RC rule is actually about −0.22 to −0.72 dB/yr. Rename it (e.g. "D2c, calibrated MD slope"). | MINOR |

No coding error was found that changes the reported numbers.

## 3. Are the claims supported?

### (a) "Conformal/ML detectors show no significant gain at matched false-alarm rates"

The claim is literally true: the smallest Holm p is 0.38. It is overstated in two places.

- **MAJOR (overclaim).** The Conclusions say the gains "were explained by their false alarms". With 26 progressors the minimum detectable difference is about 35 pp, so "not significant" is not "explained". For D8 at k6, retest-calibrated D8 is +19.2 pp (bootstrap 95% CI 0.8 to 37.1), and the CI excludes zero. The Discussion admits this ("cannot be excluded"), but the Abstract and Conclusions do not.
  - Fix: replace "were explained by" with "were largely explained by, … although a moderate gain for D8 with six tests could not be excluded (+19.2 pp, 95% CI 0.8 to 37.1)".
  - Fix: add the D8 k6 CI to the Abstract.
- **MODERATE.** "Matched false-alarm rate" means matched on Artes (weekly noise with clinic dates), not on clinic data. On reference-stable eyes the matched detectors still differ (D2-RC specificity 92–96% vs D1 96–100%). State that the matching is on retest noise only.

### (b) The calibrated rate score's gain depends on calibration source and is likely optimistic

- The dependence on calibration source is shown directly: the threshold ratio is about 3.0, and the sensitivity gap reverses sign. This part is supported.
- That the gain is "likely optimistic because weekly retest noise < yearly clinic noise" is plausible but not tested. The data cannot test it as analysed, because the stable reference eyes all have non-negative slopes and the 80 indeterminate eyes (where a −0.3 dB/yr rule would fire) are excluded. **MAJOR.**
  - Fix: apply the RC-calibrated D2 and D1 thresholds (label-free, so this is legitimate) to (i) the 80 indeterminate test eyes and report the flag rates, and (ii) all 314 labelled eyes in B3 (150/164 eyes, about 6× the power). Report the D2-RC specificity there.
  - Fix: estimate long-term residual SD in reference-stable eyes vs Artes, to show the noise gap directly rather than asserting it.

### (c) "The trend test is robust to calibration source"

D1 is robust: threshold ratio 0.98–1.17, and false alarms of 3.3–5.8% across all time-label variants. **The comparative claims are not supported. MAJOR (statement contradicted by the paper's own table).**

- Key Summary Points say "the trend test's threshold and false-alarm rate changed least". Table 5 shows that D8's threshold changed less (ratio 0.99–1.02) and D6's changed about as little (0.90–1.04).
- The false-alarm change between SC and RC was 0.1–1.6 pp for D1 and 0.1–1.7 pp for D6. The mean absolute change is similar (0.97 vs 0.86 pp), so D6 changed no more than D1.
- The Discussion's sentence that D6's "false-alarm rates varied more" is therefore not true for D6. It is true for D8 and D9.
- The Conclusions say "most stable across all sources of no-change data we tried". D6, D8 and D9 were never run in the B4 time-label check, so the claim is untested for them.
- Fix: rephrase as "D1's threshold and false-alarm rate changed little across sources; unlike the raw slope (D2), it does not depend on the noise level". Drop "least" and "most stable", or run D6/D8/D9 through B4 and compare formally.

### (d) Circularity: RC slope threshold (~0.3 dB/yr) vs reference definition (−0.3 dB/yr)

**MAJOR, not adequately disclosed.** The reference progressor is a whole-series MTD slope below −0.3 dB/yr with p < 0.01. The reference-stable eye has one-sided p > 0.5, i.e. a non-negative slope (median +0.07). Eyes in between are excluded. D2-RC at k5/k6 flags a slope of the first 5–6 tests below −0.30 or −0.22 dB/yr.

- Reference eyes have a median of 11 tests, so the first 6 tests are about half of the series that defines the label.
- A slope cut-off placed exactly at the reference's own magnitude cut-off, applied to a large part of the same data, approximates the reference itself. D1 instead needs p < 0.05 on only k points. This is incorporation bias plus spectrum bias, and it favours D2-RC more than D1.
- The manuscript notes that the threshold is "close to" −0.3 dB/yr, but draws no conclusion from it. The Discussion attributes the D2 gain only to noise level.
- The Limitations still say incorporation "favours D1". After Amendment B it favours MD-slope rules most of all, and especially one whose cut-off coincides with the reference's.
- The PoPLR-reference result (46.6% vs 27.6%) is reported without a CI or paired test. Its specificity is lower (88–94% vs 100%, n = 17), and PoPLR over the whole series also includes the first k tests and correlates with MD decline. It mitigates the bias only partly.

Fixes:

1. State explicitly in Results, Discussion and Limitations that the D2-RC gain is probably partly an artefact of the MD-slope reference cut-off and of the excluded grey zone.
2. Report the future-only reference (tests k+1 to end, as in S5) for D2-RC vs D1, even if underpowered.
3. Vary the reference slope cut-off (−0.5 and −1.0 dB/yr) and show whether the D2-RC advantage follows the cut-off.
4. Give the PoPLR-reference paired difference with a bootstrap CI and the specificity.
5. Note that a −0.22 dB/yr flag at k6 is clinically implausible as a trigger for treatment escalation.
6. Label these as exploratory additions to Amendment B.

### Other

- **MODERATE.** The B3 text says "with four to six tests, D1 flagged more progressors than D2, D3 and D4". This is not significant for D2 at k4 (p = 0.11, CI −13.4 to 0.0), D4 at k5 (p = 0.052) or D4 at k6 (p = 0.26, CI includes 0).
  - Fix: "point estimates favoured D1; significant for D3 at k4–6, D2 at k5–6, D4 at k4".
- **MINOR.** The Abstract says "then it flagged fewer progressors than D1" for SC-calibrated D2. This is significant only at k6 (Holm p = 0.031).
- **MINOR.** The Fig. 5 y-axis says "future-confirmed progressors", but the reference includes the first k tests. Use "reference progressors". Also add CIs or report the RC false-alarm rates in the figure legend.
- **MINOR.** The Abstract says the extension was "pre-specified". It was written after the round-1 results and reviews. The Limitations say so; the Abstract should say "pre-specified before analysis, after first results".
- **MINOR.** HB2 failed (70% < 75%). The Discussion still recommends the shuffle audit, and its use as a calibration source (not just an audit) is undermined by C5. Make this explicit.

## 4. Novelty and desk-rejection risks

**Novelty: 3/5.** This is up from about 2.5. A matched-false-alarm comparison with two label-free calibration sources, plus the finding that raw-rate rules are fragile to the calibration source, is a useful methodological contribution. However, the main detector conclusions are underpowered, and the detectors are in-house implementations.

**Top 3 remaining desk-rejection risks**

1. **Reference circularity and spectrum bias.** The MD-slope reference (−0.3 dB/yr, whole series, grey zone excluded) now drives the headline D2-RC result. An editor will see the 0.30 vs −0.3 coincidence. Fix as in 3(d).
2. **Power.** With 26 progressors and 26 stable eyes, "no significant gain" carries little information. The minimum detectable difference is about 35 pp, the D8 k6 CI excludes 0, and HB3 depends on the Holm family. Use the B3-sized cohort (150/164) for the label-free RC-thresholded detectors wherever training allows, and frame the results as estimation.
3. **Post-hoc and in-house design.** Amendment B came after the results and reviews, the plan is in the repository rather than a public registry, the "complex" detectors are the authors' own baselines, and the only true no-change data are 30 weekly-retest patients. Reviewers may call this a self-constructed benchmark. Mitigate with a timestamped public registration (OSF snapshot of the protocol commit hash), consistently hedged wording, and the limitations listed above.

## Summary of severities

- FATAL: none.
- MAJOR:
  - 3(a) Conclusions overstate "explained by false alarms" (D8 k6 CI 0.8–37.1).
  - 3(b) The noise explanation is untested; apply the RC thresholds to the indeterminate eyes and to all eyes.
  - 3(c) "Changed least" / "most stable" for D1 is contradicted by Table 5 (D6/D8 thresholds) and untested in B4 for D6/D8/D9.
  - 3(d) Circularity of the D2-RC gain with the −0.3 dB/yr MD-slope reference is not adequately disclosed or analysed.
- MODERATE: C5 (in-sample SC for ML), C6 (HB3 depends on Holm family), C7, C9 (HB1 near-tautological), the B3 wording, and "matched" meaning matched on Artes only.
- MINOR: C3, C8, C10, Fig. 5 label, "pre-specified" wording, SC-D2 "fewer" wording.
- Number mismatches: none.
