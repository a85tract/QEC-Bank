"""R2 representation: length-3 chain complex over GF(2), qubits on the middle grading."""
from __future__ import annotations
import numpy as np
from . import gf2
from .checkmatrix import CheckMatrix

class ChainComplex:
    def __init__(self, d1, d2):
        if np.asarray(d1).ndim != 2 or np.asarray(d2).ndim != 2:
            raise ValueError("boundary maps must be 2-D matrices")
        self.d1 = (np.atleast_2d(np.asarray(d1, dtype=np.uint8)) & 1).astype(np.uint8)
        self.d2 = (np.atleast_2d(np.asarray(d2, dtype=np.uint8)) & 1).astype(np.uint8)
        if self.d1.shape[1] != self.d2.shape[0]:
            raise ValueError("d1 columns must equal d2 rows (both index C1 = qubits)")

    @property
    def n(self) -> int:
        return self.d1.shape[1]

    def validate(self) -> None:
        if np.any((self.d1 @ self.d2) % 2):
            raise ValueError("not a chain complex: d1 @ d2 != 0 over GF(2)")

    def homology_dim(self) -> int:
        return self.n - gf2.rank(self.d1) - gf2.rank(self.d2)

    def to_checkmatrix(self) -> CheckMatrix:
        return CheckMatrix.from_css(HX=self.d1, HZ=self.d2.T)
