# The Bravyi–Poulin–Terhal tradeoff in two dimensions

> Level 2 derivation: why bounded-range commuting constraints in an ordinary
> two-dimensional geometry force \(k d^2=O(n)\).

The memorable slogan is:

> **In two Euclidean dimensions, one distance-\(d\) logical qubit consumes
> area of order \(d^2\).**

This is not proved by drawing a logical string and counting its length. A
general commuting-projector code need not be a stabilizer code and need not
have string-shaped logical operators. The proof instead turns local
correctability into an entropy statement:

1. a correctable square can be enlarged whenever its boundary is also
   correctable;
2. therefore every square whose side is a sufficiently small constant
   multiple of \(d\) is correctable;
3. the lattice can be divided into two correctable checkerboards \(A,B\)
   plus small corner patches \(C\);
4. correctability of \(A\) and \(B\) forces all \(k\) logical qubits through
   \(C\);
5. the area of \(C\) is \(O(n/d^2)\).

The third step is where two-dimensional geometry enters. The fourth is
where quantum information differs from classical information: a region
whose erasure is correctable has *negative* conditional entropy.

## 1. Precise statement

Put \(n\) particles on a regular square lattice with open or periodic
boundary conditions. Assume:

- every site has Hilbert-space dimension at most a fixed \(q\);
- the codespace \(\mathcal C\) is the common \(+1\) eigenspace of pairwise
  commuting projectors \(\Pi_a\);
- the support of every \(\Pi_a\) fits inside a \(w\times w\) square;
- \(\dim\mathcal C=2^k\);
- every erasure on fewer than \(d\) sites is correctable.

Here \(w\) and \(q\) are independent of the lattice size. Then there is a
constant \(c(w,q)\), independent of \(n,k,d\), such that

\[
             \boxed{k\,d^2\leq c(w,q)\,n.}                     \tag{1.1}
\]

The theorem is often called a stabilizer-code bound because stabilizer
codes are its most common application. The original result is stronger:
commuting local projectors need not be Pauli projectors.

Three qualifications are load-bearing.

1. **Local means Euclidean bounded range.** A weight-six check may still be
   nonlocal if its six qubits separate by a distance growing with the code.
2. **The constraints commute.** The boundary factorization below uses
   commutativity, not merely a gapped local Hamiltonian.
3. **The local dimension is bounded.** Otherwise one site can hide a growing
   number of qubits and the entropy count \(S(C)\leq |C|\log_2q\) has no
   size-independent coefficient.

If \(k=0\), (1.1) is immediate. The proof below therefore assumes \(k>0\).
Cases with \(d\) comparable to the fixed microscopic scale \(w^2\) are also
immediate from \(k\leq n\log_2q\); the geometric argument handles the
macroscopic-distance regime.

## 2. Dictionary: what “correctable” means

Let

\[
       \Pi=\prod_a\Pi_a
\]

be the codespace projector. For a set of sites \(M\), write
\(\overline M\) for its complement.

### 2.1 Erasure criterion

A region \(M\) is **correctable** when erasing all sites in \(M\) can be
reversed on every encoded state. The Knill–Laflamme condition for this
known-location error is

\[
        \Pi O_M\Pi=c(O_M)\Pi
        \quad\text{for every operator }O_M
        \text{ supported in }M.                               \tag{2.1}
\]

Why does (2.1) characterize erasure? Choose an operator basis
\(\{E_\alpha\}\) on \(M\). Erasure has error products
\(E_\alpha^\dagger E_\beta\), and these span the full operator algebra on
\(M\). The ordinary Knill–Laflamme equations for all pairs
\(\alpha,\beta\) are therefore exactly (2.1).

Two consequences will be used repeatedly.

- Any subset of a correctable region is correctable.
- Every region with fewer than \(d\) sites is correctable, by the definition
  of distance used in the theorem.

For a Pauli stabilizer code, (2.1) says that a region contains no
nontrivial logical Pauli. Thus this erasure distance agrees with the usual
minimum weight of a nontrivial logical Pauli.

