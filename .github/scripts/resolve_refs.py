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


def check_schema(schema_path: Path) -> list[str]:
    schema = json.loads(schema_path.read_text())
    sid = schema.get("$id", schema_path.absolute().as_uri())
    registry = Registry(retrieve=fetch_remote).with_resource(
        sid, Resource.from_contents(schema, default_specification=DRAFT202012)
    )

    failures: list[str] = []
    try:
        validator = Draft202012Validator(schema, registry=registry)
        list(validator.iter_errors({}))
    except Exception as exc:  # noqa: BLE001 -- broad catch is intentional for CI reporting
        failures.append(f"{schema_path}: {exc}")
    return failures


def main() -> int:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else "descriptors/schemas")
    schema_files = sorted(root.rglob("*.json"))
    if not schema_files:
        print(f"No JSON files under {root}; nothing to resolve.")
        return 0

    all_failures: list[str] = []
    for schema_path in schema_files:
        print(f"Schema: {schema_path}")
        all_failures.extend(check_schema(schema_path))

    if all_failures:
        print(f"\n{len(all_failures)} unresolved reference(s):", file=sys.stderr)
        for failure in all_failures:
            print(f"  - {failure}", file=sys.stderr)
        return 1

    print("\nAll references resolved.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
