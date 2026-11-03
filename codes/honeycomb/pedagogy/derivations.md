# Honeycomb Floquet code — Level-2 map

The schedule, instantaneous code, spacetime detector model, and physical
circuit answer different questions. This index keeps their claims separate
and links each long argument exactly once.

1. [From plaquette coloring to a periodic ISG](schedule-isg-cycle.md):
   the two edge labels, perfect-matching proof, weight-six plaquette
   invariants, startup rank profile, steady rank count, torus-coloring
   constraint, and the direction-grouped anti-test.
2. [The instantaneous toric frame and its anyon automorphism](toric-frame-automorphism.md):
   contraction of the latest matching, the effective toric stabilizers,
   winding logicals, redressing between rounds, and the electric-magnetic
   exchange after one period.
3. [Detectors and distance live in spacetime](spacetime-detectors-distance.md):
   how random edge outcomes become plaquette detectors, why snapshot distance
   is insufficient, and what a future machine verifier must compute.
4. [Decoder and circuit ledger](decoding-circuit-ledger.md):
   correlated matching, circuit/noise-model boundaries, threshold
   normalization, leakage, and the quantitative claims that must not be
   transferred between models.
5. [Boundaries and variant axes](boundaries-variants.md):
   planar termination, CSS, X3Z3, hyperbolic, twist, qudit, fabrication-defect,
   and higher-dimensional relatives, with an explicit map of non-transferable
   claims.
6. [Logical operations from automorphisms, twists, and geometry](logical-operations.md):
   the native electric-magnetic frame cycle, twist-defect processing,
   cross-cap gates, and the boundary of the known gate set.
7. [What hardware has and has not demonstrated](realization-ledger.md):
   the literal IBM plaquette experiment separated from Majorana, photonic,
   dynamic-circuit, and adjacent Floquet evidence.
8. [Representation dictionary](representation-dictionary.md):
   schedule/ISG, instantaneous toric, Majorana, detector, anyon-automorphism,
   measurement-QCA, and ZX-spacetime views, including the conversions that
   remain curated.

## Reproduction contract

Run from the repository root:

```bash
source .venv/bin/activate
python atlas/honeycomb/pedagogy/reproduce.py
make verify-entry E=atlas/honeycomb
```

`reproduce.py` loads the shipped entry and recomputes both reference
instances, the `3 x 3` startup rank profile, steady periodic rank,
`dynamic_k`, perfect-matching and mixed-Pauli properties, the rank-eight
plaquette backbone, representative measurement supports, all small
torus-colorability decisions from dimensions two through nine, and the
`6 x 6` direction-grouped counterexample. The ordinary verifier separately
checks every structured claim in `instances.yaml`.

The `construction:` recipe now binds `L1,L2` into
`honeycomb_torus_schedule@1`, whose pinned convention fixes vertices, faces,
plaquette colors, rounds, and measurement order. The
`plaquette_colored_floquet@1` operation applies the fixed six-period ISG
burn-in and must reproduce the ordinary constructor's complete stabilizer
array for both shipped tori. Construction replay v1 compares that final
`CheckMatrix`; the reproduction transcript separately checks the intervening
schedule and phase-by-phase ISG facts.

## Provenance split

- **Recomputed facts:** `n`, snapshot `k`, non-CSS presentation, periodic
  `dynamic_k`, the full startup rank profile, round period and perfect
  matchings, equal `XX`/`YY`/`ZZ` counts within each round, plaquette weights
  and rank, the face-coloring constraint over the documented scan, and the
  direction-grouped anti-test.
- **Bounded facts:** none. The entry intentionally makes no static or
  spacetime `d` claim, so it does not attach a seeded witness to an
  inapplicable distance definition.
- **Literature claims:** instantaneous local-Clifford equivalence to toric
  code, electric-magnetic anyon exchange, detector constructions, thresholds,
  benign-error distance theory, boundary and variant behavior, logical
  operations, and every hardware result. Each depends on an analytical map,
  circuit, decoder, geometry, or device not reproduced by the current
  constructor.
- **Citation reconciliation:** the fetch-verified sweep used
  `hastings2021dynamical` and `gidney2021honeycomb`; the controlled registry
  records them as aliases of the canonical structured keys
  `hastings2021dynamically` and `gidney2021fault`. This entry uses the
  canonical keys.
