"""Machine-validated, constructor-derived scenes for generic QEC-Bank viewers."""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path

from jsonschema import Draft202012Validator


_SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schemas" / "scene.schema.json"
_VALIDATOR = Draft202012Validator(json.loads(_SCHEMA_PATH.read_text()))


def _point(value) -> list[float]:
    return [float(value[0]), float(value[1])]


def _centroid(points: list[list[float]]) -> list[float]:
    return [
        sum(point[0] for point in points) / len(points),
        sum(point[1] for point in points) / len(points),
    ]


def _ordered(points: list[list[float]], center: list[float]) -> list[list[float]]:
    return sorted(
        points,
        key=lambda point: math.atan2(point[1] - center[1], point[0] - center[0]),
    )


def _basis(layout: dict | None) -> list[list[float]] | None:
    candidate = layout.get("basis") if isinstance(layout, dict) else None
    if (
        not isinstance(candidate, list)
        or len(candidate) != 2
        or any(not isinstance(vector, (list, tuple)) or len(vector) != 2 for vector in candidate)
    ):
        return None
    vectors = [_point(vector) for vector in candidate]
    determinant = (
        vectors[0][0] * vectors[1][1]
        - vectors[0][1] * vectors[1][0]
    )
    if abs(determinant) < 1e-12:
        raise ValueError("scene periodic basis must be non-singular")
    return vectors


def _fractional_coordinates(
    point: list[float],
    origin: list[float],
    basis: list[list[float]],
) -> list[float]:
    """Coordinates of ``point - origin`` in a two-vector periodic basis."""
    first, second = basis
    determinant = (
        first[0] * second[1]
        - first[1] * second[0]
    )
    delta = [point[0] - origin[0], point[1] - origin[1]]
    return [
        (delta[0] * second[1] - delta[1] * second[0]) / determinant,
        (-delta[0] * first[1] + delta[1] * first[0]) / determinant,
    ]


def _periodic_representative(
    point: list[float],
    layout: dict | None,
) -> list[float]:
    """Move a point into the layout's half-open fundamental domain."""
    point = _point(point)
    basis = _basis(layout)
    if basis is None:
        return point
    origin = _point(layout.get("origin", [0, 0]))
    fractional = _fractional_coordinates(point, origin, basis)
    wrapped = []
    for value in fractional:
        representative = value % 1.0
        if math.isclose(representative, 0.0, abs_tol=1e-12) or math.isclose(
            representative,
            1.0,
            abs_tol=1e-12,
        ):
            representative = 0.0
        wrapped.append(representative)
    return [
        origin[axis]
        + wrapped[0] * basis[0][axis]
        + wrapped[1] * basis[1][axis]
        for axis in (0, 1)
    ]


def _minimal_image(
    point: list[float],
    anchor: list[float],
    basis: list[list[float]] | None,
) -> list[float]:
    if basis is None:
        return list(point)
    a, b = basis
    determinant = a[0] * b[1] - a[1] * b[0]
    delta = [point[0] - anchor[0], point[1] - anchor[1]]
    fractional = [
        (delta[0] * b[1] - delta[1] * b[0]) / determinant,
        (-delta[0] * a[1] + delta[1] * a[0]) / determinant,
    ]
    center_shift = [round(fractional[0]), round(fractional[1])]
    candidates = []
    for first in range(center_shift[0] - 1, center_shift[0] + 2):
        for second in range(center_shift[1] - 1, center_shift[1] + 2):
            adjusted = [
                point[0] - first * a[0] - second * b[0],
                point[1] - first * a[1] - second * b[1],
            ]
            distance = (
                (adjusted[0] - anchor[0]) ** 2
                + (adjusted[1] - anchor[1]) ** 2
            )
            candidates.append((distance, adjusted))
    return min(candidates, key=lambda candidate: candidate[0])[1]


