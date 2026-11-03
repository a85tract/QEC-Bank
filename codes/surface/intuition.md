# Surface code (planar, unrotated)

## Essence

**The object.** Put data qubits on the even-even and odd-odd sites of a
`(2L−1) × (2L−1)` checkerboard. The two blocks contain `L²` and `(L−1)²`
qubits. Put X-checks on the even-odd sites and Z-checks on the odd-even
sites; a check acts on the data qubits one lattice step away. Interior checks
have weight four and boundary checks have weight three. The resulting family
has

`[[2L²−2L+1, 1, L]]`.

The shipped instances are `[[13,1,3]]`, `[[25,1,4]]`, and `[[41,1,5]]`.
The verifier recomputes `n` and `k` for all three, enumerates `d=3,4`
exactly, and reruns a seeded weight-five upper-bound witness for `L=5`; the
matching lower bound is literature-backed. The complete calculation is in
[the HGP construction transcript](pedagogy/hgp-construction.md) and
[the distance proof](pedagogy/distance-proof.md).

**The idea.** A repetition code stores one observable nonlocally and leaves
its conjugate local: with checks `Z_i Z_{i+1}`, one can choose
`X_L=X⊗...⊗X` but `Z_L=Z_1`. In the Ising picture, a one-site order
parameter distinguishes the two ground states. That is fatal for a quantum
memory: the [Knill–Laflamme condition](../../foundations/knill-laflamme/)
requires every operator supported in a correctable region to act as a scalar
inside the code space.

