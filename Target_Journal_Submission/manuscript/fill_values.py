"""Fill manuscript_template.md and cover_letter_template.md with numbers read from ../results/*.json.
No number in the Results/Abstract is typed by hand: every one is a {{placeholder}} resolved here.
Citations are written [@n] / [@n,m] / [@n-m] using the index in references.json (= DOIS order in build_refs.py) and are
renumbered here in order of first citation (Vancouver); the reference list is generated from references.json.
Usage: python fill_values.py  -> manuscript_filled.md, cover_letter_filled.md, figure_legends.json, ../tables/*.md"""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
R = lambda f: json.load(open(os.path.join(ROOT, 'results', f)))
M, S, C, RW = R('v2/metrics.json'), R('v2/statistics.json'), R('dataset_counts.json'), R('realworld.json')
X = R('v2/extras.json')
for _m in M:   # aliases so the primary GRAPE label (MD criterion) keeps its v1 key names
    for _a in ('', '_lo', '_hi', '_n'):
        _m['grape_sens' + _a] = _m.get('grape_md_sens' + _a); _m['grape_spec' + _a] = _m.get('grape_md_spec' + _a)
REFS = json.load(open(os.path.join(HERE, 'references.json')))
DETS = sorted({m['detector'] for m in M}, key=lambda s: int(s.split()[0][1:]))
CODE = {d.split()[0]: d for d in DETS}
SHORT = {'D1': 'OLS-MD', 'D2': 'MD rate', 'D3': 'PLR-3', 'D4': 'PoPLR', 'D5': 'Pooled-shuffle conformal',
         'D6': 'Pooled-detrended conformal', 'D7': 'Event analysis', 'D8': 'ML tabular (LightGBM)',
         'D9': 'ML sequence (GRU)', 'D10': 'Self-supervised order net'}
EP = {'sens': 'sensitivity', 'fp': 'false positives (1-spec)', 'gsens': 'GRAPE MD sensitivity', 'gfp': 'GRAPE MD false positives',
      'p2sens': 'GRAPE PLR2 sensitivity', 'p2fp': 'GRAPE PLR2 false positives'}

def met(code, k):
    return next(m for m in M if m['detector'] == CODE[code] and m['k'] == int(k))
def pair(k, ep, code):
    return next(p for p in S['paired_tests'] if p['k'] == int(k) and p['endpoint'] == EP[ep] and p['detector'] == CODE[code])
def pct(x, dp=1): return 'n/a' if x is None else f'{100 * x:.{dp}f}%'
def pnum(x, dp=1): return f'{100 * x:.{dp}f}'
def pval(p): return '< 0.001' if p < 0.001 else f'= {p:.3f}' if p < 0.1 else f'= {p:.2f}'
def valid(m):
    """Operational rule A3 (results/v2): 95% CI upper <= 10% and lower <= 5%; None = not applicable (cannot flag)."""
    return m['valid_A3']
def excessive(m): return m['clearly_excessive']

