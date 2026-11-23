"""Revision R1 statistics (responds to review round 1; v1 outputs in results/*.json are kept unchanged for the record).
Changes vs v1 (all disclosed in the manuscript's deviations table):
 - ONE estimand: each unit's flag is averaged over seeds (deterministic detectors: one seed); proportions AND paired
   differences use these seed-mean flags (v1 used majority-vote flags for differences).
 - Paired-difference CIs use a PATIENT-cluster bootstrap (v1 resampled eyes, contrary to the Methods).
 - Exact McNemar tests use majority-vote flags (binary needed); Holm within (k, endpoint) over APPLICABLE detectors only.
 - D4, D7, D10 at k = 3 are 'not applicable' (cannot flag by design) and excluded from counts and Holm families.
 - Validity reported under three rules: literal protocol (CI upper <= 5%), operational A3 (upper <= 10% and lower <= 5%),
   and 'clearly excessive' (CI lower > 5%).
 - Adds pre-registered outputs missing in v1: GRAPE PLR2 / PLR3 / any-criterion labels, secondary-reference specificity,
   cluster-bootstrap CI for the audit rho; and exploratory analyses requested by reviewers: cumulative false alarms over
   serial looks (k = 3..6) on the true no-change arm, a future-only reference (tests k+1..end), audit rho restricted to
   applicable cells.
Usage (from code/): python -m src.statistics.summarise_v2  -> ../results/v2/{metrics,statistics,extras}.json"""
import os, sys, json
import numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.statistics.tests import holm
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'results', 'v2'); B = 2000
NA_K3 = ('D4', 'D7', 'D10')

def code(det): return det.split()[0]
def applicable(det, k): return not (int(k) == 3 and code(det) in NA_K3)
def cluster_of(ev, unit):
    if ev == 'E2': return 'A' + unit.split('|')[0]
    if ev == 'E3': return 'U' + unit.split('|')[0][:-1]
    if ev == 'E1': return 'U' + unit[:-1]
    return 'G' + unit[:-2]

def boot_prop(u, seed=0):
    """u: DataFrame(cluster, flag in [0,1]). Ratio estimator with patient-cluster bootstrap."""
    g = u.groupby('cluster')['flag'].agg(['sum', 'count']); s, n = g['sum'].to_numpy(), g['count'].to_numpy()
    if n.sum() == 0: return None
    rng = np.random.default_rng(seed); idx = rng.integers(0, len(g), size=(B, len(g)))
    bs = s[idx].sum(1) / n[idx].sum(1)
    return dict(est=float(s.sum() / n.sum()), lo=float(np.quantile(bs, .025)), hi=float(np.quantile(bs, .975)), n=int(n.sum()))

def unit_means(d):
    return d.groupby(['detector', 'k', 'eval', 'unit', 'cluster'], as_index=False).agg(flag=('flag', 'mean'), label=('label', 'first'), extra=('extra', 'first'))

