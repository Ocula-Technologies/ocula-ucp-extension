# ocula-ucp-extension

Ocula's open vendor extensions to the [Universal Commerce Protocol (UCP)](https://ucp.dev).
v0.1 scope: `tech.ocula.shopping.descriptors` — the descriptive layer for agentic commerce.

> **Status:** `v0.1-draft — pre-release.` RFC not yet submitted to the UCP working group.
> Schemas, taxonomy, and validator are under active development; shapes may change before the
> v0.1 launch.

## What this is

A vendor extension to UCP's `catalog` capability that adds a structured **descriptive layer** to
product responses: highlights, Q&A pairs, use cases, intent tags, and competitive differentiators.
These are the descriptive structures AI agents need to evaluate contextual fit and describe
products to buyers.

Published under the reverse-domain namespace `tech.ocula.shopping.descriptors`, composing against
`dev.ucp.shopping.catalog.search` and `dev.ucp.shopping.catalog.lookup` via `allOf` + `$ref` per
the UCP [Schema Authoring Guide](https://ucp.dev/documentation/schema-authoring/).

## What this is not

- **Not a competing standard.** It's a UCP-conformant vendor extension, designed for promotion
  into the `dev.ucp.*` namespace if it gains adoption.
- **Not a content-quality methodology.** The validator checks structural conformance only —
  whether fields are present, well-formed, and use documented vocabulary terms. Content quality
  assessment (whether a highlight is well-written, whether a use case is coherent) is a separate
  methodology, offered as part of Ocula's commercial enrichment services.
- **Not finished.** This repository tracks the v0.1 draft as it lands.

## Repository layout

| Path | Purpose |
|------|---------|
| [`descriptors/`](./descriptors/) | The capability schema and its component types, examples, and design documentation. |
| [`taxonomy/`](./taxonomy/) | The companion shopping-intent taxonomy — machine-readable JSON + human-readable Markdown. |
| [`validator/`](./validator/) | Python CLI for validating product responses and manifest entries against the schema. |

## Hosting

Canonical `$id` URLs for the schemas resolve under `https://ucp-extension.ocula.tech/...` once
GitHub Pages + DNS are wired (tracked separately). The hostname is a subdomain of `ocula.tech`,
which preserves UCP's origin-validation expectation that schemas come from the namespace
authority domain (`tech.ocula.*` ⇄ `ocula.tech`).

## License

Apache 2.0 — see [`LICENSE`](./LICENSE).

## Contributing

The repository is private during v0.1 development. Contribution guidelines will be published
alongside the v0.1 launch.
