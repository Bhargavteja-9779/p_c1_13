# Citation audit (2026-11-23)

Method: every DOI resolved via Crossref API (code/scripts/build_refs.py); cross-checked against PubMed E-utilities
(manuscript/pubmed_check.json: first author, title, author count). Each in-text use checked against title-level content;
claims that go beyond what the title/abstract supports were softened (see "use" column). No reference was added from memory.

| New # | Old # | DOI | Crossref | PubMed | First author match | Note / use check |
|---|---|---|---|---|---|---|
| 1 | 1 | 10.1016/j.ophtha.2014.05.013 | ok | PMID 24974815 | yes |  |
| 2 | 2 | 10.1001/jama.2014.3192 | ok | PMID 24825645 | yes | subtitle from PubMed 24825645 |
| 3 | 3 | 10.1001/archopht.120.10.1268 | ok | PMID 12365904 | yes | Crossref lists only first author; authors, subtitle and pages 1268-79 verified in PubMed 12365904 esummary. |
| 4 | 8 | 10.1016/j.ophtha.2014.01.020 | ok | PMID 24629617 | yes |  |
| 5 | 4 | 10.1136/bjo.2007.135012 | ok | PMID 18211935 | yes |  |
| 6 | 27 | 10.1016/j.ogla.2025.11.004 | ok | PMID 41314338 | yes |  |
| 7 | 5 | 10.1038/eye.2017.1 | ok | PMID 28128796 | yes |  |
| 8 | 6 | 10.1167/iovs.12-10049 | ok | PMID 22952123 | yes |  |
| 9 | 12 | 10.1016/j.ajo.2007.09.038 | ok | PMID 18078852 | yes |  |
| 10 | 36 | 10.1016/j.xops.2023.100423 | ok | PMID 38192682 | yes |  |
| 11 | 7 | 10.1016/j.ophtha.2014.04.015 | ok | PMID 24878173 | yes | Crossref title lacks subtitle; full title taken from visualFields 1.0.7 documentation (man/vfpwgRetest24d2.Rd). |
| 12 | 11 | 10.1167/tvst.7.4.20 | ok | PMID 30159212 | yes |  |
| 13 | 13 | 10.1016/j.ophtha.2008.02.005 | ok | PMID 18378317 | yes |  |
| 14 | 9 | 10.1167/iovs.15-16957 | ok | PMID 26393667 | yes |  |
| 15 | 10 | 10.1167/tvst.10.14.13 | ok | PMID 34910103 | yes |  |
| 16 | 35 | 10.1167/tvst.10.12.4 | ok | PMID 34609479 | yes |  |
| 17 | 16 | 10.1167/tvst.10.7.27 | ok | PMID 34157101 | yes |  |
| 18 | 17 | 10.1016/j.ophtha.2020.12.020 | ok | PMID 33359887 | yes |  |
| 19 | 18 | 10.1167/iovs.18-25568 | ok | PMID 30682206 | yes |  |
| 20 | 19 | 10.1371/journal.pone.0214875 | ok | PMID 30951547 | yes |  |
| 21 | 20 | 10.1038/s41598-019-54653-6 | ok | PMID 31792321 | yes |  |
| 22 | 21 | 10.1167/tvst.5.3.2 | ok | PMID 27152250 | yes |  |
| 23 | 23 | 10.64898/2026.11.16.26368187 | ok | not indexed | n/a |  |
| 24 | 24 | 10.1007/978-3-032-05182-0_53 | ok | PMID 42427494 | yes |  |
| 25 | 34 | 10.1016/j.ophtha.2014.02.021 | ok | PMID 24704136 | yes |  |
| 26 | 22 | 10.1371/journal.pone.0357179 | ok | PMID 42664209 | yes |  |
| 27 | 32 | 10.1136/bmj-2023-078378 | ok | PMID 38636956 | n/a | Replaced DOI 10.1136/bmj.q902 (Crossref record without authors; PubMed 38636956 lists no authors - likely a notice) by the main statement article. |
| 28 | 14 | 10.1167/tvst.11.1.1 | ok | PMID 34978561 | yes |  |
| 29 | 15 | 10.1038/s41597-023-02424-4 | ok | PMID 37543686 | yes |  |
| 30 | 31 | 10.1561/2200000101 | ok | not indexed | n/a |  |
| 31 | 29 | 10.2202/1544-6115.1585 | ok | PMID 21044043 | yes |  |
| 32 | 30 | 10.1080/07350015.1983.10509354 | ok | not indexed | n/a |  |
| 33 | 33 | 10.1214/19-aoas1241 | ok | not indexed | n/a |  |
| 34 | 25 | 10.1016/j.ophtha.2017.01.027 | ok | PMID 28268099 | yes |  |
| 35 | 26 | 10.1167/iovs.12-9476 | ok | PMID 22427597 | yes |  |
| 36 | 28 | 10.1167/tvst.10.13.21 | ok | PMID 34779836 | yes |  |

## Notes
- Non-PubMed items (Freedman & Lane 1983; Angelopoulos & Bates conformal tutorial; Gagnon-Bartsch & Shem-Tov 2019;
  medRxiv preprint 2026) verified by Crossref only. The medRxiv item is a preprint and is labelled as such in the list.
- Use checks: Artes 2014 cited for retest data and for examining GPA specificity (title-level); Wu & Medeiros 2018 cited
  only as a comparison of event vs trend analyses; ML papers [16-21 old] cited as evaluated against other-criterion labels
  (general statement; detailed threshold practice in each paper NOT individually verified -> wording kept general).
- "Expert guidance suggests six tests in the first two years" -> Chauhan et al. 2008 BJO practical recommendations (well-known
  recommendation; abstract-level check: UNVERIFIED in this environment beyond the title, flagged for author check).
- Plagiarism: all text written fresh; no copied sentences from sources (no source full texts were pasted). Automated
  similarity check (iThenticate) not available here -> UNVERIFIED; journal will run its own.

## Abstract-level checks (PubMed efetch, 2026-11-23)
- Chauhan 2008 (BJO): abstract states three examinations per year are needed to identify a 4 dB MD change over 2 years
  -> supports "six tests in the first two years". VERIFIED.
- Artes 2014 (Ophthalmology): specificity of GPA; "possible progression" false-positive rate 18.5% vs "likely" 2.6% after
  10 follow-up tests; large between-patient variation -> supports added Discussion sentence. VERIFIED.
- Stagg 2026 (Ophthalmol Glaucoma): median 1.59 years between tests in a US insured population; years to detect progression
  -> supports "routine care rarely reaches this frequency" and "clinics often need many years". VERIFIED.
- Kim 2026 (PLoS One, "Labeling matters"): labelling strategy a major determinant of ML performance. VERIFIED.
- Wu & Medeiros 2018 (TVST): compares event-based and trend-based analysis at matched specificity. VERIFIED.
- Gardiner 2014 (Ophthalmology): response saturation / unreliable sensitivity in damaged regions -> supports "noise grows
  as sensitivity falls" (paraphrase). VERIFIED at abstract level.
