# Ophthalmology and Therapy - raw style notes (ML/AI + glaucoma-progression subset)

Source: PMC full-text XML (efetch db=pmc), parsed with `code/scripts/benchmark_extract.py`; semantic observations from reading the abstract, introduction, methods and discussion text. All observations are paraphrased; no sentences are copied. Subset = 17 papers: 14 in category (a) ML/AI/prediction and 3 in category (b) glaucoma progression / visual field. The candidate list held no further glaucoma-progression papers, so the (b) group is small.

Counting conventions (same as the CSV):
- Main-text words = body paragraphs and section titles, excluding the Key Summary Points box, figure and table captions, table cells, supplementary-information stubs and back matter.
- Sentence length = words per sentence over body paragraphs, after removing bracketed numeric citations. Sentences are split at end-of-sentence punctuation, with an abbreviation guard.
- Intro sentences/paragraphs = the section headed "Introduction".

## 1. Per-paper record

| PMCID | cat | title words / pattern | abstract (words, headings) | intro: first-sentence type; n sentences / paragraphs; ending; hypothesis? | mean words/sentence | KSP bullets | limitations style |
|---|---|---|---|---|---|---|---|
| PMC13782322 | a | 13; method-forward noun phrase ("An agentic AI workflow for ...") with no colon | 323; Intro/Methods/Results/Conclusions | Opens on what AI can do across ophthalmology; 13 s / 2 p; ends by describing what the orchestration agent does (aim is stated a little earlier as "we propose and evaluate"); no hypothesis | 22.5 | 4 | Its own paragraph that starts with a one-line admission of limitations, then lists them (single-class external sets, need for real-world testing) |
| PMC13546392 | a | 16; topic + colon + design label (ML prediction ... : Design - cross-sectional comparative device study) | 629 (very long); I/M/R/C | Opens on how common myopia is worldwide, with a projected count for 2050; 31 s / 5 p; ends with three numbered research questions and a pointer to the Fig. 1 pipeline; no hypothesis | 27.9 | 7 (sits in a "Digital Features" front section, not the usual box) | Separate "Limitations" subsection inside the Discussion; long and enumerated; repeatedly flags the lack of external validation |
| PMC13518649 | a | 14; descriptive ("Predictive modeling of X using Y-based features of Z") | 271; I/M/R/C | Opens on the burden of disease (CAD as the top cause of death); 15 s / 3 p; ends with a first-of-its-kind claim plus the aim; no hypothesis | 22.1 | 6 | Spread through the Discussion (AutoMorph segmentation failures, no external set), with no ordinal list |
| PMC13250024 | a | 14; topic + colon + perspective tag ("...: A Multicenter AI Perspective") | 260; I/M/R/C | Opens on burden (DME as the main cause of vision loss in diabetes); 11 s / 3 p; ends with a formal "the aim of this study was to ..." sentence; no hypothesis | 30.2 (longest) | 5 | One run-on sentence listing the limitations (retrospective design, two different drugs), plus a remark on algorithm counting |
| PMC13249992 | a | 17; gerund lead ("Predicting ... using an internally validated ML model") | 219; I/M/R/C + Trial Registration | Opens on why IOL position matters clinically; 15 s / 4 p; ends with a formal aim sentence; no hypothesis | 19.7 (shortest) | 5 | Short: a sentence naming small sample size, then a few sentences on subgroups |
| PMC13046889 | a | 10; plain descriptive noun phrase | 297; I/M/R/C | Opens on how central slit-lamp examination is; 21 s / 4 p; ends with an anticipated-benefit sentence (less workload, telemedicine); no hypothesis | 24.8 | 3 | No explicitly labelled limitations paragraph found |
| PMC13046881 | a | 18; "Validation of [device] for [task] using public datasets and deep learning" | 373; I/M/R/C | Opens on burden (DR prevalence with a 2045 projection); 43 s / 8 p (longest intro; includes a "Related Work" subsection); explicit noninferiority hypothesis; ends on why explainability matters | 26.1 | 6 | Separate "Limitations" subsection with an ordinal list |
| PMC12976255 | a | 14; topic + colon + method tag ("...: A Deep Learning Assessment") | 241; I/M/R/C | Opens on epidemiology/definition (myopia as the main cause of refractive error); 17 s / 4 p; ends on expected preventive value; no hypothesis | 22.4 | 5 | Leads with a one-line admission ("some limitations") then lists them in ordinal sentences |
| PMC12882899 | a | 14; object + colon + framework description | 225; I/M/R/C | Opens by defining the device (EVO ICL); 22 s / 6 p; ends with "specifically, we developed ..." contribution sentence; no hypothesis | 23.6 | 4 | Leads with "several limitations" then First/Second/Third... |
| PMC12882927 | a | 19; "Prediction models for X after Y: A multicenter cohort study" | 305; I/M/R/Conclusion | Opens on burden (ROP as a leading cause of childhood blindness, with WHO priority); 14 s / 3 p; ends with "in this study, we aimed to develop ..."; no hypothesis | 25.1 | 5 | Leads with "several limitations" then an ordinal list; asks for validation in other ethnic groups |
| PMC12579022 | a | 11; method-forward ("AI-based quantitative assessment of ... in [disease]") | 253; I/M/R/Conclusion | Opens by classifying the disease into subtypes; 26 s / 4 p; aim sentence near the end, then one sentence on expected value; no hypothesis | 23.7 | 4 | Leads with "several limitations" then an ordinal list |
| PMC12579097 | a | 12; declarative finding ("Machine learning identifies predictors of ...") | 306; I/M/R/Conclusion | Opens by defining the disease and its cause; 25 s / 6 p; ends with a forward-looking impact sentence; no hypothesis | 21.3 | 5 | Names retrospective single-centre design up front, then small n and need for multicentre external validation |
| PMC12579089 | a | 15; gerund + colon + value proposition ("Leveraging ChatGPT for ...: An accuracy-driven and cost-efficient solution ...") | 292; I/M/R/C | Opens on why multimodal imaging exams matter clinically; 15 s / 3 p; ends with aim + impact; no hypothesis | 25.4 | 4 | Opens with a hedge (the study has limitations), then gives them in prose |
| PMC13424006 | a | 15; topic + colon + design ("...: A Population-Based Cohort Study") | 290; I/M/R/Conclusion | Opens on burden (CRC incidence and deaths, with numbers); 17 s / 5 p; explicit hypothesis; ends with an aim/impact sentence | 22.7 | 5 | Strengths paragraph first, then limitations introduced as warranting consideration and enumerated First...Seventh |
| PMC13424024 | b | 16; topic + colon + method/setting ("...: A 5-year VFI-based classification in a real-world cohort") | 260; I/M/R/C | Opens on burden (glaucoma as the leading cause of irreversible blindness, with a count); 24 s / 9 p; ends with "therefore, this ... study aimed to ..."; no hypothesis | 25.6 | 5 | Stand-alone top-level "Limitations" section between Discussion and Conclusions, enumerated |
| PMC13176423 | b | 13; descriptive ("Stereophotographic assessment of X in Y") | 242; I/M/R/C | Opens on epidemiology (myopia prevalence in East Asia); 12 s / 4 p; ends with an expected-value sentence; aim phrased as "this study aims to investigate whether ..."; no hypothesis | 22.3 | 4 | One compact sentence listing small sample, young cohort and short follow-up |
| PMC12901774 | b | 14; "Reassessment of [trial]: statistical evidence and implications ..." | 266; I/M/R/Conclusion | Opens on a conceptual/historical premise (glaucoma long tied to IOP); 33 s / 9 p; the intro mentions competing aetiological hypotheses but the study itself states no hypothesis; ends with a formal aim sentence | 25.8 | 6 | Separate "Limitations" subsection inside the Discussion |

