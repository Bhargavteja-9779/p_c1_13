# Leakage audit (completed before the final run, 2026-11-23)
| Risk | Check | Status |
|---|---|---|
| Duplicate fields | UWHVF curators merged exact duplicates (datasheet); we keep one record per (eye, age) | OK |
| Patient leakage (two eyes) | split by patient id (salted SHA-256), both eyes in the same split | OK |
| Calibration leakage | D5/D6 pools and D7 limits use TRAIN eyes only (GRAPE: other folds only) | OK |
| Threshold leakage | ML thresholds set on VAL reference-stable eyes; test never used for tuning | OK |
| Temporal leakage in features | detectors see only the first k tests; nothing after test k | OK |
| Reference overlap | future reference uses the full series, which includes the first k tests (partial verification); stated as a limitation; secondary PoPLR reference reported | DISCLOSED |
| Preprocessing on test data | no data-dependent preprocessing apart from blind-spot removal (fixed indices) | OK |
| True-null arm reuse | Artes data were inspected once in development (round 5 FPR check); no tuning used them afterwards | DISCLOSED |
| Label leakage (GRAPE) | GRAPE labels never used for tuning or thresholds | OK |
| Quick mode | evaluates on a validation subset; never touches the test split | OK |
Split files: split assignment is reproducible from code (src/data/uwhvf.py patient_split); exported to
results/split_assignment.csv by scripts/export_split.py.
