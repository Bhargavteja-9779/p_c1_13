"""Order-dependent per-location features for a VF series under many candidate orderings (vectorised)."""
import numpy as np, torch

def grid_neighbors():
    """8-neighbour adjacency of the 54 24-2 points on the 8x9 grid (right-eye orientation, as stored in UWHVF)."""
    rows = [4, 6, 8, 9, 9, 8, 6, 4]
    starts = [3, 2, 1, 0, 0, 1, 2, 3]
    pos = []
    for r, (n, c0) in enumerate(zip(rows, starts)):
        for c in range(c0, c0 + n):
            pos.append((r, c))
    pos = np.array(pos)
    A = np.zeros((54, 54))
    for i in range(54):
        for j in range(54):
            if i != j and np.abs(pos[i] - pos[j]).max() == 1:
                A[i, j] = 1
    return pos, A

def ols_features(Y, t):
    """Y: (..., k, L) sensitivities; t: (..., k) times in years. Returns slope b, t-stat, (..., L)."""
    tm = t.mean(-1, keepdim=True)
    tc = t - tm
    sxx = (tc ** 2).sum(-1, keepdim=True).clamp_min(1e-6)            # (...,1)
    Ym = Y.mean(-2, keepdim=True)
    b = (tc.unsqueeze(-1) * (Y - Ym)).sum(-2) / sxx                   # (..., L)
    res = Y - Ym - tc.unsqueeze(-1) * b.unsqueeze(-2)
    k = Y.shape[-2]
    s2 = (res ** 2).sum(-2) / max(k - 2, 1)
    se = torch.sqrt(s2 / sxx + 1e-4)
    return b, b / se
