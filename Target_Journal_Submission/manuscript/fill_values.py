"""Fill manuscript_template.md and cover_letter_template.md with numbers read from ../results/*.json.
No number in the Results/Abstract is typed by hand: every one is a {{placeholder}} resolved here.
Citations are written [@n] / [@n,m] / [@n-m] using the index in references.json (= DOIS order in build_refs.py) and are
renumbered here in order of first citation (Vancouver); the reference list is generated from references.json.
Usage: python fill_values.py  -> manuscript_filled.md, cover_letter_filled.md, figure_legends.json, ../tables/*.md"""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
R = lambda f: json.load(open(os.path.join(ROOT, 'results', f)))
M, S, C, RW = R('metrics.json'), R('statistics.json'), R('dataset_counts.json'), R('realworld.json')
REFS = json.load(open(os.path.join(HERE, 'references.json')))
DETS = sorted({m['detector'] for m in M}, key=lambda s: int(s.split()[0][1:]))
CODE = {d.split()[0]: d for d in DETS}
SHORT = {'D1': 'OLS-MD', 'D2': 'MD rate', 'D3': 'PLR-3', 'D4': 'PoPLR', 'D5': 'Pooled-shuffle conformal',
         'D6': 'Pooled-detrended conformal', 'D7': 'Event analysis', 'D8': 'ML tabular (LightGBM)',
         'D9': 'ML sequence (GRU)', 'D10': 'Self-supervised order net'}
EP = {'sens': 'sensitivity', 'fp': 'false positives (1-spec)', 'gsens': 'GRAPE sensitivity', 'gfp': 'GRAPE false positives'}

def met(code, k):
    return next(m for m in M if m['detector'] == CODE[code] and m['k'] == int(k))
def pair(k, ep, code):
    return next(p for p in S['paired_tests'] if p['k'] == int(k) and p['endpoint'] == EP[ep] and p['detector'] == CODE[code])
def pct(x, dp=1): return 'n/a' if x is None else f'{100 * x:.{dp}f}%'
def pnum(x, dp=1): return f'{100 * x:.{dp}f}'
def pval(p): return '< 0.001' if p < 0.001 else f'= {p:.3f}' if p < 0.1 else f'= {p:.2f}'
def valid(m):
    """Validity rule fixed in the analysis plan before results: 95% CI upper limit <= 10% and lower limit <= 5%."""
    return m['fpr_true_null_hi'] <= 0.10 and m['fpr_true_null_lo'] <= 0.05

def val(key):
    t, *a = key.split('.')
    if t == 'm': return pct(met(a[0], a[1])[a[2]])
    if t == 'mci':
        m = met(a[0], a[1]); f = a[2]
        return f"{pct(m[f])} (95% CI {pnum(m[f + '_lo'])}–{pnum(m[f + '_hi'])}%)"
    if t == 'n': return f"{int(met(a[0], a[1])[a[2]]):,}"
    if t == 'pt':
        p = pair(a[0], a[1], a[2]); f = a[3]
        if f == 'diff': return f"{100 * p['diff']:+.1f}"
        if f == 'absdiff': return f"{abs(100 * p['diff']):.1f}"
        if f in ('p', 'p_holm'): return pval(p[f])
        return str(p[f])
    if t == 'ptci':
        p = pair(a[0], a[1], a[2])
        return (f"{100 * p['diff']:+.1f} percentage points vs D1; 95% CI {100 * p['diff_lo']:.1f} to {100 * p['diff_hi']:.1f}; "
                f"Holm-adjusted p {pval(p['p_holm'])}").replace(' -', ' −')
    if t == 'c':
        v = C[a[0]]
        if isinstance(v, int): return f'{v:,}'
        return f'{v:.{int(a[1]) if len(a) > 1 else 1}f}'.replace('-', '−')
    if t == 'rw':
        v = RW[CODE[a[0]]][a[1]]
        if a[1].startswith('false_flags'): return f'{v:.0f}'
        if a[1].startswith('median_tests'): return '> 6' if v > 6 else f'{v:g}'
        if a[1].startswith('mean_tests'): return f'{v:.1f}'
        return pct(v, 0)
    if t == 'a':
        v = S['rq3_audit_concordance'][a[0]]
        if a[0] == 'spearman_rho': return f'{v:.2f}'
        if a[0] == 'spearman_p': return pval(v)
        if a[0] == 'n_cells': return str(v)
        if a[0] == 'share_within_3pp': return pct(v, 0)
        return f'{100 * v:.1f} percentage points'
    if t == 'valid':
        k = a[0]; ok = [c for c in CODE if valid(met(c, k))]; bad = [c for c in CODE if not valid(met(c, k))]
        x = ok if a[1] == 'yes' else bad
        return 'none' if not x else x[0] if len(x) == 1 else ', '.join(x[:-1]) + ' and ' + x[-1]
    if t == 'nvalid': return str(sum(valid(met(c, a[0])) for c in CODE))
    if t == 'ratio': return f"{met(a[0], a[1])[a[2]] / met('D1', a[1])[a[2]]:.1f}"
    if t == 'x' and a[0].startswith('refcorr'):
        from scipy.stats import spearmanr
        r = [spearmanr([m['sens'] for m in M if m['k'] == k], [m['sens_ref2'] for m in M if m['k'] == k])[0] for k in (3, 4, 5, 6)]
        return f"{(min(r) if a[0] == 'refcorr_min' else max(r)):.2f}"
    if t == 'meta': return f"{R('run_meta_full.json')[a[0]]:,.0f}"
    raise KeyError(key)

