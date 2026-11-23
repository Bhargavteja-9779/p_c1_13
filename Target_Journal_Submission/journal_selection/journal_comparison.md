# Journal comparison (internal)

Method: Crossref "assertion" Received/Accepted dates (only Springer Nature and Taylor & Francis deposit them; Elsevier, Wiley,
IEEE, OUP, SAGE, ACM, CUP do not, and their web pages are blocked here (HTTP 403/418) -> acceptance time UNVERIFIABLE).
Scanned 740 Springer Nature / T&F journals with OpenAlex 2-yr mean citedness > 5 in relevant fields (scan_summary.txt,
scan_retry.txt, dates_raw/). Screening used up to 120-200 most recent records; research-only re-computation for shortlist.

| Journal | Publisher | IF (2025, publisher page) | Research-only median / p75 (d) | Scope fit for our work | Decision |
|---|---|---|---|---|---|
| Ophthalmology and Therapy | Springer (Adis) | 4.2 | 52.5 / 70.25 (n=266, full window) | glaucoma monitoring/therapy decisions: good | **SELECTED** |
| Intensive Care Medicine | Springer | 24.3 | 48 / 73 (n=49) | ICU ML: fair; extreme desk-reject bar | rejected: p75 > 72 |
| Critical Care | Springer (BMC) | 11.4 | 63 / 81 | ICU ML: good | rejected: p75 > 72 |
| Cardiovascular Diabetology | Springer (BMC) | 15.6 | 64 / 87 | epidemiology | rejected: p75 |
| Virtual and Physical Prototyping | T&F | n/a here | 63 / 85 | additive manufacturing | rejected: p75 |
| Transactions of Tianjin University | Springer | 7.8 | 50.5 / 69 | catalysis/chemistry only: no fit | rejected: scope |
| Patient Safety in Surgery | Springer (BMC) | 3.3 | 48 / 70 | surgical safety | rejected: lower IF, quartile uncertain |
| Environmental Systems Research | Springer | 5.1 | 54.5 / 73.25 | environment | rejected: p75 + scope |
| Science China Materials | Springer | n/a | 52 / 76 | materials | rejected |
| J. King Saud Univ. CIS | Springer | n/a | 72 / 95 | CS: good | rejected: time |
| Energy Informatics | Springer | none shown | 73 / 90.5 | energy AI | rejected: time, no IF |
| Journal of Translational Medicine | Springer (BMC) | n/a | 96 / 144 | | rejected |
| Eye / Graefe's / BMC Ophthalmol / Eye and Vision | Springer | | 79/214; 133/172; 110/183; 150/187 | ophthalmology | rejected: time |
| Scientific Reports, J Big Data, Complex & Intell Syst, IJCIS, Cybersecurity, npj Digit Med, BMC Med Inform | Springer | | all medians >= 134 | | rejected: time |
| Elsevier fast OA journals (e.g., Alexandria Eng J, Results in Engineering) | Elsevier | | UNVERIFIABLE | | rejected: cannot verify |
| IEEE Access | IEEE | Q2 | UNVERIFIABLE | | rejected: Q2 |
