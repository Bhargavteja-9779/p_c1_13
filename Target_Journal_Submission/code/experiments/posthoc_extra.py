"""Post hoc analyses P1-P3 (see experiments/protocol.md, 'Post hoc analysis plan P'). Seed 0.
Usage (from code/): python experiments/posthoc_extra.py  -> ../results/posthoc_extra_raw.csv, ../results/posthoc_extra.json"""
import os, sys, json, time, hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np, pandas as pd
from scipy import stats
from run_all import reference, make
from src.utils import set_seed
from src.data.uwhvf import load_series, patient_split, blind_spot_mask
from src.data.artes_retest import load_artes
from src.data.grape import load_grape
from src.models import detectors as D
from src.models.deferral import ols

RES = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'results'))
KS = (3, 4, 5, 6); SEED = 0; B = 2000


class MLTabularShuffleCal(D.MLTabular):
    """D8 with threshold = 95th percentile of scores on shuffled training series (P3)."""
    name = 'D8s ML-tabular, shuffle-calibrated threshold'
    def fit(self, train, val, ks=KS):
        super().fit(train, val, ks)
        rng = np.random.default_rng(self.seed + 77)
        for k in ks:
            X = [D.tab_features(s['t'][:k], s['Y'][:k][rng.permutation(k)]) for s in train if len(s['t']) >= k for _ in range(20)]
            sc = self.models[k].predict_proba(np.array(X))[:, 1]; self.thr[k] = float(np.quantile(sc, 0.95))
        return self


def boot(df, col='flag'):
    g = df.groupby('cluster')[col].agg(['sum', 'count']); s, n = g['sum'].to_numpy(float), g['count'].to_numpy(float)
    rng = np.random.default_rng(0); idx = rng.integers(0, len(g), (B, len(g))); bs = s[idx].sum(1) / n[idx].sum(1)
    return dict(est=float(s.sum() / n.sum()), lo=float(np.quantile(bs, .025)), hi=float(np.quantile(bs, .975)), n=int(n.sum()))


