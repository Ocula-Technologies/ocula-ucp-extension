# ocula-ucp-extension

Ocula's open vendor extensions to the [Universal Commerce Protocol (UCP)](https://ucp.dev).
Initial scope: `tech.ocula.shopping.descriptors` — the descriptive layer for agentic commerce.

> **Status:** `draft — pre-release.` RFC not yet submitted to the UCP working group.
> Schemas, taxonomy, and validator are under active development; shapes may change before the
> first public release.

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
  into the `dev.ucp.*` namespace if it gains adoption — following the precedent of
  [Affirm's payment extension RFC (#384)](https://github.com/Universal-Commerce-Protocol/ucp/issues/384).
- **Not a content-quality methodology.** The validator checks structural conformance only —
  whether fields are present, well-formed, and use documented vocabulary terms. Content quality
  assessment (whether a highlight is well-written, whether a use case is coherent) is a separate
  methodology, offered as part of Ocula's commercial enrichment services.
- **Not finished.** This repository tracks the draft as it lands.

## Repository layout

| Path | Purpose |
|------|---------|
| [`descriptors/`](https://github.com/Ocula-Technologies/ocula-ucp-extension/tree/main/descriptors) | The capability schema and its component types, examples, and design documentation. |
| [`taxonomy/`](https://github.com/Ocula-Technologies/ocula-ucp-extension/tree/main/taxonomy) | The companion shopping-intent taxonomy — machine-readable JSON + human-readable Markdown. |
| [`validator/`](https://github.com/Ocula-Technologies/ocula-ucp-extension/tree/main/validator) | Python CLI for validating product responses and manifest entries against the schema. |

## Hosting

Canonical `$id` URLs for the schemas resolve under `https://ocula.tech/ucp-extension/...`. They
sit on the `ocula.tech` root domain — the same domain the `tech.ocula.*` namespace claims
authority over — so they satisfy UCP's origin-validation rule under the strict reading of the
spec.

## License

Apache 2.0 — see [`LICENSE`](./LICENSE).

## Contributing

Contributions are welcome — see [`CONTRIBUTING.md`](./CONTRIBUTING.md) for how to propose schema,
taxonomy, and documentation changes and what the conformance checks expect. By participating you
agree to our [Code of Conduct](./CODE_OF_CONDUCT.md).
