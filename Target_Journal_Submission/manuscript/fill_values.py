"""Fill manuscript templates with numbers taken ONLY from machine-generated result files.
Inputs : ../results/metrics.json, statistics.json, descriptives.json, run_meta_full.json, references.json
Templates: front_template.md, sections_intro_methods.md, results_discussion_template.md, back_template.md,
           cover_letter_template.md, figure_legends_template.json
Outputs: manuscript_filled.md, cover_letter_filled.md, figure_legends.json, claim_checks.json

Placeholder grammar ({{...}}):
  d:<dotted.path>:<fmt>       descriptives.json value (fmt: int | 0 | 1 | 2 | pct)
  s:<dotted.path>:<fmt>       statistics.json rq3_audit_concordance value
  m:runtime_min               run time in minutes
  p:<col>:<Dn>:<k>            metric as percent, 1 decimal (col: sens spec fpr_true_null fpr_shuffle grape_sens grape_spec sens_ref2)
  ci:<col>:<Dn>:<k>           "x% (95% CI a–b%)"
  sd:<col>:<Dn>:<k>           seed SD in percentage points
  n:<col>:<Dn>:<k>            denominator
  f1000:<Dn>:<k>              false flags per 1,000 stable eyes (true no-change)
  dt:<endpoint>:<Dn>:<k>      paired difference vs D1 with CI and Holm p (endpoint: sens fp gsens gfp)
  ttd:<Dn>                    % of reference progressors flagged by the 6th test (seed mean)
  table:<name>                generated Markdown table
Citations [n] in the templates use the numbering of references.json (DOIS order in code/scripts/build_refs.py); they are
renumbered here in order of first citation (Vancouver) and the reference list is generated accordingly.
Claims made in words (e.g. 'not significant') are checked by assertions in CHECKS below; the script fails if any is false."""
import os, re, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, '..'))
J = lambda *p: json.load(open(os.path.join(ROOT, *p)))
M = J('results', 'metrics.json'); ST = J('results', 'statistics.json'); DE = J('results', 'descriptives.json')
META = J('results', 'run_meta_full.json'); REFS = J('manuscript', 'references.json')
PT = ST['paired_tests']; RQ3 = ST['rq3_audit_concordance']
EX = J('results', 'extra_stats.json')
EP = {'sens': 'sensitivity', 'fp': 'false positives (1-spec)', 'gsens': 'GRAPE sensitivity', 'gfp': 'GRAPE false positives'}

def det_name(code):
    names = sorted({r['detector'] for r in M}); hit = [n for n in names if n.split()[0] == code]
    assert len(hit) == 1, code; return hit[0]
def row(code, k):
    r = [x for x in M if x['detector'] == det_name(code) and x['k'] == int(k)]; assert len(r) == 1; return r[0]
def val(col, code, k):
    v = row(code, k).get(col); assert v is not None, (col, code, k); return v
def pair(ep, code, k):
    r = [x for x in PT if x['detector'] == det_name(code) and x['k'] == int(k) and x['endpoint'] == EP[ep]]
    assert len(r) == 1, (ep, code, k); return r[0]
def valid(code, k):
    r = row(code, k); return r['fpr_true_null_lo'] <= 0.05 and r['fpr_true_null_hi'] <= 0.10
def borderline(code, k):
    r = row(code, k); return (not valid(code, k)) and r['fpr_true_null_lo'] <= 0.05 and round(100 * r['fpr_true_null_hi'], 1) <= 10.0
def pc(x): return f"{100 * x:.1f}"
def pv(p):
    return '< 0.001' if p < 0.001 else f"= {p:.3f}" if p < 0.01 else f"= {p:.2f}"
def dig(d, path):
    for k in path.split('.'): d = d[k]
    return d
def fmt(v, f):
    if f == 'int': return f"{int(round(v)):,}"
    if f == 'pct': return f"{100 * v:.0f}%"
    if f == 'pp': return f"{100 * v:.1f} percentage points"
    return f"{v:.{int(f)}f}"