def _coordinate_system(layout: dict | None) -> dict:
    basis = _basis(layout)
    coordinate_system = {
        "kind": "periodic" if basis is not None else "cartesian",
        "origin": _point(layout.get("origin", [0, 0]))
        if isinstance(layout, dict)
        else [0.0, 0.0],
    }
    if basis is not None:
        coordinate_system["basis"] = basis
    return coordinate_system


def _layout_from(lattice: dict | None, schedule: dict | None) -> dict:
    if isinstance(lattice, dict) and isinstance(lattice.get("layout"), dict):
        return lattice["layout"]
    if isinstance(schedule, dict) and isinstance(schedule.get("layout"), dict):
        return schedule["layout"]
    return {}


def _coords_from(
    lattice: dict | None,
    schedule: dict | None,
    layout: dict,
) -> list[list[float]]:
    if isinstance(lattice, dict) and isinstance(lattice.get("coords"), list):
        coords = lattice["coords"]
    elif isinstance(schedule, dict) and isinstance(schedule.get("coords"), list):
        coords = schedule["coords"]
    else:
        return []
    return [_periodic_representative(point, layout) for point in coords]


def _lattice_frame(
    lattice: dict,
    coords: list[list[float]],
    layout: dict,
) -> dict | None:
    checks = lattice.get("checks", [])
    if not checks:
        return None
    basis = _basis(layout)
    anchors = layout.get("checkAnchors", [])
    styles = layout.get("checkStyles", {})
    objects = []
    for item, check in enumerate(checks):
        support = check["support"]
        raw_points = [coords[qubit] for qubit in support]
        anchor = (
            _point(anchors[item])
            if item < len(anchors)
            else _centroid(raw_points)
        )
        anchor = _periodic_representative(anchor, layout)
        points = [
            _minimal_image(point, anchor, basis)
            for point in raw_points
        ]
        kind = styles.get(check["type"], "face")
        if len(points) == 2:
            kind = "segment"
        elif kind == "spokes":
            points = [anchor, *points]
        else:
            points = _ordered(points, anchor)
        objects.append({
            "id": f"check-{item}",
            "kind": kind,
            "points": points,
            "style": check["type"],
            "layer": "checks",
            "item": item,
            "hitPoint": anchor,
            "label": (
                f"{check['type']}-check {item}; support "
                f"{{{', '.join(str(qubit) for qubit in support)}}}."
            ),
        })
    return {"id": "lattice", "mode": "lattice", "objects": objects}


def _logical_frames(
    lattice: dict,
    coords: list[list[float]],
) -> list[dict]:
    logicals = lattice.get("logicalOperators", [])
    if not logicals:
        return []
    objects = []
    for item, logical in enumerate(logicals):
        logical_type = logical.get("type")
        label = logical.get("label")
        support = logical.get("support")
        path = logical.get("path")
        if logical_type not in {"X", "Z"}:
            raise ValueError(
                f"logical operator {item} must have type X or Z"
            )
        if not isinstance(label, str) or not label.strip():
            raise ValueError(
                f"logical operator {item} needs a non-empty label"
            )
        if (
            not isinstance(support, list)
            or not support
            or len(support) != len(set(support))
            or any(
                not isinstance(qubit, int)
                or qubit < 0
                or qubit >= len(coords)
                for qubit in support
            )
        ):
            raise ValueError(
                f"logical operator {item} has an invalid qubit support"
            )
        if (
            not isinstance(path, list)
            or len(path) < 2
            or any(
                not isinstance(point, (list, tuple))
                or len(point) != 2
                for point in path
            )
        ):
            raise ValueError(
                f"logical operator {item} needs a two-dimensional path"
            )
        points = [_point(point) for point in path]
        objects.append({
            "id": f"logical-{item}",
            "kind": "polyline",
            "points": points,
            "style": logical_type,
            "layer": "logical-operators",
            "item": item,
            "hitPoint": _centroid(points),
            "label": (
                f"{label}; {logical_type}-type logical; weight {len(support)}; "
                f"support {{{', '.join(str(qubit) for qubit in support)}}}."
            ),
        })
    return [
        {"id": "data", "mode": "data", "objects": []},
        {"id": "logical", "mode": "logical", "objects": objects},
    ]


