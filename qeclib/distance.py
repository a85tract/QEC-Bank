"""Distance computers. Exact = weight enumeration (small only). UB = seeded random search.
Every result carries its method; callers must store provenance (spec section 4)."""
from __future__ import annotations
from itertools import combinations, product
from math import comb
import numpy as np
from . import gf2
from .checkmatrix import CheckMatrix
from .diagnostics import make_diagnostic
from .logicals import (
    LogicalWitnessError,
    dressed_logical_quotient_basis,
    subsystem_gauge_basis,
    validate_dressed_logical_witness,
)
from .pauli import Pauli


MAX_EXACT_SUBSYSTEM_CANDIDATES = 2_000_000
SUBSYSTEM_RANDOM_METHOD = "rand-subsystem-dressed-logical-coset-v1"


class DistanceUnverifiable(Exception):
    def __init__(
        self,
        message: str,
        *,
        code: str = "distance.unverifiable",
        context: dict | None = None,
    ):
        super().__init__(message)
        self.code = code
        self.context = dict(context or {})

    def diagnostic(self) -> dict:
        return make_diagnostic(self.code, str(self), context=self.context)


def _exact_subsystem_dressed_distance(
    cm: CheckMatrix,
    *,
    w_max: int,
) -> tuple[int, str]:
    quotient = dressed_logical_quotient_basis(cm)
    if quotient.shape[0] == 0:
        raise DistanceUnverifiable(
            "subsystem code encodes no logical qubits",
            code="distance.subsystem_no_logical",
        )

    n = cm.n
    stabilizers = _independent_rows(cm.stab)
    gauge = subsystem_gauge_basis(cm)
    commutation = np.hstack([stabilizers[:, n:], stabilizers[:, :n]])
    candidates = 0
    for weight in range(1, min(w_max, n) + 1):
        layer_candidates = comb(n, weight) * (3**weight)
        if candidates + layer_candidates > MAX_EXACT_SUBSYSTEM_CANDIDATES:
            raise DistanceUnverifiable(
                "subsystem exact enumeration exceeds its deterministic candidate budget",
                code="distance.subsystem_exact_budget",
                context={
                    "candidate_budget": MAX_EXACT_SUBSYSTEM_CANDIDATES,
                    "completed_through_weight": weight - 1,
                    "next_weight": weight,
                    "next_layer_candidates": layer_candidates,
                },
            )
        for support in combinations(range(n), weight):
            for letters in product("XYZ", repeat=weight):
                chars = ["_"] * n
                for qubit, letter in zip(support, letters):
                    chars[qubit] = letter
                pauli = Pauli.from_str("".join(chars))
                vector = pauli.symplectic()
                if np.any((commutation @ vector) % 2):
                    continue
                if gf2.in_rowspace(vector, gauge):
                    continue
                validate_dressed_logical_witness(cm, pauli)
                return weight, "exact-subsystem-dressed-enum-v1"
        candidates += layer_candidates
    raise DistanceUnverifiable(
        f"no dressed logical found with weight <= {w_max}",
        code="distance.subsystem_exact_weight_limit",
        context={"w_max": w_max},
    )

def exact_distance(cm: CheckMatrix, w_max: int = 8) -> tuple[int, str]:
    if cm.gauge is not None:
        return _exact_subsystem_dressed_distance(cm, w_max=w_max)
    if cm.is_css():
        HX, HZ = cm.to_css()
        n = cm.n
        for w in range(1, w_max + 1):
            for support in combinations(range(n), w):
                v = np.zeros(n, dtype=np.uint8)
                v[list(support)] = 1
                if not np.any((HZ @ v) % 2) and not gf2.in_rowspace(v, HX):
                    return w, "exact-css-enum"   # X-type logical of weight w
                if not np.any((HX @ v) % 2) and not gf2.in_rowspace(v, HZ):
                    return w, "exact-css-enum"   # Z-type logical of weight w
        raise DistanceUnverifiable(f"no logical found with weight <= {w_max}")
    n = cm.n
    if n > 12:
        raise DistanceUnverifiable("generic Pauli enumeration limited to n <= 12")
    S = cm.stab
    M = np.hstack([S[:, n:], S[:, :n]])   # commutation test: M @ v == 0
    for w in range(1, n + 1):
        for support in combinations(range(n), w):
            for letters in product("XYZ", repeat=w):
                chars = ["_"] * n
                for q, c in zip(support, letters):
                    chars[q] = c
                v = Pauli.from_str("".join(chars)).symplectic()
                if not np.any((M @ v) % 2) and not gf2.in_rowspace(v, S):
                    return w, "exact-pauli-enum"
    raise DistanceUnverifiable("no logical operator exists (k = 0?)")

