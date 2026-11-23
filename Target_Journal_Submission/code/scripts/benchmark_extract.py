#!/usr/bin/env python3
"""Structural metadata extraction from PMC full-text XML (efetch db=pmc).

Usage:
    python benchmark_extract.py XML_DIR OUT_JSON [--text-dir DIR]

For every <PMCID>.xml in XML_DIR, extracts the mechanically derivable fields
(doi, title, year, article-type, dates from <history>, author / figure / table /
reference counts, main-text word count, sentence statistics, section headings,
title length, abstract headings, keywords, Key Summary Points presence) and
writes them to OUT_JSON. With --text-dir it also dumps plain text
(abstract + body) per paper for manual reading of the semantic fields.

Counting rules:
  * word_count: words in <body> paragraphs and section titles, excluding
    figure/table captions, table contents, and the Key Summary Points box
    (boxed-text), and excluding back-matter (declarations, references).
  * n_figures: <fig> elements in body; n_tables: <table-wrap> elements in body.
  * n_references: <ref> elements in <ref-list>.
  * n_authors: <contrib contrib-type="author"> with a person name or collab.
  * dates: <history><date date-type="received|accepted">.
  * mean sentence length: body paragraph text split on sentence-final
    punctuation followed by whitespace + capital/digit; words per sentence.
"""
import json
import re
import statistics
import sys
import xml.etree.ElementTree as ET
from pathlib import Path


def text_of(el):
    return " ".join("".join(el.itertext()).split()) if el is not None else ""


def date_str(d):
    if d is None:
        return "NR"
    y, m, dd = d.findtext("year"), d.findtext("month"), d.findtext("day")
    if not y:
        return "NR"
    return "-".join(p.zfill(2) if i else p for i, p in enumerate([y, m or "", dd or ""]) if p)


ABBR = re.compile(r"\b(e\.g|i\.e|et al|vs|Fig|Figs|approx|no|Dr|Inc|Ltd|ca|cf)\.$", re.I)


def split_sentences(txt):
    # remove bracketed citations like [1, 2] or [3–5]
    txt = re.sub(r"\[[\d,\s–\-]+\]", "", txt)
    parts = re.split(r"(?<=[.!?])\s+(?=[A-Z0-9(])", txt)
    out, buf = [], ""
    for p in parts:
        buf = (buf + " " + p).strip() if buf else p
        if ABBR.search(buf) or re.search(r"\b[A-Z]\.$", buf):
            continue  # abbreviation / initial: keep joining
        out.append(buf)
        buf = ""
    if buf:
        out.append(buf)
    return [s for s in out if len(s.split()) >= 3]


def strip_nontext(el):
    """Copy-free removal of figures, tables, boxed-text from a body element."""
    for parent in el.iter():
        for child in list(parent):
            if child.tag in ("fig", "table-wrap", "boxed-text", "fig-group", "table-wrap-group",
                             "supplementary-material", "disp-formula"):
                parent.remove(child)


