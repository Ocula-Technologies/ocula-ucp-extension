"""Resolve every $ref in the local schemas (including remote URLs).

Used by CI to catch broken references before they ship. Exits non-zero if any schema has an
unresolvable reference; exits 0 if the schemas directory is empty so the bootstrap commit
doesn't fail this check.
"""

import json
import sys
import urllib.request
from functools import lru_cache
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012


@lru_cache(maxsize=None)
def fetch_remote(uri: str) -> Resource:
    print(f"  fetching {uri}")
    with urllib.request.urlopen(uri) as response:
        return Resource.from_contents(
            json.loads(response.read()), default_specification=DRAFT202012
        )


def build_registry(local_schemas: list[dict]) -> Registry:
    # Pre-register every local schema by its `$id` so refs into our own apex URLs
    # resolve from disk. Anything else falls through to `fetch_remote` (upstream UCP).
    registry = Registry(retrieve=fetch_remote)
    for schema in local_schemas:
        sid = schema.get("$id")
        if not sid:
            continue
        registry = registry.with_resource(
            sid, Resource.from_contents(schema, default_specification=DRAFT202012)
        )
    return registry


def check_schema(schema: dict, schema_path: Path, registry: Registry) -> list[str]:
    sid = schema.get("$id", schema_path.absolute().as_uri())

    # Validate `{}` against the root and against every `$defs` entry, so refs nested
    # inside named definitions are exercised even when the empty instance wouldn't
    # otherwise walk into them.
    targets: list[tuple[str, dict]] = [("", schema)]
    for def_name in (schema.get("$defs") or {}):
        targets.append((f"#/$defs/{def_name}", {"$ref": f"{sid}#/$defs/{def_name}"}))

    failures: list[str] = []
    for pointer, target in targets:
        try:
            validator = Draft202012Validator(target, registry=registry)
            list(validator.iter_errors({}))
        except Exception as exc:  # noqa: BLE001 -- broad catch is intentional for CI reporting
            failures.append(f"{schema_path}{pointer}: {exc}")
    return failures


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "descriptors/schemas")
    schema_files = sorted(root.rglob("*.json"))
    if not schema_files:
        print(f"No JSON files under {root}; nothing to resolve.")
        return 0

    schemas = [(p, json.loads(p.read_text())) for p in schema_files]
    registry = build_registry([s for _, s in schemas])

    all_failures: list[str] = []
    for schema_path, schema in schemas:
        print(f"Schema: {schema_path}")
        all_failures.extend(check_schema(schema, schema_path, registry))

    if all_failures:
        print(f"\n{len(all_failures)} unresolved reference(s):", file=sys.stderr)
        for failure in all_failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("\nAll references resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
