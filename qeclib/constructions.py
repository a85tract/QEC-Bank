"""Code combinators. Constructions take codes (parity matrices) and emit codes (spec section 3.1)."""
from __future__ import annotations
import numpy as np

def rep_parity(L: int) -> np.ndarray:
    """(L-1) x L parity-check matrix of the length-L repetition code (open chain)."""
    H = np.zeros((L - 1, L), dtype=np.uint8)
    for i in range(L - 1):
        H[i, i] = H[i, i + 1] = 1
    return H

def hgp(H1, H2) -> tuple[np.ndarray, np.ndarray]:
    """Hypergraph product (Tillich-Zemor). Returns (HX, HZ) over GF(2).

    HX = [H1 (x) I_n2 | I_m1 (x) H2^T],  HZ = [I_n1 (x) H2 | H1^T (x) I_m2]
    n = n1*n2 + m1*m2;  HX HZ^T = H1 (x) H2^T + H1 (x) H2^T = 0 (mod 2).
    """
    H1 = (np.atleast_2d(np.asarray(H1, dtype=np.uint8)) & 1).astype(np.uint8)
    H2 = (np.atleast_2d(np.asarray(H2, dtype=np.uint8)) & 1).astype(np.uint8)
    m1, n1 = H1.shape
    m2, n2 = H2.shape
    HX = np.hstack([np.kron(H1, np.eye(n2, dtype=np.uint8)),
                    np.kron(np.eye(m1, dtype=np.uint8), H2.T)]) % 2
    HZ = np.hstack([np.kron(np.eye(n1, dtype=np.uint8), H2),
                    np.kron(H1.T, np.eye(m2, dtype=np.uint8))]) % 2
    return HX.astype(np.uint8), HZ.astype(np.uint8)