def _schedule_frames(
    schedule: dict,
    coords: list[list[float]],
    layout: dict,
) -> list[dict]:
    basis = _basis(layout)
    frames = []
    for round_data in schedule.get("rounds", []):
        objects = []
        for item, measurement in enumerate(round_data.get("measurements", [])):
            raw_points = [coords[qubit] for qubit in measurement["support"]]
            if not raw_points:
                continue
            anchor = raw_points[0]
            points = [
                _minimal_image(point, anchor, basis)
                for point in raw_points
            ]
            center = _centroid(points)
            kind = (
                "segment"
                if len(points) == 2
                else "polyline"
            )
            objects.append({
                "id": f"round-{round_data['index']}-measurement-{item}",
                "kind": kind,
                "points": points,
                "style": measurement["type"]
                if measurement["type"] in {"X", "Y", "Z", "mixed"}
                else "neutral",
                "layer": "measurements",
                "item": item,
                "hitPoint": center,
                "label": (
                    f"{measurement['type']} measurement {item}; qubits "
                    f"{{{', '.join(str(qubit) for qubit in measurement['support'])}}}; "
                    f"operator {measurement.get('pauli', 'not exported')}."
                ),
            })
        frames.append({
            "id": f"round-{round_data['index']}",
            "mode": "schedule",
            "round": round_data["index"],
            "objects": objects,
        })
    return frames


def _scene_layers(frames: list[dict]) -> list[dict]:
    kinds = {
        "checks": ("Stabilizer checks", "checks"),
        "incidence": ("Stabilizer incidence", "checks"),
        "construction": ("Construction structure", "annotations"),
        "logical-operators": ("Logical operators", "logicals"),
        "measurements": ("Measurements", "measurements"),
    }
    layer_ids = {
        item["layer"]
        for frame in frames
        for item in frame["objects"]
    }
    layers = [{
        "id": "data",
        "label": "Data qubits",
        "kind": "data",
        "defaultVisible": True,
    }]
    for layer_id in sorted(layer_ids):
        label, kind = kinds.get(
            layer_id,
            (layer_id.replace("-", " ").title(), "annotations"),
        )
        layers.append({
            "id": layer_id,
            "label": label,
            "kind": kind,
            "defaultVisible": True,
        })
    return layers


def _cross(first: list[float], second: list[float]) -> list[float]:
    return [
        first[1] * second[2] - first[2] * second[1],
        first[2] * second[0] - first[0] * second[2],
        first[0] * second[1] - first[1] * second[0],
    ]


def _norm(vector: list[float]) -> float:
    return math.sqrt(sum(value * value for value in vector))


def _validate_common(scene: dict) -> tuple[set[str], set[str]]:
    layer_ids = [layer["id"] for layer in scene["layers"]]
    if len(layer_ids) != len(set(layer_ids)):
        raise ValueError("invalid scene v2: layer ids must be unique")
    node_ids = [node["id"] for node in scene["nodes"]]
    if len(node_ids) != len(set(node_ids)):
        raise ValueError("invalid scene v2: node ids must be unique")
    frame_ids = [frame["id"] for frame in scene["frames"]]
    if len(frame_ids) != len(set(frame_ids)):
        raise ValueError("invalid scene v2: frame ids must be unique")
    frame_keys = [(frame["mode"], frame.get("round")) for frame in scene["frames"]]
    if len(frame_keys) != len(set(frame_keys)):
        raise ValueError("invalid scene v2: frame mode/round keys must be unique")
    return set(layer_ids), set(node_ids)


