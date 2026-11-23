"""Pre-specified Study 2 analyses (protocol_v2.md). Inputs: results/study2_raw.csv(.gz), study2_refs.csv.
Outputs: results/study2_metrics.json, results/study2_stats.json, tables/study2_*.csv.  Run from code/."""
import os, sys, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np, pandas as pd
from scipy import stats
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RES = os.path.join(ROOT, 'results'); TAB = os.path.join(ROOT, 'tables')
B = 2000; KS = (3, 4, 5, 6)
PERLOOK = ['D1 OLS-MD', 'D7 Event', 'S1 SC-Trend', 'S2 SC-Rate', 'S3 SC-PoPLR', 'S4 SC-Event', 'S5 SC-LightGBM',
           'S6 Order-LightGBM', 'S7 SC-GRU', 'B8 LightGBM-95spec']
HOLM_SET = ['D7 Event', 'S1 SC-Trend', 'S2 SC-Rate', 'S3 SC-PoPLR', 'S4 SC-Event', 'S5 SC-LightGBM', 'S6 Order-LightGBM', 'S7 SC-GRU']
CUM = ['D1-repeated', 'D7-repeated', 'Q1 Sequential trend', 'Q2 Confirmed trend', 'Q3 Confirmed SC-Event', 'Q4 Sequential Order-LightGBM']

def boot(vals, clusters, seed=0):
    """Cluster bootstrap of a mean. vals: per-unit values; clusters: per-unit cluster ids."""
    vals = np.asarray(vals, float); cl = pd.Series(clusters)
    codes, uniq = pd.factorize(cl); sums = np.bincount(codes, vals); cnts = np.bincount(codes)
    rng = np.random.default_rng(seed); est = vals.mean(); bs = []
    for _ in range(B):
        i = rng.integers(0, len(uniq), len(uniq)); bs.append(sums[i].sum() / cnts[i].sum())
    return float(est), float(np.quantile(bs, .025)), float(np.quantile(bs, .975)), int(len(vals))

def boot_diff(a, b, clusters, seed=0):
    d = np.asarray(a, float) - np.asarray(b, float); return boot(d, clusters, seed)

def mcnemar(a, b):
    b01 = int(((a == 1) & (b == 0)).sum()); b10 = int(((a == 0) & (b == 1)).sum()); n = b01 + b10
    p = 1.0 if n == 0 else float(min(1.0, 2 * stats.binom.cdf(min(b01, b10), n, 0.5)))
    return p, b01, b10

def holm(ps):
    ps = np.asarray(ps); o = np.argsort(ps); adj = np.empty(len(ps)); run = 0
    for r, i in enumerate(o):
        run = max(run, (len(ps) - r) * ps[i]); adj[i] = min(1.0, run)
    return adj.tolist()

