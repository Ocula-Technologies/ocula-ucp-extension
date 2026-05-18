"""Capability schema loading + registry construction."""

from __future__ import annotations

from pathlib import Path

import pytest

from ocula_ucp_validator.schema import build_registry, load_capability_schema


def test_load_capability_schema_returns_descriptors_dict(capability_path: Path) -> None:
    schema = load_capability_schema(capability_path)
    assert schema["name"] == "tech.ocula.shopping.descriptors"
    assert "augmented_search_response" in schema["$defs"]


def test_load_capability_schema_missing_file_raises_with_path(tmp_path: Path) -> None:
    missing = tmp_path / "nope.json"
    with pytest.raises(FileNotFoundError, match=str(missing)):
        load_capability_schema(missing)


def test_build_registry_resolves_remote_ucp_refs(capability_path: Path, offline) -> None:
    registry = build_registry(capability_path, retrieve=offline)
    resolved = registry.contents("https://ucp.dev/2026-04-08/schemas/shopping/catalog_search.json")
    assert resolved["name"] == "dev.ucp.shopping.catalog.search"


def test_build_registry_unreachable_remote_raises_with_uri(capability_path: Path) -> None:
    def broken(uri: str):
        raise RuntimeError(f"could not retrieve {uri!r}: simulated outage")

    with pytest.raises(Exception, match="ucp.dev"):
        build_registry(capability_path, retrieve=broken)
