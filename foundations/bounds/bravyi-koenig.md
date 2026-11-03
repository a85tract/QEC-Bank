# The Bravyi–König bound for topological Pauli stabilizer codes

> Level 2 derivation: why a geometrically local, bounded-spread logical
> unitary on a \(D\)-dimensional topological Pauli stabilizer code cannot rise
> above level \(D\) of the Clifford hierarchy.

The memorable slogan is:

> **A constant-depth local circuit gets one hierarchy level per spatial
> dimension.**

The proof is not a statement about the surface code's particular square
lattice. It uses four ingredients that survive every change of stabilizer
layout:

1. local circuits have bounded light cones;
2. logical Paulis can be cleaned out of correctable regions;
3. a \(D\)-dimensional lattice can be partitioned into \(D+1\) correctable
   regions;
4. each group commutator removes one region from the possible support.

After \(D\) commutators, the remaining operator is trapped in the last
correctable region and therefore acts as a phase on the codespace. Reading
that statement backward is exactly the recursive definition of the Clifford
hierarchy.

## 1. Precise statement

Put physical qubits on a \(D\)-dimensional lattice. Let a **Pauli stabilizer
code** have

- stabilizer generators of geometric diameter at most \(\xi\);
- distance \(d\);
- a unitary \(U\), built from a depth-\(h\) circuit whose gates have geometric
  range at most \(r\);
- and the property that \(U\) preserves the codespace.

Write \(\overline U\) for the induced logical unitary. If \(D\geq 2\) and the
length scales obey

\[
        \xi,\;hr \ll d^{1/D},
\]

then

\[
        \overline U\in\mathcal C_D,
\]

where \(\mathcal C_D\) is level \(D\) of the Clifford hierarchy.

For a family with bounded \(\xi,h,r\) and growing distance, the scale
inequality holds for every sufficiently large member. “Constant depth” is
therefore the clean asymptotic formulation, but the actual resource in the
proof is the light-cone radius \(hr\).

The paper proves a stronger morphism version. The source and target may be two
different \(D\)-dimensional topological Pauli stabilizer codes on the same lattice,
with the same number of logical qubits. If \(U\) maps the first codespace
unitarily onto the second, use the smaller distance and the larger stabilizer
range in the scale inequality; the induced map is still in
\(\mathcal C_D\). The codespace-preserving theorem is the special case in
which the two codes coincide.

Immediate specializations:

- \(D=2\): \(\overline U\in\mathcal C_2\), the Clifford group. A logical
  \(T\) gate is excluded.
- \(D=3\): \(\overline U\in\mathcal C_3\). This level contains non-Clifford
  gates such as \(T\), so the theorem permits them but does not guarantee
  that a given code has one.

For the modern convention \(T=\operatorname{diag}(1,e^{i\pi/4})\),
\(TXT^\dagger=(X+Y)/\sqrt2\), which is a Clifford but not a Pauli, while
\(TZT^\dagger=Z\). Thus \(T\in\mathcal C_3\setminus\mathcal C_2\), making it
the simplest witness to the difference between the two- and
three-dimensional ceilings.

## 2. Dictionary

All Pauli phases are irrelevant below.

### 2.1 Stabilizers, logicals, and encoded action

Let \(\mathcal S\) be the stabilizer group and \(\Pi\) the codespace
projector. A physical Pauli \(P\) is a logical Pauli when it commutes with
every stabilizer. Two such Paulis have the same encoded action when they
differ by a stabilizer.

Choose an encoding isometry

\[
        J:(\mathbb C^2)^{\otimes k}\longrightarrow
        (\mathbb C^2)^{\otimes n},
        \qquad JJ^\dagger=\Pi .
\]

For a physical operator \(O\) preserving the codespace, its encoded action is

\[
        \overline O=J^\dagger OJ .
\]

The distance \(d\) is the minimum weight of a logical Pauli whose encoded
action is not a scalar.