def _validate_scene_2d(scene: dict, layer_ids: set[str]) -> list[float]:
    if scene["camera"]["maxZoom"] <= scene["camera"]["minZoom"]:
        raise ValueError("invalid scene v2: camera.maxZoom must exceed camera.minZoom")
    system = scene["coordinateSystem"]
    numbers = [
        *system["origin"],
        scene["camera"]["padding"],
        scene["camera"]["minZoom"],
        scene["camera"]["maxZoom"],
    ]
    for vector in system.get("basis", []):
        numbers.extend(vector)
    for node in scene["nodes"]:
        numbers.extend(node["position"])
    for frame in scene["frames"]:
        object_ids = [item["id"] for item in frame["objects"]]
        item_ids = [item["item"] for item in frame["objects"]]
        if len(object_ids) != len(set(object_ids)):
            raise ValueError(
                f"invalid scene v2: object ids in frame {frame['id']} must be unique"
            )
        if len(item_ids) != len(set(item_ids)):
            raise ValueError(
                f"invalid scene v2: item ids in frame {frame['id']} must be unique"
            )
        for item in frame["objects"]:
            if item["layer"] not in layer_ids:
                raise ValueError(
                    f"invalid scene v2: object {item['id']} references "
                    f"unknown layer {item['layer']}"
                )
            numbers.extend(item["hitPoint"])
            for point in item["points"]:
                numbers.extend(point)
    return numbers


def _validate_cell(primitive: dict, node_ids: set[str]) -> None:
    vertices = set(primitive["vertices"])
    if not vertices <= node_ids:
        missing = sorted(vertices - node_ids)
        raise ValueError(
            f"invalid scene v2: primitive {primitive['id']} references "
            f"unknown vertices {missing}"
        )
    if primitive["kind"] != "cell":
        return
    edge_counts = Counter()
    for face in primitive["faces"]:
        if not set(face) <= vertices:
            raise ValueError(
                f"invalid scene v2: cell {primitive['id']} face references "
                "a vertex outside the cell"
            )
        for index, first in enumerate(face):
            second = face[(index + 1) % len(face)]
            edge_counts[tuple(sorted((first, second)))] += 1
    if not edge_counts or any(count != 2 for count in edge_counts.values()):
        raise ValueError(
            f"invalid scene v2: cell {primitive['id']} must be a closed "
            "two-manifold (every face edge appears twice)"
        )


def _validate_scene_3d(
    scene: dict,
    layer_ids: set[str],
    node_ids: set[str],
) -> list[float]:
    camera = scene["camera"]
    if camera["far"] <= camera["near"]:
        raise ValueError("invalid scene v2: camera.far must exceed camera.near")
    if camera["maxDistance"] <= camera["minDistance"]:
        raise ValueError(
            "invalid scene v2: camera.maxDistance must exceed camera.minDistance"
        )
    view = [
        camera["target"][axis] - camera["position"][axis]
        for axis in range(3)
    ]
    if _norm(view) < 1e-12:
        raise ValueError("invalid scene v2: camera position must differ from target")
    if _norm(camera["up"]) < 1e-12 or _norm(_cross(view, camera["up"])) < 1e-12:
        raise ValueError(
            "invalid scene v2: camera up vector must be nonzero and not "
            "parallel to the viewing direction"
        )

    for node in scene["nodes"]:
        if node["layer"] not in layer_ids:
            raise ValueError(
                f"invalid scene v2: node {node['id']} references "
                f"unknown layer {node['layer']}"
            )
    primitive_ids = [primitive["id"] for primitive in scene["primitives"]]
    if len(primitive_ids) != len(set(primitive_ids)):
        raise ValueError("invalid scene v2: primitive ids must be unique")
    primitives = {
        primitive["id"]: primitive
        for primitive in scene["primitives"]
    }
    for primitive in scene["primitives"]:
        if primitive["layer"] not in layer_ids:
            raise ValueError(
                f"invalid scene v2: primitive {primitive['id']} references "
                f"unknown layer {primitive['layer']}"
            )
        _validate_cell(primitive, node_ids)
    for frame in scene["frames"]:
        unknown = set(frame["primitives"]) - set(primitives)
        if unknown:
            raise ValueError(
                f"invalid scene v2: frame {frame['id']} references "
                f"unknown primitives {sorted(unknown)}"
            )
        items = [
            primitives[primitive_id]["item"]
            for primitive_id in frame["primitives"]
        ]
        if len(items) != len(set(items)):
            raise ValueError(
                f"invalid scene v2: item ids in frame {frame['id']} must be unique"
            )

    system = scene["coordinateSystem"]
    if system["kind"] == "periodic":
        first, second, third = system["basis"]
        determinant = sum(
            first[axis] * _cross(second, third)[axis]
            for axis in range(3)
        )
        if abs(determinant) < 1e-12:
            raise ValueError("invalid scene v2: 3D periodic basis must be non-singular")

    numbers = [
        *system["origin"],
        *camera["position"],
        *camera["target"],
        *camera["up"],
        camera["near"],
        camera["far"],
        camera["minDistance"],
        camera["maxDistance"],
    ]
    if "fov" in camera:
        numbers.append(camera["fov"])
    for vector in system.get("basis", []):
        numbers.extend(vector)
    for node in scene["nodes"]:
        numbers.extend(node["position"])
    return numbers


