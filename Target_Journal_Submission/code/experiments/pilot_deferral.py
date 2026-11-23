"""PILOT for risk-controlled deferral (validation split only, halves by patient: calibration / evaluation)."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np, lightgbm as lgb
from scipy import stats
from src.data.uwhvf import load_series, patient_split
from src.models.deferral import *
rng = np.random.default_rng(0)
S = load_series(); sp = patient_split(S)
train = [s for s in S if sp[s['pid']] == 'train' and len(s['ages']) >= 4]
val = [s for s in S if sp[s['pid']] == 'val' and len(s['ages']) >= 4]
half = lambda p: int(hashlib.sha256(('half' + p).encode()).hexdigest()[:4], 16) % 2
cal = [s for s in val if half(s['pid']) == 0]; evl = [s for s in val if half(s['pid']) == 1]

def build_training(series, n_aug=3):
    X, y = [], []
    for s in series:
        t = s['ages'] - s['ages'][0]; n = len(t)
        Tf, _ = first_detection(t, s['td'], np.arange(n))
        for a in range(n_aug):
            keep = [0, 1]
            for j in range(2, n):
                if a > 0 and keep[-1] == j - 1 and rng.random() < 0.3 and j < n - 1:
                    continue
                keep.append(j)
            keep = np.array(keep)
            for m in range(2, len(keep)):
                sub = keep[:m]; j = sub[-1]
                if j + 2 > n - 1: break
                f = features(t[sub], s['sens'][sub], s['td'][sub], s['ages'][0])
                if f[-1] > 0.5: break
                X.append(f); y.append(float(Tf is not None and Tf <= t[j + 2] + 1e-9))
    return np.array(X), np.array(y)
X, y = build_training(train); print('train rows', X.shape, 'pos rate', y.mean())
model = lgb.LGBMClassifier(n_estimators=300, learning_rate=0.03, num_leaves=15, min_child_samples=40, subsample=0.8,
                           subsample_freq=1, colsample_bytree=0.8, verbose=-1, random_state=0).fit(X, y)

def run(series, policy):
    outs = [evaluate(s, simulate(s, policy)) for s in series]
    tests_full = sum(o['n_full'] for o in outs); tests = sum(o['n_perf'] for o in outs)
    ev = [o for o in outs if o['event']]
    return dict(saved=1 - tests / tests_full, n_event=len(ev), delayed=np.mean([o['delay'] > 1e-9 for o in ev]),
                mean_delay=np.mean([o['delay'] for o in ev]), missed=np.mean([o['missed'] for o in ev]),
                false_flag=np.mean([o['flag_pol'] for o in outs if not o['event']])), ev

risk_policy = lambda lam: (lambda f, s, j: model.predict_proba(f[None])[0, 1] < lam)
res = {'full': run(evl, lambda f, s, j: False)[0], 'skip_alternate': run(evl, lambda f, s, j: True)[0],
       'severity_md>-6': run(evl, lambda f, s, j: f[2] > -6)[0], 'slope_rule': run(evl, lambda f, s, j: f[5] > -0.3)[0]}
for k, v in res.items(): print(k, {a: round(b, 3) for a, b in v.items()})
# Learn-then-Test calibration on cal half: risk = P(delayed | event eye), fixed-sequence from small lambda
grid = np.round(np.linspace(0.0, 0.6, 61), 3)
for eps in (0.05, 0.10, 0.20):
    delta = 0.1; lam_hat = 0.0
    for lam in grid[1:]:
        _, ev = run(cal, risk_policy(lam)); n = len(ev); k = sum(o['delay'] > 1e-9 for o in ev)
        p = stats.binom.cdf(k, n, eps)               # H0: risk > eps ; exact binomial p-value
        if p <= delta: lam_hat = lam
        else: break
    r, _ = run(evl, risk_policy(lam_hat))
    res[f'ours_eps{eps}'] = dict(lam=lam_hat, **r); print(f'ours eps={eps} lam={lam_hat}', {a: round(b, 3) for a, b in r.items()})
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'pilot_deferral.json'), 'w'), indent=1, default=float)
