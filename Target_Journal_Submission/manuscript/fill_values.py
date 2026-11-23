"""Fill manuscript templates with numbers read from machine-generated result files (no hand-typed results).

Placeholder syntax (inside {{ }}):
  m:D1:3:sens            metric (proportion) as percent, 1 decimal       -> 19.2%
  ci:D1:3:sens           metric with 95% CI                               -> 19.2% (95% CI 7.4-33.3%)
  pp:D6:3:sensitivity    paired difference vs D1 in percentage points, CI  -> +38.5 percentage points (95% CI 19.2 to 57.7)
  ph:D6:3:sensitivity    Holm-adjusted McNemar p                          -> 0.018
  n:D6:3:sensitivity     discordant pairs "only detector / only D1"         -> 10 vs 0
  ff:D6:3                false flags per 1,000 stable eyes                -> 224
  rw:D1:key              realworld.json value (proportion -> percent; *_k -> number)
  d:path.to.value        descriptives.json value (int with commas; float 1 decimal)
  s:key                  statistics.json rq3_audit_concordance (rho 2 dp; diffs in percentage points)
  rq3ci                  bootstrap CI of rho
  meta:key               run_meta_full.json
  check:valid:D1:3 / check:invalid:D6:3 / check:ns:D2:3:sensitivity / check:sig:D6:3:sensitivity
                         assertion of a textual claim; renders as empty string, aborts if the claim is false
  TABLE1, TABLE2, TABLE3, REFS
Citations are written with the numbers of code/scripts/build_refs.py (references.json order) and renumbered here
in order of first appearance (Vancouver).
Usage: python fill_values.py  -> manuscript_filled.md, cover_letter_filled.md, figure_legends.json,
       ../supplementary/Supplementary_Material.md, claim_check_log.txt"""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
J = lambda *p: json.load(open(os.path.join(ROOT, *p)))
M = J('results', 'metrics.json'); S = J('results', 'statistics.json'); DESC = J('results', 'descriptives.json')
RW = J('results', 'realworld.json'); META = J('results', 'run_meta_full.json'); REFS = J('manuscript', 'references.json')
CHECKS = []

def det(code):
    names = {m['detector'] for m in M}
    hit = [n for n in names if n.split()[0] == code]
    assert len(hit) == 1, code
    return hit[0]

def met(code, k):
    r = [m for m in M if m['detector'] == det(code) and m['k'] == int(k)]
    assert len(r) == 1, (code, k); return r[0]

def pair(code, k, endpoint):
    ep = {'sensitivity': 'sensitivity', 'fp': 'false positives (1-spec)', 'gsens': 'GRAPE sensitivity', 'gfp': 'GRAPE false positives'}[endpoint]
    r = [t for t in S['paired_tests'] if t['detector'] == det(code) and t['k'] == int(k) and t['endpoint'] == ep]
    assert len(r) == 1, (code, k, endpoint); return r[0]

pct = lambda x: f"{100 * x:.1f}%"
def pval(p):
    return '<0.001' if p < 0.001 else f"{p:.3f}" if p < 0.1 else f"{p:.2f}"

def valid(code, k):
    m = met(code, k); return m['fpr_true_null_lo'] <= 0.05 and m['fpr_true_null_hi'] <= 0.10

def dig(d, path):
    for p in path.split('.'): d = d[p]
    return d