def validate_scene(scene: dict) -> None:
    """Raise ``ValueError`` for schema or semantic scene-contract violations."""
    errors = sorted(_VALIDATOR.iter_errors(scene), key=lambda error: list(error.path))
    if errors:
        details = "; ".join(
            f"{'.'.join(str(part) for part in error.absolute_path) or 'scene'}: "
            f"{error.message}"
            for error in errors
        )
        raise ValueError(f"invalid scene v2: {details}")
    layer_ids, node_ids = _validate_common(scene)
    numbers = (
        _validate_scene_2d(scene, layer_ids)
        if scene["dimension"] == 2
        else _validate_scene_3d(scene, layer_ids, node_ids)
    )
    if any(not math.isfinite(number) for number in numbers):
        raise ValueError("invalid scene v2: coordinates must be finite")


def checkmatrix_scene(
    checkmatrix,
    *,
    coords: list[list[float]] | None = None,
    check_positions: list[list[float]] | None = None,
    node_labels: list[str] | None = None,
    mode: str = "incidence",
    origin_method: str = "checkmatrix-incidence-scene-v1",
) -> dict:
    """Derive a topology-only qubit–stabilizer incidence Scene v2.

    A circular fallback is deliberately labeled as incidence, never lattice:
    it preserves exact operator support without claiming a physical embedding.
    Constructions may supply verified block coordinates and select the
    ``construction`` mode while retaining the same generic scene grammar.
    """
    if mode not in {"incidence", "construction"}:
        raise ValueError("checkmatrix scene mode must be incidence or construction")
    n = checkmatrix.n
    if coords is None:
        coords = [
            [
                round(math.cos(math.tau * qubit / max(n, 1) - math.pi / 2), 12),
                round(math.sin(math.tau * qubit / max(n, 1) - math.pi / 2), 12),
            ]
            for qubit in range(n)
        ]
    coords = [_point(point) for point in coords]
    if len(coords) != n:
        raise ValueError(
            f"checkmatrix scene needs one coordinate per qubit ({len(coords)} != {n})"
        )
    row_count = len(checkmatrix.stab)
    if check_positions is None:
        center = _centroid(coords) if coords else [0.0, 0.0]
        extent = max(
            [
                math.hypot(point[0] - center[0], point[1] - center[1])
                for point in coords
            ]
            or [1.0]
        )
        radius = max(extent * 0.38, 0.25)
        check_positions = [
            [
                center[0] + radius * math.cos(
                    math.tau * row / max(row_count, 1) - math.pi / 2
                ),
                center[1] + radius * math.sin(
                    math.tau * row / max(row_count, 1) - math.pi / 2
                ),
            ]
            for row in range(row_count)
        ]
    check_positions = [_point(point) for point in check_positions]
    if len(check_positions) != row_count:
        raise ValueError(
            "checkmatrix scene needs one check position per stabilizer row "
            f"({len(check_positions)} != {row_count})"
        )
    if node_labels is None:
        node_labels = [str(qubit) for qubit in range(n)]
    if len(node_labels) != n:
        raise ValueError("checkmatrix scene needs one label per qubit")

    objects = []
    for item, row in enumerate(checkmatrix.stab):
        x_part = row[:n]
        z_part = row[n:]
        support = [
            qubit
            for qubit in range(n)
            if bool(x_part[qubit]) or bool(z_part[qubit])
        ]
        letters = [
            (
                "Y" if bool(x_part[qubit]) and bool(z_part[qubit])
                else "X" if bool(x_part[qubit])
                else "Z" if bool(z_part[qubit])
                else "_"
            )
            for qubit in range(n)
        ]
        styles = {letters[qubit] for qubit in support}
        style = next(iter(styles)) if len(styles) == 1 else "mixed"
        anchor = check_positions[item]
        points = [anchor, *(coords[qubit] for qubit in support)]
        kind = "spokes" if len(support) >= 2 else "segment"
        if len(points) < 2:
            raise ValueError(f"stabilizer row {item} has empty support")
        objects.append({
            "id": f"stabilizer-{item}",
            "kind": kind,
            "points": points,
            "style": style,
            "layer": mode,
            "item": item,
            "hitPoint": anchor,
            "label": (
                f"Stabilizer {item}: {''.join(letters)}; support "
                f"{{{', '.join(str(qubit) for qubit in support)}}}."
            ),
        })
    layer_label = (
        "Construction relations" if mode == "construction"
        else "Stabilizer incidence"
    )
    layer_kind = "annotations" if mode == "construction" else "checks"
    scene = {
        "schema": "qec-atlas-scene-v2",
        "dimension": 2,
        "origin": {"kind": "verified", "method": origin_method},
        "coordinateSystem": {"kind": "cartesian", "origin": [0.0, 0.0]},
        "camera": {
            "fit": "contain",
            "padding": 0.1,
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
                "id": mode,
                "label": layer_label,
                "kind": layer_kind,
                "defaultVisible": True,
            },
        ],
        "nodes": [
            {
                "id": f"q{qubit}",
                "position": point,
                "role": "data",
                "label": node_labels[qubit],
            }
            for qubit, point in enumerate(coords)
        ],
        "frames": [{"id": mode, "mode": mode, "objects": objects}],
    }
    validate_scene(scene)
    return scene


