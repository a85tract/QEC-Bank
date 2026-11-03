"""GF(2) linear algebra on numpy uint8 arrays."""
import numpy as np

def _as_mat(A):
    A = (np.atleast_2d(np.asarray(A, dtype=np.uint8)) & 1).astype(np.uint8)
    return A

def rref(A):
    """Reduced row echelon form over GF(2). Returns (R, pivot_columns)."""
    R = _as_mat(A).copy()
    rows, cols = R.shape
    pivots, r = [], 0
    for c in range(cols):
        if r >= rows:
            break
        hit = np.nonzero(R[r:, c])[0]
        if hit.size == 0:
            continue
        pr = r + hit[0]
        if pr != r:
            R[[r, pr]] = R[[pr, r]]
        mask = R[:, c].astype(bool)
        mask[r] = False
        R[mask] ^= R[r]
        pivots.append(c)
        r += 1
    return R, pivots

def rank(A) -> int:
    A = _as_mat(A)
    if A.size == 0:
        return 0
    return len(rref(A)[1])

def nullspace(A) -> np.ndarray:
    """Basis of the right nullspace; rows are basis vectors. Shape (dim, n)."""
    A = _as_mat(A)
    m, n = A.shape
    R, piv = rref(A)
    free = [c for c in range(n) if c not in piv]
    basis = np.zeros((len(free), n), dtype=np.uint8)
    for bi, f in enumerate(free):
        basis[bi, f] = 1
        for i, p in enumerate(piv):
            if R[i, f]:
                basis[bi, p] = 1
    return basis

def in_rowspace(v, A) -> bool:
    A = _as_mat(A)
    v = _as_mat(v)
    if A.size == 0:
        return not np.any(v)
    return rank(np.vstack([A, v])) == rank(A)
