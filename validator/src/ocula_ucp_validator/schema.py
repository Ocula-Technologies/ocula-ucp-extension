"""Capability schema loading and `$ref` registry construction."""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from collections.abc import Callable
from pathlib import Path
from typing import Any

from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

Retrieve = Callable[[str], Resource]

APEX_SCHEMA_PREFIX = "https://ocula.tech/ucp-extension/"


def _as_resource(contents: Any) -> Resource:
    return Resource.from_contents(contents, default_specification=DRAFT202012)


def load_capability_schema(path: Path | str) -> dict[str, Any]:
    """Load and parse the capability schema JSON file."""
    return json.loads(Path(path).read_text())


def build_registry(
    schema: dict[str, Any] | Path | str,
    retrieve: Retrieve | None = None,
) -> Registry:
    """Build a `referencing` Registry rooted at the capability schema.

    Eagerly resolves every absolute `$ref` URI in the schema so callers can probe the
    populated registry with `registry.contents(uri)`. `retrieve` is the callable used
    for unknown `$ref` URIs (e.g. live ucp.dev schemas). Defaults to `http_retrieve`,
    which raises with the URL on any fetch failure.
    """
    if retrieve is None:
        retrieve = http_retrieve
    if not isinstance(schema, dict):
        schema = load_capability_schema(schema)
    root = _as_resource(schema)
    registry = Registry(retrieve=retrieve).with_resource(schema["$id"], root)
    for uri in _collect_remote_refs(schema):
        registry = registry.get_or_retrieve(uri).registry
    return registry


def _collect_remote_refs(node: Any, found: set[str] | None = None) -> set[str]:
    """Walk a schema dict and collect every absolute `$ref` URI (scheme://...)."""
    if found is None:
        found = set()
    if isinstance(node, dict):
        ref = node.get("$ref")
        if isinstance(ref, str) and "://" in ref:
            found.add(ref.split("#", 1)[0])
        for value in node.values():
            _collect_remote_refs(value, found)
    elif isinstance(node, list):
        for item in node:
            _collect_remote_refs(item, found)
    return found


def http_retrieve(uri: str) -> Resource:
    """Fetch a schema over HTTP and parse it as a Draft 2020-12 Resource.

    Wraps urllib errors so the URI is always present in the surfaced message.
    """
    try:
        with urllib.request.urlopen(uri) as response:
            payload = json.loads(response.read())
    except (urllib.error.URLError, OSError) as exc:
        raise RuntimeError(f"could not retrieve {uri!r}: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"could not parse JSON from {uri!r}: {exc}") from exc
    return _as_resource(payload)


def local_first_retrieve(root: Path | str, fallback: Retrieve | None = None) -> Retrieve:
    """Resolve `ocula.tech/ucp-extension/*` `$ref`s from `root` on disk; delegate the rest.

    `root` is the directory the apex serves `/ucp-extension/*` from (the repo root), so CI can
    validate the working tree's own schemas instead of the deployed copy. `fallback` (default
    `http_retrieve`) handles non-apex URIs such as upstream `ucp.dev` schemas.
    """
    root = Path(root)

    def retrieve(uri: str) -> Resource:
        if not uri.startswith(APEX_SCHEMA_PREFIX):
            return (fallback or http_retrieve)(uri)
        path = root / uri.removeprefix(APEX_SCHEMA_PREFIX)
        if not path.is_file():
            raise RuntimeError(f"could not retrieve {uri!r}: no local file at {path}")
        return _as_resource(json.loads(path.read_text()))

    return retrieve