def scene_data(lattice: dict | None = None, schedule: dict | None = None) -> dict | None:
    """Compile lattice/schedule exports into one generic Scene v2 payload."""
    layout = _layout_from(lattice, schedule)
    coords = _coords_from(lattice, schedule, layout)
    if not coords:
        return None
    frames = []
    if isinstance(lattice, dict):
        lattice_frame = _lattice_frame(lattice, coords, layout)
        if lattice_frame is not None:
            frames.append(lattice_frame)
        frames.extend(_logical_frames(lattice, coords))
    if isinstance(schedule, dict):
        frames.extend(_schedule_frames(schedule, coords, layout))
    if not frames:
        return None
    scene = {
        "schema": "qec-atlas-scene-v2",
        "dimension": 2,
        "origin": {
            "kind": "verified",
            "method": "constructor-derived-scene-v2",
        },
        "coordinateSystem": _coordinate_system(layout),
        "camera": {
            "fit": "contain",
            "padding": 0.08,
            "minZoom": 0.5,
            "maxZoom": 8.0,
        },
        "layers": _scene_layers(frames),
        "nodes": [
            {
                "id": f"q{qubit}",
                "position": point,
                "role": "data",
                "label": str(qubit),
            }
            for qubit, point in enumerate(coords)
        ],
        "frames": frames,
    }
    validate_scene(scene)
    return scene