### 2.2 The entropy identity

Let \(\rho\) be any encoded state. Correctability of \(M\) implies

\[
          S(M\mid\overline M)=-S(M),                           \tag{2.2}
\]

where logarithms are base two.

Here is the information-theoretic content of the equation. Purify the
logical input with a reference \(R\), encode it into
\(M\overline M\), and apply (2.1). No observable on \(M\) depends on the
logical input, including its off-diagonal coherences, so

\[
          \rho_{RM}=\rho_R\otimes\rho_M .
\]

Equivalently \(I(R:M)=0\). The global state on
\(RM\overline M\) is pure, hence

\[
\begin{aligned}
0=I(R:M)
 &=S(R)+S(M)-S(RM)\\
 &=S(M\overline M)+S(M)-S(\overline M).
\end{aligned}
\]

Rearranging gives (2.2). The negative sign is not a formal curiosity:
\(\overline M\) can reconstruct the quantum information lost from \(M\),
so the two regions share the entanglement needed to undo that loss.

For the maximally mixed encoded state

\[
             \rho_*=\frac{\Pi}{2^k},
\]

the entropy of the full lattice is

\[
             S(\Lambda)=k.                                    \tag{2.3}
\]

Equations (2.2) and (2.3) will convert geometry into a bound on \(k\).

### 2.3 Internal and external boundaries

The external boundary \(\partial_+M\subseteq\overline M\) contains every
outside site belonging to a projector that also touches \(M\). The internal
boundary is

\[
             \partial_-M=\partial_+(\overline M),
\]

and \(\partial M=\partial_-M\cup\partial_+M\).

For an \(R\times R\) square on a square lattice,

\[
             |\partial M|\leq c_\square\,w(R+w),               \tag{2.4}
\]

where \(c_\square\) is a geometry-only constant. Equation (2.4) is simply a
perimeter count: only a collar of thickness \(O(w)\) can participate in a
constraint crossing the cut.

## 3. Why commuting projectors can be split at a boundary

The proof must do more than clean Pauli operators. It must disentangle an
arbitrary commuting-projector codespace at the boundary of a correctable
region.

### 3.1 Boundary-algebra decomposition

Suppose two commuting projectors act on \(AB\) and \(BC\):

\[
        P_{AB}Q_{BC}=Q_{BC}P_{AB}.
\]

There is a decomposition

\[
 \mathcal H_B=
 \bigoplus_x
 \mathcal H_{B_x^L}\otimes\mathcal H_{B_x^R}                  \tag{3.1}
\]

such that, in every sector \(x\), the \(AB\) projector acts only on
\(AB_x^L\) and the \(BC\) projector acts only on \(B_x^RC\).

To see the mechanism, take operator-Schmidt expansions

\[
 P_{AB}=\sum_i A_i\otimes L_i,\qquad
 Q_{BC}=\sum_j R_j\otimes C_j
\]

with linearly independent outer operators. Commutativity forces
\([L_i,R_j]=0\) for every \(i,j\). The finite-dimensional algebras
\(\mathcal L=\operatorname{alg}\{L_i\}\) and
\(\mathcal R=\operatorname{alg}\{R_j\}\) therefore commute.

Decompose the center of \(\mathcal L\) into minimal central projectors.
Inside one central block, a finite-dimensional factor is a full matrix
algebra on one tensor factor with an identity on its multiplicity factor:

\[
       \mathcal L_x\simeq
       \mathsf M(\mathcal H_{B_x^L})\otimes I_{B_x^R}.
\]

Every operator commuting with \(\mathcal L_x\) acts on the other factor, so

\[
       \mathcal R_x\subseteq
       I_{B_x^L}\otimes\mathsf M(\mathcal H_{B_x^R}).
\]

This proves (3.1). The label \(x\) is a classical boundary sector; the left
and right quantum degrees of freedom separate inside each sector.

For many commuting constraints, group the product of all constraints
meeting the left side into \(P_{AB}\) and the product of the rest into
\(Q_{BC}\). Their interaction algebras obey the same decomposition.

