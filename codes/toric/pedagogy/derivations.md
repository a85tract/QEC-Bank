# Toric code — Level-2 map

This index separates proofs, decoder assumptions, operation protocols, and
hardware evidence. Each page answers one question completely and states which
facts are algebraic, machine-recomputed, or literature-claimed.

1. [Why the square torus gives [[2L²,2,L]]](homology-and-distance.md): cell
   counts, CSS commutation, the two global check dependencies, homology, and
   matching upper and lower distance bounds.
2. [Why cyclic HGP is exactly the Toric matrix](cyclic-hgp.md): the square
   cyclic parity maps, HGP block order, two kernel sectors, exact constructor
   equality, and the contrast with open Surface factors.
3. [Why syndrome is only the boundary of an error chain](syndrome-decoding.md):
   endpoint cancellation, homology-class ambiguity, perfect and noisy records,
   loss and coherent-noise boundaries, and decoder objectives.
4. [Which threshold a Toric number refers to](threshold-ledger.md): selected
   primary-source tuples and the reason no scalar belongs to the bare code.
5. [Which operations are verified and what hardware demonstrated](operations-and-realizations.md):
   logical loops, stacked-block CNOT, proposed Clifford protocols,
   non-Clifford boundaries, state preparation, and repeated correction.
6. [What each representation preserves](representations.md): chain, symplectic,
   anyon, HGP, statistical, PEPS, and Majorana dictionaries.

## Reproduction contract

Run from the repository root:

```bash
source .venv/bin/activate
python atlas/toric/pedagogy/reproduce.py
make verify-entry E=atlas/toric
```

The same computation can be launched from a Python session:

```python
from runpy import run_path

run_path("atlas/toric/pedagogy/reproduce.py", run_name="__main__")
```

`reproduce.py` imports the shipped constructor and asserts the parameter
refusal boundary, cell counts, check ranks, row weights, CSS commutation,
global dependencies, exact small distances, four logical supports, periodic
scene contract, endpoint-syndrome walk, exact cyclic-HGP matrix equality, and
the two-block transversal-CNOT symplectic action. It exits nonzero on the first
disagreement. The entry verifier independently recomputes every claim in
`instances.yaml`.

The provenance split is deliberate:

- `n`, `k`, CSS structure, the committed small distances, logical supports,
  cyclic-HGP equality, and stacked-block CNOT are machine-verified.
- The all-`L` distance lower bound is a worked homological proof backed by the
  primary Toric literature.
- Decoder thresholds, proposed Clifford gadgets, and hardware results do not
  follow from a check matrix. They remain literature claims with their full
  model or protocol identity written beside them.
