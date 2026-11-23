"""Descriptive numbers for the manuscript (data sets, cohorts) and the pre-registered real-world measures.
Every number used in the paper's text is written here by code; nothing is typed by hand.
Usage (from code/): python -m src.statistics.describe  -> ../results/dataset_counts.json, ../results/realworld.json"""
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
RES = os.path.join(ROOT, 'results')


def dataset_counts():
    from src.data.uwhvf import load_series, patient_split, UWHVF_JSON
    from src.data.artes_retest import load_artes
    from src.data.grape import load_grape, XLSX
    from run_all import reference
    hdr = json.load(open(UWHVF_JSON))
    S = load_series(); sp = patient_split(S)
    out = dict(uw_patients_file=hdr['pts'], uw_eyes_file=hdr['eyes'], uw_fields_file=hdr['hvfs'],
               uw_patients=len({s['pid'] for s in S}), uw_eyes=len(S), uw_fields=int(sum(len(s['ages']) for s in S)))
    for part in ('train', 'val', 'test'):
        E = [s for s in S if sp[s['pid']] == part and len(s['ages']) >= 3]
        out[f'uw_{part}_eyes_ge3'] = len(E); out[f'uw_{part}_patients_ge3'] = len({s['pid'] for s in E})
    T = [s for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 8]
    lab = [reference(s) for s in T]
    R = [s for s, l in zip(T, lab) if l is not None]
    out.update(uw_test_eyes_ge8=len(T), uw_test_ref_prog=sum(l == 1 for l in lab), uw_test_ref_stable=sum(l == 0 for l in lab),
               uw_test_ref_excluded=sum(l is None for l in lab), uw_test_ref_patients=len({s['pid'] for s in R}))
    nt = np.array([len(s['ages']) for s in R]); fu = np.array([s['ages'][-1] - s['ages'][0] for s in R])
    gap = np.concatenate([np.diff(s['ages']) for s in R]); age0 = np.array([s['ages'][0] for s in R])
    md0 = []
    from src.models.deferral import md_series
    for s in R: md0.append(md_series(s['td'][:1])[0])
    md0 = np.array(md0)
    for name, v in (('ntests', nt), ('followup_y', fu), ('interval_y', gap), ('age0', age0), ('md0', md0)):
        out[f'uw_ref_{name}_median'] = float(np.median(v)); out[f'uw_ref_{name}_q1'] = float(np.quantile(v, .25))
        out[f'uw_ref_{name}_q3'] = float(np.quantile(v, .75))
    A = load_artes()
    out.update(artes_patients=len({a['pid'] for a in A}), artes_eyes=len(A), artes_fields=int(sum(len(a['t']) for a in A)),
               artes_span_days_median=float(np.median([a['t'][-1] * 365.25 for a in A])))
    G = load_grape()
    f = pd.read_excel(XLSX, 'Follow-up', header=None).iloc[2:]
    out.update(grape_records=len(f), grape_eyes=len(G), grape_patients=len({g['pid'] for g in G}),
               grape_points=int(G[0]['sens'].shape[1]),
               grape_md_prog=sum(g['MD'] == 1 for g in G), grape_plr2_prog=sum(g['PLR2'] == 1 for g in G),
               grape_plr3_prog=sum(g['PLR3'] == 1 for g in G),
               grape_eyes_ge3=sum(len(g['t']) >= 3 for g in G), grape_eyes_ge4=sum(len(g['t']) >= 4 for g in G),
               grape_visits_median=float(np.median([len(g['t']) for g in G])))
    return out


def realworld():
    """Pre-registered real-world measures (protocol.md):
    (a) expected false progression flags per 1,000 stable eyes per detection opportunity = 1000 x true-no-change FPR;
    (b) number of tests to first detection among reference progressors (eyes followed to >= 8 tests), using the
        first k = 3..6 tests; an eye not flagged by 6 tests counts as '> 6'.
    Exploratory (not pre-registered, labelled as such in the paper): share of reference-STABLE eyes flagged at least
    once over the four looks k = 3..6 (cumulative false alarm in routine repeated review)."""
    M = json.load(open(os.path.join(RES, 'metrics.json')))
    d = pd.read_csv(os.path.join(RES, 'raw_results.csv.gz'), dtype={'unit': str, 'extra': str}, low_memory=False)
    e1 = d[(d['eval'] == 'E1') & d['label'].notna()]
    out = {}
    for det, g in e1.groupby('detector'):
        r = {}
        for m in M:
            if m['detector'] == det:
                r[f'false_flags_per_1000_k{m["k"]}'] = 1000 * m['fpr_true_null']
        firsts, cum_fp = [], []
        for seed, gs in g.groupby('seed'):
            w = gs.pivot_table(index=['unit', 'label'], columns='k', values='flag').reset_index()
            ks = [k for k in (3, 4, 5, 6) if k in w.columns]
            prog = w[w['label'] == 1]; stab = w[w['label'] == 0]
            first = np.full(len(prog), 99.0)
            for k in reversed(ks):
                first = np.where(prog[k].to_numpy() == 1, k, first)
            firsts.append(first)
            cum_fp.append(float((stab[ks].max(axis=1) == 1).mean()))
        F = np.stack(firsts)                     # seeds x eyes
        r['n_prog'] = int(F.shape[1])
        r['detected_by6_share'] = float((F <= 6).mean())
        r['median_tests_to_first_flag'] = float(np.median(np.median(F, axis=0)))  # 99 = not detected by 6 tests
        r['mean_tests_to_first_flag_among_detected'] = float(F[F <= 6].mean()) if (F <= 6).any() else None
        for k in (3, 4, 5, 6):
            r[f'cum_detected_by_k{k}'] = float((F <= k).mean())
        r['exploratory_cum_stable_flagged_k3to6'] = float(np.mean(cum_fp))
        out[det] = r
    return out


if __name__ == '__main__':
    json.dump(dataset_counts(), open(os.path.join(RES, 'dataset_counts.json'), 'w'), indent=1)
    json.dump(realworld(), open(os.path.join(RES, 'realworld.json'), 'w'), indent=1)
    print(open(os.path.join(RES, 'dataset_counts.json')).read()); print(open(os.path.join(RES, 'realworld.json')).read())
