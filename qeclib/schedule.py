"""R3 representation: measurement schedules and sign-free ISG (instantaneous
stabilizer group) tracking. Static codes are the period-1 special case."""
from __future__ import annotations
import numpy as np
from . import gf2
from .checkmatrix import CheckMatrix
from .pauli import Pauli

class Schedule:
    def __init__(self, n: int, rounds: list[list[Pauli]]):
        self.n = int(n)
        self.rounds = rounds
        if not rounds:
            raise ValueError("schedule needs at least one round")

    @classmethod
    def static_from_checkmatrix(cls, cm: CheckMatrix) -> "Schedule":
        paulis = [Pauli.from_symplectic(r) for r in cm.stab]
        return cls(cm.n, [paulis])

    def validate(self) -> None:
        for ri, rnd in enumerate(self.rounds):
            for i in range(len(rnd)):
                if rnd[i].n != self.n:
                    raise ValueError(f"round {ri}: Pauli width != n")
                for j in range(i + 1, len(rnd)):
                    if not rnd[i].commutes(rnd[j]):
                        raise ValueError(f"round {ri}: measurements {i},{j} anticommute")

class ISGTracker:
    def __init__(self, n: int):
        self.n = int(n)
        self.gens = np.zeros((0, 2 * n), dtype=np.uint8)

    def _sympl_with_all(self, v: np.ndarray) -> np.ndarray:
        n = self.n
        if self.gens.shape[0] == 0:
            return np.zeros(0, dtype=np.uint8)
        return (self.gens[:, :n] @ v[n:] + self.gens[:, n:] @ v[:n]) % 2

    def measure(self, p: Pauli) -> None:
        v = p.symplectic()
        anti = np.nonzero(self._sympl_with_all(v))[0]
        if anti.size == 0:
            if not gf2.in_rowspace(v, self.gens):
                self.gens = np.vstack([self.gens, v]).astype(np.uint8)
            return
        g0 = self.gens[anti[0]].copy()
        for idx in anti[1:]:
            self.gens[idx] ^= g0
        self.gens[anti[0]] = v

    def rank(self) -> int:
        return gf2.rank(self.gens)

def evolve(schedule: Schedule, cycles: int = 4) -> list[int]:
    t = ISGTracker(schedule.n)
    ranks = []
    for _ in range(cycles):
        for rnd in schedule.rounds:
            for p in rnd:
                t.measure(p)
            ranks.append(t.rank())
    return ranks

def periodic_rank(schedule: Schedule, max_cycles: int = 6) -> int:
    per_cycle = []
    t = ISGTracker(schedule.n)
    for _ in range(max_cycles):
        cyc = []
        for rnd in schedule.rounds:
            for p in rnd:
                t.measure(p)
            cyc.append(t.rank())
        per_cycle.append(cyc)
        if len(per_cycle) >= 2 and per_cycle[-1] == per_cycle[-2]:
            return per_cycle[-1][-1]
    raise RuntimeError(f"ISG ranks did not stabilize within {max_cycles} cycles")

def dynamic_k(schedule: Schedule) -> int:
    return schedule.n - periodic_rank(schedule)
