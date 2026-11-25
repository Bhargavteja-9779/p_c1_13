import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'experiments'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from scipy import stats
from amendment_c import tab_features_batch, fit_var_prior
from src.models.detectors import tab_features

def test_batch_features_match_scalar():
    rng = np.random.default_rng(0)
    for k in (3, 5, 8):
        T = np.sort(rng.uniform(0, 6, (5, k)), 1); T -= T[:, :1]; Y = rng.normal(25, 3, (5, k, 52))
        assert np.abs(tab_features_batch(T, Y) - np.stack([tab_features(T[i], Y[i]) for i in range(5)])).max() < 1e-9

def test_var_prior_recovers_truth():
    n = 20000; d0, s0, df = 6.0, 1.5, 4.0
    sig2 = s0 / (stats.chi2.rvs(d0, size=n, random_state=2) / d0)
    s2 = sig2 * stats.chi2.rvs(df, size=n, random_state=1) / df
    e_d0, e_s0 = fit_var_prior(s2, np.full(n, df))
    assert abs(e_d0 - d0) < 1.0 and abs(e_s0 - s0) < 0.1
