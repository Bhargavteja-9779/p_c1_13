import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import numpy as np
exec(open(os.path.join(os.path.dirname(__file__), 'pilot_deferral.py')).read().split("risk_policy = ")[0])
risk_policy = lambda lam: (lambda f, s, j: model.predict_proba(f[None])[0, 1] < lam)
for lam in (0.01, 0.02, 0.04, 0.06, 0.1, 0.15, 0.25, 0.4, 1.0):
    r, _ = run(evl, risk_policy(lam)); print('risk', lam, {a: round(float(b), 3) for a, b in r.items()})
for thr in (-2, -4, -6, -10, -15):
    r, _ = run(evl, lambda f, s, j: f[2] > thr); print('sev', thr, {a: round(float(b), 3) for a, b in r.items()})
