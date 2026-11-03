# Pauli operators as binary symplectic vectors

## Essence

Ignore a Pauli operator's global phase and record, for each qubit, whether an
`X` component and a `Z` component are present. The operator becomes

\[
P \longleftrightarrow [x\mid z]\in \mathbb F_2^{2n},
\qquad
I=(0,0),\;X=(1,0),\;Z=(0,1),\;Y=(1,1).
\]

The order is fixed: all `x` bits in increasing qubit order, then all `z`
bits. There is no hidden phase field. This convention is the exact
`phase-free-x-then-z-bits-v1` interface used by the machine proof.

Two phase-free Paulis commute precisely when

\[
\langle[x\mid z],[x'\mid z']\rangle_s
=x\cdot z'+z\cdot x'=0\pmod 2.
\]

That formula is not a mnemonic. It counts, modulo two, the qubits where the
local factors anticommute.

## Why the parity is the whole commutation test

At one qubit, `X` anticommutes with `Z`; the same is true for the pairs
`X,Y` and `Y,Z`. In binary coordinates, the local indicator is

\[
x_i z'_i+z_i x'_i \pmod 2.
\]

Check the four possibilities for each operand's `(x_i,z_i)` pair: the
indicator is one exactly for the six ordered pairs of distinct nonidentity
Paulis that anticommute, and zero otherwise. Tensor factors on different
qubits commute past each other. Moving the entire left Pauli past the right
one therefore contributes one minus sign per locally anticommuting overlap.
The global sign is positive exactly when their number is even, which is the
vanishing symplectic sum above.

This derivation also explains why global phase is safely omitted here. A phase
multiplies the complete operator by a scalar, so it does not change which
local swaps contribute minus signs. Phase matters for representing the full
Pauli group; it does not change this commutation predicate.

## Three pictures of the same calculation

### Bit-string picture

For `XX` and `ZZ`, the serialized rows are

\[
[1,1\mid0,0],\qquad[0,0\mid1,1].
\]

Each qubit contributes one, so the sum is zero in \(\mathbb F_2\): the two
minus signs cancel and the operators commute. For `X_` and `Z_`, only the
first qubit contributes, so the sum is one and the operators anticommute.

These are the two frozen fixtures. Their expectations are recomputed by
`qeclib.pauli.Pauli.commutes` and by Lean rather than copied as claimed data.

### Crossing-count picture

Draw an `X` mark from the first operator and a `Z` mark from the second at each
shared qubit; draw the reverse `Z`–`X` marks as well. Every crossing means one
local anticommutation. The symplectic inner product is simply the parity of
those crossings. This picture makes the two terms \(x\cdot z'\) and
\(z\cdot x'\) visible.

### Matrix picture

With column vectors \(v=[x\mid z]^T\) and \(w=[x'\mid z']^T\), define

\[
\Lambda=\begin{pmatrix}0&I\\I&0\end{pmatrix}.
\]

Then \(\langle v,w\rangle_s=v^T\Lambda w\). A collection of stabilizer rows
is mutually commuting exactly when its binary check matrix \(H\) satisfies
\(H\Lambda H^T=0\). The pairwise parity rule and the matrix criterion are the
same statement at different scales.

## What the Lean bridge proves

The bridge is deliberately small. It imports only
`QEC.Stabilizer.Foundations.BinarySymplectic.SymplecticInner` from the exact
pinned QECLean checkout and defines a total translation from any two Boolean
functions `x z : Fin n → Bool` to QECLean's phase-zero Pauli group element.

Its first theorem expands the QECLean symplectic sum term by term and proves
that it equals the Atlas sum above. Its second theorem rewrites QECLean's named
`commutes_iff_symplectic_inner_zero` theorem through that equality. Thus the
machine-checked chain is

\[
\text{Atlas bits}
\rightarrow\text{QECLean Pauli}
\rightarrow\text{QECLean symplectic product}
\rightarrow\text{commutation}.
\]

The proof then evaluates both frozen fixtures and prints every theorem's axiom
dependencies. Accepted output may use only `propext`, `Classical.choice`, and
`Quot.sound`; `sorry`, `sorryAx`, `Lean.ofReduceBool`, and `native_decide` are
refused. The committed manifest is verified offline during `make verify`.
Re-running Lean itself is opt-in because it requires the exact pinned external
toolchain and dependency checkout.

The machine result has origin
`{kind: verified, method: v9-production-focused-qeclean-replay}`. Its resource
limits have origin
`{kind: bounded, method: human-owner-authorized-t139-v8-envelope-2026-08-15}`.

## What this proof does not claim

This bridge proves the representation and commutation seam only. It does not
formalize a stabilizer code, CSS construction, distance, decoder, threshold,
or any Atlas code instance. It also does not close the broader Lean Wanted
item. Those gaps stay explicit because a trustworthy narrow theorem is more
useful than an umbrella claim whose assumptions and trust boundary are hard to
audit.

## Litmus questions

- Given `[x|z]`, can you recover the local Pauli at every qubit without a phase
  convention left unspecified?
- Can you point to the two local anticommutations that make `XX` commute with
  `ZZ`?
- Can you explain why a single `X_`–`Z_` overlap changes the parity?
- Can you derive `HΛHᵀ=0` by applying the pairwise rule to every row pair?
- Can you state exactly where the checked bridge stops before making a claim
  about stabilizer codes or distance?
