"""Load UWHVF (Montesano et al. 2022, TVST, BSD-3) into per-eye series and make a locked patient-level split."""
import json, os, hashlib
import numpy as np

UWHVF_JSON = os.environ.get("UWHVF_JSON", "/home/user/uw-biomedical-ml/uwhvf/alldata.json")
MASK_VALUE = 100.0

def load_series(path=UWHVF_JSON):
    """Return list of dicts: pid, eye, ages (sorted), sens (k x 54), td (k x 54), gender."""
    d = json.load(open(path))
    out = []
    for pid, pt in d["data"].items():
        for eye in ("L", "R"):
            if eye not in pt:
                continue
            s = sorted(pt[eye], key=lambda v: v["age"])
            sens = np.array([v["hvf_seq"] for v in s], float)
            td = np.array([v["td_seq"] for v in s], float)
            out.append(dict(pid=str(pid), eye=eye, ages=np.array([v["age"] for v in s]), sens=sens, td=td,
                            gender=pt.get("gender", "")))
    return out

BLIND_SPOT_IDX = (25, 34)  # 24-2 points at the physiological blind spot; TD is undefined there (TD == sensitivity in UWHVF)

def blind_spot_mask(series=None):
    """Boolean mask over the 54 points, True = blind spot (excluded). Verified from data: td == sens only at 25 and 34."""
    m = np.zeros(54, bool); m[list(BLIND_SPOT_IDX)] = True
    return m

def patient_split(series, fractions=(0.6, 0.2, 0.2), salt="uwhvf-split-v1"):
    """Deterministic patient-level split using a salted hash of the patient id (no RNG state dependence)."""
    pids = sorted({s["pid"] for s in series})
    def u(p):
        return int(hashlib.sha256((salt + p).encode()).hexdigest()[:8], 16) / 0xFFFFFFFF
    split = {}
    for p in pids:
        x = u(p)
        split[p] = "train" if x < fractions[0] else ("val" if x < fractions[0] + fractions[1] else "test")
    return split
