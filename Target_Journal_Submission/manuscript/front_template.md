# How Early Can Glaucomatous Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm

**Article type:** Original Research

**Authors:** [AUTHOR NAMES, DEGREES — to be completed by the authors]

**Affiliations:** [INSTITUTION, CITY, COUNTRY — to be completed by the authors]

**Corresponding author:** [NAME, FULL POSTAL ADDRESS, EMAIL — to be completed by the authors]

**ORCID iDs:** [to be completed by the authors]

**Prior presentation:** [TO BE CONFIRMED BY THE AUTHORS: none.]

## Abstract

**Introduction:** New methods for detecting glaucomatous visual-field progression often claim earlier detection. Their false-alarm rates are rarely measured on series in which no change occurred. We asked whether any detector finds more progression than a simple trend test of mean sensitivity while keeping false alarms at the nominal 5%.

**Methods:** Ten detectors (trend, pointwise, permutation, conformal, event-based and machine-learning), specified before the final analysis, used only the first 3–6 tests of each series. We measured sensitivity and specificity against a future-confirmed reference in held-out eyes of the University of Washington data set ({{d:ref_progressors.n_eyes:int}} progressing, {{d:ref_stable.n_eyes:int}} stable eyes); false alarms on retest series of {{d:artes.n_patients:int}} patients with glaucoma tested about weekly for 3 months; and agreement with progression labels in an external clinic ({{d:grape.n_eyes:int}} eyes). We also tested whether re-running detectors on shuffled test orders (a "shuffle audit") estimates the true false-alarm rate.

**Results:** At three tests, the trend test detected {{p:sens:D1:3}} of progressing eyes with a false-alarm rate of {{p:fpr_true_null:D1:3}}. The only significantly more sensitive detector, a pooled-detrended conformal test (sensitivity {{p:sens:D6:3}}), had a false-alarm rate of {{p:fpr_true_null:D6:3}}. Gradient-boosted trees thresholded at 95% specificity had false-alarm rates of {{p:fpr_true_null:D8:3}} at three tests and {{p:fpr_true_null:D8:5}} at five. No detector with a valid false-alarm rate was significantly more sensitive than the trend test, but only gains of {{x:mdd_pp}} percentage points or more could reach significance. Across four repeated looks, event analysis flagged {{x:cum:D7}} of no-change series, versus {{x:cum:D1}} for the trend test. The shuffle audit was within 3 percentage points of true false-alarm rates in {{s:share_within_3pp:pct}} of cells (Spearman ρ = {{s:spearman_rho:2}}, below the pre-specified 0.70).

**Conclusion:** Apparent gains in early detection of visual-field progression can be false alarms that conventional specificity estimates miss. New detectors should report false alarms on true no-change data, including over repeated looks, before they guide treatment escalation.

## Keywords

Benchmark; False alarms; Glaucoma; Machine learning; Perimetry; Progression; Specificity; Visual field

## Key Summary Points

**Why carry out this study?**

- Escalating glaucoma treatment depends on detecting visual-field progression, but each test is noisy and several tests are needed, which delays decisions.
- Many new detectors claim earlier detection, yet their false-alarm rates are seldom measured on data in which the disease did not change.
- We hypothesised that no detector would flag substantially more progressing eyes than a simple trend test of mean sensitivity while keeping a valid false-alarm rate.

**What was learned from the study?**

- Across ten detectors and 3–6 tests, the only detector that flagged significantly more progressing eyes than the trend test had a false-alarm rate of {{p:fpr_true_null:D6:3}}, and a machine-learning model thresholded at 95% specificity reached {{p:fpr_true_null:D8:3}}, although specificity against stable reference eyes looked high for all detectors.
- Claims of earlier detection should be accompanied by false-alarm rates on true no-change data, including over repeated looks; a shuffle audit of routine records is a useful but imperfect screening check.

## Plain Language Summary

Glaucoma slowly damages side vision. Doctors use a visual-field test to see if the damage is getting worse. If it is, they may add eye drops, laser or surgery. Each test result varies from day to day, so doctors need several tests before they can be sure. This can take years. Many new computer methods promise to spot worsening sooner. But a method can look better simply because it raises more false alarms. A false alarm could lead to extra tests or treatment that a patient does not need. We tested ten methods on records from three sources. One source had patients tested about every week for three months, when their glaucoma could not really have changed. Any alarm in these patients was false. No method that kept false alarms low found clearly more worsening than the simplest method, which draws a straight line through the average results. The method that found the most worsening early also raised a false alarm in about one in five patients whose eyes had not changed. A method that waits for the change to be confirmed on a second test raised the fewest false alarms over repeated tests. We also tried a simple check that any clinic can run on its own records: mixing up the order of each patient's tests and seeing how often a method still raises an alarm. This check caught the worst methods but was not exact. New methods should report their false alarms before they are used to change treatment.
