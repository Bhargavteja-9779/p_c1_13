"""PILOT v2 (validation only): early detection at visit k vs a future reference standard from the full series.
Reference progressor: MD slope over ALL tests < -0.3 dB/yr with one-sided p < 0.01 (eyes with >= 8 tests).
Reference stable: MD slope over all tests >= 0 dB/yr... (p > 0.5). Others excluded (uncertain)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np, torch
from pilot_v0 import S, sp, keep, series_tensor, stat_md, stat_poplr, perm_pvalue
from src.models.deferral import ols, md_series
rng = np.random.default_rng(7)
train = [s for s in S if sp[s['pid']] == 'train' and len(s['ages']) >= 3]
val = [s for s in S if sp[s['pid']] == 'val' and len(s['ages']) >= 8]
def ref(s):
    b, p, _ = ols(s['ages'] - s['ages'][0], md_series(s['td']))
    return 1 if (b < -0.3 and p < 0.01) else (0 if p > 0.5 else -1)
labs = np.array([ref(s) for s in val]); print('val eyes', len(val), 'prog', (labs == 1).sum(), 'stable', (labs == 0).sum())
def lvl(Y):
    m = Y.mean().item(); return 0 if m < 20 else (1 if m < 26 else 2)
def detrend_shuffle(Y, t, P):
    # Freedman-Lane style: remove the eye's own pointwise linear trend, then permute residuals (keeps level, noise)
    tc = t - t.mean(); b = (tc[:, None] * (Y - Y.mean(0))).sum(0) / (tc ** 2).sum()
    R = Y - tc[:, None] * b[None]
    return R[P]
stats = {'md': stat_md, 'poplr': stat_poplr}
res = {}
for k in (3, 4, 5):
    cal = {(m, v): {0: [], 1: [], 2: []} for m in stats for v in ('shuf', 'detr')}
    for s in [s for s in train if len(s['ages']) >= k]:
        Y, t = series_tensor(s, k); b = lvl(Y)
        P = torch.stack([torch.tensor(rng.permutation(k)) for _ in range(20)])
        Yd = torch.stack([detrend_shuffle(Y, t, p) for p in P])
        with torch.no_grad():
            for m, f in stats.items():
                cal[(m, 'shuf')][b] += list(np.asarray(f(Y[P], t.expand(20, k))))
                cal[(m, 'detr')][b] += list(np.asarray(f(Yd, t.expand(20, k))))
    out = {}
    for s, lab in zip(val, labs):
        if lab < 0: continue
        Y, t = series_tensor(s, k); b = lvl(Y)
        for m, f in stats.items():
            sr = float(f(Y[None], t[None])[0])
            for v in ('shuf', 'detr'):
                c = np.asarray(cal[(m, v)][b]); out.setdefault(f'{m}_pop_{v}', []).append(((1 + (c >= sr).sum()) / (len(c) + 1), lab))
            out.setdefault(f'{m}_within', []).append((perm_pvalue(f, Y, t, 999, rng), lab))
    res[k] = {}
    for name, v in out.items():
        p = np.array([a for a, _ in v]); l = np.array([b for _, b in v])
        res[k][name] = dict(sens=float((p[l == 1] <= 0.05).mean()), spec=float((p[l == 0] > 0.05).mean()))
    print(k, json.dumps(res[k]), flush=True)
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'pilot_v2.json'), 'w'), indent=1)
