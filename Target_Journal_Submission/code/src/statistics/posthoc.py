"""POST-HOC analyses added after peer-review simulation (not in the pre-registered protocol; reported as post hoc).
Usage (from code/): python -m src.statistics.posthoc  -> ../results/posthoc.json, ../tables/table_S4_posthoc_*.csv
 P1 Non-overlapping reference: progression label computed only from the fields AFTER the first k (needs >= 5 later
    fields), same slope rule as the primary reference; sensitivity/specificity of the existing flags.
 P2 Cumulative false alarms: share of true no-change series (Artes window start i, time draw d) flagged at ANY of
    3, 4, 5, 6 fields (nested prefixes of the same window).
 P3 Positive predictive value at the GRAPE prevalence of the MD label (from GRAPE sens/spec) and from UWHVF
    sensitivity with true no-change false-alarm rate, at prevalence 10% and 20%.
 P4 GRAPE sensitivity of D1 by number of visits (label computed on the whole short series; overlap check).
 P5 Paired comparison of sensitivity vs D1 with the non-overlapping reference (exact McNemar, Holm within k)."""
import os, json
import numpy as np, pandas as pd
from scipy import stats
from src.data.uwhvf import load_series, patient_split
from src.data.grape import load_grape
from src.models.deferral import ols, md_series
from src.statistics.tests import holm
ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
RES = os.path.join(ROOT, 'results'); B = 2000


def boot(flags, clusters, seed=0):
    f = pd.Series(np.asarray(flags, float)).groupby(np.asarray(clusters)).agg(['sum', 'count'])
    s, n = f['sum'].to_numpy(), f['count'].to_numpy(); est = s.sum() / n.sum()
    ix = np.random.default_rng(seed).integers(0, len(f), size=(B, len(f))); bs = s[ix].sum(1) / n[ix].sum(1)
    lo, hi = np.quantile(bs, [.025, .975])
    if hi - lo < 1e-12:
        ci = stats.binomtest(int(round(s.sum())), int(n.sum())).proportion_ci(method='exact'); lo, hi = ci.low, ci.high
    return dict(est=float(est), lo=float(lo), hi=float(hi), n=int(n.sum()))


def later_label(s, k):
    t = s['ages'][k:] - s['ages'][k]
    if len(t) < 5: return None
    b, p, _ = ols(t, md_series(s['td'][k:]))
    return 1 if (b < -0.3 and p < 0.01) else (0 if p > 0.5 else None)


