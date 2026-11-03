"""Kitaev's toric code on an L x L periodic square lattice.

Qubits live on edges of the lattice (periodic in both directions).
X-checks sit on vertices (product of X on the 4 incident edges).
Z-checks sit on plaquettes/faces (product of Z on the 4 boundary edges).

We build this as a length-2 chain complex over GF(2):

    C2 (plaquettes) --d2--> C1 (edges = qubits) --d1--> C0 (vertices)

with d1 the vertex-edge incidence matrix (shape n0 x n1) and d2 the
edge-plaquette incidence matrix (shape n1 x n2), satisfying d1 @ d2 = 0
(the boundary of a boundary vanishes: each edge of a plaquette touches
each of its two endpoint-vertices an even number of times when you sum
over the plaquette's boundary... concretely here every plaquette
contributes exactly 2 edges to each of its corner vertices, but the
relevant identity is checked directly by ChainComplex.validate()).

ChainComplex(d1, d2) puts qubits on the middle grading and exposes
HX = d1 (vertex checks against edges), HZ = d2.T (plaquette checks
against edges). Both check sets have weight 4 (each vertex has degree
4, each plaquette has 4 boundary edges), and commute because every
plaquette shares exactly 0 or 2 edges with the star of the incident
vertex -- guaranteed by d1 @ d2 = 0 over GF(2).

Standard facts (Kitaev 2003): n = 2 L^2 qubits, k = 2 logical qubits
(one pair per handle of the torus), d = L (minimum-weight logical
operator is a non-contractible loop of length L on the lattice or its
dual).
"""
import numpy as np

from qeclib.chain import ChainComplex
from qeclib.gf2 import in_rowspace


