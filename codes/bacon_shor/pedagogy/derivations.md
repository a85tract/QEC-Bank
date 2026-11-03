# Bacon–Shor — Level-2 map

The phrase "local subsystem repetition code" compresses several different
statements. These pages separate the algebra that is recomputed from the
protocol claims that remain tied to literature.

1. [Gauge group, center, and subsystem qubit count](gauge-center-and-qubits.md):
   the declared orientation, pair-generator ranks, strip stabilizers,
   noncommutation, center containment, protected-qubit count, and gauge-qubit
   count.
2. [Dressed distance and the two repetition decoders](dressed-distance-and-decoding.md):
   row/column parity quotients, exact sector lower bounds and witnesses,
   bare-versus-dressed representatives, and worked perfect-syndrome tables.
3. [Gauge measurement and fault-tolerance boundaries](measurement-and-fault-tolerance.md):
   reconstructing center outcomes from pair measurements, why time order is
   decoder data, and why static, encoded-ancilla, concatenated, and Floquet
   performance claims cannot be merged.
4. [Operations, gauge fixing, and variants](operations-gauge-fixing-and-variants.md):
   pairwise CNOT, square-block Hadamard with transposition, exact Shor
   row-space recovery with the logical-label dictionary, and the resources
   consumed by cited non-Clifford and surgery mechanisms.
5. [Representation and realization ledger](representations-and-realizations.md):
   compass, tensor, frustration-graph, autonomous, and Floquet dictionaries;
   static trapped-ion versus dynamical superconducting evidence; and explicit
   non-equivalences.

## Reproduction contract

Run from the repository root:

```bash
source .venv/bin/activate
python atlas/bacon_shor/pedagogy/reproduce.py
make verify-entry E=atlas/bacon_shor
```

`reproduce.py` builds all three shipped rectangles and independently derives
their gauge and center support matrices. It asserts generator counts and
ranks, center containment, noncommuting local pairs, protected and gauge
dimensions, bare logical commutation, exact pure-X and pure-Z dressed
distances, repetition-syndrome factorization, pair-outcome reconstruction,
square-block Hadamard/transposition symmetry, the exact Shor gauge-fixed row
space and logical-label swap, scene/tour integrity, and T3 packet state.

The shared `qeclib.distance` API now minimizes physical Pauli weight in
`C(S)/G`: exact search finishes complete weight layers and the verifier
recomputes the three shipped finite `d` claims. The committed evidence rows
also retain one seeded `5 × 7` witness of achieved weight `12` as
`bounded`, with method `rand-subsystem-dressed-logical-coset-v1`, seed `17`,
and `not-certified` optimality. The independent witness gate checks
stabilizer commutation, gauge nontriviality, and physical weight. This row is
not a lower bound, an exact distance, or evidence for the family formula.

The card also omits a `construction:` tree. No registered operation adapter
currently expresses the rectangular pair-gauge construction with exact row
and qubit order. The deterministic constructor and this transcript establish
the shipped presentation without pretending that an unsupported generic
replay exists. The broader problem of certifying equality across gauge-fixed,
subsystem, and subspace presentations is tracked by
`wanted:code-equivalence`; the exact square-to-Shor row-space witness on this
entry is evidence for one pair, not a general canonicalizer.

## Provenance split

- **Recomputed facts:** qubit order; local gauge and center supports; all
  finite-instance ranks; center/gauge containment; `n=rc`, `k=1`, and
  `(r-1)(c-1)` gauge qubits; bare logical row/column algebra; exact pure-sector
  dressed distances for the shipped rectangles; repetition quotient and
  single-error syndrome tables; center-outcome products; square
  Hadamard/transposition mapping; exact `3 × 3` gauge-fixed Shor stabilizer
  row space and the cross-entry logical-label dictionary; constructor-derived
  scene and tour data.
- **Bounded facts:** the committed `5 × 7`, seed-`17`, `32`-trial search
  achieves a weight-`12` dressed-logical representative and independently
  validates it. Its only guarantee is an upper bound; optimality is explicitly
  `not-certified`.
- **Literature claims:** historical subsystem construction; fault-tolerant
  extraction and decoder behavior beyond perfect gauge outcomes; biased-noise
  optimization; thresholds or logical rates of named circuits; transversal
  controlled-phase families; surgery, teleportation, deformation, and
  autonomous-dynamics resources; compass, tensor, and frustration-graph
  dictionaries; and every hardware demonstration.

No threshold, pseudo-threshold, one-point logical error rate, or device error
rate is quoted in this packet. Dated negative findings are retained at the
reader-facing location where they are used.
