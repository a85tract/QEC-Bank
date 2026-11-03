"""Logical-operator quotients and independently checked Pauli witnesses."""
from __future__ import annotations
import numpy as np
from . import gf2
from .checkmatrix import CheckMatrix
from .diagnostics import make_diagnostic
from .pauli import Pauli


class LogicalWitnessError(ValueError):
    """A logical witness or its subsystem presentation is invalid."""

    def __init__(self, message: str, *, code: str, context: dict | None = None):
        super().__init__(message)
        self.code = code
        self.context = dict(context or {})

    def diagnostic(self) -> dict:
        return make_diagnostic(self.code, str(self), context=self.context)


def _canonical_basis(rows: np.ndarray) -> np.ndarray:
    reduced, pivots = gf2.rref(rows)
    return reduced[: len(pivots)].astype(np.uint8, copy=True)


def _subsystem_spaces(cm: CheckMatrix) -> tuple[np.ndarray, np.ndarray]:
    if cm.gauge is None:
        raise LogicalWitnessError(
            "dressed logical witnesses require a subsystem gauge presentation",
            code="logicals.subsystem_required",
        )
    try:
        cm.validate()
    except ValueError as error:
        raise LogicalWitnessError(
            f"invalid subsystem presentation: {error}",
            code="logicals.subsystem_invalid",
        ) from error

    stabilizers = _canonical_basis(cm.stab)
    gauge = _canonical_basis(np.vstack([cm.stab, cm.gauge]))
    stabilizer_rank = stabilizers.shape[0]
    gauge_rank = gauge.shape[0]
    if (stabilizer_rank + gauge_rank) % 2:
        raise LogicalWitnessError(
            "invalid subsystem presentation: stabilizer and gauge ranks have odd sum",
            code="logicals.subsystem_invalid",
            context={
                "stabilizer_rank": stabilizer_rank,
                "gauge_rank": gauge_rank,
            },
        )
    quotient_dimension = 2 * cm.n - stabilizer_rank - gauge_rank
    if quotient_dimension != 2 * cm.k:
        raise LogicalWitnessError(
            "invalid subsystem presentation: dressed quotient dimension disagrees with k",
            code="logicals.subsystem_invalid",
            context={
                "quotient_dimension": quotient_dimension,
                "expected_dimension": 2 * cm.k,
            },
        )
    return stabilizers, gauge


def subsystem_gauge_basis(cm: CheckMatrix) -> np.ndarray:
    """Return a canonical basis of the full gauge group, including its center."""
    _, gauge = _subsystem_spaces(cm)
    return gauge


def dressed_logical_quotient_basis(cm: CheckMatrix) -> np.ndarray:
    """Return canonical representatives spanning ``C(S) / G`` as rows."""
    stabilizers, gauge = _subsystem_spaces(cm)
    n = cm.n
    commutation = np.hstack([stabilizers[:, n:], stabilizers[:, :n]])
    centralizer = gf2.nullspace(commutation)

    pivots = [int(np.flatnonzero(row)[0]) for row in gauge]
    residuals: list[np.ndarray] = []
    for row in centralizer:
        residual = row.copy()
        for basis_row, pivot in zip(gauge, pivots):
            if residual[pivot]:
                residual ^= basis_row
        if residual.any():
            residuals.append(residual)
    if residuals:
        quotient = _canonical_basis(np.asarray(residuals, dtype=np.uint8))
    else:
        quotient = np.zeros((0, 2 * n), dtype=np.uint8)

    if quotient.shape[0] != 2 * cm.k:
        raise LogicalWitnessError(
            "invalid subsystem presentation: could not construct the dressed quotient",
            code="logicals.subsystem_invalid",
            context={
                "quotient_basis_rows": quotient.shape[0],
                "expected_rows": 2 * cm.k,
            },
        )
    return quotient


def validate_dressed_logical_witness(
    cm: CheckMatrix,
    witness: str | Pauli,
) -> Pauli:
    """Validate one sign-free representative of a nonzero class in ``C(S) / G``."""
    stabilizers, gauge = _subsystem_spaces(cm)
    if isinstance(witness, str):
        try:
            pauli = Pauli.from_str(witness)
        except ValueError as error:
            raise LogicalWitnessError(
                f"invalid dressed logical witness: {error}",
                code="logicals.witness_format",
            ) from error
    elif isinstance(witness, Pauli):
        pauli = witness
    else:
        raise LogicalWitnessError(
            "dressed logical witness must be a Pauli or sign-free Pauli string",
            code="logicals.witness_format",
            context={"witness_type": type(witness).__name__},
        )

    if pauli.n != cm.n:
        raise LogicalWitnessError(
            f"dressed logical witness has width {pauli.n}; expected {cm.n}",
            code="logicals.witness_width",
            context={"actual_qubits": pauli.n, "expected_qubits": cm.n},
        )

    vector = pauli.symplectic()
    n = cm.n
    commutation = np.hstack([stabilizers[:, n:], stabilizers[:, :n]])
    if np.any((commutation @ vector) % 2):
        raise LogicalWitnessError(
            "dressed logical witness does not commute with the stabilizer",
            code="logicals.witness_noncommuting",
        )
    if gf2.in_rowspace(vector, gauge):
        raise LogicalWitnessError(
            "dressed logical witness is trivial modulo the gauge group",
            code="logicals.witness_gauge_trivial",
        )
    return pauli

def _sympl(u: np.ndarray, v: np.ndarray) -> int:
    n = u.size // 2
    return int((u[:n] @ v[n:] + u[n:] @ v[:n]) % 2)

def logical_basis(cm: CheckMatrix) -> list[tuple[Pauli, Pauli]]:
    if cm.gauge is not None:
        raise NotImplementedError("bare/dressed logicals for subsystem codes: Part 2")
    n = cm.n
    S = cm.stab
    # Centralizer = nullspace of S·Omega (swap the halves of S's rows).
    M = np.hstack([S[:, n:], S[:, :n]])
    C = gf2.nullspace(M)
    # Quotient out the stabilizer rowspace: keep 2k independent coset reps.
    reps: list[np.ndarray] = []
    base = S.copy()
    for v in C:
        if not gf2.in_rowspace(v, base):
            reps.append(v.copy())
            base = np.vstack([base, v])
    if len(reps) != 2 * cm.k:
        raise RuntimeError(f"expected {2*cm.k} logical reps, got {len(reps)}")
    # Symplectic Gram-Schmidt into (Lx, Lz) pairs.
    pairs: list[tuple[Pauli, Pauli]] = []
    while reps:
        a = reps.pop(0)
        j = next((i for i, b in enumerate(reps) if _sympl(a, b) == 1), None)
        if j is None:
            raise RuntimeError("no symplectic partner found (degenerate basis)")
        b = reps.pop(j)
        reps = [(r + _sympl(r, b) * a + _sympl(r, a) * b) % 2 for r in reps]
        reps = [r.astype(np.uint8) for r in reps]
        pairs.append((Pauli.from_symplectic(a), Pauli.from_symplectic(b)))
    return pairs
