"""Prompt-2 extension (protocol amendment A3, see experiments/protocol.md). Usage: python run_v2.py [--quick]
Whole-cohort 5-fold patient-level cross-fitting on UWHVF (all splits) for detectors D1-D8 and the new D11
(null-calibrated ML), with (i) the original full-series reference, (ii) a FUTURE-ONLY reference computed from tests
after the first k, (iii) the Artes true no-change arm, (iv) the shuffle audit.
Writes ../results/raw_results_v2.csv(.gz) and ../results/run_meta_v2.json."""
import sys, os, json, time, hashlib, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from src.utils import set_seed
from src.data.uwhvf import load_series, blind_spot_mask
from src.data.artes_retest import load_artes
from src.models import detectors as D
from src.models.deferral import ols, md_series
from run_all import reference, make
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
KS = (3, 4, 5, 6)

def future_reference(s, k):
    """Reference from tests k+1..end only (needs >= 5 future tests). Same thresholds as the primary reference."""
    if len(s['ages']) < k + 5: return None
    t = s['ages'][k:] - s['ages'][k]; b, p, _ = ols(t, md_series(s['td'][k:]))
    return 1 if (b < -0.3 and p < 0.01) else (0 if p > 0.5 else None)

def future_reference_sym(s, k):
    """Symmetric 'no-change' stable definition: |future slope| <= 0.2 dB/yr (progressor rule unchanged)."""
    if len(s['ages']) < k + 5: return None
    t = s['ages'][k:] - s['ages'][k]; b, p, _ = ols(t, md_series(s['td'][k:]))
    return 1 if (b < -0.3 and p < 0.01) else (0 if abs(b) <= 0.2 else None)

def fold_of(pid, salt='uwhvf-cf-v1'): return int(hashlib.sha256((salt + pid).encode()).hexdigest()[:8], 16) % 5
def inner_val(pid): return int(hashlib.sha256(('uwhvf-cf-inner' + pid).encode()).hexdigest()[:8], 16) % 4 == 0

class NullCalibratedML(D.MLTabular):            # D11
    """D8's LightGBM score, but the decision threshold is a conformal p-value against SHUFFLED validation series
    (5 shuffles per eye, Mondrian strata = mean-sensitivity tertile), instead of 95% specificity on reference-stable eyes."""
    name = 'D11 Null-calibrated ML (LightGBM + shuffle conformal)'
    def fit(self, train, val, ks=KS):
        super().fit(train, val, ks); rng = np.random.default_rng(10_000 + self.seed); self.pool = {}
        for k in ks:
            X, b = [], []
            for s in val:
                if len(s['t']) < k: continue
                for _ in range(5):
                    X.append(D.tab_features(s['t'][:k], s['Y'][:k][rng.permutation(k)])); b.append(D.lvl3(s['Y'][:k]))
            sc = self.models[k].predict_proba(np.array(X))[:, 1]; b = np.array(b)
            self.pool[k] = {j: np.sort(sc[b == j]) for j in np.unique(b)}
        return self
    def flags(self, k, T, Ys):
        X = np.array([D.tab_features(t, Y) for t, Y in zip(T, Ys)]); sc = self.models[k].predict_proba(X)[:, 1]
        out = []
        for s, Y in zip(sc, Ys):
            c = self.pool[k].get(D.lvl3(Y));
            if c is None or len(c) < 50: c = np.sort(np.concatenate(list(self.pool[k].values())))
            out.append((1 + len(c) - np.searchsorted(c, s, side='left')) / (len(c) + 1) < 0.05)
        return np.array(out)

def batch_flags(det, k, T, Ys):
    if hasattr(det, 'flags'): return det.flags(k, T, Ys)
    if isinstance(det, D.MLTabular):
        X = np.array([D.tab_features(t, Y) for t, Y in zip(T, Ys)])
        return det.models[k].predict_proba(X)[:, 1] > det.thr[k]
    return np.array([bool(det.flag(t, Y)) for t, Y in zip(T, Ys)])

DETS = [D.OLSMD, D.MDRate, D.PLR3, D.PoPLRWithin, D.PooledShuffleMD, D.PooledDetrendedRegion, D.EventAnalysis,
        D.MLTabular, NullCalibratedML]
STOCH = D.STOCHASTIC | {NullCalibratedML.name}

