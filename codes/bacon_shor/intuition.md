# Bacon–Shor code

## Essence

**The object.** Put one qubit at every site of a `rows × columns` rectangle,
using row-major labels `q(r,c)`. Generate a subsystem gauge group from

- `XX` on every vertical nearest-neighbour pair, and
- `ZZ` on every horizontal nearest-neighbour pair.

A vertical `XX` and a horizontal `ZZ` that meet at one site anticommute. That
is not a defect: gauge generators are allowed to disturb an unprotected gauge
subsystem. The protected codespace is fixed only by the commuting center of
the gauge group. Multiplying all vertical `XX` links across one gap between
rows produces an X-type center strip; multiplying all horizontal `ZZ` links
across one gap between columns produces a Z-type center strip. The
[gauge-center derivation](pedagogy/gauge-center-and-qubits.md) proves their
centrality and counts every protected and gauge degree of freedom.

For an `r × c` rectangle the formal ledger is

`n = rc`, `k = 1`, `gauge qubits = (r-1)(c-1)`,
`d_X = c`, `d_Z = r`, and `d = min(r,c)`.

Here `d_X` names the lightest X-type dressed logical and `d_Z` the lightest
Z-type dressed logical in the entry's Pauli convention. The shared Atlas
referee now constructs `C(S)/G`, enumerates complete Pauli-weight layers, and
recomputes the total dressed distance of every shipped finite instance. Those
three `d` claims are therefore `verified`. The named sector formulas remain
literature-attributed because the shared API does not separately certify
`d_X` and `d_Z`. Beyond the exact-search ceiling, a seeded search may establish
an achieved upper bound only; scalable lower bounds and equivalence-safe
presentation changes remain on the
[subsystem dressed-distance gap](../../wanted.html#subsystem-dressed-distance).

**The trick.** Bacon–Shor does not make Shor's long repetition constraints
disappear. It factorizes each long center measurement into local weight-two
gauge measurements whose outcomes can be multiplied afterward. Locality is
gained at the measurement interface; the stabilizers in the center still
span complete two-row or two-column strips.

**One sentence.** Bacon–Shor protects one qubit by reducing X and Z errors,
modulo local gauge motion, to two perpendicular classical repetition
problems.

## Design problem

Shor's nested repetition code has a clean decoding story, but some of its
stabilizer checks cover two complete length-`c` or length-`r` blocks. Directly
coupling an ancilla to such a growing support invites correlated faults and a
large circuit. The subsystem move asks a sharper question:

> Which local observables contain the same protected syndrome if we agree not
> to preserve every degree of freedom inside the encoded block?

The answer is the pair-gauge grammar above. Individual gauge outcomes are not
simultaneous eigenvalues because perpendicular links can anticommute. Only
products in the center define persistent stabilizer syndromes. An error and
that error multiplied by a gauge operator act identically on the protected
logical qubit, so recovery only needs the correct gauge coset.

This trade has four costs that the word "local" can hide:

- the center stabilizers remain long strips even though their measured factors
  have weight two;
- X- and Z-type gauge measurements must be ordered, repeated, or embedded in
  a circuit whose time history is part of the decoder input;
- the disposable subsystem grows as `(r-1)(c-1)`, so `n-rank(S)` is not the
  protected logical-qubit count;
- a decoder, threshold, or logical operation belongs to a specified
  extraction protocol and noise model, not to the static rectangle alone.

The [measurement and fault-tolerance ledger](pedagogy/measurement-and-fault-tolerance.md)
keeps perfect gauge readout, repeated circuits, encoded-ancilla extraction,
self-concatenated surgery, and the Floquet descendant separate.

## Derivation chain

**1. Fix the orientation.** Qubits are ordered by rows. X-type gauge edges are
vertical and Z-type gauge edges are horizontal. Transposing the rectangle and
swapping X with Z gives an equivalent convention, but formulas such as
`d_X=c` and `d_Z=r` depend on declaring this orientation first.

**2. Multiply local edges into center strips.** For a fixed gap between rows,
multiply its `c` vertical `XX` edges. Interior cancellations do not occur;
instead the product is X on every qubit in the two adjacent rows. Any
horizontal `ZZ` gauge edge meets that strip on zero or two sites, so it
commutes. The perpendicular construction gives a Z strip over two adjacent
columns. Thus all `r-1+c-1` strips commute with the entire gauge group.

**3. Count the quotient.** There are `c(r-1)` independent X gauge rows and
`r(c-1)` independent Z gauge rows. Their symplectic supports occupy different
halves of the binary matrix, so

`rank(G) = c(r-1) + r(c-1) = 2rc-r-c`.

The center basis has rank `rank(S)=r+c-2`. The subsystem identities

`k = n - (rank(G)+rank(S))/2`

and

`g = (rank(G)-rank(S))/2`

give one protected qubit and `(r-1)(c-1)` gauge qubits. The
[rank ledger](pedagogy/gauge-center-and-qubits.md) derives these formulas from
open-chain incidence matrices rather than assuming the generators are
independent.

**4. Find bare logicals.** X on one complete row commutes with every gauge
generator: each horizontal Z edge overlaps it twice. Z on one complete column
commutes for the perpendicular reason. The two strings cross once and
anticommute. Moving to a parallel row or column multiplies by a center strip,
which is itself in the gauge group, so the protected action is unchanged.

**5. Dress and reduce.** Multiplying an X logical by vertical X gauge edges can
move its one X within each column independently. What survives gauge motion is
the parity in every column. A nontrivial X logical has odd parity in all `c`
columns, so it needs at least one occupied site per column and has weight at
least `c`. A row realizes the bound. Likewise, a Z logical has odd parity in
all `r` rows and has weight exactly `r`. The
[dressed-distance proof](pedagogy/dressed-distance-and-decoding.md) makes the
quotient and the lower bounds explicit.

**6. Read two repetition syndromes.** Modulo horizontal Z gauge edges, a Z
error is completely specified by one parity bit per row. An X center strip
between rows `i` and `i+1` reports the XOR of the two adjacent row parities.
That is the open repetition-check matrix of length `r`. X errors reduce to
column parities and the length-`c` repetition check in the other direction.
Perfect-syndrome decoding is therefore two classical decisions; noisy gauge
extraction is a spacetime inference problem.

**7. Gauge-fix without confusing logical names.** On the `3 × 3` member,
promote all six horizontal `ZZ` gauge pairs to stabilizers and retain the two
X center strips. Their row space equals the repository's nine-qubit Shor
stabilizer row space. The neighboring Shor entry chooses encoded-basis names
in which its logical X is the Z column and its logical Z is the X row, the
reverse of this card's Pauli-type labels. The
[operation and gauge-fixing page](pedagogy/operations-gauge-fixing-and-variants.md)
records both the exact row-space equality and this logical-basis dictionary.

## Multiple pictures

- **Gauge group, center, quotient.** `G` is nonabelian, `S=Z(G)` fixes the
  codespace, and protected Paulis live in the centralizer of `S` modulo `G`.
  This is the executable picture used by `constructor.py`.

- **Two repetition codes.** Z errors collapse to row parities and X errors to
  column parities. Center syndromes are adjacent parity differences. This is
  the shortest decoding picture and explains why stretching the rectangle
  changes the two distances in opposite directions.

- **Compass Hamiltonian.** Reading the same pair generators as Hamiltonian
  terms produces alternating XX/ZZ compass interactions and rigid line
  symmetries. The dictionary exposes the center but does not make the ordinary
  static model a topological or self-correcting memory.

- **Gauge-fixed Shor block.** Choosing a commuting set of horizontal ZZ gauge
  edges removes gauge freedom and recovers the nine-qubit Shor stabilizer
  space. Gauge fixing changes which observables are fixed; it is not deletion
  of qubits or proof that all subsystem and subspace conventions coincide.

- **Tensor-leg reassignment.** A surface-code tensor network can expose
  selected legs as logical rather than physical, yielding the Bacon–Shor
  gauge bookkeeping. This is a representation dictionary, not an exact
  check-matrix replay adapter in the present repository.

- **Frustration graph and dynamical descendant.** The gauge anticommutation
  graph records which perpendicular pair terms meet once. A period-four
  Floquet–Bacon–Shor schedule turns related local measurements into
  time-dependent detectors and logical representatives; it is a different
  spacetime object, not another rendering of this static center.

The [representations and realizations ledger](pedagogy/representations-and-realizations.md)
states the equivalences and non-equivalences. The guided
[gauge-to-center tour](../../tours/bacon_shor.html) lets the reader inspect the
exact pair edges, center strips, bare logicals, gauge fix, and rectangular
counterfactual from constructor data.

## Why these parameters

**Why `n=rc`.** The rectangle has one physical qubit per site and no boundary
identifications or deleted sites.

**Why only one protected qubit.** The local gauge span has rank
`2rc-r-c`; its center has rank `r+c-2`. Substituting those two independently
recomputed ranks into the subsystem dimension formula leaves `k=1` for every
`r,c >= 2`. The remaining `(r-1)(c-1)` encoded degrees of freedom are gauge
qubits, not extra protected logicals.

**Why the distances follow the opposite dimension.** An X-type dressed
logical must carry odd parity in each column and therefore occupies at least
`c` sites; a complete row attains that weight. A Z-type dressed logical must
carry odd parity in each row and therefore has weight `r`; a complete column
attains it. The scalar distance is the smaller sector.

**Why the square members look symmetric.** For `r=c=L`, X and Z distances
both equal `L`, while the gauge count becomes `(L-1)^2`. Symmetry exchanges X
and Z only after transposing the grid; physical Hadamards without that
permutation do not restore the declared orientation.

**Why the `3 × 5` member is useful.** Its X logical crosses five columns
while its Z logical crosses three rows. Aspect ratio can therefore match a
noise bias, but the optimal rectangle also depends on physical error rates,
extraction circuits, objective, and operation costs. It is not a code-only
constant.

`instances.yaml` marks `n`, `k`, and CSS status `verified`. Distances and gauge
counts remain structured literature claims because the shared verifier has no
subsystem quotient implementation; `pedagogy/reproduce.py` supplies an
entry-specific independent audit without silently upgrading their provenance.

## Failure modes

- **Treating every gauge generator as a stabilizer.** A vertical `XX` and an
  incident horizontal `ZZ` anticommute. Requiring simultaneous `+1`
  eigenvalues would define no common stabilizer subspace. Only center products
  are stabilizers.

- **Counting `n-rank(S)` protected qubits.** That expression also counts the
  disposable gauge subsystem. The protected count uses both `rank(G)` and
  `rank(S)`; the `3 × 3` block has one protected qubit and four gauge qubits,
  not five protected qubits.

- **Confusing bare and dressed logicals.** A bare logical commutes with every
  gauge generator and appears as a complete row or column. A dressed logical
  need only commute with the center; gauge multiplication can bend it to one
  occupied site per column or row. Distance minimizes dressed weight.

- **Calling local gauge checks local stabilizers.** The measured factors have
  weight two, but their center products span complete strips whose weight
  grows with the perpendicular block dimension.

- **Multiplying outcomes from incompatible times without a circuit model.**
  Noncommuting X- and Z-gauge measurements disturb one another's raw values.
  A persistent detector requires an ordered schedule, repeated outcomes, and
  a convention for which products are compared across rounds.

- **Importing a threshold from a different protocol.** Static perfect gauge
  readout, repeated noisy pair extraction, encoded-ancilla Steane extraction,
  self-concatenated surgery, and period-four Floquet detectors expose
  different syndrome objects. As of the 2026-08-02 decoder sweep, no
  extraction-independent threshold for unspecified static Bacon–Shor
  stabilizer products was found.

- **Equating gauge fixing with an identity of logical labels.** The square
  gauge fix reproduces the Shor stabilizer row space, but this entry and the
  Shor entry choose opposite encoded-basis names for the X-row/Z-column pair.
  The algebra is the same only after that dictionary is stated.

## Operations story

**Pairwise CNOT.** Apply one physical CNOT between corresponding sites of two
equally shaped blocks. An X gauge on the control maps to the product of the
matching X gauges on control and target; a Z gauge on the target maps to the
matching pair on both blocks. The other two gauge types stay in their own
blocks. The gauge group and its center are preserved, and the row-X/column-Z
logical pair undergoes logical CNOT. Routing, extraction, and recovery are
additional resources.

**Hadamard on a square.** Physical H swaps X and Z, turning vertical X edges
into vertical Z edges and horizontal Z edges into horizontal X edges. A row/
column transposition then restores the declared gauge orientation and swaps
the logical row and column. The permutation is part of the gate.

**Gauge fixing.** Measuring and fixing the horizontal Z gauge edges on the
`3 × 3` block yields the Shor stabilizer presentation. More general choices
produce compass-code descendants. Which gauges are promoted, how their
outcomes set the Pauli frame, and how faults are handled are operation data,
not consequences of the word "gauge fix."

**Geometry-assisted non-Clifford routes.** Dimension-matched rectangular
blocks support cited transversal multi-controlled-Z constructions, while
biased-noise architectures combine strong aspect ratios with teleportation
and verified ancillas. Subsystem lattice surgery consumes compatible
boundaries and repeated joint measurements. Measurement-free deformation
replaces mid-circuit measurement with coherent correction and extra qubits.
The [operations ledger](pedagogy/operations-gauge-fixing-and-variants.md)
separates these mechanisms and their resource boundaries.

**Dynamical descendant.** Floquet–Bacon–Shor logical operations require a
period-four schedule, time-dependent logical tracking, detector decoding, and
feed-forward. They are evidence for the descendant named in the card, not
verified operations of the static check matrix exported here.

## Litmus questions

**Q1:** Why may two Bacon–Shor gauge generators anticommute? **A:** Gauge
outcomes describe an unprotected subsystem and need not be simultaneous
stabilizer eigenvalues. The protected subspace is fixed by center elements,
which commute with the whole gauge group.

**Q2:** How does a product of anticommuting local checks become a commuting
stabilizer? **A:** Multiply every parallel pair check across a complete gap.
Any perpendicular gauge edge then intersects the product on zero or two
qubits, so the total symplectic overlap is even.

**Q3:** Why does a `3 × 5` block have `d_X=5` and `d_Z=3` in this convention?
**A:** X gauge motion preserves one parity per column, so a nontrivial X
logical needs one occupied site in all five columns. Z gauge motion preserves
one parity per row, so a nontrivial Z logical needs one site in all three rows.

**Q4:** If the `3 × 3` center has four stabilizers, why is `k` not five?
**A:** Four additional encoded degrees of freedom are gauge qubits. Using
`rank(G)=12` and `rank(S)=4` gives
`k=9-(12+4)/2=1` and `g=(12-4)/2=4`.

**Q5:** What information does perfect Z-error decoding actually use? **A:**
Horizontal Z gauge motion erases all detail except each row's error parity.
The two X center syndromes on a three-row block report adjacent differences of
those three bits, exactly the classical repetition syndrome.

**Q6:** Does gauge-fixing Bacon–Shor to Shor preserve the names logical X and
logical Z used by both entry cards? **A:** It preserves the protected Pauli
algebra and exactly reproduces the Shor stabilizer row space, but the Shor
entry's encoded-basis convention calls the Z column logical X and the X row
logical Z. The labels are swapped relative to this card's Pauli-type names.
