# Dressed distance and the two repetition decoders

The same parity quotient proves both the sector distances and the
perfect-gauge-readout decoder. This page fixes the meaning of "modulo gauge"
before using a repetition analogy.

## X-type dressed operators

Represent an X-type Pauli by a binary `r × c` support matrix `A`. Multiplying
by a vertical X gauge edge flips two adjacent entries in one column. Such
moves preserve the column-parity vector

$$p_j=\sum_{i=0}^{r-1}A_{i,j}\pmod 2.$$

Conversely, adjacent-pair moves generate every even-parity pattern inside a
column. Two X supports are therefore in the same X-gauge coset exactly when
they have the same `c` column parities.

Commutation with the Z center strip between columns `j` and `j+1` requires

$$p_j+p_{j+1}=0.$$

All column parities of a dressed X normalizer must be equal. The all-zero
choice is X-gauge-trivial. The only nontrivial protected choice is

$$p=(1,1,\ldots,1).$$

Any support in this coset contains at least one X in every column, so its
weight is at least `c`. A complete X row has exactly one occupied site per
column and realizes the bound:

$$d_X=c.$$

The row is bare, but a general minimum representative can zig-zag by
multiplying vertical gauge edges. This is the concrete difference between a
bare logical and a dressed logical.

## Z-type dressed operators

For a Z support matrix `B`, horizontal Z gauge edges generate every
even-parity pattern within a row. The gauge invariant is the row-parity vector

$$u_i=\sum_{j=0}^{c-1}B_{i,j}\pmod 2.$$

Commutation with adjacent-row X center strips forces every `u_i` to be equal.
The zero vector is gauge-trivial; the nontrivial protected coset has one in
every row. At least one Z is needed per row, and a complete column reaches the
bound:

$$d_Z=r.$$

For a CSS subsystem code with this single protected pair, a mixed Pauli cannot
beat both pure-sector minima: its X and Z support components must each be
either gauge-trivial or in the corresponding logical parity class, and its
Pauli weight contains the support of every nontrivial component. Hence

$$d=\min(r,c).$$

`reproduce.py` exhausts all pure-X and pure-Z supports through these minima
for every shipped rectangle and checks nonmembership in the full gauge row
space. Independently, the shared referee enumerates mixed Pauli supports in
increasing weight and verifies the total `d` values `2`, `3`, and `3` for the
shipped `2 × 2`, `3 × 3`, and `3 × 5` instances. The structured total-distance
claims therefore carry `verified` origins. The `d_X` and `d_Z` rows remain
literature-attributed because the generic referee reports the minimum over all
Pauli types rather than two named sectors.

The exact enumerator refuses an over-budget layer before treating partial
work as a lower bound. For the committed `5 × 7` case, the separate seeded
search finds a weight-`12` representative in `32` trials with seed `17`; the
independent validator accepts the Pauli, while the evidence envelope records
`optimality: not-certified`. This is an achieved upper bound only and does not
replace the parity proof of the rectangular family formula.

## Z errors become a repetition problem on rows

Let `E` be a Z-error support and retain only its row parities `u`. Horizontal
Z gauge motion changes positions within a row without changing `u`. The
X-center syndrome between rows `i` and `i+1` is

$$s^X_i=u_i+u_{i+1}.$$

Thus the protected syndrome is exactly the open repetition parity matrix
applied to `u`. There are two row-parity patterns for a given syndrome; they
differ by the all-one vector. That difference is the logical Z coset. Under a
specified independent-noise prior, the decoder chooses between those two
cosets by likelihood or majority logic.

For the `3 × 3` block, one Z error in each possible row gives:

| representative | row parity `u` | X-center syndrome `(s0,s1)` |
|---|---|---|
| `Z` on `q0` | `100` | `10` |
| `Z` on `q3` | `010` | `11` |
| `Z` on `q6` | `001` | `01` |

The column position is absent because changing it by horizontal Z gauge edges
does not change the protected action.

If physical Z errors are independent with probability `p`, the probability
that one row of length `c` has odd parity is

$$p_{row}=\sum_{w\text{ odd}}{c\choose w}p^w(1-p)^{c-w}
=\frac{1-(1-2p)^c}{2}.$$

This formula defines the perfect-readout effective repetition channel. It is
not a circuit-level threshold: measurement faults, propagation, correlations,
and repeated-round inference are absent.

## X errors become a repetition problem on columns

The perpendicular argument retains one parity `p_j` for each column. The
Z-center syndrome is

$$s^Z_j=p_j+p_{j+1}.$$

On the `3 × 3` block:

| representative | column parity `p` | Z-center syndrome `(s0,s1)` |
|---|---|---|
| `X` on `q0` | `100` | `10` |
| `X` on `q1` | `010` | `11` |
| `X` on `q2` | `001` | `01` |

For independent X errors with probability `p`, the odd parity of a column of
height `r` has probability `[1-(1-2p)^r]/2`. A `3 × 5` rectangle therefore
creates a length-five column-parity repetition decision for X errors and a
length-three row-parity decision for Z errors. Which shape is optimal depends
on both physical channels and the complete correction protocol.

## Degeneracy is the algorithm, not a nuisance

An ordinary decoder might try to identify the exact physical error. Here that
goal is unnecessarily strict. All supports with the same row or column parity
differ by gauge action and are equivalent on the protected subsystem. The
minimal sufficient statistic for perfect readout is the parity vector, and
the only remaining ambiguity is whether it belongs to the trivial or logical
all-one coset.

This quotient is also why a stabilizer-only distance routine is wrong for the
entry. Quotienting only by `S` would retain many operators that differ by
noncentral gauge action and would misclassify disposable degrees of freedom as
protected logicals.

## Boundary of the perfect-syndrome result

The tables above assume exact center syndromes. In a hardware circuit one
normally measures weight-two gauge generators, not the strips directly. Raw
gauge outcomes from different Pauli rounds can be disturbed, and a faulty
ancilla interaction can change both data and measurement records. The decoder
must consume the actual schedule's history. The next page derives the safe
outcome products and then separates the named circuit-level regimes:
[gauge measurement and fault tolerance](measurement-and-fault-tolerance.md).