def resolve(key):
    a = key.split(':')
    t = a[0]
    if t == 'm': return pct(met(a[1], a[2])[a[3]])
    if t == 'ci':
        m = met(a[1], a[2]); return f"{pct(m[a[3]])} (95% CI {100 * m[a[3] + '_lo']:.1f}–{100 * m[a[3] + '_hi']:.1f}%)"
    if t == 'pp':
        r = pair(a[1], a[2], a[3]); return f"{100 * r['diff']:+.1f} percentage points [95% CI {100 * r['diff_lo']:.1f} to {100 * r['diff_hi']:.1f}]".replace('-', '−')
    if t == 'ph': return pval(pair(a[1], a[2], a[3])['p_holm'])
    if t == 'n': r = pair(a[1], a[2], a[3]); return f"{r['only_det']} vs {r['only_D1']}"
    if t == 'ff': return f"{1000 * met(a[1], a[2])['fpr_true_null']:.0f}"
    if t == 'rw':
        v = RW['per_detector'][det(a[1])][a[2]]
        return f"{v:g}" if a[2].endswith(('_k_detected', '_n')) else pct(v)
    if t == 'd':
        v = dig(DESC, a[1])
        return f"{v:,}" if isinstance(v, int) else f"{v:.0f}" if float(v).is_integer() else f"{v:.1f}".replace('-', '−')
    if t == 's':
        v = S['rq3_audit_concordance'][a[1]]
        return f"{v:.2f}" if a[1] == 'spearman_rho' else pval(v) if a[1] == 'spearman_p' else f"{v:g}" if a[1] == 'n_cells' else pct(v) if a[1] == 'share_within_3pp' else f"{100 * v:.1f}"
    if t == 'rq3ci': c = RW['rq3_rho_ci']; return f"{c['rho_ci_lo']:.2f} to {c['rho_ci_hi']:.2f}"
    if t == 'meta': v = META[a[1]]; return f"{v:,}" if isinstance(v, int) else f"{v:.0f}"
    if t == 'check':
        kind = a[1]
        if kind == 'valid': ok = valid(a[2], a[3])
        elif kind == 'invalid': ok = not valid(a[2], a[3])
        elif kind == 'ns': ok = pair(a[2], a[3], a[4])['p_holm'] >= 0.05
        elif kind == 'sig': ok = pair(a[2], a[3], a[4])['p_holm'] < 0.05
        elif kind == 'gt': ok = met(a[2], a[3])[a[4]] > float(a[5])
        elif kind == 'lt': ok = met(a[2], a[3])[a[4]] < float(a[5])
        elif kind == 'same': ok = all(pair(a[2], k, 'sensitivity')['only_det'] == 0 == pair(a[2], k, 'sensitivity')['only_D1'] for k in (3, 4, 5, 6))
        elif kind == 'pairhi_gt': ok = pair(a[2], a[3], a[4])['diff_hi'] > float(a[5])
        elif kind == 'minspec': ok = min(m['spec'] for m in M if m['detector'].split()[0] in ('D8', 'D9')) == met(a[2], a[3])['spec']
        else: raise ValueError(kind)
        CHECKS.append(f"{'PASS' if ok else 'FAIL'} {key}")
        assert ok, 'Claim check failed: ' + key
        return ''
    raise KeyError(key)

ORDER = ['D1', 'D2', 'D3', 'D4', 'D5', 'D6', 'D7', 'D8', 'D9', 'D10']
SHORT = {'D1': 'D1 OLS-MD', 'D2': 'D2 MD rate', 'D3': 'D3 PLR-3', 'D4': 'D4 PoPLR', 'D5': 'D5 Pooled-shuffle conformal',
         'D6': 'D6 Pooled-detrended conformal', 'D7': 'D7 Event analysis', 'D8': 'D8 ML tabular', 'D9': 'D9 ML sequence (GRU)',
         'D10': 'D10 Self-supervised order'}
ci = lambda m, key: '–' if m.get(key) is None else f"{100 * m[key]:.1f} ({100 * m[key + '_lo']:.1f}–{100 * m[key + '_hi']:.1f})"

def table1():
    rows = ['| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | False alarms, true no-change, % (95% CI) | False alarms, shuffle audit, % | Valid |',
            '|---|---|---|---|---|---|---|']
    for k in (3, 4, 5, 6):
        for c in ORDER:
            m = met(c, k); v = valid(c, k)
            rows.append(f"| {k} | {SHORT[c]} | {ci(m, 'sens')} | {ci(m, 'spec')} | {ci(m, 'fpr_true_null')} | {100 * m['fpr_shuffle']:.1f} | {'Yes' if v else '**No**'} |")
    return '\n'.join(rows)

def table2():
    rows = ['| Tests | Detector | Sensitivity, % (95% CI) | Specificity, % (95% CI) | Sensitivity vs D1, pp (Holm p) | False positives vs D1, pp (Holm p) |',
            '|---|---|---|---|---|---|']
    for k in (3, 4):
        for c in ORDER:
            m = met(c, k)
            if m.get('grape_sens') is None: continue
            if c == 'D1': ds = dfp = 'reference'
            else:
                a, b = pair(c, k, 'gsens'), pair(c, k, 'gfp')
                ds, dfp = f"{100 * a['diff']:+.1f} ({pval(a['p_holm'])})", f"{100 * b['diff']:+.1f} ({pval(b['p_holm'])})"
            rows.append(f"| {k} | {SHORT[c]} | {ci(m, 'grape_sens')} | {ci(m, 'grape_spec')} | {ds} | {dfp} |")
    return '\n'.join(rows)

def table3():
    rows = ['| Detector | False flags per 1,000 stable eyes at 3 / 4 / 5 / 6 tests | Progressors flagged by test 6, % | Median test of first flag* | Reference-stable eyes ever flagged by test 6, % |',
            '|---|---|---|---|---|']
    for c in ORDER:
        r = RW['per_detector'][det(c)]
        ff = ' / '.join(f"{1000 * met(c, k)['fpr_true_null']:.0f}" for k in (3, 4, 5, 6))
        med = '–' if r['prog_median_first_k_detected'] is None else f"{r['prog_median_first_k_detected']:g}"
        rows.append(f"| {SHORT[c]} | {ff} | {100 * r['prog_detected_by_6']:.1f} | {med} | {100 * r['stable_ever_flagged_by_6']:.1f} |")
    return '\n'.join(rows)

