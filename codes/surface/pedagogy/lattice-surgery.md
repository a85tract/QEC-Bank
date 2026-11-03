# A seam of local checks measures logical parity

> **Claim.** A smooth lattice-surgery merge measures `Z_L⊗Z_L` because the
> product of its new local Z-checks telescopes to that logical operator.

The dual rough merge measures `X_L⊗X_L`.

## 1. The `L=3` geometry

Place two unrotated distance-three patches side by side. Patch A occupies
`x=0,...,4`, patch B occupies `x=6,...,10`, and the missing seam is `x=5`.
Add the two horizontal seam data qubits at `(5,1)` and `(5,3)`, initialized
in `|+⟩`.

The old boundary X-stars extend across the seam. Their new X support has a
known `+1` contribution from the `|+⟩` seam qubits. Measure three new
Z-plaquettes centered at `(5,0)`, `(5,2)`, and `(5,4)`.

Multiplying those three outcomes cancels the two seam-qubit Z operators:
each appears in two neighboring plaquettes. What remains is

```text
Z(4,0) Z(4,2) Z(4,4) · Z(6,0) Z(6,2) Z(6,4),
```

the right-column representative of patch A's `Z_L` times the left-column
representative of patch B's `Z_L`. The product of local seam checks is
therefore the joint logical parity.

This is the content of lattice surgery: topology turns a nonlocal observable
into a product of simultaneously measured local checks
([Horsman et al.](https://arxiv.org/abs/1111.4022)).

## 2. Dimension and spacelike distance

Before the merge, the two patches have `26` data qubits and encode two
logical qubits. The two seam qubits give `n=28`. There are `27` independent
checks after the merge, so `k=1`: measuring one joint logical parity removes
one logical degree of freedom.

The merged patch is the rectangular product
`HGP(rep_3, rep_6)`. `reproduce.py` asks the engine for its exact parameters
and obtains

```text
n=28, k=1, independent checks=27, d=3
```

The long horizontal logical grows, while the short vertical logical remains
length three. Thus the merge preserves the original spacelike distance; it
does not magically turn the rectangle into distance six.

## 3. Why `d` rounds are needed

If the only possible fault were an independent flip of the inferred seam
parity in each round, repeating the parity and majority-voting would be a
one-dimensional repetition code in time.

That toy reduction is not the full fault-tolerance argument. Real extraction
circuits also contain data faults, ancilla propagation, and faults crossing
the start or end of the merge. They create correlated detection events in
space and time, and can change which representative of the joint logical
observable is being tracked. The merge syndrome must therefore be decoded as
one spacetime history. Running order `d` rounds supplies timelike distance;
the decoder, not a bare majority rule, combines seam and bulk detectors to
infer the logical parity.

## 4. Split and CNOT

To split, stop the seam checks and measure the seam data qubits in X. The
outcomes update the Pauli frame and restore two encoded patches.

A logical CNOT uses an ancilla patch prepared in `|+⟩`:

1. measure `Z_L^C Z_L^A`;
2. measure `X_L^A X_L^T`;
3. measure the ancilla logical Z;
4. classically track the outcome-dependent Pauli corrections.

Each joint measurement is the telescoping construction above, with X and Z
exchanged for the dual merge. The operation is Clifford and remains inside
the stabilizer formalism throughout.