def main():
    t0 = time.time(); keep = ~blind_spot_mask(); S = load_series(); sp = patient_split(S)
    def to_d(s):
        lab = reference(s) if len(s['ages']) >= 8 else None
        return dict(pid=s['pid'], eye=s['eye'], t=s['ages'] - s['ages'][0], Y=s['sens'][:, keep], label=lab)
    train = [to_d(s) for s in S if sp[s['pid']] == 'train' and len(s['ages']) >= 3]
    val = [to_d(s) for s in S if sp[s['pid']] == 'val' and len(s['ages']) >= 3]
    test = [to_d(s) for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 3]
    A = load_artes(); G = load_grape()
    # P2 sigma estimates
    sig_uw = float(np.median([np.std(s['Y'].mean(1) - np.polyval(np.polyfit(s['t'], s['Y'].mean(1), 1), s['t']), ddof=2)
                              for s in train if s['label'] == 0]))
    sig_ar = float(np.median([np.std(a['sens'][:, keep].mean(1), ddof=1) for a in A]))
    s_add = float(np.sqrt(max(sig_uw ** 2 - sig_ar ** 2, 0)))
    print('sigma_UW', sig_uw, 'sigma_Artes', sig_ar, 'added SD', s_add, flush=True)
    donors = {k: [s['t'][:k] for s in test if len(s['t']) >= k] for k in KS}
    rows = []
    rec = lambda det, k, ev, unit, f, lab=None: rows.append(dict(detector=det, k=k, eval=ev, unit=unit, flag=int(f), label=lab))
    classes = list(D.ALL) + [MLTabularShuffleCal]
    for cls in classes:
        name = cls.name; set_seed(SEED); det = make(cls, SEED)
        fit_kw = {'ks': KS} if 'ks' in det.fit.__code__.co_varnames else {}
        det.fit(train, val, **fit_kw)
        rng = np.random.default_rng(5000)
        for k in KS:
            for a in A:                                      # P2 inflated null
                for i in range(0, 12 - k + 1):
                    for d in range(10):
                        tt = donors[k][rng.integers(len(donors[k]))]
                        Y = a['sens'][i:i + k][:, keep] + rng.normal(0, s_add, size=(k, 1))
                        rec(name, k, 'P2', f"{a['pid']}|{i}|{d}", det.flag(tt, Y))
            if cls is MLTabularShuffleCal:                   # P3 E1 + true null
                rng2 = np.random.default_rng(1000)
                for s in test:
                    if len(s['t']) >= 8 and s['label'] is not None:
                        rec(name, k, 'E1', s['pid'] + s['eye'], det.flag(s['t'][:k], s['Y'][:k]), s['label'])
                for a in A:
                    for i in range(0, 12 - k + 1):
                        for d in range(10):
                            tt = donors[k][rng2.integers(len(donors[k]))]
                            rec(name, k, 'E2', f"{a['pid']}|{i}|{d}", det.flag(tt, a['sens'][i:i + k][:, keep]))
        print(name, 'done', round(time.time() - t0), flush=True)
        # P1 GRAPE shuffle audit
        if name in D.GRID_AGNOSTIC:
            pids = sorted({g['pid'] for g in G})
            fold_of = {p: int(hashlib.sha256(('grape' + p).encode()).hexdigest()[:4], 16) % 5 for p in pids}
            rng3 = np.random.default_rng(2000)
            for fo in range(5):
                if name == 'D8 ML-tabular (LightGBM)':
                    if fo == 0:
                        gdet = D.MLTabular(seed=SEED); set_seed(SEED); gdet.fit(train, val, ks=(3, 4))
                    gd = gdet
                else:
                    gd = make(cls, SEED); gtr = [dict(t=g['t'], Y=g['sens'], label=None) for g in G if fold_of[g['pid']] != fo]
                    kw = {'ks': (3, 4)} if 'ks' in gd.fit.__code__.co_varnames else {}
                    gd.fit(gtr, None, **kw)
                for g in G:
                    if fold_of[g['pid']] != fo: continue
                    for k in (3, 4):
                        if len(g['t']) >= k:
                            for r in range(10):
                                P = rng3.permutation(k)
                                rec(name, k, 'P1', f"{g['pid']}{g['eye']}|{r}", gd.flag(g['t'][:k], g['sens'][:k][P]))
            print(name, 'GRAPE shuffle done', round(time.time() - t0), flush=True)
    R = pd.DataFrame(rows); R.to_csv(os.path.join(RES, 'posthoc_extra_raw.csv'), index=False)
    def cl(ev, u):
        return u.split('|')[0] if ev in ('P2', 'E2') else (u.split('|')[0][:-2] if ev == 'P1' else u[:-1])
    R['cluster'] = [cl(e, u) for e, u in zip(R['eval'], R['unit'])]
    out = dict(sigma_uw=sig_uw, sigma_artes=sig_ar, added_sd=s_add, seed=SEED, P1={}, P2={}, P3={})
    for (det, k, ev), g in R.groupby(['detector', 'k', 'eval']):
        key = f"{det}|{k}"
        if ev in ('P1', 'P2'): out[ev][key] = boot(g)
        elif ev == 'E2': out['P3'].setdefault(key, {})['fpr_true_null'] = boot(g)
        elif ev == 'E1':
            out['P3'].setdefault(key, {})['sens'] = boot(g[g.label == 1])
            sp_ = boot(g[g.label == 0].assign(flag=1 - g[g.label == 0].flag)); out['P3'][key]['spec'] = sp_
    # P3 paired McNemar vs D1 (sensitivity) using committed D1 E1 flags
    raw = pd.read_csv(os.path.join(RES, 'raw_results.csv.gz'), dtype={'unit': str, 'extra': str})
    d1 = raw[(raw.detector == 'D1 OLS-MD') & (raw['eval'] == 'E1') & (raw.label == 1)]
    for k in KS:
        a = d1[d1.k == k].set_index('unit')['flag']
        b = R[(R.detector == MLTabularShuffleCal.name) & (R['eval'] == 'E1') & (R.k == k) & (R.label == 1)].set_index('unit')['flag']
        j = a.index.intersection(b.index); only_b = int(((b[j] == 1) & (a[j] == 0)).sum()); only_a = int(((b[j] == 0) & (a[j] == 1)).sum())
        p = 1.0 if only_a + only_b == 0 else float(stats.binomtest(min(only_a, only_b), only_a + only_b, .5).pvalue)
        out['P3'][f"{MLTabularShuffleCal.name}|{k}"]['vs_D1'] = dict(only_D8s=only_b, only_D1=only_a, p_mcnemar=p, n=len(j))
    out['runtime_s'] = time.time() - t0
    json.dump(out, open(os.path.join(RES, 'posthoc_extra.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
