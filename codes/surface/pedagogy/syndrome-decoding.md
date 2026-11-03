# Syndrome is the boundary of an error chain

> **Claim.** For a surface-code Pauli error chain `E`, the fired checks are
> exactly its boundary `∂E`. A correction succeeds precisely when error plus
> correction is a trivial relative cycle.

This single statement explains defect pairs, boundary nodes, matching, and
logical failure.

## 1. Algebra

Represent an X-error support by a binary vector `e_X`. The fired Z-checks are

`H_Z e_X`.

Each interior check sees the parity of incident error edges. Along a chain,
two incident segments cancel modulo two; only endpoints remain. The dual
statement sends a Z-error vector to `H_X e_Z`.

At a condensing boundary, a chain can end without a second physical check.
In a decoder graph this is represented by pairing the remaining defect to a
boundary node.

## 2. Computed `L=3` walk

The shipped constructor labels the central data qubit `q4` and a middle-row
crossing by `q3,q4,q5`. Direct matrix multiplication gives

```text
single X on q4          -> Z-checks {Z2, Z3}
single Z on q4          -> X-checks {X1, X4}
single X on left q3     -> Z-check  {Z2}
X on {q3,q4}            -> Z-check  {Z3}
X on {q3,q4,q5}         -> no fired checks
```

The last support is outside the X-stabilizer row space, so “no syndrome” means
a logical X, not a stabilizer. The sequence shows one defect entering at the
smooth boundary, walking across the patch, and disappearing at the opposite
smooth boundary.

## 3. What the decoder decides

Given a syndrome `s`, every candidate correction `C` satisfies
`∂C=s`. If the actual error is `E`, then

`∂(E+C)=s+s=0`.

Thus `E+C` is a cycle. Recovery succeeds if that cycle is a stabilizer
boundary and fails if it is a nontrivial relative homology class.

Minimum-weight matching chooses low-cost pairings of syndrome endpoints.
Maximum-likelihood decoding instead sums probabilities over all chains in
each logical class. That distinction is why path degeneracy can separate the
matching and optimal code-capacity thresholds; the exact model-dependent
numbers live in the [threshold ledger](threshold-ledger.md).

## 4. Repeated measurements

With noisy measurements, a detector compares the same check outcome in
successive rounds. Data faults create spacelike-separated detector events;
measurement faults create timelike-separated events; circuit propagation can
create correlated small patterns. Decoding therefore takes place in a
`2+1`-dimensional detector graph.

A relevant single fault has a bounded detector footprint, but not every
physical fault must light a detector: a late fault can be observationally
equivalent to a fault in the next round, a harmless Pauli can cancel, and
some faults affect only a tracked observable. The correct invariant is that
the detector error model lists the observable detector/logic signature of
each fault mechanism.

Ancilla faults deserve special attention. During a four-neighbor check
measurement, one ancilla Pauli can propagate through later CNOTs into a
two-data-qubit hook. A schedule that aligns those hooks with a shortest
logical direction can reduce circuit distance even though the static check
matrix still has distance `d`. Static-code distance and fault distance are
different claims and must be verified separately.
