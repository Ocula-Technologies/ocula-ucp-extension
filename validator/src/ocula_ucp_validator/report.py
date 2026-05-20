"""Structured validation results."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class ValidationError:
    """A single structural validation failure."""

    path: list[str | int]
    json_pointer: str
    rule: str
    message: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "json_pointer": self.json_pointer,
            "rule": self.rule,
            "message": self.message,
        }


@dataclass(frozen=True)
class ValidationResult:
    """Outcome of validating a document."""

    errors: list[ValidationError] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "is_valid": self.is_valid,
            "errors": [e.to_dict() for e in self.errors],
        }


def to_json_pointer(path: tuple[str | int, ...] | list[str | int]) -> str:
    """Render a jsonschema absolute_path as an RFC 6901 JSON Pointer."""
    if not path:
        return ""
    return "".join("/" + _escape(str(segment)) for segment in path)


def _escape(segment: str) -> str:
    return segment.replace("~", "~0").replace("/", "~1")


def render_human(result: ValidationResult) -> str:
    """Format a ValidationResult for terminal output, grouped by JSON Pointer."""
    if result.is_valid:
        return "OK: 0 errors."
    grouped: dict[str, list[ValidationError]] = {}
    for err in result.errors:
        grouped.setdefault(err.json_pointer or "<root>", []).append(err)
    lines = [f"{len(result.errors)} error(s):"]
    for pointer, errs in grouped.items():
        lines.append(f"  {pointer}")
        for err in errs:
            lines.append(f"    - [{err.rule}] {err.message}")
    return "\n".join(lines)