def supp_tables():
    out = ['| Tests | Detector | Seed SD of sensitivity, pp | Seed SD of true no-change false alarms, pp | Sensitivity, secondary PoPLR reference, % (95% CI) | Valid under strict reading (upper limit ≤5%) |', '|---|---|---|---|---|---|']
    for k in (3, 4, 5, 6):
        for c in ORDER:
            m = met(c, k)
            out.append(f"| {k} | {SHORT[c]} | {100 * m['sens_seed_sd']:.1f} | {100 * m['fpr_true_null_seed_sd']:.1f} | {ci(m, 'sens_ref2')} | {'Yes' if m['fpr_true_null_hi'] <= 0.05 else 'No'} |")
    pt = ['| Tests | Endpoint | Detector | n | Difference vs D1, pp (95% CI) | Only detector / only D1 | McNemar p | Holm p |', '|---|---|---|---|---|---|---|---|']
    for t in S['paired_tests']:
        c = t['detector'].split()[0]
        pt.append(f"| {t['k']} | {t['endpoint']} | {SHORT[c]} | {t['n']} | {100 * t['diff']:+.1f} ({100 * t['diff_lo']:.1f} to {100 * t['diff_hi']:.1f}) | {t['only_det']} / {t['only_D1']} | {pval(t['p'])} | {pval(t['p_holm'])} |")
    return '\n'.join(out), '\n'.join(pt)

CIT = re.compile(r'\[(\d+(?:\s*[,–-]\s*\d+)*)\]')
def expand(g):
    out = []
    for part in re.split(r'\s*,\s*', g):
        if re.search('[–-]', part):
            a, b = map(int, re.split('[–-]', part)); out += list(range(a, b + 1))
        else: out.append(int(part))
    return out

def compress(nums):
    nums = sorted(set(nums)); out = []; i = 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1: j += 1
        out.append(f"{nums[i]}–{nums[j]}" if j - i >= 2 else ', '.join(map(str, nums[i:j + 1]))); i = j + 1
    return ', '.join(out)

def renumber(text):
    order = []
    for g in CIT.findall(text):
        for n in expand(g):
            if n not in order: order.append(n)
    new = {o: i + 1 for i, o in enumerate(order)}
    text = CIT.sub(lambda mm: '[' + compress([new[n] for n in expand(mm.group(1))]) + ']', text)
    refs = '\n'.join(f"{new[o]}. {REFS[o - 1]['vancouver']}" for o in order)
    assert all(REFS[o - 1]['verified'] for o in order)
    return text, refs, order

def fill(text):
    def sub(mm):
        k = mm.group(1).strip()
        if k in ('TABLE1', 'TABLE2', 'TABLE3', 'REFS', 'SUPP_T1', 'SUPP_T2', 'INTRO_METHODS'): return mm.group(0)
        return resolve(k)
    return re.sub(r'\{\{([^}]+)\}\}', sub, text)

if __name__ == '__main__':
    tpl = open(os.path.join(HERE, 'template_main.md')).read()
    tpl = tpl.replace('{{INTRO_METHODS}}', open(os.path.join(HERE, 'sections_intro_methods.md')).read().strip())
    body, back = tpl.split('<!--REFS-->')
    body = fill(body); body, refs, order = renumber(body)
    back = fill(back).replace('{{REFS}}', refs).replace('{{TABLE1}}', table1()).replace('{{TABLE2}}', table2()).replace('{{TABLE3}}', table3())
    out = re.sub(r'\n{3,}', '\n\n', body + back)
    left = re.findall(r'\{\{[^}]+\}\}', out); assert not left, left
    open(os.path.join(HERE, 'manuscript_filled.md'), 'w').write(out)
    for name in ('cover_letter', 'figure_legends'):
        src = open(os.path.join(HERE, f'template_{name}.{"md" if name == "cover_letter" else "json"}')).read()
        src = fill(src); assert '{{' not in src
        open(os.path.join(HERE, f'{name}_filled.md' if name == 'cover_letter' else 'figure_legends.json'), 'w').write(src)
    st1, st2 = supp_tables()
    sup = fill(open(os.path.join(HERE, 'template_supplementary.md')).read()).replace('{{SUPP_T1}}', st1).replace('{{SUPP_T2}}', st2)
    os.makedirs(os.path.join(ROOT, 'supplementary'), exist_ok=True)
    open(os.path.join(ROOT, 'supplementary', 'Supplementary_Material.md'), 'w').write(sup)
    open(os.path.join(HERE, 'claim_check_log.txt'), 'w').write('\n'.join(CHECKS) + f"\n{len(CHECKS)} checks passed\nreferences cited (original ids in order): {order}\n")
    words = len(re.sub(r'\|.*', '', out.split('# Introduction')[1].split('# Declarations')[0]).split())
    print('filled; main-text words (Intro-Conclusions, excl. tables):', words, '| checks:', len(CHECKS), '| refs:', len(order))