def val(key):
    t, *a = key.split('.')
    if t == 'm': return pct(met(a[0], a[1])[a[2]])
    if t == 'mci':
        m = met(a[0], a[1]); f = a[2]
        return f"{pct(m[f])} (95% CI {pnum(m[f + '_lo'])}–{pnum(m[f + '_hi'])}%)"
    if t == 'n': return f"{int(met(a[0], a[1])[a[2]]):,}"
    if t == 'pt':
        p = pair(a[0], a[1], a[2]); f = a[3]
        if f == 'diff': return f"{100 * p['diff']:+.1f}".replace('-', '−')
        if f == 'absdiff': return f"{abs(100 * p['diff']):.1f}"
        if f in ('p', 'p_holm'): return pval(p[f])
        return str(p[f])
    if t == 'ptci':
        p = pair(a[0], a[1], a[2])
        return (f"{100 * p['diff']:+.1f} percentage points vs D1; 95% CI {100 * p['diff_lo']:.1f} to {100 * p['diff_hi']:.1f}; "
                f"Holm-adjusted p {pval(p['p_holm'])}").replace(' -', ' −').replace('(-', '(−').lstrip('-') if p['diff'] >= 0 else ('−' + f"{abs(100 * p['diff']):.1f} percentage points vs D1; 95% CI {100 * p['diff_lo']:.1f} to {100 * p['diff_hi']:.1f}; Holm-adjusted p {pval(p['p_holm'])}").replace(' -', ' −')
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
    if t in ('valid', 'excess', 'literal'):
        k = a[0]; f = {'valid': 'valid_A3', 'excess': 'clearly_excessive', 'literal': 'valid_literal'}[t]
        ok = [c for c in CODE if met(c, k)[f] is True]; bad = [c for c in CODE if met(c, k)[f] is False]
        x = ok if a[1] == 'yes' else bad
        return 'none' if not x else x[0] if len(x) == 1 else ', '.join(x[:-1]) + ' and ' + x[-1]
    if t == 'nvalid': return str(sum(bool(valid(met(c, a[0]))) for c in CODE))
    if t == 'napp': return str(sum(met(c, a[0])['applicable'] for c in CODE))
    if t == 'cum':
        v = X['cumulative_true_null_any_flag_k3to6'][CODE[a[0]]]
        return f"{pnum(v['est'])}% (95% CI {pnum(v['lo'])}–{pnum(v['hi'])}%)" if len(a) == 1 else pct(v['est'])
    if t == 'rq':
        v = X['rq3_' + a[0]][a[1]]
        return str(v) if a[1] == 'n_cells' else pct(v, 0) if a[1] == 'share_within_3pp' else f'{100 * v:.1f} percentage points' if a[1] == 'median_abs_diff' else f'{v:.2f}'
    if t == 'slope':
        v = X['reference_slopes_dB_per_year'][a[0]][a[1]]
        return pct(v, 0) if a[1] == 'share_positive' else f'{v:.2f}'.replace('-', '−')
    if t == 'ratio': return f"{met(a[0], a[1])[a[2]] / met('D1', a[1])[a[2]]:.1f}"
    if t == 'x' and a[0].startswith('refcorr'):
        from scipy.stats import spearmanr
        r = [spearmanr([m['sens'] for m in M if m['k'] == k], [m['sens_ref2'] for m in M if m['k'] == k])[0] for k in (3, 4, 5, 6)]
        return f"{(min(r) if a[0] == 'refcorr_min' else max(r)):.2f}"
    if t == 'x' and a[0] == 'na_cells': return str(sum(not m['applicable'] for m in M))
    if t == 'x' and a[0] == 'mindiff':
        from scipy.stats import binomtest
        n = met('D1', 3)['sens_n']; b = 1
        while binomtest(0, b, 0.5).pvalue >= 0.05 / 9: b += 1
        return f'{100 * b / n:.0f}'
    if t == 'x' and a[0] == 'years_to_flag':
        return f"{(RW[CODE['D1']]['median_tests_to_first_flag'] - 1) * C['uw_ref_interval_y_median']:.0f}"
    if t == 'meta': return f"{R('run_meta_full.json')[a[0]]:,.0f}"
    raise KeyError(key)

def table1():
    L = ['**Table 1** Detection of future-confirmed progression (UWHVF test set) and false alarms on true no-change series',
         '', '| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | False alarms, true no-change, % (95% CI) | False alarms, shuffle audit, % | Excess false alarms | Valid (rule A3) |',
         '|---|---|---|---|---|---|---|---|']
    for k in (3, 4, 5, 6):
        for c in CODE:
            m = met(c, k)
            L.append(f"| {k} | {c} {SHORT[c]} | {pnum(m['sens'])} ({pnum(m['sens_lo'])}–{pnum(m['sens_hi'])}) | "
                     f"{pnum(m['spec'])} ({pnum(m['spec_lo'])}–{pnum(m['spec_hi'])}) | "
                     f"{pnum(m['fpr_true_null'])} ({pnum(m['fpr_true_null_lo'])}–{pnum(m['fpr_true_null_hi'])}) | "
                     f"{pnum(m['fpr_shuffle'])} | {'n/a' if excessive(m) is None else '**Yes**' if excessive(m) else 'No'} | {'n/a' if valid(m) is None else 'Yes' if valid(m) else '**No**'} |")
    L += ['', (f"Sensitivity: {met('D1', 3)['sens_n']} reference progressors; specificity: {met('D1', 3)['spec_n']} reference-stable eyes "
               f"(first k tests only). True no-change: all windows of k consecutive tests in {C['artes_patients']} Artes retest "
               "patients, 10 time-label draws per window. Shuffle audit: UWHVF test-set eyes with their first k tests randomly "
               "re-ordered, 10 times. Excess false alarms: the whole 95% CI of the true no-change false-alarm rate lies above 5%. "
               "Valid (rule A3, a deviation from the protocol, see Methods): upper CI limit at most 10% and lower limit at most 5%. "
               "Under the protocol's literal rule (upper limit at most 5%) no detector that can flag at the nominal level, including D1, "
               "would be valid with 30 retest patients. Stochastic detectors (D5, D6, D8–D10): each eye's flag averaged over 5 seeds. "
               "CI: patient-level bootstrap (2,000 resamples). n/a: D4, D7 and D10 cannot flag with 3 tests by design.")]
    return '\n'.join(L)

