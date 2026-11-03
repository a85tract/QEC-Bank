"""Finite, deterministic witnesses for the quantum-expander HGP family.

The family definition is asymptotic: a biregular Tanner graph must satisfy
left and right small-set expansion with fixed parameters along a growing
sequence.  The founding paper obtains the required graphs probabilistically
and does not provide a deterministic asymptotic generator.  This constructor
therefore does something deliberately narrower and machine-checkable:

* build one of two named finite incidence matrices in a fixed order;
* exhaust every subset inside a declared finite cutoff on both Tanner sides;
* apply the repository's exact ``hgp(H, H)`` convention; and
* export the factor graph, expansion certificate, and a factor-derived logical
  witness from the same matrix.

Passing the finite predicate is not advertised as an explicit asymptotic
quantum-expander construction.  That distinction is part of the returned
certificate rather than a prose-only caveat.
"""

from __future__ import annotations

from itertools import combinations
from math import gcd

import numpy as np

from qeclib import gf2
from qeclib.checkmatrix import CheckMatrix
from qeclib.constructions import hgp
from qeclib.scene import validate_scene


_FACTOR_IDS = {
    "complete-graph-5-incidence",
    "affine-plane-4-incidence",
}


def _validate_factor_id(factor: str) -> str:
    if type(factor) is not str or factor not in _FACTOR_IDS:
        allowed = ", ".join(sorted(_FACTOR_IDS))
        raise ValueError(f"factor must be one of: {allowed}")
    return factor


def complete_graph_incidence(order: int = 5) -> tuple[np.ndarray, list[tuple[int, int]]]:
    """Return the vertex-edge incidence matrix of ``K_order``.

    Rows are vertices ``0, ..., order-1``.  Columns are unordered edges in
    lexicographic order.  T73 ships only ``order=5`` as an entry instance; the
    argument keeps the ordering rule directly testable.
    """
    if type(order) is not int or order < 3:
        raise ValueError("order must be an integer at least 3")
    edges = list(combinations(range(order), 2))
    matrix = np.zeros((order, len(edges)), dtype=np.uint8)
    for column, (first, second) in enumerate(edges):
        matrix[first, column] = 1
        matrix[second, column] = 1
    return matrix, edges


def _gf4_multiply(first: int, second: int) -> int:
    """Multiply polynomial-basis GF(4) elements modulo x^2+x+1."""
    if first not in range(4) or second not in range(4):
        raise ValueError("GF(4) elements must be integers from 0 through 3")
    result = 0
    multiplicand = first
    multiplier = second
    while multiplier:
        if multiplier & 1:
            result ^= multiplicand
        multiplier >>= 1
        multiplicand <<= 1
        if multiplicand & 0b100:
            multiplicand ^= 0b111
    return result


def affine_plane_4_incidence() -> tuple[np.ndarray, list[tuple], list[tuple[int, int]]]:
    """Return point-line incidence for AG(2,4) in a fixed GF(4) basis.

    Points are ``(x,y)`` in lexicographic order.  The first sixteen columns
    are ``y = slope*x + intercept`` ordered by ``(slope, intercept)``; the
    final four are vertical lines ``x = intercept``.
    """
    points = [(x, y) for x in range(4) for y in range(4)]
    lines: list[tuple] = [
        ("slope", slope, intercept)
        for slope in range(4)
        for intercept in range(4)
    ] + [("vertical", intercept) for intercept in range(4)]
    matrix = np.zeros((len(points), len(lines)), dtype=np.uint8)
    for row, (x, y) in enumerate(points):
        for column, line in enumerate(lines):
            if line[0] == "slope":
                _, slope, intercept = line
                matrix[row, column] = y == (
                    _gf4_multiply(slope, x) ^ intercept
                )
            else:
                _, intercept = line
                matrix[row, column] = x == intercept
    return matrix, lines, points


