# Surface-code threshold ledger

> **Rule.** A threshold number is meaningless without its elementary fault
> model, syndrome model, decoder, and normalization.

The regimes below are deliberately not merged into one “surface-code
threshold.”

### Code capacity, optimal

- **Model and decoder:** independent X or Z data errors, perfect syndrome,
  and class-probability/maximum-likelihood decoding.
- **Reported value:** about `10.9%`.
- **Provenance:** [Dennis–Kitaev–Landahl–Preskill](https://arxiv.org/abs/quant-ph/0110143).

### Code capacity, minimum energy

- **Model and decoder:** the same perfect-syndrome setting, using the
  zero-temperature/minimum-chain approximation associated with matching.
- **Reported value:** `0.1031 ± 0.0001`.
- **Provenance:** [Wang–Harrington–Preskill](https://arxiv.org/abs/quant-ph/0207088).

### Phenomenological spacetime

- **Model and decoder:** repeated data and syndrome errors in the
  random-plaquette gauge/matching model.
- **Reported value:** `0.0293 ± 0.0002` in the quoted symmetric convention.
- **Provenance:** [Wang–Harrington–Preskill](https://arxiv.org/abs/quant-ph/0207088).

### Scheduled circuit

- **Model and decoder:** Fowler's specified eight-step syndrome circuit and
  per-step stochastic fault model.
- **Reported value:** `p_th=0.57%` per step, roughly `4%` per full eight-step
  cycle.
- **Provenance:** [Fowler–Mariantoni–Martinis–Cleland](https://arxiv.org/abs/1208.0928).

### Hardware fit

- **Model and decoder:** Google Willow rotated memories with the device's
  measured heterogeneous noise and real-time decoder.
- **Reported value:** `Λ=2.14 ± 0.02` per `d→d+2`; distance seven at
  `0.143% ± 0.003%` per cycle.
- **Provenance:** [Google Quantum AI, 2024](https://arxiv.org/abs/2408.13687).

## 1. Why `10.9%` and `10.3%` differ

For a fixed syndrome, the probability of a logical class is a sum over all
error chains in that class. In the random-bond Ising mapping this is a
partition function. Optimal decoding compares free energies on the Nishimori
line. A minimum-chain decoder compares energies and discards most of the
entropy from nearly degenerate paths. The numerical gap is therefore a
decoder/statistical-mechanics distinction within one perfect-syndrome model,
not experimental uncertainty on one number.

## 2. Why `2.9%` is not a gate threshold

Adding noisy syndrome bits creates a time direction and a
three-dimensional matching/gauge problem. A phenomenological “data error per
round” and “measurement-bit flip per round” do not specify physical
preparation, CNOT, idle, leakage, reset, or readout locations. The resulting
threshold is valuable for decoder physics but cannot be compared directly
with a circuit-location threshold.

## 3. Why the `0.57%` conversion uses eight steps

The cited Fowler simulation defines `p` per step and explicitly uses eight
steps per cycle. Its quoted “roughly four percent per cycle” is the
conversion for that model. A different six-layer circuit may also be a valid
surface-code schedule, but one may not attach Fowler's eight-step conversion
to it without rebuilding the noise accounting.

## 4. Scaling below threshold

For simple independent models, the leading low-`p` logical failure mechanism
needs `⌈d/2⌉` faults, motivating an empirical form

`p_L ≈ A (p/p_th)^⌈d/2⌉`.

Increasing odd distance by two then contributes roughly one further factor
of `p/p_th`, before prefactors, degeneracy, correlations, and finite-size
effects. Hardware `Λ` is fitted from the complete device-and-decoder stack.
It should not be identified exactly with `p_th/p`.

## 5. Citation discipline

When a new threshold is added to the Atlas, record:

1. data-error channel;
2. whether syndrome is perfect, phenomenological, or circuit-derived;
3. complete circuit-location convention if applicable;
4. decoder and whether it uses correlations/degeneracy;
5. normalization: per location, step, round, cycle, or unit time.

Without those five fields, retain the number in the literature sweep rather
than promoting it into reader-facing content.
