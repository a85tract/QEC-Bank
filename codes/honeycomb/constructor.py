"""Honeycomb (Hastings-Haah) Floquet code on an L1 x L2 hexagonal torus.

Rounds are grouped by the plaquette-3-coloring label of each edge (the one
color its two adjacent hexagons do not use), per Hastings-Haah; the Pauli type
of each check stays direction-determined (XX on x-links, YY on y-links, ZZ on
z-links), so every round mixes all three Pauli types. Grouping rounds by edge
direction instead yields the anisotropic Kitaev sequence, whose steady state
is wrong (dynamic_k = 0 at 2x2 and grows as (L-1)(L-2) on LxL tori).

Torus sizes must satisfy the plaquette 3-colorability constraint, which holds
iff L1 % 3 == 0 and L2 % 3 == 0 (verified empirically over L1, L2 in 2..9);
other sizes raise ValueError rather than building a silently wrong code.
"""
import math

from qeclib.checkmatrix import CheckMatrix
from qeclib.pauli import Pauli
from qeclib.schedule import Schedule, ISGTracker

_NEXT_TYPE = {"z": "x", "x": "y", "y": "z"}
_LETTER = {"x": "X", "y": "Y", "z": "Z"}

def _edges(L1: int, L2: int):
    """Hexagonal torus, two sites per cell: A=2*(i*L2+j), B=A+1.
    z-edge A(i,j)-B(i,j); x-edge B(i,j)-A(i+1,j); y-edge B(i,j)-A(i,j+1)."""
    A = lambda i, j: 2 * ((i % L1) * L2 + (j % L2))
    B = lambda i, j: A(i, j) + 1
    z, x, y = [], [], []
    for i in range(L1):
        for j in range(L2):
            z.append((A(i, j), B(i, j)))
            x.append((B(i, j), A(i + 1, j)))
            y.append((B(i, j), A(i, j + 1)))
    return x, y, z

def _faces(L1: int, L2: int, x, y, z):
    """Hexagonal faces traced from the adjacency: standing on a directed edge of
    type t, leave its head along that vertex's unique edge of type _NEXT_TYPE[t].
    Starting once per directed z-edge (A->B) yields each hexagon exactly once.
    Verifies: every walk closes in 6 steps with 6 distinct edges, and every
    edge of the graph borders exactly 2 hexagons."""
    n = 2 * L1 * L2
    nbr = [dict() for _ in range(n)]
    for et, edges in (("x", x), ("y", y), ("z", z)):
        for a, b in edges:
            nbr[a][et] = b
            nbr[b][et] = a
    faces = []
    for a, b in z:
        u, v, et = a, b, "z"
        face = []
        for _ in range(6):
            face.append((min(u, v), max(u, v), et))
            net = _NEXT_TYPE[et]
            u, v, et = v, nbr[v][net], net
        if (u, v, et) != (a, b, "z") or len(set(face)) != 6:
            raise ValueError(f"face walk from z-edge {(a, b)} is not a hexagon")
        faces.append(face)
    edge_faces = {}
    for fi, face in enumerate(faces):
        for e in face:
            edge_faces.setdefault(e, []).append(fi)
    if len(edge_faces) != 3 * L1 * L2 or any(len(fs) != 2 for fs in edge_faces.values()):
        raise ValueError("face structure invalid: every edge must border exactly 2 hexagons")
    return faces, edge_faces

def _face_coloring(faces, edge_faces, L1, L2):
    """Proper 3-coloring of the hexagons (faces sharing an edge get different
    colors). Tries the constructor convention, then triangle-forcing propagation.
    Returns None when the torus admits no proper coloring."""
    def proper(c):
        return all(c[f1] != c[f2] for f1, f2 in edge_faces.values())
    c = [
        (face_index // L2 - face_index % L2) % 3
        for face_index in range(len(faces))
    ]
    if proper(c):
        return c
    adj = {fi: set() for fi in range(len(faces))}
    for f1, f2 in edge_faces.values():
        adj[f1].add(f2)
        adj[f2].add(f1)
    f0, f1 = next(iter(edge_faces.values()))
    col = {f0: 0, f1: 1}  # wlog up to color permutation
    changed = True
    while changed:
        changed = False
        for g in adj:
            if g in col:
                continue
            known = {col[h] for h in adj[g] if h in col}
            if len(known) == 3:
                return None
            if len(known) == 2:
                col[g] = ({0, 1, 2} - known).pop()
                changed = True
    if len(col) != len(faces):
        return None
    c = [col[i] for i in range(len(faces))]
    return c if proper(c) else None


def _geometry(L1: int, L2: int) -> dict:
    """Exact equal-edge honeycomb embedding and its two torus period vectors."""
    basis_i = [math.sqrt(3) / 2, 1.5]
    basis_j = [-math.sqrt(3) / 2, 1.5]
    period_i = [L1 * basis_i[0], L1 * basis_i[1]]
    period_j = [L2 * basis_j[0], L2 * basis_j[1]]
    origin = [
        -(period_i[0] + period_j[0]) / 2,
        -(period_i[1] + period_j[1]) / 2,
    ]
    # Put both sublattices strictly inside the chosen cut.  The one-third-cell
    # shift centers the A/B pair in each cell and prevents a torus vertex from
    # being duplicated exactly at a fundamental-domain corner.
    cell_offset = [
        (basis_i[axis] + basis_j[axis]) / 3
        for axis in (0, 1)
    ]
    coords = []
    for i in range(L1):
        for j in range(L2):
            a_site = [
                origin[0] + cell_offset[0]
                + i * basis_i[0] + j * basis_j[0],
                origin[1] + cell_offset[1]
                + i * basis_i[1] + j * basis_j[1],
            ]
            coords.append(a_site)
            coords.append([a_site[0], a_site[1] + 1.0])
    return {
        "coords": coords,
        "layout": {
            "kind": "periodic",
            "origin": origin,
            "basis": [period_i, period_j],
        },
    }

def build(L1: int = 3, L2: int = 3):
    """Honeycomb Floquet code; checkmatrix = steady-state ISG snapshot after 6
    full periods (sign-free). Raises ValueError for non-3-colorable tori."""
    n = 2 * L1 * L2
    x, y, z = _edges(L1, L2)
    faces, edge_faces = _faces(L1, L2, x, y, z)
    coloring = _face_coloring(faces, edge_faces, L1, L2)
    if coloring is None:
        raise ValueError(
            f"honeycomb torus requires plaquette-3-colorable dimensions "
            f"(L1 % 3 == 0 and L2 % 3 == 0); got {L1}x{L2}")
    by_label = [[], [], []]
    for (a, b, et), (f1, f2) in edge_faces.items():
        label = 3 - coloring[f1] - coloring[f2]
        by_label[label].append((a, b, et))
    rounds = []
    for redges in by_label:
        if sorted(q for a, b, _ in redges for q in (a, b)) != list(range(n)):
            raise ValueError("honeycomb round is not a perfect matching")
        rnd = []
        for a, b, et in redges:
            chars = ["_"] * n
            chars[a] = chars[b] = _LETTER[et]
            rnd.append(Pauli.from_str("".join(chars)))
        rounds.append(rnd)
    sched = Schedule(n, rounds)
    sched.validate()
    tr = ISGTracker(n)
    for _ in range(6):
        for rnd in sched.rounds:
            for p in rnd:
                tr.measure(p)
    cm = CheckMatrix(tr.gens.copy())
    cm.validate()
    return {
        "checkmatrix": cm,
        "schedule": sched,
        "geometry": _geometry(L1, L2),
    }