### 3.2 Boundary Disentangling Lemma

**Lemma.** Let \(M\) and its external boundary \(\partial_+M\) both be
correctable. Then a unitary supported on \(\partial M\) transforms the
codespace projector into

\[
 U_{\partial M}\Pi U_{\partial M}^\dagger
       =|\phi_M\rangle\langle\phi_M|\otimes\Pi_{\overline M}
                                                               \tag{3.2}
\]

for a fixed pure state \(|\phi_M\rangle\) independent of the encoded state.

**Proof.** Partition the lattice as

\[
\begin{aligned}
A&=M\setminus\partial_-M,& B&=\partial_-M,\\
C&=\partial_+M,& D&=\overline M\setminus\partial_+M.
\end{aligned}
\]

Thus \(M=AB\), \(\overline M=CD\), and all communication between the two
interiors passes through \(BC\).

First split \(C\). Group the commuting constraints into those supported on
\(ABC\) and those supported on \(CD\). Applying (3.1) to their interaction
algebras gives

\[
 \Pi=\bigoplus_x
       \Pi^{(x)}_{AB\,C_x^L}\otimes
       \Pi^{(x)}_{C_x^R D}.                                   \tag{3.3}
\]

If two nonzero sectors \(x\) occurred, measuring the sector label on \(C\)
would distinguish orthogonal code states. That contradicts correctability
of \(C\subseteq\partial_+M\). Hence only one sector occurs, and a unitary
\(U_C\) exposes a tensor split \(C=C^LC^R\).

Apply the same argument to the internal boundary \(B\), grouping constraints
on \(AB\) against those on \(BCD\). Because \(B\subseteq M\) is correctable,
only one boundary sector occurs. After a unitary \(U_B\), the projector has
the product form

\[
 \Pi'=
     \Pi_{AB^L}\otimes
     \Theta_{B^R C^L}\otimes
     \Pi_{C^R D}.                                              \tag{3.4}
\]

Correctability of \(M\) forces \(\Pi_{AB^L}\) to have rank one. Otherwise
two orthogonal states in that factor could be distinguished by an
observable supported in \(M\).

The middle projector \(\Theta_{B^RC^L}\) also has rank one. If it encoded a
nontrivial system, correctability of \(B^R\subseteq M\) would make that
system recoverable from \(C^L\), while correctability of
\(C^L\subseteq\partial_+M\) would make the same system recoverable from
\(B^R\). Two disjoint systems would then each contain the full unknown
quantum state, contradicting no-cloning.

A final unitary on \(B^RC^L\) maps its fixed pure state into the \(M\)
factor. Together with \(U_B\) and \(U_C\), it gives (3.2). \(\square\)

The unitary \(U_{\partial M}\) need not be a geometrically local circuit
inside the boundary. The theorem needs only its support, not a depth bound.

### 3.3 Growth Lemma: a correctable boundary lets a region expand

**Lemma.** Write the lattice as \(ABCD\), with \(M=AB\). Suppose:

- \(M\) is correctable;
- \(BC\) is correctable;
- every constraint crossing the boundary of \(M\) is supported in \(BC\).

Then \(ABC=M\cup C\) is correctable.

**Proof.** Since \(\partial_+M\subseteq C\subseteq BC\), both \(M\) and its
external boundary are correctable. Apply (3.2). After the boundary unitary,
every encoded state has the form

\[
       \eta_{AB}\otimes\eta_{CD},                              \tag{3.5}
\]

where \(\eta_{AB}\) is a known pure state independent of the logical input.

Consider the error that first applies the boundary unitary from (3.2) and
then erases \(BC\). Its support lies in the correctable region \(BC\), so it has a
recovery map. Its surviving state is

\[
       \eta_A\otimes\rho_D.                                    \tag{3.6}
\]

The factor \(\eta_A\) is fixed and can be prepared for free. Therefore
\(\rho_D\) alone determines and reconstructs the original encoded state.
Erasure of \(ABC\) is correctable. \(\square\)

