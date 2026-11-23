# Summary of review issues (deduplicated; from review_01..10 + stakeholder_review)
Recommendations: R01-R09 major revision (R06 near reject), R10 reject, stakeholder major.
All numbers in Tables 1-3, S1-S2 matched the result files. Issues concern methods/protocol/claims.
(rc) = reviewer recomputation.

| ID | Sev | Raised by | Issue -> fix |
|---|---|---|---|
| I01 | FATAL | R01,R03,R09 | Validity rule differs from protocol ("upper CI vs 5%"); under strict reading D1 is invalid at every k; rule text written after quick run that touched Artes/GRAPE -> report both, make conclusions robust, disclose timing |
| I02 | FATAL | R01,R07,R09,R10 | D6 failure on Artes known from development round 5; general claim "apparent gains explained by false alarms" unsupported -> present D6 as known-invalid development variant, drop general claim |
| I03 | FATAL | R06,R02,R04,R05 | Stable = full-series p>0.5 (positive slope) and includes first k tests -> specificity built in -> future-only reference, limitation |
| I09 | FATAL | R08,R06 | GRAPE: many eyes have exactly 3-4 visits so detector sees whole labelled series; labels criterion-based not clinician -> restrict to >=k+2 visits, rename, report PLR2/PLR3/any |
| I04 | MAJOR | R01,R02,R03,R10 | Underpowered (26 progressors); 10-pp margin dropped -> state MDD, estimation framing |
| I05 | MAJOR | R03,R05,R09 | Paired bootstrap/McNemar ignore patient clustering -> cluster bootstrap |
| I06 | MAJOR | R03,R08 | Degenerate percentile CIs; D9 k6 call on 0.100002 -> exact intervals, borderline label |
| I07 | MAJOR | many | Shuffle audit overclaimed; H3 not met; misses D6 k6; flags valid D2/D7; not new -> say H3 not supported |
| I08 | MAJOR | R07,R02 | Weekly Artes noise lacks long-term fluctuation -> rate-threshold detectors biased toward "valid" -> limitation/classify |
| I10 | MAJOR | R04,R10 | ML trained on 192 labelled eyes; threshold+selection share validation set; "common practice" attribution -> narrow claims |
| I11 | MAJOR | R04,R08 | D8 transferred to different perimeter with absolute-dB features -> covariate shift caveat |
| I12 | MAJOR | R08 | D6/D9/D10 not on GRAPE; no external null -> state; shuffle audit on GRAPE |
| I13 | MAJOR | R01,R05,R09 | "Pre-registered" = private commit; quick run touched Artes/GRAPE -> "time-stamped plan", disclose |
| I14 | MAJOR | R05,R08,R09 | "No other deviations" untrue -> full deviation list |
| I15 | MAJOR | R03,R05,R06 | Secondary-reference "same ordering" unsupported -> report numbers |
| I16 | MAJOR | R06,R09 | "Stable eyes have low variability" explanation contradicted (1.03 vs 0.48 dB rc) -> remove |
| I17 | MAJOR | R01,R09,R10 | Overclaims in abstract/KSP/discussion -> rewrite |
| I18 | MAJOR | R01,R09 | Author placeholders; AI-use disclosure in Methods |
| I19 | MAJOR | R03,R05 | D4 seed SD arises from donor-time draws only -> explain |
| I20 | MAJOR | R02,R05 | D7 limits from single-test differences vs mean-of-two baseline -> conservative; soften "GPA-like" |
| I21 | MAJOR | R01,R02,R10 | Novelty: true-null + reordering idea exist (Artes 2014 etc.); ANSWERS, Bayes, VFI, real GPA missing |
| I22 | MAJOR | R01,R10,SH | Journal fit: no management/operational outcome |
| I23-I40 | MODERATE | various | per-look vs cumulative false alarms; time in tests not years; 61% indeterminate excluded, no flow diagram; MS vs MTD; multiplicity; Artes effective n=30; D8 features vs protocol; no calibration plots; strata bins reused on GRAPE; GRAPE D7 limits from 153 pairs; per-eye point removal; local paths; Artes stationarity; severity strata; reference cut-off; citation checks; no TRIPOD+AI checklist; untested advice |
| I41-I46 | MINOR | various | wording ("close to nominal"), figure shading vs rule, label overlap, Fig 1 arrow, declarations, GRAPE demographics, D10 rationale, "detected by test 6" definition |