The map from commuting physical Paulis to encoded Paulis has kernel exactly
\(\mathcal S\), up to phase. Suppose a Pauli \(P\) commutes with
\(\mathcal S\), fixes every code state, and is independent of
\(\mathcal S\). Adding \(P\) as a new independent stabilizer would halve the
joint \(+1\) eigenspace, yet by assumption it would leave that eigenspace
unchanged. The contradiction shows that \(P\) was already a stabilizer.

### 2.2 Correctable regions

A set of qubits \(M\) is **correctable** when every logical Pauli supported
entirely in \(M\) acts as a scalar on the codespace. Any set with fewer than
\(d\) qubits is correctable by the definition of distance.

Correctability is stronger than the Pauli-only wording suggests. If \(O\) is
any operator supported in \(M\), expand it in the Pauli basis:

\[
        O=\sum_\alpha c_\alpha P_\alpha .
\]

For each \(P_\alpha\):

- if it anticommutes with a stabilizer \(S\), then
  \(\Pi P_\alpha\Pi=\Pi SP_\alpha\Pi
  =-\Pi P_\alpha S\Pi=-\Pi P_\alpha\Pi=0\);
- if it commutes with every stabilizer, it is a logical Pauli in \(M\), so
  correctability gives
  \(\Pi P_\alpha\Pi=x_\alpha\Pi\).

Therefore

\[
        \Pi O\Pi=c(O)\Pi                                      \tag{2.1}
\]

for every operator supported in a correctable region. In particular, a
logical unitary supported there is logically only a phase.

### 2.3 Neighborhoods and circuit range

For a region \(M\), let \(B_\rho(M)\) contain all lattice sites within
distance \(\rho\) of \(M\). A depth-\(h\), range-\(r\) circuit expands support
by at most \(hr\):

\[
 \operatorname{supp}(UOU^\dagger)
 \subseteq B_{hr}(\operatorname{supp}O).                     \tag{2.2}
\]

This follows one layer at a time. In one layer, only gates meeting the current
support can matter, and each such gate reaches at most distance \(r\).

### 2.4 Clifford hierarchy

Let \(\mathcal C_1\) be the logical Pauli group. Recursively,

\[
 \mathcal C_j=
 \{V:VPV^\dagger\in\mathcal C_{j-1}
       \text{ for every logical Pauli }P\}.
                                                                  \tag{2.3}
\]

Thus \(\mathcal C_2\) is the Clifford group. The hierarchy is nested, but
\(\mathcal C_j\) is generally not a group for \(j\geq3\). Multiplying an
element of \(\mathcal C_j\) on either side by a Pauli leaves it in
\(\mathcal C_j\); this follows directly from (2.3), inducting on \(j\).

For unitaries \(A,B\), write their group commutator as

\[
        [A,B]=ABA^\dagger B^\dagger .
\]

The proof repeatedly asks what happens to the hierarchy level when such a
commutator becomes simpler.

## 3. Four lemmas

### 3.1 Cleaning Lemma

**Lemma.** If \(M\) is correctable, every logical Pauli \(P\) has an equivalent
representative with no support in \(M\).

**Proof.** Represent phase-free \(n\)-qubit Paulis by vectors in
\(\mathbb F_2^{2n}\), with the symplectic product recording commutation. Let
\(\mathsf S\) be the vector space spanned by the stabilizers, let
\(\mathsf S^\perp\) be its symplectic orthogonal, and let
\(\pi_M\) restrict a Pauli vector to \(M\).

A logical Pauli is a vector \(p\in\mathsf S^\perp\). We need to find
\(s\in\mathsf S\) with

\[
        \pi_M(p+s)=0,
\]

or equivalently \(\pi_M(p)\in\pi_M(\mathsf S)\).

Assume instead that \(\pi_M(p)\notin\pi_M(\mathsf S)\). The symplectic form on
the Pauli space of \(M\) is nondegenerate, so there is a Pauli vector \(q\)
supported in \(M\) such that

