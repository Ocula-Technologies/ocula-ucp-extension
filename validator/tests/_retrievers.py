"""Offline `$ref` retriever used by the test suite."""

from __future__ import annotations

import json
from pathlib import Path

from referencing import Resource
from referencing.jsonschema import DRAFT202012

UCP_URI_PREFIX = "https://ucp.dev/2026-04-08/schemas/shopping/"
UCP_SCHEMAS = Path(__file__).parent / "fixtures" / "ucp_schemas"


def offline_retrieve(uri: str) -> Resource:
    """Read vendored ucp.dev stubs from disk instead of the network."""
    if not uri.startswith(UCP_URI_PREFIX):
        raise RuntimeError(f"offline retriever has no mapping for {uri!r}")
    path = UCP_SCHEMAS / uri.removeprefix(UCP_URI_PREFIX)
    if not path.exists():
        raise RuntimeError(f"could not retrieve {uri!r}: no fixture at {path}")
    return Resource.from_contents(json.loads(path.read_text()), default_specification=DRAFT202012)
