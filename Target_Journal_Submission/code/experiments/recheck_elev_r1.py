"""Prompt-2 elevation round 1 (VALIDATION ONLY; never touches the locked test split or Artes/GRAPE).
H1 mechanism (reference-stable eyes improve), H2 null-calibrated ML, H3 change-only features.
Output: ../results/recheck_elev_r1.json"""
import sys, os, json, hashlib
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
import numpy as np
from scipy import stats
from src.data.uwhvf import load_series, patient_split, blind_spot_mask
from src.models import detectors as D
from src.models.deferral import ols, md_series
from run_all import reference

KS = (3, 4, 5, 6); N_SHUF = 5; SEEDS = [0, 1, 2]
keep = ~blind_spot_mask(); S = load_series(); sp = patient_split(S)
def to_d(s):
    lab = reference(s) if len(s['ages']) >= 8 else None
    return dict(pid=s['pid'], eye=s['eye'], t=s['ages'] - s['ages'][0], Y=s['sens'][:, keep], label=lab, raw=s)
train = [to_d(s) for s in S if sp[s['pid']] == 'train' and len(s['ages']) >= 3]
val = [to_d(s) for s in S if sp[s['pid']] == 'val' and len(s['ages']) >= 3]
half = lambda p: int(hashlib.sha256(('valhalf' + p).encode()).hexdigest()[:4], 16) % 2
valA = [s for s in val if half(s['pid']) == 0]; valB = [s for s in val if half(s['pid']) == 1]
out = {'n_train': len(train), 'n_val': len(val), 'n_valA': len(valA), 'n_valB': len(valB)}

# ---------------- H1: slope of reference-stable / progressor eyes (train+val, full series)
def full_slope(s):
    b, p, _ = ols(s['t'], md_series(s['raw']['td'])); return b
for lab in (0, 1):
    sl = np.array([full_slope(s) for s in train + val if s['label'] == lab])
    out[f'h1_fullslope_label{lab}'] = dict(n=len(sl), mean=float(sl.mean()), median=float(np.median(sl)),
                                           share_positive=float((sl > 0).mean()))
allsl = np.array([full_slope(s) for s in train + val if len(s['t']) >= 8])
out['h1_fullslope_all_ge8'] = dict(n=len(allsl), mean=float(allsl.mean()), median=float(np.median(allsl)),
                                   share_positive=float((allsl > 0).mean()))

# first-k OLS-MD slope in reference-stable eyes vs shuffled series
rng = np.random.default_rng(7)
for k in KS:
    st = [D.md_slope(s['t'][:k], s['Y'][:k])[0] for s in val if s['label'] == 0]
    sh = [D.md_slope(s['t'][:k], s['Y'][:k][rng.permutation(k)])[0] for s in val if len(s['t']) >= k]
    out[f'h1_firstk_slope_k{k}'] = dict(stable_mean=float(np.mean(st)), shuffled_mean=float(np.mean(sh)),
                                        stable_sd=float(np.std(st)), shuffled_sd=float(np.std(sh)))

# ---------------- H2/H3 variants of D8
CHANGE_IDX = [0, 1, 4, 5, 6, 7, 8, 9, 10, 11]      # drop md[-1], md.mean(), Y.std, md range (order-invariant level/variability)
class D8Change(D.MLTabular):
    def _rows(self, data, k):
        X, y = super()._rows(data, k); return (X[:, CHANGE_IDX] if len(X) else X), y
    def score(self, t, Y): return float(self.models[len(t)].predict_proba(D.tab_features(t, Y)[CHANGE_IDX][None])[0, 1])
    def flag(self, t, Y): return self.score(t, Y) > self.thr[len(t)]
class D8(D.MLTabular):
    def score(self, t, Y): return float(self.models[len(t)].predict_proba(D.tab_features(t, Y)[None])[0, 1])

def evaluate(det, cal_set, ev_set, k, rng, lvl=True):
    """Return sens/spec on ev_set reference eyes, and shuffled-null FPR, for (a) the standard threshold and
    (b) a null-calibrated threshold from shuffles of cal_set (Mondrian by mean-sensitivity tertile)."""
    pool = {}
    for s in cal_set:
        if len(s['t']) < k: continue
        b = D.lvl3(s['Y'][:k]) if lvl else 0
        for _ in range(N_SHUF):
            pool.setdefault(b, []).append(det.score(s['t'][:k], s['Y'][:k][rng.permutation(k)]))
    pool = {b: np.sort(v) for b, v in pool.items()}
    def pval(t, Y):
        b = D.lvl3(Y) if lvl else 0; c = pool.get(b, np.sort(np.concatenate(list(pool.values()))))
        sc = det.score(t, Y); return (1 + len(c) - np.searchsorted(c, sc, side='left')) / (len(c) + 1)
    r = {}
    for nm, fl in (('std', lambda t, Y: det.flag(t, Y)), ('nullcal', lambda t, Y: pval(t, Y) < 0.05)):
        pos = [fl(s['t'][:k], s['Y'][:k]) for s in ev_set if s['label'] == 1 and len(s['t']) >= 8]
        neg = [fl(s['t'][:k], s['Y'][:k]) for s in ev_set if s['label'] == 0 and len(s['t']) >= 8]
        nul = [fl(s['t'][:k], s['Y'][:k][rng.permutation(k)]) for s in ev_set if len(s['t']) >= k for _ in range(N_SHUF)]
        r[nm] = dict(sens=float(np.mean(pos)), spec=1 - float(np.mean(neg)), fpr_shuffle=float(np.mean(nul)),
                     n_pos=len(pos), n_neg=len(neg), n_null=len(nul))
    return r

res = {}
ols_det = D.OLSMD()
for k in KS:
    pos = [ols_det.flag(s['t'][:k], s['Y'][:k]) for s in valB if s['label'] == 1 and len(s['t']) >= 8]
    nul = [ols_det.flag(s['t'][:k], s['Y'][:k][rng.permutation(k)]) for s in valB if len(s['t']) >= k for _ in range(N_SHUF)]
    res[f'D1_k{k}'] = dict(sens=float(np.mean(pos)), fpr_shuffle=float(np.mean(nul)), n_pos=len(pos))
for seed in SEEDS:
    for cls, nm in ((D8, 'D8'), (D8Change, 'D8change')):
        det = cls(seed=seed).fit(train, valA)            # model selection + std threshold on valA
        for k in KS:
            res[f'{nm}_seed{seed}_k{k}'] = evaluate(det, valA, valB, k, np.random.default_rng(100 + seed))
        print(nm, seed, 'done', flush=True)
out['variants'] = res
# feature importance (gain) of D8 seed 0
det = D8(seed=0).fit(train, valA)
names = ['k', 'span', 'md_last', 'md_mean', 'md_last_minus_first', 'md_slope', 'md_z', 'plr_frac', 'p05_frac', 'mean_neglogp',
         'worst10pct_slope', 'slope_sd', 'pointwise_sd', 'md_range']
out['d8_importance_gain'] = {k: dict(zip(names, (det.models[k].booster_.feature_importance('gain') /
                                                 det.models[k].booster_.feature_importance('gain').sum()).round(3).tolist())) for k in KS}
json.dump(out, open(os.path.join(os.path.dirname(__file__), '..', '..', 'results', 'recheck_elev_r1.json'), 'w'), indent=1)
print(json.dumps(out)[:3000])
