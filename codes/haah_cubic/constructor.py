"""Periodic CSS Code 1 from Haah's cubic-code classification.

The convention is fixed by the Laurent-polynomial pair

    f = 1 + x + y + z,
    g = 1 + xy + yz + zx.

An X generator uses ``f`` on orbital A and ``g`` on orbital B.  The Z
generator is obtained by spatial inversion and orbital exchange; after a
common ``xyz`` translation its supports are ``x+y+z+xyz`` on A and
``xy+xz+yz+xyz`` on B.  Translating both rows over an ``L x L x L`` torus
produces the finite CSS check matrix.

The returned Scene v2 is deliberately two-dimensional.  It is a dimetric
projection of exact three-dimensional constructor coordinates, not a planar
embedding of the code.  The projection metadata remains in the lattice
payload so a reader cannot mistake missing depth for physical locality.
"""

from __future__ import annotations

from itertools import product

import numpy as np

from qeclib import gf2
from qeclib.checkmatrix import CheckMatrix
from qeclib.scene import validate_scene


_X_OFFSETS = (
    ((0, 0, 0), (1, 0, 0), (0, 1, 0), (0, 0, 1)),
    ((0, 0, 0), (1, 1, 0), (0, 1, 1), (1, 0, 1)),
)
_Z_OFFSETS = tuple(
    tuple((1 - x, 1 - y, 1 - z) for x, y, z in offsets)
    for offsets in reversed(_X_OFFSETS)
)
_ORDERED_CORNERS = (
    (0, 0, 0),
    (1, 0, 0),
    (0, 1, 0),
    (0, 0, 1),
    (1, 1, 0),
    (0, 1, 1),
    (1, 0, 1),
    (1, 1, 1),
)
_PROJECTION = ((1.0, 0.0, 0.58), (0.0, -1.0, 0.41))
_ORBITAL_OFFSETS = ((-0.07, -0.045), (0.07, 0.045))


def _validate_length(L: int) -> int:
    if type(L) is not int or L < 2:
        raise ValueError("L must be an integer at least 2")
    return L


def vertex_index(L: int, x: int, y: int, z: int) -> int:
    """Return the periodic lexicographic vertex index."""
    L = _validate_length(L)
    return ((x % L) * L + (y % L)) * L + (z % L)


def qubit_index(L: int, x: int, y: int, z: int, orbital: int) -> int:
    """Return the index of orbital A=0 or B=1 at a periodic vertex."""
    if orbital not in (0, 1):
        raise ValueError("orbital must be 0 (A) or 1 (B)")
    return 2 * vertex_index(L, x, y, z) + orbital


def corner_operators() -> list[dict]:
    """Return the complete positive-cube Code 1 corner convention."""
    rows = []
    for corner in _ORDERED_CORNERS:
        x_letters = "".join(
            "X" if corner in _X_OFFSETS[orbital] else "I"
            for orbital in (0, 1)
        )
        z_letters = "".join(
            "Z" if corner in _Z_OFFSETS[orbital] else "I"
            for orbital in (0, 1)
        )
        rows.append(
            {"offset": list(corner), "X": x_letters, "Z": z_letters}
        )
    return rows


def cube_support(
    L: int,
    anchor: tuple[int, int, int],
    pauli: str,
) -> list[int]:
    """Return one translated weight-eight cube-generator support."""
    L = _validate_length(L)
    if pauli not in {"X", "Z"}:
        raise ValueError("pauli must be 'X' or 'Z'")
    offsets_by_orbital = _X_OFFSETS if pauli == "X" else _Z_OFFSETS
    x, y, z = anchor
    support = [
        qubit_index(L, x + dx, y + dy, z + dz, orbital)
        for orbital, offsets in enumerate(offsets_by_orbital)
        for dx, dy, dz in offsets
    ]
    if len(set(support)) != 8:
        raise ValueError("the local Code 1 support must contain eight qubits")
    return support


def _matrices(L: int) -> tuple[np.ndarray, np.ndarray]:
    row_count = L**3
    n = 2 * row_count
    hx = np.zeros((row_count, n), dtype=np.uint8)
    hz = np.zeros((row_count, n), dtype=np.uint8)
    for x, y, z in product(range(L), repeat=3):
        row = vertex_index(L, x, y, z)
        hx[row, cube_support(L, (x, y, z), "X")] = 1
        hz[row, cube_support(L, (x, y, z), "Z")] = 1
    return hx, hz


def _project_vertex(x: float, y: float, z: float) -> list[float]:
    return [
        _PROJECTION[0][0] * x
        + _PROJECTION[0][1] * y
        + _PROJECTION[0][2] * z,
        _PROJECTION[1][0] * x
        + _PROJECTION[1][1] * y
        + _PROJECTION[1][2] * z,
    ]


def _qubit_point(x: int, y: int, z: int, orbital: int) -> list[float]:
    center = _project_vertex(x, y, z)
    offset = _ORBITAL_OFFSETS[orbital]
    return [center[0] + offset[0], center[1] + offset[1]]