def factor_matrix(factor: str) -> tuple[np.ndarray, dict]:
    """Return one named factor and its deterministic label convention."""
    factor = _validate_factor_id(factor)
    if factor == "complete-graph-5-incidence":
        matrix, edges = complete_graph_incidence(5)
        return matrix, {
            "name": "vertex-edge incidence of K5",
            "leftLabels": [f"edge {first}-{second}" for first, second in edges],
            "rightLabels": [f"vertex {vertex}" for vertex in range(5)],
            "leftCutoff": 1,
            "rightCutoff": 2,
            "ordering": "K5 vertices 0..4; edges lexicographic",
        }
    matrix, lines, points = affine_plane_4_incidence()
    line_labels = [
        (
            f"y={line[1]}x+{line[2]}"
            if line[0] == "slope"
            else f"x={line[1]}"
        )
        for line in lines
    ]
    return matrix, {
        "name": "point-line incidence of AG(2,4)",
        "leftLabels": line_labels,
        "rightLabels": [f"point ({x},{y})" for x, y in points],
        "leftCutoff": 2,
        "rightCutoff": 2,
        "ordering": (
            "points lexicographic; nonvertical lines by slope/intercept, "
            "then vertical lines"
        ),
    }


def _fraction(numerator: int, denominator: int) -> dict:
    common = gcd(numerator, denominator)
    return {
        "numerator": numerator // common,
        "denominator": denominator // common,
    }


def _side_expansion(
    matrix: np.ndarray,
    *,
    side: str,
    cutoff: int,
) -> dict:
    """Exhaust one side's neighborhood deficit through ``cutoff``."""
    if side == "left":
        side_count = matrix.shape[1]
        degrees = matrix.sum(axis=0)

        def neighbors(subset: tuple[int, ...]) -> list[int]:
            return np.flatnonzero(matrix[:, subset].any(axis=1)).tolist()

    elif side == "right":
        side_count = matrix.shape[0]
        degrees = matrix.sum(axis=1)

        def neighbors(subset: tuple[int, ...]) -> list[int]:
            return np.flatnonzero(matrix[list(subset), :].any(axis=0)).tolist()

    else:
        raise ValueError("side must be 'left' or 'right'")
    if cutoff < 1 or cutoff > side_count:
        raise ValueError("expansion cutoff must be inside the finite side")
    if len(set(int(value) for value in degrees.tolist())) != 1:
        raise ValueError(f"{side} factor degrees are not biregular")
    degree = int(degrees[0])
    worst: tuple[int, int, tuple[int, ...], list[int]] | None = None
    tested = 0
    for size in range(1, cutoff + 1):
        for subset in combinations(range(side_count), size):
            neighborhood = neighbors(subset)
            denominator = degree * size
            loss = denominator - len(neighborhood)
            tested += 1
            candidate = (loss, denominator, subset, neighborhood)
            if worst is None or loss * worst[1] > worst[0] * denominator:
                worst = candidate
    if worst is None:
        raise ValueError("expansion enumeration tested no nonempty subset")
    loss, denominator, subset, neighborhood = worst
    return {
        "side": side,
        "vertexCount": side_count,
        "degree": degree,
        "cutoff": cutoff,
        "gamma": _fraction(cutoff, side_count),
        "worstDelta": _fraction(loss, denominator),
        "worstSubset": list(subset),
        "worstNeighborhood": neighborhood,
        "subsetsTested": tested,
        "strictlyBelowOneSixth": 6 * loss < denominator,
    }


def expansion_certificate(matrix: np.ndarray, left_cutoff: int, right_cutoff: int) -> dict:
    """Return an exhaustive finite two-sided small-set certificate."""
    matrix = np.asarray(matrix, dtype=np.uint8)
    if matrix.ndim != 2 or not matrix.size or np.any(matrix > 1):
        raise ValueError("factor matrix must be a nonempty binary matrix")
    left = _side_expansion(matrix, side="left", cutoff=left_cutoff)
    right = _side_expansion(matrix, side="right", cutoff=right_cutoff)
    if not left["strictlyBelowOneSixth"] or not right["strictlyBelowOneSixth"]:
        raise ValueError("finite factor does not meet delta_A, delta_B < 1/6")
    return {
        "schema": "qec-atlas-finite-bipartite-expansion-v1",
        "definition": "|Gamma(S)| >= (1-delta) * degree * |S|",
        "left": left,
        "right": right,
        "scope": "finite-cutoff-certificate-not-asymptotic-family",
    }


