# Review 10: "Reviewer 2", hostile novelty assessment

## Summary
Read against the authors' own novelty map (`journal_selection/novelty_map.csv`, 55 entries), this paper re-establishes things the field already knows:

- Pointwise and global trend methods have known false-positive rates on retest data.
- Re-ordering a series estimates specificity.
- Short series cannot support reliable progression calls.
- ML labels drive ML results.

The one "positive" finding, that a detector with a big sensitivity gain is anti-conservative, concerns an in-house variant the authors had already shown to be anti-conservative during development. The authors' own scorecard rates novelty 22/30, and their log says "Honest label expected: NOT REMARKABLE". I agree with that self-assessment.

## Recommendation
**Reject** in current form. A substantially re-scoped resubmission could be considered.

## Issues

1. **FATAL – The headline was a foregone conclusion.**
   - *Location:* Abstract; Key Summary Points; Discussion paragraph 3.
   - *Problem:* Round 5 of the development log reports, on the same Artes data, "region-max detrended: sens 35.5%, FPR 20–22% → INVALID". The pre-specified benchmark then includes this detector and "discovers" that its gain comes with 22.4% false alarms. That is a replication on the same data, not a finding. Removing D6, the paper's RQ2 result is: no detector differs significantly from D1 in a 26-eye sample.
   - *Fix:* Remove D6 from the headline, or present it only as a positive control for the framework. Re-evaluate what is left as the paper's contribution.

2. **MAJOR – True no-change evaluation is not new.**
   - *Location:* Introduction ("Only a few studies have measured false alarms on true no-change data [9]").
   - *Problem:* The novelty map lists the following:
     - Artes 2014 [9]: GPA specificity on exactly these 12-test retest series, with 1,000 random re-orderings. This is both a true-null arm and a shuffle audit.
     - Montesano 2021 [14]: false-positive rates matched via permutations of a test–retest cohort.
     - Marín-Franch 2021 [13]: false-positive rates by permuting series.
     - O'Leary 2012 [7]: within-series permutation.
     - Wu & Medeiros 2018 [10]: specificity on simulated stable eyes.

     The paper's two "innovations" (true no-change arm and shuffle audit) are both present in [9] alone.
   - *Fix:* State plainly that the true-null arm and the shuffle audit follow [9, 13, 14]. The contribution then reduces to "applying these to a broader detector set including ML", and that is what the title and Abstract should say.

3. **MAJOR – The shuffle audit is PoPLR's permutation idea presented as a clinic tool, and it failed its own test.**
   - *Location:* RQ3; Key Summary Points.
   - *Problem:* The pre-specified ρ ≥ 0.7 was missed (0.65), and the success rule for "most cells within 3 pp" was defined loosely. The post hoc rescue ("for detectors based on a p-value, the audit was within 3 pp") is near-tautological: for a p-value detector whose null is the permutation null, a permutation audit must approximately reproduce α.
   - *Fix:* Present H3 as not supported, and drop the post hoc rescue from the main text.

4. **MAJOR – The comparators are weak; the strongest published methods are missing.**
   - *Location:* Detectors; Limitations ("we did not test every published method").
   - *Problem:*
     - ANSWERS [12], hierarchical Bayes [14], smoothing [33], VFI trend and the real GPA are absent.
     - The ML baselines are small re-implementations trained on 192 labelled eyes (see Review 04).
     - Three of the ten "detectors" are the authors' own failed development ideas (D5 = round 1, D6 = round 5, D10 = round 0, per S1).

     A benchmark mostly of in-house variants cannot support statements about "new methods" in the literature.
   - *Fix:*
     - Add at least ANSWERS, or a hierarchical Bayesian model (code is public in the `visualFields` ecosystem / author repositories), plus VFI.
     - Reframe the ML part as illustrative.
     - Move D5/D6/D10 to a separate "development variants" block.

5. **MAJOR – The negative conclusion comes from an underpowered comparison.**
   - *Location:* RQ2.
   - *Problem:* With 26 progressors and Holm over 9 tests, only a ~35-pp gain is detectable. The conclusion "a simple trend test remained hard to beat" restates the null hypothesis.
   - *Fix:* Enlarge the reference set or present the result as estimation with an explicit minimum detectable difference.

6. **MODERATE – Overlap with "Labeling matters" [23] and with the frequency-of-testing literature [5, 30–32].**
   - *Location:* Discussion paragraph 2.
   - *Problem:* The finding that ML thresholds set on label-defined stable eyes do not transfer is the message of Kim et al. [23]. The finding that variability limits early detection is the message of [5, 30, 31].
   - *Fix:* Say explicitly what this study adds beyond [23] and [5, 30, 31].

7. **MODERATE – Journal fit.**
   - *Location:* Whole paper.
   - *Problem:* For a therapy journal, the paper gives no therapeutic or management outcome. The only practical advice ("run a shuffle audit") is not validated as a decision tool: there is no audit threshold and no classification accuracy.
   - *Fix:* Define an audit decision rule (e.g. audit rate > 7.5%), report its sensitivity and specificity for detecting invalid detectors, and validate it on GRAPE.