SHORT = {'D1': 'D1 Trend, MD', 'D2': 'D2 MD rate', 'D3': 'D3 PLR-3', 'D4': 'D4 PoPLR', 'D5': 'D5 Pooled conformal',
         'D6': 'D6 Pooled-detrended', 'D7': 'D7 Event', 'D8': 'D8 LightGBM', 'D9': 'D9 GRU', 'D10': 'D10 Order net'}

def T_main():
    ks = sorted({r['k'] for r in M}); out = ['| Detector | k | Sensitivity, % (95% CI) | Specificity, % | False alarms, true no-change, % (95% CI) | False alarms, shuffle audit, % | Valid |',
                                            '|---|---|---|---|---|---|---|']
    for k in ks:
        for code in [f'D{i}' for i in range(1, 11)]:
            r = row(code, k)
            out.append(f"| {SHORT[code]} | {k} | {pc(r['sens'])} ({pc(r['sens_lo'])}–{pc(r['sens_hi'])}) | {pc(r['spec'])} | "
                       f"{pc(r['fpr_true_null'])} ({pc(r['fpr_true_null_lo'])}–{pc(r['fpr_true_null_hi'])}) | {pc(r['fpr_shuffle'])} | {'yes' if valid(code, k) else ('no (borderline)' if borderline(code, k) else '**no**')} |")
    return '\n'.join(out)

def T_cohort():
    P, S, A, G = DE['ref_progressors'], DE['ref_stable'], DE['artes'], DE['grape']
    mq = lambda q, d=1: f"{q['median']:.{d}f} ({q['q1']:.{d}f}{' to ' if q['q1'] < 0 else '–'}{q['q3']:.{d}f})"
    return '\n'.join([
        '| Characteristic | UWHVF reference progressors | UWHVF reference stable | Artes retest (true no change) | GRAPE (external) |', '|---|---|---|---|---|',
        f"| Patients / eyes, n | {P['n_patients']} / {P['n_eyes']} | {S['n_patients']} / {S['n_eyes']} | {A['n_patients']} / {A['n_series']} | {G['n_patients']} / {G['n_eyes']} |",
        f"| Age at first test, years | {mq(P['age0'])} | {mq(S['age0'])} | not used | {mq(G['age'])} |",
        f"| Female patients, n (%) | {P['female_patients']} ({100 * P['female_patients'] / P['n_patients']:.0f}%) | {S['female_patients']} ({100 * S['female_patients'] / S['n_patients']:.0f}%) | not available | {G['female_patients']} ({100 * G['female_patients'] / G['n_patients']:.0f}%) |",
        f"| Tests per eye, n | {mq(P['n_tests'], 0)} | {mq(S['n_tests'], 0)} | {A['n_fields'] // A['n_series']} | {mq(G['n_visits'], 0)} |",
        f"| Follow-up, years | {mq(P['followup_y'])} | {mq(S['followup_y'])} | {mq(dict((k, v / 365.25) for k, v in A['span_days'].items() if k in ('median', 'q1', 'q3')), 2)} | {mq(G['followup_y'])} |",
        f"| Time from first to third test, years | {mq(P['years_to_test3'])} | {mq(S['years_to_test3'])} | 2 weeks by design | not computed |",
        f"| Mean total deviation at first test, dB | {mq(P['md_baseline_proxy'])} | {mq(S['md_baseline_proxy'])} | not available | not available |",
        f"| Mean sensitivity, dB | not shown | not shown | {mq(A['md_proxy'])} | not shown |",
        f"| Progression label positive, n | {P['n_eyes']} (reference) | 0 | 0 (by design) | {G['md_label_pos']} (MD criterion) |"])

