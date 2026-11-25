# Supplementary Material

**How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm**

## S1 Development history: ideas tried and abandoned

Before the final protocol, we tried to develop a new detection method. Rounds 0–3 and 5 used the UWHVF training and validation sets; Round 4 used a different open data set (Moorfields neovascular AMD), and Round 5 also used the Artes retest data. The UWHVF test set and the GRAPE labels were locked. A Round 5 variant (weighted mean sensitivity) had a division-by-zero error; its results were void and it was not carried forward. The full log, with every hypothesis, falsifier and result file, is in the code repository (`code/experiments/development_log.md`; result files `results/pilot_v0.json`, `pilot_v1.json`, `pilot_deferral.json`, `pilot_v2.json`, `d6_round5.json`). In summary:

- **Round 0.** A self-supervised network that recognises the true time order of tests, used as a within-eye permutation statistic (D10 in the final benchmark). It did not flag more eyes than PoPLR or the mean-sensitivity trend. Abandoned as a new method.
- **Round 1.** A pooled ("population-calibrated") null built from shuffled series of other eyes, to allow valid tests with three fields (D5 in the final benchmark). Gains were small and limited to three or four tests.
- **Round 2.** Reformulation as risk-controlled deferral of visual-field tests. Deferral rules delayed detection in most progressing eyes, and the risk-control procedure could not certify any useful threshold. Abandoned.
- **Round 3.** Pooled-detrended null against a future reference in the validation set. It appeared more sensitive at three and four tests.
- **Round 4.** A different clinical problem (anti-VEGF treatment rhythm in neovascular AMD, Moorfields open data). Treatment rhythm added no prognostic value. Abandoned.
- **Round 5.** The pooled-detrended variants (D6 in the final benchmark) were checked on the Artes retest data. They raised far more false alarms than the nominal 5%. This led to the final research question: whether apparent early-detection gains are explained by false alarms. This is the one development use of the Artes data, disclosed in the main text.

Ideas counted: six rounds, nine candidate method variants. Because no development idea is claimed as a new method, the final benchmark tests all ten detectors with Holm correction within each number of tests.

## S2 Sensitivity against the secondary (PoPLR-based) reference

{{TABLES2}}

## S3 All paired comparisons with D1

{{TABLES3}}

## S4 GRAPE: PLR3 and any-criterion labels

{{TABLES4}}

## S5 Exploratory future-only reference

{{TABLES5}}


## S6 Untrained detectors on all eligible eyes

{{TABLES6}}


## S7 Post-hoc robustness of the calibrated rate rule

{{TABLES7}}

## S8 Semi-synthetic sensitivity (amendment C)

{{TABLES8}}

## S9 Literature search for amendment C (prior art)

On 25 November 2026 we searched OpenAlex (titles and abstracts), Crossref, Europe PMC and the web for combinations of "visual field", "progression", "moderated t", "empirical Bayes", "variance shrinkage", "sequential monitoring", "CUSUM", "cumulative false positive", "repeated testing" and "simulation". The closest prior work was: CUSUM charts for visual fields and nerve-fibre-layer thickness (Ledolter and Kardon, 2013); hierarchical Bayesian models, which shrink slopes and model variance (Montesano et al., 2021; Mohammadzadeh et al., 2025); and data-driven simulation of longitudinal fields from clinic residuals (Wu and Medeiros, 2018; Li et al., 2023). We found no study that used a clinic-residual null to set detector thresholds, compared threshold sources on true no-change data, applied a closed-form empirical-Bayes moderated trend test to visual fields, or calibrated a monitoring rule to a cumulative false-alarm budget. Google Scholar, Scopus and Web of Science could not be searched from our computing environment, so this claim is limited to the sources named.
