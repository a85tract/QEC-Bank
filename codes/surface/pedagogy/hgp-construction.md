# HGP(rep_L, rep_L) is the unrotated planar surface code

> **Claim.** The shipped constructor produces local CSS checks on
> `n=L²+(L−1)²` qubits and encodes exactly one logical qubit.

Distance is intentionally deferred to
[its own proof](distance-proof.md). This page establishes the object and its
dimension.

## 1. The classical factor

Let `H=rep_parity(L)` be the `(L−1) × L` binary matrix

```text
1 1 0 0 ...
0 1 1 0 ...
      ...
... 0 1 1
```

Its rows are independent: beginning at the left edge, column zero occurs only
in row zero, so a zero linear combination forces the first coefficient to
vanish; repeating column by column forces every coefficient to vanish.
Therefore

`rank(H)=L−1`, `dim ker(H)=1`, and `dim ker(Hᵀ)=0`.

The one vector in `ker(H)` is the all-ones repetition word. The zero
transpose dimension is the algebraic signature of an open chain.

## 2. The quantum product

For two copies of `H`, the hypergraph product puts qubits in two blocks:

- bit×bit: `L²` qubits;
- check×check: `(L−1)²` qubits.

It defines

```text
H_X = [ H ⊗ I_L       | I_(L−1) ⊗ Hᵀ ]
H_Z = [ I_L ⊗ H       | Hᵀ ⊗ I_(L−1) ]
```

The CSS commutator has one contribution from each block:

```text
(H ⊗ I)(I ⊗ H)ᵀ       = H ⊗ Hᵀ
(I ⊗ Hᵀ)(Hᵀ ⊗ I)ᵀ     = H ⊗ Hᵀ
```

Their sum is zero over `F₂`. Block two is not decorative: it supplies the
second copy of the would-be commutation defect.

At `L=3`, the matrices asserted by the shipped computation are

```text
H_X =
100100000 | 1000
010010000 | 1100
001001000 | 0100
000100100 | 0010
000010010 | 0011
000001001 | 0001

H_Z =
110000000 | 1000
011000000 | 0100
000110000 | 1010
000011000 | 0101
000000110 | 0010
000000011 | 0001
```

Before reduction modulo two, every entry of `H_X H_Zᵀ` is either zero or two.
After reduction, all entries vanish.

## 3. Why the checks are geometrically local

Use the constructor's coordinates:

- bit×bit qubit `(a,b)` is at `(2b,2a)`;
- check×check qubit `(a,b)` is at `(2b+1,2a+1)`;
- X-check `(a,b)` is at `(2b,2a+1)`;
- Z-check `(a,b)` is at `(2b+1,2a)`.

Every `1` in a check row then joins sites at Manhattan distance exactly one.
Interior checks see four neighbors. At the left/right or top/bottom edge one
neighbor is absent, leaving weight three. `reproduce.py` checks this
adjacency for every shipped size, not only for the drawn `L=3` patch.

The `L=3` interleaved lattice is

```text
y=4  q6   Z4   q7   Z5   q8
y=3  X3   q11  X4   q12  X5
y=2  q3   Z2   q4   Z3   q5
y=1  X0   q9   X1   q10  X2
y=0  q0   Z0   q1   Z1   q2
```

Weight-three Z-checks lie on the top and bottom rough boundaries.
Weight-three X-checks lie on the left and right smooth boundaries.

## 4. Why `k=1`

There are `L(L−1)` rows in each quantum check matrix. The HGP rank identity
gives

```text
rank(H_X)
  = rank(H)L + (L−1)rank(H) − rank(H)²
  = L(L−1),
```

and the same for `H_Z`. Hence

```text
k = [L²+(L−1)²] − 2L(L−1) = 1.
```

Equivalently, the HGP dimension formula gives

```text
k_Q = k₁k₂ + k₁ᵀk₂ᵀ = 1·1 + 0·0 = 1.
```

If each open chain is closed into an `L`-edge cycle, the added parity row is
dependent. The ordinary kernel remains one-dimensional and the transpose
kernel becomes one-dimensional, giving `1·1+1·1=2`: the toric code.

## 5. Recompute it

```bash
source .venv/bin/activate
python atlas/surface/pedagogy/reproduce.py
```

The script asserts the matrix formulas, integer `{0,2}` cancellation,
nearest-neighbor geometry, and ranks for `L=3,4,5`.