def T_grape():
    out = ['| Detector | k | Sensitivity, % (95% CI) | Specificity, % (95% CI) |', '|---|---|---|---|']
    for k in (3, 4):
        for code in ['D1', 'D2', 'D3', 'D4', 'D5', 'D7', 'D8']:
            r = row(code, k)
            if r.get('grape_sens') is None: continue
            out.append(f"| {SHORT[code]} | {k} | {pc(r['grape_sens'])} ({pc(r['grape_sens_lo'])}–{pc(r['grape_sens_hi'])}) | "
                       f"{pc(r['grape_spec'])} ({pc(r['grape_spec_lo'])}–{pc(r['grape_spec_hi'])}) |")
    return '\n'.join(out)

TABLES = dict(main=T_main, cohort=T_cohort, grape=T_grape)

def sub(m):
    a = m.group(1).split(':'); t = a[0]
    if t == 'd': return fmt(dig(DE, a[1]), a[2])
    if t == 's': return fmt(RQ3[a[1]], a[2])
    if t == 'm': return f"{META['runtime_s'] / 60:.0f}"
    if t == 'p': return pc(val(a[1], a[2], a[3])) + '%'
    if t == 'ci':
        c, d, k = a[1:]; return f"{pc(val(c, d, k))}% (95% CI {pc(val(c + '_lo', d, k))}–{pc(val(c + '_hi', d, k))}%)"
    if t == 'sd': return f"{100 * val(a[1] + '_seed_sd', a[2], a[3]):.1f}"
    if t == 'n': return f"{int(val(a[1] + '_n', a[2], a[3])):,}"
    if t == 'f1000': return f"{1000 * val('fpr_true_null', a[1], a[2]):.0f}"
    if t == 'dt':
        r = pair(*a[1:]); sg = '+' if r['diff'] > 0 else '−' if r['diff'] < 0 else ''
        return (f"{sg}{abs(100 * r['diff']):.1f} percentage points (95% CI {100 * r['diff_lo']:.1f} to {100 * r['diff_hi']:.1f}; "
                f"Holm-adjusted p {pv(r['p_holm'])})")
    if t == 'ttd': return f"{100 * DE['time_to_detection_ref_progressors'][det_name(a[1])]['detected_by6_mean']:.0f}%"
    if t == 'table': return TABLES[a[1]]()
    if t == 'x':
        w = a[1]
        if w == 'cum': return f"{100 * EX['cumulative_false_alarm_artes_start0'][a[2]]['any_flag_k3_to_6']:.1f}%"
        if w == 'mdd_pp': return f"{100 * EX['min_significant_gain']['gain']:.1f}"
        if w == 'mdd_eyes': return str(EX['min_significant_gain']['discordant_eyes'])
        if w == 'rho_ci': lo, hi = EX['rho_cell_bootstrap_ci']; return f"{lo:.2f} to {hi:.2f}"
        if w == 'd1hi': return ', '.join(f"{100 * EX['D1_fpr_hi_by_k'][str(k)]:.1f}%" for k in (3, 4, 5, 6))
        if w == 'strict_list':
            cells = {}
            for c in EX['strict_valid_cells']:
                d, k = c.split('@'); cells.setdefault(d, []).append(k)
            return '; '.join(f"{SHORT[d]} (k = {', '.join(sorted(v))})" for d, v in sorted(cells.items(), key=lambda kv: int(kv[0][1:])))
        if w == 'gplr': return f"{100 * EX['grape_secondary_labels'][a[2] + '@' + a[3]][a[4]][a[5]]:.1f}%"
        if w == 'grape_3visit': return str(DE['grape']['n_eyes'] - DE['grape']['eyes_ge4'])
        if w == 'sec_ref_prog': return str(int(row('D1', 3)['sens_ref2_n']))
        raise KeyError(m.group(0))
    if t == 'REFERENCES': return m.group(0)
    raise KeyError(m.group(0))

def fill(text):
    out = re.sub(r'\{\{(.+?)\}\}', sub, text)
    return re.sub(r'(?<![A-Za-z0-9])-(?=\d)', '−', out)   # typographic minus for negative numbers