def main(quick):
    t0 = time.time(); keep = ~blind_spot_mask(); S = load_series(); A = load_artes()
    def to_d(s):
        return dict(pid=s['pid'], eye=s['eye'], t=s['ages'] - s['ages'][0], Y=s['sens'][:, keep],
                    label=reference(s) if len(s['ages']) >= 8 else None, raw=s)
    E = [to_d(s) for s in S if len(s['ages']) >= 3]
    for e in E:
        e['fref'] = {k: future_reference(e['raw'], k) for k in KS}
        e['fsym'] = {k: future_reference_sym(e['raw'], k) for k in KS}
        e['fold'] = fold_of(e['pid'])
    seeds = [0] if quick else [0, 1, 2, 3, 4]; folds = [0] if quick else range(5); rows = []
    for fo in folds:
        tr_all = [e for e in E if e['fold'] != fo]; ev = [e for e in E if e['fold'] == fo]
        train = [e for e in tr_all if not inner_val(e['pid'])]; val = [e for e in tr_all if inner_val(e['pid'])]
        if quick: train, ev = train[::5], ev[::3]
        donors = {k: [e['t'][:k] for e in ev if len(e['t']) >= k] for k in KS}
        for cls in DETS:
            for seed in (seeds if cls.name in STOCH else [0]):
                set_seed(seed); det = make(cls, seed)
                if quick and hasattr(det, 'GRID'): det.GRID = det.GRID[:2]
                kw = {'ks': KS} if 'ks' in det.fit.__code__.co_varnames else {}
                det.fit(train, val, **kw); rng = np.random.default_rng(1000 * fo + seed)
                for k in KS:
                    # E1 (full-series ref), E1F (future-only ref), E1S (future-only, symmetric stable)
                    R = [e for e in ev if len(e['t']) >= 8 and (e['label'] is not None or e['fref'][k] is not None or e['fsym'][k] is not None)]
                    f = batch_flags(det, k, [e['t'][:k] for e in R], [e['Y'][:k] for e in R])
                    for e, fl in zip(R, f):
                        u = e['pid'] + e['eye']
                        if e['label'] is not None: rows.append((cls.name, seed, fo, k, 'E1', u, int(fl), e['label']))
                        if e['fref'][k] is not None: rows.append((cls.name, seed, fo, k, 'E1F', u, int(fl), e['fref'][k]))
                        if e['fsym'][k] is not None: rows.append((cls.name, seed, fo, k, 'E1S', u, int(fl), e['fsym'][k]))
                    # E2 Artes windows with donor spacing (2 draws per window per fold -> 10 over folds)
                    T, Ys, U = [], [], []
                    for a in A:
                        for i in range(0, 12 - k + 1):
                            for d in range(2):
                                T.append(donors[k][rng.integers(len(donors[k]))]); Ys.append(a['sens'][i:i + k][:, keep])
                                U.append(f"{a['pid']}{a['eye']}|{i}|{fo}{d}")
                    for u, fl in zip(U, batch_flags(det, k, T, Ys)): rows.append((cls.name, seed, fo, k, 'E2', u, int(fl), 0))
                    # E3 shuffle audit (2 shuffles per eye)
                    T, Ys, U = [], [], []
                    for e in ev:
                        if len(e['t']) >= k:
                            for r in range(2):
                                T.append(e['t'][:k]); Ys.append(e['Y'][:k][rng.permutation(k)]); U.append(f"{e['pid']}{e['eye']}|{r}")
                    for u, fl in zip(U, batch_flags(det, k, T, Ys)): rows.append((cls.name, seed, fo, k, 'E3', u, int(fl), 0))
                print(f'fold {fo} {cls.name} seed {seed} {time.time() - t0:.0f}s', flush=True)
    d = pd.DataFrame(rows, columns=['detector', 'seed', 'fold', 'k', 'eval', 'unit', 'flag', 'label'])
    out = os.path.join(ROOT, 'results', 'raw_results_v2_quick.csv' if quick else 'raw_results_v2.csv'); d.to_csv(out, index=False)
    meta = dict(mode='quick' if quick else 'full', ks=KS, seeds=seeds, folds=list(folds), n_eyes=len(E),
                n_ref_full=dict(prog=sum(e['label'] == 1 for e in E), stable=sum(e['label'] == 0 for e in E)),
                n_ref_future={k: dict(prog=sum(e['fref'][k] == 1 for e in E), stable=sum(e['fref'][k] == 0 for e in E),
                                      stable_sym=sum(e['fsym'][k] == 0 for e in E)) for k in KS}, runtime_s=time.time() - t0)
    json.dump(meta, open(os.path.join(ROOT, 'results', f"run_meta_v2{'_quick' if quick else ''}.json"), 'w'), indent=1, default=int)
    print(json.dumps(meta, default=int))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--quick', action='store_true'); main(ap.parse_args().quick)
