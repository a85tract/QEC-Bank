# Surface code — Level-2 map

This is the index to the worked derivations, not a second intuition essay.
Each linked page answers one question completely and states which facts are
algebraic, recomputed, bounded, or literature-derived.

1. [Why HGP(rep_L, rep_L) is the unrotated planar patch](hgp-construction.md):
   the two qubit blocks, check matrices, CSS cancellation, geometry, locality,
   and `k=1`.
2. [Why the distance is exactly L](distance-proof.md): an upper-bound string,
   a disjoint-representative lower bound, exact enumeration at `L=3,4`, and the
   bounded `L=5` claim.
3. [Why syndrome is the boundary of an error chain](syndrome-decoding.md):
   bulk pairs, boundary condensation, the invisible completed string, detector
   histories, and what a decoder is deciding.
4. [Why a lattice-surgery seam measures logical parity](lattice-surgery.md):
   the telescoping seam product, merge dimension and distance, and why full
   fault tolerance uses spacetime decoding rather than bare majority vote.
5. [Which surface-code threshold a number refers to](threshold-ledger.md):
   a model-by-model provenance ledger that keeps code-capacity,
   phenomenological, circuit-level, and hardware numbers separate.

## Reproduction contract

Run from the repository root:

```bash
source .venv/bin/activate
python atlas/surface/pedagogy/reproduce.py
make verify-entry E=atlas/surface
```

The same computation can be launched from a Python session:

```python
from runpy import run_path

run_path("atlas/surface/pedagogy/reproduce.py", run_name="__main__")
```

`reproduce.py` imports the shipped constructor and asserts every computed
statement used across these pages: check matrices, locality, ranks, logical
representatives, syndrome walk, exact distances, the seeded `L=5` upper
bound, resource counts, and the `L=3` rectangular surgery merge. It exits
nonzero on the first disagreement. The verifier independently reruns the
claims in `instances.yaml`.

The provenance split is deliberate:

- `n`, `k`, CSS structure, and the two small exact distances are
  machine-verified.
- The `L=5` lower bound is theorem/literature-backed; its upper bound is a
  seeded machine-rerunnable witness, so the instance is marked `bounded`.
- Thresholds and hardware results are not properties of a bare check matrix.
  They remain literature claims with the complete noise model and decoder
  written beside each number.
