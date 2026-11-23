# Stakeholder review: "How Early Can Glaucoma Visual-Field Progression Be Detected Without False Alarms?"

Reviewed file: `manuscript/manuscript_filled.md` (with `tables/table1_main.md`, `table2_grape.md`, `table3_realworld.md`, `table_paired_tests_vs_D1.csv`).
Perspective: non-methodological readers who would use or be affected by the findings. Every number quoted below is taken from the manuscript or its tables; nothing here is new data.

Severity tags: **FATAL** (message is wrong or unsafe as written), **MAJOR** (likely to mislead a stakeholder or blocks practical use), **MODERATE** (confusing or incomplete, but recoverable), **MINOR** (wording/presentation).

No FATAL issues were found. The central message (no detector that kept its false-alarm rate under control beat the simple trend test, and the usual check on stable eyes missed false alarms) follows from Tables 1–3. The problems are about how the message reaches people outside methods research: how it is framed, translated and bounded.

---

## Cross-cutting issues (affect all three stakeholders)

**X1. MAJOR: "Valid" sounds like "clinically validated".** In the tables and text, "valid" means only "the 95% CI of the no-change false-alarm rate has upper limit <= 10% and lower limit <= 5%". A clinic lead or payer reading "Valid: Yes" next to D2 or D8 (6 tests) may take it as an endorsement. Under this rule a detector with a true false-alarm rate near 9% per review could still be "valid".
*Fix:* Rename the column and term, e.g. "False alarms within target (Yes/No)". Define it in plain words at first use and in every table footnote. Add one sentence saying that passing this check is necessary, not sufficient, for clinical use.

**X2. MAJOR: The benefit is counted cumulatively but the harm is counted per review.** Table 3 counts a progressor as "flagged by test k" if *any* review from 3 to k flagged it. False flags are given *per single review* ("per 1,000 no-change eyes at test 3 / 4 / 5 / 6"). In practice a stable patient is reviewed at every visit, so false alarms add up over time just as detections do. The only cumulative false-alarm measure ("stable eyes ever flagged", exploratory) uses the 26 reference-stable eyes. The manuscript itself says these eyes are selected for a flat course and give optimistic specificity.
*Fix:* Using the Artes series (12 tests each), report the share of no-change series flagged at least once over reviews 3–6, per detector, with CI. Put it next to "progressors flagged by test 4/5/6" so both sides use the same unit. If that is not possible, state the asymmetry explicitly in the Table 3 footnote and the Real-World Measures text.

**X3. MAJOR: "Not significantly better" is easy to read as "proven no better".** The abstract, Key Summary Points and Conclusions say that no valid detector flagged significantly more progressors. The comparison rests on 26 progressors. The CIs allow gains of about 20 percentage points (D2 at 3 tests: +19.2 pp, 95% CI 0.0 to 42.3; D8 at 6 tests: +11.5 pp, CI −7.7 to 30.8). The Results and Limitations sections say this, but the abstract and Key Points do not. A vendor, payer or clinic could quote the paper as showing that new software has no added value.
*Fix:* Add to the abstract Conclusion and to the Key Points: "the study was small, and gains of 10–20 percentage points for some detectors cannot be excluded." Avoid "explained by false alarms" in the abstract Conclusion. That wording fits D6 and D8 at 3 tests, not every apparent gain; D8 at 6 tests was within target and had a point gain. Suggested wording: "the largest apparent early-detection gains came with false alarms that only a true no-change check revealed".

**X4. MODERATE: The abstract does not name the detector, so readers may blame "conformal" methods in general.** The abstract says "A pooled conformal detector flagged 56.9% ... but raised false alarms on 22.4%". This is D6 (pooled-*detrended* conformal). D5 (pooled-*shuffle* conformal) was within target and matched D1 in both data sets. Readers may conclude that conformal methods as a class are unsafe.
*Fix:* In the abstract, say "a pooled-detrended conformal detector". Add a clause noting that a simpler pooled conformal test (D5) kept its false-alarm rate near target.

