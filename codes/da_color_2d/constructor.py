"""Finite schedule witness for the Pauli-triangle DA color-code protocol.

The constructor encodes the complete padded ``t=0,...,8`` ledger selected by
T71.  Twelve labelled sites are doubled into layers 1 and 2.  The first nine
sites form a finite three-edge-coloured triangle incidence graph; the last
three are the red, green, and blue docking sites used at the Y boundary.

This is a schedule-complete *incidence witness*: it makes every measured Pauli
literal, checks commutation within every round, and recomputes the sign-free
instantaneous stabilizer group (ISG).  It is not a claim that the coarse
coordinates reproduce the metric embedding of the paper's smallest
distance-three patch.  In particular, no static or spacetime distance is
exported from this constructor.

The reference ``CheckMatrix`` is the first complete post-startup ISG, after
round index 4.  The engine can verify its rank and the repeated row space at
round 8.  Transport of logical representatives through outcome-dependent
measurements is not yet a qeclib primitive, so the paper's X_L -> Z_L -> Y_L
frame map is exported separately with a fail-closed, curated status.
"""

from __future__ import annotations

import numpy as np

from qeclib import gf2
from qeclib.checkmatrix import CheckMatrix
from qeclib.pauli import Pauli
from qeclib.schedule import ISGTracker, Schedule
from qeclib.scene import validate_scene


PATCH_ID = "table8-pauli-triangle-incidence-v1"
SITE_COUNT = 12
QUBIT_COUNT = 2 * SITE_COUNT
REFERENCE_ROUND = 4

# Same-colour edges are disjoint.  The three matchings make the measurement
# class E_c(P_layer) executable without smuggling a drawing into the logic.
EDGE_SETS = {
    "red": ((0, 1), (3, 4), (5, 6), (2, 8), (7, 10)),
    "green": ((2, 3), (5, 0), (4, 7), (1, 8), (6, 9)),
    "blue": ((1, 2), (4, 5), (0, 6), (3, 7), (8, 11)),
}
DOCK_SITES = {"red": 10, "green": 9, "blue": 11}
X_BOUNDARY_SITES = (0,)
Z_BOUNDARY_SITES = (1, 3, 5)
BULK_VERTICAL_SITES = (2, 4, 6, 7, 8)

# A topology-first triangular layout.  Layer 2 is offset slightly so vertical
# and intralayer measurements remain distinguishable in the shared viewer.
SITE_COORDS = (
    (-1.80, -1.00),
    (-1.05, -0.15),
    (-0.65, -1.00),
    (-0.15, 0.70),
    (0.25, -1.00),
    (0.55, 0.20),
    (0.85, 1.10),
    (1.15, -0.35),
    (1.45, 0.55),
    (2.35, 1.20),
    (2.55, 0.25),
    (2.60, -0.80),
)


def _validate_patch(patch: str) -> str:
    if type(patch) is not str or patch != PATCH_ID:
        raise ValueError(f"patch must be {PATCH_ID!r}")
    return patch


def _qubit(site: int, layer: int) -> int:
    if site not in range(SITE_COUNT):
        raise ValueError("site must be between 0 and 11")
    if layer not in (1, 2):
        raise ValueError("layer must be 1 or 2")
    return site + (layer - 1) * SITE_COUNT


def _pauli(assignments: tuple[tuple[int, str], ...]) -> Pauli:
    word = ["_"] * QUBIT_COUNT
    for qubit, letter in assignments:
        if qubit not in range(QUBIT_COUNT):
            raise ValueError("measurement qubit is outside the patch stack")
        if letter not in {"X", "Y", "Z"}:
            raise ValueError("measurement letters must be X, Y, or Z")
        if word[qubit] != "_" and word[qubit] != letter:
            raise ValueError("one measurement assigns two Paulis to one qubit")
        word[qubit] = letter
    return Pauli.from_str("".join(word))


def _edge_measurements(
    color: str,
    layer: int,
    letter: str,
) -> list[Pauli]:
    return [
        _pauli(((_qubit(first, layer), letter), (_qubit(second, layer), letter)))
        for first, second in EDGE_SETS[color]
    ]


def _vertical(site: int, first: str, second: str) -> Pauli:
    return _pauli(((_qubit(site, 1), first), (_qubit(site, 2), second)))


def _single(site: int, layer: int, letter: str) -> Pauli:
    return _pauli(((_qubit(site, layer), letter),))


