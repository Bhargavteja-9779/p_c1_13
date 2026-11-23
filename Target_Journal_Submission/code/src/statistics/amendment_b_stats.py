"""Statistics for protocol amendment B. Usage (from code/): python -m src.statistics.amendment_b_stats
Inputs: ../results/amendB/{scores,b3_all_eyes,b4_timelabels}.csv.gz  Output: ../results/amendB/amendB.json"""
import os, sys, json, hashlib
import numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.statistics.tests import holm
from src.statistics.summarise_v2 import boot_prop
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'results', 'amendB'); B = 2000
fold = lambda pid: int(hashlib.sha256(('artes' + pid).encode()).hexdigest()[:4], 16) % 5

def paired(base, other, cl_of):
    """base/other: Series unit -> seed-mean flag; returns diff with patient-cluster bootstrap CI, McNemar on majority."""
    j = base.index.intersection(other.index); diff = other[j].to_numpy() - base[j].to_numpy()
    cl = np.array([cl_of(u) for u in j]); ucl, inv = np.unique(cl, return_inverse=True)
    ssum, scnt = np.bincount(inv, diff), np.bincount(inv)
    idx = np.random.default_rng(0).integers(0, len(ucl), size=(B, len(ucl))); bs = ssum[idx].sum(1) / scnt[idx].sum(1)
    a, b = other[j].round().to_numpy(), base[j].round().to_numpy()
    b01, b10 = int(((a == 1) & (b == 0)).sum()), int(((a == 0) & (b == 1)).sum())
    p = 1.0 if b01 + b10 == 0 else float(stats.binomtest(min(b01, b10), b01 + b10, .5).pvalue)
    return dict(n=len(j), n_patients=len(ucl), diff=float(diff.mean()), diff_lo=float(np.quantile(bs, .025)),
                diff_hi=float(np.quantile(bs, .975)), p=p, only_det=b01, only_D1=b10)

def ci(u):
    r = boot_prop(u[['cluster', 'flag']]); return r

