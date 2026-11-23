# Close calls (overlap >= 4) - hostile prior-art recheck, 2026-11-23

Basis: abstracts from Europe PMC / OpenAlex / PubMed / Crossref / arXiv (see prior_art_search_log.md).
Full texts were NOT read. Anything stated beyond the abstract is marked UNVERIFIED.
No paper scored 5 (identical study). Eight papers scored 4.

## 1. Artes PH, O'Leary N, Nicolela MT, Chauhan BC, Crabb DP. Ophthalmology 2014. 10.1016/j.ophtha.2014.04.015
- What they did that we also do: they measured the false-positive rate of a clinical progression method (GPA) on TRUE no-change data. The data were 30 glaucoma eyes, each tested 12 times over 3 months, which is the same retest set we use as E2. They also re-analysed each series after 1000 random re-orderings. So they already used both "true no-change retest" and "permutation" for specificity. They showed that false alarms vary widely between patients (<1% to 80%).
- What is truly different: one event-based detector (GPA). No trend, conformal or ML detectors. No restriction to 3-6 tests. No comparison of a shuffle audit on CLINIC series against the true-null rate. No detectors calibrated on clinic labels.

## 2. Montesano G, Garway-Heath DF, Ometto G, Crabb DP. TVST 2021. 10.1167/tvst.10.12.4
- What they did that we also do: they compared several detectors (hierarchical Bayesian models, simple linear regression, PoPLR) at a false-positive rate taken from permutations of a separate test-retest cohort (360 tests, 30 glaucoma eyes). Those numbers match the Artes data, but whether it is the same data is UNVERIFIED. The setup is a multi-detector comparison with a true-retest null, which is close to our E2.
- What is truly different: they used the retest null to EQUALISE specificity before comparing sensitivity. We report each detector's raw true-null false-alarm rate as it would be calibrated in practice. Their comparison has no supervised ML or sequence models, does not focus on 3-6 tests, and has no shuffle-audit validation.

## 3. Yousefi S et al. Am J Ophthalmol 2018. 10.1016/j.ajo.2018.06.007
- What they did that we also do: ML compared with global, region-wise and pointwise classical detectors. All thresholds were set at 95% specificity on a no-change test-retest dataset (133 eyes, 10 tests in 10 weeks; this is probably the same cohort as Gardiner 2017, UNVERIFIED).
- What is truly different: they calibrated the ML index ON true no-change data, so its false-alarm rate is controlled by design. We calibrate supervised ML on clinic "reference-stable" eyes, which is how most recent ML papers do it, and show 19-28% true-null false alarms. They evaluated time-to-detection on long series, not on 3-6 tests. This paper is the strongest counter to any claim that "nobody calibrates ML on retest data". It is also our best citation for the remedy.

## 4. Garway-Heath DF et al. Health Technol Assess 2018. 10.3310/hta22040
- What they did that we also do: a multi-method benchmark (GPA, PoPLR, ANSWERS, sANSWERS, plus new PERM / MaHMIC / MaGIC methods). Specificity was set from a TRUE short-term no-change cohort (RAPID: 72 stable patients, 11 VF and OCT tests within 3 months). Hit rates were compared at 95% specificity.
- What is truly different: no supervised ML, no shuffle-vs-true-null check, not limited to 3-6 tests, and the data are not open. As with Montesano 2021, specificity was equalised rather than audited.

## 5. Marin-Franch I, Artes PH, Turpin A, Racette L. TVST 2021. 10.1167/tvst.10.14.13
- What they did that we also do: they estimated each detector's false-positive rate by randomly re-ordering clinic series (our shuffle audit) and found that a sophisticated model-based detector (ANSWERS) had a false-alarm rate about 3x nominal (15-17% at alpha 0.05, against 3-7% for PoPLR). After equating specificity, the simpler method was at least as sensitive. This is the closest precedent for our message: "the complex method looks better only because of excess false alarms; once specificity is controlled, the simple method is as good".
- What is truly different: no true no-change retest arm, so they could not check whether the shuffle estimate is right. No supervised ML. Not 3-6 tests (their series had 7 to 17.5 tests on average).

## 6. O'Leary N, Chauhan BC, Artes PH. IOVS 2012 (PoPLR). 10.1167/iovs.12-10049
- What they did that we also do: they used within-eye permutation both as a test and to estimate false-positive rates from randomly re-ordered clinic series, at the 5th, 8th and final exam. They showed PoPLR false-positive rates equal nominal levels.
- What is truly different: one method (also one of our detectors). No true-null retest comparison and no ML.

## 7. Gardiner SK, Mansberger SL, Demirel S. IOVS 2017. 10.1167/iovs.17-21562
- What they did that we also do: they set global, pointwise and cluster criteria to exactly 95% specificity using re-orderings of 133 test-retest eyes (7-10 tests each), then compared time-to-detection.
- What is truly different: classical methods only, long series, and no audit comparing clinic shuffles with the true null.

## 8. Gardiner SK, Demirel S. Am J Ophthalmol 2017. 10.1016/j.ajo.2017.01.013
- What they did that we also do: they used a short-term test-retest cohort (45 eyes, 5 tests) with randomly ordered artificial dates to set critical P values for MD, VFI and PSD trends at 95% specificity over 5-test series. This is close to our 3-6 test horizon.
- What is truly different: global indices only. No ML, conformal or pointwise permutation detectors, and no shuffle-audit validation.

