# Operations, gauge fixing, and variants

This page separates operations proved from the exported gauge algebra from
protocols whose fault tolerance and resource cost remain literature claims.

## Pairwise physical CNOT

Take two identically ordered `r × c` blocks, A as control and B as target,
and apply physical CNOT pairwise at every grid site. Pauli conjugation gives

$$X_A\mapsto X_AX_B,\quad X_B\mapsto X_B,$$

$$Z_A\mapsto Z_A,\quad Z_B\mapsto Z_AZ_B.$$

Apply these rules to each local generator:

- an X gauge edge in A maps to the matching X gauge edge in both A and B;
- an X gauge edge in B remains in B;
- a Z gauge edge in A remains in A;
- a Z gauge edge in B maps to the matching Z gauge edge in both blocks.

Every image is in the two-block gauge group, so the center and protected
subsystem are preserved. The bare logical row and column obey the same
conjugation rules, giving logical CNOT in this card's Pauli-type convention.
This establishes the abstract transversal layer. It does not include routing,
faulty CNOT locations, extraction, or recovery.

## Hadamard requires a square and a transpose

Physical H swaps X and Z. On the declared grid it maps vertical X gauge edges
to vertical Z edges and horizontal Z gauge edges to horizontal X edges, which
does not match `constructor.py`'s orientation. Transpose the grid coordinates
after the H layer:

`(i,j) -> (j,i)`.

Vertical edges become horizontal and horizontal edges become vertical. For a
square block this restores the gauge-generator set and exchanges the logical
X row with the logical Z column. A nonsquare rectangle is mapped to the
transposed `c × r` block, so it is not an unchanged-block transversal H.

`reproduce.py` performs this support map on the `3 × 3` generator set and
checks exact equality after the Pauli swap.

## Exact `3 × 3` gauge fix to the Shor stabilizer space

The square Bacon–Shor center contains two X strips:

`XXXXXX___` and `___XXXXXX`.

Promote all six horizontal Z gauge pairs to stabilizers:

`ZZ_______`, `_ZZ______`, `___ZZ____`, `____ZZ___`,
`______ZZ_`, and `_______ZZ`.

These eight rows are exactly the set exported by `atlas/shor_nine/`, up to row
order. The reproduction transcript loads both constructors and proves mutual
row-space containment and equal rank; this is stronger than comparing the
parameter label `[[9,1,3]]`.

### The logical-label dictionary

The stabilizer equality does not license silently copying logical names. This
entry uses Pauli-type labels:

| Bacon–Shor name | representative | Shor entry's encoded-basis name |
|---|---|---|
| logical X | `XXX______` | logical Z |
| logical Z | `Z__Z__Z__` | logical X |

Both pairs generate the same protected Pauli algebra and anticommute once.
The Shor entry names them by their action on Shor's chosen encoded cat-state
basis, while this entry names them by physical Pauli type. The gauge fix
preserves the protected algebra but the cross-entry dictionary includes a
logical Hadamard relabeling.

Promoting a gauge operator also fixes one formerly disposable degree of
freedom. A fault-tolerant gauge-fixing protocol must record the measured
outcomes, any repeated checks, and the Pauli-frame update; row-space equality
alone is not a circuit.

## Compass-code gauge fixes

The full rectangle promotes all horizontal Z gauges in the Shor specialization.
Other commuting promotion patterns produce two-dimensional compass-code
descendants (`li2019compass`). The selected pattern changes stabilizer weights,
exposed syndrome information, and decoding geometry. It cannot be represented
by changing only `rows` and `columns` on this card, so the relation target is a
separate pending family.

Bravyi–Bacon–Shor changes a different resource: a binary occupancy matrix
chooses which grid sites exist. Its encoded dimension and distances are
properties of row and column codes of that matrix. The full rectangular
family here is a special case; generalized rate claims do not flow backward
to this card.

## Cited non-Clifford and interface mechanisms

| mechanism | what changes or is consumed | claim boundary |
|---|---|---|
| dimension-matched transversal controlled-Z family | rectangle dimensions and correction between protocol pieces | `yoder2017universalbacon`; not a universal transversal set on one fixed square |
| biased-noise teleportation | strong aspect ratio, verified ancillas, teleportation measurements, correction | `brooks2013asymmetric`; geometry alone is not the architecture |
| subsystem lattice surgery | compatible boundaries, ancilla code patch, repeated joint gauge measurements, feed-forward | `nautrup2017interface`; not pairwise block transversality |
| measurement-free deformation | coherent correction circuitry and extra qubits replace mid-circuit measurement | `veroni2025measurementfree`; measurement-free is not correction-free |
| Floquet logical control | period-four schedule, detector decoding, time-dependent logical tracking | `sun2025floquetbacon`; descendant only |

As of the 2026-08-02 operations sweep, no fetched source supports a universal
transversal set on one unchanged square Bacon–Shor block. Universality in the
cited protocols uses aspect-ratio changes, teleportation, deformation,
concatenation, surgery, or error-correction steps between pieces.

## Static algebra versus fault-tolerant gadget

The CNOT and square-H support maps are exact statements about ideal Pauli
conjugation. Calling them fault tolerant additionally requires a fault set,
propagation analysis, extraction schedule, decoder, and recovery placement.
The remaining operations in the table are kept `claimed` on `card.yaml`
because their resource and fault-tolerance statements come from named
protocols rather than the static constructor.