def _greedy_reduce(v: np.ndarray, H: np.ndarray) -> np.ndarray:
    improved = True
    while improved:
        improved = False
        for row in H:
            if int((v ^ row).sum()) < int(v.sum()):
                v = v ^ row
                improved = True
    return v


def _pauli_weight(v: np.ndarray) -> int:
    n = v.size // 2
    return int(np.count_nonzero(v[:n] | v[n:]))


def _independent_rows(rows: np.ndarray) -> np.ndarray:
    reduced, pivots = gf2.rref(rows)
    return reduced[:len(pivots)].astype(np.uint8, copy=True)


def _quotient_complement(
    space_basis: np.ndarray,
    subspace_basis: np.ndarray,
) -> np.ndarray:
    """Canonical complement of subspace inside space, with vectors as rows."""
    width = space_basis.shape[1]
    pivots = [int(np.flatnonzero(row)[0]) for row in subspace_basis]
    residuals: list[np.ndarray] = []
    for row in space_basis:
        residual = row.copy()
        for basis_row, pivot in zip(subspace_basis, pivots):
            if residual[pivot]:
                residual ^= basis_row
        if residual.any():
            residuals.append(residual)
    if not residuals:
        return np.zeros((0, width), dtype=np.uint8)
    return _independent_rows(np.asarray(residuals, dtype=np.uint8))


def _logical_coefficients(
    trial: int,
    dimension: int,
    rng: np.random.Generator,
) -> np.ndarray:
    coefficients = np.zeros(dimension, dtype=np.uint8)
    if trial < dimension:
        coefficients[trial] = 1
        return coefficients
    while not coefficients.any():
        coefficients = rng.integers(0, 2, dimension, dtype=np.uint8)
    return coefficients


def _steepest_reduce_pauli(v: np.ndarray, stabilizers: np.ndarray) -> np.ndarray:
    """Descend strictly in Pauli weight using a canonical stabilizer basis."""
    current = v.copy()
    while True:
        current_weight = _pauli_weight(current)
        best: np.ndarray | None = None
        best_key: tuple[int, str] | None = None
        for row in stabilizers:
            candidate = current ^ row
            weight = _pauli_weight(candidate)
            if weight >= current_weight:
                continue
            key = (weight, Pauli.from_symplectic(candidate).to_str())
            if best_key is None or key < best_key:
                best = candidate
                best_key = key
        if best is None:
            return current
        current = best


def _random_noncss_upper_bound(
    cm: CheckMatrix,
    *,
    iters: int,
    seed: int,
) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    n = cm.n
    stabilizers = _independent_rows(cm.stab)
    commutation = np.hstack([cm.stab[:, n:], cm.stab[:, :n]])
    centralizer = gf2.nullspace(commutation)
    logical_basis = _quotient_complement(centralizer, stabilizers)
    if logical_basis.shape[0] == 0:
        raise DistanceUnverifiable("non-CSS code encodes no logical qubits")

    best: np.ndarray | None = None
    best_key: tuple[int, str] | None = None
    stabilizer_rank = stabilizers.shape[0]
    for trial in range(iters):
        logical_coefficients = _logical_coefficients(
            trial,
            logical_basis.shape[0],
            rng,
        )
        representative = (logical_coefficients @ logical_basis) % 2
        if stabilizer_rank:
            stabilizer_coefficients = rng.integers(
                0,
                2,
                stabilizer_rank,
                dtype=np.uint8,
            )
            representative ^= (stabilizer_coefficients @ stabilizers) % 2
        representative = _steepest_reduce_pauli(representative, stabilizers)
        pauli = Pauli.from_symplectic(representative)
        key = (pauli.weight(), pauli.to_str())
        if best_key is None or key < best_key:
            best = representative.copy()
            best_key = key

    if best is None or best_key is None:  # guarded by iters >= 1
        raise DistanceUnverifiable("non-CSS random search found no logical")
    if np.any((commutation @ best) % 2) or gf2.in_rowspace(best, cm.stab):
        raise RuntimeError("non-CSS distance search produced an invalid witness")

    return {
        "value": best_key[0],
        "method": "rand-noncss-logical-coset-v2",
        "iters": iters,
        "seed": seed,
        "witness": {
            "format": "sign-free-pauli-v1",
            "pauli": best_key[1],
        },
        "method_metadata": {
            "guarantee": "logical-witness-upper-bound-only",
            "optimality": "not-certified",
            "logical_sampling": "basis-warm-start-then-uniform-nonzero-v1",
            "coset_sampling": "uniform-stabilizer-offset-v1",
            "reduction": "rref-steepest-descent-v1",
            "rng": "numpy-pcg64",
        },
    }


