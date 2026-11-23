"""POST HOC sensitivity analyses added after adversarial review (2026-11-23). Not pre-registered; reported as such.
(a) Future-only reference (review I03): the reference label for an eye at k tests is computed only from tests k+1..end
    (>= 5 remaining tests). Progressor: slope of mean TD < -0.3 dB/yr with one-sided p < 0.01 (as primary).
    Stable (two definitions): 'p>0.5' as primary, and 'no evidence' = one-sided p >= 0.05 or slope >= -0.3 dB/yr... see code.
(b) GRAPE restricted to eyes with >= k + 2 visits (review I09), with the pre-specified secondary labels PLR2, PLR3, any.
(c) Patient-cluster bootstrap CIs for paired sensitivity differences vs D1 (review I05).
(d) Exact (Clopper-Pearson) intervals for E1 sensitivity / specificity, eye level (review I06).
(e) Validity under three readings (review I01): 'significantly above nominal' (lower CI > 5%), manuscript rule
    (lower <= 5% and upper <= 10%), strict protocol reading (upper <= 5%).
Writes results/posthoc_sensitivity.json. Usage (from code/): python -m src.statistics.sensitivity"""
import os, sys, json
import numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.data.uwhvf import load_series, patient_split
from src.data.grape import load_grape
from src.models.deferral import ols, md_series

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RES = os.path.join(ROOT, 'results')
B = 2000


def cp(x, n):
    if n == 0: return (None, None)
    lo = 0.0 if x == 0 else stats.beta.ppf(.025, x, n - x + 1)
    hi = 1.0 if x == n else stats.beta.ppf(.975, x + 1, n - x)
    return float(lo), float(hi)


def cluster_boot(df, col, seed=0):
    """df: unit, cluster, col. Mean with patient-cluster bootstrap 95% CI."""
    g = df.groupby('cluster')[col].agg(['sum', 'count']); s, n = g['sum'].to_numpy(float), g['count'].to_numpy(float)
    rng = np.random.default_rng(seed); idx = rng.integers(0, len(g), (B, len(g)))
    bs = s[idx].sum(1) / np.maximum(n[idx].sum(1), 1)
    return float(s.sum() / n.sum()), float(np.quantile(bs, .025)), float(np.quantile(bs, .975)), int(n.sum())


