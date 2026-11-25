"""Amendment C statistics from ../results/amendC/scores.pkl -> ../results/amendC/amendC.json (+ tables).
Usage (from code/): python -m src.statistics.amendment_c_stats"""
import os, json, pickle
import numpy as np
from scipy import stats
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
D = os.path.join(ROOT, 'results', 'amendC')
KS = (3, 4, 5, 6, 7, 8); K4 = (3, 4, 5, 6); DETS = ['D1', 'D2c', 'D6s', 'D8c', 'D11']; NF = 5; B = 2000
ALPHA = 0.05

def q95(x): return float(np.quantile(x[~np.isnan(x)], 1 - ALPHA))

def cluster_boot(vals, clusters, stat=np.mean, b=B, seed=0):
    """Patient-cluster bootstrap CI of stat over unit-level values (vals may be 1-D or (n,2) for paired differences)."""
    rng = np.random.default_rng(seed); u, inv = np.unique(clusters, return_inverse=True)
    idx = [np.where(inv == i)[0] for i in range(len(u))]
    est = float(stat(vals)); bs = []
    for _ in range(b):
        pick = np.concatenate([idx[i] for i in rng.integers(len(u), size=len(u))]); bs.append(stat(vals[pick]))
    return est, float(np.quantile(bs, 0.025)), float(np.quantile(bs, 0.975))

def mcnemar(a, b):
    """Exact two-sided McNemar on binary paired flags a, b."""
    n10 = int(((a == 1) & (b == 0)).sum()); n01 = int(((a == 0) & (b == 1)).sum())
    n = n10 + n01
    return 1.0 if n == 0 else float(min(1, 2 * stats.binom.cdf(min(n10, n01), n, 0.5)))

def holm(ps):
    ps = np.asarray(ps, float); o = np.argsort(ps); m = len(ps); adj = np.empty(m); run = 0
    for r, i in enumerate(o):
        run = max(run, min(1, (m - r) * ps[i])); adj[i] = run
    return adj.tolist()

def budget_gamma(Sc):
    """Common per-review quantile level gamma s.t. P(any score_k > q_k(1-gamma), k=3..8) = ALPHA on calibration null Sc (N,6)."""
    lo, hi = 1e-5, ALPHA
    for _ in range(50):
        g = (lo + hi) / 2; thr = np.nanquantile(Sc, 1 - g, axis=0)
        if (Sc > thr).any(1).mean() > ALPHA: hi = g
        else: lo = g
    return lo, np.nanquantile(Sc, 1 - lo, axis=0)

def seq_first(S, thr, rule):
    """S (N,6) scores for reviews k=3..8; returns index (0..5) of first flag or -1."""
    X = S > thr[None]
    if rule == 'confirm':
        X = np.concatenate([np.zeros((len(S), 1), bool), X[:, 1:] & X[:, :-1]], 1)
    first = np.where(X.any(1), X.argmax(1), -1); return first

