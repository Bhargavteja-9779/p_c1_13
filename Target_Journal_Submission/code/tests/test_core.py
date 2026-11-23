import sys, os, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from src.models.conformal_vf import stat_md, stat_poplr, pvalue_within, ConformalCalibrator, _ols
from src.statistics.tests import holm, bootstrap_ci

def test_ols_slope_exact():
    t = np.array([0, 1, 2, 3.]); Y = np.stack([30 - 2 * t, 25 - 1 * t], 1) + np.array([[0, 0], [0.1, -0.1], [-0.1, 0.1], [0, 0]])
    b, _ = _ols(t, Y); assert np.allclose(b, [-2, -1], atol=0.1)

def test_within_permutation_floor_k3():
    rng = np.random.default_rng(0); t = np.array([0, 1, 2.]); Y = np.array([[30.] * 52, [25.] * 52, [20.] * 52]) + rng.normal(0, .1, (3, 52))
    p = pvalue_within(stat_poplr, t, Y, rng); assert abs(p - 1 / 6) < 1e-9     # minimum attainable p with 3 tests

def test_conformal_valid_under_null():
    rng = np.random.default_rng(1); series = []
    for _ in range(400):
        t = np.sort(rng.uniform(0, 5, 4)); Y = rng.normal(25, 2, (1, 52)) + rng.normal(0, 1.5, (4, 52)); series.append((t, Y))
    cal = ConformalCalibrator(stat_md, null='shuffle', n_null=20, seed=0).fit(series[:300])
    ps = np.array([cal.pvalue(t, Y) for t, Y in series[300:]]); assert abs((ps <= 0.05).mean() - 0.05) < 0.05

def test_holm():
    assert np.allclose(holm([0.01, 0.04, 0.03]), [0.03, 0.06, 0.06])

def test_bootstrap_ci_contains_mean():
    x = np.arange(100.); m, lo, hi = bootstrap_ci(x, n_boot=500); assert lo < m < hi