## 2. Pattern notes (own words)

**Titles.** Median 14 words (IQR 13-16; range 10-19). 9/17 use a colon. After the colon there is usually a design label (multicentre cohort, population-based cohort, deep-learning assessment, real-world cohort) or a value statement. Method-forward openings are common in ML papers: "AI-based...", "Machine learning...", "Predicting...", "An agentic AI workflow...". Only one title states a finding as a full clause ("ML identifies predictors..."). Acronyms are mostly spelled out. Device or brand names appear when the paper validates that device (Eyerobo, EVO-ICL, ChatGPT).

**Abstract.** All 17 use the journal's fixed structured format: Introduction / Methods / Results / Conclusion(s). The first heading is "Introduction", not "Background" or "Purpose". Trial registration appears as an extra heading only when the study was registered. A "Supplementary Information" stub is added automatically. Median 271 words (IQR 253-305), so most fit a ~300-word cap; one outlier runs to about 630 words. Results paragraphs are dense with numbers: point estimates, 95% CIs, AUC and p-values.

**Introduction opening.** 9/17 open with disease burden or epidemiology, often with a headline number or a future projection (2045/2050 counts, "leading cause of..."). 3/17 open by defining the disease or device, 3/17 by stating why a clinical task or examination matters, 1/17 with what AI can do in ophthalmology, and 1/17 with a historical/conceptual premise. Typical flow over 3-5 paragraphs: burden, then current practice and its shortcomings, then prior AI/ML work (often listed author by author with their metrics), then an explicit gap phrased as nothing published yet / first time, then the aim.

**Introduction length and ending.** Median 17 sentences (IQR 15-25) in a median 4 paragraphs (IQR 3-6). About 11/17 end on, or within one sentence of, an explicit aim sentence. Common phrasings are "The aim of this study was to...", "In this study, we aimed to...", "This study aimed to...", and "Specifically, we developed...". The other 6 add one closing sentence about expected clinical value or impact after the aim. Only 2/17 state the study's own hypothesis (noninferiority of the device; retinal phenotyping revealing CRC-related changes). Hypothesis-driven framing is therefore the exception. Numbered research questions appear once (the longest, most CS-style paper).

