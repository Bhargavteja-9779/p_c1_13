"""Cohort descriptives and pre-registered real-world measures -> ../results/descriptives.json.
Run from code/:  python scripts/descriptives.py   (needs the three public data sets, see README; and raw_results.csv[.gz])."""
import os, sys, json, gzip
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import numpy as np, pandas as pd
from src.data.uwhvf import load_series, patient_split, blind_spot_mask
from src.data.artes_retest import load_artes
from src.data.grape import load_grape
from src.models.deferral import md_series
from run_all import reference

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
RES = os.path.join(ROOT, 'results')

def q(x):
    x = np.asarray(x, float)
    return dict(median=float(np.median(x)), q1=float(np.percentile(x, 25)), q3=float(np.percentile(x, 75)),
                mean=float(x.mean()), max=float(x.max()), min=float(x.min()), sd=float(x.std(ddof=1)) if len(x) > 1 else 0.0, n=int(len(x)))

def main():
    out = {}
    S = load_series(); sp = patient_split(S)
    out['uw_all'] = dict(n_fields=int(sum(len(s['ages']) for s in S)), n_eyes=len(S), n_patients=len({s['pid'] for s in S}))
    for part in ('train', 'val', 'test'):
        P = [s for s in S if sp[s['pid']] == part]
        out[f'uw_{part}'] = dict(n_patients=len({s['pid'] for s in P}), n_eyes=len(P),
                                 n_eyes_ge3=sum(len(s['ages']) >= 3 for s in P), n_fields=int(sum(len(s['ages']) for s in P)))
    # test-set reference cohort (eyes >= 8 tests)
    test = [s for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 8]
    rows = []
    for s in test:
        lab = reference(s)
        md = md_series(s['td'])
        rows.append(dict(label=lab, age0=s['ages'][0], n=len(s['ages']), fu=s['ages'][-1] - s['ages'][0],
                         md0=md[0], gap=float(np.median(np.diff(s['ages']))), t6=s['ages'][min(5, len(s['ages']) - 1)] - s['ages'][0],
                         t3=s['ages'][2] - s['ages'][0], pid=s['pid'], female=float(str(s['gender']).upper().startswith('F'))))
    R = pd.DataFrame(rows)
    out['uw_test_ge8'] = dict(n_eyes=len(R), n_patients=R.pid.nunique())
    for lab, name in ((1, 'progressors'), (0, 'stable')):
        g = R[R.label == lab]
        out[f'ref_{name}'] = dict(n_eyes=len(g), n_patients=g.pid.nunique(), age0=q(g.age0), n_tests=q(g.n), followup_y=q(g.fu),
                                  md_baseline_proxy=q(g.md0), years_to_test3=q(g.t3), years_to_test6=q(g.t6),
                                  female_eyes=int(g.female.sum()), female_patients=int(g.groupby('pid').female.max().sum()))
    out['ref_excluded_eyes'] = int(R.label.isna().sum())
    out['uw_gender_values'] = sorted({str(s['gender']) for s in S})
    # labelled eyes available to supervised detectors (D8, D9): train/val eyes with >= 8 tests and a reference label
    for part in ('train', 'val'):
        labs = [reference(s) for s in S if sp[s['pid']] == part and len(s['ages']) >= 8]
        out[f'labelled_{part}'] = dict(progressors=sum(l == 1 for l in labs), stable=sum(l == 0 for l in labs))
    # Study 2 cross-fitted reference cohort (all UWHVF eyes with >= 8 tests)
    rp = os.path.join(RES, 'study2_refs.csv')
    if os.path.exists(rp):
        R2 = pd.read_csv(rp, dtype={'unit': str, 'pid': str}); byu = {s['pid'] + s['eye']: s for s in S}
        for lab, val, name in (('R1', 1, 's2_progressors'), ('R1', 0, 's2_stable'), ('R2', 0, 's2_flat_stable')):
            g = R2[R2[lab] == val]; ss = [byu[u] for u in g.unit]
            out[name] = dict(n_eyes=len(g), n_patients=int(g.pid.nunique()), age0=q([x['ages'][0] for x in ss]),
                             n_tests=q([len(x['ages']) for x in ss]), followup_y=q([x['ages'][-1] - x['ages'][0] for x in ss]),
                             md_baseline_proxy=q([md_series(x['td'])[0] for x in ss]),
                             years_to_test3=q([x['ages'][2] - x['ages'][0] for x in ss]), years_to_test6=q([x['ages'][5] - x['ages'][0] for x in ss]),
                             female_patients=int(len({x['pid'] for x in ss if str(x['gender']).upper().startswith('F')})))
        out['s2_all'] = dict(n_eyes=len(R2), n_patients=int(R2.pid.nunique()))
    # Artes
    A = load_artes()
    out['artes'] = dict(n_patients=len({a['pid'] for a in A}), n_series=len(A), n_fields=int(sum(len(a['t']) for a in A)),
                        md_proxy=q([np.mean(a['sens'][:, ~blind_spot_mask()]) for a in A]),
                        span_days=q([a['t'][-1] * 365.25 for a in A]),
                        windows={str(k): int(sum(len(a['t']) - k + 1 for a in A)) for k in (3, 4, 5, 6)})
    # GRAPE
    G = load_grape()
    from src.data.grape import XLSX
    b = pd.read_excel(XLSX, 'Baseline', header=None).iloc[2:]
    gb = {(str(int(r[0])), str(r[1])): r[3] for _, r in b.iterrows()}
    cat = {(str(int(r[0])), str(r[1])): str(r[10]) for _, r in b.iterrows()}
    out['grape'] = dict(n_eyes=len(G), n_patients=len({g['pid'] for g in G}), n_records=int(sum(len(g['t']) for g in G)),
                        n_visits=q([len(g['t']) for g in G]), followup_y=q([g['t'][-1] for g in G]),
                        age=q([g['age'] for g in G]),
                        female_patients=int(len({g['pid'] for g in G if str(gb.get((g['pid'], g['eye']), '')).upper().startswith('F')})),
                        category=pd.Series([cat.get((g['pid'], g['eye']), 'NA') for g in G]).value_counts().to_dict(), n_points=q([g['sens'].shape[1] for g in G]),
                        md_label_pos=int(sum(g['MD'] == 1 for g in G)), plr2_pos=int(sum(g['PLR2'] == 1 for g in G)),
                        plr3_pos=int(sum(g['PLR3'] == 1 for g in G)), eyes_ge3=int(sum(len(g['t']) >= 3 for g in G)),
                        eyes_ge4=int(sum(len(g['t']) >= 4 for g in G)))
    # real-world measure: tests to first detection among reference progressors (eyes followed >= 8 tests), k = 3..6
    p = os.path.join(RES, 'raw_results.csv')
    raw = pd.read_csv(p) if os.path.exists(p) else pd.read_csv(p + '.gz')
    e1 = raw[(raw['eval'] == 'E1') & (raw['label'] == 1)]
    ttd = {}
    for det, g in e1.groupby('detector'):
        per_seed = []
        for seed, h in g.groupby('seed'):
            piv = h.pivot_table(index='unit', columns='k', values='flag')
            first = piv.apply(lambda r: next((k for k in sorted(piv.columns) if r[k] == 1), np.nan), axis=1)
            per_seed.append(dict(detected_by6=float(first.notna().mean()), n=int(len(first)),
                                 mean_first_k_detected=float(first.mean()) if first.notna().any() else None))
        ttd[det] = dict(detected_by6_mean=float(np.mean([x['detected_by6'] for x in per_seed])),
                        detected_by6_sd=float(np.std([x['detected_by6'] for x in per_seed], ddof=1)) if len(per_seed) > 1 else 0.0,
                        n=per_seed[0]['n'], n_seeds=len(per_seed),
                        mean_first_k_detected=float(np.mean([x['mean_first_k_detected'] for x in per_seed if x['mean_first_k_detected'] is not None])))
    out['time_to_detection_ref_progressors'] = ttd
    json.dump(out, open(os.path.join(RES, 'descriptives.json'), 'w'), indent=1)
    print(json.dumps(out, indent=1)[:4000])

if __name__ == '__main__':
    main()
