"""Core logic for retrospective VF-test deferral: detection rules, history features, policy simulation."""
import numpy as np
from scipy import stats

KEEP = np.ones(54, bool); KEEP[[25, 34]] = False

def md_series(td):
    """Unweighted mean total deviation over the 52 non-blind-spot points (MD proxy)."""
    return td[:, KEEP].mean(1)

def ols(t, y):
    t = np.asarray(t, float); y = np.asarray(y, float); n = len(t)
    tc = t - t.mean(); sxx = (tc ** 2).sum()
    if n < 3 or sxx <= 0:
        return 0.0, 1.0, 0.0
    b = (tc * (y - y.mean())).sum() / sxx
    res = y - y.mean() - b * tc
    se = np.sqrt((res ** 2).sum() / (n - 2) / sxx) + 1e-9
    p = stats.t.cdf(b / se, df=n - 2)   # one-sided p for negative slope
    return b, p, b / se

def detect_md(t, td, min_tests=5, alpha=0.05):
    """Primary detection rule: MD slope < 0 with one-sided p < alpha using all tests so far, >= min_tests tests."""
    if len(t) < min_tests:
        return False
    b, p, _ = ols(t, md_series(td))
    return (b < 0) and (p < alpha)

def first_detection(t, td, idx, rule=detect_md):
    """Time of first detection when only tests in idx (sorted) are performed. Returns (time or None, position)."""
    for m in range(1, len(idx) + 1):
        sub = idx[:m]
        if rule(t[sub], td[sub]):
            return t[sub[-1]], sub[-1]
    return None, None

def features(t, sens, td, age0):
    """History features after the latest performed test (all arrays restricted to performed tests)."""
    md = md_series(td); n = len(t)
    b, p, z = ols(t, md) if n >= 3 else (0.0, 1.0, 0.0)
    # pointwise slopes
    if n >= 3:
        tc = t - t.mean(); sxx = (tc ** 2).sum()
        B = (tc[:, None] * (td[:, KEEP] - td[:, KEEP].mean(0))).sum(0) / sxx
        R = td[:, KEEP] - td[:, KEEP].mean(0) - tc[:, None] * B
        SE = np.sqrt((R ** 2).sum(0) / (n - 2) / sxx) + 1e-6
        P = stats.t.cdf(B / SE, df=n - 2)
        n_sig = (P < 0.01).sum(); n_fast = (B < -1).sum(); poplr = -np.log(np.clip(P, 1e-12, 1)).sum()
    else:
        n_sig = n_fast = 0; poplr = 52 * 1.0
    gap = t[-1] - t[-2] if n >= 2 else 0.0
    return np.array([n, t[-1] - t[0], md[-1], md.mean(), md[-1] - md[0], b, z, p, n_sig, n_fast, poplr,
                     (td[-1, KEEP] < -10).sum(), age0 + t[-1], gap, float(detect_md(t, td))])

FEATURE_NAMES = ['n_tests', 'followup_yrs', 'md_last', 'md_mean', 'md_change', 'md_slope', 'md_slope_z', 'md_slope_p',
                 'n_pts_p01', 'n_pts_fast', 'poplr_S', 'n_pts_deep', 'age', 'last_gap', 'flag_now']

def simulate(s, policy, max_consec_skip=1, n_baseline=2):
    """Run a deferral policy on an observed series. policy(feature_vector, s, j) -> True to defer the next observed test.
    Returns performed indices list."""
    t = s['ages'] - s['ages'][0]; n = len(t)
    perf = list(range(min(n_baseline, n))); j = perf[-1]; consec = 0
    while j < n - 1:
        sub = np.array(perf)
        defer = False
        if len(perf) >= n_baseline and consec < max_consec_skip and j + 2 <= n - 1:
            f = features(t[sub], s['sens'][sub], s['td'][sub], s['ages'][0])
            if f[-1] < 0.5:            # never defer once progression is already flagged
                defer = policy(f, s, j)
        if defer:
            consec += 1; j += 2
        else:
            consec = 0; j += 1
        perf.append(j)
    return np.array(perf)

def evaluate(s, perf, rule=detect_md):
    """Outcome of a schedule versus the full schedule."""
    t = s['ages'] - s['ages'][0]; full = np.arange(len(t))
    T_full, _ = first_detection(t, s['td'], full, rule)
    T_pol, _ = first_detection(t, s['td'], perf, rule)
    out = dict(n_full=len(t), n_perf=len(perf), event=T_full is not None, flag_pol=T_pol is not None)
    if T_full is not None:
        if T_pol is None:
            out['delay'] = t[-1] - T_full + 1.0   # censored: not detected by end of follow-up (+1 yr penalty)
            out['missed'] = True
        else:
            out['delay'] = max(0.0, T_pol - T_full); out['missed'] = False
    return out
