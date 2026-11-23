"""Independent re-computation of deterministic detectors (D1-D3) on E1 (UW test, locked split) from raw data,
compared with the committed full-run flags in results/raw_results.csv.gz. Usage (from code/): python scripts/repro_check.py"""
import sys, os, json
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import pandas as pd
from src.data.uwhvf import load_series, patient_split, blind_spot_mask
from src.models import detectors as D
from run_all import reference
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
raw = pd.read_csv(os.path.join(ROOT, 'results', 'raw_results.csv.gz'), low_memory=False)
keep = ~blind_spot_mask(); S = load_series(); sp = patient_split(S)
test = [s for s in S if sp[s['pid']] == 'test' and len(s['ages']) >= 8]
out = {}
for cls in (D.OLSMD, D.MDRate, D.PLR3):
    det = cls(); det.fit([], None) if hasattr(det, 'fit') else None
    r = raw[(raw.detector == cls.name) & (raw['eval'] == 'E1')].set_index(['unit', 'k'])['flag']
    agree = n = 0
    for s in test:
        lab = reference(s); 
        t = s['ages'] - s['ages'][0]; Y = s['sens'][:, keep]
        for k in (3, 4, 5, 6):
            key = (s['pid'] + s['eye'], k)
            if key in r.index:
                n += 1; agree += int(det.flag(t[:k], Y[:k]) == r.loc[key])
    out[cls.name] = dict(n=n, agree=agree)
json.dump(out, open(os.path.join(ROOT, 'results', 'repro_check.json'), 'w'), indent=1); print(out)
