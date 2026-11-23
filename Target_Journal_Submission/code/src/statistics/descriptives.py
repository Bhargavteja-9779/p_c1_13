"""Dataset descriptives (Table 1) and the two pre-registered real-world measures.
Usage (from code/): python -m src.statistics.descriptives
Writes ../results/descriptives.json and ../tables/table1_datasets.csv. Reads the public data sets and
../results/raw_results.csv.gz (no detector is re-run)."""
import os, json
import numpy as np, pandas as pd
from src.data.uwhvf import load_series, patient_split
from src.data.artes_retest import load_artes
from src.data.grape import load_grape
from run_all import reference
from src.models.deferral import md_series

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
RES = os.path.join(ROOT, 'results')


def q(x):
    x = np.asarray(x, float)
    return dict(median=float(np.median(x)), q1=float(np.percentile(x, 25)), q3=float(np.percentile(x, 75)),
                mean=float(x.mean()), sd=float(x.std(ddof=1)), min=float(x.min()), max=float(x.max()), n=int(len(x)))


def uwhvf_block():
    S = load_series(); sp = patient_split(S)
    out = dict(n_fields=int(sum(len(s['ages']) for s in S)), n_eyes=len(S), n_patients=len({s['pid'] for s in S}))
    for part in ('train', 'val', 'test'):
        e = [s for s in S if sp[s['pid']] == part and len(s['ages']) >= 3]
        out[f'{part}_eyes_ge3'] = len(e); out[f'{part}_patients_ge3'] = len({s['pid'] for s in e})
    test8 = [s for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 8]
    labs = [reference(s) for s in test8]
    ref = [s for s, l in zip(test8, labs) if l is not None]
    out.update(test_eyes_ge8=len(test8), test_ref_prog=int(sum(l == 1 for l in labs)),
               test_ref_stable=int(sum(l == 0 for l in labs)), test_ref_indeterminate=int(sum(l is None for l in labs)),
               test_ref_patients=len({s['pid'] for s in ref}))
    for name, grp in (('ref', ref), ('ref_prog', [s for s, l in zip(test8, labs) if l == 1]),
                      ('ref_stable', [s for s, l in zip(test8, labs) if l == 0])):
        out[f'{name}_age_baseline'] = q([s['ages'][0] for s in grp])
        out[f'{name}_n_tests'] = q([len(s['ages']) for s in grp])
        out[f'{name}_followup_yr'] = q([s['ages'][-1] - s['ages'][0] for s in grp])
        out[f'{name}_md_baseline'] = q([md_series(s['td'][:1])[0] for s in grp])
        out[f'{name}_interval_first6_yr'] = q([np.diff(s['ages'][:6]).mean() for s in grp])
        out[f'{name}_time_to_test6_yr'] = q([s['ages'][5] - s['ages'][0] for s in grp])
    return out


def artes_block():
    A = load_artes()
    n = [len(a['t']) for a in A]
    return dict(n_eyes=len(A), n_patients=len({a['pid'] for a in A}), n_fields=int(sum(n)), tests_per_eye=q(n),
                span_days=q([a['t'][-1] * 365.25 for a in A]),
                windows={k: int(sum(max(0, m - k + 1) for m in n)) for k in (3, 4, 5, 6)})


def grape_block():
    G = load_grape()
    n = [len(g['t']) for g in G]
    return dict(n_eyes=len(G), n_patients=len({g['pid'] for g in G}), n_records=int(sum(n)), visits_per_eye=q(n),
                followup_yr=q([g['t'][-1] for g in G]), age=q([g['age'] for g in G]),
                n_points=int(G[0]['sens'].shape[1]),
                eyes_ge4=int(sum(m >= 4 for m in n)),
                label_MD=int(sum(g['MD'] for g in G)), label_PLR2=int(sum(g['PLR2'] for g in G)),
                label_PLR3=int(sum(g['PLR3'] for g in G)))


def real_world(raw):
    """(a) false progression flags per 1,000 stable eyes per detection opportunity = true-null FPR x 1000 (from metrics);
    (b) tests to first detection among E1 reference progressors: smallest k in 3..6 flagged (>6 if never), per seed."""
    e1 = raw[(raw['eval'] == 'E1') & (raw['label'] == 1)]
    res = []
    for (det, seed), g in e1.groupby(['detector', 'seed']):
        w = g.pivot_table(index='unit', columns='k', values='flag', aggfunc='max').reindex(columns=[3, 4, 5, 6]).fillna(0)
        first = w.apply(lambda r: next((k for k in (3, 4, 5, 6) if r[k] == 1), 7), axis=1)
        res.append(dict(detector=det, seed=int(seed), n=int(len(first)), flagged_by6=float((first <= 6).mean()),
                        median_first=float(np.median(first)), mean_first_capped7=float(first.mean())))
    r = pd.DataFrame(res)
    agg = r.groupby('detector').agg(n=('n', 'first'), flagged_by6=('flagged_by6', 'mean'),
                                    flagged_by6_sd=('flagged_by6', 'std'), median_first=('median_first', 'median'),
                                    mean_first_capped7=('mean_first_capped7', 'mean')).reset_index()
    return json.loads(agg.fillna(0).to_json(orient='records'))


def main():
    raw = pd.read_csv(os.path.join(RES, 'raw_results.csv.gz'), low_memory=False)
    M = pd.DataFrame(json.load(open(os.path.join(RES, 'metrics.json'))))
    fl = M[['detector', 'k', 'fpr_true_null', 'fpr_true_null_lo', 'fpr_true_null_hi']].copy()
    for c in ('fpr_true_null', 'fpr_true_null_lo', 'fpr_true_null_hi'):
        fl[c.replace('fpr_true_null', 'false_flags_per_1000')] = fl[c] * 1000
    out = dict(uwhvf=uwhvf_block(), artes=artes_block(), grape=grape_block(),
               tests_to_first_detection=real_world(raw),
               false_flags_per_1000=json.loads(fl.drop(columns=['fpr_true_null', 'fpr_true_null_lo', 'fpr_true_null_hi'])
                                               .to_json(orient='records')))
    json.dump(out, open(os.path.join(RES, 'descriptives.json'), 'w'), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k not in ('false_flags_per_1000',)}, indent=1)[:6000])


if __name__ == '__main__':
    main()