### Near misses (overlap 3) a reviewer will cite
- Goldbaum 2012 IOVS (POP; 10.1167/iovs.11-8363): an ML classifier calibrated on 55 eyes with 5 VFs in 4 weeks. Calibrating ML on retest data dates from 2012.
- Mandal 2024 AJO (10.1016/j.ajo.2024.04.030): an OCT deep-learning model trained with SCRAMBLED sequences to learn test-retest noise. This is the closest analogue of our self-supervised order network.
- Urata 2020 AJO (10.1016/j.ajo.2019.10.034) and Gardiner 2022 TVST (10.1167/tvst.11.8.3): long-term variability is larger than short-term retest variability. This directly threatens E2. A 12-week retest null probably UNDERSTATES real-world false alarms, so our ML false-alarm rates (19-28%) are, if anything, a lower bound. We must say this.
- Saeedi 2021 TVST, Dixit 2021 Ophthalmology, Kim 2026 PLoS One ("Labeling matters"): ML VF progression models trained and scored against algorithm-derived labels. They report "specificity" only relative to those labels. These papers are the target our E2 result critiques.
- Tan 2026 Ophthalmol Glaucoma (10.1016/j.ogla.2026.01.004): 21% of eyes show an OLS P<0.05 "reversion" (a false-positive proxy) in clinic data. This is relevant to the early-series false-alarm rate of our OLS baseline.

## Blunt verdicts

1. Is evaluating VF progression detectors on true no-change retest data already established? YES, firmly. Artes 2014 (the very dataset we use), Garway-Heath 2018 (RAPID), Montesano 2021, Yousefi 2018, Gardiner 2017 (x2), Goldbaum 2012 and Mayama 2004 (via simulation from retest data) all do it. We cannot claim the E2 arm as a methodological novelty. We can only claim to apply it to a broader set of detectors (supervised ML, sequence, self-supervised, conformal) at 3-6 tests on open data.

2. Is shuffle/permutation as a specificity audit already established? YES, for more than 10 years: O'Leary 2012, Artes 2014, Gardiner 2017/2020, Marin-Franch 2021 and Montesano 2021 in VF, Thompson 2020 and Marin-Franch 2025 in OCT, and surrogate-data testing in physics since Theiler 1992. What we did NOT find in any abstract: a per-detector check of how well clinic-series shuffle false-alarm rates track a TRUE no-change rate (our Spearman 0.65). This "audit of the audit" is the only part of E3 that may be new. Because full texts were not read, it is possible that O'Leary 2012, Artes 2014 or Montesano 2021 report something similar inside their results (UNVERIFIED). It needs a full-text check before submission.

3. Is "ML detectors have inflated true-null false-alarm rates" new? PARTLY. No abstract found shows that supervised ML VF progression detectors, thresholded on clinic "stable" labels, give 19-28% false alarms on true no-change data. In that specific form it appears new. However:
   - Marin-Franch 2021 already showed inflated false alarms for a sophisticated (non-ML) model.
   - Yousefi 2018 and Goldbaum 2012 already avoided the problem by calibrating ML on retest data. A reviewer will say "known pitfall, known fix".
   - Schuemie 2013/2014 (negative controls) shows the same phenomenon in epidemiology.
   - Mechanistically, the result is the standard imperfect-reference-standard bias (Reitsma 2009): "stable" labels contain undetected progressors and noise, so the 95th percentile is set too low.
   The finding is a useful empirical warning, not a conceptual discovery. Its strength depends on showing it holds across model classes and in GRAPE.

4. The claim "no valid detector beats OLS at 3-6 tests" echoes Marin-Franch 2021 (PoPLR ~ ANSWERS once specificity is equated), Gardiner & Demirel 2017 (MD is fastest) and Wu & Medeiros 2018 (event ~ trend at matched specificity). It is a confirmatory negative result, extended to ML and short series.

## Contribution framings that survive this prior art
1. **Validity audit of modern ML VF progression detectors.** "Specificity reported against clinic-derived 'stable' labels does not transfer to true no-change data. On the public Artes 12-week retest set, supervised ML detectors calibrated in the usual way give 19-28% false alarms at a nominal 5%." Cite Yousefi 2018 and Goldbaum 2012 as the correct practice that recent ML papers (Dixit 2021, Saeedi 2021, Kim 2026) do not follow. Recommend a minimum reporting standard: true-null false-alarm rate on a public retest set.
2. **Does the shuffle audit work? An "audit of the audit".** This is the first systematic comparison we found of clinic-shuffle false-alarm estimates against true no-change false-alarm rates across 10 detector families. The shuffle audit ranks detectors moderately (rho 0.65), and the paper would describe where it fails (for example detrended/pooled statistics, and long- vs short-term variability per Urata 2020). The full texts of O'Leary 2012, Artes 2014 and Montesano 2021 must be checked first.
3. **Open, reproducible short-series benchmark (3-6 tests).** All public data (UWHVF, visualFields retest, GRAPE) and code. The result: once false alarms are controlled, no detector clearly beats the OLS trend p-value at 3-6 tests. Present it as an extension of Marin-Franch 2021, Gardiner & Demirel 2017 and Wu & Medeiros 2018 to ML and very short series. The novelty is the scope (10 detectors, 4 arms, open), not the idea.
4. (Weaker) **Cross-field "negative-control" framing for longitudinal clinical AI.** Borrow negative-control and surrogate-data logic (Schuemie, Lipsitch, Theiler, MIRIAD rescans) as a general evaluation template for progression detectors. This only works if framed as a methods or reporting paper, not a new-method paper.

Framings to DROP: "first to evaluate VF detectors on test-retest/no-change data"; "first to use permutation/shuffling to estimate specificity"; "novel conformal/pooled null makes 3-test detection possible". The pooled detrended method's apparent gain comes from its 22% false-alarm rate, which supports the audit message rather than a method claim.
