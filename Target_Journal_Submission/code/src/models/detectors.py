"""Ten progression detectors (protocol D1-D10). Common interface:
    det.fit(train, val)   (train/val: lists of dicts with 't' (years), 'Y' (k_full x L dB), 'label' (1/0/None))
    det.flag(t, Y) -> bool  using only the given tests (k x L)
Grid-agnostic detectors work for 24-2 (52 points) and Octopus G1 (59 points)."""
import itertools
import numpy as np
from scipy import stats
from .conformal_vf import _ols, stat_md, stat_poplr, stat_region, level, ConformalCalibrator, pvalue_within

ALPHA = 0.05

def md_slope(t, Y):
    b, z = _ols(t, Y.mean(1, keepdims=True)); return float(b[0]), float(z[0])

class OLSMD:                                   # D1
    name = 'D1 OLS-MD'
    def fit(self, train, val): return self
    def flag(self, t, Y):
        k = len(t); return stats.t.cdf(-stat_md(t, Y), df=max(k - 2, 1)) < ALPHA

class MDRate:                                  # D2
    name = 'D2 MD-rate <= -1 dB/yr'
    def fit(self, train, val): return self
    def flag(self, t, Y): return md_slope(t, Y)[0] <= -1.0

class PLR3:                                    # D3
    name = 'D3 PLR >=3 points'
    def fit(self, train, val): return self
    def flag(self, t, Y):
        k = len(t); b, z = _ols(t, Y); p = stats.t.cdf(np.clip(z, -50, 50), df=max(k - 2, 1))
        return int(((b <= -1.0) & (p < 0.01)).sum()) >= 3

class PoPLRWithin:                             # D4
    name = 'D4 PoPLR (within-eye permutation)'
    def __init__(self, seed=0): self.rng = np.random.default_rng(seed)
    def fit(self, train, val): return self
    def flag(self, t, Y): return pvalue_within(stat_poplr, t, Y, self.rng) < ALPHA

def lvl3(Y): return int(np.digitize(level(Y), [20, 26]))

class PooledShuffleMD:                         # D5
    name = 'D5 Pooled-shuffle conformal MD'
    def __init__(self, seed=0): self.seed = seed; self.cals = {}
    def fit(self, train, val, ks=(3, 4, 5, 6)):
        for k in ks:
            self.cals[k] = ConformalCalibrator(stat_md, null='shuffle', n_null=20, strata=lvl3, seed=self.seed).fit(
                [(s['t'][:k], s['Y'][:k]) for s in train if len(s['t']) >= k])
        return self
    def flag(self, t, Y): return self.cals[len(t)].pvalue(t, Y) < ALPHA

def make_regions(n_points):
    """24-2 (52 points after blind-spot removal): superior/inferior x central/peripheral. Other grids: split by index
    halves/quarters (approximate; only used for D6, which is not evaluated on GRAPE as a primary result)."""
    if n_points == 52:
        rows = [4, 6, 8, 9, 9, 8, 6, 4]; starts = [3, 2, 1, 0, 0, 1, 2, 3]; pos = []
        for r, (n, c0) in enumerate(zip(rows, starts)):
            for c in range(c0, c0 + n): pos.append((r, c))
        keep = np.ones(54, bool); keep[[25, 34]] = False; pos = np.array(pos)[keep]
        sup = pos[:, 0] <= 3; cen = (np.abs(pos[:, 0] - 3.5) <= 1.5) & (np.abs(pos[:, 1] - 4) <= 2)
        return [np.where(sup & cen)[0], np.where(sup & ~cen)[0], np.where(~sup & cen)[0], np.where(~sup & ~cen)[0]]
    return [a for a in np.array_split(np.arange(n_points), 4)]

class PooledDetrendedRegion:                   # D6
    name = 'D6 Pooled-detrended conformal region-max'
    def __init__(self, seed=0): self.seed = seed; self.cals = {}
    def fit(self, train, val, ks=(3, 4, 5, 6)):
        L = train[0]['Y'].shape[1]; self.regions = make_regions(L)
        f = lambda t, Y: stat_region(t, Y, self.regions)
        for k in ks:
            self.cals[k] = ConformalCalibrator(f, null='detrended', n_null=20, strata=lvl3, seed=self.seed).fit(
                [(s['t'][:k], s['Y'][:k]) for s in train if len(s['t']) >= k])
        return self
    def flag(self, t, Y): return self.cals[len(t)].pvalue(t, Y) < ALPHA