def main(suffix=''):
    p = os.path.join(RES, f'study2_raw{suffix}.csv')
    d = pd.read_csv(p if os.path.exists(p) else p + '.gz', dtype={'unit': str})
    refs = pd.read_csv(os.path.join(RES, f'study2_refs{suffix}.csv'), dtype={'unit': str, 'pid': str}).set_index('unit').drop(columns=['fold'])
    out = {'metrics': [], 'cumulative': [], 'paired': [], 'paired_cum': [], 'grape': [], 'seed_sd': []}
    # ---------- E1 per look
    e1 = d[d['eval'] == 'E1']
    u1 = e1.groupby(['detector', 'k', 'unit'])['flag'].agg(['mean', lambda x: x.mean().round()]).reset_index()
    u1.columns = ['detector', 'k', 'unit', 'flag', 'maj']
    u1 = u1.join(refs, on='unit')
    e2 = d[d['eval'] == 'E2'].copy(); e2['pid'] = e2.unit.str.split('|').str[0]
    u2 = e2.groupby(['detector', 'k', 'unit', 'pid'])['flag'].mean().reset_index()
    for det in PERLOOK:
        for k in KS:
            r = dict(detector=det, k=k); x = u1[(u1.detector == det) & (u1.k == k)]
            for key, lab, val in (('sens', 'R1', 1), ('spec', 'R1', 0), ('spec_R2', 'R2', 0), ('sens_R3', f'R3_{k}', 1), ('spec_R3', f'R3_{k}', 0)):
                y = x[x[lab] == val]
                if len(y) == 0: continue
                v = y.flag if key.startswith('sens') else 1 - y.flag
                e, lo, hi, n = boot(v, y.pid); r.update({key: e, key + '_lo': lo, key + '_hi': hi, key + '_n': n})
            z = u2[(u2.detector == det) & (u2.k == k)]
            e, lo, hi, n = boot(z.flag, z.pid); r.update(fa=e, fa_lo=lo, fa_hi=hi, fa_n=n)
            r['valid'] = bool(lo <= 0.05 and hi <= 0.10); r['valid_strict'] = bool(hi <= 0.05)
            # seed SD of sensitivity
            ps = e1[(e1.detector == det) & (e1.k == k)].join(refs, on='unit')
            ps = ps[ps.R1 == 1].groupby('seed').flag.mean(); r['sens_seed_sd'] = float(ps.std(ddof=1)) if len(ps) > 1 else 0.0
            out['metrics'].append(r)
    # ---------- paired vs D1 (per look): sensitivity R1, specificity R1, R2
    for k in KS:
        for endpoint, lab, val in (('sens', 'R1', 1), ('spec_R1', 'R1', 0), ('spec_R2', 'R2', 0)):
            base = u1[(u1.detector == 'D1 OLS-MD') & (u1.k == k) & (u1[lab] == val)].set_index('unit')
            res = []
            for det in HOLM_SET + ['B8 LightGBM-95spec']:
                o = u1[(u1.detector == det) & (u1.k == k) & (u1[lab] == val)].set_index('unit').loc[base.index]
                pv, b01, b10 = mcnemar(o.maj.values, base.maj.values)
                e, lo, hi, n = boot_diff(o.flag.values, base.flag.values, base.pid.values)
                if endpoint != 'sens': e, lo, hi = -e, -hi, -lo          # specificity difference
                res.append(dict(k=k, endpoint=endpoint, detector=det, n=n, diff=e, diff_lo=lo, diff_hi=hi, p=pv, only_det=b01, only_D1=b10))
            adj = holm([r['p'] for r in res if r['detector'] in HOLM_SET])
            for r, a in zip([r for r in res if r['detector'] in HOLM_SET], adj): r['p_holm'] = a
            for r in res:
                r.setdefault('p_holm', None)
            out['paired'] += res
    # ---------- cumulative (E1cum, E2cum): flagged at any look up to k
    c1 = d[d['eval'] == 'E1cum'].sort_values('k'); c1['cum'] = c1.groupby(['fold', 'seed', 'detector', 'unit']).flag.cummax()
    cu1 = c1.groupby(['detector', 'k', 'unit']).cum.agg(['mean', lambda x: x.mean().round()]).reset_index()
    cu1.columns = ['detector', 'k', 'unit', 'flag', 'maj']; cu1 = cu1.join(refs, on='unit')
    c2 = d[d['eval'] == 'E2cum'].sort_values('k'); c2['cum'] = c2.groupby(['fold', 'seed', 'detector', 'unit']).flag.cummax()
    c2['pid'] = c2.unit.str.split('|').str[0]
    cu2 = c2.groupby(['detector', 'k', 'unit', 'pid']).cum.mean().reset_index().rename(columns={'cum': 'flag'})
    for det in CUM:
        for k in KS:
            r = dict(detector=det, k=k)
            x = cu1[(cu1.detector == det) & (cu1.k == k)]
            for key, lab, val in (('sens', 'R1', 1), ('spec', 'R1', 0), ('spec_R2', 'R2', 0)):
                y = x[x[lab] == val]; v = y.flag if key == 'sens' else 1 - y.flag
                e, lo, hi, n = boot(v, y.pid); r.update({key: e, key + '_lo': lo, key + '_hi': hi, key + '_n': n})
            z = cu2[(cu2.detector == det) & (cu2.k == k)]; e, lo, hi, n = boot(z.flag, z.pid)
            r.update(fa=e, fa_lo=lo, fa_hi=hi, fa_n=n); out['cumulative'].append(r)
    # H8: each Q vs D1-repeated, cumulative sensitivity at k = 6 (one-sided 95% CI = 5th percentile)
    base = cu1[(cu1.detector == 'D1-repeated') & (cu1.k == 6) & (cu1.R1 == 1)].set_index('unit')
    for det in CUM[1:]:
        o = cu1[(cu1.detector == det) & (cu1.k == 6) & (cu1.R1 == 1)].set_index('unit').loc[base.index]
        dlt = o.flag.values - base.flag.values; cl = pd.factorize(base.pid)[0]; rng = np.random.default_rng(0); bs = []
        sums = np.bincount(cl, dlt); cnt = np.bincount(cl)
        for _ in range(B):
            i = rng.integers(0, cnt.size, cnt.size); bs.append(sums[i].sum() / cnt[i].sum())
        pv, b01, b10 = mcnemar(o.maj.values, base.maj.values)
        out['paired_cum'].append(dict(detector=det, diff=float(dlt.mean()), lo_one_sided_95=float(np.quantile(bs, .05)),
                                      lo95=float(np.quantile(bs, .025)), hi95=float(np.quantile(bs, .975)), p_mcnemar=pv,
                                      only_det=b01, only_D1=b10, noninferior_10pp=bool(np.quantile(bs, .05) > -0.10)))
    # time of first flag (years from first test) among R1 progressors flagged by look 6 (majority over seeds/folds)
    from src.data.uwhvf import load_series as _ls
    tt = {s['pid'] + s['eye']: s['ages'] - s['ages'][0] for s in _ls()}
    ttf = []
    for det in CUM:
        x = cu1[(cu1.detector == det) & (cu1.R1 == 1)].pivot_table(index='unit', columns='k', values='maj')
        first = x.apply(lambda r: next((k for k in KS if r[k] == 1), None), axis=1).dropna()
        yrs = [tt[u][int(k) - 1] for u, k in first.items()]
        ttf.append(dict(detector=det, n_detected=int(len(first)), n=int(len(x)), median_years=float(np.median(yrs)) if yrs else None,
                        median_look=float(np.median(first.values)) if len(first) else None))
    out['time_to_first_flag'] = ttf
    # ---------- GRAPE
    e4 = d[d['eval'] == 'E4'].copy()
    e4['pid'] = e4.unit.str.extract(r'^(\d+)')[0]
    for lab in ('MD', 'PLR2', 'PLR3'): e4[lab] = e4.unit.str.extract(lab + r'=(\d)')[0].astype(int)
    u4 = e4.groupby(['detector', 'k', 'unit', 'pid', 'MD', 'PLR2', 'PLR3']).flag.agg(['mean', lambda x: x.mean().round()]).reset_index()
    u4.columns = ['detector', 'k', 'unit', 'pid', 'MD', 'PLR2', 'PLR3', 'flag', 'maj']
    for (det, k), x in u4.groupby(['detector', 'k']):
        r = dict(detector=det, k=int(k))
        for lab in ('MD', 'PLR2', 'PLR3'):
            for key, val in (('sens', 1), ('spec', 0)):
                y = x[x[lab] == val]; v = y.flag if key == 'sens' else 1 - y.flag
                e, lo, hi, n = boot(v, y.pid); r.update({f'{key}_{lab}': e, f'{key}_{lab}_lo': lo, f'{key}_{lab}_hi': hi, f'{key}_{lab}_n': n})
        out['grape'].append(r)
    # ---------- Study 1 locked-test subset (consistency)
    from src.data.uwhvf import load_series, patient_split
    sp = patient_split(load_series()); test_pids = {p for p, v in sp.items() if v == 'test'}
    sub = []
    for det in PERLOOK:
        for k in KS:
            y = u1[(u1.detector == det) & (u1.k == k) & (u1.R1 == 1) & (u1.pid.isin(test_pids))]
            sub.append(dict(detector=det, k=k, sens=float(y.flag.mean()) if len(y) else None, n=int(len(y))))
    out['study1_test_subset'] = sub
    os.makedirs(TAB, exist_ok=True)
    pd.DataFrame(out['metrics']).to_csv(os.path.join(TAB, f'study2_perlook{suffix}.csv'), index=False)
    pd.DataFrame(out['cumulative']).to_csv(os.path.join(TAB, f'study2_cumulative{suffix}.csv'), index=False)
    pd.DataFrame(out['paired']).to_csv(os.path.join(TAB, f'study2_paired{suffix}.csv'), index=False)
    pd.DataFrame(out['grape']).to_csv(os.path.join(TAB, f'study2_grape{suffix}.csv'), index=False)
    json.dump(out, open(os.path.join(RES, f'study2_metrics{suffix}.json'), 'w'), indent=1)
    M = pd.DataFrame(out['metrics'])
    print(M[['detector', 'k', 'sens', 'spec', 'spec_R2', 'fa', 'fa_hi', 'valid']].round(3).to_string())
    print(pd.DataFrame(out['cumulative'])[['detector', 'k', 'sens', 'spec_R2', 'fa']].round(3).to_string())
    P = pd.DataFrame(out['paired']); print(P[(P.endpoint == 'sens')][['k', 'detector', 'diff', 'diff_lo', 'diff_hi', 'p_holm']].round(3).to_string())
    print(pd.DataFrame(out['paired_cum']).round(3).to_string()); print(pd.DataFrame(ttf).round(2).to_string())
    print(pd.DataFrame(out['grape'])[['detector', 'k', 'sens_MD', 'spec_MD', 'spec_PLR2']].round(3).to_string())

if __name__ == '__main__':
    main(sys.argv[1] if len(sys.argv) > 1 else '')