def _coords(L: int) -> list[list[float]]:
    coords: list[list[float] | None] = [None] * (2 * L**3)
    for x, y, z in product(range(L), repeat=3):
        for orbital in (0, 1):
            coords[qubit_index(L, x, y, z, orbital)] = _qubit_point(
                x, y, z, orbital
            )
    if any(point is None for point in coords):
        raise ValueError("projection did not assign every data qubit")
    return [point for point in coords if point is not None]


def _binary_row(n: int, support: list[int]) -> np.ndarray:
    row = np.zeros(n, dtype=np.uint8)
    row[support] = 1
    return row


def _plane_logicals(
    L: int,
    hx: np.ndarray,
    hz: np.ndarray,
) -> list[dict]:
    """Return one conjugate plane-logical pair when odd L makes it explicit."""
    if L % 2 == 0:
        return []
    logical_x = [
        qubit_index(L, 0, y, z, 0)
        for y, z in product(range(L), repeat=2)
    ]
    logical_z = [
        qubit_index(L, x, y, z, 0)
        for x, y, z in product(range(L), repeat=3)
        if (x + y) % L == 0
    ]
    x_row = _binary_row(2 * L**3, logical_x)
    z_row = _binary_row(2 * L**3, logical_z)
    if np.any((hz @ x_row) % 2) or np.any((hx @ z_row) % 2):
        raise ValueError("declared plane operators do not commute with checks")
    if gf2.in_rowspace(x_row, hx) or gf2.in_rowspace(z_row, hz):
        raise ValueError("declared plane operator is a stabilizer")
    if int((x_row @ z_row) % 2) != 1:
        raise ValueError("declared plane operators are not a conjugate pair")
    return [
        {
            "type": "X",
            "label": "X plane: orbital A on x = 0",
            "support": logical_x,
            "plane": "x = 0 (mod L)",
            "physicalShape": "two-dimensional periodic plane",
        },
        {
            "type": "Z",
            "label": "Z plane: orbital A on x + y = 0",
            "support": logical_z,
            "plane": "x + y = 0 (mod L)",
            "physicalShape": "two-dimensional periodic plane",
        },
    ]


def _centroid(points: list[list[float]]) -> list[float]:
    return [
        sum(point[0] for point in points) / len(points),
        sum(point[1] for point in points) / len(points),
    ]


def _cube_edges(anchor: tuple[int, int, int]) -> list[tuple[tuple[int, int, int], tuple[int, int, int]]]:
    vertices = [
        (anchor[0] + dx, anchor[1] + dy, anchor[2] + dz)
        for dx, dy, dz in product((0, 1), repeat=3)
    ]
    return [
        (first, second)
        for index, first in enumerate(vertices)
        for second in vertices[index + 1 :]
        if sum(a != b for a, b in zip(first, second)) == 1
    ]


