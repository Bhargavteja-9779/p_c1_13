"""Study 2 (protocol_v2.md): cross-fitted, shuffle-calibrated, matched-false-alarm benchmark.
Usage: python study2.py --mode quick|full
Writes ../results/study2_raw.csv(.gz) and ../results/study2_meta.json. Quick mode runs one fold / one seed on a subsample
and writes study2_raw_quick.csv; it prints only counts and timing (no outcome metrics)."""
import os, sys, json, time, argparse, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from scipy import stats
from src.utils import set_seed
from src.data.uwhvf import load_series, blind_spot_mask
from src.data.artes_retest import load_artes
from src.data.grape import load_grape
from src.models.conformal_vf import _ols, stat_md, stat_poplr
from src.models import detectors as D
from src.models.deferral import ols, md_series

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RES = os.path.join(ROOT, 'results')
KS = (3, 4, 5, 6)
ALPHA = 0.05
Q_GRID = (0.01, 0.025, 0.05, 0.10, 0.15, 0.20)
M_GRID = (2, 3, 4)

def h(s, salt): return int(hashlib.sha256((salt + s).encode()).hexdigest()[:8], 16)

# ------------------------------------------------------------------ references
def ref_rule(t, md):
    b, p, _ = ols(t, md)
    prog = b < -0.3 and p < 0.01
    return b, p, prog

def references(s):
    t = s['ages'] - s['ages'][0]; md = md_series(s['td']); n = len(t); out = {}
    if n >= 8:
        b, p, prog = ref_rule(t, md)
        out['R1'] = 1 if prog else (0 if p > 0.5 else None)
        out['R2'] = 1 if prog else (0 if (-0.3 <= b <= 0.3 and p > 0.1) else None)
    for k in KS:
        if n - k >= 5:
            b, p, prog = ref_rule(t[k:] - t[k], md[k:])
            out[f'R3_{k}'] = 1 if prog else (0 if p > 0.5 else None)
    return out