def main():
    R = pickle.load(open(os.path.join(D, 'scores.pkl'), 'rb'))
    J = dict(thresholds={}, HC={}, artes={}, ho_cnn={}, real={}, syn={}, seq={}, prior={})
    meta = json.load(open(os.path.join(D, 'meta.json'))); J['meta'] = {k: v for k, v in meta.items() if k != 'priors'}
    J['prior'] = meta['priors']
    # ---------------- thresholds per fold, source, det, k
    thr = {f: {'CNN': {}, 'RC': {}, 'SC': {}} for f in range(NF)}
    for f in range(NF):
        o = R[f]; cS = o['cal_cnn'][0]
        for d in DETS:
            thr[f]['CNN'][d] = {k: q95(cS[d][:, KS.index(k)]) for k in KS}
            thr[f]['RC'][d] = {k: q95(o['artes'][k][0][d][:, KS.index(k)]) for k in KS}
            thr[f]['SC'][d] = {k: q95(o['cal_sc'][k][d]) for k in K4}
    J['thresholds'] = {src: {d: {k: float(np.mean([thr[f][src][d][k] for f in range(NF)])) for k in (K4 if src == 'SC' else KS)}
                             for d in DETS} for src in ('CNN', 'RC', 'SC')}
    # ---------------- (b) Artes true null with CNN thresholds (flag averaged over the 5 fold detectors)
    for d in DETS:
        J['artes'][d] = {}
        for k in K4:
            fl = np.mean([R[f]['artes'][k][0][d][:, KS.index(k)] > thr[f]['CNN'][d][k] for f in range(NF)], 0)
            J['artes'][d][k] = cluster_boot(fl, R[0]['artes'][k][1])
    # ---------------- (c) held-out CNN null, each source
    for src in ('CNN', 'RC', 'SC'):
        J['ho_cnn'][src] = {}
        for d in DETS:
            J['ho_cnn'][src][d] = {}
            for k in K4:
                fl = np.concatenate([R[f]['ho_cnn'][0][d][:, KS.index(k)] > thr[f][src][d][k] for f in range(NF)]).astype(float)
                P = np.concatenate([R[f]['ho_cnn'][1] for f in range(NF)])
                J['ho_cnn'][src][d][k] = cluster_boot(fl, P, b=500)
    # ---------------- (a) real clinic, all labelled eyes, CNN (main) and RC/SC thresholds
    lab = np.concatenate([R[f]['real8_meta']['label'] for f in range(NF)])
    pid = np.concatenate([R[f]['real8_meta']['pid'] for f in range(NF)])
    fut = np.concatenate([R[f]['real8_meta']['fut'] for f in range(NF)])
    J['real']['n'] = dict(progressors=int((lab == 1).sum()), stable=int((lab == 0).sum()), indeterminate=int((lab == -1).sum()),
                          patients_labelled=int(len(np.unique(pid[lab >= 0]))), eyes8=int(len(lab)))
    def flags(src, d, k):
        return np.concatenate([R[f]['real8'][d][:, KS.index(k)] > thr[f][src][d][k] for f in range(NF)]).astype(int)
    for src in ('CNN', 'RC', 'SC'):
        J['real'][src] = {}
        for k in K4:
            J['real'][src][k] = {}
            ref = flags(src, 'D1', k); pv = {}
            for d in DETS:
                fl = flags(src, d, k); e = {}
                for name, m in (('sens', lab == 1), ('spec', lab == 0), ('indet_flag', lab == -1)):
                    v = fl[m] if name != 'spec' else 1 - fl[m]
                    e[name] = cluster_boot(v.astype(float), pid[m], b=1000)
                if d != 'D1':
                    m = lab == 1
                    e['sens_diff_vs_D1'] = cluster_boot((fl[m] - ref[m]).astype(float), pid[m], b=1000)
                    e['spec_diff_vs_D1'] = cluster_boot(((1 - fl[lab == 0]) - (1 - ref[lab == 0])).astype(float), pid[lab == 0], b=1000)
                    e['mcnemar_p'] = mcnemar(fl[m], ref[m]); pv[d] = e['mcnemar_p']
                # exploratory future-only reference
                fk = fut[:, KS.index(k)]
                e['fut_sens'] = [float(fl[fk == 1].mean()) if (fk == 1).any() else None, int((fk == 1).sum())]
                e['fut_spec'] = [float(1 - fl[fk == 0].mean()) if (fk == 0).any() else None, int((fk == 0).sum())]
                J['real'][src][k][d] = e
            ds = list(pv); adj = holm([pv[d] for d in ds])
            for d, a in zip(ds, adj): J['real'][src][k][d]['mcnemar_p_holm'] = a
    # HC3 Holm over k=3..6 for D11 vs D1 (CNN)
    p11 = [J['real']['CNN'][k]['D11']['mcnemar_p'] for k in K4]; a11 = holm(p11)
    for k, a in zip(K4, a11): J['real']['CNN'][k]['D11']['mcnemar_p_holm_HC3'] = a
    # ---------------- (d) semi-synthetic sensitivity (CNN thresholds)
    keys = list(R[0]['syn'][0].keys())
    for key in keys:
        J['syn'][key] = {}
        P = np.concatenate([R[f]['syn'][1] for f in range(NF)])
        for d in DETS:
            J['syn'][key][d] = {}
            for k in K4:
                fl = np.concatenate([R[f]['syn'][0][key][d][:, KS.index(k)] > thr[f]['CNN'][d][k] for f in range(NF)]).astype(float)
                J['syn'][key][d][k] = cluster_boot(fl, P, b=300)
                if d != 'D1':
                    f1 = np.concatenate([R[f]['syn'][0][key]['D1'][:, KS.index(k)] > thr[f]['CNN']['D1'][k] for f in range(NF)]).astype(float)
                    J['syn'][key][d][f'{k}_diff_vs_D1'] = cluster_boot(fl - f1, P, b=300)
    # ---------------- (e) sequential monitoring, reviews 3..8
    for d in DETS:
        J['seq'][d] = {}
        per = {f: np.array([thr[f]['CNN'][d][k] for k in KS]) for f in range(NF)}
        bud = {f: budget_gamma(R[f]['cal_cnn'][0][d]) for f in range(NF)}
        J['seq'][d]['budget_gamma'] = [float(bud[f][0]) for f in range(NF)]
        rules = {'naive': (per, 'naive'), 'confirm': (per, 'confirm'), 'budget': ({f: bud[f][1] for f in range(NF)}, 'naive')}
        for rn, (th, rule) in rules.items():
            e = {}
            # Artes: 8-test windows (5 starts x 10 donor draws); scores at k=3..8 are prefixes of each window
            fl = np.mean([seq_first(R[f]['artes'][8][0][d], th[f], rule) >= 0 for f in range(NF)], 0)
            e['artes_cum_fa'] = cluster_boot(fl, R[0]['artes'][8][1])
            fl = np.concatenate([seq_first(R[f]['ho_cnn'][0][d], th[f], rule) >= 0 for f in range(NF)]).astype(float)
            P = np.concatenate([R[f]['ho_cnn'][1] for f in range(NF)]); e['ho_cnn_cum_fa'] = cluster_boot(fl, P, b=500)
            first = np.concatenate([seq_first(R[f]['real8'][d], th[f], rule) for f in range(NF)])
            for name, m in (('prog_by8', lab == 1), ('stable_by8', lab == 0), ('indet_by8', lab == -1)):
                e[name] = cluster_boot((first[m] >= 0).astype(float), pid[m], b=1000)
            fp = first[lab == 1]; tests = np.where(fp >= 0, fp + 3, np.inf)
            e['prog_median_tests'] = float(np.median(tests)) if np.isfinite(np.median(tests)) else '>8'
            e['prog_flag_by_test'] = {k: float((tests <= k).mean()) for k in KS}
            for key in ('global_1.0', 'local_1.0'):
                fs = np.concatenate([seq_first(R[f]['syn'][0][key][d], th[f], rule) for f in range(NF)])
                P = np.concatenate([R[f]['syn'][1] for f in range(NF)])
                e[f'syn_{key}_by8'] = cluster_boot((fs >= 0).astype(float), P, b=300)
                ts = np.where(fs >= 0, fs + 3, np.nan); e[f'syn_{key}_mean_tests_if_flagged'] = float(np.nanmean(ts))
            J['seq'][d][rn] = e
    # ---------------- hypotheses
    H = {}
    rc = [J['ho_cnn']['RC']['D2c'][k][0] for k in K4]; scv = [J['ho_cnn']['SC']['D2c'][k][0] for k in K4]
    cn = [J['ho_cnn']['CNN'][d][k][0] for d in DETS for k in K4]
    H['HC1'] = dict(RC_D2c_fa=rc, SC_D2c_fa=scv, CNN_share_within_2pp=float(np.mean([abs(x - .05) <= .02 for x in cn])),
                    supported=bool(all(x > .10 for x in rc) and all(x < .025 for x in scv) and np.mean([abs(x - .05) <= .02 for x in cn]) >= .9))
    exc = {f'{d}_k{k}': J['artes'][d][k][1] > .05 for d in DETS for k in K4}
    H['HC2'] = dict(cells_with_excess=[c for c, v in exc.items() if v], supported=not any(exc.values()))
    h3 = {}
    for k in (3, 4):
        e = J['real']['CNN'][k]['D11']
        h3[k] = dict(diff=e['sens_diff_vs_D1'], p_holm=e['mcnemar_p_holm_HC3'], spec_diff=e['spec_diff_vs_D1'][0],
                     ok=bool(e['sens_diff_vs_D1'][1] > 0 and e['mcnemar_p_holm_HC3'] < .05 and e['spec_diff_vs_D1'][0] >= -.05))
    H['HC3'] = dict(by_k=h3, supported=all(v['ok'] for v in h3.values()))
    s = J['seq']['D1']
    h4 = dict(naive_artes=s['naive'].get('artes_cum_fa'), budget_ho=[J['seq'][d]['budget']['ho_cnn_cum_fa'][0] for d in DETS],
              budget_artes=[J['seq'][d]['budget'].get('artes_cum_fa') for d in DETS])
    h4['supported'] = bool(h4['naive_artes'] is not None and h4['naive_artes'][0] >= .15 and all(.03 <= x <= .07 for x in h4['budget_ho'])
                           and all(a is not None and a[1] <= .05 for a in h4['budget_artes']))
    H['HC4'] = h4
    dn = J['seq']['D11']['naive']['prog_by8'][0]; db = J['seq']['D11']['budget']['prog_by8'][0]
    H['HC5'] = dict(naive=dn, budget=db, drop_pp=100 * (dn - db), supported=bool(dn - db <= .15))
    J['HC'] = H
    json.dump(J, open(os.path.join(D, 'amendC.json'), 'w'), indent=1, default=lambda o: o.tolist() if hasattr(o, 'tolist') else str(o))
    print(json.dumps(H, indent=1, default=str))

if __name__ == '__main__':
    main()
