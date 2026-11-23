# C1 Candidate real-life problems (internal working list, 2026-11-23)
Evidence column = source to be verified (DOI checked before any use in the paper). "Data" = legally usable open data.

| # | Stakeholder | Problem / cost | Documented failure of current methods | Open data | Real-world measure | Status |
|---|---|---|---|---|---|---|
| 1 | ICU nurses/physicians | Sepsis early warning; sepsis ~11M deaths/yr (Rudd 2020 Lancet) | Epic Sepsis Model AUROC 0.63, alerts on 18% of hospitalised pts (Wong 2021 JAMA IM); alert volume doubled in COVID (Wong 2021 JAMA Netw Open) -> thresholds not portable | PhysioNet 2019 (40k pts, 2 hospital systems, open) | alerts per patient-day, cases caught, lead time | candidate (crowded on accuracy; gap on workload portability) |
| 2 | Anaesthetists | Intraoperative hypotension -> AKI/MI | HPI selection bias (Enevoldsen 2022 Anesthesiology); MAP alone competitive (Mulder) | VitalDB (6,388 cases, open) | false alarms / hour, minutes of hypotension | crowded (many VitalDB papers 2024-26, arXiv 2611.09259 on alert budgets) |
| 3 | ICU clinicians | 12-lead/1-lead ECG arrhythmia across devices | performance drops across sources (CinC 2020/21) | PhysioNet/CinC 2021 | missed AF | crowded |
| 4 | Water utilities | Leakage (non-revenue water) | leak detection benchmarks synthetic | BattLeDIM/LeakDB | m3 lost, detection delay | low journal fit with fast journals |
| 5 | Microbiology labs | AMR, 24-48 h delay for susceptibility | MALDI-TOF ML drops across sites/time (Weis 2022 Nat Med) | DRIAMS | inappropriate therapy | candidate |
| 6 | People with T1D | hypoglycaemia prediction from CGM | patient shift | Shanghai T1DM (Sci Data 2023) | missed hypo events | crowded |
| 7 | AM engineers | porosity/defects in metal AM | process-monitoring models don't transfer across builds | NIST AM-Bench | scrap rate | data-limited |
| 8 | PV plant operators | PV fault detection | thresholds manual | PVOD etc. | energy lost | fit unclear |
| 9 | Grid operators | weather-driven outages | | EAGLE-I | customer-hours | |
| 10 | City air agencies | low-cost PM sensor drift | calibration doesn't transfer across seasons/sites | EPA collocation | exposure misclassification | |
| 11 | ICU | in-hospital mortality (PhysioNet 2012) | old benchmark | open | | weak novelty |
| 12 | Older adults | fall detection wearables | lab-vs-real gap | SisFall/FARSEEING | false alarms/day | |
| 13 | Diabetes clinics | CVD risk in diabetes (NHANES) | risk scores miscalibrated | NHANES + public LMF | | epidemiology style |
| 14 | Toxicologists | in-silico toxicity (Tox21) | scaffold shift | Tox21 | | crowded |
| 15 | Hospital managers | ICU bed occupancy forecasting | | limited open data | | data-limited |
