# Detectors and distance live in spacetime

An instantaneous stabilizer matrix describes which Pauli operators are known
at one time. A noisy Floquet memory is a history of parity measurements.
Distance must therefore distinguish harmless changes of that history from
undetectable histories that act logically.

## From random outcomes to a detector

An edge measurement outcome is not itself a syndrome bit. Even without
physical noise, measuring an operator outside the current ISG can produce a
fresh random sign. The useful invariant is a plaquette product assembled from
edge outcomes in the rounds where its factors were measured.

Let `s_p(t)` be the inferred sign of plaquette `p` after the required outcomes
have become available. A detector compares compatible inferences, for
example

`D_p(t) = s_p(t) s_p(t-Delta)`.

In an ideal history, `D_p(t)=+1`. A fault can flip a collection of nearby
detectors. The exact delay `Delta`, which outcomes enter `s_p`, and the
startup/readout rules belong to the measurement circuit. They are not stored
in the static `CheckMatrix`.

[A Fault-Tolerant Honeycomb Memory](https://arxiv.org/abs/2108.10457)
constructs the periodic detector graphs and correlation-aware matching
problem for explicit circuits. The Atlas schedule export stops one layer
earlier: it gives the ideal measured Paulis and their order.

## Why snapshot distance answers the wrong question

Suppose a Pauli error has low weight on one time slice. Three cases are
possible:

1. it creates detectors and is therefore visible;
2. it can be absorbed into changes of measurement outcomes or stabilizer
   representatives without changing encoded information;
3. it creates no detector but transports or flips a logical class.

Only the third case is a logical fault. A minimum-weight normalizer element
of one snapshot does not account for faulty measurements, errors extended
over several rounds, or equivalences that move faults through the measurement
history.

Blackwell and Haah formalize this distinction in
[The Code Distance of Floquet Codes](https://arxiv.org/abs/2510.05549).
Their distance minimizes the weight of an undetectable **non-benign**
spacetime error. Benign errors form the equivalence class that neither
changes detector data nor acts on the encoded information.

## Three quantities that must not be collapsed

| quantity | formal input | question answered |
|---|---|---|
| snapshot `k` | one steady ISG | how many logical qubits exist in this frame? |
| `dynamic_k` | repeated ideal schedule | how many logical qubits survive continued measurement? |
| circuit fault distance | full noisy spacetime protocol | what is the lightest undetectable non-benign fault history? |

The current Atlas engine recomputes the first two. It has no generic
spacetime benign-error quotient, so the third remains an honest gap. Recording
a static exact distance under property `d` would attach machine certainty to
the wrong object.

## What a replayable fault-distance artifact needs

A future verifier must receive at least:

1. preparation and final-readout conventions;
2. the physical measurement circuit for every ideal parity operator;
3. a named fault alphabet and location weights;
4. detector definitions, including temporal boundaries;
5. logical observables in the chosen input/output frames;
6. benign generators or an equivalent quotient rule;
7. an exact or bounded search with a replayable witness.

The result should be keyed by circuit and observation window, not placed as a
family-wide scalar on the honeycomb check matrix. This missing engine is
tracked by the project's Floquet fault-distance Wanted item.

## Decoder consequence

The instantaneous toric map is still useful: it predicts topological detector
structure and helps identify logical homology classes. It does not remove the
time coordinate. A matching graph for the honeycomb memory includes
spacelike and timelike edges, correlations from two-qubit measurements, and
special nodes at boundaries. Rebuilding that graph after a circuit change is
part of the code definition at the fault-tolerant level.
