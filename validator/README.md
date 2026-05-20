# `ocula-ucp-validate`

Structural conformance validator for the `tech.ocula.shopping.descriptors` UCP extension.

Validates two things:

- **Feed responses** — a `catalog.search` (or `catalog.lookup`) response, decorated with the
  `descriptors` block, against the capability schema.
- **Manifests** — a `/.well-known/ucp` document, checking the `tech.ocula.shopping.descriptors`
  capability it advertises.

Structural conformance only. Content quality (is the highlight statement useful? is the QA pair
specific enough?) is out of scope and is Ocula's commercial layer.

## Install

```sh
uv tool install ocula-ucp-validator
# or
pip install ocula-ucp-validator
```

## Usage

```sh
# Validate a feed response
ocula-ucp-validate response path/to/response.json \
    --capability path/to/descriptors.json

# Validate a manifest entry
ocula-ucp-validate manifest path/to/manifest.json

# Machine-readable output for CI
ocula-ucp-validate response response.json --capability descriptors.json --json

# Validate a working copy: resolve ocula.tech/ucp-extension/* refs from the repo, not the apex
ocula-ucp-validate response response.json --capability descriptors.json --schema-root .
```

`--variant` selects a `$defs` entry in the capability schema (defaults to
`augmented_search_response`).

By default the published schema's remote `$ref`s are fetched over the network (the live apex and
`ucp.dev`). Pass `--schema-root <dir>` to resolve `ocula.tech/ucp-extension/*` refs from a local
directory instead — useful in CI to validate a branch's own schemas before they're deployed.
`ucp.dev` refs are still fetched.

## Exit codes

| Code | Meaning |
|------|---------|
| 0 | Document is valid. |
| 1 | Validation found errors. |
| 2 | Bad input — file not found, unreadable, malformed JSON, or an unresolvable schema `$ref`. |

## Library usage

```python
from pathlib import Path
from ocula_ucp_validator import validate_response, validate_manifest

result = validate_response(response_json, Path("descriptors.json"))
if not result.is_valid:
    for err in result.errors:
        print(err.json_pointer, err.rule, err.message)
```

`validate_response` accepts an optional `retrieve` callable for resolving remote `$ref` URIs —
inject a local-fixture retriever to validate offline.

## Development

```sh
uv sync --extra dev
uv run pytest
uv run ruff check
```
