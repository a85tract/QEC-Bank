"""R1 representation: stabilizer (+ optional gauge) generators as symplectic GF(2) rows."""
from __future__ import annotations
import numpy as np
from . import gf2
from .pauli import Pauli

def _symplectic_products(A: np.ndarray, B: np.ndarray) -> np.ndarray:
    """Matrix of symplectic inner products between rows of A and rows of B."""
    n = A.shape[1] // 2
    return (A[:, :n] @ B[:, n:].T + A[:, n:] @ B[:, :n].T) % 2

class CheckMatrix:
    def __init__(self, stab, gauge=None):
        self.stab = (np.atleast_2d(np.asarray(stab, dtype=np.uint8)) & 1).astype(np.uint8)
        self.gauge = None
        if gauge is not None and np.size(gauge):
            self.gauge = (np.atleast_2d(np.asarray(gauge, dtype=np.uint8)) & 1).astype(np.uint8)
            if self.gauge.shape[1] != self.stab.shape[1]:
                raise ValueError("stab and gauge widths differ")
        if self.stab.shape[1] % 2:
            raise ValueError("symplectic width must be even")

    @classmethod
    def from_paulis(cls, stab_strs, gauge=None) -> "CheckMatrix":
        rows = np.array([Pauli.from_str(s).symplectic() for s in stab_strs], dtype=np.uint8)
        grows = None
        if gauge:
            grows = np.array([Pauli.from_str(s).symplectic() for s in gauge], dtype=np.uint8)
        return cls(rows, grows)

    @classmethod
    def from_css(cls, HX, HZ) -> "CheckMatrix":
        HX = np.atleast_2d(np.asarray(HX, dtype=np.uint8)) & 1
        HZ = np.atleast_2d(np.asarray(HZ, dtype=np.uint8)) & 1
        n = HX.shape[1]
        x_rows = np.hstack([HX, np.zeros_like(HX)])
        z_rows = np.hstack([np.zeros_like(HZ), HZ])
        return cls(np.vstack([x_rows, z_rows]).astype(np.uint8))

    @property
    def n(self) -> int:
        return self.stab.shape[1] // 2

    @property
    def k(self) -> int:
        s = gf2.rank(self.stab)
        if self.gauge is None:
            return self.n - s
        g = gf2.rank(np.vstack([self.stab, self.gauge]))
        return self.n - (g + s) // 2

    def validate(self) -> None:
        if np.any(_symplectic_products(self.stab, self.stab)):
            raise ValueError("stabilizer generators do not mutually commute")
        if self.gauge is not None and np.any(_symplectic_products(self.stab, self.gauge)):
            raise ValueError("gauge generators do not commute with the stabilizer")

    def is_css(self) -> bool:
        n = self.n
        x_part, z_part = self.stab[:, :n], self.stab[:, n:]
        pure = ~(np.any(x_part, axis=1) & np.any(z_part, axis=1))
        return bool(np.all(pure))

    def to_css(self):
        if not self.is_css():
            raise ValueError("not a CSS check matrix")
        n = self.n
        x_rows = self.stab[np.any(self.stab[:, :n], axis=1)][:, :n]
        z_rows = self.stab[np.any(self.stab[:, n:], axis=1)][:, n:]
        return x_rows.copy(), z_rows.copy()
