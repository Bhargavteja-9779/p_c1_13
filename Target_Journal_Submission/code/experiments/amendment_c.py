"""Amendment C (protocol.md): clinic-noise null (CNN) calibration, moderated trend test (D11), semi-synthetic truth and
budgeted sequential monitoring, with 5-fold patient-level cross-fitting over all UWHVF eyes.
Step 1 (this file): compute continuous scores for k = 3..8 -> ../results/amendC/scores_*.npz + meta.json
Step 2: python -m src.statistics.amendment_c_stats -> ../results/amendC/amendC.json
Usage (from code/): python experiments/amendment_c.py"""
import os, sys, time, json, hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np
from scipy import stats, special, optimize
from src.data.uwhvf import load_series, blind_spot_mask
from src.data.artes_retest import load_artes
from src.models import detectors as D
from src.models.conformal_vf import _ols, stat_md, stat_region
from run_all import reference
from src.models.deferral import ols, md_series
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'results', 'amendC'); os.makedirs(OUT, exist_ok=True)
KS = (3, 4, 5, 6, 7, 8); KMAX = 8; NNULL = 20; NFOLD = 5
DETS = ['D1', 'D2c', 'D6s', 'D8c', 'D11']
RATES = (0.5, 1.0, 2.0); PATTERNS = ('global', 'local')
REGIONS = D.make_regions(52)

def fold_of(pid): return int(hashlib.sha256(('amendC-fold' + pid).encode()).hexdigest()[:8], 16) % NFOLD