# ---------- claim checks (every qualitative statement in the text is listed here) ----------
def CHECKS():
    c = {}
    ks = (3, 4, 5, 6); others = [f'D{i}' for i in range(2, 11)]
    c['D1 valid at all k'] = all(valid('D1', k) for k in ks)
    c['D6 invalid at k=3'] = not valid('D6', 3)
    c['D8 invalid at k=3,4,5'] = all(not valid('D8', k) for k in (3, 4, 5))
    c['D8 valid at k=6'] = valid('D8', 6)
    c['D9 invalid at k=3,5'] = not valid('D9', 3) and not valid('D9', 5)
    c['D6 sens gain k3 significant'] = pair('sens', 'D6', 3)['p_holm'] < 0.05 and pair('sens', 'D6', 3)['diff'] > 0
    # H2: no VALID detector beats D1 by >= 10 pp with Holm p < 0.05 at any k
    c['H2 not falsified'] = not any(valid(d, k) and pair('sens', d, k)['diff'] >= 0.10 and pair('sens', d, k)['p_holm'] < 0.05 for d in others for k in ks)
    c['only significant sens gain is invalid'] = all((not valid(d, k)) for d in others for k in ks if pair('sens', d, k)['p_holm'] < 0.05 and pair('sens', d, k)['diff'] > 0)
    c['exactly one significant sens gain'] = sum(pair('sens', d, k)['p_holm'] < 0.05 and pair('sens', d, k)['diff'] > 0 for d in others for k in ks) == 1
    c['no specificity difference vs D1 significant'] = all(pair('fp', d, k)['p_holm'] >= 0.05 for d in others for k in ks)
    c['D4, D7, D10 never flag at k=3'] = all(val('sens', d, 3) == 0 and val('fpr_true_null', d, 3) == 0 for d in ('D4', 'D7', 'D10'))
    c['D2 k3 valid on Artes but shuffle >5%'] = valid('D2', 3) and val('fpr_shuffle', 'D2', 3) > 0.10
    c['D7 shuffle > true null at k=6'] = val('fpr_shuffle', 'D7', 6) - val('fpr_true_null', 'D7', 6) > 0.05
    c['D2 k3 gain not significant'] = pair('sens', 'D2', 3)['p_holm'] >= 0.05
    c['D8 k6 gain not significant'] = pair('sens', 'D8', 6)['p_holm'] >= 0.05
    c['D3 lower than D1 at k6 significant'] = pair('sens', 'D3', 6)['p_holm'] < 0.05 and pair('sens', 'D3', 6)['diff'] < 0
    c['H3 rho below 0.7'] = RQ3['spearman_rho'] < 0.7
    c['H3 >=50% within 3pp'] = RQ3['share_within_3pp'] >= 0.5
    c['GRAPE D8 more FP than D1 k3 and k4 significant'] = all(pair('gfp', 'D8', k)['p_holm'] < 0.05 and pair('gfp', 'D8', k)['diff'] > 0 for k in (3, 4))
    c['GRAPE D2 more FP than D1 k3 significant'] = pair('gfp', 'D2', 3)['p_holm'] < 0.05 and pair('gfp', 'D2', 3)['diff'] > 0
    c['GRAPE D8,D2 sens gain k3 not significant'] = all(pair('gsens', d, 3)['p_holm'] >= 0.05 for d in ('D2', 'D8'))
    c['GRAPE D5 within 5pp of D1 at k3'] = abs(val('grape_sens', 'D5', 3) - val('grape_sens', 'D1', 3)) < 0.05
    c['D6 ref2 sens > D1 ref2 sens at k3'] = val('sens_ref2', 'D6', 3) > val('sens_ref2', 'D1', 3)
    c['D5 equals D1 sens at k3-5, within 1pp at k6'] = all(abs(val('sens', 'D5', k) - val('sens', 'D1', k)) < 1e-9 for k in (3, 4, 5)) and abs(val('sens', 'D5', 6) - val('sens', 'D1', 6)) < 0.01
    c['D1 FA rate within 3.5-5.5% at all k'] = all(0.035 <= val('fpr_true_null', 'D1', k) <= 0.055 for k in ks)
    c['D8 most sensitive at k6'] = max(ks and [val('sens', d, 6) for d in ['D1'] + others]) == val('sens', 'D8', 6)
    c['D6 and D8 highest ttd'] = sorted(DE['time_to_detection_ref_progressors'].items(), key=lambda kv: -kv[1]['detected_by6_mean'])[0][0].split()[0] in ('D8', 'D6')
    inval = sorted((d, k) for d in ['D1'] + others for k in ks if not valid(d, k))
    c['invalid cells exactly as stated'] = inval == sorted([('D6', 3), ('D8', 3), ('D9', 3), ('D8', 4), ('D8', 5), ('D9', 5), ('D6', 6), ('D9', 6)])
    c['D9 k6 upper limit just above 10%'] = 0.10 < row('D9', 6)['fpr_true_null_hi'] < 0.101
    c['D3 max FA at k3'] = max(val('fpr_true_null', 'D3', k) for k in ks) == val('fpr_true_null', 'D3', 3)
    c['min spec is D9 k6'] = min(val('spec', d, k) for d in ['D1'] + others for k in ks) == val('spec', 'D9', 6)
    c['D6 highest ref2 sens at k3'] = max(val('sens_ref2', d, 3) for d in ['D1'] + others) == val('sens_ref2', 'D6', 3)
    c['D7 highest sens among valid at k5'] = max(val('sens', d, 5) for d in ['D1'] + others if valid(d, 5)) == val('sens', 'D7', 5)
    c['shuffle flags D6,D8 at k3 (>10%)'] = val('fpr_shuffle', 'D6', 3) > 0.10 and val('fpr_shuffle', 'D8', 3) > 0.10
    c['shuffle underestimates D9 k3'] = val('fpr_shuffle', 'D9', 3) < val('fpr_true_null', 'D9', 3)
    c['GRAPE D3,D4,D7 sens <=5% at k3'] = all(val('grape_sens', d, 3) <= 0.05 for d in ('D3', 'D4', 'D7'))
    c['D6 spec >= 95% at k3'] = val('spec', 'D6', 3) >= 0.95
    c['D9 k6 borderline'] = borderline('D9', 6)
    sv = set(EX['strict_valid_cells'])
    c['strict rule: D1 fails all k'] = not any(f'D1@{k}' in sv for k in ks)
    c['strict rule: no strict-valid detector has significant sens gain'] = not any(f'{d}@{k}' in sv and pair('sens', d, k)['p_holm'] < 0.05 and pair('sens', d, k)['diff'] > 0 for d in others for k in ks)
    cum = EX['cumulative_false_alarm_artes_start0']
    c['D7 lowest cumulative FA among D1,D2,D6,D7,D8'] = min(cum[d]['any_flag_k3_to_6'] for d in ('D1', 'D2', 'D6', 'D7', 'D8')) == cum['D7']['any_flag_k3_to_6']
    c['D6,D8 highest cumulative FA'] = sorted(cum, key=lambda d: -cum[d]['any_flag_k3_to_6'])[:2] == ['D8', 'D6']
    c['D7 sens >= D1 at k5,k6'] = val('sens', 'D7', 5) >= val('sens', 'D1', 5) and val('sens', 'D7', 6) >= val('sens', 'D1', 6)
    c['D7 sens gain at k5 not significant'] = pair('sens', 'D7', 5)['p_holm'] >= 0.05
    c['ref2 valid D7,D10,D8 > D1 at k6'] = all(val('sens_ref2', d, 6) > val('sens_ref2', 'D1', 6) and valid(d, 6) for d in ('D7', 'D10', 'D8'))
    c['shuffle lower than true for D6 at k6'] = val('fpr_shuffle', 'D6', 6) < val('fpr_true_null', 'D6', 6)
    c['GRAPE PLR2 spec D8 < D1'] = EX['grape_secondary_labels']['D8@3']['PLR2']['spec'] < EX['grape_secondary_labels']['D1@3']['PLR2']['spec']
    c['D1 misses most at k3,k4'] = val('sens', 'D1', 3) < 0.5 and val('sens', 'D1', 4) < 0.5
    c['D8 highest sens at k6'] = max(val('sens', d, 6) for d in ['D1'] + others) == val('sens', 'D8', 6)
    bad = [k for k, v in c.items() if not v]
    assert not bad, f'CLAIM CHECK FAILED: {bad}'
    return c