def _base_rounds() -> list[list[Pauli]]:
    """Return the four Table-8 measurement classes before padding repeats."""
    round_zero = [
        _vertical(site, "Z", "Z") for site in BULK_VERTICAL_SITES
    ]
    round_zero += [_vertical(site, "X", "X") for site in X_BOUNDARY_SITES]
    round_zero += [
        _single(site, layer, "Z")
        for site in Z_BOUNDARY_SITES
        for layer in (1, 2)
    ]
    round_zero += [
        _vertical(DOCK_SITES["red"], "X", "Y"),
        _vertical(DOCK_SITES["green"], "Y", "X"),
        _vertical(DOCK_SITES["blue"], "X", "Y"),
    ]

    round_one = _edge_measurements("red", 1, "X")
    round_one += _edge_measurements("green", 2, "X")
    round_one += [
        _vertical(DOCK_SITES["red"], "X", "Z"),
        _vertical(DOCK_SITES["green"], "Z", "X"),
        _vertical(DOCK_SITES["blue"], "X", "Z"),
        _vertical(DOCK_SITES["blue"], "Z", "X"),
    ]
    round_one += [
        _single(site, layer, "X")
        for site in X_BOUNDARY_SITES
        for layer in (1, 2)
    ]

    round_two = _edge_measurements("green", 1, "Z")
    round_two += _edge_measurements("blue", 2, "Z")
    round_two += [
        _vertical(DOCK_SITES["blue"], "X", "Z"),
        _vertical(DOCK_SITES["green"], "Z", "X"),
        _vertical(DOCK_SITES["red"], "X", "Z"),
        _vertical(DOCK_SITES["red"], "Z", "X"),
    ]
    round_two += [
        _single(site, layer, "Z")
        for site in Z_BOUNDARY_SITES
        for layer in (1, 2)
    ]

    round_three = _edge_measurements("blue", 1, "X")
    round_three += _edge_measurements("red", 2, "X")
    round_three += [
        _vertical(DOCK_SITES["blue"], "X", "Z"),
        _vertical(DOCK_SITES["red"], "Z", "X"),
        _vertical(DOCK_SITES["green"], "X", "Z"),
        _vertical(DOCK_SITES["green"], "Z", "X"),
    ]
    round_three += [
        _single(site, layer, "X")
        for site in X_BOUNDARY_SITES
        for layer in (1, 2)
    ]
    return [round_zero, round_one, round_two, round_three]


def _schedule() -> Schedule:
    base = _base_rounds()
    rounds = [base[index] for index in (0, 1, 2, 3, 0, 1, 2, 3, 0)]
    schedule = Schedule(QUBIT_COUNT, rounds)
    schedule.validate()
    return schedule


def _rowspace_signature(rows: np.ndarray) -> tuple[tuple[int, ...], ...]:
    reduced, _ = gf2.rref(rows)
    return tuple(
        tuple(int(bit) for bit in row)
        for row in reduced
        if np.any(row)
    )


def _evolve(schedule: Schedule) -> tuple[list[int], list[tuple[tuple[int, ...], ...]]]:
    tracker = ISGTracker(schedule.n)
    ranks = []
    signatures = []
    for measurements in schedule.rounds:
        for measurement in measurements:
            tracker.measure(measurement)
        ranks.append(tracker.rank())
        signatures.append(_rowspace_signature(tracker.gens))
    return ranks, signatures


def _reference_checkmatrix(schedule: Schedule) -> CheckMatrix:
    tracker = ISGTracker(schedule.n)
    for measurements in schedule.rounds[: REFERENCE_ROUND + 1]:
        for measurement in measurements:
            tracker.measure(measurement)
    checkmatrix = CheckMatrix(tracker.gens.copy())
    checkmatrix.validate()
    return checkmatrix


def _geometry() -> dict:
    coords = []
    site_of_qubit = []
    layer_of_qubit = []
    for layer, offset in ((1, (-0.06, 0.06)), (2, (0.06, -0.06))):
        for site, (x, y) in enumerate(SITE_COORDS):
            coords.append([x + offset[0], y + offset[1]])
            site_of_qubit.append(site)
            layer_of_qubit.append(layer)
    return {
        "coords": coords,
        "layout": {"kind": "finite", "origin": [-2.1, -1.3]},
        "siteOfQubit": site_of_qubit,
        "layerOfQubit": layer_of_qubit,
        "siteLabels": [
            "X-boundary representative",
            "Z-boundary red representative",
            "bulk representative 0",
            "Z-boundary green representative",
            "bulk representative 1",
            "Z-boundary blue representative",
            "bulk representative 2",
            "bulk representative 3",
            "bulk representative 4",
            "green Y-boundary dock",
            "red Y-boundary dock",
            "blue Y-boundary dock",
        ],
        "boundaries": {
            "X": list(X_BOUNDARY_SITES),
            "YDock": [DOCK_SITES[color] for color in ("red", "green", "blue")],
            "Z": list(Z_BOUNDARY_SITES),
        },
        "edgeSets": {
            color: [list(edge) for edge in edges]
            for color, edges in EDGE_SETS.items()
        },
        "scope": (
            "finite incidence layout for schedule and ISG verification; "
            "not a metric or distance certificate"
        ),
    }


