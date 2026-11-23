# Stakeholder review — clinician and patient perspectives

Manuscript: *Detecting Glaucomatous Visual Field Progression From Few Tests Without False Alarms: An Open Benchmark With a True No-Change Arm*

Two short perspectives, written as the intended readers would react. Numbers quoted were checked against `tables/table2_main.csv`, `tables/table3_grape.csv`, `results/descriptives.json` and `results/statistics.json`.

---

## (a) Consultant glaucoma specialist running a busy clinic

### Summary

The message I take away is: "don't trust a new progression algorithm's flag until someone has shown its false-alarm rate on stable patients; the trend line you already have is calibrated; and you will only detect earlier if you test more often." I agree with that, and it is useful. But the paper does not tell me what to do differently on Monday. Parts of the summary could be read as "the trend test is good enough", which is not what the numbers say.

### Issues

**1. MAJOR — "Strong default" reads as reassurance the data do not give.**
- *Location:* Abstract Conclusion ("a simple trend test remains a strong default"); Key Summary Points ("the evidence does not support replacing it in routine care").
- *Problem:* At three fields the trend test caught 19% of eyes that went on to progress, and at six fields 58% (Table 2). Among progressors it took a median of 5 fields, ≈ 5 years at this clinic's spacing, to flag, and 31% were still unflagged at six fields (`descriptives.json`). In practice "strong default" means "I will miss most early progressors". The honest message is "well-calibrated but slow".
- *Fix:* Replace "strong" with "well-calibrated". Add a sentence to the Key Summary Points saying that no detector, including the trend test, reliably detects progression from three or four fields at the testing frequencies seen here.

**2. MAJOR — The tools I actually use are not tested.**
- *Location:* Methods, Detectors (D7 "similar in spirit to Guided Progression Analysis"); Introduction.
- *Problem:* My decisions rest on the perimeter's own event and trend analyses (and increasingly on vendor or commercial AI). D7 is a research re-implementation, and none of the commercial or published AI products cited is evaluated. The "new detectors" being warned about are the authors' own models. I cannot tell from this paper whether the product a vendor is selling me has a valid false-alarm rate.
- *Fix:* State plainly in the Discussion and Key Summary Points that commercial and published detectors were not tested. Give a concrete ask for vendors and journals: report the false-alarm rate on a public no-change data set such as the Artes series, by number of fields.

**3. MODERATE — The shuffle audit is not something my clinic can do.**
- *Location:* Key Summary Points ("a shuffle audit of a clinic's own records is a cheap first check").
- *Problem:* I cannot re-order fields in the perimeter software, and I do not have an analyst. "Cheap" assumes data export, code and statistical support. The audit also gave misleading results for some rules (e.g. the MD-rate rule: 11.7% audit versus 2.6% true at three fields).
- *Fix:* Reword it as a check that "vendors, researchers or clinics with data-analysis support" can run, and say what output to ask a vendor for.

**4. MODERATE — No guidance on confirmation.**
- *Problem:* In real practice I repeat a field before escalating. The paper's flags are single-review flags. I want to know how many false flags survive one confirmation field, and how much delay confirmation adds. Table 2 hints that many three-field flags do not persist (D6 sensitivity drops from 57% to 25% at four fields).
- *Fix:* Add a "flag confirmed at the next field" analysis and one sentence of practical guidance.

**5. MINOR — The escalation framing is overstated.**
- *Location:* Introduction ("A false alarm can lead to unnecessary escalation, with extra drops, laser or surgery").
- *Problem:* A single algorithm flag rarely leads directly to surgery. The more realistic cost is extra visits, extra fields and patient anxiety.
- *Fix:* Soften to "can prompt extra testing and, if not recognised, unnecessary escalation".

**Clinician verdict:** Useful and credible as a warning to developers and journals. The summary needs to be more candid that early detection from sparse fields is poor with *every* method, and more practical about what a clinic can do.

---

## (b) Patient with glaucoma reading the Key Summary Points and plain-language framing

### Summary

I understood that computers or tests sometimes say my eyesight is getting worse when it is not, and that some newer methods do this a lot. That part is clear and reassuring: my doctor should not change my treatment because of one result alone. But I had to work hard at the wording. I could also come away with the wrong idea that "no change" on my test means I am fine.

### Issues

**1. MAJOR — Missing the most important patient message: a "no progression" result after a few tests is not reassurance.**
- *Location:* Key Summary Points, "What was learned".
- *Problem:* The points stress false alarms (being told I am worse when I am not). They say nothing about the opposite: with three tests the standard method picked up fewer than 1 in 5 people who were really getting worse (19%, Table 2). As a patient, missed worsening is what I fear most. Read alone, the summary might make me less willing to have extra or more frequent tests.
- *Fix:* Add a Key Summary Point such as: "With only three or four field tests, every method missed most eyes that were truly getting worse; more frequent testing early in follow-up is likely to matter more than which method is used to analyse the tests."

**2. MODERATE — Jargon makes the summary hard to follow.**
- *Location:* Key Summary Points.
- *Problem:* "Detectors", "future-confirmed progression", "true no-change data", "nominal 5%", "valid false-alarm rate" and "shuffle audit" are not explained. I did not know what "fields" are (visual field tests) or why weekly testing in 30 people means "no change".
- *Fix:* The journal allows an optional plain-language summary of up to 250 words (`selected_journal.md`), and none is provided. Write one using everyday terms: "visual field test (the test where you press a button when you see a light)", "methods that read a series of tests", and "people tested every week for 12 weeks, when their eyes could not have really changed".

**3. MODERATE — Percentages without a reference frame.**
- *Problem:* "22.4% and 27.7% of true no-change series" does not tell me what would happen to someone like me. "Out of 100 people whose eyes are stable, about 4 would be wrongly flagged by the standard method at one check, and about 22–28 by the two worst methods" is clearer, and it matches the paper's own per-1,000 figures (44, 224 and 277 per 1,000).
- *Fix:* Use "out of 100 people" framing in the plain-language summary.

**4. MINOR — Possible worry about AI.**
- *Problem:* The summary could read as "AI is bad at this". The authors' own Discussion is more balanced ("This does not mean that machine learning cannot help").
- *Fix:* Carry that balanced sentence into the plain-language summary.

**Patient verdict:** Not misleading about false alarms, but incomplete in a way that matters to patients. Add the "missed worsening / test more often" message and a plain-language summary.

---

## Overall recommendation (stakeholder panel)

**Minor-to-major revision of the summary material.** The Key Summary Points need (i) the correction raised by other reviewers (the "two detectors that flagged the most progressors" statement is wrong: the MD-rate rule flagged 38% at three fields with a valid false-alarm rate), (ii) a balancing point about low sensitivity of all methods with few fields, and (iii) "well-calibrated" in place of "strong default". A plain-language summary should be added.
