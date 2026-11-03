"""Executable rectangular Bacon–Shor subsystem family.

Qubits use row-major order.  The orientation is chosen so that the square
3-by-3 member gauge-fixes directly to the repository's Shor-code convention:
X gauge generators are vertical nearest-neighbour pairs and Z gauge
generators are horizontal nearest-neighbour pairs.
"""

from __future__ import annotations

import numpy as np

from qeclib import gf2
from qeclib.checkmatrix import CheckMatrix
from qeclib.pauli import Pauli
from qeclib.scene import validate_scene


def _validated_size(value: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 2:
        raise ValueError(f"{name} must be an integer at least 2")
    return value


def _index(row: int, column: int, columns: int) -> int:
    return row * columns + column


def _pauli(n: int, kind: str, support: list[int]) -> str:
    letters = ["_"] * n
    for qubit in support:
        letters[qubit] = kind
    return "".join(letters)


def _symplectic_product(first: np.ndarray, second: np.ndarray) -> int:
    n = len(first) // 2
    return int((first[:n] @ second[n:] + first[n:] @ second[:n]) % 2)


def gauge_supports(rows: int, columns: int) -> list[tuple[str, list[int]]]:
    """Return the independent local gauge generators in declared row order."""
    x_vertical = [
        (
            "X",
            [
                _index(row, column, columns),
                _index(row + 1, column, columns),
            ],
        )
        for row in range(rows - 1)
        for column in range(columns)
    ]
    z_horizontal = [
        (
            "Z",
            [
                _index(row, column, columns),
                _index(row, column + 1, columns),
            ],
        )
        for row in range(rows)
        for column in range(columns - 1)
    ]
    return [*x_vertical, *z_horizontal]


def stabilizer_supports(rows: int, columns: int) -> list[tuple[str, list[int]]]:
    """Return an independent basis for the center of the gauge group."""
    x_row_pairs = [
        (
            "X",
            [
                *(_index(row, column, columns) for column in range(columns)),
                *(
                    _index(row + 1, column, columns)
                    for column in range(columns)
                ),
            ],
        )
        for row in range(rows - 1)
    ]
    z_column_pairs = [
        (
            "Z",
            [
                *(_index(row, column, columns) for row in range(rows)),
                *(
                    _index(row, column + 1, columns)
                    for row in range(rows)
                ),
            ],
        )
        for column in range(columns - 1)
    ]
    return [*x_row_pairs, *z_column_pairs]


def logical_supports(rows: int, columns: int) -> list[tuple[str, list[int]]]:
    """Return one bare logical pair: X across row zero, Z down column zero."""
    return [
        ("X", [_index(0, column, columns) for column in range(columns)]),
        ("Z", [_index(row, 0, columns) for row in range(rows)]),
    ]


def _operator_label(prefix: str, item: int, pauli: str, support: list[int]) -> str:
    return (
        f"{prefix} {item}: {pauli}; support "
        f"{{{', '.join(str(qubit) for qubit in support)}}}."
    )


def _scene(
    rows: int,
    columns: int,
    stabilizers: list[tuple[str, list[int]]],
    gauges: list[tuple[str, list[int]]],
) -> dict:
    coords = [
        [float(column), float(-row)]
        for row in range(rows)
        for column in range(columns)
    ]
    n = rows * columns

    gauge_objects = []
    for item, (kind, support) in enumerate(gauges):
        points = [coords[qubit] for qubit in support]
        gauge_objects.append(
            {
                "id": f"gauge-{item}",
                "kind": "segment",
                "points": points,
                "style": kind,
                "layer": "gauge-generators",
                "item": item,
                "hitPoint": [
                    sum(point[0] for point in points) / 2.0,
                    sum(point[1] for point in points) / 2.0,
                ],
                "label": _operator_label(
                    "Gauge generator",
                    item,
                    _pauli(n, kind, support),
                    support,
                ),
            }
        )

    center_objects = []
    for item, (kind, support) in enumerate(stabilizers):
        if kind == "X":
            row = item
            polygon_support = [
                *(_index(row, column, columns) for column in range(columns)),
                *(
                    _index(row + 1, column, columns)
                    for column in reversed(range(columns))
                ),
            ]
        else:
            column = item - (rows - 1)
            polygon_support = [
                *(_index(row, column, columns) for row in range(rows)),
                *(
                    _index(row, column + 1, columns)
                    for row in reversed(range(rows))
                ),
            ]
        points = [coords[qubit] for qubit in polygon_support]
        center_objects.append(
            {
                "id": f"stabilizer-{item}",
                "kind": "face",
                "points": points,
                "style": kind,
                "layer": "stabilizer-center",
                "item": item,
                "hitPoint": [
                    sum(coords[qubit][0] for qubit in support) / len(support),
                    sum(coords[qubit][1] for qubit in support) / len(support),
                ],
                "label": _operator_label(
                    "Center stabilizer",
                    item,
                    _pauli(n, kind, support),
                    support,
                ),
            }
        )

    logical_objects = []
    for item, (kind, support) in enumerate(logical_supports(rows, columns)):
        points = [coords[qubit] for qubit in support]
        logical_objects.append(
            {
                "id": f"logical-{item}",
                "kind": "polyline",
                "points": points,
                "style": kind,
                "layer": "logical-operators",
                "item": item,
                "hitPoint": [
                    sum(point[0] for point in points) / len(points),
                    sum(point[1] for point in points) / len(points),
                ],
                "label": _operator_label(
                    "Bare logical",
                    item,
                    _pauli(n, kind, support),
                    support,
                ),
            }
        )

    scene = {
        "schema": "qec-atlas-scene-v2",
        "dimension": 2,
        "origin": {
            "kind": "verified",
            "method": "bacon-shor-gauge-center-scene-v1",
        },
        "coordinateSystem": {"kind": "cartesian", "origin": [0.0, 0.0]},
        "camera": {
            "fit": "contain",
            "padding": 0.12,
            "minZoom": 0.5,
            "maxZoom": 8.0,
        },
        "layers": [
            {
                "id": "data",
                "label": "Data qubits",
                "kind": "data",
                "defaultVisible": True,
            },
            {
                "id": "gauge-generators",
                "label": "Weight-two gauge generators",
                "kind": "checks",
                "defaultVisible": True,
            },
            {
                "id": "stabilizer-center",
                "label": "Gauge-group center",
                "kind": "checks",
                "defaultVisible": True,
            },
            {
                "id": "logical-operators",
                "label": "Bare logical operators",
                "kind": "logicals",
                "defaultVisible": True,
            },
        ],
        "nodes": [
            {
                "id": f"q{qubit}",
                "position": point,
                "role": "data",
                "label": (
                    f"q{qubit} · row {qubit // columns}, "
                    f"column {qubit % columns}"
                ),
            }
            for qubit, point in enumerate(coords)
        ],
        "frames": [
            {
                "id": "gauge-generators",
                "mode": "construction",
                "objects": gauge_objects,
            },
            {
                "id": "stabilizer-center",
                "mode": "incidence",
                "objects": center_objects,
            },
            {
                "id": "bare-logicals",
                "mode": "logical",
                "objects": logical_objects,
            },
        ],
    }
    validate_scene(scene)
    return scene


def _lattice_data(
    rows: int,
    columns: int,
    stabilizers: list[tuple[str, list[int]]],
) -> dict:
    """Expose the shared lattice/logical ports consumed by generic tours."""
    coords = [
        [float(column), float(-row)]
        for row in range(rows)
        for column in range(columns)
    ]
    logicals = logical_supports(rows, columns)
    return {
        "coords": coords,
        "checks": [
            {"type": kind, "support": support}
            for kind, support in stabilizers
        ],
        "logicalOperators": [
            {
                "type": kind,
                "label": "Bare logical X" if kind == "X" else "Bare logical Z",
                "support": support,
                "path": [coords[qubit] for qubit in support],
            }
            for kind, support in logicals
        ],
    }


def _validate_subsystem_structure(
    cm: CheckMatrix,
    rows: int,
    columns: int,
    logicals: list[tuple[str, list[int]]],
) -> None:
    stabilizer_rank = gf2.rank(cm.stab)
    gauge_rank = gf2.rank(cm.gauge)
    if stabilizer_rank != rows + columns - 2:
        raise ValueError("unexpected Bacon-Shor stabilizer rank")
    if gauge_rank != 2 * rows * columns - rows - columns:
        raise ValueError("unexpected Bacon-Shor gauge rank")
    if gf2.rank(np.vstack([cm.gauge, cm.stab])) != gauge_rank:
        raise ValueError("stabilizer center is not contained in the gauge span")
    if cm.k != 1:
        raise ValueError("rectangular Bacon-Shor constructor must encode one qubit")

    logical_rows = [
        Pauli.from_str(_pauli(cm.n, kind, support)).symplectic()
        for kind, support in logicals
    ]
    for logical in logical_rows:
        if any(_symplectic_product(logical, row) for row in cm.stab):
            raise ValueError("declared logical does not commute with the stabilizer")
        if any(_symplectic_product(logical, row) for row in cm.gauge):
            raise ValueError("declared bare logical does not commute with the gauge group")
    if _symplectic_product(logical_rows[0], logical_rows[1]) != 1:
        raise ValueError("declared Bacon-Shor logical pair must anticommute")


def build(rows: int, columns: int) -> dict:
    """Return a deterministic subsystem CheckMatrix and derived Scene v2."""
    rows = _validated_size(rows, "rows")
    columns = _validated_size(columns, "columns")
    n = rows * columns
    stabilizers = stabilizer_supports(rows, columns)
    gauges = gauge_supports(rows, columns)
    logicals = logical_supports(rows, columns)

    cm = CheckMatrix.from_paulis(
        [_pauli(n, kind, support) for kind, support in stabilizers],
        gauge=[_pauli(n, kind, support) for kind, support in gauges],
    )
    cm.validate()
    _validate_subsystem_structure(cm, rows, columns, logicals)
    return {
        "checkmatrix": cm,
        "lattice": _lattice_data(rows, columns, stabilizers),
        "scene": _scene(rows, columns, stabilizers, gauges),
    }
