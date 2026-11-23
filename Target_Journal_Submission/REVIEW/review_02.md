# Review 02: Glaucoma clinician-scientist (perimetry)

## Summary
The study asks a clinically sensible question: can progression be detected from 3–6 fields without extra false alarms? The authors conclude that an OLS trend of mean sensitivity at p < 0.05 is hard to beat. I largely agree with the direction of the conclusion, but much of the clinical framing is not supported by the design:

- Detector definitions are simplified versions of tools clinicians actually use (GPA, VFI, MD with age correction).
- The reference eyes are an unusual, highly selected group.
- The "real-world" measures do not reflect how false alarms accumulate in clinic.

## Recommendation
**Major revision.**

## Issues

1. **MAJOR – The reference "stable" eyes are improving eyes, not stable ones.**
   - *Location:* Methods, Reference standard ("An eye was stable if the one-sided p was above 0.5").
   - *Problem:* In `run_all.reference` / `deferral.ols`, the one-sided p is `t.cdf(b/se)`. A value above 0.5 means the full-series slope is **positive**. "Stable" eyes are therefore eyes whose MTD improved over a median of 12.9 years. Clinically, a glaucoma eye that improves over 13 years is unusual and may reflect learning, cataract surgery or other confounders. Such eyes will rarely produce early negative trends, which explains specificity of 96–100% for nearly every detector (Table 1).
   - *Fix:*
     - Define stability with a two-sided equivalence band, e.g. slope 95% CI within ±0.2 dB/yr.
     - Report the slope distribution of the stable group.
     - Re-run E1.

2. **MAJOR – The comparator is not MD and not age-corrected; the detectors are not the clinical tools.**
   - *Location:* Detectors D1, D2, D7.
   - *Problem:*
     - D1 and D2 regress *mean raw sensitivity* (`Y.mean`), which includes normal ageing of about 0.06–0.1 dB/yr. The reference uses mean total deviation.
     - D2 is labelled "MD rate".
     - D7 is "GPA-like" but uses limits from short-interval pairs within UWHVF, not GPA's pattern-deviation-based limits from a stable cohort.
     - VFI, which clinicians use daily, is absent.
   - *Fix:*
     - Use MTD (or pattern deviation for D7) consistently.
     - Rename D2 "mean-sensitivity rate".
     - Add VFI or justify its absence.
     - Avoid "similar in spirit to Guided Progression Analysis" unless the limits are validated against GPA.

3. **MAJOR – Per-opportunity false alarms understate the clinical burden.**
   - *Location:* Results, Real-world measures; Table 3.
   - *Problem:* "False flags per 1,000 stable eyes per detection opportunity" is not what a clinic experiences. A patient is re-evaluated at tests 3, 4, 5 and 6, so the chance of at least one false flag is higher. Table 3 reports cumulative flags only for 26 reference-stable eyes, where 1 eye equals 3.8%. The Artes windows allow a direct estimate of cumulative false alarms over 4 looks.
   - *Fix:*
     - Report the cumulative probability of ≥1 false flag by test 6 on Artes.
     - Report flags per 1,000 patient-years at a stated testing frequency.
     - Evaluate a "flag then confirm on the next test" rule, which is how most clinicians act.

4. **MAJOR – Timing is in test number, not time.**
   - *Location:* Results, Real-world measures ("median of the 4th test").
   - *Problem:* Reference eyes had a median inter-test interval of 1.0 year (`descriptives.json`), so "test 4" means about 3 years after baseline. Clinicians make decisions in time units.
   - *Fix:* Report the median time (years) to first true flag, and discuss the result in relation to Chauhan's six-tests-in-two-years recommendation [5].

5. **MODERATE – Spectrum of the reference eyes.**
   - *Location:* Results, Study sample.
   - *Problem:* Only eyes with ≥8 tests were used (132), and 80 of these (61%) were excluded as indeterminate. The remaining eyes had early disease (median MTD −4.4 dB) and about 13 years of annual follow-up. Moderate-progression eyes, the hardest and most relevant group, are excluded, which inflates the apparent separation.
   - *Fix:*
     - Report results for the indeterminate group, e.g. the flag rate.
     - Discuss spectrum bias.
     - Add a flow diagram: 1,489 → 869 → 132 → 52.

6. **MODERATE – Clinical recommendations are not tested.**
   - *Location:* Discussion paragraph 4 ("More frequent early testing … is likely to help more than a more complex detector"; "best balance … in both clinics").
   - *Problem:* Neither statement was analysed. In GRAPE, D5 was statistically identical to D1, so "best" is not established.
   - *Fix:* Phrase both as hypotheses, or test frontloading by simulation with the Artes noise.

7. **MODERATE – Reliability indices are ignored.**
   - *Location:* Data sources; Limitations.
   - *Problem:* UWHVF lacks reliability indices, but the Artes data include false-positive rate, false-negative rate and fixation losses (loaded in `artes_retest.py`) and they are unused. Clinicians discard unreliable fields.
   - *Fix:* Run a sensitivity analysis on Artes excluding unreliable tests (e.g. FP > 15%).

8. **MINOR – Overstatement of D1's behaviour.**
   - *Location:* RQ1 paragraph ("So did the rate rule, the pointwise rule … kept false alarms close to the nominal 5%").
   - *Problem:* D2 and D3 are far below 5% (0.2–2.6%). They are conservative, not "close to nominal".
   - *Fix:* Say "at or below".

9. **MINOR – Missing perimeter details for GRAPE.**
   - *Location:* Data sources, GRAPE.
   - *Problem:* The text says only "a different perimeter".
   - *Fix:* Name the instrument and test pattern, and state how sensitivities relate to the HFA dB scale.
