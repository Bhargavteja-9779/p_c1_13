"""Statistical tools: bootstrap CIs, paired tests, effect sizes, Holm correction."""
import numpy as np
from scipy import stats

def bootstrap_ci(x, func=np.mean, n_boot=10000, alpha=0.05, seed=0):
    x = np.asarray(x); rng = np.random.default_rng(seed)
    idx = rng.integers(0, len(x), size=(n_boot, len(x)))
    b = np.array([func(x[i]) for i in idx])
    return float(func(x)), float(np.quantile(b, alpha / 2)), float(np.quantile(b, 1 - alpha / 2))

def paired_bootstrap_diff(a, b, n_boot=10000, alpha=0.05, seed=0):
    """CI of mean(a-b) over paired units."""
    return bootstrap_ci(np.asarray(a) - np.asarray(b), np.mean, n_boot, alpha, seed)

def wilcoxon(a, b):
    d = np.asarray(a) - np.asarray(b)
    if np.allclose(d, 0):
        return 1.0
    return float(stats.wilcoxon(a, b, zero_method="wilcox").pvalue)

def cliffs_delta(a, b):
    a = np.asarray(a); b = np.asarray(b)
    gt = (a[:, None] > b[None, :]).sum(); lt = (a[:, None] < b[None, :]).sum()
    return float((gt - lt) / (len(a) * len(b)))

def paired_cohens_d(a, b):
    d = np.asarray(a) - np.asarray(b); sd = d.std(ddof=1)
    return float(d.mean() / sd) if sd > 0 else float("inf") * np.sign(d.mean())

def holm(pvals):
    p = np.asarray(pvals, float); m = len(p); order = np.argsort(p); adj = np.empty(m); running = 0.0
    for k, i in enumerate(order):
        running = max(running, (m - k) * p[i]); adj[i] = min(1.0, running)
    return adj

def mcnemar(y, pa, pb):
    """Exact McNemar on paired binary correctness."""
    ca = pa == y; cb = pb == y
    b_ = int((ca & ~cb).sum()); c_ = int((~ca & cb).sum())
    n = b_ + c_
    if n == 0:
        return 1.0
    return float(stats.binomtest(min(b_, c_), n, 0.5).pvalue)
