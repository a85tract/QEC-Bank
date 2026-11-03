# Which operations are verified, and what did hardware demonstrate?

## Constructor-verified logical Paulis

The constructor exports two primal `Z` cycles and two dual `X` cycles. For
each support it builds a binary symplectic row and verifies three conditions:

1. the row commutes with every stabilizer;
2. it is not in the stabilizer row space; and
3. the four rows have exactly two conjugate odd-intersection pairs.

Applying one string is a logical Pauli. Because its single-qubit factors can be
applied in parallel, the physical depth is one when the control hardware
allows simultaneous Paulis. In practice a decoded logical Pauli is usually
recorded in a classical Pauli frame, avoiding a physical layer.

The support has weight `L`; “depth one” does not mean “weight one” and does not
remove control, calibration, or correlated-fault concerns.

## Verified stacked-block CNOT

Align two identical blocks and apply physical CNOT from each control edge to
the corresponding target edge. Pauli conjugation acts as

```text
Xc -> Xc Xt,   Xt -> Xt,
Zc -> Zc,      Zt -> Zc Zt.
```

An `X` star on the control becomes the product of corresponding stars on both
blocks; a target `Z` plaquette similarly becomes the product on both blocks.
The other two stabilizer sectors remain in place, so the joint stabilizer
group is preserved. Exactly the same mapping holds for each homological
logical pair, implementing CNOT separately on both encoded qubits.

`reproduce.py` constructs the doubled symplectic stabilizer space, performs
this conjugation, checks equality of row spaces, and checks every selected
logical generator. This proves the code-space action. It does not prove that a
given device can align blocks, suppress transport faults, or decode correlated
two-block events.

## Claimed single-block Clifford protocol

`guernut2024toric` proposes and simulates a constant-depth Toric Clifford
toolkit combining fold-transversal gates, Dehn twists, and single-shot logical
Pauli measurements. These ingredients require geometric pairings,
cellulation-deformation schedules, ancillas, and decoding assumptions absent
from the static constructor. The card therefore marks the toolkit and logical
measurement as `{kind: claimed, ref: guernut2024toric}`.

`bravyi2013classification` supplies a boundary rather than an implementation:
locality-preserving constant-depth logical gates for two-dimensional
topological stabilizer codes are restricted to the Clifford level. A
non-Clifford protocol for a broader abelian phase may add twists or enriched
structure, as in `bauer2025nonclifford`; it is not a native operation of the
unmodified square Toric stabilizer. T144 consequently adds no bare `T` gate.

## Hardware evidence ledger

| Source | Demonstrated object | Quantitative identity | Explicit non-claim |
|---|---|---|---|
| `bluvstein2022processor` | Neutral-atom preparation and characterization of a Toric-code state on periodic geometry | A twenty-four-qubit Toric state in the experiment's transported-atom processor | Not repeated syndrome extraction, arbitrary logical-state memory, or below-threshold scaling |
| `atomcomputing2026toric` | Repeated mid-circuit Toric syndrome extraction with lost-atom replacement and reservoir reloading | Logical error characterized through as many as ninety cycles; two code distances compared only through eight rounds, with lower absolute logical error for the larger distance in that range | Not an asymptotic or model-independent threshold claim |

Both rows are `demonstrated` because the reported protocols ran on hardware.
The descriptions remain different because demonstration status does not erase
the distinction between state preparation and active error correction.

## Reader decision procedure

When encountering a Toric operation or experiment, ask in this order:

1. Is the statement only a logical symplectic action, or is there a physical
   protocol?
2. If physical, what geometry, ancilla, measurement, and decoder resources are
   assumed?
3. Is fault tolerance proved, simulated, or measured?
4. For hardware, was a code state prepared, were syndromes repeated, was an
   unknown logical state preserved, and was distance scaling established over
   a declared range?

This sequence prevents a valid algebraic gate from becoming an unsupported
hardware claim and prevents a finite experiment from becoming a universal
threshold statement.

Primary sources: `kitaev2003fault`, `bravyi2013classification`,
`guernut2024toric`, `bauer2025nonclifford`, `bluvstein2022processor`, and
`atomcomputing2026toric`.
