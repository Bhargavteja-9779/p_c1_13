# Review 02 — Glaucoma clinician

## Summary
The authors ask whether any of ten progression detectors flags more future-confirmed progressors than an OLS trend of mean sensitivity in the first 3–6 fields, while keeping a valid false-alarm rate on a weekly-retest data set. They conclude that the simple trend is "hard to beat". They also conclude that complex detectors' gains are explained by false alarms. The clinical question matters, and the true no-change arm is a good idea. However, the clinical translation goes beyond the data. The "progressor" and "stable" groups do not resemble the patients a clinician actually has to decide about. Several clinically relevant facts are buried or absent: severity, reliability, treatment status and the cumulative false-alarm burden of repeated review.

**Recommendation: Major revision.**

## Issues

1. **MAJOR — The reference-stable group consists of improving eyes, not "stable" eyes (Methods, "Reference Standard"; Results, "Specificity on Reference-Stable Eyes...").** A one-sided p > 0.5 for a negative slope means the estimated full-series slope is positive. I re-ran the reference function on all UWHVF eyes with ≥ 8 tests. All 164 reference-stable eyes had a positive MD slope (median +0.10 dB/yr). Clinically, these are eyes whose fields improved over about 13 years. Specificity of 96–100% on such eyes says little about the eyes clinicians worry about: those with a slow drift of −0.1 to −0.3 dB/yr. The text says these eyes were "selected for a flat long-term course" (Results, last sentence of that subsection; Limitations, "Fourth"). That understates the problem. *Fix:* state plainly that "stable" means "non-negative long-term slope". Add a specificity analysis in eyes with slopes between −0.3 and 0 dB/yr and p > 0.05, i.e., clinically stable but not improving.

2. **MAJOR — The progressors are slow and late (Results "Study Data"; Table 1).** The progressor definition is slope < −0.3 dB/yr with p < 0.01 over a median of 11 tests and 12.9 years. Across all UWHVF progressors in my re-run, the median slope was −0.57 dB/yr (IQR −0.85 to −0.41). Detecting a −0.5 dB/yr eye from 3 tests spanning about 2 years is close to impossible for any method. The clinically urgent group is fast progressors (≤ −1 to −2 dB/yr), and it is not analysed separately. *Fix:* report sensitivity stratified by full-series rate (e.g., < −1 dB/yr vs −0.3 to −1 dB/yr) and by baseline MD. Report how many fast progressors were in the 26.

3. **MAJOR — The conclusion overgeneralises (Abstract Conclusion; Conclusions para 2; Discussion para 2).** "Apparent early-detection gains were explained by false alarms" is contradicted by the authors' own data:
   - The MD-rate rule (D2) at 3 tests was valid (2.6% true-null false alarms) and flagged 38.5% vs 19.2%.
   - LightGBM (D8) at 6 tests was valid (3.6%) and flagged 70.8% vs 57.7%.
   - In Table 3, D8 flags 78% of progressors by test 6 vs 69% for D1.

   These gains were not shown to be false alarms; they were simply not statistically significant with 26 eyes. *Fix:* restrict the claim to D6, D8 and D9 at the specific numbers of tests where they were invalid. Say explicitly that gains of 10–20 points for some valid detectors remain possible.

4. **MAJOR — The cumulative false-alarm burden of serial review is not reported on the true-null arm (Results, "Real-World Measures"; Table 3).** Clinicians re-run the analysis at every visit. Table 3 gives cumulative sensitivity ("flagged by test k if any review with 3 to k tests flagged it"). The false flags, however, are per single look, which is an asymmetric comparison. The only cumulative false-alarm figure comes from 26 improving eyes (exploratory). The Artes series have 12 tests, so the cumulative false-alarm probability over looks 3–6 can be computed directly. *Fix:* report the cumulative true-null false-alarm probability over looks 3..6 for every detector. Put it next to cumulative sensitivity in Table 3.

5. **MODERATE — "Unnecessary escalation discussions" (Results, "Real-World Measures", last sentence; Introduction para 3).** A flag is not an escalation. Most clinicians would confirm with a repeat field, which is what GPA's "likely progression" logic encodes. The figure of 224–277 per 1,000 is a hypothetical upper bound. *Fix:* call it "false progression flags requiring confirmation". Add a scenario in which a flag must be confirmed on the next test, and report the confirmed false-alarm rate on Artes.

6. **MODERATE — Treatment, IOP and severity are absent.** UWHVF has no diagnoses or reliability indices (acknowledged). It is therefore unclear whether the cohort is glaucoma, suspect or neuro-ophthalmic. *Fix:* state this as a limitation in the Abstract or Methods. Describe the reference cohort's baseline MD distribution (given: median −4.4 dB). Discuss whether eyes with ocular hypertension or non-glaucomatous field loss were likely included.

7. **MODERATE — Artes patients vs clinic patients (Methods, "Artes retest data").** The Artes cohort is 30 patients with glaucoma from one centre, tested weekly. Its noise may differ from routine clinic testing: practice effects, motivated research participants, a single technician. Notably, the shuffle audit gives D2 at 3 tests 11.7% vs 2.6% on Artes. That fits clinic series having more variability than the Artes series. *Fix:* compare Artes test–retest variability with UWHVF short-interval pairs, which are already used for D7, and discuss the direction of bias.

8. **MODERATE — Clinical advice in the Discussion is not tested (Discussion para 3: "Front-loading or clustering tests ... is therefore likely to help more than a more complex detector").** No analysis compared testing schedules. *Fix:* label it as speculation, or remove it.

9. **MINOR — Terminology.** The text uses "mean sensitivity" for D1, "mean total deviation" for the reference, and "MD" in detector names (OLS-MD, MD rate). Clinicians read MD as the HFA's weighted mean deviation. *Fix:* rename the detectors "OLS-MS" and "MS rate", or define MD as unweighted mean TD at first use. Explain that D1 uses sensitivity, not TD.

10. **MINOR — Running title and title promise "how early".** The answer, a median of 5 tests (about 5 years at UWHVF intervals), is in Table 3 but not in the Abstract. *Fix:* give the clinically useful number in the Abstract.
