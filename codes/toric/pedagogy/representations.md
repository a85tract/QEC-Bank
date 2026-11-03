# What does each Toric representation preserve?

## One object, several dictionaries

The code is one stabilizer subspace, but different representations make
different invariants cheap to see. A responsible conversion states what is
preserved and what extra assumptions are introduced.

| Picture | Native object | Makes immediate | Does not provide by itself |
|---|---|---|---|
| Symplectic CSS | binary `HX`, `HZ` | commutation, rank, finite syndrome, row-space logical tests | geometry, circuit, or likelihood |
| Chain complex | `C2 -> C1 -> C0` | boundary cancellation, homology, primal/dual cycles | decoder probabilities or hardware schedule |
| Cyclic HGP | two square neighbor-parity maps | tensor-separated directions and two kernel sectors | identity with arbitrary HGP outputs |
| Anyon strings | charges, strings, intersections | endpoint motion, fusion, logical commutation | a finite check ordering or decoder runtime |
| Statistical mechanics | disorder sectors and partition functions | class likelihoods and phase transitions | one model-free threshold |
| PEPS | local tensors with virtual symmetry | topological degeneracy and local indistinguishability | active QEC or repeated syndrome circuits |
| Majorana simulation | quadratic fermionic evolution in restricted channels | efficient coherent-error calculation | a physical tetron realization or arbitrary coherent-noise decoder |

## Symplectic and chain-complex equivalence

The constructor takes the face boundary `d2` and edge boundary `d1`, then
emits `HX=d1` and `HZ=d2^T`. This conversion preserves the exact qubit and
check order. The identity `d1 d2=0` becomes `HX HZ^T=0`; chain cycles become
commuting Pauli rows, and chain boundaries become stabilizer products.

The symplectic picture forgets why the matrices commute but is ideal for
machine checks. The chain picture restores the geometric reason and gives the
quotient `ker/im` that classifies logicals.

## HGP is exact but factor-sensitive

The cyclic-HGP converter preserves the ordered matrices only for the stated
orientation `HGP(C_L,C_L^T)`. Open repetition factors change dimensions and
kernel sectors, producing the planar Surface witness. General HGP factors can
produce codes with no two-dimensional local embedding. The exact dictionary
therefore supports a typed construction relation, not a claim that Toric and
HGP are synonyms. See [cyclic HGP](cyclic-hgp.md).

## Anyons and statistical mechanics

The anyon dictionary turns a violated star or plaquette into an endpoint
charge. Local Pauli errors create pairs; extending a string moves an endpoint;
closing and winding the string performs a logical. It preserves fusion and
intersection information but suppresses the row ordering used by software.

The statistical dictionary fixes a syndrome and groups compatible error
chains by homology. A disorder-sector partition function sums the probability
of a class. The critical point depends on the channel and syndrome model, so
the representation explains thresholds only after the model tuple is fixed.
`dennis2002topological` supplies the direct QEC mapping, while earlier Ising
papers remain classical precursors.

## PEPS and Majorana boundaries

In a PEPS representation, a virtual `Z2` symmetry makes distinct torus sectors
locally indistinguishable and produces topological degeneracy
[`schuch2010peps`]. This is a ground-space representation. It does not imply
that preparing the PEPS, measuring syndromes fault tolerantly, and decoding a
memory are the same task.

For selected coherent channels, the correction calculation maps to free
Majorana fermions and admits efficient simulation [`bravyi2018coherent`].
`iverson2020coherence` gives a conditional logical-channel result and states
the fixed-noise-strength limitation. The mapping is therefore curated with
the `majorana-pairs` dialect and routed to `wanted:fermionic-compiler`; the
Atlas has no general executable converter for this view.

## Relation boundary

Sharing a representation or bulk phase is weaker than code identity. The open
Surface entry shares star/plaquette bulk but changes boundary homology. The
Honeycomb protocol has Toric-equivalent instantaneous frames but remains a
periodic measurement process with an anyon automorphism. A broad `Z2`
topological phase can share anyon data while using a different microscopic
Hamiltonian or qubit layout. The Toric card keeps these as typed relations and
never expands its identity to absorb them.

Primary sources: `kitaev2003fault`, `dennis2002topological`,
`tillich2009quantum`, `schuch2010peps`, `bravyi2018coherent`,
`iverson2020coherence`, `hastings2021dynamically`, and
`aasen2022automorphism`.
