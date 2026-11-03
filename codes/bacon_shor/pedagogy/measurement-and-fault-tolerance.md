# Gauge measurement and fault-tolerance boundaries

The algebra says a center strip is a product of local gauge generators. A
fault-tolerant protocol must additionally say when those factors are measured,
which outcomes are multiplied, how measurement faults are detected, and what
history reaches the decoder.

## Reconstructing one center outcome

All X-type gauge generators commute with one another. In an X-gauge round,
measure the `c` vertical pairs crossing a fixed adjacent-row gap and record
outcomes `m^X_{i,j}` in `{+1,-1}`. Their product is the eigenvalue of the
X-center strip:

$$\sigma^X_i=\prod_{j=0}^{c-1}m^X_{i,j}.$$

Likewise, in a Z-gauge round the product of the `r` horizontal-pair outcomes
across one adjacent-column gap gives

$$\sigma^Z_j=\prod_{i=0}^{r-1}m^Z_{i,j}.$$

`reproduce.py` verifies the operator identities by XORing the corresponding
symplectic gauge rows and comparing the exact constructor stabilizer rows.
This proves the noiseless product rule. It does not certify a measurement
circuit.

## Why raw gauge outcomes are not persistent syndrome bits

An X gauge edge and a Z gauge edge that meet once anticommute. Measuring the Z
edge after the X edge may randomize the earlier X gauge eigenvalue. The center
product survives because it commutes with every gauge generator, but the
individual factor history depends on time order.

A circuit-level detector therefore needs at least:

1. an ordered X/Z gauge schedule;
2. a convention identifying which same-type outcomes form one center sample;
3. repeated samples or other redundancy for measurement faults;
4. data-error propagation rules for each ancilla interaction;
5. a decoder mapping the resulting spacetime record to a protected logical
   correction modulo gauge.

Multiplying one X-round outcome with a later Z-round outcome has no
schedule-independent meaning. Even comparing the same gauge factor at two
times is safe only after the intervening measurements and detector convention
are specified.

## Four decoder inputs that must not be conflated

| regime | data presented to the decoder | statement licensed |
|---|---|---|
| perfect static gauge readout | exact center parities derived from exact pair outcomes | two finite classical repetition decisions modulo gauge |
| repeated low-weight extraction | a time history of pair outcomes, repetitions, and possibly flags | performance of that named extraction circuit and recovery rule |
| encoded-ancilla Steane extraction | encoded-ancilla verification plus blockwise extraction outcomes | comparison with other complete ancilla/extraction protocols |
| period-four Floquet descendant | constant-weight spacetime detectors from the scheduled dynamical code | performance and logical behavior of the descendant, not the static center |

The first row is derived on the
[distance/decoding page](dressed-distance-and-decoding.md). The other rows are
literature claims because their circuit, noise, and postprocessing layers are
not exported by this static constructor.

## Repeated pair extraction

Low gauge weight limits how many data qubits one ancilla interaction chain
touches, but "weight two" is not itself fault tolerance. A fault can occur on
the ancilla, a two-qubit gate, preparation, measurement, idling data, or a
classical record. Repeating gauge measurements supplies time redundancy, and
the decoder must infer a protected center history despite local gauge values
that may legitimately change.

Cross, DiVincenzo, and Terhal (`cross2009comparative`) provide the fixed-block
repeated-syndrome/majority baseline. Its performance belongs to the complete
small-block circuit and stochastic model. It is not a universal property of
the `3 × 3` check matrix.

## Encoded-ancilla extraction

Steane-style extraction couples an encoded ancilla block transversally rather
than measuring every gauge pair with an individual bare ancilla. The ancilla
preparation, verification, coupling direction, measured block, accepted
histories, and recovery rule define a different syndrome object.

Escobar-Arrieta and Gutiérrez (`escobar2025improved`) compare this route with a
Shor-style extraction protocol. The comparison cannot be transferred to an
unspecified "Bacon–Shor decoder" because changing extraction changes both the
fault locations and the available side information.

## Self-concatenated surgery and Floquet detectors

`gidney2023less` obtains threshold behavior from local lattice-surgery
circuits arranged in a self-concatenating construction. The fitted family is
the circuit construction, not a direct sequence of increasingly large static
rectangles under an unspecified stabilizer measurement.

`alam2025board` instead defines a period-four measurement schedule with
constant-weight spacetime detectors and applies matching under a uniform
circuit-level model. Time-dependent checks and logical representatives are
part of that code definition. The scheduled descendant is therefore recorded
as an R3 view, not as a schedule exported by this static entry.

## Threshold identity boundary

This packet quotes no threshold-like number. Before any future number enters,
the full identity tuple must include:

1. static rectangle, concatenated circuit, or Floquet descendant;
2. scaling variable and fitted logical observable;
3. exact extraction circuit or measurement schedule;
4. noise model and normalization per location or round;
5. decoder, repetition/postselection rule, and version;
6. source figure, table, or section;
7. threshold, pseudo-threshold, one-point logical rate, bound, or hardware
   result.

The 2026-08-02 decoder sweep found no extraction-independent threshold for
plain unspecified static stabilizer products. That dated negative result does
not say no Bacon–Shor-derived protocol has a threshold; it says the protocol
identity cannot be erased.

## Source ledger

- `aliferis2007subsystem`: low-weight gauge extraction and subsystem
  fault-tolerant gadgets.
- `cross2009comparative`: repeated-syndrome fixed-block circuit baseline.
- `napp2013optimal`: perfect-readout biased-noise decoding and rectangle
  optimization, with model-dependent optima.
- `escobar2025improved`: complete encoded-ancilla versus Shor-style extraction
  comparison.
- `gidney2023less`: self-concatenated local-surgery threshold construction.
- `alam2025board`: scheduled period-four detectors and MWPM for the Floquet
  descendant.

Every bibkey resolves in `registry/refs.yaml`; the fetch-verification details
and dated searches are retained in `docs/lit/bacon_shor/`.