def main():
    raw = pd.read_csv(os.path.join(RES, 'raw_results.csv.gz'), low_memory=False)
    out = {}
    # ---- P1 / P5
    S = load_series(); sp = patient_split(S)
    test = {s['pid'] + s['eye']: s for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 8}
    e1 = raw[raw['eval'] == 'E1']
    flag = e1.groupby(['detector', 'k', 'unit'])['flag'].mean()             # seed mean per eye
    rows, tests = [], []
    for k in (3, 4, 5, 6):
        lab = {u: later_label(s, k) for u, s in test.items()}
        prog = [u for u, l in lab.items() if l == 1]; stab = [u for u, l in lab.items() if l == 0]
        base = None
        for det in sorted(raw.detector.unique(), key=lambda x: int(x.split()[0][1:])):
            f = flag.loc[det, k]
            fp = [f.get(u, np.nan) for u in prog]; fs = [f.get(u, np.nan) for u in stab]
            ok_p = [u for u, v in zip(prog, fp) if not np.isnan(v)]; ok_s = [u for u, v in zip(stab, fs) if not np.isnan(v)]
            se = boot([f[u] for u in ok_p], [u[:-1] for u in ok_p]); spc = boot([1 - f[u] for u in ok_s], [u[:-1] for u in ok_s])
            rows.append(dict(detector=det, k=k, n_prog=len(ok_p), n_stable=len(ok_s), sens=se['est'], sens_lo=se['lo'],
                             sens_hi=se['hi'], spec=spc['est'], spec_lo=spc['lo'], spec_hi=spc['hi']))
            v = f.reindex(ok_p).round().to_numpy()
            if det.startswith('D1 '): base = (ok_p, v); continue
            j = [u for u in ok_p if u in base[0]]
            a = f.reindex(j).round().to_numpy(); b = pd.Series(base[1], index=base[0]).reindex(j).to_numpy()
            b01, b10 = int(((a == 1) & (b == 0)).sum()), int(((a == 0) & (b == 1)).sum())
            p = 1.0 if b01 + b10 == 0 else float(stats.binomtest(min(b01, b10), b01 + b10).pvalue)
            tests.append(dict(detector=det, k=k, n=len(j), diff=float((a - b).mean()), only_det=b01, only_D1=b10, p=p))
    T = pd.DataFrame(tests); T['p_holm'] = np.nan
    for k, g in T.groupby('k'): T.loc[g.index, 'p_holm'] = holm(g.p.tolist())
    P1 = pd.DataFrame(rows)
    P1.to_csv(os.path.join(ROOT, 'tables', 'table_S4_posthoc_later_reference.csv'), index=False)
    T.to_csv(os.path.join(ROOT, 'tables', 'table_S5_posthoc_later_reference_tests.csv'), index=False)
    out['P1_later_reference'] = json.loads(P1.to_json(orient='records'))
    out['P5_later_reference_tests'] = json.loads(T.to_json(orient='records'))
    # ---- P2 cumulative false alarms over nested windows (start i <= 6 so that all four lengths exist)
    e2 = raw[raw['eval'] == 'E2'].copy()
    parts = e2.unit.str.split('|', expand=True); e2['pid'] = parts[0]; e2['i'] = parts[1].astype(int)
    e2 = e2[e2.i <= 6]
    cum = []
    for det, g in e2.groupby('detector'):
        anyf = g.groupby(['seed', 'unit', 'pid'])['flag'].max().reset_index()
        r = boot(anyf.groupby(['unit', 'pid'])['flag'].mean().to_numpy(), anyf.groupby(['unit', 'pid']).size().index.get_level_values(1))
        cum.append(dict(detector=det, any_flag_3to6=r['est'], lo=r['lo'], hi=r['hi'], n_series=r['n']))
    out['P2_cumulative_false_alarms'] = cum
    # ---- P3 PPV
    M = pd.DataFrame(json.load(open(os.path.join(RES, 'metrics.json'))))
    G = load_grape(); prev_g = float(np.mean([g['MD'] for g in G]))
    ppv = []
    for _, r in M.iterrows():
        def f(se, fpr, pi): return float(se * pi / (se * pi + fpr * (1 - pi))) if se * pi + fpr * (1 - pi) > 0 else None
        ppv.append(dict(detector=r.detector, k=int(r.k),
                        ppv_grape=None if pd.isna(r.grape_sens) else f(r.grape_sens, 1 - r.grape_spec, prev_g),
                        ppv_uw_truenull_10=f(r.sens, r.fpr_true_null, 0.10), ppv_uw_truenull_20=f(r.sens, r.fpr_true_null, 0.20)))
    out['P3_ppv'] = ppv; out['grape_prevalence_MD'] = prev_g
    # ---- P4 GRAPE overlap
    e4 = raw[(raw['eval'] == 'E4') & (raw.detector == 'D1 OLS-MD') & (raw.k == 3) & (raw.label == 1)]
    nv = {g['pid'] + g['eye']: len(g['t']) for g in G}
    e4 = e4.assign(nvis=e4.unit.map(nv))
    out['P4_grape_D1_k3_by_visits'] = dict(
        exactly3=dict(flagged=int(e4[e4.nvis == 3].flag.sum()), n=int((e4.nvis == 3).sum())),
        ge4=dict(flagged=int(e4[e4.nvis >= 4].flag.sum()), n=int((e4.nvis >= 4).sum())),
        n_eyes_exactly3=int(sum(v == 3 for v in nv.values())),
        points_per_eye=dict(min=int(min(g['sens'].shape[1] for g in G)), median=float(np.median([g['sens'].shape[1] for g in G])),
                            max=int(max(g['sens'].shape[1] for g in G)),
                            n_below_max=int(sum(g['sens'].shape[1] < max(h['sens'].shape[1] for h in G) for g in G))))
    json.dump(out, open(os.path.join(RES, 'posthoc.json'), 'w'), indent=1)
    print(P1.round(3).to_string()); print(T.round(3).to_string()); print(pd.DataFrame(cum).round(3).to_string())
    print(out['P4_grape_D1_k3_by_visits'], prev_g)


if __name__ == '__main__':
    main()