This is the holographic step: once the interior is known to be
correctable, only a boundary collar can obstruct enlarging it.

### 3.4 Separated-Union Lemma

**Lemma.** Let \(M_1,\ldots,M_t\) be correctable regions such that no local
projector overlaps two of them. If every external boundary
\(\partial_+M_i\) is correctable, then

\[
               M_1\cup\cdots\cup M_t
\]

is correctable.

**Proof.** It is enough to verify (2.1). Expand an arbitrary operator on the
union as a sum of tensor products
\(O_{M_1}\otimes\cdots\otimes O_{M_t}\).

Apply the factorization from the proof of the Disentangling Lemma to
\(M_1\). No constraint touching \(M_1\) reaches any other \(M_j\), so

\[
\Pi
 (O_{M_1}\otimes O_{M_2}\otimes\cdots\otimes O_{M_t})
\Pi
=f_1(O_{M_1})
\Pi(O_{M_2}\otimes\cdots\otimes O_{M_t})\Pi.                  \tag{3.7}
\]

Repeat for \(M_2,\ldots,M_t\). The result is

\[
       \Pi O\Pi=c(O)\Pi,
\]

which is (2.1) for the union. \(\square\)

This is the first point where bounded interaction range matters. Weight
alone is insufficient: one bounded-weight projector could touch two
distant blocks and prevent (3.7).

## 4. Holographic correctability: side length is linear in distance

Let \(R_*\) be the largest integer such that **every** \(R_*\times R_*\)
square is correctable. Such a maximum exists for \(k>0\), because the full
lattice cannot be erased and recovered.

Distance alone gives only \(R_*=\Omega(\sqrt d)\): a square with fewer than
\(d\) sites is correctable. Locality improves this to

\[
                    R_*=\Omega(d/w).                           \tag{4.1}
\]

Take any correctable \(R_*\times R_*\) square \(M\). Let \(B\) be an
internal collar and \(C\) an external collar, each of thickness sufficient
to contain the support of every constraint crossing the cut. Then
\(\partial M\subseteq BC\), and (2.4) gives

\[
                    |BC|\leq c_\square w(R_*+w).               \tag{4.2}
\]

Suppose the right-hand side were smaller than \(d\). The collar \(BC\)
would be correctable. The Growth Lemma would make \(M\cup C\), a strictly
larger square, correctable. The construction works at every position, so it
would contradict maximality of \(R_*\).

Therefore

\[
             d\leq c_\square w(R_*+w).                         \tag{4.3}
\]

When \(d\) is larger than a fixed multiple of \(w^2\), (4.3) gives (4.1).
When it is not, the final theorem follows from the trivial entropy bound
\(k\leq n\log_2q\) after enlarging \(c(w,q)\).

Now choose a smaller mesoscopic length

\[
             \ell=\left\lfloor\alpha\,\frac d w\right\rfloor, \tag{4.4}
\]

where the geometry-only constant \(\alpha>0\) is small enough that:

1. \(\ell\leq R_*\), so every \(\ell\times\ell\) square is correctable;
2. every width-\(O(w)\) boundary collar of such a square has fewer than
   \(d\) sites and is therefore correctable.

This is the exact content hidden by the phrase “a box of side proportional
to \(d\) is correctable.” The proportionality constant depends on the
interaction range because the information bottleneck is the perimeter
\(O(w\ell)\).

## 5. The checkerboard partition

Tile the lattice by \(\ell\times\ell\) squares and color the tiles black and
white in a checkerboard pattern.

- \(A\) is the union of the black tiles after shaving an \(O(w)\)-sized
  patch from every corner.
- \(B\) is the analogous union of the white tiles.
- \(C\) is the union of all shaved corner patches.

The corner patches have two jobs. Black tiles meet other black tiles only
at corners, as do white tiles. Removing a collar wider than the interaction
range ensures that no projector touches two components of \(A\), and no
projector touches two components of \(B\).

Each component of \(A\) or \(B\) is a subset of an
\(\ell\times\ell\) correctable square. Its external boundary is correctable
by the choice of \(\ell\). The Separated-Union Lemma therefore gives:

\[
                        A\text{ and }B\text{ are correctable}. \tag{5.1}
\]

There are \(O(n/\ell^2)\) tile corners, and each removed patch contains
\(O(w^2)\) sites. Boundary fragments at the edge of an open lattice change
only the geometry constant. Hence

\[
                         |C|\leq c_C\,\frac{n w^2}{\ell^2}.     \tag{5.2}
\]

The diagram to keep in mind is not “large boxes separated by wide
corridors.” Wide corridors would occupy \(O(nw/\ell)\) sites and lose one
power of \(d\). The checkerboard needs only codimension-two intersections:
in two dimensions, those are isolated corner patches.

## 6. The entropy calculation

Evaluate the maximally mixed code state \(\rho_*=\Pi/2^k\) on the partition
\(\Lambda=ABC\).

Correctability of \(A\) and (2.2) give

\[
\begin{aligned}
k
  &=S(ABC)\\
  &=S(BC)+S(A\mid BC)\\
  &=S(BC)-S(A)\\
  &\leq S(B)+S(C)-S(A).                                      \tag{6.1}
\end{aligned}
\]

The last line is subadditivity. Interchanging \(A\) and \(B\) gives

\[
              k\leq S(A)+S(C)-S(B).                           \tag{6.2}
\]

Add (6.1) and (6.2). The unknown entropies of the two large checkerboards
cancel:

\[
                         k\leq S(C).                           \tag{6.3}
\]

Each site has dimension at most \(q\), so

\[
                         S(C)\leq |C|\log_2q.                  \tag{6.4}
\]

Substitute (5.2) and \(\ell=\Theta(d/w)\):

\[
\begin{aligned}
k
 &\leq c_C\log_2q\,\frac{n w^2}{\ell^2}\\
 &\leq c'(w,q)\,\frac{n}{d^2}.
\end{aligned}
\]

Equivalently,

