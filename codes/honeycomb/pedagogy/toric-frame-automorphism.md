# The instantaneous toric frame and its anyon automorphism

The steady ISG is locally equivalent to a toric code after every round, but
the equivalence itself moves. Keeping those two facts together explains both
memory and logical-frame motion.

## Contract the latest matching

Immediately after round `r`, every measured edge in matching `M_r` has a
known two-qubit parity. Regard its two endpoints as one effective qubit.
Because `M_r` is a perfect matching, this contraction covers the lattice
without overlap.

The measured parity fixes one Pauli degree of freedom inside each pair. A
depth-one product of two-qubit Clifford changes of basis can send that parity
to a single-qubit stabilizer on an auxiliary degree of freedom, leaving the
other degree of freedom as the effective qubit. This is a local change of
basis, not a projection that discards logical information.

Under this map:

- products of neighboring honeycomb plaquettes become one family of toric
  stabilizers;
- compatible products involving the current matching become the conjugate
  family;
- noncontractible dressed strings become toric winding strings.

The resulting torus has two anticommuting winding pairs and therefore two
logical qubits. Hastings and Haah give the explicit local-Clifford
identification in
[Dynamically Generated Logical Qubits](https://arxiv.org/abs/2107.02194).
The Atlas constructor currently verifies the ISG rank, not the Clifford
circuit, so `card.yaml` marks this view as curated.

## Logical representatives must be redressed

A fixed physical Pauli string need not commute with the next round. If a
representative crosses an incoming measured edge with the wrong local Pauli,
multiply it by current ISG generators until it commutes with the entire
incoming matching. Multiplication changes the physical string but not its
logical class in the current code.

This redressing is the logical-operator analogue of the generator update in
the ISG tracker. It is why the statement “the same logical string survives”
is misleading. What survives is an equivalence class transported through a
sequence of changing stabilizer quotients.

## One period exchanges electric and magnetic labels

The effective toric lattice after round `r+1` is not identified with the
effective lattice after round `r` by the identity map. Composing the three
local changes of frame around one period exchanges the electric and magnetic
anyon types:

`e -> m`, `m -> e`, and `em -> em`.

On logical Paulis, the same action exchanges the two conjugate winding
characters, up to the chosen cycle basis and outcome-dependent Pauli frame.
The anyon label therefore closes after two periods, not one.

This is a protected automorphism of the topological order, as organized by
[Aasen, Wang, and Hastings](https://arxiv.org/abs/2203.11137). It is a logical
operation performed by continued memory cycling, but it is not a claim that
every physical logical representative literally returns after six rounds.

## What the equivalence does not imply

The instantaneous toric frame establishes:

- topological order at a fixed steady time;
- two torus logical qubits;
- string-like logical representatives and their anyon labels;
- a local route for comparing consecutive frames.

It does not establish:

- the detector graph of a noisy parity-measurement circuit;
- circuit fault distance or threshold;
- the behavior of a planar boundary;
- a complete universal logical gate set;
- equivalence to the static Kitaev honeycomb Hamiltonian dynamics.

Those require spacetime, boundary, or circuit data. The distinction is why
`instances.yaml` verifies `k` and `dynamic_k` but leaves `d` unclaimed.

## A useful transport test

To analyze a proposed schedule modification:

1. identify the effective code after each round;
2. choose a basis of logical winding classes;
3. redress each representative to commute with the next measurements;
4. express the transported classes in the next basis;
5. compose the induced symplectic maps over the full period.

Preserving the ISG rank checks only that information survives. The composed
map determines what logical automorphism was performed.