def b1():
    d = pd.read_csv(os.path.join(OUT, 'scores.csv.gz'), dtype={'unit': str})
    res, flags = [], {}
    for (det, k), g in d.groupby(['detector', 'k']):
        fl_e1, fl_e2 = {'SC': [], 'RC': []}, {'SC': [], 'RC': []}
        for seed, gs in g.groupby('seed'):
            sc = gs[gs['eval'] == 'SC'].score.to_numpy(); thr_sc = np.quantile(sc, .95)
            e2 = gs[gs['eval'] == 'E2'].copy(); e2['pid'] = e2.unit.str.split('|').str[0]; e2['fold'] = e2.pid.map(fold)
            thr_all = np.quantile(e2.score, .95)
            thr_f = {f: np.quantile(e2.score[e2.fold != f], .95) for f in range(5)}
            e1 = gs[gs['eval'] == 'E1']
            fl_e1['SC'].append(pd.Series((e1.score > thr_sc).astype(float).to_numpy(), index=e1.unit, name=seed))
            fl_e1['RC'].append(pd.Series((e1.score > thr_all).astype(float).to_numpy(), index=e1.unit, name=seed))
            fl_e2['SC'].append(pd.Series((e2.score > thr_sc).astype(float).to_numpy(), index=e2.unit))
            fl_e2['RC'].append(pd.Series((e2.score > e2.fold.map(thr_f)).astype(float).to_numpy(), index=e2.unit))
        lab = g[g['eval'] == 'E1'].drop_duplicates('unit').set_index('unit')['label']
        for cal in ('SC', 'RC'):
            f1 = pd.concat(fl_e1[cal], axis=1).mean(axis=1); f2 = pd.concat(fl_e2[cal], axis=1).mean(axis=1)
            flags[(det, k, cal)] = f1
            r = dict(detector=det, k=int(k), calibration=cal, n_seeds=len(fl_e1[cal]))
            u1 = pd.DataFrame(dict(flag=f1, label=lab.reindex(f1.index).to_numpy(), cluster=[u[:-1] for u in f1.index]))
            u2 = pd.DataFrame(dict(flag=f2.to_numpy(), cluster=[u.split('|')[0] for u in f2.index]))
            for key, x, inv in (('sens', u1[u1.label == 1], False), ('spec', u1[u1.label == 0], True), ('fpr_true_null', u2, False)):
                c = ci(x)
                if inv: c = dict(est=1 - c['est'], lo=1 - c['hi'], hi=1 - c['lo'], n=c['n'])
                r.update({key: c['est'], key + '_lo': c['lo'], key + '_hi': c['hi'], key + '_n': c['n']})
            r['no_excess'] = bool(r['fpr_true_null_lo'] <= .05 <= r['fpr_true_null_hi']) or bool(r['fpr_true_null_hi'] < .05)
            res.append(r)
        flags[('lab', k)] = lab
    R = pd.DataFrame(res)
    # HB3: matched (RC) comparison vs RC-calibrated D1; also SC
    tests = []
    for cal in ('RC', 'SC'):
        for k in (3, 4, 5, 6):
            lab = flags[('lab', k)]; base = flags[('D1 OLS-MD', k, cal)]
            for ep, lv in (('sensitivity', 1), ('false positives (1-spec)', 0)):
                bu = base[lab.reindex(base.index) == lv]; rows = []
                for det in ('D2 MD-rate <= -1 dB/yr', 'D6 Pooled-detrended conformal region-max', 'D8 ML-tabular (LightGBM)', 'D9 ML-sequence (GRU)'):
                    o = flags[(det, k, cal)]; o = o[lab.reindex(o.index) == lv]
                    rows.append(dict(calibration=cal, k=k, endpoint=ep, detector=det, **paired(bu, o, lambda u: u[:-1])))
                for r, a in zip(rows, holm([r['p'] for r in rows])): r['p_holm'] = float(a)
                tests += rows
    T = pd.DataFrame(tests)
    hb = dict(HB1_RC_no_excess_all=bool(R[R.calibration == 'RC'].no_excess.all()),
              HB1_RC_cells_no_excess=int(R[R.calibration == 'RC'].no_excess.sum()), HB1_cells=int((R.calibration == 'RC').sum()),
              HB2_SC_share_within_3pp=float((R[R.calibration == 'SC'].fpr_true_null.sub(.05).abs() <= .03).mean()),
              HB3_falsified=bool(((T.calibration == 'RC') & (T.endpoint == 'sensitivity') & (T['diff'] >= .10) & (T.p_holm < .05)).any()))
    return R, T, hb

def b3():
    d = pd.read_csv(os.path.join(OUT, 'b3_all_eyes.csv.gz'), dtype={'unit': str})
    d['cluster'] = d.unit.str[:-1]; res, tests = [], []
    for (det, k), g in d.groupby(['detector', 'k']):
        r = dict(detector=det, k=int(k))
        for key, x, inv in (('sens', g[g.label == 1], False), ('spec', g[g.label == 0], True)):
            c = ci(x)
            if inv: c = dict(est=1 - c['est'], lo=1 - c['hi'], hi=1 - c['lo'], n=c['n'])
            r.update({key: c['est'], key + '_lo': c['lo'], key + '_hi': c['hi'], key + '_n': c['n']})
        r['n_patients'] = int(g.cluster.nunique()); res.append(r)
    for k in (3, 4, 5, 6):
        for ep, lv in (('sensitivity', 1), ('false positives (1-spec)', 0)):
            g = d[(d.k == k) & (d.label == lv)]; base = g[g.detector == 'D1 OLS-MD'].set_index('unit').flag.astype(float)
            rows = [dict(k=k, endpoint=ep, detector=det, **paired(base, g[g.detector == det].set_index('unit').flag.astype(float), lambda u: u[:-1]))
                    for det in ('D2 MD-rate <= -1 dB/yr', 'D3 PLR >=3 points', 'D4 PoPLR (within-eye permutation)') if not (k == 3 and det.startswith('D4'))]
            for r, a in zip(rows, holm([r['p'] for r in rows])): r['p_holm'] = float(a)
            tests += rows
    counts = dict(eyes=int(d.unit.nunique()), patients=int(d.cluster.nunique()),
                  progressors=int(d[d.label == 1].unit.nunique()), stable=int(d[d.label == 0].unit.nunique()))
    return pd.DataFrame(res), pd.DataFrame(tests), counts