def _minimum_kernel_word(matrix: np.ndarray) -> tuple[int, list[int]]:
    """Exhaust a small binary kernel and return its first minimum support."""
    width = matrix.shape[1]
    for weight in range(1, width + 1):
        for support in combinations(range(width), weight):
            if not np.any(matrix[:, support].sum(axis=1) % 2):
                return weight, list(support)
    raise ValueError("factor kernel is trivial; no finite distance word exists")


def _first_coordinate_outside_rowspace(matrix: np.ndarray) -> int:
    for coordinate in range(matrix.shape[1]):
        unit = np.zeros(matrix.shape[1], dtype=np.uint8)
        unit[coordinate] = 1
        if not gf2.in_rowspace(unit, matrix):
            return coordinate
    raise ValueError("factor row space fills its ambient coordinate space")


def _logical_witness(
    matrix: np.ndarray,
    hx: np.ndarray,
    hz: np.ndarray,
) -> tuple[dict, dict]:
    """Lift one minimum factor word into an exact HGP X logical."""
    distance, factor_support = _minimum_kernel_word(matrix)
    transpose_distance, transpose_support = _minimum_kernel_word(matrix.T)
    anchor = _first_coordinate_outside_rowspace(matrix)
    n_a = matrix.shape[1]
    n_b = matrix.shape[0]
    quantum_n = n_a * n_a + n_b * n_b
    support = [anchor * n_a + coordinate for coordinate in factor_support]
    word = np.zeros(quantum_n, dtype=np.uint8)
    word[support] = 1
    if np.any((hz @ word) % 2):
        raise ValueError("factor-derived X witness does not commute with Z checks")
    if gf2.in_rowspace(word, hx):
        raise ValueError("factor-derived X witness is an X stabilizer")
    witness = {
        "type": "X",
        "sector": "A-by-A",
        "anchorFirstCoordinate": anchor,
        "factorSupport": factor_support,
        "support": support,
        "weight": len(support),
    }
    distances = {
        "classicalDistance": distance,
        "classicalDistanceSupport": factor_support,
        "transposeDistance": transpose_distance,
        "transposeDistanceSupport": transpose_support,
        "hgpTheoremLower": min(distance, transpose_distance),
        "logicalWitnessUpper": len(support),
    }
    return witness, distances


def _vertical_points(count: int, x: float) -> list[list[float]]:
    spacing = 0.45 if count > 12 else 0.7
    center = (count - 1) / 2
    return [[x, (center - index) * spacing] for index in range(count)]


def _product_point(qubit: int, n_a: int, n_b: int) -> list[float]:
    first_sector = n_a * n_a
    if qubit < first_sector:
        first, second = divmod(qubit, n_a)
        return [
            1.5 + 3.0 * second / max(1, n_a - 1),
            2.0 - 4.0 * first / max(1, n_a - 1),
        ]
    shifted = qubit - first_sector
    first, second = divmod(shifted, n_b)
    return [
        5.5 + 2.5 * second / max(1, n_b - 1),
        2.0 - 4.0 * first / max(1, n_b - 1),
    ]


def _centroid(points: list[list[float]]) -> list[float]:
    return [
        sum(point[0] for point in points) / len(points),
        sum(point[1] for point in points) / len(points),
    ]


