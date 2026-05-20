"""Structural validation of responses and manifest entries."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

from ocula_ucp_validator.report import ValidationError, ValidationResult, to_json_pointer
from ocula_ucp_validator.schema import Retrieve, build_registry, load_capability_schema

DEFAULT_VARIANT = "augmented_search_response"
VERSION_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")
DESCRIPTORS_CAPABILITY = "tech.ocula.shopping.descriptors"
ENTRY_REQUIRED = ("version", "extends", "spec", "schema")


def validate_response(
    response: Any,
    capability_path: Path | str,
    variant: str = DEFAULT_VARIANT,
    retrieve: Retrieve | None = None,
) -> ValidationResult:
    """Validate a response against `$defs/<variant>` in the capability schema."""
    schema = load_capability_schema(capability_path)
    registry = build_registry(schema, retrieve=retrieve)
    variant_ref = {"$ref": f"{schema['$id']}#/$defs/{variant}"}
    validator = Draft202012Validator(variant_ref, registry=registry)
    errors = [
        ValidationError(
            path=list(err.absolute_path),
            json_pointer=to_json_pointer(err.absolute_path),
            rule=str(err.validator),
            message=err.message,
        )
        for err in sorted(validator.iter_errors(response), key=lambda e: list(e.absolute_path))
    ]
    return ValidationResult(errors=errors)


def validate_manifest(manifest: Any) -> ValidationResult:
    """Validate the descriptors capability in a `/.well-known/ucp` manifest."""
    if not isinstance(manifest, dict):
        return _fail([], "type", "manifest must be a JSON object")

    ucp = manifest.get("ucp")
    capabilities = ucp.get("capabilities") if isinstance(ucp, dict) else None
    if not isinstance(capabilities, dict):
        return _fail(["ucp", "capabilities"], "required", "manifest has no 'ucp.capabilities'")

    base = ["ucp", "capabilities", DESCRIPTORS_CAPABILITY]
    entries = capabilities.get(DESCRIPTORS_CAPABILITY)
    if entries is None:
        return _fail(base, "required", f"manifest does not advertise {DESCRIPTORS_CAPABILITY!r}")
    if not _is_non_empty_array(entries):
        return _fail(base, "type", f"{DESCRIPTORS_CAPABILITY!r} must be a non-empty array")

    errors: list[ValidationError] = []
    for index, entry in enumerate(entries):
        errors.extend(_validate_entry(entry, [*base, index]))
    return ValidationResult(errors=errors)


def _validate_entry(entry: Any, path: list[str | int]) -> list[ValidationError]:
    """Check a single capability entry's required fields and field shapes."""
    if not isinstance(entry, dict):
        return [_err(path, "type", "capability entry must be a JSON object")]

    errors = [
        _err(path, "required", f"missing required field {field_name!r}")
        for field_name in ENTRY_REQUIRED
        if field_name not in entry
    ]

    version = entry.get("version")
    if isinstance(version, str) and not VERSION_PATTERN.fullmatch(version):
        errors.append(
            _err([*path, "version"], "pattern", f"version {version!r} does not match YYYY-MM-DD")
        )

    extends = entry.get("extends")
    if extends is not None and not _is_non_empty_string_array(extends):
        errors.append(
            _err([*path, "extends"], "type", "extends must be a non-empty array of strings")
        )

    schema_url = entry.get("schema")
    if isinstance(schema_url, str) and not _is_absolute_url(schema_url):
        errors.append(
            _err([*path, "schema"], "format", f"schema {schema_url!r} must be an absolute URL")
        )

    return errors


def _err(path: list[str | int], rule: str, message: str) -> ValidationError:
    return ValidationError(
        path=path, json_pointer=to_json_pointer(path), rule=rule, message=message
    )


def _fail(path: list[str | int], rule: str, message: str) -> ValidationResult:
    return ValidationResult(errors=[_err(path, rule, message)])


def _is_non_empty_array(value: Any) -> bool:
    return isinstance(value, list) and bool(value)


def _is_non_empty_string_array(value: Any) -> bool:
    return _is_non_empty_array(value) and all(isinstance(x, str) for x in value)


def _is_absolute_url(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme) and bool(parsed.netloc)