\[
 \langle q,\pi_M(s)\rangle=0
 \quad\text{for every }s\in\mathsf S,
 \qquad
 \langle q,\pi_M(p)\rangle=1 .
\]

Extended by zero outside \(M\), \(q\) commutes with every stabilizer and is
therefore a logical Pauli supported in \(M\). Correctability says its encoded
action is scalar, so \(q\) is a stabilizer up to phase. But \(p\), being
logical, must commute with every stabilizer, contradicting
\(\langle q,p\rangle=1\). Hence the required \(s\) exists. Multiplying \(P\)
by its stabilizer representative removes its support from \(M\) without
changing its encoded action. \(\square\)

Cleaning does not erase a logical operator. It moves the same logical class
out of a region known to contain no logical information.

### 3.2 Union Lemma

**Lemma.** Let \(M\) and \(N\) be correctable regions separated by more than
the maximum stabilizer-generator diameter \(\xi\). Then \(M\cup N\) is
correctable.

**Proof.** Let a logical Pauli \(P\) be supported in \(M\cup N\), and factor it
as \(P=P_M P_N\). No stabilizer generator can meet both regions. For a
generator meeting only \(M\), commutation with \(P\) is exactly commutation
with \(P_M\); similarly for \(N\). Because \(P\) commutes with every
generator, both \(P_M\) and \(P_N\) commute with every generator separately.
They are logical Paulis supported in correctable regions, so both have scalar
encoded action. Their product does too. \(\square\)

Induction gives the version used below: a union of mutually well-separated
correctable chunks is correctable. This is the first indispensable use of
stabilizer locality. Without local generators, one generator could touch two
distant chunks and the factorization argument would fail.

### 3.3 Causal-intersection Lemma

**Lemma.** Let \(P,Q\) be tensor-product Paulis and let \(U\) be a
depth-\(h\), range-\(r\) circuit. Up to a constant factor in the radius, the
commutator

\[
        K=[P,UQU^\dagger]
\]

can have support only where the causal neighborhoods of
\(\operatorname{supp}P\) and \(\operatorname{supp}Q\) meet.

**Proof.** Draw the circuit for \(UQU^\dagger\). Delete every gate of \(U\)
and \(U^\dagger\) outside the forward and backward light cones of
\(\operatorname{supp}Q\). Those gates occur in mutually inverse pairs and
cancel, so this deletion does not change \(UQU^\dagger\).

Now place this pruned circuit next to its inverse in
\(P(UQU^\dagger)P^\dagger(UQ^\dagger U^\dagger)\). Delete every remaining
gate whose causal cone misses \(\operatorname{supp}P\). It also meets its
inverse without encountering \(P\), so it cancels. What survives must lie
both near \(\operatorname{supp}Q\) and near
\(\operatorname{supp}P\). The composite circuit has depth \(O(h)\), so the
thickening radius is \(O(hr)\). \(\square\)

This is the second indispensable use of locality. A long-range gate can join
the two supports without passing through their geometric intersection.

### 3.4 Pauli-character Lemma

**Lemma.** Let \(V\) be a logical unitary. If

\[
        [P,V]\propto I
\]

for every logical Pauli \(P\), then \(V\) is a logical Pauli up to phase.

**Proof.** The assumption is equivalent to

\[
        PVP^\dagger=\chi(P)V .
\]

Conjugating twice by the same Pauli gives \(\chi(P)^2=1\), so every
\(\chi(P)\) is a commutation sign. Expand \(V\) in the logical Pauli basis.
Every nonzero Pauli component must have the same commutation sign
\(\chi(P)\) against every \(P\). Two distinct Paulis cannot have identical
commutation signs against the entire Pauli group: their product would be a
nonidentity Pauli commuting with every Pauli, contradicting nondegeneracy of
the symplectic form. Only one Pauli coefficient can therefore be nonzero.
\(\square\)

## 4. The geometric partition

Choose a mesoscopic length \(R\) satisfying

\[
        \max(\xi,c_Dhr)\ll R\ll d_*^{1/D},                    \tag{4.1}
\]

