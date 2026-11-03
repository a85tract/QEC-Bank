# Representation and realization ledger

Several literatures use the same row/column structure for different purposes.
This ledger states what each picture preserves and what it does not license.

## Representation dictionary

| picture | exact object retained | insight gained | boundary |
|---|---|---|---|
| gauge-center quotient | symplectic gauge rows, center rows, protected quotient | why noncommuting local checks can protect one qubit | canonical executable view |
| perpendicular repetition | row and column parity quotients | sector distances, degeneracy, and perfect-readout decoding | does not define a noisy extraction circuit |
| quantum compass Hamiltonian | local XX/ZZ interaction pattern and line symmetries | center strips as rigid symmetries | does not make the static model topological or self-correcting |
| surface-tensor leg reassignment | tensor-network operator-pushing dictionary | how physical/logical leg bookkeeping exposes weight-two gauges | not an exact constructor replay or equality of stabilizer row order |
| frustration graph | pairwise anticommutation of gauge terms | which perpendicular links obstruct simultaneous gauge values | ordinary Bacon–Shor is the obstructed relative, not labeled free-fermion solvable |
| autonomous gauge dynamics | gauge interactions plus a chosen dissipative/control model | how the disposable subsystem affects dynamical correction | dynamics claim, not a new static code parameter |
| period-four Floquet descendant | scheduled measurement graph, detectors, time-dependent logicals | how related pair measurements define a dynamical qubit | not the static `CheckMatrix` rendered at landing |

The first two rows are recomputed. The other rows are curated dictionaries
with registered primary references.

## Compass Hamiltonian

Assign the pair operators as local Hamiltonian terms. The same vertical-X and
horizontal-Z pattern becomes the square quantum compass model. Products along
complete lines commute with the Hamiltonian and mirror the center-strip
symmetries. This makes the energetic role of gauge degrees of freedom visible.

It does not follow that local pair terms produce a topologically ordered or
self-correcting memory. `dorier2005compass`, `bacon2006operator`, and
`sarma2013gauge` discuss the interaction/symmetry and autonomous-dynamics
questions with their own model assumptions. The static code entry exports no
Hamiltonian gap, bath, lifetime, or thermal scaling claim.

## Tensor-leg reassignment

`cao2022quantumlego` obtains a Bacon–Shor description by reorganizing a
surface-code tensor network and declaring selected dangling legs logical
rather than physical. Operator pushing then exposes the pair-gauge structure.

This is a useful explanation of subsystem bookkeeping: changing which tensor
legs count as protected versus disposable can turn a stabilizer presentation
into a gauge presentation. It is not an exact operation-tree adapter in this
repository. A contraction or leg reassignment can also create a new code whose
parameters must be recomputed rather than inherited.

## Frustration graph and the free-fermion boundary

Build a graph whose vertices are gauge terms and whose edges connect
anticommuting pairs. For the rectangular compass pattern, a vertical X edge is
adjacent to each horizontal Z edge sharing exactly one endpoint. The graph is
constructor-derivable and exposes the nonabelian measurement conflicts.

`chapman2022freefermion` uses Bacon–Shor as the obstructed comparison when
constructing a related free-fermion subsystem model. The fetched source does
not establish that ordinary Bacon–Shor is itself free-fermion solvable. The
card therefore labels this view a boundary, not a free-fermion realization.

## Static and dynamical hardware evidence

| platform/result | code object | established | not established |
|---|---|---|---|
| thirteen-qubit trapped-ion processor (`egan2021fault`) | nine data qubits in a static Bacon–Shor logical block plus four ancillas | fault-tolerant preparation, measurement, corrected rotations, and stabilizer-extraction primitives on a fixed block | increasing-distance below-threshold memory scaling |
| superconducting processor (`sun2025floquetbacon`) | scheduled Floquet–Bacon–Shor descendant | operations on a time-dependent dynamical logical qubit | realization of this card's static center/checkmatrix experiment |
| bias-preserving teleportation architecture (`brooks2013asymmetric`) | proposed strongly rectangular blocks inside a larger protocol | architecture and resource analysis under biased elementary operations | hardware demonstration or a code-only optimum aspect ratio |

The static trapped-ion experiment is the direct realization attached to this
card. The superconducting result is recorded as descendant evidence because
its logical qubit and detectors depend on a schedule absent from the static
constructor.

As of the 2026-08-02 realization sweep, no increasing-distance below-threshold
Bacon–Shor hardware scaling demonstration was found. That dated negative
result does not diminish the demonstrated fixed-block primitive suite; it
prevents the two evidence levels from being merged.

## Variant invariants

Use the following test before transferring a claim:

- changing only `r` and `c` preserves the rectangular pair-gauge grammar but
  changes sector distances and gauge count;
- changing the occupancy matrix creates Bravyi–Bacon–Shor row/column codes and
  can change protected dimension;
- promoting a commuting gauge subset changes the stabilizer group and creates
  a compass-code or Shor gauge fix;
- adding a time schedule changes the detector graph and logical evolution;
- changing tensor leg roles supplies a representation map whose exact output
  still needs parameter verification.

Matching words such as "compass," "Bacon–Shor," or "subsystem" do not prove
these objects have interchangeable distances, thresholds, operations, or
hardware evidence.

## Source and negative-result ledger

- Gauge/compass/autonomous: `bacon2006operator`, `dorier2005compass`,
  `sarma2013gauge`.
- Tensor dictionary: `cao2022quantumlego`.
- Frustration/free-fermion boundary: `chapman2022freefermion`.
- Static hardware: `egan2021fault`.
- Floquet descendant: `alam2025board`, `sun2025floquetbacon`.
- Biased architecture: `brooks2013asymmetric`.

The 2026-08-02 representation sweep found no source calling the ordinary
two-dimensional compass Hamiltonian a self-correcting topological memory, and
no source making the base code free-fermion solvable. Bibliographic identity,
queries, and correction notes are retained in the six local literature files.
