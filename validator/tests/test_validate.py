"""Structural validation of responses and manifests."""

from __future__ import annotations

import json
from pathlib import Path

from ocula_ucp_validator.validate import (
    DESCRIPTORS_CAPABILITY,
    validate_manifest,
    validate_response,
)


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


def _manifest_with(**entry_overrides: object) -> dict:
    """A valid `/.well-known/ucp` manifest with the descriptors entry field-patched."""
    entry = {
        "version": "2026-05-18",
        "extends": ["dev.ucp.shopping.catalog.search"],
        "spec": "https://ocula.tech/ucp-extension/descriptors/",
        "schema": "https://ocula.tech/ucp-extension/descriptors/schemas/2026-05-18/descriptors.json",
    }
    entry.update(entry_overrides)
    return {"ucp": {"capabilities": {DESCRIPTORS_CAPABILITY: [entry]}}}


def test_valid_response_passes(fixtures_dir: Path, capability_path: Path, offline) -> None:
    response = _load(fixtures_dir / "valid_search_response.json")
    result = validate_response(response, capability_path, retrieve=offline)
    assert result.is_valid is True
    assert result.errors == []


def test_invalid_descriptors_block_surfaces_error_at_expected_pointer(
    fixtures_dir: Path, capability_path: Path, offline
) -> None:
    response = _load(fixtures_dir / "invalid_descriptors_wrong_type.json")
    result = validate_response(response, capability_path, retrieve=offline)
    assert result.is_valid is False
    descriptor_errors = [e for e in result.errors if "descriptors" in e.path]
    assert descriptor_errors, [e.message for e in result.errors]
    err = descriptor_errors[0]
    assert err.path == ["products", 0, "descriptors", "highlights"]
    assert err.json_pointer == "/products/0/descriptors/highlights"
    assert err.rule == "type"
    assert "array" in err.message


def test_valid_manifest_passes(fixtures_dir: Path) -> None:
    result = validate_manifest(_load(fixtures_dir / "manifest_valid.json"))
    assert result.is_valid is True
    assert result.errors == []


def test_manifest_without_descriptors_capability_fails(fixtures_dir: Path) -> None:
    result = validate_manifest(_load(fixtures_dir / "manifest_missing_capability.json"))
    assert result.is_valid is False
    assert any(e.rule == "required" and DESCRIPTORS_CAPABILITY in e.message for e in result.errors)


def test_manifest_bad_version_fails(fixtures_dir: Path) -> None:
    result = validate_manifest(_load(fixtures_dir / "manifest_bad_version.json"))
    assert result.is_valid is False
    assert any(
        e.path == ["ucp", "capabilities", DESCRIPTORS_CAPABILITY, 0, "version"]
        and e.rule == "pattern"
        for e in result.errors
    )


def test_manifest_rejects_empty_extends() -> None:
    result = validate_manifest(_manifest_with(extends=[]))
    assert any(e.path[-1] == "extends" for e in result.errors)


def test_manifest_rejects_relative_schema_url() -> None:
    result = validate_manifest(_manifest_with(schema="/relative"))
    assert any(e.path[-1] == "schema" and e.rule == "format" for e in result.errors)