where \(d_*\) is the smaller source/target distance and \(c_D\) is a constant
large enough to contain every light cone created by the \(D\) nested
commutators below.

Triangulate the physical lattice at scale \(R\). Thicken the simplices in
order of dimension:

- \(\Lambda_1\) is a union of separated neighborhoods of vertices;
- \(\Lambda_2\) is a union of separated interiors of edges after the vertex
  neighborhoods are removed;
- continue through faces and higher-dimensional simplices;
- \(\Lambda_{D+1}\) is the union of the remaining interiors of the
  \(D\)-simplices.

These \(D+1\) regions partition the lattice. Each \(\Lambda_j\) is a union of
chunks with diameter \(O(R)\), while distinct chunks in the same region are
separated by \(\Omega(R)\).

A fixed-radius neighborhood of one chunk contains \(O(R^D)\) qubits. The
right inequality in (4.1) makes this number smaller than \(d_*\), so the
chunk and every light-cone neighborhood needed below are correctable for
both codes. The left inequality keeps distinct thickened chunks farther apart
than the stabilizer range. The Union Lemma then makes each complete
\(\Lambda_j\), with the required collars, correctable.

### The two-dimensional picture

For \(D=2\), triangulate the surface into triangles of side \(R\):

- \(C\): disks around the vertices;
- \(B\): thickened edge segments after removing those disks;
- \(A\): the capped triangle interiors left over.

Each letter denotes many disconnected pieces, but pieces bearing the same
letter are far apart. Each letter is therefore one correctable region by the
Union Lemma.

On the toric or surface code, one can instead picture a horizontal logical
string and a displaced vertical logical string. After conjugation by a local
circuit, a string becomes a fat string; its commutator with the transverse
string lives near their small intersection. This is the right intuition.
It is not the general proof: an arbitrary two-dimensional stabilizer code
need not present every logical as a simple string. The \(A,B,C\) partition
plus cleaning supplies the same “small intersection” conclusion without
assuming string-shaped logicals.

## 5. Complete proof in two dimensions

Use the stronger two-code formulation. Let \(\Pi_1,\Pi_2\) project onto the
source and target codespaces, and suppose

\[
        U\Pi_1U^\dagger=\Pi_2 .
\]

Choose the partition \(\Lambda=A\cup B\cup C\) above, with collars wide enough
for all circuit light cones.

Let \(Q\) be an arbitrary logical Pauli of the source code and \(P\) an
arbitrary logical Pauli of the target code.

1. Since \(B_\rho(A)\) is correctable for the source code, clean \(Q\) out of
   \(B_\rho(A)\).
2. Since \(B_\rho(B)\) is correctable for the target code, clean \(P\) out of
   \(B_\rho(B)\).
3. Form the target-code logical operator

   \[
        K=P(UQU^\dagger)P^\dagger(UQ^\dagger U^\dagger).
                                                                  \tag{5.1}
   \]

The cleaned \(Q\) has no support near \(A\), so the bounded light cone of
\(UQU^\dagger\) avoids \(A\). The cleaned \(P\) has no support near \(B\).
By the Causal-intersection Lemma, all parts of (5.1) away from the common
causal intersection cancel. Thus \(K\) is supported in \(C\).

Every factor in (5.1) preserves the target codespace: \(P\) is a target
logical, while \(UQU^\dagger\) is the image of a source logical under the
codespace morphism. Hence \(K\) is a logical unitary supported in the
correctable region \(C\). Equation (2.1) gives

\[
        K\Pi_2=c\Pi_2,\qquad |c|=1.                              \tag{5.2}
\]

In fact \(c=\pm1\). On the codespace let
\(R=\overline U\,\overline Q\,\overline U^\dagger\). Equation (5.2) says

\[
        \overline P R\overline P^\dagger R^\dagger=cI,
        \quad\text{or}\quad
        \overline P R\overline P^\dagger=cR .
\]

