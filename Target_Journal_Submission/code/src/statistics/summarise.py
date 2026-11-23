"""Summaries with patient-cluster bootstrap CIs, McNemar vs D1 with Holm correction, audit concordance (RQ3).
Usage: python -m src.statistics.summarise [raw_results.csv]  -> results/metrics.json, statistics.json, tables/*.csv"""
import sys, os, json
import numpy as np, pandas as pd
from scipy import stats
from .tests import holm
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
B = 2000

def cluster_of(ev, unit):
    if ev == 'E2': return unit.split('|')[0]
    if ev == 'E3': return unit.split('|')[0][:-1]          # patient id (strip eye letter)
    return unit[:-1] if ev == 'E1' else unit[:-2] if unit.endswith(('OD', 'OS')) else unit

def boot_prop(df, col='flag', seed=0):
    """Mean of col with patient-cluster bootstrap 95% CI. df has columns cluster, col."""
    g = df.groupby('cluster')[col].agg(['sum', 'count']); s, n = g['sum'].to_numpy(), g['count'].to_numpy()
    est = s.sum() / n.sum() if n.sum() else np.nan
    rng = np.random.default_rng(seed); idx = rng.integers(0, len(g), size=(B, len(g)))
    bs = s[idx].sum(1) / np.maximum(n[idx].sum(1), 1)
    return float(est), float(np.quantile(bs, .025)), float(np.quantile(bs, .975)), int(n.sum())

def mcnemar(a, b):
    b01 = int(((a == 1) & (b == 0)).sum()); b10 = int(((a == 0) & (b == 1)).sum()); n = b01 + b10
    return 1.0 if n == 0 else float(stats.binomtest(min(b01, b10), n, 0.5).pvalue), b01, b10

def main(path=None):
    path = path or os.path.join(ROOT, 'results', 'raw_results.csv')
    d = pd.read_csv(path, dtype={'unit': str, 'extra': str})
    d['cluster'] = [cluster_of(e, u) for e, u in zip(d['eval'], d['unit'])]
    metrics = []
    for (det, k), g in d.groupby(['detector', 'k']):
        row = dict(detector=det, k=int(k))
        # average over seeds: per unit mean flag (seed-averaged) for point estimate; seed SD reported separately
        for ev, sub, key in [('E1', lambda x: x[x.label == 1], 'sens'), ('E1', lambda x: x[x.label == 0], 'spec_fp'),
                             ('E2', lambda x: x, 'fpr_true_null'), ('E3', lambda x: x, 'fpr_shuffle'),
                             ('E4', lambda x: x[x.label == 1], 'grape_sens'), ('E4', lambda x: x[x.label == 0], 'grape_fp')]:
            x = sub(g[g['eval'] == ev])
            if len(x) == 0: continue
            u = x.groupby(['unit', 'cluster'], as_index=False)['flag'].mean()
            est, lo, hi, n = boot_prop(u)
            per_seed = x.groupby('seed')['flag'].mean()
            if key in ('spec_fp', 'grape_fp'):
                est, lo, hi = 1 - est, 1 - hi, 1 - lo; key = key.replace('_fp', '_spec') if key == 'grape_fp' else 'spec'
                per_seed = 1 - per_seed
            row.update({key: est, key + '_lo': lo, key + '_hi': hi, key + '_n': n, key + '_seed_sd': float(per_seed.std(ddof=1)) if len(per_seed) > 1 else 0.0})
        # secondary reference (PoPLR) sensitivity on E1
        x = g[(g['eval'] == 'E1') & (g['extra'] == '1')]
        if len(x):
            u = x.groupby(['unit', 'cluster'], as_index=False)['flag'].mean(); est, lo, hi, n = boot_prop(u)
            row.update(sens_ref2=est, sens_ref2_lo=lo, sens_ref2_hi=hi, sens_ref2_n=n)
        metrics.append(row)
    M = pd.DataFrame(metrics).sort_values(['k', 'detector'])
    # paired tests vs D1 (seed-0 flags; stochastic detectors use majority over seeds)
    tests = []
    for k in sorted(d.k.unique()):
        for ev, lab, endpoint in [('E1', 1, 'sensitivity'), ('E1', 0, 'false positives (1-spec)'), ('E4', 1, 'GRAPE sensitivity'), ('E4', 0, 'GRAPE false positives')]:
            base = d[(d.detector == 'D1 OLS-MD') & (d.k == k) & (d['eval'] == ev) & (d.label == lab)].groupby('unit')['flag'].mean().round()
            res = []
            for det in sorted(d.detector.unique()):
                if det == 'D1 OLS-MD': continue
                o = d[(d.detector == det) & (d.k == k) & (d['eval'] == ev) & (d.label == lab)].groupby('unit')['flag'].mean().round()
                j = base.index.intersection(o.index)
                if len(j) == 0: continue
                p, b01, b10 = mcnemar(o[j].to_numpy(), base[j].to_numpy())
                diff = o[j].to_numpy() - base[j].to_numpy()
                rng = np.random.default_rng(0); bs = [diff[rng.integers(0, len(diff), len(diff))].mean() for _ in range(B)]
                res.append(dict(k=int(k), endpoint=endpoint, detector=det, n=len(j), diff=float(diff.mean()),
                                diff_lo=float(np.quantile(bs, .025)), diff_hi=float(np.quantile(bs, .975)), p=p, only_det=b01, only_D1=b10))
            if res:
                adj = holm([r['p'] for r in res])
                for r, a in zip(res, adj): r['p_holm'] = float(a)
                tests += res
    T = pd.DataFrame(tests)
    # RQ3 concordance between shuffle audit and true null
    c = M.dropna(subset=['fpr_true_null', 'fpr_shuffle'])
    rho = stats.spearmanr(c.fpr_shuffle, c.fpr_true_null)
    absdiff = (c.fpr_shuffle - c.fpr_true_null).abs()
    rq3 = dict(n_cells=len(c), spearman_rho=float(rho.statistic), spearman_p=float(rho.pvalue),
               median_abs_diff=float(absdiff.median()), share_within_3pp=float((absdiff <= 0.03).mean()),
               max_abs_diff=float(absdiff.max()))
    os.makedirs(os.path.join(ROOT, 'tables'), exist_ok=True)
    M.to_csv(os.path.join(ROOT, 'tables', 'table_metrics_all.csv'), index=False)
    T.to_csv(os.path.join(ROOT, 'tables', 'table_paired_tests_vs_D1.csv'), index=False)
    json.dump(json.loads(M.to_json(orient='records')), open(os.path.join(ROOT, 'results', 'metrics.json'), 'w'), indent=1)
    json.dump(dict(paired_tests=json.loads(T.to_json(orient='records')), rq3_audit_concordance=rq3),
              open(os.path.join(ROOT, 'results', 'statistics.json'), 'w'), indent=1)
    print(M[['detector', 'k', 'sens', 'spec', 'fpr_true_null', 'fpr_shuffle'] + [c for c in ['grape_sens', 'grape_spec'] if c in M]].round(3).to_string())
    print(rq3)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
