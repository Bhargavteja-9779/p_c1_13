"""Summaries for the A3 cross-fitted analysis (run_v2.py).
Usage: python -m src.statistics.summarise_v2 -> results/metrics_v2.json, statistics_v2.json, tables/table_v2_*.csv
Unit of analysis: eye (E1/E1F/E1S), Artes window (E2), shuffled eye series (E3); CIs = patient-cluster bootstrap (2,000).
Paired comparisons vs D1: exact McNemar on seed-majority flags + Holm within (k, endpoint); effect = difference in
proportions with patient-cluster paired bootstrap CI. Seed robustness: per-seed estimates and rank flips."""
import os, json, sys
import numpy as np, pandas as pd
from scipy import stats
from .tests import holm
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
B = 2000

def cluster(ev, unit):
    if ev == 'E2': return 'A' + unit.split('|')[0][:-2]          # Artes patient id (strip OD/OS)
    return unit.split('|')[0][:-1]                                 # UWHVF patient id (strip L/R)

def boot(u, seed=0):
    g = u.groupby('cluster')['flag'].agg(['sum', 'count']); s, n = g['sum'].to_numpy(), g['count'].to_numpy()
    rng = np.random.default_rng(seed); idx = rng.integers(0, len(g), (B, len(g)))
    bs = s[idx].sum(1) / np.maximum(n[idx].sum(1), 1)
    return float(s.sum() / n.sum()), float(np.quantile(bs, .025)), float(np.quantile(bs, .975)), int(n.sum()), int(len(g))

def main(path=None):
    path = path or os.path.join(ROOT, 'results', 'raw_results_v2.csv')
    d = pd.read_csv(path, dtype={'unit': str})
    d['cluster'] = [cluster(e, u) for e, u in zip(d['eval'], d['unit'])]
    ENDS = [('E1', 1, 'sens'), ('E1', 0, 'fp_ref'), ('E1F', 1, 'sens_future'), ('E1F', 0, 'fp_future'),
            ('E1S', 0, 'fp_future_sym'), ('E2', 0, 'fpr_true_null'), ('E3', 0, 'fpr_shuffle')]
    rows, seedrows = [], []
    for (det, k), g in d.groupby(['detector', 'k']):
        r = dict(detector=det, k=int(k))
        for ev, lab, key in ENDS:
            x = g[(g['eval'] == ev) & (g.label == lab)]
            if not len(x): continue
            u = x.groupby(['unit', 'cluster'], as_index=False)['flag'].mean()   # seed-averaged per unit
            est, lo, hi, n, nc = boot(u)
            r.update({key: est, key + '_lo': lo, key + '_hi': hi, key + '_n': n, key + '_clusters': nc})
            ps = x.groupby('seed')['flag'].mean()
            r[key + '_seed_sd'] = float(ps.std(ddof=1)) if len(ps) > 1 else 0.0
            for s_, v in ps.items(): seedrows.append(dict(detector=det, k=int(k), endpoint=key, seed=int(s_), value=float(v)))
        rows.append(r)
    M = pd.DataFrame(rows).sort_values(['k', 'detector'])
    # paired comparisons vs D1
    tests = []
    for k in sorted(d.k.unique()):
        for ev, lab, key in [('E1', 1, 'sens'), ('E1F', 1, 'sens_future'), ('E1', 0, 'fp_ref'), ('E1F', 0, 'fp_future')]:
            sub = d[(d.k == k) & (d['eval'] == ev) & (d.label == lab)]
            base = sub[sub.detector == 'D1 OLS-MD'].groupby(['unit', 'cluster'])['flag'].mean().round()
            res = []
            for det in sorted(sub.detector.unique()):
                if det == 'D1 OLS-MD': continue
                o = sub[sub.detector == det].groupby(['unit', 'cluster'])['flag'].mean().round()
                j = base.index.intersection(o.index); a, b = o[j].to_numpy(), base[j].to_numpy()
                b01, b10 = int(((a == 1) & (b == 0)).sum()), int(((a == 0) & (b == 1)).sum())
                p = 1.0 if b01 + b10 == 0 else float(stats.binomtest(min(b01, b10), b01 + b10, .5).pvalue)
                cl = np.array([c for _, c in j]); uc, inv = np.unique(cl, return_inverse=True)
                diff = a - b; sd = np.bincount(inv, diff); sn = np.bincount(inv)
                rng = np.random.default_rng(0); idx = rng.integers(0, len(uc), (B, len(uc)))
                bs = sd[idx].sum(1) / sn[idx].sum(1)
                res.append(dict(k=int(k), endpoint=key, detector=det, n=len(j), diff=float(diff.mean()),
                                diff_lo=float(np.quantile(bs, .025)), diff_hi=float(np.quantile(bs, .975)), p=p,
                                only_det=b01, only_D1=b10))
            for r_, a_ in zip(res, holm([r_['p'] for r_ in res])): r_['p_holm'] = float(a_)
            tests += res
    T = pd.DataFrame(tests)
    # seed-rank robustness: for each (k, endpoint), rank detectors per seed; report whether ranking vs D1 flips
    SR = pd.DataFrame(seedrows); flips = []
    for (k, ep), g in SR.groupby(['k', 'endpoint']):
        d1 = g[g.detector == 'D1 OLS-MD'].set_index('seed')['value']
        for det, h in g.groupby('detector'):
            if det == 'D1 OLS-MD' or len(h) < 2: continue
            s = np.sign(h.set_index('seed')['value'] - d1.reindex(h.seed).fillna(d1.iloc[0]))
            flips.append(dict(k=int(k), endpoint=ep, detector=det, n_seeds=len(h), above_D1=int((s > 0).sum()),
                              below_D1=int((s < 0).sum()), tie=int((s == 0).sum())))
    F = pd.DataFrame(flips)
    c = M.dropna(subset=['fpr_true_null', 'fpr_shuffle'])
    rho = stats.spearmanr(c.fpr_shuffle, c.fpr_true_null); ad = (c.fpr_shuffle - c.fpr_true_null).abs()
    rq3 = dict(n_cells=len(c), spearman_rho=float(rho.statistic), spearman_p=float(rho.pvalue), median_abs_diff=float(ad.median()),
               share_within_3pp=float((ad <= .03).mean()), max_abs_diff=float(ad.max()))
    os.makedirs(os.path.join(ROOT, 'tables'), exist_ok=True)
    M.to_csv(os.path.join(ROOT, 'tables', 'table_v2_metrics.csv'), index=False)
    T.to_csv(os.path.join(ROOT, 'tables', 'table_v2_paired_vs_D1.csv'), index=False)
    F.to_csv(os.path.join(ROOT, 'tables', 'table_v2_seed_rank_flips.csv'), index=False)
    json.dump(json.loads(M.to_json(orient='records')), open(os.path.join(ROOT, 'results', 'metrics_v2.json'), 'w'), indent=1)
    json.dump(dict(paired_tests=json.loads(T.to_json(orient='records')), rq3_audit_concordance=rq3,
                   n_comparisons_total=len(T)), open(os.path.join(ROOT, 'results', 'statistics_v2.json'), 'w'), indent=1)
    pd.set_option('display.width', 250)
    print(M[['detector', 'k', 'sens', 'sens_future', 'fp_ref', 'fp_future_sym', 'fpr_true_null', 'fpr_true_null_lo', 'fpr_shuffle']].round(3).to_string())
    print(rq3)

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else None)
