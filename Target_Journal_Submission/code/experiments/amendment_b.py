"""Amendment B (protocol.md): no-change-calibrated thresholds (B1/B2), all eligible eyes (B3), time-label sensitivity (B4).
Step 1 (this file, slow): compute continuous detector SCORES and B3/B4 flags -> ../results/amendB/*.csv.gz
Step 2: python -m src.statistics.amendment_b_stats  -> ../results/amendB/amendB.json
Usage (from code/): python experiments/amendment_b.py"""
import os, sys, time, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np, pandas as pd
from src.utils import set_seed
from src.data.uwhvf import load_series, patient_split, blind_spot_mask
from src.data.artes_retest import load_artes
from src.models import detectors as D
from src.models.conformal_vf import stat_md, stat_region
from run_all import reference, make
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
OUT = os.path.join(ROOT, 'results', 'amendB'); os.makedirs(OUT, exist_ok=True)
KS = (3, 4, 5, 6); SEEDS = [0, 1, 2, 3, 4]

def main():
    t0 = time.time(); keep = ~blind_spot_mask(); S = load_series(); sp = patient_split(S)
    def to_d(s):
        lab = reference(s) if len(s['ages']) >= 8 else None
        return dict(pid=s['pid'], eye=s['eye'], t=s['ages'] - s['ages'][0], Y=s['sens'][:, keep], label=lab, raw=s, split=sp[s['pid']])
    allE = [to_d(s) for s in S if len(s['ages']) >= 3]
    train = [s for s in allE if s['split'] == 'train']; val = [s for s in allE if s['split'] == 'val']
    test = [s for s in allE if s['split'] == 'test']
    for s in test:
        s['label2'] = reference(s['raw'], 'poplr') if len(s['t']) >= 8 else None
    A = load_artes()
    donors = {k: [s['t'][:k] for s in test if len(s['t']) >= k] for k in KS}
    rows = []
    def rec(det, seed, k, ev, unit, score, label=None):
        rows.append(dict(detector=det, seed=seed, k=k, eval=ev, unit=unit, score=float(score), label=label))
    # ---- score functions (higher = more evidence of progression) ----
    def scorer(det):
        n = det.name
        if n.startswith('D1'): return lambda t, Y: float(stat_md(t[None], Y[None])[0])
        if n.startswith('D2'): return lambda t, Y: -D.md_slope(t, Y)[0]
        if n.startswith('D6'): return lambda t, Y: float(stat_region(t[None], Y[None], det.regions)[0])
        if n.startswith('D8'): return lambda t, Y: float(det.models[len(t)].predict_proba(D.tab_features(t, Y)[None])[0, 1])
        if n.startswith('D9'):
            import torch
            def f(t, Y):
                x = np.hstack([Y / 35.0, np.diff(np.r_[0, t])[:, None]])
                with torch.no_grad(): return float(det.models[len(t)](torch.tensor(x[None], dtype=torch.float32))[0])
            return f
    plan = [(D.OLSMD, [0]), (D.MDRate, [0]), (D.PooledDetrendedRegion, [0]), (D.MLTabular, SEEDS), (D.MLSequence, SEEDS)]
    for cls, seeds in plan:
        for seed in seeds:
            set_seed(seed)
            det = make(cls, seed)
            fk = {'ks': KS} if 'ks' in det.fit.__code__.co_varnames else {}
            det.fit(train, val, **fk); f = scorer(det)
            rng = np.random.default_rng(1000 + seed)       # identical donor draws to the main run (E2), E3 draws consumed
            for k in KS:
                for s in test:
                    if len(s['t']) >= 8 and (s['label'] is not None or s['label2'] is not None):
                        rec(det.name, seed, k, 'E1', s['pid'] + s['eye'], f(s['t'][:k], s['Y'][:k]), s['label'])
                for a in A:
                    for i in range(0, 12 - k + 1):
                        for d in range(10):
                            tt = donors[k][rng.integers(len(donors[k]))]
                            rec(det.name, seed, k, 'E2', f"{a['pid']}|{i}|{d}", f(tt, a['sens'][i:i + k][:, keep]))
                for s in test:                                # consume E3 draws exactly as run_all did
                    if len(s['t']) >= k:
                        for r in range(10): rng.permutation(k)
                rs = np.random.default_rng(2000 + seed)       # SC: shuffled TRAIN eyes
                for s in train:
                    if len(s['t']) >= k:
                        for r in range(5):
                            P = rs.permutation(k); rec(det.name, seed, k, 'SC', f"{s['pid']}{s['eye']}|{r}", f(s['t'][:k], s['Y'][:k][P]))
            print(f'B1 {det.name} seed {seed} {time.time() - t0:.0f}s', flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'scores.csv.gz'), index=False)
    # ---- B3: untrained detectors on all eligible eyes ----
    rows = []
    for cls in (D.OLSMD, D.MDRate, D.PLR3, D.PoPLRWithin):
        det = make(cls, 0); det.fit(train, val)
        for s in allE:
            if s['label'] is None: continue
            for k in KS:
                rows.append(dict(detector=det.name, k=k, unit=s['pid'] + s['eye'], split=s['split'], label=s['label'],
                                 flag=int(det.flag(s['t'][:k], s['Y'][:k]))))
        print(f'B3 {det.name} {time.time() - t0:.0f}s', flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'b3_all_eyes.csv.gz'), index=False)
    # ---- B4: time-label sensitivity on Artes ----
    rows = []; stable_donors = {k: [s['t'][:k] for s in test if s['label'] == 0 and len(s['t']) >= k] for k in KS}
    for cls in (D.OLSMD, D.MDRate, D.PLR3, D.EventAnalysis):
        det = cls(); det.fit(train, val); rng = np.random.default_rng(3000)
        for k in KS:
            for a in A:
                for i in range(0, 12 - k + 1):
                    Y = a['sens'][i:i + k][:, keep]
                    rows.append(dict(detector=det.name, k=k, variant='annual', unit=f"{a['pid']}|{i}", flag=int(det.flag(np.arange(k, dtype=float), Y))))
                    for d in range(10):
                        tt = stable_donors[k][rng.integers(len(stable_donors[k]))]
                        rows.append(dict(detector=det.name, k=k, variant='stable_donor', unit=f"{a['pid']}|{i}|{d}", flag=int(det.flag(tt, Y))))
        print(f'B4 {det.name} {time.time() - t0:.0f}s', flush=True)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, 'b4_timelabels.csv.gz'), index=False)
    json.dump(dict(runtime_s=time.time() - t0), open(os.path.join(OUT, 'run_meta.json'), 'w'))

if __name__ == '__main__':
    main()