def main():
    raw = pd.read_csv(os.path.join(RES, 'raw_results.csv.gz'), dtype={'unit': str, 'extra': str})
    M = json.load(open(os.path.join(RES, 'metrics.json')))
    out = {}
    # (e) validity readings
    out['validity'] = [dict(detector=m['detector'], k=m['k'], fpr=m['fpr_true_null'], lo=m['fpr_true_null_lo'], hi=m['fpr_true_null_hi'],
                            above_nominal=m['fpr_true_null_lo'] > 0.05,
                            manuscript_rule=m['fpr_true_null_lo'] <= 0.05 and m['fpr_true_null_hi'] <= 0.10,
                            strict_protocol=m['fpr_true_null_hi'] <= 0.05) for m in M]
    # majority-over-seeds flag per unit
    F = raw.groupby(['detector', 'k', 'eval', 'unit'])['flag'].mean().round().reset_index()
    E1 = F[F['eval'] == 'E1']
    # (a) future-only reference
    S = load_series(); sp = patient_split(S)
    T = {s['pid'] + s['eye']: s for s in S if sp[s['pid']] == 'test'}
    rows = []
    for k in (3, 4, 5, 6):
        for u, s in T.items():
            if len(s['ages']) - k < 5: continue
            t = s['ages'][k:] - s['ages'][k]; y = md_series(s['td'][k:])
            b, p, _ = ols(t, y)
            prog = b < -0.3 and p < 0.01
            rows.append(dict(k=k, unit=u, cluster=s['pid'], prog=int(prog), stable_p05=int((not prog) and p > 0.5),
                             stable_noev=int((not prog) and not (b < -0.3 and p < 0.05)), n_future=len(t)))
    R = pd.DataFrame(rows)
    fo = []
    for (det, k), g in E1.groupby(['detector', 'k']):
        r = R[R.k == k].merge(g[['unit', 'flag']], on='unit', how='left')
        # eyes with >= k + 5 tests are all in E1 (E1 = test eyes with >= 8 tests), but guard anyway
        r = r.dropna(subset=['flag'])
        d = dict(detector=det, k=int(k))
        for lab, key in (('prog', 'sens'), ('stable_p05', 'spec_p05'), ('stable_noev', 'spec_noev')):
            x = r[r[lab] == 1]
            if not len(x): continue
            col = x.assign(v=x.flag if key == 'sens' else 1 - x.flag)
            est, lo, hi, n = cluster_boot(col, 'v')
            d.update({key: est, key + '_lo': lo, key + '_hi': hi, key + '_n': n})
        fo.append(d)
    out['future_only_reference'] = fo
    out['future_only_counts'] = {int(k): dict(n_eyes=int(len(g)), prog=int(g.prog.sum()), stable_p05=int(g.stable_p05.sum()),
                                              stable_noev=int(g.stable_noev.sum())) for k, g in R.groupby('k')}
    # (d) exact intervals for primary E1
    ex = []
    for (det, k), g in raw[raw['eval'] == 'E1'].groupby(['detector', 'k']):
        u = g.groupby(['unit', 'label'])['flag'].mean().round().reset_index()
        p, s_ = u[u.label == 1], u[u.label == 0]
        ex.append(dict(detector=det, k=int(k), sens_x=int(p.flag.sum()), sens_n=len(p), sens_cp=cp(int(p.flag.sum()), len(p)),
                       spec_x=int((1 - s_.flag).sum()), spec_n=len(s_), spec_cp=cp(int((1 - s_.flag).sum()), len(s_))))
    out['exact_e1'] = ex
    # (c) cluster bootstrap paired differences (sensitivity vs D1), primary reference
    e1 = raw[raw['eval'] == 'E1'].groupby(['detector', 'k', 'unit', 'label'])['flag'].mean().round().reset_index()
    e1['cluster'] = e1.unit.str[:-1]
    pdiff = []
    for k in (3, 4, 5, 6):
        base = e1[(e1.detector == 'D1 OLS-MD') & (e1.k == k) & (e1.label == 1)].set_index('unit')
        for det in sorted(e1.detector.unique()):
            if det == 'D1 OLS-MD': continue
            o = e1[(e1.detector == det) & (e1.k == k) & (e1.label == 1)].set_index('unit')
            j = base.index.intersection(o.index)
            df = pd.DataFrame(dict(cluster=base.loc[j, 'cluster'], v=o.loc[j, 'flag'] - base.loc[j, 'flag']))
            est, lo, hi, n = cluster_boot(df, 'v')
            pdiff.append(dict(detector=det, k=k, diff=est, lo=lo, hi=hi, n=n))
    out['paired_sens_cluster_ci'] = pdiff
    # minimum detectable difference (approximate): with n=26 progressors, exact McNemar, Holm over 9 tests ->
    # smallest number of discordant pairs all in one direction that gives Holm-adjusted p < 0.05 for the best test
    alpha = 0.05 / 9
    mdd = next(n for n in range(1, 27) if 2 * 0.5 ** n < alpha)
    out['min_discordant_all_one_direction_for_holm'] = dict(n_discordant=mdd, as_pp_of_26=100 * mdd / 26)
    # (b) GRAPE restricted to eyes with >= k + 2 visits; secondary labels
    G = {g['pid'] + g['eye']: g for g in load_grape()}
    E4 = F[F['eval'] == 'E4']
    gr = []
    for (det, k), g in E4.groupby(['detector', 'k']):
        for restrict in (False, True):
            for lab in ('MD', 'PLR2', 'PLR3', 'any'):
                rr = []
                for _, r in g.iterrows():
                    e = G[r.unit]
                    if restrict and len(e['t']) < k + 2: continue
                    y = int(e['PLR2'] or e['PLR3'] or e['MD']) if lab == 'any' else int(e[lab])
                    rr.append(dict(cluster=e['pid'], y=y, flag=r.flag))
                rr = pd.DataFrame(rr)
                d = dict(detector=det, k=int(k), restricted=restrict, label=lab, n=len(rr), n_pos=int(rr.y.sum()))
                for key, sub, v in (('sens', rr[rr.y == 1], 'flag'), ('spec', rr[rr.y == 0], None)):
                    if len(sub):
                        sub = sub.assign(v=sub.flag if key == 'sens' else 1 - sub.flag)
                        est, lo, hi, n = cluster_boot(sub, 'v'); d.update({key: est, key + '_lo': lo, key + '_hi': hi})
                gr.append(d)
    out['grape_restricted_and_labels'] = gr
    json.dump(out, open(os.path.join(RES, 'posthoc_sensitivity.json'), 'w'), indent=1)
    return out


if __name__ == '__main__':
    o = main()
    print(o['future_only_counts'], o['min_discordant_all_one_direction_for_holm'])
    for r in o['future_only_reference']:
        print(r['detector'][:3], r['k'], *(f"{k}={100*r.get(k, float('nan')):.1f}" for k in ('sens', 'spec_p05', 'spec_noev')))
    for r in o['grape_restricted_and_labels']:
        if r['label'] in ('MD',) and r['restricted']:
            print('GRAPE>=k+2', r['detector'][:3], r['k'], r['n'], r['n_pos'], f"{100*r.get('sens',float('nan')):.1f} {100*r.get('spec',float('nan')):.1f}")
