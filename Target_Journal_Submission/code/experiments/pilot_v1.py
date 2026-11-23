"""PILOT v1 (validation split only): population-calibrated null from shuffled series of TRAIN eyes,
stratified by series length k and baseline mean sensitivity tertile. Compares FPR on shuffled VAL series and
positive rate on real VAL series at alpha = 0.05."""
import sys, os, json
sys.path.insert(0, os.path.dirname(__file__)); sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np, torch
from pilot_v0 import S, sp, keep, series_tensor, stat_md, stat_poplr, train_ordernet, perm_pvalue
rng = np.random.default_rng(5)
train = [s for s in S if sp[s['pid']] == 'train' and len(s['ages']) >= 3]
val = [s for s in S if sp[s['pid']] == 'val']
net = train_ordernet(train, epochs=10); net.eval()
stats = {'md': stat_md, 'poplr': stat_poplr, 'learned': lambda Y, t: net(Y, t)}
def level_bin(Y): 
    m = Y.mean().item(); return 0 if m < 20 else (1 if m < 26 else 2)
res = {}
for k in (3, 4, 5, 6):
    # calibration: each train eye with >=k tests, first k tests, 20 random shuffles
    cal = {m: {0: [], 1: [], 2: []} for m in stats}
    for s in [s for s in train if len(s['ages']) >= k]:
        Y, t = series_tensor(s, k); b = level_bin(Y)
        P = torch.stack([torch.tensor(rng.permutation(k)) for _ in range(20)])
        with torch.no_grad():
            for m, f in stats.items(): cal[m][b] += list(np.asarray(f(Y[P], t.expand(20, k))))
    ev = [s for s in val if len(s['ages']) >= k]
    out = {m: {'real': [], 'null': [], 'within': []} for m in stats}
    for s in ev:
        Y, t = series_tensor(s, k); b = level_bin(Y)
        pn = torch.tensor(rng.permutation(k))
        with torch.no_grad():
            for m, f in stats.items():
                c = np.asarray(cal[m][b])
                sr = float(f(Y[None], t[None])[0]); sn = float(f(Y[pn][None], t[None])[0])
                out[m]['real'].append((1 + (c >= sr).sum()) / (len(c) + 1))
                out[m]['null'].append((1 + (c >= sn).sum()) / (len(c) + 1))
                if k <= 6: out[m]['within'].append(perm_pvalue(f, Y, t, 999, rng))
    res[k] = {m: {kk: float(np.mean(np.array(v) <= 0.05)) for kk, v in d.items() if v} for m, d in out.items()}
    res[k]['n'] = len(ev); print(k, json.dumps(res[k]), flush=True)
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'pilot_v1.json'), 'w'), indent=1)