class EventAnalysis:                           # D7
    name = 'D7 Event analysis (GPA-like)'
    def fit(self, train, val):
        base, diff = [], []
        for s in train:
            t, Y = s['t'], s['Y']
            for i in range(len(t) - 1):
                if t[i + 1] - t[i] <= 0.5:
                    base.append(Y[i]); diff.append(Y[i + 1] - Y[i])
        base = np.concatenate(base); diff = np.concatenate(diff)
        self.edges = np.arange(0, 42, 2); self.lim = np.full(len(self.edges), np.nan)
        for j, a in enumerate(self.edges):
            m = (base >= a) & (base < a + 2)
            if m.sum() >= 200: self.lim[j] = np.quantile(diff[m], 0.05)
        ok = ~np.isnan(self.lim); self.lim = np.interp(self.edges, self.edges[ok], self.lim[ok])
        return self
    def flag(self, t, Y):
        if len(t) < 4: return False
        b = Y[:2].mean(0); idx = np.clip((b // 2).astype(int), 0, len(self.edges) - 1)
        det = (Y[2:] - b[None]) < self.lim[idx][None]
        cons = det[1:] & det[:-1]
        return bool((cons.sum(1) >= 3).any())

def tab_features(t, Y):
    k = len(t); b, z = _ols(t, Y); p = stats.t.cdf(np.clip(z, -50, 50), df=max(k - 2, 1))
    mb, mz = md_slope(t, Y); md = Y.mean(1); sb = np.sort(b)
    return np.array([k, t[-1] - t[0], md[-1], md.mean(), md[-1] - md[0], mb, mz, ((b <= -1) & (p < 0.01)).mean(),
                     (p < 0.05).mean(), -np.log(np.clip(p, 1e-12, 1)).mean(), sb[:max(1, len(sb) // 10)].mean(),
                     b.std(), Y.std(0).mean(), md.max() - md.min()])

class MLTabular:                               # D8
    name = 'D8 ML-tabular (LightGBM)'
    GRID = [dict(n_estimators=n, learning_rate=lr, num_leaves=nl) for n in (200, 400) for lr in (0.03, 0.1) for nl in (7, 15, 31)]
    def __init__(self, seed=0): self.seed = seed; self.models = {}; self.thr = {}
    def _rows(self, data, k):
        X, y = [], []
        for s in data:
            if s['label'] is None or len(s['t']) < k: continue
            X.append(tab_features(s['t'][:k], s['Y'][:k])); y.append(s['label'])
        return np.array(X), np.array(y)
    def fit(self, train, val, ks=(3, 4, 5, 6)):
        import lightgbm as lgb
        from sklearn.metrics import roc_auc_score
        for k in ks:
            Xt, yt = self._rows(train, k); Xv, yv = self._rows(val, k)
            best = None
            for cfg in self.GRID:                       # same 12-config budget as D9
                m = lgb.LGBMClassifier(**cfg, min_child_samples=10, subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                                       random_state=self.seed, verbose=-1).fit(Xt, yt)
                a = roc_auc_score(yv, m.predict_proba(Xv)[:, 1])
                if best is None or a > best[0]: best = (a, m)
            self.models[k] = best[1]
            sv = best[1].predict_proba(Xv)[:, 1]; self.thr[k] = float(np.quantile(sv[yv == 0], 0.95))
        return self
    def flag(self, t, Y):
        k = len(t); return float(self.models[k].predict_proba(tab_features(t, Y)[None])[0, 1]) > self.thr[k]

class MLSequence:                              # D9 (24-2 only)
    name = 'D9 ML-sequence (GRU)'
    GRID = [dict(h=h, lr=lr, ep=ep) for h in (16, 32, 64) for lr in (1e-3, 3e-3) for ep in (20, 40)]
    def __init__(self, seed=0): self.seed = seed; self.models = {}; self.thr = {}
    def _tensor(self, data, k):
        import torch
        X, y = [], []
        for s in data:
            if s['label'] is None or len(s['t']) < k: continue
            Y = s['Y'][:k] / 35.0; dt = np.diff(np.r_[0, s['t'][:k]])[:, None]
            X.append(np.hstack([Y, dt])); y.append(s['label'])
        return torch.tensor(np.array(X), dtype=torch.float32), torch.tensor(np.array(y), dtype=torch.float32)
    def _net(self, d, h):
        import torch.nn as nn
        class Net(nn.Module):
            def __init__(s):
                super().__init__(); s.g = nn.GRU(d, h, batch_first=True); s.o = nn.Linear(h, 1)
            def forward(s, x): return s.o(s.g(x)[1][-1]).squeeze(-1)
        return Net()
    def fit(self, train, val, ks=(3, 4, 5, 6)):
        import torch
        from sklearn.metrics import roc_auc_score
        for k in ks:
            Xt, yt = self._tensor(train, k); Xv, yv = self._tensor(val, k); best = None
            pw = ((1 - yt.mean()) / yt.mean()).detach()
            for cfg in self.GRID:
                torch.manual_seed(self.seed); net = self._net(Xt.shape[-1], cfg['h'])
                opt = torch.optim.Adam(net.parameters(), cfg['lr'], weight_decay=1e-4)
                for _ in range(cfg['ep']):
                    perm = torch.randperm(len(Xt))
                    for i in range(0, len(Xt), 64):
                        j = perm[i:i + 64]; loss = torch.nn.functional.binary_cross_entropy_with_logits(net(Xt[j]), yt[j], pos_weight=pw)
                        opt.zero_grad(); loss.backward(); opt.step()
                with torch.no_grad(): sv = net(Xv).numpy()
                a = roc_auc_score(yv.numpy(), sv)
                if best is None or a > best[0]: best = (a, net, sv)
            self.models[k] = best[1]; yvn = yv.numpy(); self.thr[k] = float(np.quantile(best[2][yvn == 0], 0.95))
        return self
    def flag(self, t, Y):
        import torch
        k = len(t); x = np.hstack([Y / 35.0, np.diff(np.r_[0, t])[:, None]])
        with torch.no_grad(): return float(self.models[k](torch.tensor(x[None], dtype=torch.float32))[0]) > self.thr[k]

class OrderNetPermutation:                     # D10 (24-2 only)
    name = 'D10 Self-supervised order net + permutation'
    def __init__(self, seed=0, epochs=15): self.seed = seed; self.epochs = epochs; self.rng = np.random.default_rng(seed)
    def fit(self, train, val):
        import torch, torch.nn as nn
        torch.manual_seed(self.seed); rng = np.random.default_rng(self.seed)
        L = train[0]['Y'].shape[1]
        class Net(nn.Module):
            def __init__(s):
                super().__init__(); s.emb = nn.Parameter(torch.randn(L, 8) * 0.1)
                s.mlp = nn.Sequential(nn.Linear(5 + 8, 32), nn.ReLU(), nn.Linear(32, 1))
            def forward(s, t, Y):
                tc = t - t.mean(-1, keepdim=True); sxx = (tc ** 2).sum(-1, keepdim=True).clamp_min(1e-6)
                Yc = Y - Y.mean(-2, keepdim=True); b = (tc.unsqueeze(-1) * Yc).sum(-2) / sxx
                res = Yc - tc.unsqueeze(-1) * b.unsqueeze(-2); k = Y.shape[-2]
                se = torch.sqrt((res ** 2).sum(-2) / max(k - 2, 1) / sxx + 1e-4); z = b / se
                g = (b.mean(-1, keepdim=True)).expand_as(b)
                x = torch.stack([b.clamp(-10, 10) / 2, z.clamp(-20, 20) / 5, Y.mean(-2) / 30, Y.std(-2) / 10, g.clamp(-10, 10) / 2], -1)
                x = torch.cat([x, s.emb.expand(*x.shape[:-1], 8)], -1)
                return s.mlp(x).squeeze(-1).sum(-1)
        self.net = Net(); opt = torch.optim.Adam(self.net.parameters(), 3e-3, weight_decay=1e-4)
        data = [s for s in train if len(s['t']) >= 3]
        for _ in range(self.epochs):
            for i0 in range(0, len(data), 64):
                loss = 0; batch = [data[j] for j in rng.permutation(len(data))[:64]]
                for s in batch:
                    n = len(s['t']); k = int(rng.integers(3, min(n, 8) + 1)); st = int(rng.integers(0, n - k + 1))
                    P = np.vstack([np.arange(k)] + [rng.permutation(k) for _ in range(31)])
                    t = torch.tensor(s['t'][st:st + k] - s['t'][st], dtype=torch.float32)
                    Y = torch.tensor(s['Y'][st:st + k], dtype=torch.float32)
                    sc = self.net(t.expand(32, k), Y[P]); loss = loss + torch.logsumexp(sc, 0) - sc[0]
                opt.zero_grad(); (loss / len(batch)).backward(); opt.step()
        self.net.eval(); return self
    def flag(self, t, Y):
        import torch
        def f(tt, YY):
            with torch.no_grad(): return self.net(torch.tensor(np.ascontiguousarray(tt), dtype=torch.float32), torch.tensor(np.ascontiguousarray(YY), dtype=torch.float32)).numpy()
        return pvalue_within(f, t, Y, self.rng) < ALPHA

ALL = [OLSMD, MDRate, PLR3, PoPLRWithin, PooledShuffleMD, PooledDetrendedRegion, EventAnalysis, MLTabular, MLSequence, OrderNetPermutation]
GRID_AGNOSTIC = {'D1 OLS-MD', 'D2 MD-rate <= -1 dB/yr', 'D3 PLR >=3 points', 'D4 PoPLR (within-eye permutation)',
                 'D5 Pooled-shuffle conformal MD', 'D7 Event analysis (GPA-like)', 'D8 ML-tabular (LightGBM)'}
STOCHASTIC = {'D4 PoPLR (within-eye permutation)', 'D5 Pooled-shuffle conformal MD', 'D6 Pooled-detrended conformal region-max',
              'D8 ML-tabular (LightGBM)', 'D9 ML-sequence (GRU)', 'D10 Self-supervised order net + permutation'}