def renumber(text):
    order = []
    def collect(m):
        for part in re.split(r',\s*', m.group(1)):
            rng = [int(x) for x in re.split(r'[–-]', part)]
            for n in (range(rng[0], rng[-1] + 1) if len(rng) == 2 else rng):
                if n not in order: order.append(n)
    CIT = re.compile(r'\[(\d+(?:\s*[–-]\s*\d+)?(?:,\s*\d+(?:\s*[–-]\s*\d+)?)*)\]')
    for m in CIT.finditer(text): collect(m)
    new = {old: i + 1 for i, old in enumerate(order)}
    def rewrite(m):
        nums = []
        for part in re.split(r',\s*', m.group(1)):
            rng = [int(x) for x in re.split(r'[–-]', part)]
            nums += list(range(rng[0], rng[-1] + 1)) if len(rng) == 2 else rng
        ns = sorted({new[n] for n in nums}); out = []; i = 0
        while i < len(ns):
            j = i
            while j + 1 < len(ns) and ns[j + 1] == ns[j] + 1: j += 1
            out.append(f"{ns[i]}–{ns[j]}" if j - i >= 2 else ', '.join(str(x) for x in ns[i:j + 1])); i = j + 1
        return '[' + ', '.join(out) + ']'
    text = CIT.sub(rewrite, text)
    unused = [i + 1 for i in range(len(REFS)) if i + 1 not in order]
    refs = '\n\n'.join(f"{new[o]}. {REFS[o - 1]['vancouver'].replace('&amp;', '&')}" for o in order)
    return text, refs, unused