def main():
    os.makedirs(OUT, exist_ok=True)
    d = pd.read_csv(os.path.join(ROOT, 'results', 'raw_results.csv.gz'), dtype={'unit': str, 'extra': str}, low_memory=False)
    d['cluster'] = [cluster_of(e, u) for e, u in zip(d['eval'], d['unit'])]
    majority = d.groupby(['detector', 'k', 'eval', 'unit'])['flag'].mean().round()   # .5 -> 0 (banker's rounding) documented
    U = unit_means(d)
    g4 = U['eval'] == 'E4'
    for lab in ('PLR2', 'PLR3'):
        U.loc[g4, lab] = U.loc[g4, 'extra'].str.extract(lab + r'=(\d)')[0].astype(float)
    U.loc[g4, 'ANY'] = U.loc[g4, ['label', 'PLR2', 'PLR3']].max(axis=1)
    U['ref2'] = pd.to_numeric(U['extra'].where(U['eval'] == 'E1'), errors='coerce')
    # ---------------- metrics ----------------
    rows = []
    for (det, k), g in U.groupby(['detector', 'k']):
        r = dict(detector=det, k=int(k), applicable=applicable(det, k))
        def put(key, x, invert=False):
            res = boot_prop(x[['cluster', 'flag']])
            if res is None: return
            if invert: res = dict(est=1 - res['est'], lo=1 - res['hi'], hi=1 - res['lo'], n=res['n'])
            r.update({key: res['est'], key + '_lo': res['lo'], key + '_hi': res['hi'], key + '_n': res['n']})
        e1, e2, e3, e4 = (g[g['eval'] == e] for e in ('E1', 'E2', 'E3', 'E4'))
        put('sens', e1[e1.label == 1]); put('spec', e1[e1.label == 0], True)
        put('sens_ref2', e1[e1.ref2 == 1]); put('spec_ref2', e1[e1.ref2 == 0], True)
        put('fpr_true_null', e2); put('fpr_shuffle', e3)
        for lab, nm in (('label', 'md'), ('PLR2', 'plr2'), ('PLR3', 'plr3'), ('ANY', 'any')):
            if len(e4): put(f'grape_{nm}_sens', e4[e4[lab] == 1]); put(f'grape_{nm}_spec', e4[e4[lab] == 0], True)
        # per-seed SD of the true-null FPR and sensitivity
        raw = d[(d.detector == det) & (d.k == k)]
        for key, sub in (('sens', raw[(raw['eval'] == 'E1') & (raw.label == 1)]), ('fpr_true_null', raw[raw['eval'] == 'E2'])):
            ps = sub.groupby('seed')['flag'].mean(); r[key + '_seed_sd'] = float(ps.std(ddof=1)) if len(ps) > 1 else 0.0
        if 'fpr_true_null' in r:
            lo, hi = r['fpr_true_null_lo'], r['fpr_true_null_hi']
            r['valid_literal'] = bool(hi <= 0.05) if r['applicable'] else None
            r['valid_A3'] = bool(hi <= 0.10 and lo <= 0.05) if r['applicable'] else None
            r['clearly_excessive'] = bool(lo > 0.05) if r['applicable'] else None
        rows.append(r)
    M = pd.DataFrame(rows).sort_values(['k', 'detector'])
    # ---------------- paired comparisons vs D1 ----------------
    tests = []
    EP = [('E1', 'label', 1, 'sensitivity'), ('E1', 'label', 0, 'false positives (1-spec)'),
          ('E4', 'label', 1, 'GRAPE MD sensitivity'), ('E4', 'label', 0, 'GRAPE MD false positives'),
          ('E4', 'PLR2', 1, 'GRAPE PLR2 sensitivity'), ('E4', 'PLR2', 0, 'GRAPE PLR2 false positives')]
    for k in sorted(U.k.unique()):
        for ev, col, val, ep in EP:
            sel = (U.k == k) & (U['eval'] == ev) & (U[col] == val)
            base = U[sel & (U.detector == 'D1 OLS-MD')].set_index('unit')
            res = []
            for det in sorted(U.detector.unique(), key=lambda s: int(code(s)[1:])):
                if det == 'D1 OLS-MD' or not applicable(det, k): continue
                o = U[sel & (U.detector == det)].set_index('unit')
                j = base.index.intersection(o.index)
                if len(j) == 0: continue
                diff = o.loc[j, 'flag'].to_numpy() - base.loc[j, 'flag'].to_numpy()
                cl = base.loc[j, 'cluster'].to_numpy(); ucl, inv = np.unique(cl, return_inverse=True)
                ssum = np.bincount(inv, diff); scnt = np.bincount(inv)
                rng = np.random.default_rng(0); idx = rng.integers(0, len(ucl), size=(B, len(ucl)))
                bs = ssum[idx].sum(1) / scnt[idx].sum(1)
                a = np.array([majority[(det, k, ev, u)] for u in j]); b = np.array([majority[('D1 OLS-MD', k, ev, u)] for u in j])
                b01 = int(((a == 1) & (b == 0)).sum()); b10 = int(((a == 0) & (b == 1)).sum())
                p = 1.0 if b01 + b10 == 0 else float(stats.binomtest(min(b01, b10), b01 + b10, 0.5).pvalue)
                res.append(dict(k=int(k), endpoint=ep, detector=det, n=len(j), n_patients=len(ucl), diff=float(diff.mean()),
                                diff_lo=float(np.quantile(bs, .025)), diff_hi=float(np.quantile(bs, .975)),
                                p=p, only_det=b01, only_D1=b10))
            if res:
                for r, a in zip(res, holm([r['p'] for r in res])): r['p_holm'] = float(a)
                tests += res
    T = pd.DataFrame(tests)
    # ---------------- RQ3 audit concordance with cluster-bootstrap CI ----------------
    ex = {}
    def cell_table(ev):
        x = U[U['eval'] == ev].copy(); x['cell'] = x.detector + '|' + x.k.astype(str)
        return x.pivot_table(index=['cluster', 'unit'], columns='cell', values='flag')
    A_, S_ = cell_table('E2'), cell_table('E3')
    cells = [c for c in A_.columns if c in S_.columns]
    def rho_for(cs, Ai, Si):
        a = Ai[cs].mean().to_numpy(); s = Si[cs].mean().to_numpy(); return stats.spearmanr(s, a).statistic, np.median(np.abs(s - a)), np.mean(np.abs(s - a) <= .03)
    appl = [c for c in cells if applicable(c.split('|')[0], c.split('|')[1])]
    for name, cs in (('all_cells', cells), ('applicable_cells', appl)):
        est = rho_for(cs, A_, S_)
        ca, cs_ = A_.index.get_level_values(0).unique(), S_.index.get_level_values(0).unique()
        rng = np.random.default_rng(0); bs = []
        for _ in range(500):
            ia = rng.choice(ca, len(ca)); is_ = rng.choice(cs_, len(cs_))
            bs.append(rho_for(cs, A_.loc[list(ia)], S_.loc[list(is_)])[0])
        ex['rq3_' + name] = dict(n_cells=len(cs), spearman_rho=float(est[0]), rho_lo=float(np.nanquantile(bs, .025)),
                                 rho_hi=float(np.nanquantile(bs, .975)), median_abs_diff=float(est[1]), share_within_3pp=float(est[2]),
                                 bootstrap='500 joint resamples of Artes and UWHVF patients')
    # ---------------- cumulative false alarms over looks k=3..6 (Artes; exploratory) ----------------
    e2 = U[U['eval'] == 'E2'].copy(); e2['start'] = e2.unit.str.split('|').str[1].astype(int)
    e2['draw'] = e2.unit.str.split('|').str[2]; e2['pid'] = e2.unit.str.split('|').str[0]
    cum = {}
    for det, g in e2[e2.start <= 6].groupby('detector'):
        w = g.pivot_table(index=['pid', 'start', 'draw', 'cluster'], columns='k', values='flag')
        # probability of >= 1 flag across looks, treating per-look seed-mean flags as probabilities
        pany = 1 - np.prod(1 - w[[3, 4, 5, 6]].to_numpy(), axis=1)
        u = pd.DataFrame(dict(cluster=w.index.get_level_values('cluster'), flag=pany))
        cum[det] = boot_prop(u)
    ex['cumulative_true_null_any_flag_k3to6'] = cum
    ex['cumulative_note'] = ('Windows starting at tests 1-7 (so tests 1..6 of the window exist); each look k uses the first k '
                             'tests of the window with its own donor time labels (draw index d); seed-mean flags treated as '
                             'per-look flag probabilities, combined as 1 - prod(1 - p).')
    # ---------------- future-only reference (exploratory; F2) ----------------
    from src.data.uwhvf import load_series, patient_split
    from src.models.deferral import ols, md_series
    S = load_series(); sp = patient_split(S); byu = {s['pid'] + s['eye']: s for s in S if sp[s['pid']] == 'test'}
    fut = []
    e1 = U[U['eval'] == 'E1']
    for (det, k), g in e1.groupby(['detector', 'k']):
        labs = []
        for u in g.unit:
            s = byu[u]; t = s['ages'][k:] - s['ages'][k]; y = md_series(s['td'][k:])
            if len(t) < 5: labs.append(np.nan); continue
            b, p, _ = ols(t, y); labs.append(1.0 if (b < -0.3 and p < 0.01) else (0.0 if p > 0.5 else np.nan))
        g = g.assign(fut=labs)
        r = dict(detector=det, k=int(k))
        for key, sub, inv in (('sens_future', g[g.fut == 1], False), ('spec_future', g[g.fut == 0], True)):
            res = boot_prop(sub[['cluster', 'flag']])
            if res:
                if inv: res = dict(est=1 - res['est'], lo=1 - res['hi'], hi=1 - res['lo'], n=res['n'])
                r.update({key: res['est'], key + '_lo': res['lo'], key + '_hi': res['hi'], key + '_n': res['n']})
        fut.append(r)
    ex['future_only_reference'] = fut
    ex['future_only_note'] = ('Exploratory: among the E1 eyes (primary or secondary reference), reference recomputed from tests '
                              'k+1..end only (>= 5 tests required), same thresholds as the primary reference.')
    # ---------------- reference-group descriptions (M5) ----------------
    from run_all import reference
    slopes = {}
    for u, s in byu.items():
        if len(s['ages']) >= 8:
            lab = reference(s)
            if lab is not None:
                b, p, _ = ols(s['ages'] - s['ages'][0], md_series(s['td'])); slopes.setdefault(int(lab), []).append(b)
    ex['reference_slopes_dB_per_year'] = {str(k): dict(n=len(v), median=float(np.median(v)), q1=float(np.quantile(v, .25)),
                                           q3=float(np.quantile(v, .75)), share_positive=float(np.mean(np.array(v) > 0)))
                                          for k, v in slopes.items()}
    json.dump(json.loads(M.to_json(orient='records')), open(os.path.join(OUT, 'metrics.json'), 'w'), indent=1)
    json.dump(dict(paired_tests=json.loads(T.to_json(orient='records'))), open(os.path.join(OUT, 'statistics.json'), 'w'), indent=1)
    json.dump(ex, open(os.path.join(OUT, 'extras.json'), 'w'), indent=1, default=float)
    print(M[['detector', 'k', 'sens', 'spec', 'fpr_true_null', 'fpr_true_null_lo', 'fpr_true_null_hi', 'valid_literal', 'valid_A3', 'clearly_excessive']].round(3).to_string())
    print(json.dumps({k: v for k, v in ex.items() if k.startswith('rq3') or k.startswith('reference')}, indent=1))

if __name__ == '__main__':
    main()
