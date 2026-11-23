# Review 08: External-validity reviewer (GRAPE, amendment A2)

## Summary
GRAPE is offered as an "external clinic", and the Abstract reports: "Externally, higher sensitivity again came with more false positives." I examined `grape.py`, the E4 block of `run_all.py`, Table 2 and the GRAPE data. The external analysis has three structural problems:

- The labels are computed from (often) the same 3–4 visits the detectors see.
- The ML comparator is transferred across perimeters with scale-dependent features.
- Under A2, three detectors (including D6, the headline detector) cannot be evaluated at all.

As designed, E4 does not test whether the UWHVF conclusions transfer.

## Recommendation
**Major revision.**

## Issues

1. **FATAL (for the external claim) – At k = 3/4, many GRAPE eyes are fully seen by the detector that is supposed to predict their label.**
   - *Location:* E4; Table 2; Abstract.
   - *Problem:* Visit counts in GRAPE (my count from the data file): 3 visits, 100 eyes; 4 visits, 75; 5 visits, 38; 6 or more, 50. Of the 27 MD-criterion progressors, 9 have exactly 3 visits and 5 have exactly 4. At k = 3, 38% of eyes contribute their whole series, and the MD-criterion label is essentially a trend rule on those same fields. Agreement of D1 and D2 with this label is therefore partly tautological. The comparison says nothing about *early* detection.
   - *Fix:* Restrict E4 to eyes with at least k + 2 visits, and report the n (it will be small: 88 eyes have ≥5 visits). Alternatively, present E4 as "agreement with the dataset's own criteria" rather than external validation of early detection.

2. **MAJOR – "Clinician-labelled" mis-describes the labels.**
   - *Location:* Data sources ("progression labels assigned with three criteria"); Results ("clinician-labelled progressing eyes"); Fig. 4 axis; Table 2 title; protocol ("clinician-applied criteria").
   - *Problem:* The labels are criterion-based (MD, PLR2, PLR3) according to the GRAPE descriptor. Calling them clinician-labelled implies independent expert judgement.
   - *Fix:* Use "criterion-based (MD) label" throughout, and quote the GRAPE definitions of each criterion.

3. **MAJOR – The D8 transfer is confounded by instrument scale.**
   - *Location:* E4 / A2 ("D8 was transferred unchanged from UWHVF"); Results External; Table 2 (D8 specificity 61.2% at k = 3).
   - *Problem:* D8 uses absolute dB-level features (`md[-1]`, `md.mean()`, range, SD) learned on HFA. GRAPE sensitivities come from a different perimeter. The +33.5 pp false-positive excess is what covariate shift would produce, so attributing it to "higher sensitivity came with more false positives" is unsafe.
   - *Fix:* Re-fit D8 within GRAPE by cross-fitting (as for D5 and D7), or harmonise scales. Report both the transfer and the refit results.

4. **MAJOR – The external arm cannot test the main claim.**
   - *Location:* A2; Table 2 footnote; Abstract.
   - *Problem:* D6 (the only significant gain), D9 and D10 are not evaluated on GRAPE. There is no external true no-change arm. GRAPE therefore cannot replicate either RQ1 or the D6 finding. The protocol's RQ5 ("Do RQ1–RQ2 conclusions hold in an independent clinic?") is answered only for RQ2, and only partially.
   - *Fix:*
     - Say so explicitly in the Abstract and Discussion.
     - Run the shuffle audit on GRAPE (it needs no retest data) for all GRAPE detectors.
     - Implement D6 regions for the GRAPE grid (the code's docstring treats GRAPE as an Octopus G1 59-point grid, for which regional clusters are well defined), or drop the claim.

5. **MAJOR – The protocol's secondary labels were not reported.**
   - *Location:* Protocol ("primary: MD label; secondary: PLR2, PLR3, any"); `run_all.py` stores `PLR2`/`PLR3` in `extra`.
   - *Problem:* The PLR2/PLR3 analyses were pre-specified but are absent from the manuscript and the Supplement. MD-based detectors are favoured by an MD label, so the PLR labels are the natural check.
   - *Fix:* Report E4 against PLR2, PLR3 and "any" (40 and 14 progressors for PLR2 and PLR3, per `descriptives.json`), or document why they were dropped.

6. **MODERATE – Own-clinic calibration on GRAPE is thin.**
   - *Location:* A2 ("D5 and D7 were re-calibrated on GRAPE itself by five-fold patient-level cross-fitting").
   - *Problem:*
     - D7 limits come from about 153 visit pairs ≤ 0.5 years in all of GRAPE (my count), which is fewer per fold, with extrapolated bins.
     - D5 uses HFA-specific strata cut-offs (20 and 26 dB).
     - The protocol said leave-one-patient-out for D5, but the code uses 5-fold. This is a deviation not listed in S2.
   - *Fix:* Report calibration-set sizes per fold, use GRAPE-specific strata (e.g. tertiles of the GRAPE level), and list the LOPO → 5-fold change.

7. **MODERATE – The GRAPE population and instrument are not described.**
   - *Location:* Data sources; Results.
   - *Problem:* The perimeter model, strategy, age, baseline MD, glaucoma type and reliability criteria are not given. Per-eye point removal also leaves some eyes with as few as 36 points.
   - *Fix:* Add a descriptive table (UWHVF reference eyes, Artes, GRAPE) and a point-count distribution.

8. **MINOR – Table 2 at four tests.**
   - *Location:* Table 2.
   - *Problem:* n = 18 progressors at k = 4 (`statistics.json`), which the table does not state. CIs such as D7 "16.7 (0.0–33.3)" are percentile-bootstrap and degenerate at the boundaries.
   - *Fix:* Add the n per k, and use exact or Wilson intervals.
