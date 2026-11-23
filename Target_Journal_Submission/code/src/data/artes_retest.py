"""Artes et al. 2014 short-term retest data: 30 glaucoma patients x 12 weekly 24-2 fields (Halifax).
Distributed in the visualFields R package (data/vfpwgRetest24d2.rda, GPL-3)."""
import os, numpy as np
RDA = os.environ.get('ARTES_RDA', '/home/user/p_c1_13/data_raw/ext/visualFields/data/vfpwgRetest24d2.rda')

def load_artes(path=RDA):
    import pyreadr
    d = list(pyreadr.read_r(path).values())[0]
    cols = [f'l{i}' for i in range(1, 55)]
    out = []
    for (pid, eye), g in d.groupby(['id', 'eye']):
        g = g.sort_values('date')
        days = (np.array(g['date'], dtype='datetime64[D]') - np.array(g['date'], dtype='datetime64[D]')[0]).astype(float)
        out.append(dict(pid=str(pid), eye=eye, t=days / 365.25, sens=g[cols].to_numpy(float),
                        fpr=g['fpr'].to_numpy(float), fnr=g['fnr'].to_numpy(float), fl=g['fl'].to_numpy(float)))
    return out