def _scene(
    L: int,
    coords: list[list[float]],
    plane_logicals: list[dict],
) -> dict:
    anchor = (1, 1, 1) if L >= 3 else (0, 0, 0)
    edges = []
    for item, (first, second) in enumerate(_cube_edges(anchor)):
        edges.append(
            {
                "id": f"projected-edge-{item}",
                "kind": "segment",
                "points": [_project_vertex(*first), _project_vertex(*second)],
                "style": "neutral",
                "layer": "projected-cell",
                "item": item,
                "hitPoint": _centroid(
                    [_project_vertex(*first), _project_vertex(*second)]
                ),
                "label": (
                    "Projected edge of one cubic cell. This is a 2D dimetric "
                    "view of 3D geometry, not a planar interaction edge."
                ),
            }
        )
    orbital_pairs = []
    for offset, (dx, dy, dz) in enumerate(product((0, 1), repeat=3)):
        vertex = (anchor[0] + dx, anchor[1] + dy, anchor[2] + dz)
        qubits = [qubit_index(L, *vertex, orbital) for orbital in (0, 1)]
        points = [coords[qubit] for qubit in qubits]
        orbital_pairs.append(
            {
                "id": f"orbital-pair-{offset}",
                "kind": "segment",
                "points": points,
                "style": "mixed",
                "layer": "projected-cell",
                "item": len(edges) + offset,
                "hitPoint": _centroid(points),
                "label": (
                    f"Vertex {vertex}: qubits {qubits[0]} (orbital A) and "
                    f"{qubits[1]} (orbital B)."
                ),
            }
        )

    anchor_point = _project_vertex(
        anchor[0] + 0.5, anchor[1] + 0.5, anchor[2] + 0.5
    )
    representative_checks = []
    for item, pauli in enumerate(("X", "Z")):
        support = cube_support(L, anchor, pauli)
        representative_checks.append(
            {
                "id": f"representative-{pauli.lower()}",
                "kind": "spokes",
                "points": [anchor_point, *(coords[qubit] for qubit in support)],
                "style": pauli,
                "layer": "representative-checks",
                "item": item,
                "hitPoint": anchor_point,
                "label": (
                    f"Representative {pauli} cube generator at {anchor}; "
                    f"support {{{', '.join(str(qubit) for qubit in support)}}}. "
                    "All other rows are periodic translates."
                ),
            }
        )

    logical_objects = []
    for item, logical in enumerate(plane_logicals):
        points = [coords[qubit] for qubit in logical["support"]]
        logical_objects.append(
            {
                "id": f"plane-logical-{logical['type'].lower()}",
                "kind": "spokes",
                "points": [_centroid(points), *points],
                "style": logical["type"],
                "layer": "logical-supports",
                "item": item,
                "hitPoint": _centroid(points),
                "label": (
                    f"{logical['label']}; weight {len(logical['support'])}. "
                    "Projection rays mark support sites; they are not a string "
                    "operator or physical coupling graph."
                ),
            }
        )

    scene = {
        "schema": "qec-atlas-scene-v2",
        "dimension": 2,
        "origin": {
            "kind": "verified",
            "method": "haah-code1-dimetric-projection-v1",
        },
        "coordinateSystem": {"kind": "cartesian", "origin": [0.0, 0.0]},
        "camera": {
            "fit": "contain",
            "padding": 0.08,
            "minZoom": 0.5,
            "maxZoom": 10.0,
        },
        "layers": [
            {
                "id": "data",
                "label": "Projected data qubits",
                "kind": "data",
                "defaultVisible": True,
            },
            {
                "id": "projected-cell",
                "label": "Projected cubic cell",
                "kind": "cells",
                "defaultVisible": True,
            },
            {
                "id": "representative-checks",
                "label": "Representative cube checks",
                "kind": "checks",
                "defaultVisible": True,
            },
            {
                "id": "logical-supports",
                "label": "Projected plane logical supports",
                "kind": "logicals",
                "defaultVisible": True,
            },
        ],
        "nodes": [
            {
                "id": f"q{qubit_index(L, x, y, z, orbital)}",
                "position": coords[qubit_index(L, x, y, z, orbital)],
                "role": "data",
                "label": (
                    f"q{qubit_index(L, x, y, z, orbital)}: vertex "
                    f"({x}, {y}, {z}), orbital {'A' if orbital == 0 else 'B'}"
                ),
            }
            for x, y, z in product(range(L), repeat=3)
            for orbital in (0, 1)
        ],
        "frames": [
            {
                "id": "projected-unit-cell",
                "mode": "construction",
                "objects": [*edges, *orbital_pairs],
            },
            {
                "id": "representative-checks",
                "mode": "incidence",
                "objects": representative_checks,
            },
            {
                "id": "plane-logicals",
                "mode": "logical",
                "objects": logical_objects,
            },
        ],
    }
    validate_scene(scene)
    return scene


def build(L: int = 3) -> dict:
    """Build the periodic ``L x L x L`` qubit CSS Code 1 instance."""
    L = _validate_length(L)
    hx, hz = _matrices(L)
    checkmatrix = CheckMatrix.from_css(hx, hz)
    checkmatrix.validate()
    if checkmatrix.n != 2 * L**3:
        raise ValueError("periodic Code 1 must have two qubits per vertex")
    if set(hx.sum(axis=1).tolist()) != {8} or set(hz.sum(axis=1).tolist()) != {8}:
        raise ValueError("every translated Code 1 generator must have weight eight")
    if np.any((hx @ hz.T) % 2):
        raise ValueError("Code 1 CSS generators do not commute")

    coords = _coords(L)
    checks = [
        {"type": pauli, "support": row.nonzero()[0].tolist()}
        for pauli, matrix in (("X", hx), ("Z", hz))
        for row in matrix
    ]
    check_anchors = [
        _project_vertex(x + 0.5, y + 0.5, z + 0.5)
        for _pauli in ("X", "Z")
        for x, y, z in product(range(L), repeat=3)
    ]
    plane_logicals = _plane_logicals(L, hx, hz)
    for logical in plane_logicals:
        logical["path"] = [coords[qubit] for qubit in logical["support"]]
    lattice = {
        "coords": coords,
        "checks": checks,
        "logicalOperators": plane_logicals,
        "planeLogicalOperators": plane_logicals,
        "layout": {
            "kind": "projected-3d-periodic",
            "origin": [0.0, 0.0],
            "checkAnchors": check_anchors,
            "checkStyles": {"X": "spokes", "Z": "spokes"},
        },
        "geometry": {
            "physicalDimension": 3,
            "renderedDimension": 2,
            "projection": "dimetric",
            "projectionMatrix": [list(row) for row in _PROJECTION],
            "periods": [[L, 0, 0], [0, L, 0], [0, 0, L]],
            "faithfulEmbedding": False,
            "warning": (
                "The viewer shows a 2D projection of a 3D periodic lattice; "
                "overlap and apparent crossings have no planar-locality meaning."
            ),
        },
        "unitCell": {
            "identity": "Haah cubic CSS Code 1",
            "polynomials": {
                "X": ["1+x+y+z", "1+xy+yz+zx"],
                "Z": ["x+y+z+xyz", "xy+xz+yz+xyz"],
            },
            "cornerOperators": corner_operators(),
        },
    }
    return {
        "checkmatrix": checkmatrix,
        "lattice": lattice,
        "scene": _scene(L, coords, plane_logicals),
    }
