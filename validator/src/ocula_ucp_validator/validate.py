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
MANIFEST_REQUIRED = ("name", "version", "extends", "spec", "schema")


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
    """Validate the structural shape of a `/.well-known/ucp` manifest entry."""
    if not isinstance(manifest, dict):
        return ValidationResult(errors=[_err([], "type", "manifest must be a JSON object")])
    errors: list[ValidationError] = []
    for field_name in MANIFEST_REQUIRED:
        if field_name not in manifest:
            errors.append(_err([], "required", f"missing required field {field_name!r}"))
    version = manifest.get("version")
    if isinstance(version, str) and not VERSION_PATTERN.fullmatch(version):
        errors.append(
            _err(["version"], "pattern", f"version {version!r} does not match YYYY-MM-DD")
        )

    extends = manifest.get("extends")
    if extends is not None and not _is_non_empty_string_array(extends):
        errors.append(_err(["extends"], "type", "extends must be a non-empty array of strings"))

    schema_url = manifest.get("schema")
    if isinstance(schema_url, str) and not _is_absolute_url(schema_url):
        errors.append(_err(["schema"], "format", f"schema {schema_url!r} must be an absolute URL"))

    return ValidationResult(errors=errors)


def _err(path: list[str | int], rule: str, message: str) -> ValidationError:
    return ValidationError(
        path=path, json_pointer=to_json_pointer(path), rule=rule, message=message
    )


def _is_non_empty_string_array(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(isinstance(x, str) for x in value)


def _is_absolute_url(value: str) -> bool:
    parsed = urlparse(value)
    return bool(parsed.scheme) and bool(parsed.netloc)
