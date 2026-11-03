# Gauge group, center, and subsystem qubit count

This page derives the static rectangular presentation exported by
`constructor.py`. It uses sign-free Pauli algebra; phases do not enter any
rank or commutation statement.

## Coordinate and Pauli convention

Let rows be indexed by `i=0,...,r-1` and columns by `j=0,...,c-1`. The
row-major qubit index is

$$q(i,j)=ic+j.$$

The local gauge generators are

$$g^X_{i,j}=X_{i,j}X_{i+1,j},\qquad
0\le i<r-1,\ 0\le j<c,$$

and

$$g^Z_{i,j}=Z_{i,j}Z_{i,j+1},\qquad
0\le i<r,\ 0\le j<c-1.$$

Thus X edges are vertical and Z edges are horizontal. The convention is
deliberate: it makes a bare X logical span a row and a bare Z logical span a
column. Transposing the grid and exchanging X/Z is equivalent, but it swaps
the sector labels used below.

## Why the gauge group is nonabelian

Two generators of the same Pauli type commute. A vertical X edge and a
horizontal Z edge anticommute exactly when they share one endpoint. For the
`3 × 3` constructor order,

`g^X_{0,0}=X_0X_3`

and

`g^Z_{0,0}=Z_0Z_1`

share only `q0`, so their symplectic product is one. The tour highlights this
pair as gauge items zero and six. This is why the individual pair outcomes
cannot all be stabilizer eigenvalues.

## Constructing the center

For each adjacent row pair, multiply every vertical X edge across the columns:

$$S^X_i=\prod_{j=0}^{c-1}g^X_{i,j}
=\prod_{j=0}^{c-1}X_{i,j}X_{i+1,j}.$$

For each adjacent column pair, multiply every horizontal Z edge across the
rows:

$$S^Z_j=\prod_{i=0}^{r-1}g^Z_{i,j}
=\prod_{i=0}^{r-1}Z_{i,j}Z_{i,j+1}.$$

An X strip and a Z strip overlap on the four corners of their `2 × 2`
intersection, so they commute. More strongly, an X strip meets an individual
horizontal Z edge on zero or two sites, and a Z strip meets an individual
vertical X edge on zero or two sites. Every strip therefore commutes with the
entire gauge group, not merely with the other strips.

The constructor checks both statements:

- `CheckMatrix.validate()` rejects any stabilizer/gauge anticommutation;
- `rank([G;S])=rank(G)` proves that every declared center row lies in the
  generated gauge span.

## Rank ledger

Within one column, the vertical X supports are the `r-1` rows of the open
length-`r` repetition parity matrix. They are independent. Different columns
have disjoint supports, so

$$rank(G_X)=c(r-1).$$

Similarly, the horizontal Z supports form an independent length-`c` open
chain inside each row:

$$rank(G_Z)=r(c-1).$$

X-only and Z-only symplectic rows occupy different binary halves, so their
ranks add:

$$rank(G)=c(r-1)+r(c-1)=2rc-r-c.$$

The X center contains `r-1` independent adjacent-row strips; the Z center
contains `c-1` independent adjacent-column strips. Hence

$$rank(S)=r+c-2.$$

For a subsystem code with gauge group `G` and center stabilizer group `S`, the
protected and gauge dimensions are

$$k=n-\frac{rank(G)+rank(S)}{2},\qquad
g=\frac{rank(G)-rank(S)}{2}.$$

Substituting `n=rc` gives

$$k=1,\qquad g=rc-r-c+1=(r-1)(c-1).$$

The three shipped instances therefore have the following independently
recomputed ledger:

| rectangle | `rank(S)` | `rank(G)` | protected `k` | gauge `g` |
|---|---:|---:|---:|---:|
| `2 × 2` | 2 | 4 | 1 | 1 |
| `3 × 3` | 4 | 12 | 1 | 4 |
| `3 × 5` | 6 | 22 | 1 | 8 |

The structured gauge-count claims cite the subsystem literature because the
ordinary entry verifier exposes `k` but does not emit gauge-qubit claims.
`reproduce.py` checks every table cell without changing that provenance class.

## Bare protected Pauli algebra

Choose

$$\bar X_b=\prod_{j=0}^{c-1}X_{0,j},\qquad
\bar Z_b=\prod_{i=0}^{r-1}Z_{i,0}.$$

The subscript `b` means *bare*: each operator commutes with the full gauge
group. `\bar X_b` meets each horizontal Z edge in its row twice, and
`\bar Z_b` meets each vertical X edge in its column twice. They meet each
other once at `q(0,0)`, so they anticommute and generate one protected Pauli
pair.

A complete X row at height `i` differs from the row at `i+1` by `S^X_i`.
Likewise, neighboring complete Z columns differ by `S^Z_j`. Parallel bare
representatives therefore differ by center elements, which are also gauge
elements.

This bare pair proves a protected qubit exists, but it is not yet the distance
proof. Distance permits multiplication by noncentral gauge operators and thus
minimizes over dressed representatives; that quotient is derived on the
[distance page](dressed-distance-and-decoding.md).

## What the calculation does not establish

- It does not specify a measurement schedule. Noncommuting pair generators
  require time ordering and a detector convention.
- It does not turn the long center strips into local stabilizers. Only their
  measurement factors are local.
- It does not prove a scalable distance theorem merely because the shared
  Atlas referee exactly enumerates the shipped small instances. Certified
  lower bounds beyond the exact-search ceiling and equivalence-safe changes
  of subsystem presentation remain routed to
  `wanted:subsystem-dressed-distance`.
- It does not make the compass Hamiltonian self-correcting or topological.
  Hamiltonian protection is a dynamics claim with separate evidence.