def _random_subsystem_upper_bound(
    cm: CheckMatrix,
    *,
    iters: int,
    seed: int,
) -> dict:
    rng = np.random.Generator(np.random.PCG64(seed))
    logical_basis = dressed_logical_quotient_basis(cm)
    if logical_basis.shape[0] == 0:
        raise DistanceUnverifiable(
            "subsystem code encodes no logical qubits",
            code="distance.subsystem_no_logical",
        )
    gauge = subsystem_gauge_basis(cm)

    best: np.ndarray | None = None
    best_key: tuple[int, str] | None = None
    gauge_rank = gauge.shape[0]
    for trial in range(iters):
        logical_coefficients = _logical_coefficients(
            trial,
            logical_basis.shape[0],
            rng,
        )
        representative = (logical_coefficients @ logical_basis) % 2
        if gauge_rank:
            gauge_coefficients = rng.integers(
                0,
                2,
                gauge_rank,
                dtype=np.uint8,
            )
            representative ^= (gauge_coefficients @ gauge) % 2
        representative = _steepest_reduce_pauli(representative, gauge)
        pauli = Pauli.from_symplectic(representative)
        key = (pauli.weight(), pauli.to_str())
        if best_key is None or key < best_key:
            best = representative.copy()
            best_key = key

    if best is None or best_key is None:  # guarded by iters >= 1
        raise DistanceUnverifiable(
            "subsystem random search found no dressed logical",
            code="distance.subsystem_search_empty",
        )
    try:
        witness = validate_dressed_logical_witness(
            cm,
            Pauli.from_symplectic(best),
        )
    except LogicalWitnessError as error:
        raise RuntimeError(
            f"subsystem distance search produced an invalid witness ({error.code})"
        ) from error
    if witness.weight() != best_key[0]:
        raise RuntimeError("subsystem distance search reported the wrong witness weight")

    return {
        "value": best_key[0],
        "method": SUBSYSTEM_RANDOM_METHOD,
        "iters": iters,
        "seed": seed,
        "witness": {
            "format": "sign-free-pauli-v1",
            "pauli": best_key[1],
            "equivalence": "mod-gauge-v1",
        },
        "method_metadata": {
            "guarantee": "dressed-logical-witness-upper-bound-only",
            "optimality": "not-certified",
            "semantics": "stabilizer-centralizer-mod-gauge-v1",
            "logical_sampling": "basis-warm-start-then-uniform-nonzero-v1",
            "coset_sampling": "uniform-gauge-offset-v1",
            "reduction": "rref-gauge-steepest-descent-v1",
            "rng": "numpy-pcg64",
        },
    }


def random_upper_bound(
    cm: CheckMatrix,
    iters: int = 2000,
    seed: int = 0,
    *,
    method: str | None = None,
) -> dict:
    if isinstance(iters, (bool, np.bool_)) or not isinstance(
        iters,
        (int, np.integer),
    ):
        raise ValueError("iters must be an integer at least 1")
    iters = int(iters)
    if iters < 1:
        raise ValueError("iters must be at least 1")
    if isinstance(seed, (bool, np.bool_)) or not isinstance(
        seed,
        (int, np.integer),
    ):
        raise ValueError("seed must be a non-negative integer")
    seed = int(seed)
    if seed < 0:
        raise ValueError("seed must be a non-negative integer")
    if cm.gauge is not None:
        if method != SUBSYSTEM_RANDOM_METHOD:
            raise DistanceUnverifiable(
                "subsystem bounded search requires an explicit dressed-distance method",
                code="distance.subsystem_method_required",
                context={"required_method": SUBSYSTEM_RANDOM_METHOD},
            )
        return _random_subsystem_upper_bound(cm, iters=iters, seed=seed)
    if not cm.is_css():
        return _random_noncss_upper_bound(cm, iters=iters, seed=seed)

    rng = np.random.default_rng(seed)
    best: int | None = None
    HX, HZ = cm.to_css()
    for H_same, H_other in ((HX, HZ), (HZ, HX)):
        N = gf2.nullspace(H_other)
        if N.shape[0] == 0:
            continue
        for _ in range(iters):
            c = rng.integers(0, 2, N.shape[0], dtype=np.uint8)
            v = (c @ N) % 2
            if not v.any() or gf2.in_rowspace(v, H_same):
                continue
            v = _greedy_reduce(v.astype(np.uint8), H_same)
            best = int(v.sum()) if best is None else min(best, int(v.sum()))
    if best is None:
        raise DistanceUnverifiable("random search found no logical; k = 0?")
    return {"value": int(best), "method": "rand-lowweight-v1", "iters": iters, "seed": seed}
