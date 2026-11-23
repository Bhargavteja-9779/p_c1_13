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
EX = json.load(open(os.path.join(ROOT, 'results', 'extra_stats.json')))
s4 = ['| Detector | k | PLR2 sens % (n+) | PLR2 spec % (n−) | PLR3 sens % (n+) | PLR3 spec % (n−) |', '|---|---|---|---|---|---|']
for key, v in sorted(EX['grape_secondary_labels'].items(), key=lambda kv: (int(kv[0].split('@')[1]), int(kv[0].split('@')[0][1:]))):
    d, k = key.split('@')
    s4.append(f"| {d} | {k} | {pc(v['PLR2']['sens'])} ({v['PLR2']['n_pos']}) | {pc(v['PLR2']['spec'])} ({v['PLR2']['n_neg']}) | {pc(v['PLR3']['sens'])} ({v['PLR3']['n_pos']}) | {pc(v['PLR3']['spec'])} ({v['PLR3']['n_neg']}) |")
cum = EX['cumulative_false_alarm_artes_start0']
s5 = ['| Detector | Flagged at least once, k = 3–6, % | Mean per-look false-alarm rate, % |', '|---|---|---|']
for d in sorted(cum, key=lambda x: int(x[1:])):
    s5.append(f"| {d} | {pc(cum[d]['any_flag_k3_to_6'])} | {pc(cum[d]['per_look_mean'])} |")
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
    '## S3. Full results', 'Table S1. All metrics by detector and number of tests (k). Seed SD: standard deviation across five seeds (stochastic detectors only). FA, false-alarm rate; PoPLR ref, secondary reference standard; pp, percentage points. Detector names are the internal code names; D1 OLS-MD = trend test of mean sensitivity, D2 MD-rate = rate rule on mean sensitivity.',
    '\n'.join(s2),
    'Table S2. All paired comparisons with D1 (exact McNemar test; Holm correction within each k and endpoint).',
    '\n'.join(s3),
    'Table S3. External clinic (GRAPE): agreement with the secondary PLR2 and PLR3 progression labels (point estimates; seed means for D8).',
    '\n'.join(s4),
    '## S4. Analyses added after internal review (not in the protocol)',
    'Table S4. Cumulative false alarms on true no-change series (Artes windows starting at the first test; same donor-date draw index across k, donor dates redrawn for each k, so the estimate is approximate).',
    '\n'.join(s5),
    f"Validity under the strict literal protocol rule (upper 95% CI limit of the false-alarm rate at or below 5%) was met only by: {', '.join(EX['strict_valid_cells'])}. The smallest sensitivity gain over D1 that could reach Holm-adjusted significance was {EX['min_significant_gain']['discordant_eyes']} of {EX['min_significant_gain']['n_progressors']} progressors ({100 * EX['min_significant_gain']['gain']:.1f} percentage points). Bootstrap 95% CI for the shuffle-audit Spearman correlation, resampling detector–k cells: {EX['rho_cell_bootstrap_ci'][0]:.2f} to {EX['rho_cell_bootstrap_ci'][1]:.2f}."])
open(os.path.join(OUT, 'Supplementary_Material.md'), 'w').write(md)
d = styled_doc(); d.styles['Normal'].paragraph_format.line_spacing = 1.15
add_markdown(d, md); d.save(os.path.join(OUT, 'Supplementary_Material.docx')); print('supplementary built')