**X5. MODERATE: Sensitivity gains in the text do not match the table differences.** The abstract and Results give D6 at 3 tests as 56.9% vs 19.2%, "+38.5 percentage points", but 56.9 − 19.2 = 37.7. Similar cases: D8 at 6 tests, 70.8 vs 57.7 ("+11.5", arithmetic 13.1); GRAPE D8 at 3 tests, 65.9 vs 44.4 ("+25.9", arithmetic 21.5). `table_paired_tests_vs_D1.csv` suggests that the paired McNemar differences come from a single realisation of the stochastic detectors, while the reported sensitivities are means over 5 seeds. Non-statistical readers will think the paper has arithmetic errors.
*Fix:* State in Methods/Statistical Analysis which seed or realisation the paired tests use. Or report the paired difference averaged over seeds so that the two numbers agree. Add a footnote to Tables 1–2.

**X6. MODERATE: Inconsistent names for the default method.** D1 is called "OLS-MD" but is defined as the slope of *mean sensitivity*. The reference standard uses *mean total deviation*. Clinicians know "MD" as the Humphrey mean deviation and "VFI/MD trend" from commercial printouts. A clinic lead cannot tell whether D1 is what their perimeter software already shows.
*Fix:* Use one name, e.g. "MS trend (D1)". Add a sentence on how D1 relates (or does not) to the MD/VFI trend shown by commercial perimeter software. Do not claim equivalence unless it is shown.

**X7. MODERATE: Plain-language translation is missing.** Terms such as detector, nominal 5% level, sensitivity, specificity, shuffle audit, reference-stable, conformal, Holm-adjusted are not explained for non-specialists. The journal's Key Summary Points also use jargon ("trend of mean sensitivity", "valid false-alarm rate").
*Fix:* Add the plain-language summary drafted at the end of this review (or similar). Add a short glossary box (5–8 terms).

**X8. MINOR: Borderline "invalid" case shown with a rounded CI.** D9 at 6 tests is labelled invalid with a CI of 2.3–10.0%. The rule says "did not exceed 10%", so readers will think the label is wrong. The text says it "failed the rule only narrowly".
*Fix:* Show one more decimal for borderline CIs, or footnote the unrounded upper limit.

---

## Viewpoint 1: A glaucoma patient who has a visual-field test every year

### Is the problem real and important to them?
Yes. A patient wants two things that pull against each other: worsening caught early, before it costs sight, and no unnecessary extra drops, laser or surgery. The paper is about exactly this trade-off. Its most useful finding for a patient is one the paper understates: with yearly tests, the standard trend test flagged only 19.2% of eyes that were truly getting worse after three tests, and needed a median of 5 tests (about 5 years of yearly testing, per the stated 1.0-year median interval) to flag half of them (Table 3).

### Is the practical message clear and correct?
Partly. The paper tells clinicians and developers what to do. It does not tell patients what this means for them. The message as written ("the simple trend test was hard to beat") is correct for its data, but it may falsely reassure a patient: the default is safe from false alarms *and slow*.

### Points

**P1. MAJOR: The slowness of detection is the patient-relevant result, but it sits in the Discussion.** The fact that most worsening is not confirmed for several years of yearly testing, with any detector that kept false alarms under control, is the outcome patients and advocacy groups care about most. The manuscript links this to front-loading/clustering tests [5, 36] only in one Discussion sentence.
*Fix:* Add a Key Summary Point along these lines: "With about one test per year, even the best-behaved method took a median of 5 tests to flag eyes that were truly getting worse; how often patients are tested may matter more than which software is used." Frame the second half as an inference from cited work, not a result of this study.

**P2. MAJOR: "Front-loading or clustering tests ... is likely to help more than a more complex detector" is not tested here.** A patient group could use this sentence to demand more frequent testing. A payer could use the rest of the paper to refuse new software. Neither is directly supported: the benchmark did not vary test frequency.
*Fix:* Change to "may help more; this study did not test different testing schedules". Cite [5, 34–36] as the evidence base.

**P3. MODERATE: What a "flag" means for the patient is not explained.** Patients could read "false alarm" as "wrong diagnosis" or "unnecessary surgery". In practice, a progression flag usually leads to a clinician review and often a confirmatory test before treatment is escalated. The manuscript equates a flag with an "unnecessary escalation discussion" without discussing confirmation testing. Confirmation would reduce the harm of a false flag and delay a true one.
*Fix:* Add a Discussion paragraph: what a flag triggers in routine care, and that the results are for single-review flags without confirmation. Recommend future work on confirmed flags. Do not quote confirmation rates that are not in the data.

