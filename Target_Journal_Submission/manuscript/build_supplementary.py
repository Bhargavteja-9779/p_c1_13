"""Build ../supplementary/Supplementary_Material.{md,docx} from result files (no hand-typed numbers)."""
import os, json, re
import pandas as pd
from docx.shared import Cm
from build_docx import styled_doc, add_markdown, add_runs
import fill_values as FV
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
OUT = os.path.join(ROOT, 'supplementary'); os.makedirs(OUT, exist_ok=True)
J = lambda *p: json.load(open(os.path.join(ROOT, *p)))
def pc(x): return '' if x is None or pd.isna(x) else f"{100 * x:.1f}"

# ---- Study 1 tables
M = pd.DataFrame(J('results', 'metrics.json')); M['n_'] = M.detector.str.split().str[0].str[1:].astype(int); M = M.sort_values(['k', 'n_'])
t1 = ['| Detector | k | Sens % (95% CI) | Seed SD | Spec % | FA true null % (95% CI) | FA shuffle % | Sens, PoPLR ref % | GRAPE sens % | GRAPE spec % |', '|---|---|---|---|---|---|---|---|---|---|']
for _, r in M.iterrows():
    t1.append(f"| {r.detector} | {r.k} | {pc(r.sens)} ({pc(r.sens_lo)}–{pc(r.sens_hi)}) | {pc(r.sens_seed_sd)} | {pc(r.spec)} | {pc(r.fpr_true_null)} ({pc(r.fpr_true_null_lo)}–{pc(r.fpr_true_null_hi)}) | "
              f"{pc(r.fpr_shuffle)} | {pc(r.sens_ref2)} | {pc(r.get('grape_sens'))} | {pc(r.get('grape_spec'))} |")
T = pd.DataFrame(J('results', 'statistics.json')['paired_tests'])
t3 = ['| k | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Only detector | Only D1 | p | Holm p |', '|---|---|---|---|---|---|---|---|---|']
for _, r in T.iterrows():
    t3.append(f"| {r.k} | {r.endpoint} | {r.detector} | {r.n} | {100 * r['diff']:.1f} ({100 * r.diff_lo:.1f} to {100 * r.diff_hi:.1f}) | {r.only_det} | {r.only_D1} | {r.p:.3g} | {r.p_holm:.3g} |")
EX = J('results', 'extra_stats.json')
cum = EX['cumulative_false_alarm_artes_start0']
t5 = ['| Detector | Flagged at least once, k = 3–6, % | Mean per-review false-alarm rate, % |', '|---|---|---|'] + \
     [f"| {d} | {pc(cum[d]['any_flag_k3_to_6'])} | {pc(cum[d]['per_look_mean'])} |" for d in sorted(cum, key=lambda x: int(x[1:]))]
# ---- Study 2 tables
S2 = J('results', 'study2_metrics.json'); M2 = pd.DataFrame(S2['metrics'])
t2 = ['| Detector | k | Sens R1 % (95% CI) | Seed SD | Spec R1 % | Spec R2 % | Sens R3 % (n) | Spec R3 % (n) | FA true null % (95% CI) | Valid | Strict valid |', '|---|---|---|---|---|---|---|---|---|---|---|']
for _, r in M2.iterrows():
    t2.append(f"| {r.detector} | {r.k} | {pc(r.sens)} ({pc(r.sens_lo)}–{pc(r.sens_hi)}) | {pc(r.sens_seed_sd)} | {pc(r.spec)} | {pc(r.spec_R2)} | {pc(r.sens_R3)} ({int(r.sens_R3_n)}) | "
              f"{pc(r.spec_R3)} ({int(r.spec_R3_n)}) | {pc(r.fa)} ({pc(r.fa_lo)}–{pc(r.fa_hi)}) | {'yes' if r.valid else 'no'} | {'yes' if r.valid_strict else 'no'} |")
P2 = pd.DataFrame(S2['paired'])
t4 = ['| k | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Only detector | Only D1 | p | Holm p |', '|---|---|---|---|---|---|---|---|---|']
for _, r in P2.iterrows():
    hp = '' if r.p_holm is None or pd.isna(r.p_holm) else f"{r.p_holm:.3g}"
    t4.append(f"| {r.k} | {r.endpoint} | {r.detector} | {r.n} | {100 * r['diff']:.1f} ({100 * r.diff_lo:.1f} to {100 * r.diff_hi:.1f}) | {r.only_det} | {r.only_D1} | {r.p:.3g} | {hp} |")
G2 = pd.DataFrame(S2['grape'])
t6 = ['| Detector | k | Sens MD % | Spec MD % | Sens PLR2 % | Spec PLR2 % | Sens PLR3 % | Spec PLR3 % |', '|---|---|---|---|---|---|---|---|']
for _, r in G2.sort_values(['k', 'detector']).iterrows():
    t6.append(f"| {r.detector} | {r.k} | {pc(r.sens_MD)} | {pc(r.spec_MD)} | {pc(r.sens_PLR2)} | {pc(r.spec_PLR2)} | {pc(r.sens_PLR3)} | {pc(r.spec_PLR3)} |")