def _scene(
    factor: str,
    matrix: np.ndarray,
    metadata: dict,
    hx: np.ndarray,
    hz: np.ndarray,
    logical_witness: dict,
) -> dict:
    """Show the classical factor first, then exact HGP sector witnesses."""
    n_b, n_a = matrix.shape
    left_points = _vertical_points(n_a, -4.0)
    # Span the same horizontal range as the product-sector frames.  Scene v2
    # shares one camera across modes, so keeping the factor sides too close
    # would compress the landing's construction view into the left margin.
    right_points = _vertical_points(n_b, 7.0)
    construction_objects = []
    for left in range(n_a):
        neighborhood = np.flatnonzero(matrix[:, left]).tolist()
        points = [left_points[left], *(right_points[right] for right in neighborhood)]
        construction_objects.append({
            "id": f"left-neighborhood-{left}",
            "kind": "spokes",
            "points": points,
            "style": "neutral",
            "layer": "factor-incidence",
            "item": left,
            "hitPoint": left_points[left],
            "label": (
                f"A[{left}] {metadata['leftLabels'][left]}; "
                f"neighbors in B {{{', '.join(str(item) for item in neighborhood)}}}."
            ),
        })
    for right in range(n_b):
        neighborhood = np.flatnonzero(matrix[right]).tolist()
        points = [right_points[right], *(left_points[left] for left in neighborhood)]
        construction_objects.append({
            "id": f"right-neighborhood-{right}",
            "kind": "spokes",
            "points": points,
            "style": "mixed",
            "layer": "factor-incidence",
            "item": n_a + right,
            "hitPoint": right_points[right],
            "label": (
                f"B[{right}] {metadata['rightLabels'][right]}; "
                f"neighbors in A {{{', '.join(str(item) for item in neighborhood)}}}."
            ),
        })

    sector_a = [[1.3, -2.2], [4.7, -2.2], [4.7, 2.2], [1.3, 2.2]]
    sector_b = [[5.3, -2.2], [8.2, -2.2], [8.2, 2.2], [5.3, 2.2]]
    incidence_objects = [
        {
            "id": "a-by-a-sector",
            "kind": "face",
            "points": sector_a,
            "style": "neutral",
            "layer": "product-sectors",
            "item": 0,
            "hitPoint": [3.0, 0.0],
            "label": f"A-by-A qubit sector with {n_a * n_a} coordinates.",
        },
        {
            "id": "b-by-b-sector",
            "kind": "face",
            "points": sector_b,
            "style": "neutral",
            "layer": "product-sectors",
            "item": 1,
            "hitPoint": [6.75, 0.0],
            "label": f"B-by-B qubit sector with {n_b * n_b} coordinates.",
        },
    ]
    quantum_n = n_a * n_a + n_b * n_b
    for item, (pauli, row) in enumerate((("X", hx[0]), ("Z", hz[0])), start=2):
        support = np.flatnonzero(row).tolist()
        points = [_product_point(qubit, n_a, n_b) for qubit in support]
        anchor = _centroid(points)
        incidence_objects.append({
            "id": f"representative-{pauli.lower()}-check",
            "kind": "spokes",
            "points": [anchor, *points],
            "style": pauli,
            "layer": "quantum-checks",
            "item": item,
            "hitPoint": anchor,
            "label": (
                f"Representative {pauli} HGP row; support "
                f"{{{', '.join(str(qubit) for qubit in support)}}} of {quantum_n}."
            ),
        })

    logical_points = [
        _product_point(qubit, n_a, n_b)
        for qubit in logical_witness["support"]
    ]
    logical_anchor = _centroid(logical_points)
    incidence_objects.append({
        "id": "minimum-factor-word-logical",
        "kind": "spokes",
        "points": [logical_anchor, *logical_points],
        "style": "X",
        "layer": "logical-witnesses",
        "item": 4,
        "hitPoint": logical_anchor,
        "label": (
            "X logical lifted from a minimum factor kernel word; "
            f"support {{{', '.join(str(qubit) for qubit in logical_witness['support'])}}}."
        ),
    })
    scene = {
        "schema": "qec-atlas-scene-v2",
        "dimension": 2,
        "origin": {
            "kind": "verified",
            "method": f"quantum-expander-factor-product-scene-v1:{factor}",
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
                "id": "factor-vertices",
                "label": "Classical factor vertices",
                "kind": "data",
                "defaultVisible": True,
            },
            {
                "id": "factor-incidence",
                "label": "Classical factor neighborhoods",
                "kind": "annotations",
                "defaultVisible": True,
            },
            {
                "id": "product-sectors",
                "label": "Quantum HGP qubit sectors",
                "kind": "cells",
                "defaultVisible": True,
            },
            {
                "id": "quantum-checks",
                "label": "Representative quantum checks",
                "kind": "checks",
                "defaultVisible": True,
            },
            {
                "id": "logical-witnesses",
                "label": "Factor-derived logical witness",
                "kind": "logicals",
                "defaultVisible": True,
            },
        ],
        "nodes": [
            *[
                {
                    "id": f"factor-a-{index}",
                    "position": point,
                    "role": "abstract",
                    "label": f"A[{index}] {metadata['leftLabels'][index]}",
                }
                for index, point in enumerate(left_points)
            ],
            *[
                {
                    "id": f"factor-b-{index}",
                    "position": point,
                    "role": "abstract",
                    "label": f"B[{index}] {metadata['rightLabels'][index]}",
                }
                for index, point in enumerate(right_points)
            ],
        ],
        "frames": [
            {
                "id": "classical-factor",
                "mode": "construction",
                "objects": construction_objects,
            },
            {
                "id": "hgp-checks",
                "mode": "incidence",
                "objects": incidence_objects,
            },
        ],
    }
    validate_scene(scene)
    return scene