def table1():
    L = ['**Table 1** Detection of future-confirmed progression (UWHVF test set) and false alarms on true no-change series',
         '', '| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | False alarms, true no-change, % (95% CI) | False alarms, shuffle audit, % | Valid |',
         '|---|---|---|---|---|---|---|']
    for k in (3, 4, 5, 6):
        for c in CODE:
            m = met(c, k)
            L.append(f"| {k} | {c} {SHORT[c]} | {pnum(m['sens'])} ({pnum(m['sens_lo'])}–{pnum(m['sens_hi'])}) | "
                     f"{pnum(m['spec'])} ({pnum(m['spec_lo'])}–{pnum(m['spec_hi'])}) | "
                     f"{pnum(m['fpr_true_null'])} ({pnum(m['fpr_true_null_lo'])}–{pnum(m['fpr_true_null_hi'])}) | "
                     f"{pnum(m['fpr_shuffle'])} | {'Yes' if valid(m) else '**No**'} |")
    L += ['', (f"Sensitivity: {met('D1', 3)['sens_n']} reference progressors; specificity: {met('D1', 3)['spec_n']} reference-stable eyes "
               f"(first k tests only). True no-change: all windows of k consecutive tests in {C['artes_patients']} Artes retest "
               "patients, 10 time-label draws per window. Shuffle audit: UWHVF test-set eyes with their first k tests randomly "
               "re-ordered, 10 times. Valid: 95% CI of the true no-change false-alarm rate has an upper limit of at most 10% "
               "and a lower limit of at most 5%. Stochastic detectors (D4–D6, D8–D10): mean over 5 seeds. CI: patient-level "
               "bootstrap (2,000 resamples). D4, D7 and D10 cannot flag at 3 tests by design.")]
    return '\n'.join(L)

def table2():
    L = ['**Table 2** External clinic (GRAPE): agreement with the clinicians\' mean-deviation progression label', '',
         '| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | Change in false positives vs D1, pp (Holm p) |',
         '|---|---|---|---|---|']
    for k in (3, 4):
        for c in CODE:
            m = met(c, k)
            if m['grape_sens'] is None: continue
            fp = '—' if c == 'D1' else f"{100 * pair(k, 'gfp', c)['diff']:+.1f} ({pval(pair(k, 'gfp', c)['p_holm']).replace('= ', '').replace('< ', '<')})"
            L.append(f"| {k} | {c} {SHORT[c]} | {pnum(m['grape_sens'])} ({pnum(m['grape_sens_lo'])}–{pnum(m['grape_sens_hi'])}) | "
                     f"{pnum(m['grape_spec'])} ({pnum(m['grape_spec_lo'])}–{pnum(m['grape_spec_hi'])}) | {fp} |")
    L += ['', (f"n = {int(met('D1', 3)['grape_sens_n'])} labelled progressors and {int(met('D1', 3)['grape_spec_n'])} non-progressors at 3 tests; "
               f"{int(met('D1', 4)['grape_sens_n'])} and {int(met('D1', 4)['grape_spec_n'])} at 4 tests. D5 and D7 calibrated on GRAPE by "
               "5-fold patient-level cross-fitting; D8 transferred unchanged from UWHVF; D6, D9, D10 not applicable (24-2 specific). "
               "pp, percentage points; Holm p, exact McNemar test vs D1 with Holm correction.")]
    return '\n'.join(L)