# ------------------------------------------------------------------ vectorised scores
def tab_features_batch(T, Y):
    """Exact batch version of detectors.tab_features. T (N,k), Y (N,k,L) -> (N,14)."""
    N, k, L = Y.shape
    b, z = _ols(T, Y); p = stats.t.cdf(np.clip(z, -50, 50), df=max(k - 2, 1))
    md = Y.mean(2); mb, mz = _ols(T, md[..., None]); mb, mz = mb[:, 0], mz[:, 0]
    sb = np.sort(b, 1)[:, :max(1, L // 10)].mean(1)
    return np.column_stack([np.full(N, k), T[:, -1] - T[:, 0], md[:, -1], md.mean(1), md[:, -1] - md[:, 0], mb, mz,
                            ((b <= -1) & (p < 0.01)).mean(1), (p < 0.05).mean(1), -np.log(np.clip(p, 1e-12, 1)).mean(1),
                            sb, b.std(1), Y.std(1).mean(1), md.max(1) - md.min(1)])

def fit_var_prior(s2, df):
    """Empirical-Bayes prior (d0, s0^2) for residual variances s2 with degrees of freedom df (Smyth 2004, moments)."""
    s2 = np.maximum(s2, 1e-8); e = np.log(s2) - special.digamma(df / 2) + np.log(df / 2)
    emean = e.mean(); evar = ((e - emean) ** 2).sum() / (len(e) - 1) - special.polygamma(1, df / 2).mean()
    if evar <= 0: d0 = 1e6
    else: d0 = 2 * optimize.brentq(lambda x: special.polygamma(1, x) - evar, 1e-6, 1e6)
    s0 = np.exp(emean + special.digamma(d0 / 2) - np.log(d0 / 2))
    return float(min(d0, 1e6)), float(s0)

class Scorer:
    """Holds the fold-specific fitted parts (variance prior for D11, LightGBM for D8c)."""
    def __init__(self, calib_eyes, seed=0):
        lv = np.array([s['Y'].mean() for s in calib_eyes if len(s['t']) >= 8])
        self.cuts = np.quantile(lv, [1 / 3, 2 / 3]); self.prior = []
        groups = [[], [], []]
        for s in calib_eyes:
            if len(s['t']) < 8: continue
            n = len(s['t']); b, p, _ = ols(s['t'], s['Y'].mean(1))
            m = s['Y'].mean(1); tc = s['t'] - s['t'].mean(); res = m - m.mean() - b * tc
            groups[int(np.digitize(s['Y'].mean(), self.cuts))].append(((res ** 2).sum() / (n - 2), n - 2))
        for g in groups:
            a = np.array(g); self.prior.append(fit_var_prior(a[:, 0], a[:, 1]))
        # D8c: LightGBM per k, config chosen on an inner patient split of the calibration folds
        import lightgbm as lgb
        from sklearn.metrics import roc_auc_score
        lab = [s for s in calib_eyes if s['label'] is not None]
        inner = np.array([int(hashlib.sha256(('amendC-inner' + s['pid']).encode()).hexdigest()[:8], 16) % 5 == 0 for s in lab])
        self.models = {}
        for k in KS:
            X = tab_features_batch(np.stack([s['t'][:k] for s in lab]), np.stack([s['Y'][:k] for s in lab]))
            y = np.array([s['label'] for s in lab]); best = None
            for cfg in D.MLTabular.GRID:
                m = lgb.LGBMClassifier(**cfg, min_child_samples=10, subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                                       random_state=seed, verbose=-1).fit(X[~inner], y[~inner])
                a = roc_auc_score(y[inner], m.predict_proba(X[inner])[:, 1])
                if best is None or a > best[0]: best = (a, cfg)
            self.models[k] = lgb.LGBMClassifier(**best[1], min_child_samples=10, subsample=0.8, subsample_freq=1,
                                                colsample_bytree=0.8, random_state=seed, verbose=-1).fit(X, y)
    def scores(self, T, Y):
        """T (N,K), Y (N,K,52) -> dict det -> (N, len(KS)) scores for k = 3..K (NaN where k > K)."""
        N, K, _ = Y.shape; out = {d: np.full((N, len(KS)), np.nan) for d in DETS}
        for j, k in enumerate(KS):
            if k > K: continue
            t, y = T[:, :k], Y[:, :k]; m = y.mean(2)
            out['D1'][:, j] = stat_md(t, y)
            b, _ = _ols(t, m[..., None]); b = b[:, 0]; out['D2c'][:, j] = -b
            out['D6s'][:, j] = stat_region(t, y, REGIONS)
            out['D8c'][:, j] = self.models[k].predict_proba(tab_features_batch(t, y))[:, 1]
            tc = t - t.mean(1, keepdims=True); sxx = np.maximum((tc ** 2).sum(1), 1e-9)
            res = m - m.mean(1, keepdims=True) - tc * b[:, None]; s2 = (res ** 2).sum(1) / (k - 2)
            g = np.digitize(y.mean((1, 2)), self.cuts); d0 = np.array([self.prior[i][0] for i in g])
            s0 = np.array([self.prior[i][1] for i in g])
            st = np.where(d0 >= 1e6, s0, (d0 * s0 + (k - 2) * s2) / (d0 + k - 2))
            out['D11'][:, j] = -b / np.sqrt(st / sxx)
        return out

# ------------------------------------------------------------------ null and synthetic series
def cnn_series(eyes, rng, n=NNULL, K=KMAX):
    T, Y, P = [], [], []
    for s in eyes:
        nt = len(s['t'])
        if nt < 8: continue
        tc = s['t'][:, None]; X = np.hstack([np.ones_like(tc), tc]); beta, *_ = np.linalg.lstsq(X, s['Y'], rcond=None)
        R = (s['Y'] - X @ beta) * np.sqrt(nt / (nt - 2)); base = beta[0]          # fitted value at the first test (t=0)
        for _ in range(n):
            idx = rng.choice(nt, K, replace=False)
            Y.append(np.clip(base[None] + R[idx], 0, None)); T.append(s['t'][:K]); P.append(s['pid'])
    return np.array(T), np.array(Y), np.array(P)

def inject(T, Y, rate, pattern, rng):
    loss = np.zeros((len(T), 52))
    if pattern == 'global': loss[:] = rate
    else:
        for i in range(len(T)):
            r = REGIONS[rng.integers(4)]; loss[i, r] = rate * 52 / len(r)
    return np.clip(Y - T[:, :, None] * loss[:, None, :], 0, None)

def main():
    t0 = time.time(); keep = ~blind_spot_mask(); S = load_series()
    eyes = []
    for s in S:
        if len(s['ages']) < 3: continue
        t = s['ages'] - s['ages'][0]; d = dict(pid=s['pid'], eye=s['eye'], t=t, Y=s['sens'][:, keep], fold=fold_of(s['pid']),
                                              label=reference(s) if len(t) >= 8 else None)
        # exploratory future-only reference: MD slope over tests k+1..end, eyes with >= k+5 tests
        fut = []
        for k in KS:
            if len(t) >= k + 5:
                tt = t[k:]; b, p, _ = ols(tt, md_series(s['td'][k:]))
                fut.append(1 if (b < -0.3 and p < 0.01) else (0 if p > 0.5 else -1))
            else: fut.append(-2)
        d['fut'] = fut; eyes.append(d)
    A = load_artes()
    meta = dict(n_eyes=len(eyes), n_eyes8=sum(len(e['t']) >= 8 for e in eyes), n_labelled=sum(e['label'] is not None for e in eyes),
                n_patients=len({e['pid'] for e in eyes}), priors={}, folds={})
    donor_pool = [e['t'][:KMAX] for e in eyes if len(e['t']) >= 8]
    drng = np.random.default_rng(777)
    # Artes windows: per-k windows of length k (all starts), and 8-test windows for sequential monitoring; 10 donor draws
    art = {}
    for k in KS:
        T, Y, P = [], [], []
        for a in A:
            for i in range(0, 12 - k + 1):
                for _ in range(10):
                    T.append(donor_pool[drng.integers(len(donor_pool))][:k]); Y.append(a['sens'][i:i + k][:, keep]); P.append(a['pid'])
        art[k] = (np.array(T), np.array(Y), np.array(P))
    res = {}
    for f in range(NFOLD):
        rng = np.random.default_rng(100 + f)
        cal = [e for e in eyes if e['fold'] != f]; ev = [e for e in eyes if e['fold'] == f]
        sc = Scorer(cal); meta['priors'][f] = dict(cuts=sc.cuts.tolist(), prior=sc.prior)
        out = {}
        # (1) calibration CNN pool
        T, Y, P = cnn_series(cal, rng); out['cal_cnn'] = (sc.scores(T, Y), P)
        # (2) calibration SC pool: first k tests shuffled (5 per eye), per k
        scs = {}
        for k in KS[:4]:
            ce = [e for e in cal if len(e['t']) >= k]
            Tk = np.repeat(np.stack([e['t'][:k] for e in ce]), 5, 0)
            Yk = np.stack([e['Y'][:k][rng.permutation(k)] for e in ce for _ in range(5)])
            scs[k] = sc.scores(Tk, Yk)
        out['cal_sc'] = {k: {d: v[d][:, KS.index(k)] for d in DETS} for k, v in scs.items()}
        # (3) Artes per-k windows (used as RC calibration source and as true-null evaluation)
        out['artes'] = {k: (sc.scores(*art[k][:2]), art[k][2]) for k in KS}
        # (4) held-out real eyes (>= 3 tests): scores on first min(n,8) tests
        ev8 = [e for e in ev if len(e['t']) >= 8]
        T = np.stack([e['t'][:8] for e in ev8]); Y = np.stack([e['Y'][:8] for e in ev8]); out['real8'] = sc.scores(T, Y)
        out['real8_meta'] = dict(pid=np.array([e['pid'] for e in ev8]), eye=np.array([e['pid'] + e['eye'] for e in ev8]),
                                 label=np.array([-1 if e['label'] is None else e['label'] for e in ev8]),
                                 fut=np.array([e['fut'] for e in ev8]))
        # (5) held-out CNN null and semi-synthetic series (same null series, with injected loss)
        T, Y, P = cnn_series(ev, rng); out['ho_cnn'] = (sc.scores(T, Y), P)
        syn = {}
        for pat in PATTERNS:
            for r in RATES:
                syn[f'{pat}_{r}'] = sc.scores(T, inject(T, Y, r, pat, rng))
        out['syn'] = (syn, P)
        res[f] = out
        meta['folds'][f] = dict(n_cal=len(cal), n_eval8=len(ev8), n_cal_cnn=len(out['cal_cnn'][1]), n_ho_cnn=len(P))
        print(f'fold {f} done {time.time() - t0:.0f}s', flush=True)
    import pickle
    pickle.dump(res, open(os.path.join(OUT, 'scores.pkl'), 'wb'))
    meta['runtime_s'] = time.time() - t0; meta['KS'] = KS; meta['DETS'] = DETS
    json.dump(meta, open(os.path.join(OUT, 'meta.json'), 'w'), indent=1, default=float)
    print(json.dumps({k: v for k, v in meta.items() if k not in ('priors',)}, default=float))

if __name__ == '__main__':
    main()