TT = pd.DataFrame(S2['time_to_first_flag'])
t7 = ['| Detector (every review) | Progressors flagged by test 6, n / N | Median review of first flag (test number) | Median years from first test to first flag |', '|---|---|---|---|'] + \
     [f"| {r.detector} | {r.n_detected} / {r.n} | {r.median_look:.0f} | {r.median_years:.1f} |" for _, r in TT.iterrows()]
log = open(os.path.join(ROOT, 'journal_selection', 'novelty_escalation_log.md')).read()
log = log.replace('# Novelty escalation log (D6) — every idea tried, including failures', '').strip()
prot = open(os.path.join(ROOT, 'code', 'experiments', 'protocol.md')).read(); amend = prot[prot.index('## Amendment A1'):]
detail = FV.fill(open(os.path.join(HERE, 'study1_stats_detail.md')).read())
md = '\n\n'.join([
    '# Supplementary Material',
    'Apparent Gains in Detecting Glaucomatous Visual-Field Progression Disappear at Matched False-Alarm Rates: A Two-Stage Benchmark',
    '## S1. Development history, including abandoned ideas',
    'This section reproduces the development log kept before Study 1. Pilot numbers were computed on the training and validation splits of UWHVF (and, in round 5, on the Artes retest data), never on the locked test split. Study 1 was specified after round 5; Study 2 was specified after Study 1 (protocol_v2). Round 4 explored a different clinical problem and was abandoned.',
    log.replace('\n## ', '\n### '),
    '## S2. Study 1 protocol amendments (made before any final result)', amend.replace('## ', '### '),
    '## S3. Study 1 statistical methods in full, including the validity-rule deviation', detail,
    f"Under the strict literal rule (upper 95% limit of the false-alarm rate at or below 5%), only the following detector–k cells were valid in Study 1: {', '.join(EX['strict_valid_cells'])}; D1 failed it at every k (upper limits {', '.join(f'{100 * v:.1f}%' for v in EX['D1_fpr_hi_by_k'].values())}), and no strict-valid detector was significantly more sensitive than D1. With {EX['min_significant_gain']['n_progressors']} progressors, the smallest significant gain was {EX['min_significant_gain']['discordant_eyes']} eyes ({100 * EX['min_significant_gain']['gain']:.1f} percentage points). Bootstrap 95% CI of the shuffle-audit Spearman correlation, resampling detector–k cells: {EX['rho_cell_bootstrap_ci'][0]:.2f} to {EX['rho_cell_bootstrap_ci'][1]:.2f}.",
    '## S4. Supplementary tables',
    'Table S1. Study 1: all metrics by detector and number of tests (k). Seed SD across five seeds; FA, false-alarm rate; PoPLR ref, secondary reference; detector names are internal code names (D1 OLS-MD = trend test; D2 MD-rate = rate rule on mean sensitivity).',
    '\n'.join(t1),
    'Table S2. Study 2: all per-review metrics. R1, primary reference; R2, flat-stable reference; R3, future-only reference (n shown); FA, false-alarm rate on true no-change series; strict valid, upper 95% limit at or below 5%.',
    '\n'.join(t2),
    'Table S3. Study 1: paired comparisons with D1 (exact McNemar; Holm within k and endpoint).',
    '\n'.join(t3),
    'Table S4. Study 2: paired comparisons with D1 (sensitivity R1, specificity R1 and R2; Holm across D7 and S1–S7 within k; B8 unadjusted).',
    '\n'.join(t4),
    'Table S5. Study 1: false alarms over repeated reviews on true no-change series (approximate; analysis added after internal review).',
    '\n'.join(t5),
    'Table S6. Study 2, external clinic (GRAPE): agreement with the mean-deviation, PLR2 and PLR3 labels.',
    '\n'.join(t6),
    'Table S7. Study 2: time of first flag among R1 progressors flagged by the sixth test (detectors applied at every review). Groups differ between detectors, so medians are descriptive only.',
    '\n'.join(t7),
    '## S5. Supplementary figures'])
open(os.path.join(OUT, 'Supplementary_Material.md'), 'w').write(md)
d = styled_doc(); d.styles['Normal'].paragraph_format.line_spacing = 1.15
add_markdown(d, md)
for f, cap in (('fig3_shuffle_audit_vs_true_null.png', '**Fig. S1** Study 1. False-alarm rate in the shuffle audit (UWHVF test set) versus on true no-change series, one point per detector and number of tests; dashed line, perfect agreement.'),
               ('fig4_grape_external.png', '**Fig. S2** Study 1, external clinic (GRAPE): sensitivity versus 1 − specificity against the mean-deviation label at three and four tests.')):
    d.add_picture(os.path.join(ROOT, 'figures', f), width=Cm(15)); p = d.add_paragraph(); add_runs(p, cap)
d.save(os.path.join(OUT, 'Supplementary_Material.docx')); print('supplementary built')
