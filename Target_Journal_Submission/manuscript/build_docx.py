"""Build Final_Manuscript.docx and cover_letter.docx from Markdown sources + result files.
Every number comes from ../results/*.json via {{placeholders}} filled by fill_values.py (no hand-typed numbers).
Usage: python build_docx.py"""
import os, re, json
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))

def set_line_numbers(section):
    sectPr = section._sectPr
    ln = OxmlElement('w:lnNumType'); ln.set(qn('w:countBy'), '1'); ln.set(qn('w:restart'), 'continuous'); ln.set(qn('w:distance'), '360')
    sectPr.append(ln)

def add_page_number(section):
    p = section.footer.paragraphs[0]; p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(); f1 = OxmlElement('w:fldChar'); f1.set(qn('w:fldCharType'), 'begin')
    it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = 'PAGE'
    f2 = OxmlElement('w:fldChar'); f2.set(qn('w:fldCharType'), 'end')
    r._r.append(f1); r._r.append(it); r._r.append(f2)

def styled_doc():
    d = Document()
    st = d.styles['Normal']; st.font.name = 'Times New Roman'; st.font.size = Pt(12)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Times New Roman')
    st.paragraph_format.space_after = Pt(6); st.paragraph_format.line_spacing = 2.0
    for name, size in (('Heading 1', 14), ('Heading 2', 12), ('Heading 3', 12), ('Title', 16)):
        h = d.styles[name]; h.font.name = 'Times New Roman'; h.font.size = Pt(size); h.font.bold = True
        h.font.color.rgb = RGBColor(0, 0, 0)
        rf = h.element.rPr.rFonts
        for a in ('w:asciiTheme', 'w:hAnsiTheme', 'w:eastAsiaTheme', 'w:cstheme'):
            if rf.get(qn(a)) is not None: del rf.attrib[qn(a)]
        for a in ('w:ascii', 'w:hAnsi', 'w:eastAsia', 'w:cs'): rf.set(qn(a), 'Times New Roman')
        h.paragraph_format.space_before = Pt(12); h.paragraph_format.space_after = Pt(6); h.paragraph_format.keep_with_next = True
        if name == 'Heading 3': h.font.italic = True
    sec = d.sections[0]; sec.page_height, sec.page_width = Cm(29.7), Cm(21.0)
    for m in ('left_margin', 'right_margin', 'top_margin', 'bottom_margin'): setattr(sec, m, Cm(2.5))
    add_page_number(sec)
    return d

INLINE = re.compile(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)')
def add_runs(p, text):
    for part in INLINE.split(text):
        if not part: continue
        if part.startswith('**'): r = p.add_run(part[2:-2]); r.bold = True
        elif part.startswith('*'): r = p.add_run(part[1:-1]); r.italic = True
        elif part.startswith('`'): r = p.add_run(part[1:-1]); r.font.name = 'Courier New'
        else: p.add_run(part)

def add_markdown(d, md):
    for block in re.split(r'\n\s*\n', md.strip()):
        lines = block.strip().split('\n')
        if lines[0].startswith('# '): d.add_heading(lines[0][2:].strip(), 1); lines = lines[1:]
        elif lines[0].startswith('## '): d.add_heading(lines[0][3:].strip(), 2); lines = lines[1:]
        elif lines[0].startswith('### '): d.add_heading(lines[0][4:].strip(), 3); lines = lines[1:]
        if not lines: continue
        if all(l.lstrip().startswith(('- ', '* ')) for l in lines):
            for l in lines:
                p = d.add_paragraph(style='List Bullet'); add_runs(p, l.lstrip()[2:])
        elif lines[0].startswith('|'):
            rows = [[c.strip() for c in l.strip().strip('|').split('|')] for l in lines if not re.match(r'^\|\s*-', l)]
            t = d.add_table(rows=len(rows), cols=len(rows[0])); t.style = 'Table Grid'
            for i, row in enumerate(rows):
                for j, c in enumerate(row):
                    cell = t.cell(i, j); cell.text = ''; pp = cell.paragraphs[0]; pp.paragraph_format.line_spacing = 1.0
                    add_runs(pp, c)
                    for r in pp.runs:
                        r.font.size = Pt(9); r.bold = r.bold or i == 0
            d.add_paragraph()
        else:
            p = d.add_paragraph(); add_runs(p, ' '.join(l.strip() for l in lines))

def build_manuscript(md_path, out_path, figures):
    d = styled_doc(); set_line_numbers(d.sections[0])
    md = open(md_path).read()
    add_markdown(d, md)
    # figures at the end, one per page, with legends (journal asks figures as separate files too)
    for fpath, legend in figures:
        p = d.add_paragraph(); p.add_run().add_break(WD_BREAK.PAGE)
        d.add_picture(fpath, width=Cm(16)); cap = d.add_paragraph(); add_runs(cap, legend)
    d.save(out_path)

def build_letter(md_path, out_path):
    d = styled_doc(); d.styles['Normal'].paragraph_format.line_spacing = 1.15
    add_markdown(d, open(md_path).read()); d.save(out_path)

if __name__ == '__main__':
    import sys
    figs = json.load(open(os.path.join(HERE, 'figure_legends.json')))
    build_manuscript(os.path.join(HERE, 'manuscript_filled.md'), os.path.join(HERE, 'Final_Manuscript.docx'),
                     [(os.path.join(ROOT, 'figures', f), leg) for f, leg in figs])
    build_letter(os.path.join(HERE, 'cover_letter_filled.md'), os.path.join(HERE, 'cover_letter.docx'))
    print('built')