**Contribution / aim phrasing.** Aims are usually one sentence with two or three infinitive clauses ("to identify..., to compare..., and to evaluate..."). Novelty claims are explicit and frequent: "first" or "for the first time" appears in the intro or KSP of several ML papers (CAD same-visit angiography, TabPFN not previously applied, first human study). The Key Summary Points restate the aim almost word for word.

**Key Summary Points.** Every paper has the box, placed before the Introduction. It has two fixed sub-heads, "Why carry out this study?" and "What was learned from the study?". Median 5 bullets (IQR 4-5; range 3-7), usually 2-3 under "why" and 2-3 under "learned". The "why" bullets give the gap and the aim. The "learned" bullets give one headline number (AUC, accuracy, percent) and one implication. Bullets are full sentences of about 20-35 words.

**Sentence length.** Mean words per sentence across the 17 bodies has a median of 23.7 (IQR 22.4-25.6; range 19.7-30.2). Sentences are long and clause-heavy, with many parenthetical abbreviations defined at first use.

**Section headings.** All papers use the flat top-level IMRaD set: Introduction | Methods | Results | Discussion | Conclusion(s). "Conclusions" is used in 12/17 and "Conclusion" in 5/17. Variations: "Patients and Methods" (once outside this subset), a top-level "Limitations" section (1/17), and a CS-style paper that adds "Related work" and "Dataset" (1/17). Methods subheads are short noun phrases: Study Design/Population/Participants, Image Acquisition, Model Construction/Architecture, Statistical Analysis (almost always the last Methods subhead). Results subheads describe content ("Baseline Characteristics", "Performance of ... Models", "External Validation Performance", "SHAP Analysis"). Discussion subheads are rare, appearing only in the longest papers (Clinical Implications, Comparison with Prior Work, Limitations). Back matter always follows the Springer/Adis order: Acknowledgements, Funding (including the Rapid Service Fee), Author Contributions, Data Availability, then Declarations (Conflict of Interest, Ethical Approval). Medical writing assistance is declared in 5/17.

**Limitations.** Almost always a paragraph near the end of the Discussion, not a heading. The most common opener is a one-line admission that the study has several or some limitations, followed by ordinal sentences (First... Second... Finally). A separate Limitations heading appears in 4/17: one top-level section and three Discussion subsections. Recurring items:
- retrospective or single-centre design
- small sample
- no external validation (a standard concession in ML papers)
- single ethnicity or region
- device or software specifics

Limitations are rarely quantified. The word "strength(s)" appears in 4/17 Discussions, but only one paper (PMC13424006) has an explicit strengths paragraph immediately before its limitations.

**Conclusions section.** A short separate section with a median of about 106 words (IQR about 81-117), usually one paragraph. It restates the main finding and ends with a call for prospective or external validation.

**References.** Numbered Vancouver style with square-bracket citations [n], [n, m] and [n–m], numbered in order of first citation. The fraction of first citations that appear in increasing order has a median of 0.97, so citation order is close to strictly sequential; small departures come from re-citing earlier references. Reference entries list up to about 6 authors before "et al.", then title, journal abbreviation, year;volume(issue):pages, with DOI and PMID/PMCID. Median 31 references (IQR 27-44; range 20-65).

**Figures and tables.**
- Labels are "Fig. N" and "Table N".
- Figure captions are long and descriptive (median about 46 words, IQR 23-70). Lettered panels are explained inside the caption, and abbreviations are expanded at the end.
- Table captions are short titles (median 9 words, IQR 8-12). 47 of the 66 tables carry footnotes that define abbreviations and statistical notation.
- Median 3 figures (IQR 3-4) and 3 tables (IQR 2-5) per paper. ML papers typically have one study-flow or pipeline figure, ROC curves and SHAP/Grad-CAM panels.

## 3. Numeric summary (n = 17 ML + glaucoma-progression papers)

| Metric | Median | IQR (Q1-Q3) | Range |
|---|---|---|---|
| Title length (words) | 14 | 13-16 | 10-19 |
| Abstract length (words, cleaned of LaTeX/stubs) | 271 | 253-305 | 219-629 |
| Intro sentences | 17 | 15-25 | 11-43 |
| Intro paragraphs | 4 | 3-6 | 2-9 |
| Mean words per sentence (body) | 23.7 | 22.4-25.6 | 19.7-30.2 |
| Body sentences | 160 | 140-171 | 112-314 |
| Main-text words | 3838 | 3601-4134 | 2561-8953 |
| KSP bullets | 5 | 4-5 | 3-7 |
| Figures | 3 | 3-4 | 0-8 |
| Tables | 3 | 2-5 | 0-10 |
| References | 31 | 27-44 | 20-65 |
| Authors | 8 | 6-13 | 3-17 |
| Conclusions section (words) | 106 | ~81-117 | 44-195 |

Proportions: titles with a colon 9/17; intro opens with burden/epidemiology 9/17; explicit study hypothesis 2/17; intro ends with (or one sentence after) an aim sentence ~11/17; Limitations as its own heading 4/17; Key Summary Points present 17/17.