Conjugating a second time by the Pauli \(\overline P\) yields
\(R=c^2R\), so \(c^2=1\).

We have proved

\[
        [\overline P,
          \overline U\,\overline Q\,\overline U^\dagger]
        =\pm I                                                    \tag{5.3}
\]

for every target Pauli \(\overline P\) and every source Pauli
\(\overline Q\). Fixing \(Q\), the Pauli-character Lemma turns (5.3) into

\[
        \overline U\,\overline Q\,\overline U^\dagger
        \in\mathcal C_1 .
\]

This is true for every \(\overline Q\), which is precisely the definition

\[
        \overline U\in\mathcal C_2 .
\]

So every such two-dimensional logical unitary is Clifford. No translation
symmetry, square lattice, homological presentation, or string form for the
logical operators entered the proof.

## 6. The \(D\)-dimensional induction

Partition the lattice into the \(D+1\) correctable regions

\[
        \Lambda=\Lambda_1\cup\cdots\cup\Lambda_{D+1}.
\]

Choose an arbitrary source logical Pauli \(P_1\), and arbitrary target
logical Paulis \(P_2,\ldots,P_D\). Use the Cleaning Lemma to choose
representatives satisfying

\[
 \operatorname{supp}(P_j)\cap B_\rho(\Lambda_j)=\varnothing,
 \qquad j=1,\ldots,D.                                           \tag{6.1}
\]

Define

\[
 \begin{aligned}
 K_1 &= UP_1U^\dagger,\\
 K_j &=P_j^\dagger K_{j-1}P_jK_{j-1}^\dagger,
        \qquad j=2,\ldots,D .                                   \tag{6.2}
 \end{aligned}
\]

Every \(K_j\) preserves the target codespace. We now track support.

- Because \(P_1\) was cleaned out of a collar of \(\Lambda_1\), causal
  pruning of the circuit \(UP_1U^\dagger\) gives a representation of \(K_1\)
  acting trivially on \(\Lambda_1\).
- Suppose \(K_{j-1}\) acts trivially on
  \(\Lambda_1\cup\cdots\cup\Lambda_{j-1}\). The next line of (6.2) is its
  commutator with \(P_j\). Since \(P_j\) was cleaned out of a collar of
  \(\Lambda_j\), the Causal-intersection Lemma removes \(\Lambda_j\) from the
  support as well. The already removed regions stay removed because their
  collars were chosen wider than the new constant-depth light cone.

The depth of these nested commutator circuits grows by only a
\(D\)-dependent constant factor. That is why one common radius
\(\rho=c_Dhr\) suffices in (4.1). Induction gives

\[
 \operatorname{supp}(K_j)
 \subseteq
 \Lambda_{j+1}\cup\cdots\cup\Lambda_{D+1}.                       \tag{6.3}
\]

At \(j=D\), \(K_D\) is a logical unitary supported in the correctable region
\(\Lambda_{D+1}\). Therefore

\[
        \overline K_D\propto I                                   \tag{6.4}
\]

for every choice of \(P_1,\ldots,P_D\).

Now read the nested commutators backward.

First, (6.2) and (6.4) say that

\[
        [\overline P_D,\overline K_{D-1}]\propto I
\]

for every Pauli \(\overline P_D\). The Pauli-character Lemma gives

\[
        \overline K_{D-1}\in\mathcal C_1 .
\]

For the induction step, suppose
\(\overline K_j\in\mathcal C_m\) for every choice of
\(\overline P_j\). Rearranging (6.2) gives

\[
 \overline K_{j-1}\overline P_j\overline K_{j-1}^\dagger
     =\overline P_j\,\overline K_j .                             \tag{6.5}
\]

The right-hand side belongs to \(\mathcal C_m\), because multiplying by a
Pauli preserves a hierarchy level. Since (6.5) holds for every Pauli
\(\overline P_j\), definition (2.3) gives

\[
        \overline K_{j-1}\in\mathcal C_{m+1}.
\]

Repeating this backward yields