**P4. MODERATE: Who the results apply to.** The reference eyes had a median MD of −4.4 dB at first test (early/moderate damage), median age 58.8. Patients with advanced damage, where test noise is larger (stated in the Introduction), may see different false-alarm behaviour. The no-change arm is 30 patients from one centre.
*Fix:* One sentence in Limitations naming the disease stage covered and stating that advanced-disease performance is not known.

**P5. MINOR: Harms are described only one way.** The Introduction lists the harms of false alarms (extra drops, laser, surgery, side effects, costs). The harm of missed or late progression (irreversible loss) is mentioned only via [7].
*Fix:* Present both harms side by side in one sentence so the paper does not read as "fewer alarms is always better".

### What could be misread or misused (patient view)
- "Simple test is best" read as "my current care catches worsening early". It does not (P1).
- "AI raised false alarms" read as "AI-assisted glaucoma care is dangerous". The finding is specific to the usual threshold rule on short series; D8 at 6 tests stayed within target (X3, X4).

---

## Viewpoint 2: A busy NHS/US glaucoma clinic lead deciding whether to adopt progression-detection software

### Is the problem real and important to them?
Yes. This is the paper's strongest audience. Vendors and academic groups market "earlier detection", and a clinic lead usually sees only sensitivity and specificity on stable eyes. The finding that this check missed 5.0–6.3-fold excess false alarms (D6, D8 at 3 tests) is directly useful for procurement.

### Is the practical message clear and correct?
The Discussion's "What should a clinic do?" paragraph is clear and correctly hedged. Three gaps stop a clinic lead from acting on it.

### Points

**C1. MAJOR: No commercial product was tested, but the paper will be cited in procurement.** Event analysis (D7) is a re-implementation "similar in spirit to Guided Progression Analysis". Limitations state that commercial software was not tested. A clinic lead skimming the abstract could take the results as applying to GPA, or to a specific AI product.
*Fix:* Add to the abstract Methods or Conclusion: "No commercial software was evaluated." In the Discussion, say the results do not rate any named product. They give a checklist of evidence to ask vendors for.

**C2. MAJOR: No positive predictive value, so "what fraction of flags are real" is unanswered.** A clinic lead needs to know, of the eyes flagged, how many are truly progressing. This depends on how common progression is in their population. The 26/26 balanced reference set cannot give it, and nobody should compute PPV from it.
*Fix:* Either report flag rates and PPV across the whole UWHVF test set (including the 80 indeterminate eyes, stated as such), or give PPV over a stated range of assumed prevalences using the no-change false-alarm rates and the sensitivities. State that the balanced 26/26 design is not a prevalence estimate.

**C3. MAJOR: Procurement-ready checklist missing.** The paper's three reporting items for developers are good, but they are aimed at developers, not buyers.
*Fix:* Add a short box, "Questions to ask before adopting a progression detector": (a) false-alarm rate on true short-interval retest (no-change) data, at the number of tests your patients typically have; (b) sensitivity at a fixed, small number of tests; (c) results in a second clinic/perimeter; (d) how the threshold was set (on stable eyes vs no-change data); (e) whether it was compared head-to-head with a simple MD/MS trend. All five are already supported by the manuscript's findings.

**C4. MODERATE: The shuffle audit is recommended but not operational.** "Any clinic can run on its own records" assumes analytical staff and the vendor's algorithm being runnable offline. Most proprietary software cannot be re-run on shuffled series. The audit over-estimated false alarms for rate and event rules (D2: 11.7% vs 2.6%; D7 at 6 tests: 11.7% vs 1.9%), so a clinic could wrongly reject a good rule. Agreement missed the pre-registered target (ρ 0.65 vs ≥ 0.7).
*Fix:* State the practical preconditions (access to raw series and the ability to run the detector). Point to the open code as a worked example. Give a decision rule for reading audit results, e.g. "a large excess over 5% is a warning sign; a modest excess for rate or event rules may be an artefact of the audit".

**C5. MODERATE: Units are mixed: tests, years and reviews.** Table 3 works in tests and states that one test is about one year in UWHVF. GRAPE test intervals are not reported in the manuscript, and NHS/US intervals vary. "False flags per 1,000 no-change eyes at test 3" is per review, not per year or per patient lifetime.
*Fix:* Add a "years since first test" column to Table 3 (UWHVF, from the stated 1.0-year median interval, labelled approximate). Report the GRAPE median test interval. Note that the per-1,000 figures are per review.

