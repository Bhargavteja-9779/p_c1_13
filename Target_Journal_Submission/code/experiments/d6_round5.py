"""D6 round 5 (VALIDATION only). Compare null constructions, strata and statistics.
Outputs: results/d6_round5.json"""
import sys, os, json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
import numpy as np
from src.data.uwhvf import load_series, patient_split, blind_spot_mask
from src.data.artes_retest import load_artes
from src.models.conformal_vf import *
from src.models.deferral import ols, md_series
KEEP = ~blind_spot_mask()
S = load_series(); sp = patient_split(S)
def tv(s, k): return s['ages'][:k] - s['ages'][0], s['sens'][:k][:, KEEP]
train = [s for s in S if sp[s['pid']] == 'train']; val = [s for s in S if sp[s['pid']] == 'val']
# regions: superior/inferior hemifield x central/peripheral (approximation, documented)
rows = [4, 6, 8, 9, 9, 8, 6, 4]; starts = [3, 2, 1, 0, 0, 1, 2, 3]; pos = []
for r, (n, c0) in enumerate(zip(rows, starts)):
    for c in range(c0, c0 + n): pos.append((r, c))
pos = np.array(pos)[KEEP]
sup = pos[:, 0] <= 3; cen = (np.abs(pos[:, 0] - 3.5) <= 1.5) & (np.abs(pos[:, 1] - 4) <= 2)
REG = [np.where(sup & cen)[0], np.where(sup & ~cen)[0], np.where(~sup & cen)[0], np.where(~sup & ~cen)[0]]
# heteroscedastic weights: inverse residual variance by sensitivity level, estimated on TRAIN detrended residuals
lv, rv = [], []
for s in train:
    if len(s['ages']) < 4: continue
    t, Y = tv(s, len(s['ages'])); b, _ = __import__('src.models.conformal_vf', fromlist=['_ols'])._ols(t, Y)
    R = Y - Y.mean(0) - (t - t.mean())[:, None] * b
    lv.append(Y.mean(0)); rv.append((R ** 2).sum(0) / (len(t) - 2))
lv = np.concatenate(lv); rv = np.concatenate(rv); bins = np.arange(-1, 40, 2); var_by = np.array([np.median(rv[(lv >= a) & (lv < a + 2)]) if ((lv >= a) & (lv < a + 2)).sum() > 30 else np.nan for a in bins])
var_by = np.where(np.isnan(var_by), np.nanmax(var_by), var_by)
def weights(Y):
    m = Y.mean(-2); idx = np.clip(((m + 1) // 2).astype(int), 0, len(bins) - 1); return 1.0 / var_by[idx]
stat_w = lambda t, Y: stat_md(t, Y, w=np.broadcast_to(weights(Y)[..., None, :], Y.shape))
stat_reg = lambda t, Y: stat_region(t, Y, REG)
STATS = {'md': stat_md, 'md_w': stat_w, 'poplr': stat_poplr, 'region': stat_reg}
lvl3 = lambda Y: int(np.digitize(level(Y), [20, 26]))
lvl_noise = lambda Y: (int(np.digitize(level(Y), [20, 26])), int(np.digitize(noise(Y), [1.5, 2.5])))
def ref(s):
    b, p, _ = ols(s['ages'] - s['ages'][0], md_series(s['td']))
    return 1 if (b < -0.3 and p < 0.01) else (0 if p > 0.5 else -1)
A = load_artes()
res = {}
for k in (3, 4, 5):
    calset = [tv(s, k) for s in train if len(s['ages']) >= k]
    evl = [s for s in val if len(s['ages']) >= 8]; labs = np.array([ref(s) for s in evl])
    nullv = [s for s in val if len(s['ages']) >= k]
    rng = np.random.default_rng(11)
    for sname, sf in STATS.items():
        for null in ('shuffle', 'detrended'):
            for strat_name, strat in (('lvl', lvl3), ('lvl_noise', lvl_noise)):
                if null == 'shuffle' and strat_name == 'lvl_noise': continue
                cal = ConformalCalibrator(sf, null=null, n_null=20, strata=strat, seed=0).fit(calset)
                p_ref = np.array([cal.pvalue(*tv(s, k)) for s in evl])
                p_null = np.array([cal.pvalue(t, Y[rng.permutation(k)]) for t, Y in (tv(s, k) for s in nullv)])
                # Artes true null: all 12-choose-consecutive windows of length k (weekly)
                pa = [cal.pvalue(a['t'][i:i + k] * 52, a['sens'][i:i + k][:, KEEP]) for a in A for i in range(0, 12 - k + 1)]
                key = f'{sname}|{null}|{strat_name}'
                res.setdefault(str(k), {})[key] = dict(sens=float((p_ref[labs == 1] <= .05).mean()), spec=float((p_ref[labs == 0] > .05).mean()),
                    fpr_shuffled=float((p_null <= .05).mean()), fpr_artes=float((np.array(pa) <= .05).mean()))
        # within-eye permutation reference
        p_ref = np.array([pvalue_within(sf, *tv(s, k), rng) for s in evl])
        pa = [pvalue_within(sf, a['t'][i:i + k], a['sens'][i:i + k][:, KEEP], rng) for a in A for i in range(0, 12 - k + 1)]
        res[str(k)][f'{sname}|within|-'] = dict(sens=float((p_ref[labs == 1] <= .05).mean()), spec=float((p_ref[labs == 0] > .05).mean()), fpr_artes=float((np.array(pa) <= .05).mean()))
    p_ref = np.array([pvalue_ols_md(*tv(s, k)) for s in evl]); pa = [pvalue_ols_md(a['t'][i:i + k], a['sens'][i:i + k][:, KEEP]) for a in A for i in range(0, 12 - k + 1)]
    res[str(k)]['md|ols|-'] = dict(sens=float((p_ref[labs == 1] <= .05).mean()), spec=float((p_ref[labs == 0] > .05).mean()), fpr_artes=float((np.array(pa) <= .05).mean()))
    for kk, v in res[str(k)].items(): print(k, kk, {a: round(b, 3) for a, b in v.items()}, flush=True)
json.dump(res, open(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'd6_round5.json'), 'w'), indent=1)