def _singleton_glyph(point: list[float], letter: str) -> list[list[float]]:
    """Draw a visible, centred tick without inventing a second-qubit support."""
    offsets = {
        "X": (0.08, 0.0),
        "Y": (0.057, 0.057),
        "Z": (0.0, 0.08),
    }
    dx, dy = offsets[letter]
    return [
        [point[0] - dx, point[1] - dy],
        [point[0] + dx, point[1] + dy],
    ]


def _scene(schedule: Schedule, geometry: dict) -> dict:
    """Compile the schedule to Scene v2, including one-qubit boundary glyphs.

    Scene v2 deliberately has no point primitive.  A one-qubit measurement is
    therefore rendered as a short Pauli-oriented tick centred on that qubit;
    its operator label and item index still come directly from the schedule.
    """
    coords = geometry["coords"]
    frames = []
    for round_index, measurements in enumerate(schedule.rounds):
        objects = []
        for item, measurement in enumerate(measurements):
            word = measurement.to_str()
            support = [
                qubit for qubit, letter in enumerate(word) if letter != "_"
            ]
            letters = {word[qubit] for qubit in support}
            style = next(iter(letters)) if len(letters) == 1 else "mixed"
            if len(support) == 1:
                hit_point = list(coords[support[0]])
                points = _singleton_glyph(hit_point, style)
            else:
                points = [list(coords[qubit]) for qubit in support]
                hit_point = [
                    sum(point[axis] for point in points) / len(points)
                    for axis in (0, 1)
                ]
            objects.append({
                "id": f"round-{round_index}-measurement-{item}",
                "kind": "segment",
                "points": points,
                "style": style,
                "layer": "measurements",
                "item": item,
                "hitPoint": hit_point,
                "label": (
                    f"{style} measurement {item}; qubits "
                    f"{{{', '.join(str(qubit) for qubit in support)}}}; "
                    f"operator {word}."
                ),
            })
        frames.append({
            "id": f"round-{round_index}",
            "mode": "schedule",
            "round": round_index,
            "objects": objects,
        })
    scene = {
        "schema": "qec-atlas-scene-v2",
        "dimension": 2,
        "origin": {
            "kind": "verified",
            "method": "da-color-table8-schedule-scene-v1",
        },
        "coordinateSystem": {"kind": "cartesian", "origin": [0.0, 0.0]},
        "camera": {
            "fit": "contain",
            "padding": 0.08,
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
                "id": "measurements",
                "label": "Measurements",
                "kind": "measurements",
                "defaultVisible": True,
            },
        ],
        "nodes": [
            {
                "id": f"q{qubit}",
                "position": list(point),
                "role": "data",
                "label": f"site {geometry['siteOfQubit'][qubit]}, "
                f"layer {geometry['layerOfQubit'][qubit]}",
            }
            for qubit, point in enumerate(coords)
        ],
        "frames": frames,
    }
    validate_scene(scene)
    return scene


def build(patch: str = PATCH_ID) -> dict:
    """Build the complete padded finite schedule and its reference-round ISG."""
    _validate_patch(patch)
    schedule = _schedule()
    ranks, signatures = _evolve(schedule)
    checkmatrix = _reference_checkmatrix(schedule)
    reference_signature = _rowspace_signature(checkmatrix.stab)
    if signatures[REFERENCE_ROUND] != reference_signature:
        raise ValueError("reference CheckMatrix disagrees with round-4 ISG")
    if signatures[8] != reference_signature:
        raise ValueError("round-8 ISG does not return to the reference row space")
    geometry = _geometry()
    return {
        "checkmatrix": checkmatrix,
        "schedule": schedule,
        "geometry": geometry,
        "scene": _scene(schedule, geometry),
        "protocol": {
            "schema": "qec-atlas-da-color-pauli-triangle-v1",
            "patch": patch,
            "sourceSteps": list(range(9)),
            "baseRoundSequence": [0, 1, 2, 3, 0, 1, 2, 3, 0],
            "measurementCounts": [len(round_) for round_ in schedule.rounds],
            "isgRanks": ranks,
            "referenceRound": REFERENCE_ROUND,
            "equivalentReferenceRounds": [4, 8],
            "referenceRowspaceRank": gf2.rank(checkmatrix.stab),
            "distanceStatus": (
                "not exported: a one-round CheckMatrix distance is not the "
                "spacetime fault distance of the measurement protocol"
            ),
        },
        "logicalFrame": {
            "status": "curated-not-machine-transported",
            "automorphism": "phi_(rbg)",
            "logicalGate": "SH",
            "map": {"X_L": "Z_L", "Z_L": "Y_L", "Y_L": "X_L"},
            "ref": "davydova2024dynamic",
            "boundary": (
                "qeclib verifies round commutation, ISG ranks, and reference "
                "row-space recurrence; it does not yet transport logical "
                "representatives through outcome-dependent measurements"
            ),
        },
    }