\[
        \overline K_1\in\mathcal C_{D-1}.
\]

Finally \(K_1=UP_1U^\dagger\), and \(P_1\) was an arbitrary source logical
Pauli. Hence

\[
        \boxed{\overline U\in\mathcal C_D}.
\]

The dimension enters only through the number of correctable regions. Each
commutator consumes one region, so \(D\) spatial dimensions leave exactly
\(D\) hierarchy levels.

## 7. Why the result also forbids a protected universal gate set

For a fixed number \(k\) of logical qubits, every finite level
\(\mathcal C_j\) contains only finitely many elements up to global phase.
This can be proved recursively. The Pauli group is finite up to phase. An
element of \(\mathcal C_j\) is specified, up to phase, by its conjugation
action on a finite generating set of Paulis, and every image lies in the
finite set \(\mathcal C_{j-1}\). If two unitaries have the same conjugation
action on every Pauli, their ratio commutes with the full matrix algebra and
is a scalar.

There is one subtlety: \(\mathcal C_D\) is not generally a group when
\(D\geq3\), so “every generator lies in \(\mathcal C_D\)” does not alone show
that all generated products remain there.

The depth assumption closes this loophole. If a product of protected
depth-\(h\) gates first left \(\mathcal C_D\) after a bounded number \(s\) of
factors, that product would itself have depth \(sh=O(1)\). The theorem would
put it back in \(\mathcal C_D\), a contradiction. Because
\(\mathcal C_D\) is finite for fixed \(k\), the maximum possible shortest
escape length over its subsets is finite. Thus, for all sufficiently large
codes, the group generated by bounded-depth protected gates remains inside a
finite set and cannot be computationally universal.

The fixed-\(k\) qualification belongs to this universality corollary. The
main hierarchy bound itself is the local statement proved in Sections 4–6.

## 8. What is and is not an escape

| Proposed maneuver | Does the theorem apply? | Reason |
|---|---|---|
| Change the shape or tiling of a 2D stabilizer code | Yes, if locality and macroscopic distance remain | The proof never uses a square lattice or translation symmetry |
| Use a geometrically local transversal physical gate | Yes | It is a particularly shallow local circuit; transversality alone does not make distant pairings geometrically local |
| Use a bounded-depth local unitary deformation between two codes | Yes | The morphism version allows distinct source and target codes |
| Braid defects through a chain of uniformly local 2D deformations | Still Clifford | Each protected local step is Clifford, and the Clifford group is closed |
| Use lattice surgery with depth growing with code distance | Not as one constant-depth unitary | Its growing time depth lies outside the theorem's circuit assumption; its standard logical operations are nevertheless Clifford |
| Inject and distill magic states | Injection is outside the protected hypothesis | At injection, the new logical state does not yet have macroscopic topological protection |
| Use measurements and adaptive classical feedback | Not covered by the literal unitary-circuit statement | A separate analysis is needed for nonunitary protocols |
| Couple distant planar qubits directly | No | The gate range is no longer geometrically bounded in the planar metric |
| Let circuit depth grow until \(hr\) is comparable to \(d^{1/D}\) | No | The mesoscopic scale \(R\) in (4.1) no longer exists |
| Replace commuting Pauli checks by generalized non-Pauli stabilizers | No | The Pauli symplectic Cleaning and Union Lemmas used here no longer apply |
| Move from 2D to 3D | Yes, with a weaker ceiling | The allowed level rises from \(\mathcal C_2\) to \(\mathcal C_3\) |

The theorem is a ceiling, not a construction. It says which hierarchy levels
are impossible under its assumptions; it does not say that every gate below
the ceiling is available for every code.

### A current boundary case: “Clifford stabilizer codes”

Kobayashi, Zhu, and Hsin constructed a two-dimensional code with a
transversal logical \(T\) gate in 2026 and explicitly described it as
surpassing the Bravyi–König bound for **Pauli** codes. There is no
contradiction. Their local “stabilizers” are Clifford unitaries rather than
Pauli operators and need not commute. The object is therefore outside the
abelian Pauli stabilizer formalism assumed in Sections 1–6.

