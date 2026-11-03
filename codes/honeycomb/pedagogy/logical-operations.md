# Logical operations from automorphisms, twists, and geometry

Floquet logical operations act by transporting an encoded space through a
sequence of code frames. They are not ordinary transversal gates on one
fixed stabilizer block.

## Native electric-magnetic exchange

After each round, contracting the measured matching exposes an instantaneous
toric frame. Composing the three frame changes around one period exchanges
the toric anyons `e` and `m`. A logical winding string of electric character
is transported to magnetic character, and vice versa.

The operation is protected because it is induced by a local path through
topologically ordered frames. Its physical cost is continued execution of the
memory schedule plus classical tracking of measurement outcomes and logical
representatives. Two periods restore the anyon label. This is the first
operation recorded in `card.yaml`.

## Twist-defect processing

[Floquet Codes with a Twist](https://arxiv.org/abs/2306.08027) introduces
fermion-condensation lines whose endpoints are twists. Schedule deformations
can create, move, fuse, and braid these endpoints while keeping two-body
measurements and trivalent connectivity.

The logical action belongs to the topology of defect worldlines, but fault
tolerance still requires repeated syndrome extraction around the moving
defects. A static picture of twist locations does not specify hook errors,
time separation, or decoder boundaries.

[Floquet Codes and Phases in Twist-Defect Networks](https://arxiv.org/abs/2303.17664)
places these operations in a broader classification of phases and anyon
permutations. The classification tells which automorphism is possible; it
does not by itself provide the hardware resource count.

## Cross-cap geometry

[Kobayashi and Zhu](https://arxiv.org/abs/2310.06917) place the honeycomb
Floquet code on a non-orientable cross-cap. One schedule period acts as
logical `HZ` on the single encoded qubit in their convention. Folding turns
the nonlocal identification into a bilayer geometry.

This gate is not a property of the ordinary orientable torus instance. Its
resource contract includes the cross-cap or folded bilayer connectivity,
schedule, and decoder adapted to that geometry.

## Fixed-point and automorphism frameworks

Automorphism codes describe a protected loop in the space of gapped
Hamiltonians or code frames. Fixed-point path-integral circuits generalize the
idea to broader non-chiral Abelian topological phases and can include
non-Clifford ingredients. These frameworks explain how to design logical
action, but applying them to the original honeycomb memory requires an
explicit schedule and fault-tolerance analysis.

## What is not claimed

The fetch-verified sweep found no complete universal, fully benchmarked
logical gate set for the unmodified planar Hastings-Haah honeycomb memory.
Three nearby results must remain separate:

- Floquet color-code fold and twist gates use a different dynamical family;
- Floquet-Bacon-Shor experiments demonstrate dynamical logical control on a
  different code;
- general non-Clifford fixed-point circuits require added phase resources and
  are not operations of the bare three-round schedule.

The card therefore records only the native anyon exchange, twist-defect
processing, and cross-cap `HZ`, each with its own mechanism and geometry.

## How to verify a proposed operation

A complete operation certificate needs:

1. input and output ISGs;
2. a logical Pauli basis in both frames;
3. redressing rules through every measurement round;
4. the induced symplectic map on logical Paulis;
5. detector definitions during the deformation;
6. a fault-distance or malignant-fault analysis;
7. geometry, time, ancilla, and routing costs.

The current constructor certifies only the undeformed periodic memory.