def table2():
    L = ['**Table 2** External clinic (GRAPE): sensitivity and specificity against two criterion-based progression labels', '',
         '| Tests | Detector | MD label: sensitivity, % (95% CI) | MD label: specificity, % (95% CI) | PLR2 label: sensitivity, % (95% CI) | PLR2 label: specificity, % (95% CI) |',
         '|---|---|---|---|---|---|']
    ci = lambda m, f: f"{pnum(m[f])} ({pnum(m[f + '_lo'])}–{pnum(m[f + '_hi'])})"
    for k in (3, 4):
        for c in CODE:
            m = met(c, k)
            if m.get('grape_md_sens') is None: continue
            if not m['applicable']:
                L.append(f"| {k} | {c} {SHORT[c]} | n/a | n/a | n/a | n/a |"); continue
            L.append(f"| {k} | {c} {SHORT[c]} | {ci(m, 'grape_md_sens')} | {ci(m, 'grape_md_spec')} | {ci(m, 'grape_plr2_sens')} | {ci(m, 'grape_plr2_spec')} |")
    m3, m4 = met('D1', 3), met('D1', 4)
    L += ['', (f"Labels are those distributed with GRAPE, assigned by rule-based criteria: MD (mean-deviation criterion; primary) and PLR2 "
               f"(pointwise linear regression criterion). Progressors at 3 tests: {m3['grape_md_sens_n']} (MD) and {m3['grape_plr2_sens_n']} (PLR2) "
               f"of {m3['grape_md_sens_n'] + m3['grape_md_spec_n']} eyes; at 4 tests: {m4['grape_md_sens_n']} and {m4['grape_plr2_sens_n']} of "
               f"{m4['grape_md_sens_n'] + m4['grape_md_spec_n']}. PLR3 and any-criterion results: Supplementary Table S4. D5 and D7 calibrated on GRAPE "
               "by 5-fold patient-level cross-fitting; D8 transferred unchanged from UWHVF; D6, D9, D10 not applicable (24-2 specific). "
               "n/a: cannot flag with 3 tests by design. CI: patient-level bootstrap.")]
    return '\n'.join(L)

def table3():
    L = ['**Table 3** Real-world measures: tests to first flag in future-confirmed progressors and false flags in no-change eyes', '',
         '| Detector | Progressors flagged by test 4 / 5 / 6, % | Median tests to first flag | False flags per 1,000 no-change eyes at a single review with 3 / 4 / 5 / 6 tests | No-change series flagged at least once over four reviews (tests 3–6), % (95% CI) |',
         '|---|---|---|---|---|']
    for c in CODE:
        r = RW[CODE[c]]
        L.append(f"| {c} {SHORT[c]} | {pnum(r['cum_detected_by_k4'], 0)} / {pnum(r['cum_detected_by_k5'], 0)} / {pnum(r['cum_detected_by_k6'], 0)} | "
                 f"{val('rw.' + c + '.median_tests_to_first_flag')} | "
                 + ' / '.join(f"{r[f'false_flags_per_1000_k{k}']:.0f}" for k in (3, 4, 5, 6)) +
                 f" | {val('cum.' + c)} |")
    L += ['', (f"Progressors: {RW[CODE['D1']]['n_prog']} UWHVF test-set reference progressors; an eye counts as flagged by test k "
               "if any review with 3..k tests flagged it. Median tests: '> 6' means fewer than half were flagged by 6 tests. In UWHVF the "
               f"median interval between tests was {C['uw_ref_interval_y_median']:.1f} years. False flags per 1,000 = 1,000 × single-review "
               "true no-change false-alarm rate. Last column (exploratory, not pre-registered): Artes retest series reviewed four times, "
               "after 3, 4, 5 and 6 tests, the cumulative counterpart of the second column.")]
    return '\n'.join(L)