def table3():
    L = ['**Table 3** Real-world measures: tests to first flag in future-confirmed progressors and false flags per 1,000 stable eyes', '',
         '| Detector | Progressors flagged by test 4 / 5 / 6, % | Median tests to first flag | False flags per 1,000 no-change eyes at test 3 / 4 / 5 / 6 | Stable eyes ever flagged over tests 3–6, % (exploratory) |',
         '|---|---|---|---|---|']
    for c in CODE:
        r = RW[CODE[c]]
        L.append(f"| {c} {SHORT[c]} | {pnum(r['cum_detected_by_k4'], 0)} / {pnum(r['cum_detected_by_k5'], 0)} / {pnum(r['cum_detected_by_k6'], 0)} | "
                 f"{val('rw.' + c + '.median_tests_to_first_flag')} | "
                 + ' / '.join(f"{r[f'false_flags_per_1000_k{k}']:.0f}" for k in (3, 4, 5, 6)) +
                 f" | {pnum(r['exploratory_cum_stable_flagged_k3to6'], 0)} |")
    L += ['', (f"Progressors: {RW[CODE['D1']]['n_prog']} UWHVF test-set reference progressors; an eye counts as flagged by test k "
               "if any look at 3..k tests flagged it. Median tests: '> 6' means fewer than half were flagged by 6 tests. In UWHVF the "
               f"median interval between tests was {C['uw_ref_interval_y_median']:.1f} years, so each extra test is roughly one extra "
               "year of follow-up. False flags per 1,000 = 1,000 × true no-change false-alarm rate. Last column: share of "
               f"{C['uw_test_ref_stable']} reference-stable eyes flagged at least once over the four looks (not pre-registered).")]
    return '\n'.join(L)


def tableS2():
    L = ['**Table S2** Sensitivity, % (95% CI), against the secondary reference (full-series PoPLR p < 0.01)', '',
         '| Detector | 3 tests | 4 tests | 5 tests | 6 tests |', '|---|---|---|---|---|']
    for c in CODE:
        cells = []
        for k in (3, 4, 5, 6):
            m = met(c, k); cells.append(f"{pnum(m['sens_ref2'])} ({pnum(m['sens_ref2_lo'])}–{pnum(m['sens_ref2_hi'])})")
        L.append(f"| {c} {SHORT[c]} | " + ' | '.join(cells) + ' |')
    L += ['', f"n = {met('D1', 3)['sens_ref2_n']} secondary-reference progressors in the UWHVF test set. Mean over seeds for stochastic detectors."]
    return '\n'.join(L)

def tableS3():
    L = ['**Table S3** Paired comparisons with D1 (exact McNemar test, Holm correction within number of tests and endpoint)', '',
         '| Tests | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Flagged only by detector / only by D1 | p | Holm p |',
         '|---|---|---|---|---|---|---|---|']
    for p in sorted(S['paired_tests'], key=lambda p: (p['k'], p['endpoint'], int(p['detector'].split()[0][1:]))):
        c = p['detector'].split()[0]
        L.append(f"| {p['k']} | {p['endpoint']} | {c} {SHORT[c]} | {p['n']} | {100 * p['diff']:+.1f} ({100 * p['diff_lo']:.1f} to {100 * p['diff_hi']:.1f}) | "
                 f"{p['only_det']} / {p['only_D1']} | {pval(p['p']).replace('= ', '')} | {pval(p['p_holm']).replace('= ', '')} |")
    L += ['', 'pp, percentage points. Stochastic detectors: majority flag over five seeds. GRAPE endpoints at 3 and 4 tests only.']
    return '\n'.join(L)