def b4():
    d = pd.read_csv(os.path.join(OUT, 'b4_timelabels.csv.gz'), dtype={'unit': str})
    d['cluster'] = d.unit.str.split('|').str[0]; res = []
    for (det, k, v), g in d.groupby(['detector', 'k', 'variant']):
        c = ci(g); res.append(dict(detector=det, k=int(k), variant=v, fpr=c['est'], fpr_lo=c['lo'], fpr_hi=c['hi'], n=c['n']))
    return pd.DataFrame(res)

def thresholds_and_ref2():
    """Calibrated thresholds by source (mean over seeds) and RC-flag sensitivity/specificity vs the secondary (PoPLR) reference."""
    d = pd.read_csv(os.path.join(OUT, 'scores.csv.gz'), dtype={'unit': str})
    raw = pd.read_csv(os.path.join(ROOT, 'results', 'raw_results.csv.gz'), dtype={'unit': str, 'extra': str}, low_memory=False)
    l2 = raw[(raw['eval'] == 'E1') & (raw.detector == 'D1 OLS-MD') & (raw.k == 3)].set_index('unit').extra
    thr, ref2 = [], []
    for (det, k), g in d.groupby(['detector', 'k']):
        rc = [np.quantile(gs[gs['eval'] == 'E2'].score, .95) for _, gs in g.groupby('seed')]
        sc = [np.quantile(gs[gs['eval'] == 'SC'].score, .95) for _, gs in g.groupby('seed')]
        thr.append(dict(detector=det, k=int(k), thr_RC=float(np.mean(rc)), thr_SC=float(np.mean(sc)), ratio_SC_RC=float(np.mean(sc) / np.mean(rc))))
        fl = []
        for (_, gs), t in zip(g.groupby('seed'), rc):
            e1 = gs[gs['eval'] == 'E1']; fl.append(pd.Series((e1.score > t).astype(float).to_numpy(), index=e1.unit))
        f = pd.concat(fl, axis=1).mean(axis=1); lab = l2.reindex(f.index)
        u = pd.DataFrame(dict(flag=f.to_numpy(), lab=lab.to_numpy(), cluster=[x[:-1] for x in f.index]))
        cs, cp = ci(u[u.lab == '1']), ci(u[u.lab == '0'])
        ref2.append(dict(detector=det, k=int(k), sens_ref2=cs['est'], sens_ref2_lo=cs['lo'], sens_ref2_hi=cs['hi'], sens_ref2_n=cs['n'],
                         spec_ref2=1 - cp['est'], spec_ref2_lo=1 - cp['hi'], spec_ref2_hi=1 - cp['lo'], spec_ref2_n=cp['n']))
    return pd.DataFrame(thr), pd.DataFrame(ref2)

if __name__ == '__main__':
    R, T, hb = b1(); R3, T3, c3 = b3(); R4 = b4(); TH, RF2 = thresholds_and_ref2()
    out = dict(B1_metrics=json.loads(R.to_json(orient='records')), B1_paired=json.loads(T.to_json(orient='records')), hypotheses=hb,
               B3_metrics=json.loads(R3.to_json(orient='records')), B3_paired=json.loads(T3.to_json(orient='records')), B3_counts=c3,
               B4_metrics=json.loads(R4.to_json(orient='records')), thresholds=json.loads(TH.to_json(orient='records')),
               B1_RC_ref2=json.loads(RF2.to_json(orient='records')))
    json.dump(out, open(os.path.join(OUT, 'amendB.json'), 'w'), indent=1)
    print(R[['detector', 'k', 'calibration', 'sens', 'spec', 'fpr_true_null', 'fpr_true_null_lo', 'fpr_true_null_hi']].round(3).to_string())
    print(T[(T.endpoint == 'sensitivity')][['calibration', 'k', 'detector', 'diff', 'diff_lo', 'diff_hi', 'p_holm']].round(3).to_string())
    print(hb); print(c3); print(R3.round(3).to_string()); print(T3[T3.endpoint == 'sensitivity'].round(3).to_string()); print(R4.round(3).to_string()); print(TH.round(3).to_string()); print(RF2.round(3).to_string())
