"""Build ../supplementary/Supplementary_Material.docx (+ .md) from result files and the development log.
S1 development history (verbatim from journal_selection/novelty_escalation_log.md and protocol amendments)
S2 full metrics with seed SDs and GRAPE results; S3 all paired McNemar tests vs D1. No hand-typed numbers."""
import os, json
import pandas as pd
from build_docx import styled_doc, add_markdown
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUT = os.path.join(ROOT, 'supplementary'); os.makedirs(OUT, exist_ok=True)

def pc(x): return '' if pd.isna(x) else f"{100 * x:.1f}"

M = pd.DataFrame(json.load(open(os.path.join(ROOT, 'results', 'metrics.json'))))
M['n_'] = M.detector.str.split().str[0].str[1:].astype(int); M = M.sort_values(['k', 'n_'])
s2 = ['| Detector | k | Sens % | Seed SD | Spec % | FA true null % | Seed SD | FA shuffle % | Sens, PoPLR ref % | GRAPE sens % | GRAPE spec % |',
      '|---|---|---|---|---|---|---|---|---|---|---|']
for _, r in M.iterrows():
    s2.append(f"| {r.detector} | {r.k} | {pc(r.sens)} | {pc(r.sens_seed_sd)} | {pc(r.spec)} | {pc(r.fpr_true_null)} | {pc(r.fpr_true_null_seed_sd)} | "
              f"{pc(r.fpr_shuffle)} | {pc(r.sens_ref2)} | {pc(r.get('grape_sens'))} | {pc(r.get('grape_spec'))} |")
T = pd.DataFrame(json.load(open(os.path.join(ROOT, 'results', 'statistics.json')))['paired_tests'])
s3 = ['| k | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Only detector | Only D1 | p | Holm p |', '|---|---|---|---|---|---|---|---|---|']
for _, r in T.iterrows():
    s3.append(f"| {r.k} | {r.endpoint} | {r.detector} | {r.n} | {100 * r['diff']:.1f} ({100 * r.diff_lo:.1f} to {100 * r.diff_hi:.1f}) | {r.only_det} | {r.only_D1} | {r.p:.3g} | {r.p_holm:.3g} |")
log = open(os.path.join(ROOT, 'journal_selection', 'novelty_escalation_log.md')).read()
log = log.replace('# Novelty escalation log (D6) — every idea tried, including failures', '').strip()
prot = open(os.path.join(ROOT, 'code', 'experiments', 'protocol.md')).read()
amend = prot[prot.index('## Amendment A1'):]
md = '\n\n'.join([
    '# Supplementary Material',
    'How Early Can Glaucomatous Visual-Field Progression Be Detected Without False Alarms? An Open Benchmark With a True No-Change Arm',
    '## S1. Development history, including abandoned ideas',
    'This section reproduces the development log kept during the study. All pilot numbers were computed on the training and validation splits of UWHVF (and, in round 5, on the Artes retest data), never on the locked test split. The benchmark reported in the main text was specified after round 5. Round 4 explored a different clinical problem (neovascular age-related macular degeneration) and was abandoned.',
    log.replace('\n## ', '\n### '),
    '## S2. Protocol amendments (made before any final result)', amend.replace('## ', '### '),
    '## S3. Full results', 'Table S1. All metrics by detector and number of tests (k). Seed SD: standard deviation across five seeds (stochastic detectors only). FA, false-alarm rate; PoPLR ref, secondary reference standard; pp, percentage points.',
    '\n'.join(s2),
    'Table S2. All paired comparisons with D1 (exact McNemar test; Holm correction within each k and endpoint).',
    '\n'.join(s3)])
open(os.path.join(OUT, 'Supplementary_Material.md'), 'w').write(md)
d = styled_doc(); d.styles['Normal'].paragraph_format.line_spacing = 1.15
add_markdown(d, md); d.save(os.path.join(OUT, 'Supplementary_Material.docx')); print('supplementary built')
