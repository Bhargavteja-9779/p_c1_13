# Stakeholder review: practising glaucoma specialist and clinic manager

*Question: "What would I do differently on Monday?"*

## Summary
I run a busy glaucoma service. Most of my patients have one field a year, and my perimetry capacity is full. The paper tells me three things:

1. The trend analysis in my perimeter software (an MD or VFI trend with a p-value) is probably as good as anything fancier at 3–6 fields.
2. Vendor or AI tools that "detect progression earlier" may simply raise more alarms.
3. I could check a tool by shuffling my own patients' fields.

Messages 1 and 2 are reassuring and consistent with what I believed. Message 3 is not yet something I could actually run on Monday. Overall, the paper does not change what I do on Monday, but it could change what I ask vendors for.

## Recommendation (as a user of the evidence)
**Major revision** before I would quote it in a business case or a clinical governance meeting.

## Issues

1. **MAJOR – I cannot act on "per-opportunity" false alarms.**
   - *Location:* Table 3; Results, Real-world measures.
   - *Problem:* "44 false flags per 1,000 stable eyes" per look does not tell me how many extra escalation discussions, extra fields or extra drops a tool causes in my clinic per year. Patients are reviewed repeatedly, so false alarms accumulate.
   - *Fix:* Give the cumulative chance that a truly stable patient is flagged at least once over 3–6 fields (estimable from the Artes windows). Translate it into flags per 1,000 patients per year at one and two fields per year.

2. **MAJOR – The "shuffle audit" is not usable as described.**
   - *Location:* Discussion paragraph 4 ("the clinic can run the shuffle audit on its own records").
   - *Problem:* Commercial tools do not let me feed in re-ordered fields with the original dates. I would need an export, a script and a statistician. The paper also gives no cut-off: what audit rate means "don't buy"? And the audit got several detectors wrong (it flagged event analysis and the rate rule, which were fine, and missed D6 at six tests).
   - *Fix:* Provide a step-by-step protocol, a decision threshold with its error rates, and a downloadable tool or an R/Python function. Say which vendors' exports it works with.

3. **MAJOR – The practical alternative (more early fields) is asserted, not shown.**
   - *Location:* Discussion ("More frequent early testing … is likely to help more").
   - *Problem:* This is the decision that actually costs me money. Booking two fields per visit in the first two years doubles perimetry demand.
   - *Fix:* Simulate, with the Artes noise and the UW series, how much earlier D1 detects progression at 2 fields per year vs 1, and the false-alarm cost of each.

4. **MODERATE – A clinician does not act on one flag.**
   - *Location:* Detectors; Real-world measures.
   - *Problem:* In practice, a suspected progression triggers a repeat field before escalation. If D1 + confirmation gives very few false escalations, that is my Monday protocol. The paper does not test confirmation strategies.
   - *Fix:* Add "flag confirmed on the next field" as a rule for D1 and D8, and report its sensitivity, delay and false-escalation rate.

5. **MODERATE – My software uses MD/VFI, not "mean sensitivity".**
   - *Location:* D1/D2.
   - *Problem:* Is D1 the same as the HFA Guided Progression Analysis MD or VFI rate with p < 0.05? If not, how close is it?
   - *Fix:* Add one sentence mapping each detector to what clinicians see in standard reports.

6. **MODERATE – Generalisability to my patients.**
   - *Location:* Results, Study sample.
   - *Problem:* The reference eyes had about 13 years of annual follow-up and early disease. The no-change arm is 30 Canadian patients. I need to know whether the message holds for advanced disease, where false alarms and missed progression both matter most.
   - *Fix:* Show results by baseline severity, even if only descriptively.

7. **MINOR – What should I ask a vendor?**
   - *Location:* Conclusions.
   - *Problem:* The conclusion recommends evaluation "on true no-change data or with a shuffle audit", but gives no checklist.
   - *Fix:* Add a box: "Questions to ask before adopting a progression tool". For example:
     - What is its false-alarm rate on test–retest data?
     - At how many fields?
     - With what confirmation rule?
     - Was the threshold set on stable eyes chosen by the same criterion as the outcome?

## What I would do on Monday (if the revised paper confirms the findings)
- Keep using the standard MD/VFI trend with a p-value as my primary trigger, and require confirmation on a repeat field before escalating on an early flag.
- Ask any vendor of an AI progression tool for false-alarm data on test–retest series before purchase.
- Not change test frequency on the basis of this paper alone, because the frontloading recommendation is not analysed here.