def renumber_citations(md):
    order = []
    def expand(body):
        ids = []
        for part in body.replace('@', '').split(','):
            part = part.strip()
            if '-' in part: a, b = map(int, part.split('-')); ids += list(range(a, b + 1))
            elif part: ids.append(int(part))
        return ids
    for m in re.finditer(r'\[@([0-9,\- @]+)\]', md):
        for i in expand(m.group(1)):
            if i not in order: order.append(i)
    new = {old: n + 1 for n, old in enumerate(order)}
    def fmt(m):
        ns = sorted(new[i] for i in expand(m.group(1))); out, s = [], 0
        while s < len(ns):
            e = s
            while e + 1 < len(ns) and ns[e + 1] == ns[e] + 1: e += 1
            out.append(f'{ns[s]}–{ns[e]}' if e - s >= 2 else ', '.join(map(str, ns[s:e + 1]))); s = e + 1
        return '[' + ', '.join(out) + ']'
    md = re.sub(r'\[@([0-9,\- @]+)\]', fmt, md)
    reflist = []
    for old in order:
        r = REFS[old - 1]
        if not r.get('verified'): raise SystemExit(f'unverified reference {r}')
        reflist.append(f"{new[old]}. {r['vancouver'].replace('&amp;', '&').replace('?.', '?')}")
    return md, reflist, order

def fill(text):
    for name, fn in (('TABLES2', tableS2), ('TABLES3', tableS3), ('TABLE1', table1), ('TABLE2', table2), ('TABLE3', table3)):
        text = text.replace('{{' + name + '}}', fn())
    text = re.sub(r'\{\{(?!REFERENCES)([^}]+)\}\}', lambda m: val(m.group(1).strip()), text)
    left = [x for x in re.findall(r'\{\{[^}]*\}\}', text) if x != '{{REFERENCES}}']
    if left: raise SystemExit(f'unresolved placeholders: {left}')
    return text

def words(s): return len(re.findall(r"[A-Za-z0-9][\w'’.%–-]*", s))

if __name__ == '__main__':
    md = fill(open(os.path.join(HERE, 'manuscript_template.md')).read())
    md, reflist, order = renumber_citations(md)
    md = md.replace('{{REFERENCES}}', '\n\n'.join(reflist)) if '{{REFERENCES}}' in md else md + '\n\n# References\n\n' + '\n\n'.join(reflist)
    open(os.path.join(HERE, 'manuscript_filled.md'), 'w').write(md)
    for name, fn in (('table1_main', table1), ('table2_grape', table2), ('table3_realworld', table3)):
        open(os.path.join(ROOT, 'tables', name + '.md'), 'w').write(fn() + '\n')
    os.makedirs(os.path.join(ROOT, 'supplementary'), exist_ok=True)
    open(os.path.join(ROOT, 'supplementary', 'Supplementary_Material.md'), 'w').write(fill(open(os.path.join(HERE, 'supplementary_template.md')).read()))
    cl = fill(open(os.path.join(HERE, 'cover_letter_template.md')).read())
    open(os.path.join(HERE, 'cover_letter_filled.md'), 'w').write(re.sub(r'\[@[0-9,\- @]+\]', '', cl))
    json.dump(json.load(open(os.path.join(HERE, 'figure_legends_template.json'))), open(os.path.join(HERE, 'figure_legends.json'), 'w'), indent=1)
    abstract = md.split('# Abstract')[1].split('\n# ')[0] if '# Abstract' in md else ''
    body = md.split('# Introduction')[1].split('# Declarations')[0]
    body_wo_tables = '\n'.join(l for l in body.split('\n') if not l.startswith('|'))
    stats = dict(abstract_words=words(abstract), main_text_words=words(body_wo_tables), references=len(reflist),
                 cited_old_indices=order, uncited=[i for i in range(1, len(REFS) + 1) if i not in order])
    json.dump(stats, open(os.path.join(HERE, 'fill_stats.json'), 'w'), indent=1); print(stats)
