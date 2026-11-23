# Apparent Gains in Detecting Glaucomatous Visual-Field Progression Disappear at Matched False-Alarm Rates: A Two-Stage Benchmark

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, DEGREES — to be completed by the authors]

**Affiliations:** [INSTITUTION, CITY, COUNTRY — to be completed by the authors]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — to be completed by the authors]

**ORCID iDs:** [to be completed by the authors]

**Prior presentation:** [TO BE CONFIRMED BY THE AUTHORS: none.]

## Abstract

**Introduction:** Decisions to escalate glaucoma treatment rely on detecting visual-field progression. New detectors, including machine-learning models, often claim earlier detection, but are rarely compared at the same false-alarm rate. We tested whether any detector beats a simple trend test of mean sensitivity when false alarms are matched.

**Methods:** Study 1 compared ten detectors on a locked test split of the University of Washington data set, using the first 3–6 tests, with false alarms measured on true no-change retest series ({{d:artes.n_patients:int}} patients tested over about 3 months). Study 2, specified in a new protocol, used 5-fold cross-fitting across all {{d:s2_all.n_eyes:int}} eyes with at least eight tests ({{d:s2_progressors.n_eyes:int}} progressing, {{d:s2_stable.n_eyes:int}} stable). Every detector's threshold was set to 5% false alarms on shuffled series from the clinic's own records ("shuffle calibration"). An external clinic ({{d:grape.n_eyes:int}} eyes) tested local recalibration.

**Results:** Gradient-boosted trees thresholded at 95% specificity on stable eyes, a common practice, appeared {{qd:sens:B8:6}} percentage points more sensitive than the trend test at six tests, but raised false alarms in {{q:fa:B8:6}} of true no-change series. With shuffle calibration, the same model raised {{q:fa:S5:6}} false alarms and gained {{qd:sens:S5:6}} points (95% CI {{qdlo:sens:S5:6}} to {{qdhi:sens:S5:6}}). Across eight shuffle-calibrated detectors and 3–6 tests, no detector was significantly more sensitive than the trend test; all upper confidence limits for the gain were below {{qmaxhi}} points. Controlling cumulative false alarms over repeated reviews to 5% reduced detection by the sixth test from {{qc:sens:D1-repeated:6}} to {{qc:sens:Q2 Confirmed trend:6}}. In the external clinic, local recalibration restored specificity of the transferred model ({{qg:spec_MD:S5 SC-LightGBM (local threshold):3}}) but reduced its sensitivity.

**Conclusion:** Apparent gains in early detection of visual-field progression can be explained by higher false-alarm rates. At matched false alarms, a plain trend test was as sensitive as machine-learning and permutation detectors. Detectors should be compared, and deployed, at a stated false-alarm rate.

## Keywords

Benchmark; False alarms; Glaucoma; Machine learning; Perimetry; Progression; Specificity; Visual field

## Key Summary Points

**Why carry out this study?**

- Escalating glaucoma treatment depends on detecting visual-field progression, and many new detectors claim to detect it earlier than simple trend analysis.
- We asked whether such gains persist when every detector is held to the same false-alarm rate, measured on data in which the disease did not change.

**What was learned from the study?**

- A machine-learning detector thresholded in the usual way appeared {{qd:sens:B8:6}} percentage points more sensitive than a trend test of mean sensitivity, but raised false alarms in {{q:fa:B8:6}} of true no-change series.
- When thresholds were calibrated to 5% false alarms on shuffled series of the clinic's own records, no detector was significantly more sensitive than the trend test, and gains of {{qmaxhi}} percentage points or more were excluded.
- Claims of earlier progression detection should report the false-alarm rate, per review and over repeated reviews, at which they were obtained.

## Plain Language Summary

Glaucoma slowly damages side vision. Doctors use a visual-field test to see whether the damage is getting worse, and if it is, they may add eye drops, laser or surgery. Each test result varies from day to day, so doctors need several tests before they can be sure. Many new computer methods, including artificial intelligence, promise to spot worsening sooner. But a method can look better simply because it raises more false alarms. We first compared ten methods and measured their false alarms in patients who were tested every week for three months, when their glaucoma could not really have changed. We then repeated the comparison in more than 300 eyes, after adjusting every method so that it raised the same small number of false alarms. We did this by mixing up the order of each patient's tests in the clinic's own records. Once false alarms were matched, no method found more worsening than the simplest one, which draws a straight line through the average results. An artificial-intelligence method that seemed to find much more worsening did so mainly by raising many more false alarms. Methods that wait for a second confirming test raised fewer false alarms but found worsening later. New methods should say how many false alarms they raise before they are used to guide treatment.
