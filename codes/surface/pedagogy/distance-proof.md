# The unrotated planar family has distance d=L

> **Theorem.** For the code `HGP(rep_L, rep_L)` with `L≥2`, every nontrivial
> logical Pauli has weight at least `L`, and weight-`L` X and Z logicals
> exist.

The proof does not infer distance from a drawing or from small-instance
enumeration.

## 1. Upper bound

Index the `L²` bit×bit block by `(a,b)`, `0≤a,b<L`.

- For fixed `a`, put X on all `(a,b)`. Each Z-check meets this row zero or two
  times, so the string commutes with every Z-check.
- For fixed `b`, put Z on all `(a,b)`. Each X-check likewise meets this column
  zero or two times.

A row and a column intersect once, so the two strings anticommute. Neither can
be a stabilizer. Both have weight `L`, proving `d≤L`.

## 2. Equivalent disjoint representatives

There are `L` row strings and `L` column strings. Adjacent X rows differ by
the product of the X-checks in the strip between them: interior qubits cancel
in pairs, leaving precisely the two boundary rows. Therefore all X rows
represent the same logical class. The same strip argument using Z-checks
makes all Z columns equivalent.

Within each family the supports are pairwise disjoint.

## 3. Lower bound

Because `k=1`, every nontrivial logical class is represented by
`X_L^a Z_L^b` with `(a,b)≠(0,0)`.

If a logical `P` anticommutes with the Z class, it anticommutes with every
equivalent Z-column representative: multiplying a representative by a
stabilizer cannot change its commutator with a logical. Anticommutation with a
pure-Z column requires `P` to have X or Y support somewhere on that column.
There are `L` disjoint columns, so `wt(P)≥L`.

If `P` instead anticommutes with the X class, the same argument uses the `L`
disjoint rows. Every nontrivial logical anticommutes with at least one of the
two conjugate classes, so every nontrivial logical has weight at least `L`.
Together with the upper bound, `d=L`.

This argument is the finite-patch version of a systolic proof: the disjoint
representatives form `L` independent cuts that every conjugate crossing must
meet.

## 4. Machine witnesses

At `L=3`, `reproduce.py` asserts the following facts:

```text
X rows logical/equivalent/disjoint: True
Z columns logical/equivalent/disjoint: True
logical X support: [0, 1, 2]
logical Z support: [0, 3, 6]
exact_distance(L=3): 3 (exact-css-enum)
```

At `L=4`, exhaustive CSS logical enumeration returns four. These are
`verified` claims in `instances.yaml`.

At `L=5`, exhaustive enumeration is not part of the verifier. The analytic
lower bound and
[Dennis–Kitaev–Landahl–Preskill](https://arxiv.org/abs/quant-ph/0110143)
support `d≥5`; a deterministic low-weight search with
`method=rand-lowweight-v1`, `seed=0`, and `iters=2000` finds a weight-five
logical. The claim is therefore stored as

```yaml
property: d
lower: {value: 5}
upper: {value: 5, method: rand-lowweight-v1, seed: 0, iters: 2000}
origin: {kind: bounded, ref: dennis2002topological}
```

The word `bounded` is intentional: the theorem supplies the lower bound and
the verifier reruns the upper-bound witness, but the pipeline does not call
the result exhaustive.
