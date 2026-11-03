# Why syndrome is only the boundary of an error chain

## Algebraic syndrome

Write a Pauli error as binary vectors `(eX,eZ)` on the edge qubits. For the CSS
checks,

```text
star syndrome       sX = HX eZ,
plaquette syndrome  sZ = HZ eX,
```

with arithmetic modulo two. A single `Z` edge has the two endpoint vertices
in `sX`. Along a longer connected path, every internal vertex touches two
error edges and cancels; only the two endpoints remain. The dual statement
holds for an `X` path and plaquette defects.

## What the syndrome forgets

Suppose an error chain `e` and a candidate correction `c` have the same
boundary. Their sum `e+c` is closed. Three cases matter:

1. `e+c` bounds a collection of faces. It is a stabilizer, so the correction
   succeeds.
2. `e+c` has horizontal or vertical winding. It is a logical operator, so the
   correction returns to the code space but changes encoded information.
3. In a noisy measurement record, `e+c` is not a purely spatial chain at all;
   its endpoints and time boundary must be evaluated in the spacetime detector
   complex.

Thus decoding is a choice of logical class consistent with the data, not an
instruction to find any path between visible endpoints.

## Decoder objectives

Minimum-weight perfect matching assigns additive costs to graph edges, pairs
defects, and chooses one minimum-cost representative. It is efficient and
geometry-aware, but it does not sum all degenerate representatives in a class.
Maximum-likelihood decoding compares the total probability of logical classes;
in the statistical picture this is a free-energy rather than ground-energy
decision.

Renormalization-group decoders approximate class probabilities while merging
scales. Tensor-network methods contract a class partition function exactly for
restricted channels or approximately at controlled bond dimension. BP-OSD
uses generic sparse-matrix soft information and post-processing; it does not
automatically exploit periodic homology. A cellular automaton restricts
communication to a finite light cone and therefore solves an additional
locality problem.

## Regime map

| Regime | Decoder receives | Added ambiguity | Claim boundary |
|---|---|---|---|
| Code capacity | one perfect spatial syndrome and a Pauli prior | which spatial homology class | No measurement or circuit faults |
| Phenomenological | syndrome changes over repeated rounds | paths may run in time | Round count, time boundary, and data/check normalization matter |
| Circuit level | detector events from a named extraction circuit | correlated hooks, leakage, and schedule faults | A threshold belongs to that circuit and decoder |
| Detectable loss | syndrome plus known missing-edge locations | supercheck geometry and percolation | Known erasure is not unheralded leakage |
| Correlated Pauli | syndrome plus a joint prior | paths no longer have independent edge weights | Matching needs reweighting or a richer objective |
| Coherent rotation | amplitudes or a channel model, not only Pauli probabilities | interference between fault histories | Pauli twirling can change the logical channel |

## A reproducible endpoint walk

`reproduce.py` applies consecutive `Z` errors along one horizontal row. Every
proper open segment has exactly two star defects. Extending the segment by one
edge moves one endpoint. Completing all `L` edges closes a noncontractible
loop: the syndrome vanishes, yet the vector is outside the stabilizer row
space and equals a constructor-provided logical support.

This small experiment is the whole failure mechanism in miniature. The
decoder sees the same zero syndrome for identity, any stabilizer, and any
closed logical loop. Only the prior and error history distinguish them.

## Threshold discipline

The [threshold ledger](threshold-ledger.md) records source-reported values only
with channel, syndrome quality, decoder, and observable. It does not transfer
an open-Surface circuit number to the torus or compare a detectable-loss
percolation point with an unheralded Pauli rate.

Primary sources: `dennis2002topological`, `wang2003confinement`,
`wang2010thresholds`, `stace2009loss`, `duclos2010fast`,
`bravyi2014efficient`, `breuckmann2017local`, `chubb2021statistical`, and
`roffe2020decoding`.
