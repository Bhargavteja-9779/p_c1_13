"""Post-hoc robustness checks requested in review round 2 (NOT pre-specified; labelled exploratory in the paper).
Retest-calibrated (RC) D1 and D2 need no training, so their RC thresholds (results/amendB/amendB.json) are applied to
ALL UWHVF eyes with >= 8 tests (train+val+test) under several reference definitions:
  primary (-0.3 dB/yr, p<0.01 / p>0.5), stricter cut-offs (-0.5 and -1.0 dB/yr), future-only (tests k+1..end, >= 5 tests),
  and the flag rate among indeterminate eyes (neither progressor nor stable under the primary reference).
Usage (from code/): python -m src.statistics.amendment_b_robust -> ../results/amendB/robust.json"""
import os, sys, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.data.uwhvf import load_series, blind_spot_mask
from src.models.deferral import ols, md_series
from src.models.conformal_vf import stat_md
from src.models.detectors import md_slope
from src.statistics.amendment_b_stats import paired, ci
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
OUT = os.path.join(ROOT, 'results', 'amendB')

def label(t, y, cut):
    b, p, _ = ols(t, y); return 1 if (b < cut and p < 0.01) else (0 if p > 0.5 else None)

def main():
    TH = {(r['detector'].split()[0], r['k']): r['thr_RC'] for r in json.load(open(os.path.join(OUT, 'amendB.json')))['thresholds']}
    keep = ~blind_spot_mask(); rows = []
    for s in load_series():
        if len(s['ages']) < 8: continue
        t = s['ages'] - s['ages'][0]; Y = s['sens'][:, keep]; y = md_series(s['td'])
        labs = {f'cut{c}': label(t, y, c) for c in (-0.3, -0.5, -1.0)}
        for k in (3, 4, 5, 6):
            tf, yf = t[k:] - t[k], y[k:]
            fut = label(tf, yf, -0.3) if len(tf) >= 5 else None
            d1 = float(stat_md(t[None, :k], Y[None, :k])[0]) > TH[('D1', k)]
            d2 = -md_slope(t[:k], Y[:k])[0] > TH[('D2', k)]
            rows.append(dict(unit=s['pid'] + s['eye'], k=k, D1=float(d1), D2=float(d2), future=fut, **labs))
    d = pd.DataFrame(rows); out = {}
    for ref in ('cut-0.3', 'cut-0.5', 'cut-1.0', 'future'):
        for k in (3, 4, 5, 6):
            g = d[d.k == k]; r = dict(reference=ref, k=k)
            for det in ('D1', 'D2'):
                for nm, lv, inv in (('sens', 1, False), ('spec', 0, True)):
                    x = g[g[ref] == lv]; u = pd.DataFrame(dict(flag=x[det].to_numpy(), cluster=x.unit.str[:-1].to_numpy()))
                    c = ci(u)
                    if inv: c = dict(est=1 - c['est'], lo=1 - c['hi'], hi=1 - c['lo'], n=c['n'])
                    r.update({f'{det}_{nm}': c['est'], f'{det}_{nm}_lo': c['lo'], f'{det}_{nm}_hi': c['hi'], f'n_{nm}': c['n']})
            x = g[g[ref] == 1]
            pr = paired(x.set_index('unit').D1, x.set_index('unit').D2, lambda u: u[:-1])
            r.update({'diff_sens': pr['diff'], 'diff_lo': pr['diff_lo'], 'diff_hi': pr['diff_hi'], 'p': pr['p']})
            out.setdefault('by_reference', []).append(r)
    ind = d[d['cut-0.3'].isna()]
    out['indeterminate'] = [dict(k=k, n=int((ind.k == k).sum()), D1_flag=float(ind[ind.k == k].D1.mean()), D2_flag=float(ind[ind.k == k].D2.mean()))
                            for k in (3, 4, 5, 6)]
    out['note'] = 'Post-hoc (review round 2). RC thresholds from amendB.json; eyes from all splits (D1, D2 untrained).'
    json.dump(out, open(os.path.join(OUT, 'robust.json'), 'w'), indent=1)
    print(pd.DataFrame(out['by_reference'])[['reference', 'k', 'n_sens', 'n_spec', 'D1_sens', 'D2_sens', 'diff_sens', 'diff_lo', 'diff_hi', 'p', 'D1_spec', 'D2_spec']].round(3).to_string())
    print(out['indeterminate'])

if __name__ == '__main__':
    main()
