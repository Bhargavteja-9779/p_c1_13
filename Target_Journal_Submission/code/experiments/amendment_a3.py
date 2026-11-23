"""Protocol amendment A3 (see protocol.md): A3a shuffle-calibrated thresholds (SCT) for D2, D6, D8, D9;
A3c enlarged reference for training-free detectors D1-D4. (A3b confirmation is computed in summarise_a3.py from the
existing full-run flags.)  Usage (from code/): python experiments/amendment_a3.py  -> ../results/a3_raw.csv.gz"""
import sys, os, json, time, hashlib
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np, pandas as pd
from src.utils import set_seed
from src.data.uwhvf import load_series, patient_split, blind_spot_mask
from src.data.artes_retest import load_artes
from src.data.grape import load_grape
from src.models import detectors as D
from run_all import reference
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')); RES = os.path.join(ROOT, 'results')
KS = (3, 4, 5, 6); SEEDS = (0, 1, 2, 3, 4); NSHUF = 10


def score_fn(name, det):
    """Higher score = more evidence of progression."""
    if name.startswith('D2'): return lambda t, Y: -D.md_slope(t, Y)[0]
    if name.startswith('D6'): return lambda t, Y: -det.cals[len(t)].pvalue(t, Y)
    if name.startswith('D8'):
        return lambda t, Y: float(det.models[len(t)].predict_proba(D.tab_features(t, Y)[None])[0, 1])
    if name.startswith('D9'):
        import torch
        def f(t, Y):
            x = np.hstack([Y / 35.0, np.diff(np.r_[0, t])[:, None]])
            with torch.no_grad(): return float(det.models[len(t)](torch.tensor(x[None], dtype=torch.float32))[0])
        return f


def shuffled_threshold(sf, series, k, rng):
    sc = []
    for t, Y in series:
        if len(t) >= k:
            for _ in range(NSHUF):
                P = rng.permutation(k); sc.append(sf(t[:k], Y[:k][P]))
    return float(np.quantile(sc, 0.95))


def main():
    t0 = time.time(); keep = ~blind_spot_mask(); S = load_series(); sp = patient_split(S)
    def to_d(s, lab=True):
        return dict(pid=s['pid'], eye=s['eye'], t=s['ages'] - s['ages'][0], Y=s['sens'][:, keep],
                    label=reference(s) if (lab and len(s['ages']) >= 8) else None, raw=s)
    train = [to_d(s) for s in S if sp[s['pid']] == 'train' and len(s['ages']) >= 3]
    val = [to_d(s) for s in S if sp[s['pid']] == 'val' and len(s['ages']) >= 3]
    test = [to_d(s) for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 3]
    A = load_artes(); G = load_grape()
    donors = {k: [s['t'][:k] for s in test if len(s['t']) >= k] for k in KS}
    rows = []
    def rec(**kw): rows.append(kw)
    # ---------------- A3a SCT ----------------
    for cls in (D.MDRate, D.PooledDetrendedRegion, D.MLTabular, D.MLSequence):
        name = cls.name
        for seed in (SEEDS if name in D.STOCHASTIC else (0,)):
            set_seed(seed)
            det = cls(seed=seed) if 'seed' in getattr(cls.__init__, '__code__', type('x', (), {'co_varnames': ()})).co_varnames else cls()
            kw = {'ks': KS} if 'ks' in det.fit.__code__.co_varnames else {}
            det.fit(train, val, **kw); sf = score_fn(name, det)
            rng = np.random.default_rng(3000 + seed)
            for k in KS:
                thr = shuffled_threshold(sf, [(s['t'], s['Y']) for s in val], k, rng)
                rec(det=name, seed=seed, k=k, eval='THR', unit='', flag=np.nan, label=np.nan, extra=thr)
                for s in test:
                    if len(s['t']) >= 8 and s['label'] is not None:
                        rec(det=name, seed=seed, k=k, eval='E1', unit=s['pid'] + s['eye'], flag=int(sf(s['t'][:k], s['Y'][:k]) > thr), label=s['label'], extra='')
                r2 = np.random.default_rng(4000 + seed)
                for a in A:
                    for i in range(0, 12 - k + 1):
                        for d in range(10):
                            tt = donors[k][r2.integers(len(donors[k]))]
                            rec(det=name, seed=seed, k=k, eval='E2', unit=f"{a['pid']}|{i}|{d}", flag=int(sf(tt, a['sens'][i:i + k][:, keep]) > thr), label=np.nan, extra='')
            print(f'{name} seed {seed} UW/Artes done {time.time() - t0:.0f}s', flush=True)
            # GRAPE: own-clinic SCT by 5-fold patient cross-fitting (D2, D8 only)
            if name.startswith(('D2', 'D8')):
                pids = sorted({g['pid'] for g in G})
                fold_of = {p: int(hashlib.sha256(('grape' + p).encode()).hexdigest()[:4], 16) % 5 for p in pids}
                rg = np.random.default_rng(5000 + seed)
                for fo in range(5):
                    cal = [(g['t'], g['sens']) for g in G if fold_of[g['pid']] != fo]
                    for k in (3, 4):
                        thr = shuffled_threshold(sf, cal, k, rg)
                        for g in G:
                            if fold_of[g['pid']] == fo and len(g['t']) >= k:
                                rec(det=name, seed=seed, k=k, eval='E4', unit=g['pid'] + g['eye'], flag=int(sf(g['t'][:k], g['sens'][:k]) > thr), label=g['MD'], extra='')
    # ---------------- A3c enlarged reference (training-free detectors) ----------------
    allref = [to_d(s) for s in S if len(s['ages']) >= 8]
    allref = [s for s in allref if s['label'] is not None]
    for cls in (D.OLSMD, D.MDRate, D.PLR3, D.PoPLRWithin):
        det = cls(seed=0) if 'seed' in getattr(cls.__init__, '__code__', type('x', (), {'co_varnames': ()})).co_varnames else cls()
        for s in allref:
            for k in KS:
                rec(det=cls.name, seed=0, k=k, eval='E1all', unit=s['pid'] + s['eye'], flag=int(det.flag(s['t'][:k], s['Y'][:k])), label=s['label'], extra=sp[s['pid']])
        print(f'{cls.name} enlarged reference done {time.time() - t0:.0f}s', flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(RES, 'a3_raw.csv.gz'), index=False)
    json.dump(dict(runtime_s=time.time() - t0, n_allref=len(allref), n_allref_prog=sum(s['label'] == 1 for s in allref),
                   n_allref_stable=sum(s['label'] == 0 for s in allref)), open(os.path.join(RES, 'a3_meta.json'), 'w'), indent=1)
    print('done', time.time() - t0)


if __name__ == '__main__':
    main()
