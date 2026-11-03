# From plaquette coloring to a periodic ISG

This page derives the exact finite object built by `constructor.py`. It does
not use the instantaneous toric-code equivalence as a substitute for the
schedule algebra.

## Two labels on every edge

Index the two vertices of cell `(i,j)` by

`A(i,j) = 2(i L2 + j)` and `B(i,j) = A(i,j) + 1`,

with both coordinates reduced periodically. The constructor uses

- `z`: `A(i,j)--B(i,j)`,
- `x`: `B(i,j)--A(i+1,j)`,
- `y`: `B(i,j)--A(i,j+1)`.

Direction fixes the measured operator: `ZZ`, `XX`, or `YY`. This is the first
edge label.

The hexagons are properly colored by `0,1,2`. If an edge separates faces with
colors `a` and `b`, its round label is the missing color

`r = 3 - a - b`.

This is the second edge label. It is transverse to direction: on the shipped
`3 x 3` torus, each round contains three `XX`, three `YY`, and three `ZZ`
measurements.

## Why every round is a perfect matching

At a honeycomb vertex, the three incident edges separate the three pairs of
neighboring face colors: `{0,1}`, `{1,2}`, and `{2,0}`. Their missing colors
are respectively `2`, `0`, and `1`. Exactly one incident edge therefore
belongs to each round.

Consequently, edges with one round label are disjoint and cover every vertex.
Their two-qubit Pauli measurements commute because they have disjoint support.
For `n = 2 L1 L2`, every round contains `n/2 = L1 L2` measurements. The
constructor turns this proof obligation into a hard check by sorting all
round supports and requiring the list `0,...,n-1` exactly once.

## The rank-eight plaquette backbone

For a face `p`, multiply the directional Pauli operator on each of its six
boundary edges. Two different letters meet at every vertex. Their product,
up to a phase omitted by the Atlas sign-free representation, is the third
Pauli letter. The resulting `W_p` has weight six.

There are two commutation cases:

1. A measured boundary edge overlaps `W_p` at two endpoints. Its Pauli letter
   differs from the plaquette letter at each endpoint, so two
   anticommutations cancel.
2. A measured edge leaving the face overlaps at one vertex. Its direction is
   the direction unused by the two boundary edges, exactly the Pauli letter
   left on `W_p` at that vertex, so the local operators commute.

Thus `W_p` commutes with every edge measurement in all rounds.

For the `3 x 3` convention, the first three plaquette words are

```text
XY___ZZ___YX______
_ZXY__YXZ_________
___ZXY__YXZ_______
```

The reproduction script constructs all nine words from the six-edge face
walks. Every word has weight six, all lie in the steady snapshot row space,
and their binary rank is eight. The one dependency is the closed-torus
global product relation.

## The measurement update

Let the current commuting ISG generators be rows `g_i` and let `p` be the next
measured Pauli.

- If `p` commutes with every `g_i` and is outside their span, append it.
- If `p` is already in the span, only its outcome sign changes; the sign-free
  row space stays fixed.
- If `p` anticommutes with generators indexed by a set `A`, choose one pivot
  `g_a`. Replace every other `g_b`, `b in A`, by `g_b g_a`, which now commutes
  with `p`, and replace `g_a` by `p`.

The third rule trades one generator for one measurement rather than
increasing rank. Binary symplectic addition implements multiplication and the
symplectic inner product selects `A`. This is the exact
`ISGTracker.measure` algorithm used by the constructor.

Starting from no generators on the `3 x 3` instance, the ranks after each
complete round are

```text
9, 12, 14, 16, 16, 16,
16, 16, 16, ...
```

Once the rank reaches sixteen, the phase-specific row spaces repeat after
each three-round period. Nine current-round measurements plus eight
plaquette generators have combined rank sixteen, so their spans share one
relation. On eighteen qubits, `dynamic_k = 18 - 16 = 2`.

## The torus coloring constraint

The face-adjacency graph is triangular. In the constructor coordinates, a
valid closed formula is

`c(i,j) = i - j mod 3`.

Transport around the first periodic handle shifts `i` by `L1`; transport
around the second shifts `j` by `L2`. The color returns to itself only if both
lengths vanish modulo three. The constructor also tries the opposite
orientation and constraint propagation, then rejects a torus when no proper
coloring is found.

The reproduction script checks all `2 <= L1,L2 <= 9` face graphs and finds a
coloring exactly when both dimensions are divisible by three. This finite
scan is a regression certificate for the shipped constructor. The winding
argument supplies the reason for its accepted family.

## The direction-grouped counterexample

The most dangerous wrong constructor measures all `XX` direction edges,
then all `YY`, then all `ZZ`. Every round is still a perfect matching.
Plaquette products still commute with every measurement. Those two local
checks therefore cannot distinguish the protocol.

The long-time ISG does. On the `6 x 6` torus:

| grouping | physical qubits | steady ISG rank | `dynamic_k` |
|---|---:|---:|---:|
| plaquette missing color | 72 | 70 | 2 |
| edge direction / Pauli letter | 72 | 52 | 20 |

Every entry in this table is recomputed by `reproduce.py`. The wrong sequence
is not a small convention change; it preserves an extensive collection of
logical degrees of freedom instead of the two toric logicals.

## What this page establishes

The schedule's correctness is certified by a chain of independent invariants:
proper face coloring, perfect matchings, mixed Pauli content, commuting
plaquette products, startup rank profile, periodic rank, and a counterexample
that passes the local checks but fails the dynamical count. The literature is
needed to interpret the steady ISG as topological order; the finite algebra
above is executable and recomputed.
