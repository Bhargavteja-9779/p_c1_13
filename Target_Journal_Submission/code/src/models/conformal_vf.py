"""Clinic-calibrated (conformal) progression tests for visual-field series.

A series = (t: k test times in years, Y: k x L sensitivities in dB, blind spots removed).
A trend statistic S(t, Y) is larger for stronger deterioration. Under H0 (no progression) an eye's tests are
assumed exchangeable over time. We compare S on the eye's true order with a calibration pool of S values computed
on (detrended-)shuffled series of OTHER patients that have the same number of tests and fall in the same stratum
(Mondrian conformal p-value). Within-eye permutation (PoPLR-style) and OLS p-values are implemented for comparison.
"""
import itertools
import numpy as np
from scipy import stats

# ---------------------------------------------------------------- statistics (vectorised over leading axes)
def _ols(t, Y):
    """t: (..., k); Y: (..., k, L). Returns slope b and t-statistic z, each (..., L)."""
    tc = t - t.mean(-1, keepdims=True)
    sxx = np.maximum((tc ** 2).sum(-1, keepdims=True), 1e-9)
    Yc = Y - Y.mean(-2, keepdims=True)
    b = (tc[..., None] * Yc).sum(-2) / sxx
    k = Y.shape[-2]
    res = Yc - tc[..., None] * b[..., None, :]
    s2 = (res ** 2).sum(-2) / max(k - 2, 1)
    se = np.sqrt(s2 / sxx + 1e-6)
    return b, b / se

def stat_md(t, Y, w=None):
    """Negative t-statistic of the slope of (weighted) mean sensitivity. Larger = worse."""
    if w is None:
        m = Y.mean(-1, keepdims=True)
    else:
        m = (Y * w).sum(-1, keepdims=True) / w.sum(-1, keepdims=True)
    return -_ols(t, m)[1][..., 0]

def stat_poplr(t, Y):
    """PoPLR combined statistic: -sum log one-sided pointwise p (O'Leary et al. 2012)."""
    k = Y.shape[-2]
    _, z = _ols(t, Y)
    p = stats.t.cdf(np.clip(z, -50, 50), df=max(k - 2, 1))
    return -np.log(np.clip(p, 1e-12, 1)).sum(-1)

def stat_region(t, Y, regions):
    """Max over regions of the negative slope t-statistic of the regional mean (cluster-type statistic)."""
    out = [stat_md(t, Y[..., r]) for r in regions]
    return np.max(np.stack(out, -1), -1)

# ---------------------------------------------------------------- order-invariant stratifiers
def level(Y):
    return Y.mean((-2, -1))

def noise(Y):
    """Order-invariant noise summary: median over points of the across-test SD (includes any trend)."""
    return np.median(Y.std(-2, ddof=1), -1)

# ---------------------------------------------------------------- null series
def shuffle(Y, rng, n):
    k = Y.shape[0]
    P = np.stack([rng.permutation(k) for _ in range(n)])
    return Y[P]

def detrended_shuffle(t, Y, rng, n):
    """Freedman-Lane-type null: remove the eye's own pointwise OLS trend (keep its mean), then permute residuals."""
    tc = t - t.mean()
    b, _ = _ols(t, Y)
    R = Y - tc[:, None] * b[None, :]
    return shuffle(R, rng, n)

# ---------------------------------------------------------------- p-values
def pvalue_ols_md(t, Y):
    k = len(t)
    return float(stats.t.cdf(-stat_md(t, Y), df=max(k - 2, 1)))

def pvalue_within(statfn, t, Y, rng, n_rand=999):
    k = len(t)
    if k <= 7:
        P = np.array(list(itertools.permutations(range(k))))
    else:
        P = np.vstack([np.arange(k)] + [rng.permutation(k) for _ in range(n_rand)])
    s = statfn(np.broadcast_to(t, (len(P), k)), Y[P])
    return float((s >= s[0] - 1e-12).mean())

class ConformalCalibrator:
    """Pool of null statistic values per (k, stratum). strata: function Y -> hashable bin (order-invariant)."""
    def __init__(self, statfn, null='detrended', n_null=20, strata=None, seed=0):
        self.statfn, self.null, self.n_null, self.strata = statfn, null, n_null, strata
        self.rng = np.random.default_rng(seed); self.pool = {}

    def _bin(self, Y):
        return self.strata(Y) if self.strata is not None else 0

    def fit(self, series_list):
        """series_list: iterable of (t, Y) with exactly k tests (any k; pooled by k)."""
        for t, Y in series_list:
            k = len(t)
            Z = detrended_shuffle(t, Y, self.rng, self.n_null) if self.null == 'detrended' else shuffle(Y, self.rng, self.n_null)
            s = self.statfn(np.broadcast_to(t, (self.n_null, k)), Z)
            self.pool.setdefault((k, self._bin(Y)), []).extend(np.asarray(s).tolist())
        self.pool = {key: np.sort(np.asarray(v)) for key, v in self.pool.items()}
        return self

    def pvalue(self, t, Y):
        k = len(t); key = (k, self._bin(Y))
        c = self.pool.get(key)
        if c is None or len(c) < 50:
            c = np.sort(np.concatenate([v for (kk, _), v in self.pool.items() if kk == k]))
        s = float(self.statfn(t[None], Y[None])[0])
        n_ge = len(c) - np.searchsorted(c, s - 1e-12, side='left')
        return (1 + n_ge) / (len(c) + 1)