\[
                         \boxed{k d^2\leq c'(w,q)n}.
\]

That completes the proof.

The flow of logical information is now visible. Both extensive regions
\(A\) and \(B\) may be erased. Quantum information cannot reside in either
one, yet together they cover almost the whole lattice. Their two entropy
identities force the logical entropy into the sparse intersection skeleton
\(C\), and geometry makes that skeleton too small to carry more than
\(O(n/d^2)\) qubits.

## 7. Consequences and saturation

### 7.1 Fixed \(k\)

For any family encoding at least one logical qubit,

\[
                         d=O(\sqrt n).
\]

This is why a two-dimensional surface-code patch with
\(n=\Theta(d^2)\) has the optimal distance exponent. The theorem does not
select the surface code or its constant prefactor; it says no code under the
same hypotheses can improve the exponent.

### 7.2 Nonzero rate

If \(k/n\) stays above a positive constant, then

\[
                         d=O(1).
\]

Thus a two-dimensional bounded-range commuting-projector family cannot
simultaneously have constant rate and growing distance.

### 7.3 Tightness

One planar surface-code patch has

\[
             k=1,\qquad n=\Theta(d^2).
\]

Placing \(k\) independent patches side by side gives

\[
             n=\Theta(kd^2).
\]

The BPT scaling is therefore tight up to a constant depending on layout and
microscopic locality. Rotating a patch or changing its boundary convention
can improve that constant, but cannot change the exponent while the theorem's
hypotheses remain true.

### 7.4 Higher dimensions

The same proof in \(D\) Euclidean dimensions uses a codimension-two
skeleton:

- the sparse region has size \(O(n/\ell^2)\);
- a cube of side \(\ell\) has boundary size
  \(O(\ell^{D-1})\);
- holographic correctability permits
  \(\ell^{D-1}=O(d)\).

Consequently,

\[
                k\leq c_D\,\frac{n}{d^{\,2/(D-1)}}.            \tag{7.1}
\]

For \(D=2\), (7.1) is the bound proved above. The original paper explicitly
notes that its higher-dimensional exponent need not be tight.

### 7.5 Why the classical companion has a different exponent

The same paper proves that a two-dimensional classical code specified by
bounded-range constraints obeys

\[
                         k\sqrt d=O(n).                         \tag{7.2}
\]

The shorter proof exposes the quantum difference. Choose separated square
blocks \(B_1,\ldots,B_t\), each containing fewer than \(d\) sites and having
side \(\Theta(\sqrt d)\). Let \(B=\bigcup_iB_i\), and let \(A\) be the
width-\(O(w)\) grid between them. Then

\[
                         |A|=O(nw/\sqrt d).                    \tag{7.3}
\]

Suppose two classical codewords \(x,y\) agree on \(A\). If they differ
inside some block \(B_i\), splice a new assignment \(z\): use \(x\) on
\(B_i\) and \(y\) everywhere else. Every local constraint sees at most one
block, and constraints meeting \(B_i\) see the same boundary values from
\(x\) and \(y\), so \(z\) is another codeword. But \(z\) and \(y\) differ
on fewer than \(d\) sites, contradicting distance. Therefore agreement on
\(A\) determines the whole codeword.

The restriction map from codewords to configurations on \(A\) is injective.
For bounded local alphabet size, the number of encoded bits satisfies

\[
                         k\leq c_q|A|,
\]

which together with (7.3) gives (7.2).

Classically, one thin grid is enough because a codeword can be copied and
compared. Quantumly, no-cloning and entanglement replace unique extension by
the negative conditional-entropy identity. Two correctable checkerboards are
needed, and their entropy cancellation leaves a codimension-two set. That is
why the quantum tradeoff contains \(d^2\), while the classical companion
contains only \(\sqrt d\).

## 8. What does and does not evade the theorem

| Change | Covered? | Reason |
|---|---|---|
| Replace square plaquettes by another bounded-density 2D tiling | Yes | Only bounded Euclidean geometry and bounded interaction range enter |
| Use qudits of a fixed dimension | Yes | The coefficient acquires a factor depending on \(\log_2 q\) |
| Use a Pauli stabilizer code with local generators | Yes | It is a special case of commuting local projectors |
| Keep checks low-weight but connect sites a growing Euclidean distance apart | No | Weight does not bound \(w\); the separated-union step fails |
| Embed the Tanner graph in two layers with long bridges | Not with a size-independent \(w\) | The relevant metric is the physical Euclidean layout, including bridges |
| Let the interaction range grow with \(n\) | No uniform asymptotic bound | The hidden coefficient depends on \(w\) |
| Use noncommuting local gauge checks of a subsystem code | Not by the original theorem | The commuting-projector boundary decomposition is unavailable |
| Move to a non-Euclidean family of graphs | Not as stated | The checkerboard and codimension-two counting use ordinary Euclidean growth |
| Move to \(D>2\) | A different tradeoff applies | Use (7.1), not the two-dimensional exponent |
| Improve a finite block's value of \(kd^2/n\) | Possibly | The theorem fixes asymptotic scaling, not a universal finite-size constant |

Two common confusions deserve emphasis.

**LDPC is not geometric locality.** LDPC bounds how many qubits a check
touches and how many checks touch a qubit. BPT additionally requires those
qubits to lie in a bounded Euclidean neighborhood. A family may be qLDPC
and still lie outside BPT.

**BPT is not a threshold theorem.** It constrains the static code parameters
\((n,k,d)\). It says nothing by itself about syndrome circuits, decoder
runtime, noise thresholds, or logical error rates.

## 9. BPT versus nearby no-go theorems

| Result | Resource constrained | Typical conclusion in 2D |
|---|---|---|
| Bravyi–Poulin–Terhal | Static information density under local commuting constraints | \(kd^2=O(n)\) |
| Bravyi–König | Logical gates implemented by bounded-depth local circuits | Only Clifford logical gates |
| Bravyi–Terhal | Thermal energy barrier of 2D local stabilizer Hamiltonians | No growing stabilizer energy barrier |
| Eastin–Knill | Exactly transversal gates on a finite-dimensional exact code | No universal transversal gate set |

These statements share examples but not proofs. BPT uses correctable-region
entropy and a geometric partition. It does not follow from the
Bravyi–König commutator argument, and neither theorem says that a surface
code is self-correcting.

## 10. Audit questions

**Q1. Why does distance first suggest only a \(\sqrt d\)-sized correctable
square, yet the proof obtains a \(d\)-sized square?**

**A.** Distance alone counts the square's area: fewer than \(d\) sites gives
side \(O(\sqrt d)\). Commuting locality changes the bottleneck from area to
boundary. The Growth Lemma says a correctable interior can keep expanding
until its width-\(w\) boundary collar has \(O(d)\) sites, which occurs at
side \(O(d/w)\).

**Q2. Where exactly is commutativity used?**

**A.** It makes the left and right interaction algebras on a boundary
commute. Their direct-sum tensor-product decomposition gives the
Disentangling Lemma and the Separated-Union Lemma. The final entropy
inequalities alone do not use commutativity.

**Q3. Why are two correctable checkerboards needed?**

**A.** One correctable region gives
\(k\leq S(B)+S(C)-S(A)\), which still contains the extensive difference
\(S(B)-S(A)\). Applying the same identity to \(B\) gives the opposite
difference; adding cancels both and leaves \(k\leq S(C)\).

**Q4. Why are the removed regions corner patches rather than corridors?**

**A.** Same-colored checkerboard tiles meet only at corners. Removing
bounded patches there separates equal colors. There are
\(O(n/\ell^2)\) corners, so the remainder has the \(1/\ell^2\) density
needed for \(1/d^2\). Width-\(w\) corridors would have density
\(O(w/\ell)\) and lose one power.

**Q5. Does a finite block with \(kd^2/n>1\) violate BPT?**

**A.** No. The constant in \(O(n)\) is not universally one, and a single
finite block cannot violate an asymptotic statement. To apply BPT to a
family, \(q\), the Euclidean interaction range, and the geometric
bounded-density constants must all remain fixed as \(n\) grows.

**Q6. Why does the theorem include non-Pauli commuting-projector codes but
exclude generic subsystem codes?**

**A.** Pauli algebra is not used. Pairwise commutativity of the defining
projectors is. Local subsystem gauge generators generally do not commute,
and their commuting stabilizers may be geometrically nonlocal, so the
boundary-algebra step does not automatically apply.

## 11. Source and citation audit

Primary source, fetch-verified on 2026-07-28:

- Sergey Bravyi, David Poulin, and Barbara Terhal, “Tradeoffs for reliable
  quantum information storage in 2D systems,”
  [arXiv:0909.5200](https://arxiv.org/abs/0909.5200), submitted
  28 September 2009; [Physical Review Letters 104, 050503
  (2010)](https://doi.org/10.1103/PhysRevLett.104.050503).

Boundary-algebra source, also fetch-verified on 2026-07-28:

- Sergey Bravyi and Mikhail Vyalyi, “Commutative version of the \(k\)-local
  Hamiltonian problem and common eigenspace problem,”
  [arXiv:quant-ph/0308021](https://arxiv.org/abs/quant-ph/0308021);
  *Quantum Information & Computation* 5, 187–215 (2005).

The precise hypotheses, erasure definition of distance, entropy identity,
Disentangling Lemma, Growth Lemma, separated-union argument, checkerboard
partition, quantum bound, classical contrast, and \(D\)-dimensional
generalization trace to the primary BPT source. This page expands the
boundary-algebra step, correctability criterion, entropy cancellation, and
constant-scale choices so that the cited paper supplies provenance rather
than a missing proof.

Atlas citation note: `atlas/surface/card.yaml` uses the bibkey
`bravyi2010tradeoffs`, while
`docs/lit/surface/surface-foundations.md` uses
`bravyipoulinterhal2010tradeoffs` for the same fetch-verified paper. T5
permits new files only, so this page records the mismatch instead of changing
either out-of-scope file. The planned reference-registry task should choose
one key and enforce it repository-wide.
