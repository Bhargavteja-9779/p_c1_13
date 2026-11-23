"""Summarise amendment A3 (protocol.md). Usage (from code/): python experiments/summarise_a3.py
Inputs: ../results/a3_raw.csv.gz (A3a, A3c), ../results/raw_results.csv.gz (A3b and D1 comparators).
Output: ../results/a3_summary.json, ../tables/table_A3_*.csv"""
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np, pandas as pd
from scipy import stats
from src.statistics.summarise import boot_prop, cluster_of
from src.statistics.tests import holm
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); RES = os.path.join(ROOT, 'results')
B = 2000


def prop(df, ev):
    """df: rows with unit, flag (any seeds). Seed-mean per unit, patient-cluster bootstrap."""
    u = df.groupby('unit', as_index=False)['flag'].mean(); u['cluster'] = [cluster_of(ev, x) for x in u.unit]
    return boot_prop(u)


def paired(a, b, ev):
    """a, b: Series unit -> seed-mean flag. Majority-vote flags; exact McNemar; patient-cluster bootstrap of difference."""
    j = a.index.intersection(b.index); x = a[j].round().to_numpy(); y = b[j].round().to_numpy()
    b01, b10 = int(((x == 1) & (y == 0)).sum()), int(((x == 0) & (y == 1)).sum())
    p = 1.0 if b01 + b10 == 0 else float(stats.binomtest(min(b01, b10), b01 + b10).pvalue)
    d = pd.Series(x - y, index=j).groupby([cluster_of(ev, u) for u in j]).agg(['sum', 'count'])
    ix = np.random.default_rng(0).integers(0, len(d), (B, len(d)))
    bs = d['sum'].to_numpy()[ix].sum(1) / d['count'].to_numpy()[ix].sum(1)
    return dict(n=len(j), diff=float((x - y).mean()), diff_lo=float(np.quantile(bs, .025)), diff_hi=float(np.quantile(bs, .975)),
                only_det=b01, only_D1=b10, p=p)


def valid(lo, hi): return bool(hi <= 0.10 and lo <= 0.05)


