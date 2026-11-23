"""Run the full benchmark. Usage: python run_all.py --mode quick|full
Writes ../results/raw_results.csv (one row per detector x seed x k x evaluation unit) and ../results/run_meta.json,
then calls src/statistics/summarise.py and src/visualization/figures.py."""
import sys, os, json, time, argparse, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, pandas as pd
from src.utils import set_seed
from src.data.uwhvf import load_series, patient_split, blind_spot_mask
from src.data.artes_retest import load_artes
from src.data.grape import load_grape
from src.models import detectors as D
from src.models.deferral import ols, md_series
from src.models.conformal_vf import _ols
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
RES = os.path.join(ROOT, 'results')

def reference(s, kind='md'):
    t = s['ages'] - s['ages'][0]
    if kind == 'md':
        b, p, _ = ols(t, md_series(s['td']))
        return 1 if (b < -0.3 and p < 0.01) else (0 if p > 0.5 else None)
    # secondary: full-series PoPLR with 2,000 random permutations
    from src.models.conformal_vf import stat_poplr
    rng = np.random.default_rng(int(hashlib.sha256((s['pid'] + s['eye']).encode()).hexdigest()[:6], 16))
    Y = s['sens'][:, ~blind_spot_mask()]; k = len(t)
    P = np.vstack([np.arange(k)] + [rng.permutation(k) for _ in range(2000)])
    sc = stat_poplr(np.broadcast_to(t, (len(P), k)), Y[P]); p = float((sc >= sc[0] - 1e-12).mean())
    return 1 if p < 0.01 else (0 if p > 0.5 else None)

def make(cls, seed):
    import inspect
    return cls(seed=seed) if 'seed' in inspect.signature(cls).parameters else cls()

def main(mode):
    t0 = time.time(); quick = mode == 'quick'
    KS = (4,) if quick else (3, 4, 5, 6)
    keep = ~blind_spot_mask(); S = load_series(); sp = patient_split(S)
    def to_d(s, with_label=True):
        lab = reference(s) if (with_label and len(s['ages']) >= 8) else None
        return dict(pid=s['pid'], eye=s['eye'], t=s['ages'] - s['ages'][0], Y=s['sens'][:, keep], label=lab, raw=s)
    train = [to_d(s) for s in S if sp[s['pid']] == 'train' and len(s['ages']) >= 3]
    val = [to_d(s) for s in S if sp[s['pid']] == 'val' and len(s['ages']) >= 3]
    test = [to_d(s) for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 3]
    if quick:   # quick mode never touches the locked test split: it evaluates on a validation subset
        train, val, test = train[::6], val[1::3], val[::3]
    for s in test:
        s['label2'] = reference(s['raw'], 'poplr') if len(s['t']) >= 8 else None
    A = load_artes(); G = load_grape()
    seeds = [0] if quick else [0, 1, 2, 3, 4]
    rows = []
    def rec(det, seed, k, ev, unit, flag, label=None, extra=''):
        rows.append(dict(detector=det, seed=seed, k=k, eval=ev, unit=unit, flag=int(flag), label=label, extra=extra))
    # spacing donors for Artes windows (amendment A1)
    donors = {k: [s['t'][:k] for s in test if len(s['t']) >= k] for k in KS}
    for cls in D.ALL:
        name = cls.name
        for seed in (seeds if name in D.STOCHASTIC else [0]):
            set_seed(seed)
            det = make(cls, seed)
            if quick and hasattr(det, 'epochs'): det.epochs = 2
            if quick and hasattr(det, 'GRID'): det.GRID = det.GRID[:2]
            fit_kw = {'ks': KS} if 'ks' in det.fit.__code__.co_varnames else {}
            det.fit(train, val, **fit_kw)
            rng = np.random.default_rng(1000 + seed)
            for k in KS:
                # E1 future reference (UW test, eyes >= 8 tests)
                for s in test:
                    if len(s['t']) >= 8 and (s['label'] is not None or s['label2'] is not None):
                        f = det.flag(s['t'][:k], s['Y'][:k])
                        rec(name, seed, k, 'E1', s['pid'] + s['eye'], f, s['label'], '' if s['label2'] is None else str(s['label2']))
                # E2 Artes true no-change windows with donor spacing
                for a in A:
                    for i in range(0, 12 - k + 1):
                        for d in range(2 if quick else 10):
                            tt = donors[k][rng.integers(len(donors[k]))]
                            rec(name, seed, k, 'E2', f"{a['pid']}|{i}|{d}", det.flag(tt, a['sens'][i:i + k][:, keep]))
                # E3 shuffle audit (UW test, first k tests re-ordered)
                for s in test:
                    if len(s['t']) >= k:
                        for r in range(2 if quick else 10):
                            P = rng.permutation(k)
                            rec(name, seed, k, 'E3', f"{s['pid']}{s['eye']}|{r}", det.flag(s['t'][:k], s['Y'][:k][P]))
            print(f'{name} seed {seed} done {time.time() - t0:.0f}s', flush=True)
        # E4 GRAPE (grid-agnostic detectors only)
        if name in D.GRID_AGNOSTIC:
            gk = [k for k in KS if k in (3, 4)]
            for seed in (seeds if name in D.STOCHASTIC else [0]):
                folds = {}
                pids = sorted({g['pid'] for g in G})
                fold_of = {p: int(hashlib.sha256(('grape' + p).encode()).hexdigest()[:4], 16) % 5 for p in pids}
                for fo in range(5):
                    gtr = [dict(t=g['t'], Y=g['sens'], label=None) for g in G if fold_of[g['pid']] != fo]
                    if name == 'D8 ML-tabular (LightGBM)':
                        det = folds.get('uw')
                        if det is None:
                            set_seed(seed); det = D.MLTabular(seed=seed)
                            if quick: det.GRID = det.GRID[:2]
                            det.fit(train, val, ks=tuple(gk)); folds['uw'] = det
                    else:
                        det = make(cls, seed)
                        fit_kw = {'ks': tuple(gk)} if 'ks' in det.fit.__code__.co_varnames else {}
                        det.fit(gtr, None, **fit_kw)
                    for g in G:
                        if fold_of[g['pid']] != fo: continue
                        for k in gk:
                            if len(g['t']) >= k:
                                rec(name, seed, k, 'E4', g['pid'] + g['eye'], det.flag(g['t'][:k], g['sens'][:k]),
                                    g['MD'], f"PLR2={g['PLR2']};PLR3={g['PLR3']}")
            print(f'{name} GRAPE done {time.time() - t0:.0f}s', flush=True)
    os.makedirs(RES, exist_ok=True)
    out = os.path.join(RES, 'raw_results.csv' if not quick else 'raw_results_quick.csv')
    pd.DataFrame(rows).to_csv(out, index=False)
    meta = dict(mode=mode, ks=KS, seeds=seeds, n_train=len(train), n_val=len(val), n_test=len(test),
                n_test_ref=sum(1 for s in test if len(s['t']) >= 8 and s['label'] is not None),
                n_test_prog=sum(1 for s in test if s['label'] == 1), n_test_stable=sum(1 for s in test if s['label'] == 0),
                n_artes=len(A), n_grape=len(G), runtime_s=time.time() - t0)
    json.dump(meta, open(os.path.join(RES, f'run_meta_{mode}.json'), 'w'), indent=1)
    print(json.dumps(meta))

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--mode', default='quick', choices=['quick', 'full'])
    main(ap.parse_args().mode)