Gauging the Ising `Z₂` symmetry replaces the local order parameter by a local
constraint. Qubits live on square-lattice edges; a star
`A_v=∏_{e∋v}X_e` imposes the Gauss law and a plaquette
`B_p=∏_{e∈∂p}Z_e` imposes zero flux. At this commuting-projector fixed
point, every sufficiently local operator has only scalar matrix elements
within the ground space, while nontrivial encoded action requires a
noncontractible string. On a torus there are two independent string qubits.
Cutting to a disk with two rough and two smooth boundary segments leaves one.
This is the planar surface code introduced through lattice boundaries by
[Bravyi and Kitaev](https://arxiv.org/abs/quant-ph/9811052), built from
Kitaev's [`Z₂` topological code](https://arxiv.org/abs/quant-ph/9707021).

**One sentence.** The surface code is the repetition code with its local
order parameter gauged away, then cut so that one conjugate pair of
boundary-to-boundary strings survives.

## Design problem

A distance-`d` quantum code detects every Pauli error of weight below `d` and
corrects arbitrary errors on at most `⌊(d−1)/2⌋` unknown qubits. It must
therefore protect both X-like and Z-like directions. Concatenated codes do
this recursively, and the threshold theorem proves that sufficiently weak
local noise can be suppressed to arbitrary accuracy
([Aharonov–Ben-Or](https://arxiv.org/abs/quant-ph/9906129)).

The engineering problem is not whether concatenation works, but what
interaction contract its recursive gadgets impose. Higher levels require
protected inner gadgets, verified ancillas, and either long-range
connectivity or routing. The surface-code alternative is to hold the
microscopic contract fixed:

- check weight stays at most four;
- interactions stay nearest-neighbor in two dimensions;
- one syndrome round has constant circuit depth;
- protection grows only by enlarging the patch.

This locality makes repeated measurement natural and turns decoding into a
bulk phase-transition problem. It also imposes two unavoidable prices.
First, two-dimensional commuting local checks obey the
[Bravyi–Poulin–Terhal tradeoff](../../foundations/bounds/bravyi-poulin-terhal.md),
`k d² = O(n)`. Second, bounded-spread local logical gates in two dimensions
are Clifford by the
[Bravyi–König theorem](../../foundations/bounds/bravyi-koenig.md), so a
native logical T gate is unavailable. The surface code is the answer to a
specific design choice: pay geometric area and magic-state overhead in
exchange for a local syndrome circuit with a reachable threshold.

## Derivation chain

**Physical route: gauge, close, then cut.**

1. The repetition/Ising code has a weight-one order parameter. Gauging its
   global `Z₂` symmetry gives edge qubits with star and plaquette constraints.
2. On an `L × L` torus there are `2L²` edge qubits. The `L²` stars have one
   product relation and so do the `L²` plaquettes, giving
   `k=2L²−(2L²−2)=2`. The logicals are the two homologically nontrivial loop
   classes and their duals.
3. A rough boundary condenses the electric endpoint of a Z string; a smooth
   boundary condenses the magnetic endpoint of an X string. A disk with only
   one boundary type has no protected string qubit. Alternating two rough and
   two smooth segments leaves a vertical Z class and a horizontal X class,
   which cross once and anticommute.
4. In the shipped geometry, top and bottom are rough and left and right are
   smooth. The [computed syndrome walk](pedagogy/syndrome-decoding.md) shows
   a bulk error producing two defects, a boundary absorbing one endpoint,
   and a completed crossing string producing no syndrome.

**Algebraic route: hypergraph product of two open chains.**

Let `H` be the `(L−1) × L` repetition parity matrix with adjacent `11`
rows. For two copies, the constructor forms

`H_X = [H ⊗ I_L | I_(L−1) ⊗ Hᵀ]`,

`H_Z = [I_L ⊗ H | Hᵀ ⊗ I_(L−1)]`.

The two qubit blocks contain `L²` bit×bit coordinates and `(L−1)²`
check×check coordinates. Commutation is designed in:

`H_X H_Zᵀ = H ⊗ Hᵀ + H ⊗ Hᵀ = 0` over `F₂`.

The open-chain matrix has rank `L−1`, hence classical dimensions
`k=1` and `kᵀ=0`. The HGP dimension formula
`k_Q=k₁k₂+k₁ᵀk₂ᵀ` therefore gives one logical qubit. Closing each chain
adds a dependent parity row: `kᵀ` becomes one and the same product gives the
toric code's two logical qubits. Thus “boundary versus handle” is the
corank of the classical factor matrix, not a metaphor.

The geometric checkerboard is exactly these Kronecker blocks laid out in the
plane. The [worked HGP page](pedagogy/hgp-construction.md) prints the matrices,
coordinate dictionary, locality checks, ranks, and commutation cancellation
from the shipped constructor.

## Multiple pictures

- **Homology.** `H_Zᵀ` and `H_X` are consecutive boundary maps. Z-logicals
  are relative cycles modulo face boundaries; X-logicals are the dual
  relative cycles. Multiplying by a stabilizer deforms a string within its
  relative homology class. Distance is the shortest nontrivial primal or dual
  relative cycle. See the
  [CSS chain-complex dictionary](../../foundations/css-chain-complexes/).

- **Anyons and decoding.** An error chain's syndrome is its boundary.
  Decoding chooses another chain with the same boundary; error plus
  correction is harmless exactly when the resulting cycle is homologically
  trivial. Maximum-likelihood decoding compares the total probability of
  homology classes, whereas minimum-weight matching keeps the lightest chain.
  The [syndrome page](pedagogy/syndrome-decoding.md) derives this statement,
  and the [threshold ledger](pedagogy/threshold-ledger.md) keeps the
  code-capacity, phenomenological, and circuit-level numbers separate.

- **Circuits and detectors.** A standard check measurement prepares one
  ancilla, entangles it with neighboring data qubits, and measures it. A
  detector is usually the parity of consecutive outcomes of the same check.
  Relevant single faults produce small detector patterns; some circuit faults
  are benign or observationally equivalent, so “every fault lights a
  detector” would be too strong. CNOT order matters because an ancilla fault
  can propagate to a two-data-qubit hook; the schedule must orient hooks away
  from the shortest logical direction.

- **Rotated cut.** The unrotated patch uses
  `2d²−2d+1` data qubits. Recutting the same bulk by 45 degrees puts the data
  on a `d × d` array while keeping both crossing lengths equal to `d`, giving
  `[[d²,1,d]]`. With one dedicated check ancilla per independent stabilizer,
  the totals are respectively `4d²−4d+1` and `2d²−1`. The saving is boundary
  geometry, not a new phase; the rotated construction is described explicitly
  in [Horsman et al.](https://arxiv.org/abs/1111.4022).

- **XZZX under biased noise.** A Hadamard on alternating data qubits maps the
  CSS presentation to XZZX checks. Under pure Z noise, XZZX defects obey
  separate parity constraints along diagonals, reducing decoding to
  independent repetition-code problems and giving a 50% code-capacity
  threshold. In the ordinary CSS presentation, pure Z errors trigger only
  X-checks—one syndrome graph—but that graph remains two-dimensional. The
  advantage is the XZZX diagonal conservation law, not a reduction from two
  CSS graphs to one. This mechanism and its finite-bias limits are derived in
  [Bonilla Ataides et al.](https://arxiv.org/abs/2009.07851).

- **Fermions and twists.** Star and plaquette defects are the `e` and `m`
  anyons. Moving one around the other produces a minus sign, so their
  composite has fermionic self-statistics. An `e↔m` duality wall can end at a
  twist defect; the patch corners are boundary-changing versions of the same
  object. This is why twist encodings inherit Majorana-like fusion
  bookkeeping without containing microscopic Majorana particles.

- **Laboratory memory.** Google's distance-five memory slightly outperformed
  distance three in the
  [2023 experiment](https://arxiv.org/abs/2207.06431). The later
  [distance-seven experiment](https://arxiv.org/abs/2408.13687) measured
  `0.143% ± 0.003%` logical error per cycle and an empirical suppression
  factor `Λ=2.14 ± 0.02` for a distance increase of two. `Λ` is a
  device-and-decoder fit, not a direct measurement of `p_th/p`.

## Why these parameters

**Length.** The HGP has one `L²` qubit block and one `(L−1)²` block, so
`n=2L²−2L+1`. The constructor and verifier recompute this for every shipped
instance.

**Dimension.** Each open repetition matrix has `k=1` and transpose dimension
zero. Künneth bookkeeping gives `1·1+0·0=1`. Direct rank computation agrees:
both quantum check matrices have rank `L(L−1)`, hence
`k=n−2L(L−1)=1`.

**Distance.** A row of the `L × L` block is an X-logical and a column is a
Z-logical, so `d≤L`. For the reverse inequality, the Z-logical class has `L`
pairwise-disjoint column representatives, all equivalent modulo
Z-stabilizers. Any logical anticommuting with that class must touch every one
of those disjoint supports and therefore has weight at least `L`; the same
argument with the X rows handles the conjugate class. Thus `d=L`. The
[distance page](pedagogy/distance-proof.md) proves the general statement and
then checks the representatives computationally.

**Verification status.** `L=3,4` use exhaustive CSS logical enumeration.
For `L=5`, the lower bound `d≥5` is carried by the family theorem and its
literature provenance, while the verifier reruns a seeded low-weight search
that finds a weight-five logical. The instance is therefore marked
`bounded`, not `verified`.

**Rate and locality.** `k/n→0` while `d=Θ(√n)`. This saturates the
two-dimensional `k d²=O(n)` tradeoff up to a constant. The complete argument,
including exactly where Euclidean bounded range enters, lives on the
[BPT derivation page](../../foundations/bounds/bravyi-poulin-terhal.md).
Likewise, the absence of a constant-depth local T gate follows from the
[full Bravyi–König derivation](../../foundations/bounds/bravyi-koenig.md),
not from a slogan about transversality.

## Failure modes

- **Area overhead.** For this unrotated family, one check ancilla per
  independent stabilizer gives `4d²−4d+1` physical qubits per logical
  memory. The rotated patch reduces this to `2d²−1`. These totals exclude
  routing lanes, spare qubits, and factory space, which must be stated
  separately rather than hidden in “physical qubits.”

- **No passive thermal memory.** A logical string can grow while paying only
  for its pointlike endpoints, so the commuting Hamiltonian has an
  order-one energy barrier. Two-dimensional local stabilizer Hamiltonians
  cannot be self-correcting
  ([Bravyi–Terhal](https://arxiv.org/abs/0810.1983)); continuous active
  measurement is part of the memory, not an optional implementation detail.

- **Decoder/model dependence.** Minimum-weight matching ignores path
  degeneracy and, when X and Z components are decoded separately, ignores
  correlations such as a single Y fault producing both syndrome types.
  Thresholds cannot be quoted without the noise model, measurement model,
  circuit schedule, and decoder; the
  [threshold ledger](pedagogy/threshold-ledger.md) records those qualifiers.

- **Bias mismatch.** A square CSS patch gives equal X and Z distances even
  when the hardware does not. Rectangular patches or an XZZX basis align the
  protection with the channel.

- **No local non-Clifford gate.** Two-dimensional bounded-spread logical
  gates stop at the Clifford group. Universal computation therefore needs
  injection plus distillation, code switching, or another resource that
  leaves the theorem's assumptions.

- **Operations consume spacetime.** On a fixed planar patch architecture,
  lattice surgery is the usual two-qubit primitive because it preserves
  nearest-neighbor connectivity, but it is not the only one: defect braiding
  also works on fixed hardware, and stacked or movable layouts can expose
  transversal CNOT. “Every fixed-layout two-qubit gate is surgery” would be
  false.

## Operations story

**Transversal CNOT.** For two identical CSS blocks, pairwise physical CNOT
maps a control X-stabilizer to the product of corresponding control and target
X-stabilizers, and maps a target Z-stabilizer to the corresponding product in
the opposite direction. The same conjugation sends
`X_L⊗I → X_L⊗X_L` and `I⊗Z_L → Z_L⊗Z_L`. It is therefore a depth-one logical
CNOT when corresponding qubits can interact. Movable neutral-atom arrays
have demonstrated improvement of this two-qubit logical operation while
scaling surface-code distance from three to seven
([Bluvstein et al.](https://arxiv.org/abs/2312.03982)); correlated errors still
require joint decoding. The transversal operation was the fault-tolerant
ingredient: preparation of the distance-five and distance-seven logical input
states was not itself fault-tolerant, so this result must not be read as an
end-to-end below-threshold memory demonstration.

**Lattice surgery.** Joining two smooth boundaries introduces local seam
checks whose product is `Z_L⊗Z_L`; the dual rough merge measures
`X_L⊗X_L`. A merge reduces `k` by one because the measured logical parity is
projected, and a split restores two output patches with a recorded Pauli
frame. Repeating the merged syndrome for `d` rounds supplies timelike
distance, but the fault-tolerant outcome comes from spacetime decoding, not
from a bare majority vote once data and circuit faults are allowed. The
[worked surgery page](pedagogy/lattice-surgery.md) derives the seam product,
checks the `L=3` rectangular merge as `n=28,k=1,d=3`, and separates the toy
measurement-only limit from the full decoder.

**Hadamard.** Applying H to every data qubit exchanges X and Z checks. For
this patch it maps the code to its dual, which is the same geometry rotated by
90 degrees. Transversal H followed by that relabeling is logical H. On fixed
hardware, restoring the original orientation is a distance-preserving code
deformation taking order `d` rounds
([Horsman et al.](https://arxiv.org/abs/1111.4022)).

**Folded Clifford gates.** If the surface code is maintained in a folded,
mirror-dual layout, paired qubits support a constant-depth logical S using
phase gates on the fold and CZ-type gates between mirror partners. The
logical gate is constant depth on an already folded layout; physically
folding or unfolding a planar patch is itself an order-`d` routing or
deformation operation. This distinction is explicit in
[Moussa's construction](https://arxiv.org/abs/1603.02286).

**Braiding and twists.** Turning off checks creates holes. A loop around one
hole and a string between like holes form a logical pair; moving a primal
hole around a dual hole implements CNOT by code deformation. Boundary-type
changes create twists, whose braiding supplies single-qubit Clifford
operations. These are alternatives within the Clifford menu, not ways around
Bravyi–König.

**Universal completion.** Logical T is supplied by a non-stabilizer resource:
inject a noisy magic state, distill it using Clifford operations, and consume
it by gate teleportation. The operations listed in `card.yaml` distinguish
surgery, transversal, braiding, twist, and fold-transversal mechanisms so
that hardware geometry is never mistaken for an intrinsic property of the
code.

## Litmus questions

**Q1:** What single rank fact distinguishes this planar code from the toric
code? **A:** The open-chain repetition matrix is `(L−1)×L` with full row rank,
so its transpose code has dimension zero. Closing the chain creates one row
relation, making the transpose dimension one. In the HGP formula this changes
`1·1+0·0=1` into `1·1+1·1=2`.

**Q2:** Why is `d=L` a proof rather than a picture of one length-`L` string?
**A:** A length-`L` row and column prove only the upper bound. The lower bound
uses `L` disjoint representatives of each logical class: anything
anticommuting with the class must touch every representative, hence at least
`L` qubits. The representative equivalence and disjointness are checked in
[the distance transcript](pedagogy/distance-proof.md).

**Q3:** Why does XZZX reach 50% under pure dephasing while the CSS surface
code does not? **A:** Pure Z errors activate only one syndrome type in either
description. XZZX adds diagonal parity conservation, splitting that
two-dimensional problem into independent repetition codes. CSS lacks this
one-dimensional decomposition and retains its roughly 10.9% optimal
code-capacity threshold.

**Q4:** May one compare 10.9%, 2.9%, and 0.57% as three estimates of the same
threshold? **A:** No. They refer respectively to perfect-syndrome
code-capacity noise, repeated phenomenological data/measurement noise, and a
particular scheduled circuit-level model. Their elementary fault locations
and decoders differ. See the
[model-by-model ledger](pedagogy/threshold-ledger.md).

**Q5:** Why are `d` surgery rounds not simply “majority vote in time”?
**A:** If only independent seam-outcome flips occur, repeated parity samples
do reduce to a repetition code. Real syndrome circuits also contain data and
propagated faults, which create correlated spacetime detection events. The
logical parity is inferred jointly with those events by a spacetime decoder.

**Q6:** How many qubits does the unrotated patch consume when ancillas are
counted? **A:** It has `2d²−2d+1` data qubits and one fewer independent
checks, so one dedicated ancilla per check gives `4d²−4d+1` total. The
rotated totals are `d²` data plus `d²−1` ancillas, or `2d²−1`.

**Q7:** Is physical H on every qubit already a logical H? **A:** It exchanges
the code with its dual. The logical gate is transversal H plus the 90-degree
geometry relabeling; restoring a fixed planar footprint requires code
deformation. An S gate is constant depth only once the mirror-dual folded
layout is available.

**Q8:** What precisely forbids logical T? **A:** A bounded-depth,
bounded-range circuit on a growing-distance two-dimensional topological
Pauli stabilizer code induces a level-two Clifford-hierarchy operation.
`T` is level three. Injection and code switching work because they add a
resource or leave an assumption of that theorem.