def build(factor: str = "complete-graph-5-incidence") -> dict:
    """Build one deterministic finite factor witness and its HGP code."""
    factor = _validate_factor_id(factor)
    matrix, metadata = factor_matrix(factor)
    certificate = expansion_certificate(
        matrix,
        metadata["leftCutoff"],
        metadata["rightCutoff"],
    )
    hx, hz = hgp(matrix, matrix)
    checkmatrix = CheckMatrix.from_css(hx, hz)
    checkmatrix.validate()
    n_b, n_a = matrix.shape
    if checkmatrix.n != n_a * n_a + n_b * n_b:
        raise ValueError("HGP qubit sectors do not match the factor dimensions")
    if np.any((hx @ hz.T) % 2):
        raise ValueError("HGP CSS checks fail exact commutation")
    expected_weight = int(matrix[:, 0].sum() + matrix[0].sum())
    if set(int(value) for value in hx.sum(axis=1)) != {expected_weight}:
        raise ValueError("X-check weights do not match Delta_A + Delta_B")
    if set(int(value) for value in hz.sum(axis=1)) != {expected_weight}:
        raise ValueError("Z-check weights do not match Delta_A + Delta_B")
    logical_witness, distance_certificate = _logical_witness(matrix, hx, hz)
    factor_data = {
        "schema": "qec-atlas-quantum-expander-factor-v1",
        "id": factor,
        "name": metadata["name"],
        "parityCheck": matrix.tolist(),
        "shape": [n_b, n_a],
        "rank": gf2.rank(matrix),
        "leftLabels": metadata["leftLabels"],
        "rightLabels": metadata["rightLabels"],
        "ordering": metadata["ordering"],
        "expansion": certificate,
        "distance": distance_certificate,
        "asymptoticStatus": (
            "finite certificate only; not a deterministic growing family "
            "with fixed degrees and fixed gamma"
        ),
    }
    coords = [
        _product_point(qubit, n_a, n_b)
        for qubit in range(checkmatrix.n)
    ]
    logical_operator = {
        "type": logical_witness["type"],
        "label": "X logical lifted from a minimum classical factor word",
        "support": logical_witness["support"],
        "path": [coords[qubit] for qubit in logical_witness["support"]],
    }
    return {
        "checkmatrix": checkmatrix,
        "factor": factor_data,
        "logicalWitness": logical_witness,
        "lattice": {
            "coords": coords,
            "checks": [],
            "logicalOperators": [logical_operator],
            "layout": {
                "kind": "abstract-product-sectors",
                "origin": [0.0, 0.0],
            },
        },
        "scene": _scene(
            factor,
            matrix,
            metadata,
            hx,
            hz,
            logical_witness,
        ),
    }