def main():
    a3 = pd.read_csv(os.path.join(RES, 'a3_raw.csv.gz'), dtype={'unit': str}, low_memory=False)
    raw = pd.read_csv(os.path.join(RES, 'raw_results.csv.gz'), dtype={'unit': str, 'extra': str}, low_memory=False)
    out = {}
    d1 = raw[raw.detector == 'D1 OLS-MD']
    # ---------- A3a SCT ----------
    rows, tests = [], []
    for (det, k), g in a3[a3['eval'].isin(['E1', 'E2', 'E4'])].groupby(['det', 'k']):
        r = dict(detector=det, k=int(k))
        for ev, lab, key in [('E1', 1, 'sens'), ('E1', 0, 'fp'), ('E2', None, 'fpr_true_null'), ('E4', 1, 'grape_sens'), ('E4', 0, 'grape_fp')]:
            x = g[g['eval'] == ev]
            if lab is not None: x = x[x.label == lab]
            if len(x) == 0: continue
            e, lo, hi, n = prop(x, ev)
            if key.endswith('fp'):
                key = 'spec' if key == 'fp' else 'grape_spec'; e, lo, hi = 1 - e, 1 - hi, 1 - lo
            r.update({key: e, key + '_lo': lo, key + '_hi': hi, key + '_n': n})
            r[key + '_seed_range'] = [float(v) for v in (x.groupby('seed').flag.mean().agg(['min', 'max']))]
        r['valid'] = valid(r['fpr_true_null_lo'], r['fpr_true_null_hi'])
        r['excess'] = bool(r['fpr_true_null_lo'] > 0.05)
        rows.append(r)
    for k in (3, 4, 5, 6):
        res = []
        base = d1[(d1.k == k) & (d1['eval'] == 'E1') & (d1.label == 1)].groupby('unit').flag.mean()
        for det, g in a3[(a3.k == k) & (a3['eval'] == 'E1') & (a3.label == 1)].groupby('det'):
            res.append(dict(detector=det, k=k, endpoint='sensitivity', **paired(g.groupby('unit').flag.mean(), base, 'E1')))
        for r_, a_ in zip(res, holm([x['p'] for x in res])): r_['p_holm'] = float(a_)
        tests += res
        if k in (3, 4):
            for lab, ep in ((1, 'GRAPE sensitivity'), (0, 'GRAPE false positives')):
                base = d1[(d1.k == k) & (d1['eval'] == 'E4') & (d1.label == lab)].groupby('unit').flag.mean()
                res = [dict(detector=det, k=k, endpoint=ep, **paired(g.groupby('unit').flag.mean(), base, 'E4'))
                       for det, g in a3[(a3.k == k) & (a3['eval'] == 'E4') & (a3.label == lab)].groupby('det')]
                for r_, a_ in zip(res, holm([x['p'] for x in res])): r_['p_holm'] = float(a_)
                tests += res
    SCT, ST = pd.DataFrame(rows), pd.DataFrame(tests)
    SCT.to_csv(os.path.join(ROOT, 'tables', 'table_A3a_sct.csv'), index=False)
    ST.to_csv(os.path.join(ROOT, 'tables', 'table_A3a_sct_tests_vs_D1.csv'), index=False)
    thr = a3[a3['eval'] == 'THR'].groupby(['det', 'k']).extra.agg(lambda v: [float(x) for x in v]).reset_index()
    out['A3a_sct'] = json.loads(SCT.to_json(orient='records')); out['A3a_tests'] = json.loads(ST.to_json(orient='records'))
    out['A3a_thresholds'] = json.loads(thr.to_json(orient='records'))
    out['H5_supported'] = bool(not SCT.excess.any()); out['H5_all_valid'] = bool(SCT.valid.all())
    s6 = ST[ST.endpoint == 'sensitivity']
    out['H6_falsified'] = bool(((s6['diff'] >= 0.10) & (s6.p_holm < 0.05)).any())
    # ---------- A3b confirmation ----------
    conf = []
    for det, g in raw[raw['eval'].isin(['E1', 'E2'])].groupby('detector'):
        for ev in ('E1', 'E2'):
            x = g[g['eval'] == ev]
            w = x.pivot_table(index=['seed', 'unit'], columns='k', values='flag', aggfunc='max')
            lab = x.groupby('unit').label.first() if ev == 'E1' else None
            for k in (4, 5, 6):
                if k not in w or k - 1 not in w: continue
                c = (w[k].fillna(0) * w[k - 1].fillna(0)).reset_index(name='flag')
                c = c[w[k].notna().to_numpy()]
                if ev == 'E1':
                    c = c[c.unit.map(lab) == 1]; key = 'sens_confirmed'
                else: key = 'fpr_true_null_confirmed'
                e, lo, hi, n = prop(c, ev)
                conf.append(dict(detector=det, k=k, measure=key, est=e, lo=lo, hi=hi, n=n))
    C = pd.DataFrame(conf); C.to_csv(os.path.join(ROOT, 'tables', 'table_A3b_confirmation.csv'), index=False)
    out['A3b_confirmation'] = json.loads(C.to_json(orient='records'))
    # ---------- A3c enlarged reference ----------
    e = a3[a3['eval'] == 'E1all']; rows, tests = [], []
    for (det, k), g in e.groupby(['det', 'k']):
        s_ = prop(g[g.label == 1], 'E1'); f_ = prop(g[g.label == 0], 'E1')
        rows.append(dict(detector=det, k=int(k), sens=s_[0], sens_lo=s_[1], sens_hi=s_[2], n_prog=s_[3],
                         spec=1 - f_[0], spec_lo=1 - f_[2], spec_hi=1 - f_[1], n_stable=f_[3]))
    for k in (3, 4, 5, 6):
        for lab, ep in ((1, 'sensitivity'), (0, 'false positives')):
            gk = e[(e.k == k) & (e.label == lab)]
            base = gk[gk.det == 'D1 OLS-MD'].groupby('unit').flag.mean()
            res = [dict(detector=det, k=k, endpoint=ep, **paired(g.groupby('unit').flag.mean(), base, 'E1'))
                   for det, g in gk[gk.det != 'D1 OLS-MD'].groupby('det')]
            for r_, a_ in zip(res, holm([x['p'] for x in res])): r_['p_holm'] = float(a_)
            tests += res
    E, ET = pd.DataFrame(rows), pd.DataFrame(tests)
    E.to_csv(os.path.join(ROOT, 'tables', 'table_A3c_enlarged_reference.csv'), index=False)
    ET.to_csv(os.path.join(ROOT, 'tables', 'table_A3c_tests_vs_D1.csv'), index=False)
    out['A3c_enlarged'] = json.loads(E.to_json(orient='records')); out['A3c_tests'] = json.loads(ET.to_json(orient='records'))
    h8 = ET[(ET.k == 3) & (ET.endpoint == 'sensitivity') & ET.detector.str.startswith('D2')].iloc[0]
    out['H8_supported'] = bool(h8['diff'] > 0 and h8.p_holm < 0.05)
    out['meta'] = json.load(open(os.path.join(RES, 'a3_meta.json')))
    json.dump(out, open(os.path.join(RES, 'a3_summary.json'), 'w'), indent=1)
    pd.set_option('display.width', 250)
    c = ['detector', 'k', 'sens', 'spec', 'fpr_true_null', 'fpr_true_null_lo', 'fpr_true_null_hi', 'valid'] + [x for x in ('grape_sens', 'grape_spec') if x in SCT]
    print(SCT[c].round(3).to_string()); print(ST.round(3).to_string())
    print(C.round(3).to_string()); print(E.round(3).to_string()); print(ET.round(3).to_string())
    print({k: v for k, v in out.items() if k.startswith('H')})


if __name__ == '__main__':
    main()
