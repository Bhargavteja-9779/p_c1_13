"""Additional analyses requested in internal review (added AFTER the main results were seen; reported as such).
Writes ../results/extra_stats.json. Run from code/:  python scripts/extra_stats.py
1. validity under the strict literal protocol reading (upper 95% CI <= 5%) vs the rule used in the paper
2. smallest gain over D1 that could reach Holm-adjusted significance with the observed number of progressors
3. approximate cumulative false-alarm rate over repeated looks (k = 3..6) on Artes series
4. bootstrap CI for the shuffle-audit Spearman rho (resampling detector-k cells; does not reflect patient-level noise)
5. GRAPE agreement with the secondary PLR2 / PLR3 labels
6. flag rate on the real (unshuffled) test order in UWHVF test eyes, for comparison with the shuffle audit"""
import os, json, sys
import numpy as np, pandas as pd
from scipy import stats
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RES = os.path.join(ROOT, 'results')

def main():
    M = pd.DataFrame(json.load(open(os.path.join(RES, 'metrics.json'))))
    p = os.path.join(RES, 'raw_results.csv')
    raw = pd.read_csv(p if os.path.exists(p) else p + '.gz', dtype={'unit': str, 'extra': str}, low_memory=False)
    out = {}
    M['code'] = M.detector.str.split().str[0]
    M['valid_paper'] = (M.fpr_true_null_lo <= 0.05) & (M.fpr_true_null_hi <= 0.10)
    M['valid_strict'] = M.fpr_true_null_hi <= 0.05
    out['strict_valid_cells'] = [f"{r.code}@{r.k}" for _, r in M[M.valid_strict].iterrows()]
    out['paper_valid_cells'] = [f"{r.code}@{r.k}" for _, r in M[M.valid_paper].iterrows()]
    out['D1_fpr_hi_by_k'] = {int(r.k): float(r.fpr_true_null_hi) for _, r in M[M.code == 'D1'].iterrows()}
    # 2. minimal number of one-way discordant eyes (b, c=0) giving exact two-sided McNemar p below 0.05/9 (Holm, smallest p)
    n_prog = int(M[M.code == 'D1'].sens_n.iloc[0]); m = 9
    b = next(b for b in range(1, n_prog + 1) if min(1.0, 2 * 0.5 ** b) < 0.05 / m)
    out['min_significant_gain'] = dict(n_progressors=n_prog, discordant_eyes=b, gain=b / n_prog, comparisons=m)
    # 3. cumulative false alarms: same patient, window start 0, same draw index d, any flag over k = 3..6
    e2 = raw[raw['eval'] == 'E2'].copy()
    parts = e2.unit.str.split('|', expand=True); e2['pid'] = parts[0]; e2['start'] = parts[1].astype(int); e2['draw'] = parts[2].astype(int)
    e2 = e2[e2.start == 0]
    cum = {}
    for det, g in e2.groupby('detector'):
        per_seed = g.groupby(['seed', 'pid', 'draw']).flag.max().groupby('seed').mean()
        per_k = g.groupby('k').flag.mean().to_dict()
        cum[det.split()[0]] = dict(any_flag_k3_to_6=float(per_seed.mean()), per_look_mean=float(np.mean(list(per_k.values()))))
    out['cumulative_false_alarm_artes_start0'] = cum
    # 4. rho CI by resampling cells
    c = M.dropna(subset=['fpr_true_null', 'fpr_shuffle']); rng = np.random.default_rng(0); rs = []
    for _ in range(2000):
        i = rng.integers(0, len(c), len(c)); rs.append(stats.spearmanr(c.fpr_shuffle.values[i], c.fpr_true_null.values[i]).statistic)
    out['rho_cell_bootstrap_ci'] = [float(np.nanquantile(rs, .025)), float(np.nanquantile(rs, .975))]
    # 5. GRAPE secondary labels
    e4 = raw[raw['eval'] == 'E4'].copy()
    for lab in ('PLR2', 'PLR3'):
        e4[lab] = e4.extra.str.extract(lab + r'=(\d)').astype(float)
    g5 = {}
    for (det, k), g in e4.groupby(['detector', 'k']):
        u = g.groupby('unit').agg(flag=('flag', 'mean'), PLR2=('PLR2', 'first'), PLR3=('PLR3', 'first'))
        g5[f"{det.split()[0]}@{int(k)}"] = {lab: dict(sens=float(u[u[lab] == 1].flag.mean()), n_pos=int((u[lab] == 1).sum()),
                                                    spec=float(1 - u[u[lab] == 0].flag.mean()), n_neg=int((u[lab] == 0).sum())) for lab in ('PLR2', 'PLR3')}
    out['grape_secondary_labels'] = g5
    # 6. real-order flag rate among UWHVF test eyes is not stored in raw results; E1 holds only eyes with >= 8 tests.
    e1 = raw[raw['eval'] == 'E1']
    out['real_order_flag_rate_E1_eyes'] = {f"{d.split()[0]}@{int(k)}": float(g.groupby('unit').flag.mean().mean())
                                           for (d, k), g in e1.groupby(['detector', 'k'])}
    json.dump(out, open(os.path.join(RES, 'extra_stats.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('grape_secondary_labels', 'real_order_flag_rate_E1_eyes')}, indent=1))

if __name__ == '__main__':
    main()
