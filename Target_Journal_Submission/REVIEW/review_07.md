# Review 07: Visual-field psychophysics expert

## Summary
Using the Artes 12-week retest series as a "true no-change" arm is attractive and has precedent (Artes et al. 2014 [9]). But the arm is a valid null only for a narrow class of statistics:

- Weekly retest data contain short-term (within-season) variability only.
- Amendment A1 then stretches these weekly fields onto clinical intervals of about one year.
- For any rule that thresholds a *rate in dB/year*, or uses absolute rate features, this makes the null too easy: the apparent rate noise is shrunk by the missing long-term fluctuation.

The paper's "valid" and "invalid" labels for rate-based and ML detectors are therefore not interpretable as clinical false-alarm rates.

## Recommendation
**Major revision.**

## Issues

1. **MAJOR – A1 produces a null without long-term fluctuation, which biases rate-based detectors towards "valid".**
   - *Location:* Methods E2 and amendment A1; Results RQ1; Limitations ("keeps the null valid but cannot reproduce long-term fluctuation").
   - *Problem:*
     - Long-term (between-visit, months-to-years) variability in perimetry exceeds short-term variability. By my computation from the provided data, the residual SD of mean sensitivity is about 1.03 dB in UW reference-stable eyes against about 0.48 dB over 12 weeks in Artes.
     - **Scale-invariant tests** (D1, D4, D5, D10, p-value based) are unaffected by relabelling time. Their Artes false-alarm rates are meaningful as a type-I error check *under short-term noise only*.
     - **Rate-threshold rules** (D2: slope ≤ −1 dB/yr; D3: slope ≤ −1 dB/yr and p < 0.01) and ML models using `md[-1] − md[0]`, slopes and time span (D8, D9) see roughly half the noise they would see in clinic. D2's 2.6% at k = 3 is therefore an under-estimate.
     - The shuffle audit (11.7%), which uses real long-term variability, is probably closer to the truth. The paper instead calls this "over-estimation".
   - *Fix:*
     - Classify detectors as scale-invariant or not.
     - For non-invariant ones, add a sensitivity analysis that inflates Artes residuals to match long-term fluctuation. Options: add a per-visit global shift drawn from the between-visit variance in UW stable eyes, or use Artes-type data with longer spacing if available.
     - Do not label D2, D3 or D7 "valid" on the A1 arm alone.

2. **MAJOR – The interpretation of shuffle-audit disagreement is reversed for rate rules.**
   - *Location:* Shuffle audit section ("The audit over-estimated false alarms for rules without a p-value"); Fig. 3 legend ("lie below the line").
   - *Problem:* The disagreement has two sources:
     - the Artes arm lacks long-term fluctuation (issue 1);
     - shuffling UW eyes that truly progress preserves their spread, which inflates the audit.

     Neither source is "the truth". The text treats Artes as ground truth throughout.
   - *Fix:* Present the two estimates as bounds with known biases. Shuffle only reference-stable or low-slope eyes as a cleaner audit, and report it.

3. **MAJOR – Global stationarity of the Artes series is assumed, not shown.**
   - *Location:* Data sources, Artes ("Glaucoma does not change in 12 weeks in a measurable way").
   - *Problem:* There are known learning and fatigue effects in repeated weekly perimetry, especially in the first sessions. Any systematic drift over the 12 sessions (a learning *improvement* lowers false alarms; fatigue raises them) violates exchangeability, so windows starting at session 1 differ from later windows.
   - *Fix:* Test for a monotone trend across sessions (a mixed model of mean sensitivity on session number), report false alarms by window start position, and consider dropping session 1.

4. **MODERATE – Heteroscedasticity and severity mismatch.**
   - *Location:* E2; RQ4.
   - *Problem:* Test–retest variability increases strongly as sensitivity falls [4]. The Artes patients (median mean sensitivity about 26.9 dB by my count) and the UW reference eyes (about 28.1 dB at baseline) differ, and pooled-null strata (<20, 20–26, ≥26 dB) put many Artes eyes near a stratum boundary. False alarms per severity stratum are not reported.
   - *Fix:* Report Artes false alarms by severity tertile, and match or weight UW donors by severity if relevant.

5. **MODERATE – The weekly spacing is not exactly weekly.**
   - *Location:* Data sources ("12 visual fields in 12 consecutive weeks").
   - *Problem:* `descriptives.json` gives a median span from first to last test of 12.0 weeks (IQR 11.0–13.3). Twelve weekly tests span 11 weeks, so some series include gaps. This is minor, but the text should be exact.
   - *Fix:* Report the span correctly. State that A1 discards the real dates.

6. **MODERATE – D6's failure has a known mechanism and does not generalise to "new detectors".**
   - *Location:* Discussion paragraph 3.
   - *Problem:* The authors correctly note that detrending with k = 3 leaves 1 residual df. That is a specific statistical error, which says little about the false-alarm behaviour of published methods (ANSWERS, hierarchical Bayes, GPA). The general claim in the Abstract and Conclusions ("apparent gains … were explained by false alarms") is not supported by psychophysical reasoning.
   - *Fix:* Narrow the conclusion to the detectors tested.

7. **MINOR – Reference [28] is misused.**
   - *Location:* Discussion ("Permutation of residuals in a model with very few degrees of freedom is known to be fragile [28]").
   - *Problem:* Freedman & Lane (1983) introduce the residual-permutation approach. As far as I know, they do not document its failure with 1 residual df.
   - *Fix:* Cite a comparative study of permutation schemes for small samples (for example, Anderson & Legendre 1999, J Stat Comput Simul; UNVERIFIED, please check), or demonstrate the problem with a short simulation in the Supplement.

8. **MINOR – Artes reliability data are unused.**
   - *Location:* E2.
   - *Problem:* The Artes data include false-positive rate, false-negative rate and fixation losses (`artes_retest.py`). Clinicians would discard some of these fields.
   - *Fix:* Run a sensitivity analysis with reliability filtering.