def build(L: int = 3):
    """Toric code on an L x L torus. Returns n = 2 L^2 qubits, k = 2, d = L.

    Lattice indexing (all coordinates taken mod L):
      - vertices v(x, y)      = x*L + y,             for x, y in [0, L)
      - horiz. edges h(x, y)  = x*L + y,              edge (x,y) -> (x+1,y)
      - vert. edges  w(x, y)  = L^2 + x*L + y,        edge (x,y) -> (x,y+1)
      - plaquettes   p(x, y)  = x*L + y,              corners (x,y),(x+1,y),
                                                       (x,y+1),(x+1,y+1)
    Qubits are the edges, indices [0, 2L^2): horizontal edges first, then
    vertical edges.
    """
    if type(L) is not int or L < 2:
        raise ValueError("L must be an integer >= 2")

    n0 = L * L        # vertices
    n1 = 2 * L * L    # edges = qubits
    n2 = L * L        # plaquettes

    def vidx(x, y):
        return (x % L) * L + (y % L)

    def hidx(x, y):
        return (x % L) * L + (y % L)

    def widx(x, y):
        return n0 + (x % L) * L + (y % L)

    def pidx(x, y):
        return (x % L) * L + (y % L)

    d1 = np.zeros((n0, n1), dtype=np.uint8)  # vertices x edges (X-checks)
    d2 = np.zeros((n1, n2), dtype=np.uint8)  # edges x plaquettes (-> Z-checks via .T)

    for x in range(L):
        for y in range(L):
            v = vidx(x, y)
            # the 4 edges incident to vertex (x, y)
            d1[v, hidx(x, y)] ^= 1       # to the right
            d1[v, hidx(x - 1, y)] ^= 1   # from the left
            d1[v, widx(x, y)] ^= 1       # upward
            d1[v, widx(x, y - 1)] ^= 1   # from below

    for x in range(L):
        for y in range(L):
            p = pidx(x, y)
            # the 4 edges bounding plaquette (x, y)
            d2[hidx(x, y), p] ^= 1
            d2[hidx(x, y + 1), p] ^= 1
            d2[widx(x, y), p] ^= 1
            d2[widx(x + 1, y), p] ^= 1

    cc = ChainComplex(d1, d2)
    cc.validate()
    cm = cc.to_checkmatrix()
    cm.validate()

    coords = [None] * n1
    checks = []
    for x in range(L):
        for y in range(L):
            coords[hidx(x, y)] = [x + 0.5, float(y)]
            coords[widx(x, y)] = [float(x), y + 0.5]

    for x in range(L):
        for y in range(L):
            v = vidx(x, y)
            support = [hidx(x, y), hidx(x - 1, y), widx(x, y), widx(x, y - 1)]
            checks.append({"type": "X", "support": sorted(set(support))})
    for x in range(L):
        for y in range(L):
            p = pidx(x, y)
            support = [hidx(x, y), hidx(x, y + 1), widx(x, y), widx(x + 1, y)]
            checks.append({"type": "Z", "support": sorted(set(support))})

    check_anchors = []
    for x in range(L):
        for y in range(L):
            check_anchors.append([float(x), float(y)])
    for x in range(L):
        for y in range(L):
            check_anchors.append([x + 0.5, y + 0.5])

    logical_operators = [
        {
            "type": "Z",
            "label": "Z_x: primal horizontal cycle",
            "support": [hidx(x, 1) for x in range(L)],
            "path": [
                [0.0, 1.0],
                *[[x + 0.5, 1.0] for x in range(L)],
                [float(L), 1.0],
            ],
        },
        {
            "type": "X",
            "label": "X_x: conjugate dual vertical cycle",
            "support": [hidx(0, y) for y in range(L)],
            "path": [
                [0.5, 0.0],
                *[[0.5, float(y)] for y in range(1, L)],
                [0.5, float(L)],
            ],
        },
        {
            "type": "Z",
            "label": "Z_y: primal vertical cycle",
            "support": [widx(1, y) for y in range(L)],
            "path": [
                [1.0, 0.0],
                *[[1.0, y + 0.5] for y in range(L)],
                [1.0, float(L)],
            ],
        },
        {
            "type": "X",
            "label": "X_y: conjugate dual horizontal cycle",
            "support": [widx(x, 0) for x in range(L)],
            "path": [
                [0.0, 0.5],
                *[[float(x), 0.5] for x in range(1, L)],
                [float(L), 0.5],
            ],
        },
    ]
    logical_rows = []
    for logical in logical_operators:
        row = np.zeros(2 * n1, dtype=np.uint8)
        offset = 0 if logical["type"] == "X" else n1
        row[offset + np.asarray(logical["support"], dtype=int)] = 1
        commutators = (
            cm.stab[:, :n1] @ row[n1:]
            + cm.stab[:, n1:] @ row[:n1]
        ) % 2
        if np.any(commutators):
            raise ValueError(
                f"{logical['label']} does not commute with every stabilizer"
            )
        if in_rowspace(row, cm.stab):
            raise ValueError(
                f"{logical['label']} is a stabilizer, not a logical operator"
            )
        logical_rows.append(row)

    symplectic_products = np.zeros((4, 4), dtype=np.uint8)
    for first, left in enumerate(logical_rows):
        for second, right in enumerate(logical_rows):
            symplectic_products[first, second] = (
                left[:n1] @ right[n1:]
                + left[n1:] @ right[:n1]
            ) % 2
    expected_products = np.zeros((4, 4), dtype=np.uint8)
    expected_products[0, 1] = expected_products[1, 0] = 1
    expected_products[2, 3] = expected_products[3, 2] = 1
    if not np.array_equal(symplectic_products, expected_products):
        raise ValueError("logical operators do not form two conjugate pairs")

    lattice = {
        "coords": coords,
        "checks": checks,
        "logicalOperators": logical_operators,
        "layout": {
            "kind": "periodic",
            "origin": [0.0, 0.0],
            "basis": [[float(L), 0.0], [0.0, float(L)]],
            "checkAnchors": check_anchors,
            "checkStyles": {"X": "spokes", "Z": "face"},
        },
    }

    return {"checkmatrix": cm, "lattice": lattice}
