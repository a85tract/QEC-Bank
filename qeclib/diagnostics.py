"""Versioned diagnostics shared by QEC-Bank command-line interfaces."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
import json
from pathlib import Path
import re
import sys
from typing import Any, TextIO


DIAGNOSTIC_SCHEMA = "qec-atlas-diagnostic-v1"
REPORT_SCHEMA = "qec-atlas-diagnostics-v1"
OUTPUT_FORMATS = frozenset({"json", "text"})
SEVERITIES = frozenset({"error", "warning", "info"})


class DiagnosticUsageError(ValueError):
    """A CLI diagnostic-output option is malformed."""


def make_diagnostic(
    code: str,
    message: str,
    *,
    severity: str = "error",
    path: str | Path | None = None,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build one JSON-serializable, versioned diagnostic.

    ``code`` is the stable machine contract. ``message`` stays concise and is
    also suitable for the default human-readable CLI output.
    """
    if not re.fullmatch(r"[a-z][a-z0-9]*(?:\.[a-z][a-z0-9_-]*)+", code):
        raise ValueError(f"invalid diagnostic code: {code!r}")
    if severity not in SEVERITIES:
        raise ValueError(f"invalid diagnostic severity: {severity!r}")
    if not isinstance(message, str) or not message:
        raise ValueError("diagnostic message must be a nonempty string")
    return {
        "schema": DIAGNOSTIC_SCHEMA,
        "severity": severity,
        "code": code,
        "message": message,
        "path": str(path) if path is not None else None,
        "context": dict(context or {}),
    }


def make_report(
    tool: str,
    status: str,
    summary: str,
    diagnostics: Sequence[Mapping[str, Any]] = (),
    *,
    data: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    """Build the stable envelope emitted by every participating CLI."""
    if status not in {"ok", "error"}:
        raise ValueError(f"invalid diagnostic report status: {status!r}")
    if not isinstance(tool, str) or not tool:
        raise ValueError("diagnostic report tool must be a nonempty string")
    if not isinstance(summary, str) or not summary:
        raise ValueError("diagnostic report summary must be a nonempty string")
    items = [dict(item) for item in diagnostics]
    has_errors = any(item.get("severity") == "error" for item in items)
    if (status == "error") != has_errors:
        raise ValueError("diagnostic report status must agree with its diagnostics")
    return {
        "schema": REPORT_SCHEMA,
        "tool": tool,
        "status": status,
        "summary": summary,
        "diagnostics": items,
        "data": dict(data or {}),
    }


def emit_report(
    report: Mapping[str, Any],
    *,
    output_format: str,
    human_lines: Sequence[str] = (),
    text_stream: TextIO | None = None,
) -> None:
    """Emit exactly one JSON report or the caller's concise text lines."""
    if output_format == "json":
        print(json.dumps(report, sort_keys=True))
        return
    if output_format != "text":
        raise ValueError(f"unsupported diagnostic output format: {output_format!r}")
    stream = text_stream or sys.stdout
    for line in human_lines:
        print(line, file=stream)


def parse_output_format(argv: Sequence[str]) -> tuple[list[str], str]:
    """Remove one optional ``--format text|json`` from arbitrary CLI args."""
    remaining: list[str] = []
    output_format = "text"
    seen = False
    index = 0
    while index < len(argv):
        argument = argv[index]
        if argument == "--format":
            if seen:
                raise DiagnosticUsageError("--format may be provided only once")
            if index + 1 >= len(argv):
                raise DiagnosticUsageError("--format requires text or json")
            output_format = argv[index + 1]
            seen = True
            index += 2
            continue
        if argument.startswith("--format="):
            if seen:
                raise DiagnosticUsageError("--format may be provided only once")
            output_format = argument.split("=", 1)[1]
            seen = True
            index += 1
            continue
        remaining.append(argument)
        index += 1
    if output_format not in OUTPUT_FORMATS:
        raise DiagnosticUsageError(
            f"unsupported --format {output_format!r}; choose text or json"
        )
    return remaining, output_format