if __name__ == '__main__':
    checks = CHECKS()
    body = '\n\n'.join(open(os.path.join(HERE, f)).read().strip() for f in
                       ('front_template.md', 'sections_intro_methods.md', 'results_discussion_template.md', 'back_template.md'))
    body = fill(body)
    body, refs, unused = renumber(body)
    assert not unused, f'uncited references: {unused}'
    body = body.replace('{{REFERENCES}}', refs)
    assert '{{' not in body, re.findall(r'\{\{.*?\}\}', body)
    open(os.path.join(HERE, 'manuscript_filled.md'), 'w').write(body)
    legends = json.load(open(os.path.join(HERE, 'figure_legends_template.json')))
    legends = [[f, fill(l)] for f, l in legends]
    json.dump(legends, open(os.path.join(HERE, 'figure_legends.json'), 'w'), indent=1)
    open(os.path.join(HERE, 'cover_letter_filled.md'), 'w').write(fill(open(os.path.join(HERE, 'cover_letter_template.md')).read()))
    json.dump(checks, open(os.path.join(HERE, 'claim_checks.json'), 'w'), indent=1)
    # word counts
    main = body.split('# Introduction')[1].split('# Declarations')[0]
    abstract = body.split('## Abstract')[1].split('## Keywords')[0] if '## Abstract' in body else ''
    wc = lambda t: len(re.findall(r"[A-Za-z0-9][\w'’.%–-]*", re.sub(r'\|.*\|', '', t)))
    print(f'claims OK ({len(checks)}); main text words ~{wc(main)}; abstract words ~{wc(abstract)}')
