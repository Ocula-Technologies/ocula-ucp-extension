# ocula-ucp-extension

Open vendor extensions to the [Universal Commerce Protocol (UCP)](https://ucp.dev) — the open
standard for how AI agents discover and transact with retailers.

Initial scope: `tech.ocula.shopping.descriptors` — a `catalog` capability extension that adds a
structured **descriptive layer** to product responses, so AI agents can judge contextual fit and
explain products to buyers.

> **Status:** `draft — pre-release.` RFC not yet submitted to the UCP working group.
> Schemas, taxonomy, and validator are under active development; shapes may change before the
> first public release.

## Why a descriptive layer

When an AI agent shops on behalf of a user, it has to answer five distinct question types about
every product. UCP and the active community proposals address four of them:

| Question | Addressed by |
|---|---|
| Hard compatibility — does it technically fit? | [Compatibility & fitment extension (#385)](https://github.com/Universal-Commerce-Protocol/ucp/issues/385) — in flight |
| Efficient catalog discovery — how do I scan the catalog? | [CommerceTXT discovery layer (#351)](https://github.com/Universal-Commerce-Protocol/ucp/issues/351) — in flight |
| Recommendations — what should I suggest alongside or instead of this? | Cross-sell, upsell, and personalisation modules — on UCP's roadmap |
| Payments & loyalty — how does the transaction complete? | [Affirm BNPL](https://github.com/Affirm/ucp-extension), `com.google.pay`, `dev.shopify.shop_pay`, `com.acme.shopping.loyalty` |
| **Descriptive content — what is this product, what is it for, what makes it distinct?** | **This extension** |

Compatibility logic assumes the agent already knows what the product *is*. Recommendation
engines assume agents can evaluate fit. Efficient discovery assumes the underlying data is worth
reading. The descriptive layer is the surface the rest builds on, and it applies to the vast
majority of consumer products — where no hard fit constraint exists.

## What this extension adds

Published under the reverse-domain namespace `tech.ocula.shopping.descriptors`, composing against
`dev.ucp.shopping.catalog.search` and `dev.ucp.shopping.catalog.lookup` via `allOf` + `$ref` per
the UCP [Schema Authoring Guide](https://ucp.dev/documentation/schema-authoring/).

When both platform and business negotiate the extension, each product in a `catalog.search` or
`catalog.lookup` response carries a `descriptors` object:

- **`highlights`** — short benefit statements with a category (`performance`, `design`,
  `durability`, `value`, `sustainability`, `compatibility`, …) and optional evidence reference.
- **`qa_pairs`** — question/answer objects with an `intent` classification drawn from the
  companion taxonomy.
- **`use_cases`** — scenario objects with `persona`, `context`, and `outcome` fields.
- **`intent_tags`** — namespaced vocabulary values (e.g. `decision_phase:research`,
  `user_type:enthusiast`) drawn from the companion shopping-intent taxonomy.
- **`differentiators`** — comparative claims with a required `comparison_basis`
  (`category_average`, `named_competitor`, `previous_generation`, `industry_standard`).

Each item can also carry an optional `source` field (`manufacturer_spec`, `retailer_test`,
`customer_reviews`, `expert_review`, `editorial`, `regulatory`, `ai_generated`) — so agents can
weight trust by provenance, and AI-generated content is disclosed at the schema level rather than
left implicit.

A worked product example lives in [`descriptors/README.md`](descriptors/README.md), with full
composed responses under [`descriptors/examples/`](descriptors/examples/).

## What v0.1 contains

Three pieces, all open and freely usable:

1. **The capability extension** — schemas, examples, and design rationale under
   [`descriptors/`](descriptors/).
2. **A shopping-intent taxonomy** — the controlled vocabulary that `intent_tags` and
   `qa_pairs.intent` draw from, as machine-readable JSON plus human-readable Markdown, under
   [`taxonomy/`](taxonomy/). No published taxonomy currently maps shopping intents (purchase
   context, decision phase, user type, situational fit) in a form AI agents can use as a stable
   reference; this is the substantive heart of v0.1.
3. **An open-source validator** — a Python CLI for checking that a product feed or manifest
   conforms to the spec, under [`validator/`](validator/).

The validator checks **structural conformance** only: fields present, well-formed, and using
documented vocabulary terms. Content quality (is a highlight well-written? is a use case
coherent? are intent tags accurately applied?) is a separate problem and out of scope for v0.1.

## Design choices worth knowing

These are decisions the schema makes on purpose. Each is documented in
[`descriptors/docs/design.md`](descriptors/docs/design.md).

- **Highlights are objects, not flat strings**, so agents can reason by category and verify
  against evidence.
- **Q&A pairs carry an explicit `intent`**, drawn from a documented vocabulary, so agents
  matching a user's question to products don't have to infer intent from question text.
- **Use cases use a four-field structure** (`scenario`, `persona`, `context`, `outcome`) —
  opinionated, and deliberately surfaces the cases where a merchant hasn't decided who a product
  is for.
- **Differentiators require a `comparison_basis`**, because a comparative claim with no
  comparison basis is just a highlight, and forcing the field makes spurious claims visible.
- **Intent tags use a namespaced vocabulary** (e.g. `decision_phase:research`), so agents match
  on stable references rather than ad-hoc strings.
- **All vocabularies are open** per UCP convention: clients MUST tolerate and ignore unknown
  values, so the taxonomy can grow without breaking older integrations.

## What this is not

- **Not a competing standard.** It's a UCP-conformant vendor extension that uses the protocol's
  documented extension mechanism, designed for promotion into the `dev.ucp.*` namespace if it
  gains adoption.
- **Not a content-quality methodology.** The validator checks structural conformance only.
  Scoring whether content is well-written, coherent, or accurate is a separate deliverable.
- **Not finished.** This repository tracks the draft as it lands.

## Roadmap

After v0.1, the directions worth signalling:

- **Category-specific extensions.** Vertical extensions for apparel (fit signals, occasion,
  season), electronics (compatibility, performance specs, certifications), beauty (skin type,
  ingredient flags, claims), and similar — each deepening coverage without bloating the core.
- **A quality-scoring methodology.** A companion methodology for measuring whether descriptive
  content is well-written, coherent, and accurate — sitting on top of the structural spec.
- **Promotion to the UCP core namespace.** If the extension gains traction across multiple
  retailers, propose graduation from `tech.ocula.*` into `dev.ucp.*` via the documented
  Tech Council route.

## Repository layout

| Path | Purpose |
|------|---------|
| [`descriptors/`](descriptors/) | The capability schema and its component types, examples, and design documentation. |
| [`taxonomy/`](taxonomy/) | The companion shopping-intent taxonomy — machine-readable JSON + human-readable Markdown. |
| [`validator/`](validator/) | Python CLI for validating product responses and manifest entries against the schema. |

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
