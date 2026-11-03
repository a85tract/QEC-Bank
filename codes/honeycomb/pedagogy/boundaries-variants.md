# Boundaries and variant axes

Honeycomb geometry, Pauli schedule, boundary termination, qudit dimension,
and physical circuit are independent design axes. This map prevents results
from one axis choice from being silently attached to another.

## Open boundaries

[Planar Floquet Codes](https://arxiv.org/abs/2110.05348) shows why a large
instantaneous distance is not enough: short spacetime fault paths can use a
boundary and the measurement order. Boundaries must be designed together
with detectors.

[Boundaries for the Honeycomb Code](https://arxiv.org/abs/2110.09545) gives
terminations compatible with the original Pauli pattern and planar logical
encodings. This Atlas constructor implements only closed tori. It does not
infer a planar patch by deleting wraparound edges because doing so would omit
boundary checks, schedule changes, detector endpoints, and readout rules.

## Pauli-pattern variants

- **CSS honeycomb.**
  [Davydova, Tantivasadakarn, and Balasubramanian](https://arxiv.org/abs/2210.02468)
  introduce schedules with CSS measurements and no parent subsystem code. The
  shared lattice does not make its ISG, detector graph, or gate set identical
  to the Hastings-Haah code.
- **X3Z3.**
  [Setiawan and McLauchlan](https://arxiv.org/abs/2411.04974) tailor a
  dynamical code to biased noise and retain a stabilizer-product symmetry. Its
  bias performance belongs to its changed Pauli pattern and circuits.
- **Aperiodic dynamic trees.** Switching among schedules changes the temporal
  code itself; period-three rank checks do not certify an aperiodic protocol.

## Geometry variants

- **Hyperbolic Floquet codes.**
  [Negative-curvature constructions](https://arxiv.org/abs/2309.10033) trade
  Euclidean locality for finite rate and logarithmic distance. A reported
  `[[400,52,8]]` instance and its thresholds are properties of that hyperbolic
  family, not a large honeycomb torus.
- **Twist networks.** Condensation lines and twist endpoints change the defect
  content while retaining trivalent connectivity and two-body measurements.
- **Three-dimensional descendants.** Tricoordinated 3D schedules can realize
  fermionic toric or fracton orders with different logical sectors. They are
  not additional `(L1,L2)` instances of this entry.

## Hardware and fabrication variants

[McLauchlan, Gehér, and Moylett](https://arxiv.org/abs/2405.15854) remove
defective qubits and stabilizers without adding connectivity, then simulate
planar performance under a fabrication-defect model. Their roughly `12%`
fabrication-defect tolerance is tied to that prescription and model. Deleting
a vertex from the torus constructor without implementing the compensating
schedule would not reproduce it.

[Claes's dynamic circuit](https://arxiv.org/abs/2507.08069) changes which
physical qubits act as data and measurement resources. Majorana and
spin-photonic proposals change the native fault alphabet. These are circuit
variants even when the ideal parity graph looks familiar.

## Qudit and defect generalizations

Twist constructions extend the schedule to `Z_N` qudits and use
fermion-condensation lines for protected processing. Qudit commutation phases,
detector values, and decoder alphabets differ from binary symplectic
arithmetic. The present `Pauli` and `CheckMatrix` objects are qubit-only and
do not machine-certify those variants.

## Transfer matrix

| claim | torus original | planar original | CSS/X3Z3 | hyperbolic/qudit |
|---|---|---|---|---|
| local weight-two ideal checks | yes | often | often | construction-dependent |
| shipped `dynamic_k = 2` | yes | no transfer | no transfer | no transfer |
| torus face-color constraint | yes | boundary removes it | schedule-dependent | geometry-dependent |
| periodic MWPM graph | source model | rebuild boundaries | rebuild Pauli/circuit model | rebuild geometry |
| original anyon exchange | source result | boundary action needs analysis | variant-dependent | phase-dependent |

The safe rule is simple: locality may transfer as motivation; logical counts,
distance, thresholds, and operations require a fresh certificate.
