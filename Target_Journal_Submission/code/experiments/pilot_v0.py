"""PILOT (motivating experiment, validation split only). Compares at matched alpha (exact permutation tests):
MD-slope permutation test, PoPLR (O'Leary 2012), and a self-supervised learned order statistic.
Positive rate on real series at alpha=0.05 (one-sided) is reported; all tests are exactly level-alpha under exchangeability."""
import sys, os, itertools, json, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np, torch, torch.nn as nn
from src.data.uwhvf import load_series, blind_spot_mask, patient_split
from src.models.features import ols_features, grid_neighbors
from src.utils import set_seed
set_seed(0)
S = load_series(); keep = ~blind_spot_mask(); sp = patient_split(S)
_, A = grid_neighbors(); A = A[keep][:, keep]; A = torch.tensor(A / A.sum(1, keepdims=True), dtype=torch.float32)
L = keep.sum()

def perms_for(k, n_rand=0, rng=None):
    if n_rand == 0:
        P = np.array(list(itertools.permutations(range(k))))
    else:
        P = np.array([np.arange(k)] + [rng.permutation(k) for _ in range(n_rand)])
    return torch.tensor(P)

def series_tensor(s, k, start=0):
    Y = torch.tensor(s['sens'][start:start + k][:, keep], dtype=torch.float32)
    t = torch.tensor(s['ages'][start:start + k] - s['ages'][start], dtype=torch.float32)
    return Y, t

def stat_md(Yp, tp):
    b, tt = ols_features(Yp.mean(-1, keepdim=True), tp)
    return -tt[..., 0]

def stat_poplr(Yp, tp):
    from scipy.stats import t as tdist
    b, tt = ols_features(Yp, tp)
    k = Yp.shape[-2]
    p = tdist.cdf(tt.clamp(-50, 50).numpy(), df=max(k - 2, 1))   # one-sided p for negative slope
    return torch.tensor(-np.log(np.clip(p, 1e-12, 1)).sum(-1))

class OrderNet(nn.Module):
    def __init__(self, L, h=32, e=8):
        super().__init__()
        self.emb = nn.Parameter(torch.randn(L, e) * 0.1)
        self.mlp = nn.Sequential(nn.Linear(7 + e, h), nn.ReLU(), nn.Linear(h, h), nn.ReLU(), nn.Linear(h, 1))
    def forward(self, Yp, tp):
        b, tt = ols_features(Yp, tp)                                # (..., L)
        m = Yp.mean(-2) / 30.0                                      # order-invariant level
        nb = b @ A.T; nt = tt @ A.T
        g = ols_features(Yp.mean(-1, keepdim=True), tp)[1].expand_as(b)
        sd = Yp.std(-2) / 10.0
        x = torch.stack([b.clamp(-10, 10) / 2, tt.clamp(-20, 20) / 5, m, nb.clamp(-10, 10) / 2, nt.clamp(-20, 20) / 5, g.clamp(-20, 20) / 5, sd], -1)
        x = torch.cat([x, self.emb.expand(*x.shape[:-2], L, -1)], -1)
        return self.mlp(x).squeeze(-1).sum(-1)

def train_ordernet(train, epochs=30, M=31, seed=0):
    set_seed(seed); rng = np.random.default_rng(seed)
    net = OrderNet(L); opt = torch.optim.Adam(net.parameters(), 3e-3, weight_decay=1e-4)
    for ep in range(epochs):
        idx = rng.permutation(len(train)); tot = 0
        for i0 in range(0, len(idx), 64):
            Ys, ts = [], []
            for j in idx[i0:i0 + 64]:
                s = train[j]; n = len(s['ages']); k = rng.integers(3, min(n, 8) + 1); st = rng.integers(0, n - k + 1)
                Y, t = series_tensor(s, k, st); P = perms_for(k, M, rng)
                Ys.append((Y[P], t.expand(M + 1, k)))
            loss = 0
            for Yp, tp in Ys:
                sc = net(Yp, tp)
                loss = loss + (torch.logsumexp(sc, 0) - sc[0])
            loss = loss / len(Ys); opt.zero_grad(); loss.backward(); opt.step(); tot += loss.item()
        print(f'epoch {ep} loss {tot / (len(idx) / 64):.4f} (chance {np.log(M + 1):.3f})', flush=True)
    return net

def perm_pvalue(statfn, Y, t, n_rand, rng):
    k = Y.shape[0]
    P = perms_for(k) if k <= 6 else perms_for(k, n_rand, rng)
    with torch.no_grad():
        sc = statfn(Y[P], t.expand(len(P), k))
    return ((sc >= sc[0] - 1e-9).sum().item()) / len(P)

if __name__ == '__main__':
    train = [s for s in S if sp[s['pid']] == 'train' and len(s['ages']) >= 3]
    val = [s for s in S if sp[s['pid']] == 'val']
    t0 = time.time(); net = train_ordernet(train, epochs=int(os.environ.get('EPOCHS', 15))); print('train s', time.time() - t0)
    net.eval(); rng = np.random.default_rng(1); res = {}
    for k in (4, 5, 6, 8):
        ev = [s for s in val if len(s['ages']) >= k]
        out = {'md': [], 'poplr': [], 'learned': []}
        for s in ev:
            Y, t = series_tensor(s, k)
            out['md'].append(perm_pvalue(stat_md, Y, t, 999, rng))
            out['poplr'].append(perm_pvalue(stat_poplr, Y, t, 999, rng))
            out['learned'].append(perm_pvalue(net, Y, t, 999, rng))
        res[k] = {m: float(np.mean(np.array(v) <= 0.05)) for m, v in out.items()}
        res[k]['n'] = len(ev)
        # null check: shuffle each series once, rerun (should give ~5%)
        print(k, res[k], flush=True)
    json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'pilot_v0.json'), 'w'), indent=1)