This distinction is load-bearing, not terminological. The proof of the
Cleaning Lemma used the symplectic vector space of Pauli operators; the Union
Lemma factorized commutation with bounded-diameter Pauli generators; and
equation (2.1) expanded errors in the Pauli basis relative to an abelian
Pauli stabilizer codespace. Those steps cannot simply be reused for
noncommuting Clifford generators. The 2026 construction changes the
algebraic hypothesis that makes the Bravyi–König ceiling possible.

## 9. Audit questions

**Q1. Why is the scale \(d^{1/D}\), rather than \(d\)?**

**A.** A chunk of linear size \(R\) in \(D\) dimensions contains
\(O(R^D)\) qubits. Distance guarantees correctability when that volume is
smaller than \(d\), hence \(R\ll d^{1/D}\).

**Q2. Where exactly is stabilizer locality used?**

**A.** In the Union Lemma. Widely separated correctable chunks remain
correctable because no bounded-diameter stabilizer generator can couple two
chunks. Circuit locality is a separate use of geometry: it bounds light
cones in the Causal-intersection Lemma.

**Q3. Why may a non-Pauli commutator \(K_D\) be declared trivial in a
correctable region?**

**A.** Correctability plus Pauli expansion gives
\(\Pi O\Pi=c(O)\Pi\) for every operator \(O\) in the region, not only for
Paulis. Since \(K_D\) also preserves the codespace, its logical action is
that scalar.

**Q4. Why is the crossing-string argument insufficient as the general
proof?**

**A.** It presumes convenient string representatives. The theorem covers
arbitrary local stabilizer codes. The simplicial partition and Cleaning
Lemma manufacture the needed separated supports without assuming any
particular shape for a logical operator.

**Q5. Does the 3D conclusion provide a universal protected gate set?**

**A.** No. It permits level-3 gates such as \(T\), but for fixed \(k\) the
bounded-depth protected gates still generate only a finite subgroup inside
the hierarchy ceiling. Additional unprotected or nonunitary resources remain
necessary for universality.

## 10. Source and citation audit

Primary source, fetch-verified on 2026-07-26:

- Sergey Bravyi and Robert König, “Classification of topologically protected
  gates for local stabilizer codes,”
  [arXiv:1206.1609](https://arxiv.org/abs/1206.1609), submitted 7 June 2012;
  [Physical Review Letters 110, 170503
  (2013)](https://doi.org/10.1103/PhysRevLett.110.170503).

Scope-boundary source, also fetch-verified on 2026-07-26:

- Ryohei Kobayashi, Guanyu Zhu, and Po-Shen Hsin, “Clifford Hierarchy
  Stabilizer Codes: Transversal Non-Clifford Gates and Magic,”
  [arXiv:2511.02900](https://arxiv.org/abs/2511.02900);
  journal version, “Clifford Hierarchy Stabilizer Codes: Transversal
  Non-Clifford Gates and Magic States,”
  [Physical Review Letters 136, 250802
  (2026)](https://doi.org/10.1103/j2q4-bnc6).

The theorem statement, the scale condition, the two-code morphism
generalization, the Cleaning and Union Lemmas, the simplicial partition, the
nested-commutator proof, and the fixed-\(k\) universality corollary all trace
to this source. The intermediate symplectic proof of cleaning, the
Pauli-basis proof of (2.1), and the expanded hierarchy induction are supplied
here so that the paper is provenance rather than a missing proof step.

Atlas citation note: `atlas/surface/card.yaml` currently uses the bibkey
`bravyi2013classification`, while
`docs/lit/surface/surface-foundations.md` uses
`bravyikonig2013classification` for the same fetch-verified paper. T4 permits
new files only, so this page records the mismatch instead of changing either
out-of-scope file. The planned reference-registry task should choose one key
and enforce it repository-wide.
