"""Validate shopping_intents.json invariants.

Enforces the two load-bearing claims the taxonomy spec makes about itself:
- every dimension name and every value is `snake_case`
- no value appears in more than one dimension (so a value alone identifies its dimension)
"""

import json
import re
import sys
from pathlib import Path

SNAKE_CASE = re.compile(r"^[a-z][a-z0-9_]*$")


def main() -> int:
    path = Path(sys.argv[1] if len(sys.argv) > 1 else "taxonomy/shopping_intents.json")
    data = json.loads(path.read_text())

    failures: list[str] = []
    seen: dict[str, str] = {}

    for dim, body in data["dimensions"].items():
        if not SNAKE_CASE.fullmatch(dim):
            failures.append(f"dimension name {dim!r} is not snake_case")
        for value in body.get("values", []):
            if not SNAKE_CASE.fullmatch(value):
                failures.append(f"{dim}:{value} is not snake_case")
            if value in seen:
                failures.append(
                    f"value {value!r} appears in both {seen[value]!r} and {dim!r}"
                )
            else:
                seen[value] = dim

    if failures:
        print(f"{len(failures)} taxonomy invariant violation(s):", file=sys.stderr)
        for f in failures:
            print(f"  - {f}", file=sys.stderr)
        return 1

    print(
        f"OK: {len(seen)} values across {len(data['dimensions'])} dimensions, "
        "all snake_case and unique."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
