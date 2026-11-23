# Stakeholder review — glaucoma service manager / patient advocate

**Overall view:** The core message ("ask new progression tools how often they raise false alarms in eyes that did not change") is useful and easy to act on. But the paper tells clinics and patients that a simple trend line is "as good as" anything else, and that message understates how many worsening eyes the simple method misses. Some of the harm framing, and the advice to "run a shuffle audit", go beyond what the study showed.

## Summary

From a service and patient perspective there are three risks. First, the reassuring "simple is as good" message could make services complacent about the trend test missing most progression early on (it flags 19% at three tests, about 2.3 years in). Second, the per-review false-alarm numbers understate what a patient actually experiences over repeated visits. Third, the recommended shuffle audit would have wrongly penalised the event-type analysis that is already used in clinics. The plain-language summary also contains a factual error about the machine-learning methods.

## Issues

### 1. MAJOR — The reassuring headline hides the miss rate that matters to patients
**Location:** PLS: "The simplest method, which draws a straight line through the average results, worked as well as any method that kept false alarms low." Conclusion: "A plain trend test of mean sensitivity remained as good as any valid alternative."
**Problem:** In the paper's own data, the trend test flagged 19.2% of eyes that went on to progress at three tests (median about 2.3 years after the first test) and 57.7% at six tests (about 6.3 years). For a patient, "as good as anything else" can read as "the current method is fine". In fact it misses most worsening for years. The study was also too small to show that alternatives are *not* better (see Review 02, Issue 2).
**Fix:** In the PLS and the Conclusion, say plainly that all methods miss many worsening eyes early, that the simple method missed about 4 in 5 at the third test and 2 in 5 at the sixth, and that the study could not rule out moderately better methods.

### 2. MAJOR — False-alarm numbers are given per single review, so the burden on patients is understated
**Location:** "In clinical units, D1 raised about 44 false progression flags per 1,000 stable eyes at a review based on three tests." "At a false-alarm rate of 22.4%, a clinic reviewing 1,000 stable eyes would see about 224 false flags, compared with about 44 with the trend test."
**Problem:** Stable patients are reviewed at every visit, and each review is another chance of a false flag. The paper reports *cumulative* detection ("By the sixth test, D1 had flagged 69% of reference progressors") but only *per-review* false alarms. Managers planning capacity (extra confirmation tests, clinic slots) and patients worried about unnecessary treatment need the cumulative figure. Also, the numbers come from 30 early-glaucoma patients and are presented as if they applied to "stable eyes" in general.
**Fix:** Report the cumulative false-flag probability over reviews 3–6 for each method. Add a sentence saying that these rates come from patients with early damage and may be higher in advanced disease.

### 3. MAJOR — The paper implies that false flags lead directly to treatment, which overstates harm and could undermine trust in monitoring
**Location:** PLS: "A false alarm could lead to treatment that a patient does not need." Discussion: "For treatment decisions, these results matter in a direct way."
**Problem:** In a well-run service, a single flag leads to a repeat or confirmation test and a review of pressure and OCT, not straight to surgery. Writing as if false flags translate into unnecessary drops, laser or surgery may frighten patients and devalue the confirmation step the paper itself implies is needed. The study measured no treatment outcomes ("we did not measure the clinical consequences of false alarms").
**Fix:** Describe the realistic pathway: a false flag usually means extra tests and visits, and sometimes unnecessary escalation. Recommend confirmation testing as the safeguard. Change "in a direct way" to "indirectly".

### 4. MAJOR — The shuffle-audit recommendation would mislead services about the method many already use
**Location:** KSP: "Clinics and developers can check false alarms with a shuffle audit of their own records". PLS: "This check gave a fair estimate of the false-alarm rate." Discussion: "In our study, both identified the same invalid detectors."
**Problem:** In the results, the audit gave 11.7% false alarms for event analysis at six tests, against a true value of 1.9%. Event analysis is the type of method used in commercial perimeter software, and a service running the audit would wrongly conclude it is unsafe. The audit also gave 11.7% for the simple −1 dB/yr rate rule (true 2.6%), and it under-estimated the machine-learning model at three tests (17.3% vs 27.7%). The pre-set accuracy target was missed. The statement that the audit and the true no-change data "identified the same invalid detectors" is not correct: the audit would have flagged D2 at three tests and D7 at six tests, and would not have flagged D6 at six tests (4.9%).
**Fix:** Present the audit as a rough screen that can both over- and under-estimate, and give the event-analysis example explicitly. Remove "fair estimate" and "identified the same invalid detectors". Advise services not to drop an established method on the basis of an audit alone.

### 5. MODERATE — The PLS statement about machine learning is wrong
**Location:** PLS: "Methods that found more worsening, including two machine-learning methods, also gave many more false alarms."
**Problem:** One of the two machine-learning methods (the recurrent network, D9) found *less* worsening than the simple method at three, four and six tests. Patient-facing text must be accurate.
**Fix:** Change to "one machine-learning method".

### 6. MODERATE — The "better-timed testing" advice is a service-design recommendation that the study did not test
**Location:** "Faster confirmation of progression will more likely come from better-timed testing than from more aggressive analysis." "Practical ways to gain time are therefore more tests early in follow-up [34] or scheduling guided by risk [21, 35]".
**Problem:** Services may act on this. Front-loading tests has real capacity costs, and the study contains no analysis of test timing or frequency.
**Fix:** Present it as a hypothesis drawn from other literature, not as a conclusion of this study. Remove it from the Conclusions section.

### 7. MODERATE — Equity and generalisability are not discussed
**Location:** Data sources; Table 1.
**Problem:** The study uses a US tertiary dataset with no diagnoses, 30 Canadian volunteers and a Chinese cohort (median age 41, on a different machine). Sex, ethnicity and disease stage are not reported. A service manager cannot judge whether the results apply to their population, for example older patients with advanced disease, or patients with cataract, who generate more variable fields.
**Fix:** Report sex and stage. Add a paragraph on which patient groups the false-alarm rates are likely to under- or over-estimate.

### 8. MINOR — The terminology may confuse non-specialist readers
**Location:** "valid", "true no-change arm", "shuffle audit", "conformal".
**Fix:** In the PLS and KSPs, use "kept false alarms at an acceptable level" instead of "valid". Explain "retest study" once. Avoid "conformal" outside the Methods.

### 9. MINOR — Open resources are promised but not delivered
**Location:** "The code, the pre-specified protocol, the patient-level split, all raw detector outputs and the scripts ... are available at [PUBLIC REPOSITORY URL — to be added by the authors before submission]."
**Fix:** Deposit the material before publication. For a service, the value of the paper is the ability to run the benchmark and audit locally.
