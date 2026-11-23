# Response to internal adversarial reviews (2026-11-23)

Status key: DONE = changed in manuscript/code; PARTLY = addressed in text, analysis not fully redone; OPEN = not done.

| ID | Status | Action taken |
|---|---|---|
| I01 validity rule | DONE | Three readings reported (significantly above 5% / draft rule / strict); conclusions based on "significantly above 5%" (lower CI > 5%), which D6 k3, D8 k3-5, D9 k3 meet under every reading; timing of draft rule after the pipeline check disclosed (Methods, S2). Table 1 shows all three. |
| I02 D6 known from development | DONE | Methods: D5, D6, D10 are own development variants; D6 included as pre-specified example of over-sensitive detector. Discussion: "illustration rather than an independent discovery". General claim narrowed to "every significant gain in this benchmark". |
| I03 reference circularity | DONE (post hoc) | Methods state built-in specificity; post hoc future-only reference (Table S3): D6/D8 specificity falls below D1 at k=3. Discussion rewritten: full-series specificity is not evidence of low false alarms. Note: future-only progressor counts are very small (17, 14, 6, 5). |
| I09 GRAPE labels/overlap | DONE (post hoc) | Labels renamed "criterion labels supplied with the data set" (text, legends, Fig. 1/4 relabelled); restriction to eyes with >= k+2 visits and PLR2/PLR3/any labels in Table S4; pattern unchanged (D8 k3: higher sensitivity, much lower specificity). |
| I04 power | DONE | Minimum detectable difference (9 discordant eyes, ~35 pp) stated in Methods/Results/Abstract; RQ2 framed as estimation. |
| I05 clustering | DONE/PARTLY | Paired-difference CIs now patient-cluster bootstrap (summarise.py); McNemar independence stated as limitation. |
| I06 degenerate CIs | DONE | Exact Clopper-Pearson intervals in Table S1; table footnote. D9 k6 no longer drives any conclusion. |
| I07 shuffle audit | DONE | "H3 not supported" stated; misses/over-flags listed; prior work (PoPLR, Artes 2014) credited; called a screening tool. Removed from Key Summary Points. |
| I08 weekly null lacks long-term fluctuation | PARTLY | Limitation added (rate-based rules may look more valid). Variance-inflated null not run. OPEN. |
| I10 ML training size / threshold reuse | PARTLY | Methods + limitation state it; "common practice" citations removed ("a common choice"). Nested CV not done. OPEN. |
| I11 D8 covariate shift on GRAPE | PARTLY | Limitation. Not refitted. OPEN. |
| I12 D6/D9/D10 not on GRAPE; no external null | PARTLY | Stated in Results and limitations. GRAPE shuffle audit not run. OPEN. |
| I13 "pre-registered" | DONE | Now "time-stamped in version control, not registered"; quick run disclosed with times (S2). |
| I14 deviations | DONE | Full list in S2 (8 items). |
| I15 secondary reference | DONE | Rewritten with numbers; D6/D10/D8 point estimates above D1 at k6 stated; untested. |
| I16 variability explanation | DONE | Removed; replaced by design explanation + future-only analysis. |
| I17 overclaims | DONE | Abstract, KSP, Discussion, Conclusions rewritten (no "best balance in both clinics", no frontloading advice, no "identified invalid detectors"). |
| I18 authors / AI use | PARTLY | AI use disclosed in Methods and Declarations; author names, affiliations, funding, COI, verification statement, repository URL must be supplied by the authors. OPEN (author action). |
| I19 D4 seed SD | DONE (explained) | Note in S2; common random numbers not implemented. |
| I20 D7 conservative | DONE (text) | Renamed "simplified"; conservativeness explained in Methods and limitations; limits not re-derived. |
| I21 novelty / missing comparators | PARTLY | Prior use of reordering and retest data credited; VFI, ANSWERS, Bayesian, real GPA listed as untested. Not added. OPEN. |
| I22 journal fit | PARTLY | Real-world measures (Table 3) kept; per-opportunity caveat added. No management-outcome analysis possible with these data. |
| I23-I40 moderate | PARTLY | Addressed: per-look caveat, D8 feature list, labels, AI disclosure, citations re-verified (audits/citation_audit.md). Not addressed: flow diagram, cumulative per patient-year false alarms, severity strata, TRIPOD+AI checklist, Artes stationarity, MS vs MTD sensitivity analysis. |
| I41-I46 minor | DONE/PARTLY | Wording fixed; Fig. 1 arrow fixed; criterion labels in Fig. 4; label overlap in Fig. 2 remains. |
