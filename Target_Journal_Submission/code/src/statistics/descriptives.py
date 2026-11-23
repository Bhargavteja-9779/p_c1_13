"""Descriptive counts of the three data sets and the pre-registered real-world measures.
Writes results/descriptives.json and results/realworld.json. Every number in the manuscript that is not in
metrics.json / statistics.json comes from these two files.
Usage (from code/): python -m src.statistics.descriptives"""
import os, sys, json
import numpy as np, pandas as pd
from scipy import stats
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from run_all import reference
from src.data.uwhvf import load_series, patient_split
from src.data.artes_retest import load_artes
from src.data.grape import load_grape

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RES = os.path.join(ROOT, 'results')


def q(x):
    x = np.asarray(x, float)
    return dict(median=float(np.median(x)), q1=float(np.quantile(x, .25)), q3=float(np.quantile(x, .75)))


def descriptives():
    S = load_series(); sp = patient_split(S)
    out = dict(uwhvf=dict(n_fields=int(sum(len(s['ages']) for s in S)), n_eyes=len(S),
                          n_patients=len({s['pid'] for s in S})))
    for part in ('train', 'val', 'test'):
        E = [s for s in S if sp[s['pid']] == part]
        E3 = [s for s in E if len(s['ages']) >= 3]
        out['uwhvf'][part] = dict(n_patients=len({s['pid'] for s in E}), n_eyes=len(E), n_eyes_ge3=len(E3),
                                  n_patients_ge3=len({s['pid'] for s in E3}))
    T8 = [s for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 8]
    labs = [reference(s) for s in T8]
    ref = [s for s, l in zip(T8, labs) if l is not None]
    md = lambda s: float(np.mean(s['td'][0][np.r_[0:25, 26:34, 35:54]]))
    out['uwhvf']['test_ge8'] = dict(
        n_eyes=len(T8), n_patients=len({s['pid'] for s in T8}), n_prog=int(sum(l == 1 for l in labs)),
        n_stable=int(sum(l == 0 for l in labs)), n_excluded=int(sum(l is None for l in labs)),
        n_ref_patients=len({s['pid'] for s in ref}),
        n_tests=q([len(s['ages']) for s in ref]), followup_years=q([s['ages'][-1] - s['ages'][0] for s in ref]),
        age_years=q([s['ages'][0] for s in ref]), baseline_mtd_db=q([md(s) for s in ref]),
        interval_years=q([np.median(np.diff(s['ages'])) for s in ref]))
    A = load_artes()
    out['artes'] = dict(n_patients=len({a['pid'] for a in A}), n_eyes=len(A), n_tests=q([len(a['t']) for a in A]),
                        span_weeks=q([a['t'][-1] * 52.18 for a in A]),
                        windows={k: int(sum(max(len(a['t']) - k + 1, 0) for a in A)) for k in (3, 4, 5, 6)})
    G = load_grape()
    out['grape'] = dict(n_eyes=len(G), n_patients=len({g['pid'] for g in G}),
                        n_records=int(sum(len(g['t']) for g in G)), n_visits=q([len(g['t']) for g in G]),
                        n_points=q([g['sens'].shape[1] for g in G]),
                        followup_years=q([g['t'][-1] for g in G]),
                        n_md_prog=int(sum(g['MD'] == 1 for g in G)), n_plr2_prog=int(sum(g['PLR2'] == 1 for g in G)),
                        n_plr3_prog=int(sum(g['PLR3'] == 1 for g in G)),
                        n_ge3=int(sum(len(g['t']) >= 3 for g in G)), n_ge4=int(sum(len(g['t']) >= 4 for g in G)))
    return out


def realworld(raw):
    """Pre-registered real-world measures:
    (a) false progression flags per 1,000 stable eyes per detection opportunity = true-null FPR x 1,000;
    (b) number of tests to first detection among reference progressors (first k in 3..6 with a flag,
        seed-majority flag for stochastic detectors), and share of progressors detected by 6 tests;
    (c) share of reference-stable eyes flagged at least once by 6 tests (cumulative false flags)."""
    M = json.load(open(os.path.join(RES, 'metrics.json')))
    d = raw[raw['eval'] == 'E1']
    f = d.groupby(['detector', 'unit', 'k', 'label'])['flag'].mean().round().reset_index()
    out = {}
    for det, g in f.groupby('detector'):
        w = g.pivot_table(index=['unit', 'label'], columns='k', values='flag').reset_index()
        ks = [k for k in (3, 4, 5, 6) if k in w]
        first = w[ks].apply(lambda r: next((k for k in ks if r[k] == 1), np.nan), axis=1)
        prog, stab = w['label'] == 1, w['label'] == 0
        fp = first[prog]
        out[det] = dict(
            false_flags_per_1000={int(m['k']): 1000 * m['fpr_true_null'] for m in M if m['detector'] == det},
            prog_detected_by_6=float(fp.notna().mean()), prog_n=int(prog.sum()),
            prog_median_first_k_detected=float(fp.median()) if fp.notna().any() else None,
            prog_mean_first_k_detected=float(fp.mean()) if fp.notna().any() else None,
            stable_ever_flagged_by_6=float(first[stab].notna().mean()), stable_n=int(stab.sum()))
    # bootstrap CI for RQ3 Spearman rho (resampling detector x k cells; protocol: 'bootstrap CI')
    c = pd.DataFrame(M).dropna(subset=['fpr_true_null', 'fpr_shuffle'])
    rng = np.random.default_rng(0); rhos = []
    for _ in range(2000):
        s = c.iloc[rng.integers(0, len(c), len(c))]
        rhos.append(stats.spearmanr(s.fpr_shuffle, s.fpr_true_null).statistic)
    rq3 = dict(rho_ci_lo=float(np.nanquantile(rhos, .025)), rho_ci_hi=float(np.nanquantile(rhos, .975)),
               method='bootstrap over detector x k cells, 2,000 resamples, seed 0')
    return dict(per_detector=out, rq3_rho_ci=rq3)


if __name__ == '__main__':
    desc = descriptives()
    json.dump(desc, open(os.path.join(RES, 'descriptives.json'), 'w'), indent=1)
    raw = pd.read_csv(os.path.join(RES, 'raw_results.csv.gz'), dtype={'unit': str, 'extra': str})
    rw = realworld(raw)
    json.dump(rw, open(os.path.join(RES, 'realworld.json'), 'w'), indent=1)
    print(json.dumps(desc, indent=1)); print(json.dumps(rw, indent=1))