def parse(path):
    root = ET.parse(path).getroot()
    art = root.find(".//article") if root.tag != "article" else root
    meta = art.find(".//front/article-meta")
    rec = {"pmcid": "PMC" + path.stem, "article_type": art.get("article-type", "NR")}
    rec["doi"] = next((a.text for a in meta.findall("article-id") if a.get("pub-id-type") == "doi"), "NR")
    rec["title"] = text_of(meta.find("title-group/article-title"))
    rec["title_words"] = len(rec["title"].split())
    rec["title_has_colon"] = ":" in rec["title"]
    subj = [text_of(s) for s in meta.findall(".//article-categories//subject")]
    rec["subject"] = "; ".join(subj)
    years = [p.findtext("year") for p in meta.findall("pub-date") if p.findtext("year")]
    rec["year"] = min(years) if years else "NR"
    hist = meta.find("history")
    rec["received_date"] = date_str(hist.find("date[@date-type='received']")) if hist is not None else "NR"
    rec["accepted_date"] = date_str(hist.find("date[@date-type='accepted']")) if hist is not None else "NR"
    authors = [c for c in meta.findall(".//contrib-group/contrib") if c.get("contrib-type") == "author"
               and (c.find("name") is not None or c.find("collab") is not None)]
    rec["n_authors"] = len(authors)
    rec["keywords"] = "; ".join(text_of(k) for k in meta.findall(".//kwd-group/kwd"))
    abstracts = meta.findall("abstract")
    main_abs = next((a for a in abstracts if not a.get("abstract-type")), abstracts[0] if abstracts else None)
    rec["abstract_headings"] = " | ".join(text_of(s.find("title")) for s in main_abs.findall("sec")) if main_abs is not None else ""
    rec["abstract_words"] = len(text_of(main_abs).split()) if main_abs is not None else 0
    rec["abstract_text"] = text_of(main_abs)
    body = art.find("body")
    # Only labelled floats count (Springer encodes the Key Summary Points box as an
    # unlabelled <table-wrap id="Taba">, which must not be counted as a table).
    rec["n_figures"] = sum(1 for f in art.iter("fig") if f.find("label") is not None)
    rec["n_tables"] = sum(1 for t in art.iter("table-wrap") if t.find("label") is not None)
    rec["key_summary_points"] = False
    rec["ksp_text"] = ""
    rec["ksp_n_bullets"] = 0
    rec["ksp_subheads"] = ""
    if body is not None:
        for sec in body.findall("sec"):
            if re.search(r"key summary", text_of(sec.find("title")), re.I):
                rec["key_summary_points"] = True
                rows = [text_of(tr) for tr in sec.iter("tr")]
                heads = [text_of(b) for b in sec.iter("bold")]
                rec["ksp_subheads"] = " | ".join(h for h in heads if h)
                rec["ksp_n_bullets"] = len([r for r in rows if r and r not in heads]) or len(list(sec.iter("list-item")))
                rec["ksp_text"] = " || ".join(rows)
                body.remove(sec)  # exclude from main-text metrics
                break
        for sec in list(body.findall("sec")):
            if re.search(r"supplementary information", text_of(sec.find("title")), re.I) or sec.get("sec-type") == "supplementary-material":
                body.remove(sec)
    rec["n_references"] = len(art.findall(".//back/ref-list//ref"))
    # main text
    words, sents, headings, sec_text = 0, [], [], {}
    intro_sents = []
    if body is not None:
        strip_nontext(body)
        for sec in body.findall("sec"):
            h = text_of(sec.find("title"))
            headings.append(h)
            paras = [text_of(p) for p in sec.iter("p")]
            stitles = [text_of(t) for t in sec.iter("title")]
            words += sum(len(p.split()) for p in paras) + sum(len(t.split()) for t in stitles)
            ss = [s for p in paras for s in split_sentences(p)]
            sents.extend(ss)
            sec_text[h] = "\n\n".join(paras)
            if not intro_sents and re.search(r"intro|background", h, re.I):
                intro_sents = ss
        loose = [text_of(p) for p in body.findall("p")]
        words += sum(len(p.split()) for p in loose)
    rec["word_count_approx"] = words
    rec["section_headings"] = " | ".join(headings)
    sub = []
    if body is not None:
        for sec in body.findall("sec"):
            for s2 in sec.findall("sec"):
                sub.append(text_of(s2.find("title")))
    rec["subheadings"] = " | ".join(sub)
    lens = [len(s.split()) for s in sents]
    rec["n_sentences"] = len(lens)
    rec["mean_words_per_sentence"] = round(statistics.mean(lens), 1) if lens else "NR"
    rec["intro_n_sentences"] = len(intro_sents)
    rec["intro_first_sentence"] = intro_sents[0] if intro_sents else ""
    rec["intro_last_sentence"] = intro_sents[-1] if intro_sents else ""
    rec["n_intro_paragraphs"] = 0
    if body is not None:
        for sec in body.findall("sec"):
            if re.search(r"intro|background", text_of(sec.find("title")), re.I):
                rec["n_intro_paragraphs"] = len(sec.findall(".//p"))
                break
    # back matter
    back = art.find("back")
    back_txt = text_of(back) if back is not None else ""
    rec["has_data_availability"] = bool(re.search(r"data availability", back_txt, re.I))
    da = ""
    if back is not None:
        for s in back.iter("sec"):
            if re.search(r"data availab", text_of(s.find("title")), re.I):
                da = text_of(s)
                break
        if not da:
            for fn in back.iter("fn"):
                t = text_of(fn)
                if re.match(r"data availab", t, re.I):
                    da = t
                    break
    if not da:
        for n in art.iter("notes"):
            if n.get("notes-type") == "data-availability" or re.search(r"data availab", text_of(n.find("title")), re.I):
                da = text_of(n)
                break
    if not da:
        for s in art.iter("sec"):
            if re.search(r"data availab", text_of(s.find("title")), re.I):
                da = text_of(s)
                break
    rec["data_availability_text"] = da
    full = text_of(art)
    rec["mentions"] = {k: bool(re.search(p, full, re.I)) for k, p in {
        "TRIPOD": r"TRIPOD", "STROBE": r"STROBE", "CONSORT": r"CONSORT", "STARD": r"STARD",
        "CLAIM": r"\bCLAIM\b", "github": r"github|gitlab|zenodo|code is available|source code",
        "calibration": r"calibration|Brier|Hosmer", "decision_curve": r"decision curve|net benefit",
        "ablation": r"ablation", "sensitivity_analysis": r"sensitivity analys|robustness",
        "external_validation": r"external(ly)? validat|external test", "CI": r"95%\s*(CI|confidence)|confidence interval",
        "cross_validation": r"cross[- ]validation|fold", "bootstrap": r"bootstrap",
    }.items()}
    rec["_sec_text"] = sec_text
    return rec


def main():
    xml_dir, out = Path(sys.argv[1]), Path(sys.argv[2])
    text_dir = Path(sys.argv[sys.argv.index("--text-dir") + 1]) if "--text-dir" in sys.argv else None
    recs = []
    for p in sorted(xml_dir.glob("*.xml")):
        try:
            r = parse(p)
        except Exception as e:  # noqa
            print("FAIL", p, e, file=sys.stderr)
            continue
        if text_dir:
            text_dir.mkdir(parents=True, exist_ok=True)
            with open(text_dir / f"{p.stem}.txt", "w") as fh:
                fh.write(f"{r['title']}\nTYPE {r['article_type']} | {r['subject']}\n\nABSTRACT\n{r['abstract_text']}\n\n")
                fh.write(f"KSP\n{r['ksp_text']}\n\n")
                for h, t in r["_sec_text"].items():
                    fh.write(f"## {h}\n{t}\n\n")
                fh.write(f"## DATA AVAILABILITY\n{r['data_availability_text']}\n")
        r.pop("_sec_text")
        recs.append(r)
    out.write_text(json.dumps(recs, indent=1))
    print(f"parsed {len(recs)} papers -> {out}")


if __name__ == "__main__":
    main()