**C6. MODERATE: "Unnecessary escalation discussions" overstates the consequence.** The Results say "roughly 224 and 277 unnecessary escalation discussions instead of 44" per 1,000 stable eyes. That holds only if every flag leads to a discussion. It also applies only at the three-test review: at four tests D6 drops to 51 per 1,000.
*Fix:* Write "224 and 277 false progression flags instead of 44 at the three-test review". Add that clinician review or confirmatory testing would turn only some of these into escalation discussions.

**C7. MODERATE: Generalisability to NHS practice.** The data come from Seattle (USA), Halifax (Canada) and Hangzhou (China). There are no UK/NHS data, no reliability indices (UWHVF) and a different perimeter in GRAPE (not named in the manuscript). The GRAPE comparison is with rule-based labels (mean-deviation criterion), yet the text calls them "clinicians' labels".
*Fix:* Name the GRAPE perimeter if the source paper reports it (mark UNVERIFIED if not checked). Replace "clinicians' labels" with "the data set's mean-deviation progression labels". Add a sentence that unreliable fields were not excluded in UWHVF because reliability indices are unavailable, which may inflate noise relative to clinics that screen reliability.

**C8. MINOR: The "default" recommendation needs a pointer for adopters.** "The trend of mean sensitivity, with a p-value, remains a sound default." State the exact rule used (one-sided OLS slope, p < 0.05, blind spot removed, first k tests), so a clinic can check whether its current software does the same.

### What could be misread or misused (clinic view)
- Using "Valid: Yes" as a quality mark for D2 or D8 (X1). In GRAPE, D2 and D8 both had significantly more false positives than D1 (+16.5 and +33.5 pp at 3 tests).
- Vendors citing D5/D7 "matched D1" as evidence for a commercial event- or conformal-based product (C1).
- Rejecting all ML tools; D8 at 6 tests stayed within target (X3).

---

## Viewpoint 3: A health-system payer/manager concerned with capacity and costs

### Is the problem real and important to them?
Yes. Glaucoma follow-up is a large, recurring workload. A detector that raises false flags creates extra visits, tests, clinician time and possibly treatment. A detector that misses progression creates later, costlier sight loss. The manuscript identifies both pressures but quantifies neither in resource terms.

### Is the practical message clear and correct?
A payer would take home two messages: "don't pay for new software without no-change evidence" (reasonable and supported) and "the free simple method is as good" (only partly supported, see X3). The paper gives no capacity or cost figures. That is acceptable for a benchmark, but it should be said explicitly.

### Points

**M1. MAJOR: The paper does not show any cost or capacity impact, and should say so.** The Introduction asserts that false alarms lead to "extra drops, laser or surgery and their side effects and costs". The Real-World Measures turn rates into flags per 1,000 eyes, which a manager will multiply by caseload to get workload or savings. No data on what follows a flag (extra visits, confirmatory tests, treatment changes) were collected.
*Fix:* Add a Limitations sentence: "We did not measure the downstream clinical actions, workload or costs that follow a flag; the per-1,000 figures are flag counts, not resource estimates." Suggest a decision-analytic or service-evaluation study as future work.

**M2. MAJOR: The paper's two implicit service messages conflict.** "Keep the simple trend test" seems cheap. But the evidence that it is slow (median 5 tests) and the suggestion to front-load or cluster tests point towards *more* perimetry early in follow-up, which costs capacity. A manager may adopt the first message and drop the second.
*Fix:* In the Discussion/Conclusion, state both together: the choice of detector did not buy earlier detection safely in this benchmark. Earlier detection probably needs more information per patient early on (e.g. more tests), which has capacity costs that were not studied here.

**M3. MODERATE: Per-review, per-1,000 figures do not scale up to a service.** See X2 and C5. A payer needs "false flags per 1,000 patients per year of follow-up" and "missed or late progressors per 1,000 patients". The paper gives single-review false flags and cumulative detection for 26 eyes.
*Fix:* Report cumulative no-change false flags over reviews 3–6 (X2). Express both columns per 1,000 eyes over roughly the same follow-up period. Mark any year conversion as approximate.

**M4. MODERATE: Low numbers in the external validation.** GRAPE had 27 progressors at 3 tests and 18 at 4, and the reference set had 26 + 26. A payer might over-read the external-clinic false-positive differences, which are precise because they are based on 236 and 145 non-progressors, alongside sensitivity gains, which are imprecise.
*Fix:* In the GRAPE paragraph and Table 2, state plainly that the false-positive differences are well estimated and the sensitivity differences are not.

