"""GRAPE (Huang et al. 2023, Sci Data, CC0): longitudinal VF + clinical progression labels (figshare file 41670009)."""
import os, numpy as np, pandas as pd
XLSX = os.environ.get('GRAPE_XLSX', '/home/user/p_c1_13/data_raw/ext/grape/vf_clinical.xlsx')

def load_grape(path=XLSX):
    b = pd.read_excel(path, 'Baseline', header=None).iloc[2:]
    f = pd.read_excel(path, 'Follow-up', header=None).iloc[2:]
    lab = {(int(r[0]), str(r[1])): dict(PLR2=int(r[7]), PLR3=int(r[8]), MD=int(r[9]), age=float(r[2])) for _, r in b.iterrows()}
    out = []
    for (sid, eye), g in f.groupby([0, 1]):
        g = g.sort_values(2)
        V = g.iloc[:, 8:69].to_numpy(float)
        valid = (V >= 0).all(0)                      # drop points coded -1 (blind spot / untested) in any visit
        t = g[3].to_numpy(float)
        L = lab.get((int(sid), str(eye)))
        if L is None:
            continue
        out.append(dict(pid=str(sid), eye=str(eye), t=t - t[0], sens=V[:, valid], **L))
    return out
