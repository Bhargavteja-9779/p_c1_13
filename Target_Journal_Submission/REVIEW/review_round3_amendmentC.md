# Adversarial self-review, round 3 (amendment C, 2026-11-25)

Numbers: every amendment-C number in the manuscript is a {{cc:...}}/{{ccx:...}} placeholder resolved from
results/amendC/amendC.json by manuscript/fill_values.py (no hand-typed results). Hand-written derived phrases checked:
"three to four times too liberal" (16.7-19.6% / 5% = 3.3-3.9x), "about one extra test" (median 6 -> 7),
"almost one in five" (18.0%), "D6s within 2 pp of D1" (-2.0..0.0), d0 "three to five" (2.6-5.3).

| # | Issue | Severity | Status |
|---|---|---|---|
| 1 | Clinic-noise null is used both to calibrate and to check (held-out folds) -> HC1 CNN part near-guaranteed | MAJOR | Stated in Results ("as expected for an out-of-fold check of the same construction") and Limitations; independent check on true retests reported (conservative) |
| 2 | Incorporation: whole-series MD reference contains the tests seen; "flagged by test 8" overlaps the reference | MAJOR | Limitation 1; future-only reference values computed (amendC.json real/*/fut_*) but few eyes |
| 3 | Single clinic for amendment C; GRAPE too short | MAJOR | Limitation 4 |
| 4 | D11 did not beat D1 (HC3 not supported) - headline method is negative | MODERATE | Reported as a finding (synthetic vs real gap); paper framed as calibration/evaluation contribution |
| 5 | HC1 SC part failed (SC D2c 3.9-4.4%, pre-stated < 2.5%) | MINOR | Reported as "not supported as a whole" |
| 6 | D8c single seed; LightGBM model choice by inner split AUC | MINOR | Table 4 |
| 7 | Amendments B and C post-date earlier results and journal reviews | MODERATE | Table 4, cover letter and Limitations; protocol commits a827dcc (C) precede results commit 3700efb |
| 8 | RC thresholds for real-eye evaluation use all 30 Artes patients (in-sample for Artes, not for UWHVF) | MINOR | Not used for any Artes claim |
| 9 | Main text ~6,850 words; TVST limit unverified | MODERATE | Author to check; candidates to cut: RQ3 shuffle-audit detail, GRAPE second paragraph, detector list to supplement |
| 10 | "To our knowledge" novelty claims limited to OpenAlex/Crossref/Europe PMC/web | MINOR | Stated with databases and date (S9) |
Verdict: no number mismatches; claims proportionate; remaining risks are design limitations, all disclosed.