**M5. MINOR: The recommendation to require no-change evidence has an implementation cost.** True short-interval retest data are scarce (30 patients here). Requiring them before procurement is reasonable, but the paper should say how they could be obtained, e.g. the open benchmark, or pooled retest studies such as the cited frontloading work [36], without claiming such data already exist for any product.
*Fix:* One sentence in the Discussion on how buyers or regulators could get no-change evidence (open benchmark submission).

### What could be misread or misused (payer view)
- "Simple trend test is enough, so no need to invest in progression tools or more testing". This omits the slowness finding (M2, P1).
- Multiplying 224/277 per 1,000 by caseload to claim savings or harms. These are single-review flag counts on a 30-patient retest sample, not costed events (M1, C6).
- Treating the absence of a significant sensitivity gain as proof of no value (X3).

---

## Summary table of points

| ID | Stakeholder | Severity | Issue (short) |
|---|---|---|---|
| X1 | All | MAJOR | "Valid" reads as clinically validated |
| X2 | All | MAJOR | Benefit cumulative, harm per review |
| X3 | All | MAJOR | Non-significance read as equivalence; abstract omits wide CIs |
| X4 | All | MODERATE | Abstract does not name D6; conformal methods blamed as a class |
| X5 | All | MODERATE | Paired differences don't match table differences (seed issue) |
| X6 | All | MODERATE | OLS-MD vs mean sensitivity vs MD naming |
| X7 | All | MODERATE | No plain-language summary or glossary |
| X8 | All | MINOR | D9 at 6 tests: rounded CI vs "invalid" |
| P1 | Patient | MAJOR | Slow detection (median 5 tests) buried |
| P2 | Patient | MAJOR | Front-loading claim not tested here |
| P3 | Patient | MODERATE | What a flag means; confirmation testing not discussed |
| P4 | Patient | MODERATE | Disease-stage applicability |
| P5 | Patient | MINOR | Harms of late detection under-stated |
| C1 | Clinic | MAJOR | No commercial software tested; say so prominently |
| C2 | Clinic | MAJOR | No PPV / prevalence context |
| C3 | Clinic | MAJOR | No buyer checklist |
| C4 | Clinic | MODERATE | Shuffle audit not operational; biased for rate/event rules |
| C5 | Clinic | MODERATE | Tests vs years vs reviews; GRAPE interval missing |
| C6 | Clinic | MODERATE | "Escalation discussions" overstates; 3-test review only |
| C7 | Clinic | MODERATE | NHS generalisability; "clinicians' labels" wording |
| C8 | Clinic | MINOR | Spell out the default rule |
| M1 | Payer | MAJOR | No cost/capacity data; say so |
| M2 | Payer | MAJOR | "Simple software" vs "more testing" tension |
| M3 | Payer | MODERATE | Figures not scalable to service units |
| M4 | Payer | MODERATE | Precision differs for sensitivity vs false positives in GRAPE |
| M5 | Payer | MINOR | How to obtain no-change evidence |

---

## Draft plain-language summary (for the authors to add; about 245 words; every number appears in the manuscript)

> **Plain-language summary**
>
> Glaucoma slowly damages side vision, and the damage cannot be undone. Most people with glaucoma have a visual-field test about once a year. Doctors look at the series of results to decide whether vision is getting worse and treatment should be stepped up. Each test is noisy, so real worsening is hard to tell apart from normal ups and downs.
>
> Many new computer methods, including machine learning, claim to spot worsening earlier. We compared ten methods using public data from Seattle (USA) and Hangzhou (China). We also tested them on 30 patients who had a test every week for 12 weeks. Glaucoma does not change measurably in 12 weeks, so any "worsening" alarm in these patients is a false alarm.
>
> After three tests, the simplest method, a trend line through the overall results, gave 44 false alarms per 1,000 checks. Two newer methods found more eyes that later truly got worse, but gave 224 and 277 false alarms per 1,000 checks. The usual way of checking new methods did not reveal this.
>
> No method that kept its false alarms low clearly beat the simple trend line. But all methods were slow: with yearly tests, the trend line needed a median of 5 tests to pick up eyes that were truly getting worse. The study was small, so modest benefits of newer methods cannot be ruled out. New "early warning" software should be tested on people whose vision is known not to have changed before it guides treatment.
