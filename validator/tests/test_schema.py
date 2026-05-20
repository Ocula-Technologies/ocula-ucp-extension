"""Capability schema loading + registry construction."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from referencing import Resource
from referencing.jsonschema import DRAFT202012

from ocula_ucp_validator.schema import (
    build_registry,
    load_capability_schema,
    local_first_retrieve,
)

APEX = "https://ocula.tech/ucp-extension/"


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


def test_local_first_retrieve_reads_apex_from_disk(tmp_path: Path) -> None:
    schemas = tmp_path / "descriptors" / "schemas"
    schemas.mkdir(parents=True)
    uri = f"{APEX}descriptors/schemas/thing.json"
    (schemas / "thing.json").write_text(json.dumps({"$id": uri}))
    resource = local_first_retrieve(tmp_path)(uri)
    assert resource.contents["$id"] == uri


def test_local_first_retrieve_delegates_non_apex_to_fallback() -> None:
    seen: list[str] = []

    def fallback(uri: str) -> Resource:
        seen.append(uri)
        return Resource.from_contents({}, default_specification=DRAFT202012)

    ucp_uri = "https://ucp.dev/2026-04-08/schemas/shopping/catalog_search.json"
    local_first_retrieve("/no/such/root", fallback=fallback)(ucp_uri)
    assert seen == [ucp_uri]


def test_local_first_retrieve_missing_apex_file_raises_with_uri(tmp_path: Path) -> None:
    uri = f"{APEX}descriptors/schemas/missing.json"
    with pytest.raises(RuntimeError, match="missing.json"):
        local_first_retrieve(tmp_path)(uri)