def table4():
    return '\n'.join(['**Table 4** Deviations from the analysis plan and other disclosures', '',
      '| Item | Plan (protocol.md) | What was done | Reason / effect |', '|---|---|---|---|',
      '| A1 time labels | Not specified | Each Artes window given the test dates of a random UWHVF test eye (10 draws) | Rate rules depend on time scale; amendment committed before the final run |',
      '| A2 GRAPE | All detectors | D5, D7 re-calibrated on GRAPE by cross-fitting; D6, D9, D10 not applied | Different perimeter and grid; amendment committed before the final run |',
      '| Validity rule | "FPR CI upper bound vs 5%" | Three rules reported; main text uses "excess false alarms" (CI lower limit > 5%) | Literal reading cannot be met by a correctly sized test with 30 patients; operational rule (upper ≤ 10%, lower ≤ 5%) written during the final run |',
      '| Estimand | Not specified | Seed-averaged flags for proportions and differences; majority flag for McNemar | First analysis used majority flags for differences; corrected after review |',
      '| Paired CI | Patient bootstrap | Patient bootstrap | First analysis resampled eyes; corrected after review |',
      '| Not-applicable detectors | Not specified | D4, D7, D10 at 3 tests excluded from counts and Holm families | Cannot flag by design |',
      '| Added analyses | — | Cumulative false alarms over four reviews; future-only reference; GRAPE PLR2/PLR3/any labels in tables | Requested in review; exploratory except GRAPE secondary labels (planned) |',
      '| Development use of data | Artes used once in development | D6 false-alarm excess on Artes known before the plan | D6 result is not confirmatory |',
      '| Quick software check | Quick mode on validation subset | Quick mode also processed Artes and GRAPE files before A1/A2 | Outputs not used for any choice |',
      '| D8 features | Features incl. PoPLR statistic and worst-region slope | 14 features: number of tests, span, level and change of mean sensitivity, its slope and z, share of declining points, mean pointwise −log p, worst-decile pointwise slope, spread measures | PoPLR-type summary (mean −log p) and worst-decile slope used instead; fixed before the final run |'])

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

def tableS4():
    L = ['**Table S4** GRAPE: sensitivity / specificity, % , against the PLR3 and any-criterion labels', '',
         '| Tests | Detector | PLR3 sensitivity | PLR3 specificity | Any-criterion sensitivity | Any-criterion specificity |', '|---|---|---|---|---|---|']
    for k in (3, 4):
        for c in CODE:
            m = met(c, k)
            if m.get('grape_md_sens') is None or not m['applicable']: continue
            L.append(f"| {k} | {c} {SHORT[c]} | " + ' | '.join(pnum(m[f]) for f in ('grape_plr3_sens', 'grape_plr3_spec', 'grape_any_sens', 'grape_any_spec')) + ' |')
    return '\n'.join(L)

def tableS5():
    L = ['**Table S5** Exploratory future-only reference (tests k+1 to end; at least 5 tests), among the eyes evaluated in E1', '',
         '| Tests | Detector | Sensitivity, % (n progressors) | Specificity, % (n stable) |', '|---|---|---|---|']
    for r in sorted(X['future_only_reference'], key=lambda r: (r['k'], int(r['detector'].split()[0][1:]))):
        c = r['detector'].split()[0]
        if not met(c, r['k'])['applicable']: continue
        L.append(f"| {r['k']} | {c} {SHORT[c]} | {pnum(r['sens_future'])} ({r['sens_future_n']}) | {pnum(r['spec_future'])} ({r['spec_future_n']}) |")
    L += ['', X['future_only_note'] + ' Sample sizes shrink quickly with k; results are imprecise and shown for completeness.']
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
    for name, fn in (('TABLES2', tableS2), ('TABLES3', tableS3), ('TABLES4', tableS4), ('TABLES5', tableS5), ('TABLE1', table1), ('TABLE2', table2), ('TABLE3', table3), ('TABLE4', table4)):
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
