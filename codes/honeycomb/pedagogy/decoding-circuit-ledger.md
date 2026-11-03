# Decoder and circuit ledger

“Decoded by matching” is incomplete. The graph, weights, correlation
approximation, circuit, and noise normalization determine the actual decoder
experiment.

## Core periodic-memory construction

[Gidney, Newman, Fowler, and Broughton](https://arxiv.org/abs/2108.10457)
derive two interleaved spacetime matching graphs for the honeycomb memory.
Detector events are vertices. Single modeled faults connect the detectors
they can trigger, and edge weights come from the circuit-level fault
probabilities. Correlation-aware minimum-weight perfect matching then chooses
a likely fault class consistent with the observed boundary.

The paper reports threshold ranges of approximately:

- `0.2%--0.3%` for its six-step CNOT-based parity circuit;
- `1.5%--2.0%` for its native entangling-measurement model.

These are literature claims under the paper's respective noise
normalizations. They are not recomputed by `constructor.py`, and the
difference between the ranges is evidence that “Honeycomb threshold” is not a
well-defined phrase without the circuit model.

## Planar benchmark models

[Benchmarking the Planar Honeycomb Code](https://arxiv.org/abs/2202.11845)
separates SD6, SI1000, and EM3 circuit assumptions. They differ in native
operations, error locations, and normalization. Opening the torus also adds
spatial boundary nodes and changes which fault chains are logically
nontrivial.

Consequently, a fair comparison must hold fixed:

- the planar patch and boundary types;
- the number of syndrome rounds and temporal boundary rules;
- the circuit schedule and native operation set;
- the probability assigned to each fault location;
- decoder correlation handling;
- whether performance is quoted per logical qubit, per round, or per unit
  spacetime volume.

## Majorana-native models

[Paetznick et al.](https://arxiv.org/abs/2202.11829) construct explicit
Majorana parity-measurement circuits and their detector models. Poisoning and
correlated parity faults do not map term-for-term onto depolarizing
two-qubit-gate noise. The hardware motivation—native weight-two parity—is
therefore also a warning against importing a superconducting threshold.

## Biased noise and changed schedules

The [X3Z3 variant](https://arxiv.org/abs/2411.04974) changes the Pauli pattern
to preserve bias. Its detector symmetry and matching simplifications belong
to that variant, not to the unmodified Hastings-Haah schedule. Setiawan and
McLauchlan also identify an obstruction to reducing the studied two-body
dynamical class to one-dimensional decoding graphs. A favorable bias does
not automatically make the original honeycomb graph one-dimensional.

## Leakage and dynamic circuits

[A Dynamic Circuit for the Honeycomb Floquet Code](https://arxiv.org/abs/2507.08069)
changes physical roles during the cycle so measured/reset qubits remove
leakage and timelike distance improves. Once the circuit changes, detector
definitions and graph weights must be regenerated. “Same ideal edge
measurements” does not imply “same fault-tolerant code.”

## Beyond pair matching

One physical fault may activate more than two detectors. A graph decoder
either decomposes such correlations into weighted edges or supplements
matching with correlation updates. Hypergraph or logical-class methods can
retain different information. The
[2026 worm-decoder work](https://arxiv.org/abs/2603.05428) includes honeycomb
Floquet examples by sampling logical-class probabilities, but this is a
research decoder rather than a replacement for the registered standard MWPM
row.

## Acceptance checklist for a number

Before copying any threshold or logical-error rate, require all of:

1. exact code variant and boundary;
2. ideal measurement schedule;
3. physical parity circuit;
4. noise channel and probability normalization;
5. detector construction;
6. decoder and correlation treatment;
7. size/time scaling and fitted observable.

If any item changes, the number is a new experiment. `card.yaml` therefore
stores circuit-qualified decoder notes rather than a bare threshold field.
