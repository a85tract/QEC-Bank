# Which threshold does a Toric number refer to?

## Rule

A threshold is a transition of a family of experiments, not an invariant of a
finite check matrix. Its identity tuple is

```text
(family and boundary, physical channel, syndrome/circuit model,
 decoder and objective, rate normalization, asymptotic observable).
```

Changing any coordinate can change the value. The Toric card therefore names
decoder regimes without putting one number in the entry summary.

## Selected primary-source tuples

Every value below has origin `{kind: claimed, ref: BIBKEY}`. None is recomputed
by the Atlas constructor.

| Source-reported value | Identity tuple | What may be concluded |
|---|---|---|
| `15.5%` | Periodic Toric family; ideal syndrome extraction; each data qubit receives `X`, `Y`, or `Z` with probability `p0/3`; graph matching; the paper converts the `X`-component rate to `p=(2/3)p0`; asymptotic logical transition | A benchmark in the paper's total single-qubit depolarizing-rate convention, not the independent-`X/Z` maximum-likelihood value from another convention. Origin: `wang2010thresholds`. |
| `7.8 × 10^-3` | Periodic Toric family; the named four-interaction-order extraction circuit; preparation, readout, memory, and two-qubit processes each assigned rate `p`, with the fifteen nonidentity two-qubit Paulis equiprobable after an ideal CNOT; repeated graph matching; asymptotic memory transition | A circuit-level result in that paper's equal-process-rate units, not a code-capacity or generic modern circuit threshold. Origin: `wang2010thresholds`. |
| `18.9(3)%` | Toric code; iid single-qubit depolarizing channel; correlations between `X`, `Y`, and `Z` components retained through an eight-vertex-model mapping; optimal-class transition | A depolarizing-channel threshold under the paper's correlated Pauli convention, not three independent binary matching problems. Origin: `bombin2012strong`. |
| `50%` detectable loss | Square-lattice topological code; erasure locations known; loss geometry controlled by bond percolation, with computational-error tradeoff treated separately | The maximum tolerable heralded-loss boundary of that model, not an unheralded leakage rate. Origin: `stace2009loss`. |
| `0.133%` | Two-dimensional Toric code; equal independent data and syndrome error probabilities; Harrington cellular automaton with finite communication speed | A local-decoder benchmark under a restrictive symmetric phenomenological model, not the capability of global matching. Origin: `breuckmann2017local`. |

These rows are deliberately heterogeneous. Their purpose is to prevent a
reader from ranking decoders or hardware using incomparable scalars.

## Other transitions that are not decoder thresholds

Coherent information can exhibit an information-theoretic transition without
choosing a decoder. `lee2025coherent` derives an exact Toric coherent-information
expression and links it to random-bond Ising criticality. That result addresses
recoverable information, not the runtime or decision rule of MWPM, tensor
contraction, or BP-OSD.

Coherent rotations also carry phase information absent from a stochastic
Pauli channel. `bravyi2018coherent` gives an efficient Majorana simulation for
declared coherent-error models; `iverson2020coherence` proves a conditional
logical-incoherence trend and explicitly does not extend it to fixed physical
noise strength as `L` grows. Neither result licenses replacing coherent noise
by a universal Pauli rate.

## Hardware is another ledger

A finite logical error per round, a two-distance comparison, a prepared-code
state fidelity, and an asymptotic decoder threshold answer different
questions. The 2026 neutral-atom Toric experiment reports repeated extraction
and a finite comparison; the Atlas records it under realizations and does not
insert it into the table above. See
[operations and realizations](operations-and-realizations.md).

## Citation corrections

- DOI `10.1103/Physics.5.50` resolves to an APS Physics Viewpoint. It is
  secondary commentary and not the primary origin of a numerical row.
- DOI `10.1103/PhysRev.88.1332` and DOI `10.1143/JPSJ.55.3305` are classical
  Ising-model sources. They are precursors to the statistical machinery, not
  direct Toric-code threshold reports.
- arXiv `1810.09621` concerns measurement-based fault tolerance beyond
  foliation; its placement near a threshold feature does not make it a Toric
  code-capacity benchmark.

Primary sources: `wang2010thresholds`, `bombin2012strong`, `stace2009loss`,
`breuckmann2017local`, `lee2025coherent`, `bravyi2018coherent`, and
`iverson2020coherence`.
