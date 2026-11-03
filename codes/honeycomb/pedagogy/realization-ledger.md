# What hardware has and has not demonstrated

The word “realized” covers several distinct milestones. This ledger attaches
each source to the strongest claim its protocol supports.

## Literal honeycomb experiment

[Measurements of Floquet Code Plaquette Stabilizers](https://arxiv.org/abs/2210.13154)
implemented measurements associated with the original honeycomb Floquet code
on IBM Falcon hardware and used changes in inferred plaquette stabilizers as
a noise diagnostic.

Established:

- hardware execution of the relevant parity-measurement pattern;
- reconstruction of plaquette information from outcomes;
- empirical syndrome-change behavior on the tested device.

Not established:

- a full encoded logical honeycomb memory;
- repeated logical error suppression;
- improvement with increasing distance;
- a below-threshold regime;
- logical gates.

The manuscript describes itself as a preliminary study not intended for
journal submission. `card.yaml` records the hardware execution as
`demonstrated` while stating the restricted claim boundary.

## Majorana parity-measurement architectures

Majorana tetrons motivate the code because fermion-parity measurements can be
native. [Karzig et al.](https://arxiv.org/abs/1610.05289) develop scalable
protected parity-measurement hardware, while
[Paetznick et al.](https://arxiv.org/abs/2202.11829) build planar Floquet
circuits, Majorana fault models, detectors, and overhead comparisons.

These works establish detailed architecture and simulation evidence. They do
not report a laboratory logical honeycomb memory. Poisoning, parity
correlations, and device constraints are part of their conclusions and cannot
be replaced by generic depolarizing noise.

## Spin-optical photonic proposal

[Dessertaine et al.](https://arxiv.org/abs/2410.07065) co-design a photonic
architecture and numerically report a `6.4%` photon-loss threshold for their
Floquet implementation. This number is a simulated architecture threshold
under a tailored loss model. It is not a laboratory threshold and does not
transfer to Majorana or superconducting circuits.

## Fabrication-defect and dynamic-circuit proposals

[McLauchlan, Gehér, and Moylett](https://arxiv.org/abs/2405.15854) provide a
schedule-preserving prescription for removing faulty hardware locations and
simulate tolerance to fabrication defects.
[Claes](https://arxiv.org/abs/2507.08069) proposes an ancilla-free dynamic
circuit with changing data/measurement roles, leakage removal, and improved
timelike distance.

Both are executable design advances. Neither is a hardware demonstration.
Each changes the detector model compared with the ideal torus constructor.

## Adjacent Floquet experiment

The
[Floquet-Bacon-Shor dynamical-qubit experiment](https://arxiv.org/abs/2503.03867)
demonstrates universal logical operations with periodic measurements on
superconducting hardware. It is evidence that Floquet control primitives can
work experimentally, but it is a different code with different geometry,
schedule, logical count, and detectors. It is intentionally absent from the
Honeycomb `realizations` facet.

## Status as of the literature sweep

As of the fetch-verified 2026-07-26 sweep, no qualifying experiment
demonstrated a full logical honeycomb memory with repeated error suppression,
distance scaling, or logical gates. This negative result is part of the
entry's knowledge boundary, not a missing citation.
