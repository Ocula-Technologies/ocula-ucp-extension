"""Structural validation of responses and manifests."""

from __future__ import annotations

import json
from pathlib import Path

from ocula_ucp_validator.validate import validate_manifest, validate_response


def _load(path: Path) -> dict:
    return json.loads(path.read_text())


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


def test_manifest_missing_name_fails(fixtures_dir: Path) -> None:
    result = validate_manifest(_load(fixtures_dir / "manifest_missing_name.json"))
    assert result.is_valid is False
    assert any(e.rule == "required" and "'name'" in e.message for e in result.errors)


def test_manifest_bad_version_fails(fixtures_dir: Path) -> None:
    result = validate_manifest(_load(fixtures_dir / "manifest_bad_version.json"))
    assert result.is_valid is False
    assert any(e.path == ["version"] and e.rule == "pattern" for e in result.errors)


def test_manifest_rejects_empty_extends() -> None:
    result = validate_manifest({
        "name": "x",
        "version": "2026-05-18",
        "extends": [],
        "spec": "https://x",
        "schema": "https://x",
    })
    assert any(e.path == ["extends"] for e in result.errors)


def test_manifest_rejects_relative_schema_url() -> None:
    result = validate_manifest({
        "name": "x",
        "version": "2026-05-18",
        "extends": ["a"],
        "spec": "https://x",
        "schema": "/relative",
    })
    assert any(e.path == ["schema"] and e.rule == "format" for e in result.errors)