# ------------------------------------------------------------------ vectorised scores
def tab_batch(T, Y):
    """Vectorised version of detectors.tab_features for arrays T (n,k), Y (n,k,L)."""
    n, k, L = Y.shape
    b, z = _ols(T, Y); p = stats.t.cdf(np.clip(z, -50, 50), df=max(k - 2, 1))
    md = Y.mean(2); mb, mz = _ols(T, md[..., None]); mb, mz = mb[:, 0], mz[:, 0]
    sb = np.sort(b, 1)[:, :max(1, L // 10)].mean(1)
    return np.column_stack([np.full(n, k), T[:, -1] - T[:, 0], md[:, -1], md.mean(1), md[:, -1] - md[:, 0], mb, mz,
                            ((b <= -1) & (p < 0.01)).mean(1), (p < 0.05).mean(1), -np.log(np.clip(p, 1e-12, 1)).mean(1),
                            sb, b.std(1), Y.std(1).mean(1), md.max(1) - md.min(1)])

def s_trend(T, Y): return stat_md(T, Y)
def s_rate(T, Y): return -_ols(T, Y.mean(2)[..., None])[0][:, 0]
def s_poplr(T, Y): return stat_poplr(T, Y)
def d1_flag(T, Y):
    k = T.shape[1]; return stats.t.cdf(-stat_md(T, Y), df=max(k - 2, 1)) < ALPHA

class EventLimits:
    """Change limits from short-interval (<= 0.5 y) test pairs of calibration eyes, per 2-dB baseline bin, for each q."""
    def __init__(self, eyes):
        base, diff = [], []
        for s in eyes:
            t, Y = s['t'], s['Y']
            for i in range(len(t) - 1):
                if t[i + 1] - t[i] <= 0.5: base.append(Y[i]); diff.append(Y[i + 1] - Y[i])
        base = np.concatenate(base); diff = np.concatenate(diff)
        self.edges = np.arange(0, 42, 2); self.lim = {}
        for q in Q_GRID + (0.05,):
            lim = np.full(len(self.edges), np.nan)
            for j, a in enumerate(self.edges):
                m = (base >= a) & (base < a + 2)
                if m.sum() >= 200: lim[j] = np.quantile(diff[m], q)
            ok = ~np.isnan(lim); self.lim[q] = np.interp(self.edges, self.edges[ok], lim[ok])
    def det(self, Y, q):
        """Y (n,k,L) -> deteriorated mask (n, k-2, L) for follow-ups 3..k."""
        b = Y[:, :2].mean(1); idx = np.clip((b // 2).astype(int), 0, len(self.edges) - 1)
        return (Y[:, 2:] - b[:, None]) < self.lim[q][idx][:, None]
    def flag(self, Y, q, m):
        k = Y.shape[1]; dm = self.det(Y, q)
        if k == 3: return dm[:, 0].sum(1) >= m
        cons = dm[:, 1:] & dm[:, :-1]
        return (cons.sum(2) >= m).any(1)

# ------------------------------------------------------------------ shuffles
def shuffled_batch(eyes, k, n_perm, rng, exclude_identity=True):
    T, Y = [], []
    for s in eyes:
        if len(s['t']) < k: continue
        for _ in range(n_perm):
            while True:
                P = rng.permutation(k)
                if not exclude_identity or (P != np.arange(k)).any(): break
            T.append(s['t'][:k]); Y.append(s['Y'][:k][P])
    return np.array(T), np.array(Y)

def shuffled_sequences(eyes, n_perm, rng, kmax=6):
    """Permute the first kmax tests (non-identity); looks are prefixes of length 3..kmax."""
    T, Y = [], []
    for s in eyes:
        if len(s['t']) < kmax: continue
        for _ in range(n_perm):
            while True:
                P = rng.permutation(kmax)
                if (P != np.arange(kmax)).any(): break
            T.append(s['t'][:kmax]); Y.append(s['Y'][:kmax][P])
    return np.array(T), np.array(Y)

def upper_thr(scores, a):
    return float(np.quantile(scores, 1 - a, method='higher'))

# ------------------------------------------------------------------ ML wrappers
class LGBLabel:
    """Study 1 D8 model (labels R1). Returns scores; thresholds handled outside."""
    def __init__(self, seed): self.seed = seed; self.m = {}; self.thr95 = {}
    def fit(self, fit_eyes, sel_eyes):
        import lightgbm as lgb
        from sklearn.metrics import roc_auc_score
        for k in KS:
            def rows(E):
                E = [s for s in E if s['R1'] is not None and len(s['t']) >= k]
                return tab_batch(np.array([s['t'][:k] for s in E]), np.array([s['Y'][:k] for s in E])), np.array([s['R1'] for s in E])
            Xt, yt = rows(fit_eyes); Xv, yv = rows(sel_eyes); best = None
            for cfg in D.MLTabular.GRID:
                mdl = lgb.LGBMClassifier(**cfg, min_child_samples=10, subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                                         random_state=self.seed, verbose=-1).fit(Xt, yt)
                a = roc_auc_score(yv, mdl.predict_proba(Xv)[:, 1])
                if best is None or a > best[0]: best = (a, mdl)
            self.m[k] = best[1]; sv = best[1].predict_proba(Xv)[:, 1]
            self.thr95[k] = float(np.quantile(sv[yv == 0], 0.95))
        return self
    def score(self, T, Y): return self.m[T.shape[1]].predict_proba(tab_batch(T, Y))[:, 1]

class OrderLGB:
    """Self-supervised: real-order vs shuffled first-k series."""
    def __init__(self, seed): self.seed = seed; self.m = {}
    def fit(self, fit_eyes, rng):
        import lightgbm as lgb
        for k in KS:
            E = [s for s in fit_eyes if len(s['t']) >= k]
            Tr = np.array([s['t'][:k] for s in E]); Yr = np.array([s['Y'][:k] for s in E])
            Ts, Ys = shuffled_batch(E, k, 3, rng)
            X = np.vstack([tab_batch(Tr, Yr), tab_batch(Ts, Ys)]); y = np.r_[np.ones(len(Tr)), np.zeros(len(Ts))]
            self.m[k] = lgb.LGBMClassifier(n_estimators=400, learning_rate=0.05, num_leaves=15, subsample=0.8, subsample_freq=1,
                                           colsample_bytree=0.8, random_state=self.seed, verbose=-1).fit(X, y)
        return self
    def score(self, T, Y): return self.m[T.shape[1]].predict_proba(tab_batch(T, Y))[:, 1]

class GRULabel:
    def __init__(self, seed): self.seed = seed; self.inner = D.MLSequence(seed=seed)
    def fit(self, fit_eyes, sel_eyes, quick=False):
        conv = lambda E: [dict(t=s['t'], Y=s['Y'], label=s['R1']) for s in E]
        if quick: self.inner.GRID = self.inner.GRID[:2]
        self.inner.fit(conv(fit_eyes), conv(sel_eyes), ks=KS); return self
    def score(self, T, Y):
        import torch
        dt = np.diff(np.concatenate([np.zeros((len(T), 1)), T], 1), axis=1)[..., None]
        x = np.concatenate([Y / 35.0, dt], 2)
        with torch.no_grad():
            return self.inner.models[T.shape[1]](torch.tensor(x, dtype=torch.float32)).numpy()

# ------------------------------------------------------------------ main
def main(mode):
    t0 = time.time(); quick = mode == 'quick'
    keep = ~blind_spot_mask(); S = load_series()
    eyes = []
    for s in S:
        if len(s['ages']) < 3: continue
        e = dict(pid=s['pid'], eye=s['eye'], t=s['ages'] - s['ages'][0], Y=s['sens'][:, keep], fold=h(s['pid'], 'uwhvf-cv-v2') % 5,
                 inner=h(s['pid'], 'uwhvf-inner-v2') % 4)
        e.update(references(s)); e.setdefault('R1', None); e.setdefault('R2', None)
        eyes.append(e)
    A = load_artes(); G = load_grape()
    seeds = [0] if quick else [0, 1, 2]
    folds = [0] if quick else [0, 1, 2, 3, 4]
    if quick: eyes = eyes[::5]
    rows = []
    def rec(fold, seed, det, k, ev, unit, flag):
        rows.append((fold, seed, det, k, ev, unit, int(flag)))
    gpids = sorted({g['pid'] for g in G}); gfold = {p: h(p, 'grape-cv-v2') % 5 for p in gpids}
    for f in folds:
        cal = [e for e in eyes if e['fold'] != f]; ev = [e for e in eyes if e['fold'] == f]
        fit_e = [e for e in cal if e['inner'] != 0]; sel_e = [e for e in cal if e['inner'] == 0]
        ev8 = [e for e in ev if len(e['t']) >= 8]
        donors = {k: [e['t'][:k] for e in ev if len(e['t']) >= k] for k in KS}
        if quick: ev8 = ev8[:20]
        for seed in seeds:
            set_seed(seed); rng = np.random.default_rng(100 * f + seed)
            ev_lim = EventLimits(cal)
            lgbm = LGBLabel(seed).fit(fit_e, sel_e)
            olgb = OrderLGB(seed).fit(fit_e, rng)
            gru = GRULabel(seed).fit(fit_e, sel_e, quick)
            print(f'fold {f} seed {seed} models fitted {time.time() - t0:.0f}s', flush=True)
            # ---- per-look calibration
            score_fns = {'S1 SC-Trend': s_trend, 'S2 SC-Rate': s_rate, 'S3 SC-PoPLR': s_poplr,
                         'S5 SC-LightGBM': lgbm.score, 'S7 SC-GRU': gru.score}
            thr, ev_cfg = {}, {}
            for k in KS:
                Tc, Yc = shuffled_batch(cal, k, 4 if quick else 20, rng)
                for name, fn in score_fns.items():
                    thr[(name, k)] = upper_thr(fn(Tc, Yc), ALPHA)
                Ts, Ys = shuffled_batch(sel_e, k, 4 if quick else 20, rng)
                thr[('S6 Order-LightGBM', k)] = upper_thr(olgb.score(Ts, Ys), ALPHA)
                best = None
                for q in Q_GRID:
                    for m in M_GRID:
                        r = ev_lim.flag(Yc, q, m).mean()
                        if r <= ALPHA and (best is None or r > best[0] or (r == best[0] and q > best[1])): best = (r, q, m)
                ev_cfg[k] = best[1:] if best else (0.01, 4)
            all_fns = dict(score_fns); all_fns['S6 Order-LightGBM'] = olgb.score
            def perlook_flags(T, Y):
                k = T.shape[1]; out = {'D1 OLS-MD': d1_flag(T, Y)}
                out['D7 Event'] = ev_lim.flag(Y, 0.05, 3) if k >= 4 else np.zeros(len(T), bool)
                out['S4 SC-Event'] = ev_lim.flag(Y, *ev_cfg[k])
                for name, fn in all_fns.items():
                    sc = fn(T, Y); out[name] = sc > thr[(name, k)]
                    if name == 'S5 SC-LightGBM': out['B8 LightGBM-95spec'] = sc > lgbm.thr95[k]
                return out
            # ---- cumulative calibration (looks = prefixes 3..6 of shuffled 6-test sequences)
            Tq, Yq = shuffled_sequences(cal, 4 if quick else 20, rng)
            seq_scores = {n: np.column_stack([fn(Tq[:, :k], Yq[:, :k]) for k in KS]) for n, fn in
                          (('Q1 Sequential trend', s_trend), ('Q4 Sequential Order-LightGBM', olgb.score))}
            cum_thr = {}
            for name, M in list(seq_scores.items()) + [('Q2 Confirmed trend', seq_scores['Q1 Sequential trend'])]:
                lo, hi = 1e-4, 0.5
                for _ in range(30):
                    a = (lo + hi) / 2; th = np.array([upper_thr(M[:, j], a) for j in range(len(KS))]); F = M > th
                    if name.startswith('Q2'): F = np.column_stack([np.zeros(len(F), bool)] + [F[:, j] & F[:, j - 1] for j in range(1, len(KS))])
                    (lo, hi) = (a, hi) if F.any(1).mean() <= ALPHA else (lo, a)
                cum_thr[name] = np.array([upper_thr(M[:, j], lo) for j in range(len(KS))])
            best = None
            for q in Q_GRID:
                for m in M_GRID:
                    F = np.column_stack([ev_lim.flag(Yq[:, :k], q, m) for k in KS]).any(1).mean()
                    if F <= ALPHA and (best is None or F > best[0] or (F == best[0] and q > best[1])): best = (F, q, m)
            q3 = best[1:] if best else (0.01, 4)
            def cumulative_flags(T6, Y6):
                """T6 (n,6), Y6 (n,6,L) -> dict name -> (n,4) per-look flags under cumulative control."""
                out = {}
                sc1 = np.column_stack([s_trend(T6[:, :k], Y6[:, :k]) for k in KS])
                sc4 = np.column_stack([olgb.score(T6[:, :k], Y6[:, :k]) for k in KS])
                out['Q1 Sequential trend'] = sc1 > cum_thr['Q1 Sequential trend']
                F = sc1 > cum_thr['Q2 Confirmed trend']
                out['Q2 Confirmed trend'] = np.column_stack([np.zeros(len(F), bool)] + [F[:, j] & F[:, j - 1] for j in range(1, len(KS))])
                out['Q3 Confirmed SC-Event'] = np.column_stack([ev_lim.flag(Y6[:, :k], *q3) for k in KS])
                out['Q4 Sequential Order-LightGBM'] = sc4 > cum_thr['Q4 Sequential Order-LightGBM']
                out['D1-repeated'] = np.column_stack([d1_flag(T6[:, :k], Y6[:, :k]) for k in KS])
                out['D7-repeated'] = np.column_stack([ev_lim.flag(Y6[:, :k], 0.05, 3) if k >= 4 else np.zeros(len(T6), bool) for k in KS])
                return out
            # ---- E1: held-out UWHVF eyes with >= 8 tests (per look and cumulative)
            for k in KS:
                Tk = np.array([e['t'][:k] for e in ev8]); Yk = np.array([e['Y'][:k] for e in ev8])
                for name, fl in perlook_flags(Tk, Yk).items():
                    for e, v in zip(ev8, fl): rec(f, seed, name, k, 'E1', e['pid'] + e['eye'], v)
            T6 = np.array([e['t'][:6] for e in ev8]); Y6 = np.array([e['Y'][:6] for e in ev8])
            for name, Fm in cumulative_flags(T6, Y6).items():
                for j, k in enumerate(KS):
                    for e, v in zip(ev8, Fm[:, j]): rec(f, seed, name, k, 'E1cum', e['pid'] + e['eye'], v)
            # ---- E2: Artes per-look windows (donor dates) and cumulative series
            draws = 2 if quick else 10
            for k in KS:
                T, Y, U = [], [], []
                for a in A:
                    for i in range(0, 12 - k + 1):
                        for d in range(draws):
                            T.append(donors[k][rng.integers(len(donors[k]))]); Y.append(a['sens'][i:i + k][:, keep]); U.append(f"{a['pid']}|{i}|{d}")
                for name, fl in perlook_flags(np.array(T), np.array(Y)).items():
                    for u, v in zip(U, fl): rec(f, seed, name, k, 'E2', u, v)
            T, Y, U = [], [], []
            for a in A:
                for d in range(draws):
                    T.append(donors[6][rng.integers(len(donors[6]))]); Y.append(a['sens'][:6][:, keep]); U.append(f"{a['pid']}|0|{d}")
            for name, Fm in cumulative_flags(np.array(T), np.array(Y)).items():
                for j, k in enumerate(KS):
                    for u, v in zip(U, Fm[:, j]): rec(f, seed, name, k, 'E2cum', u, v)
            # ---- E4: GRAPE (grid-agnostic: D1, S1, S5, B8, S6) with UWHVF thresholds and local cross-fitted thresholds
            for k in (3, 4):
                Gk = [g for g in G if len(g['t']) >= k]
                for gf in range(5):
                    gcal = [dict(t=g['t'], Y=g['sens']) for g in G if gfold[g['pid']] != gf]
                    gev = [g for g in Gk if gfold[g['pid']] == gf]
                    if not gev: continue
                    # local shuffle pools, scored eye by eye (GRAPE eyes differ in number of analysable points)
                    pools = {n: [] for n in ('S1 SC-Trend', 'S5 SC-LightGBM', 'S6 Order-LightGBM')}
                    for c in gcal:
                        if len(c['t']) < k: continue
                        Tc, Yc = shuffled_batch([c], k, 4 if quick else 20, rng)
                        pools['S1 SC-Trend'].append(s_trend(Tc, Yc)); pools['S5 SC-LightGBM'].append(lgbm.score(Tc, Yc))
                        pools['S6 Order-LightGBM'].append(olgb.score(Tc, Yc))
                    loc_thr = {n: upper_thr(np.concatenate(v), ALPHA) for n, v in pools.items()}
                    groups = {}
                    for i, g in enumerate(gev): groups.setdefault(g['sens'].shape[1], []).append(i)
                    for L, idx in groups.items():
                        Ti = np.array([gev[i]['t'][:k] for i in idx]); Yi = np.array([gev[i]['sens'][:k] for i in idx])
                        outs = {'D1 OLS-MD': d1_flag(Ti, Yi)}
                        for name, fn in (('S1 SC-Trend', s_trend), ('S5 SC-LightGBM', lgbm.score), ('S6 Order-LightGBM', olgb.score)):
                            sc = fn(Ti, Yi)
                            outs[name + ' (UW threshold)'] = sc > thr[(name, k)]
                            outs[name + ' (local threshold)'] = sc > loc_thr[name]
                            if name == 'S5 SC-LightGBM': outs['B8 LightGBM-95spec'] = sc > lgbm.thr95[k]
                        for name, fl in outs.items():
                            for i, v in zip(idx, fl):
                                g = gev[i]; rec(f, seed, name, k, 'E4', f"{g['pid']}{g['eye']}|MD={g['MD']};PLR2={g['PLR2']};PLR3={g['PLR3']}", v)
            print(f'fold {f} seed {seed} done {time.time() - t0:.0f}s', flush=True)
    df = pd.DataFrame(rows, columns=['fold', 'seed', 'detector', 'k', 'eval', 'unit', 'flag'])
    os.makedirs(RES, exist_ok=True)
    out = os.path.join(RES, 'study2_raw_quick.csv' if quick else 'study2_raw.csv'); df.to_csv(out, index=False)
    refs = pd.DataFrame([dict(unit=e['pid'] + e['eye'], pid=e['pid'], fold=e['fold'], n_tests=len(e['t']),
                              **{k: e.get(k) for k in ['R1', 'R2'] + [f'R3_{k}' for k in KS]}) for e in eyes if len(e['t']) >= 8])
    refs.to_csv(os.path.join(RES, 'study2_refs_quick.csv' if quick else 'study2_refs.csv'), index=False)
    meta = dict(mode=mode, folds=folds, seeds=seeds, n_rows=len(df), n_eval_eyes=int(len(refs)),
                n_R1_prog=int((refs.R1 == 1).sum()), n_R1_stable=int((refs.R1 == 0).sum()), runtime_s=time.time() - t0)
    json.dump(meta, open(os.path.join(RES, f'study2_meta_{mode}.json'), 'w'), indent=1); print(json.dumps(meta))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--mode', default='quick', choices=['quick', 'full'])
    main(ap.parse_args().mode)
