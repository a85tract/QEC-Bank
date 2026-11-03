# Representation dictionary

No single representation makes every Honeycomb claim transparent. The useful
maps form a chain, and every arrow has a different proof status.

## Schedule and ISG

**Objects:** measured Pauli words grouped into ordered rounds; a commuting
binary symplectic row space updated after each outcome.

**Best for:** exact round content, commutation within a round, startup rank,
periodic rank, `dynamic_k`, and machine export.

**Atlas status:** executable. `constructor.py`, `Schedule`, and `ISGTracker`
recompute these facts.

**Blind spot:** physical outcome signs, preparation/readout circuits,
detectors, and geometry coordinates are not present.

## Plaquette backbone and moving matching

**Objects:** rank-eight span of weight-six plaquette products plus the
currently measured perfect matching.

**Best for:** understanding the steady ISG rank and why incompatible
measurements do not erase the code.

**Atlas status:** recomputed by `reproduce.py`; the first plaquette words and
all row-space memberships are asserted.

**Blind spot:** the logical anyon labels require the toric-frame conversion.

## Instantaneous toric code

**Map:** contract the just-measured matching and apply local Clifford changes
of basis.

**Best for:** two torus logical qubits, winding strings, topological order, and
the meaning of electric/magnetic labels.

**Atlas status:** curated from Hastings-Haah. The current engine checks the
rank consequence but does not replay the local Clifford circuit.

**Blind spot:** one frame omits measurement faults and logical transport
through time.

## Majorana / parton gauge theory

Represent a spin by four Majoranas `b^x,b^y,b^z,c` with a local parity
constraint. A directional edge term factors schematically as

`sigma_u^a sigma_v^a = (i b_u^a b_v^a)(i c_u c_v)`.

The first factor is a `Z2` gauge link and the second pairs matter Majoranas.
Plaquette products become gauge fluxes. Cycling measurements changes the
pairing pattern.

**Best for:** the local anticommuting edge algebra, gauge-invariant
plaquettes, and weak/coherent-measurement extensions.

**Atlas status:** curated from
[Kitaev](https://arxiv.org/abs/cond-mat/0506438) and
[later monitored-fermion work](https://arxiv.org/abs/2311.08450). There is no
generic fermionic compiler in the repository, so this view is not
machine-derived.

**Blind spot:** a static Kitaev Hamiltonian and a projective measurement
schedule have different dynamics.

## Spacetime detector model

**Map:** compile the physical parity circuit into measurement outcomes,
detector parities, logical observables, and fault-to-detector incidence.

**Best for:** matching, correlations, timelike boundaries, leakage, logical
error rates, and fault distance.

**Atlas status:** literature-curated. The ideal schedule is exported, but no
Honeycomb circuit/DEM is produced by this constructor.

**Blind spot:** detector graphs depend on the circuit and noise model; there
is no circuit-independent threshold graph.

## Anyon automorphism

**Map:** compose the local equivalences between consecutive instantaneous
topological frames.

**Best for:** the `e <-> m` exchange, logical-frame transport, twist defects,
and cross-cap gates.

**Atlas status:** curated from Hastings-Haah and the automorphism-code
framework.

**Blind spot:** naming an automorphism does not supply detector circuits or
hardware costs.

## Measurement QCA

**Objects:** a locality-preserving transformation of quantum information
induced by periodic measurement and classical outcomes.

**Best for:** anomalous boundary information flow and why bulk stabilizer rank
misses boundary dynamics.

**Atlas status:** curated from
[Aasen, Haah, Li, and Mong](https://arxiv.org/abs/2304.01277).

**Blind spot:** the classification is coarser than a device noise model.

## ZX spacetime

**Objects:** a graphical tensor network in which parity measurements,
preparations, fusions, and feed-forward are ZX nodes and connections.

**Best for:** relating circuit, measurement-based, fusion-based, and Floquet
protocols by local diagram rewrites.

**Atlas status:** curated from
[Bombin et al.](https://arxiv.org/abs/2303.08829); no Honeycomb ZX artifact
ships with the entry.

**Blind spot:** a local diagram equivalence preserves logical structure under
its assumptions, not the numerical noise performance of every physical
realization.

## Conversion ledger

| from | to | status in this entry |
|---|---|---|
| constructor schedule | ideal round/edge export | verified |
| schedule history | steady ISG snapshot | verified |
| face walks | plaquette row space | verified in reproduction |
| steady ISG | toric stabilizers | curated local-Clifford map |
| physical circuit | detector graph | cited, not exported |
| spin Paulis | Majorana gauge variables | curated dictionary |
| period of frames | anyon automorphism | curated |
| measurement protocol | ZX / measurement-QCA | curated |

This ledger prevents a derived rank from lending machine certainty to a
curated conversion farther down the chain.
