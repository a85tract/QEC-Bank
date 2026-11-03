"""Sign-free n-qubit Paulis in symplectic form. Phases are deliberately dropped."""
from __future__ import annotations
import numpy as np

_CHARS = {(0, 0): "_", (1, 0): "X", (0, 1): "Z", (1, 1): "Y"}

class Pauli:
    def __init__(self, x, z):
        self.x = (np.asarray(x, dtype=np.uint8) & 1).astype(np.uint8)
        self.z = (np.asarray(z, dtype=np.uint8) & 1).astype(np.uint8)
        if self.x.shape != self.z.shape or self.x.ndim != 1:
            raise ValueError("x and z must be equal-length 1D arrays")

    @classmethod
    def from_str(cls, s: str) -> "Pauli":
        s = s.upper()
        x = [1 if c in "XY" else 0 for c in s]
        z = [1 if c in "ZY" else 0 for c in s]
        if any(c not in "IXYZ_" for c in s):
            raise ValueError(f"bad Pauli string: {s}")
        return cls(x, z)

    @classmethod
    def from_symplectic(cls, row) -> "Pauli":
        row = np.asarray(row, dtype=np.uint8)
        n = row.size // 2
        return cls(row[:n], row[n:])

    @property
    def n(self) -> int:
        return int(self.x.size)

    def to_str(self) -> str:
        return "".join(_CHARS[(int(a), int(b))] for a, b in zip(self.x, self.z))

    def symplectic(self) -> np.ndarray:
        return np.concatenate([self.x, self.z])

    def weight(self) -> int:
        return int(np.count_nonzero(self.x | self.z))

    def commutes(self, other: "Pauli") -> bool:
        if self.n != other.n:
            raise ValueError(f"Pauli length mismatch: {self.n} vs {other.n}")
        s = (int(self.x @ other.z) + int(self.z @ other.x)) % 2
        return s == 0

    def __mul__(self, other: "Pauli") -> "Pauli":
        if self.n != other.n:
            raise ValueError(f"Pauli length mismatch: {self.n} vs {other.n}")
        return Pauli(self.x ^ other.x, self.z ^ other.z)

    def __eq__(self, other) -> bool:
        return isinstance(other, Pauli) and np.array_equal(self.x, other.x) and np.array_equal(self.z, other.z)

    def __repr__(self) -> str:
        return f"Pauli({self.to_str()})"
