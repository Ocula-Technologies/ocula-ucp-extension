# Descriptors — design rationale

> **DRAFT.** This captures the design choices the schemas in
> `descriptors/schemas/2026-05-18/` are predicated on — identity, composition,
> authoring conventions, field shapes, and structural required/optional rules.

## Identity and versioning

### Capability name: `tech.ocula.shopping.descriptors`

Plural noun. Matches UCP's single-word noun convention for core capabilities
(`catalog`, `checkout`, `fulfillment`, `discount`, `pay`), survives a future
promotion into the `dev.ucp.*` namespace, and aligns with the framing of this
extension as the *descriptive layer* of the catalog response — what the
returned product objects describe, rather than a process or workflow applied
to them.

### Date-based versioning

Versions use the form `YYYY-MM-DD`. New versions get new dates; older versions
stay resolvable at their original `$id` URLs so existing integrations don't
break when a new draft ships. Version cadence is independent of UCP's own
release schedule.

### `$id` URL on the namespace authority domain

Canonical `$id` URLs take the shape
`https://ocula.tech/ucp-extension/<version>/descriptors.json`. UCP requires
each capability's `spec` and `schema` URLs to originate from the domain the
reverse-domain namespace claims authority over — under the strict reading of
the spec, schemas served from raw GitHub URLs would not satisfy
origin-validation. Hosting on `ocula.tech` from day one avoids that debt.

### Required top-level metadata

Each schema carries `$schema` (`https://json-schema.org/draft/2020-12/schema`),
`$id`, `title`, `description`, `name`, and `version` per UCP's self-describing
convention.

## Composition mechanism

### Manifest and schema are two artefacts

The `extends` declaration lives in the **capability manifest** — the discovery
block a business publishes at `/.well-known/ucp`. The actual schema composition
(`allOf` + `$ref`) lives inside the **schema file's `$defs`**. They ship
together but are authored as distinct concerns. This mirrors how
`dev.ucp.shopping.discount` is structured in the live spec: the discount
schema file itself has no `extends` field; the relationship is declared by
manifests that reference it.

The repository's
[`descriptors/examples/manifest.json`](../examples/manifest.json) shows the
manifest side; the schema files under
[`descriptors/schemas/2026-05-18/`](../schemas/2026-05-18/) show the
composition side.

### Multi-parent extension

The manifest declares
`extends: ["dev.ucp.shopping.catalog.search", "dev.ucp.shopping.catalog.lookup"]`.
In the live UCP spec, `catalog.search` and `catalog.lookup` are two separate
capabilities — not two operations of a single `catalog` capability — so
multi-parent extension is required, not optional, for a single capability that
decorates both response surfaces consistently.

### Composition target: `products[].items`

The `descriptors` field decorates each product *inside* the response's
`products` array, one level deeper than the discount precedent. The `allOf`
composition wraps the augmented product object, not the response root. This
keeps the extension's footprint scoped to where the enrichment actually lives
and lets the same composition apply to both `search` and `lookup` responses
without restating it at two different roots.

## Response shape: nested under `descriptors`

Each augmented product carries a single `descriptors` field at its root,
holding the five sub-structures, rather than five flat `descriptor_*` fields
on the product:

```json
{
  "id": "prod_abc123",
  "title": "Blue Runner Pro",
  "descriptors": {
    "highlights": [...],
    "qa_pairs": [...],
    "use_cases": [...],
    "intent_tags": [...],
    "differentiators": [...]
  }
}
```

This follows the precedent set by `dev.ucp.shopping.discount`, which adds a
single `discounts` field to the cart rather than flat discount-related
fields. The capability name and the field name align (`descriptors` capability
→ `descriptors` field). A single negotiation flag controls a single
container, namespace pollution on the product root stays contained, and future
sub-structures can be added under `descriptors` without claiming new top-level
keys on the product object.

## `$defs` structure

Keyed by structural pieces — one `$def` per sub-structure (`highlight`,
`qa_pair`, `use_case`, `differentiator`), plus a composition variant for the
augmented `products[].items`. This matches how the live `catalog_search.json`
keys `$defs` by structural piece (`search_request`, `search_response`) and
how `discount.json` keys by piece (`allocation`, `applied_discount`,
`discounts_object`).

The UCP authoring guide prescribes a three-variant `$defs` pattern
(`platform_schema` / `business_schema` / `response_schema`); no live UCP
schema actually uses it, so this extension follows the live precedent rather
than the documented one.

## Per-field rationale

### 1. Highlights are objects, not flat strings

Each highlight carries a `category` and an optional `evidence_ref` because
agents need to reason by category ("give me the durability highlights") and
verify claims against evidence, rather than parse free-form benefit text. A
flat string array would lose both of those affordances.

### 2. Q&A pairs carry an `intent` field

Agents matching user queries to products benefit hugely from explicit intent
classification rather than having to infer intent from question text. The
`intent` field makes the matching surface stable and predictable across
authoring styles.

### 3. Use cases have a four-field structure (`scenario`, `persona`, `context`, `outcome`)

Opinionated by design. The four-field shape surfaces cases where merchants
don't actually know who their product is for — which is exactly the gap
descriptors are meant to close. A looser shape would let weak content hide
behind structure. All four fields are required for the same reason: if the
authoring can't name the persona or the outcome, the use case isn't ready to
publish yet.

### 4. Differentiators require a `comparison_basis`

A claim without a comparison basis is just a highlight. Forcing the field
makes spurious comparative claims visible in validation and disciplines
authoring — "lighter" is a highlight; "40% lighter than the previous
generation" is a differentiator.

### 5. Intent tags are namespaced strings

Values use the form `<dimension>:<value>` (e.g. `decision_phase:research`,
`user_type:enthusiast`) drawn from the companion taxonomy at
`taxonomy/shopping_intents.json`. Agents match queries to products on stable
references rather than ad-hoc strings, which is the whole point of having a
taxonomy. The taxonomy is a separate artefact with its own version cadence;
the schema references it by name and version rather than inlining values.

### 6. All vocabularies are open, not closed enums

`category`, `intent`, `comparison_basis`, and `source` are all open string
fields with documented `examples`, not closed enums. Per UCP convention,
clients MUST tolerate unknown values. This lets the taxonomy and well-known
value lists grow without breaking older integrations — a closed enum would
force a breaking version bump for every new value.

### 7. Each non-tag sub-structure object carries an optional `source` field

Provenance is load-bearing in agentic commerce: agents should weight trust by
origin — manufacturer-stated and AI-inferred claims do not carry the same
weight. `source` applies the same authoring discipline to non-comparative
claims that `comparison_basis` already applies to differentiators.

The field is **optional** (retailers without provenance tracking aren't
blocked), **per-item** rather than a `descriptors`-block default (draft-stage
simplicity; defaults may be revisited later), and an **open vocabulary** so
values can evolve.

`source` is the *categorical type of origin* (`manufacturer_spec`,
`ai_generated`, etc.); `evidence_ref` on highlights remains a complementary
URL to a specific backing document, not a substitute.

## Well-known values

Each open vocabulary documents its well-known values via `examples` and
`description` in the schema. The current set:

| Field | Well-known values |
|------|------|
| `highlight.category` | `performance`, `design`, `durability`, `value`, `sustainability`, `compatibility` |
| `qa_pair.intent` | `compatibility`, `sizing`, `use_case`, `comparison`, `care`, `warranty`, `shipping` |
| `differentiator.comparison_basis` | `category_average`, `named_competitor`, `previous_generation`, `industry_standard` |
| `source` (highlights, qa_pairs, use_cases, differentiators) | `manufacturer_spec`, `retailer_test`, `customer_reviews`, `expert_review`, `editorial`, `regulatory`, `ai_generated` |

Clients MUST tolerate values outside these lists. The lists evolve without a
breaking version bump.

## Authoring conventions

These are repository-wide schema-authoring rules, applied consistently across
all `$defs`:

- **`additionalProperties: false` is not set on any object.** JSON Schema's
  default is open; UCP keeps it that way so future backward-compatible field
  additions don't break older clients. Exceptions in the wider UCP spec are
  protocol envelopes and polymorphic discriminators — neither applies to the
  descriptor structures.
- **No `minProperties` / `maxProperties` on objects, no `minItems` /
  `maxItems` on arrays.** UCP defers size constraints to implementers. Empty
  objects and empty arrays are valid against the schema.
- **Open string vocabularies, not closed enums** for any field that may grow.
  Well-known values are documented via `description` and `examples` rather
  than enforced via `enum`.

## Required vs optional structure

- The `descriptors` block itself is **optional** at the product level — a
  product object can omit it entirely and remain valid.
- Within `descriptors`, all five sub-structures (`highlights`, `qa_pairs`,
  `use_cases`, `intent_tags`, `differentiators`) are **optional arrays**.
- Within a `use_case` item, all four fields (`scenario`, `persona`, `context`,
  `outcome`) are **required** — see *Use cases have a four-field structure*
  above for the rationale.
- `statement` on a highlight, `question` and `answer` on a Q&A pair, `claim`
  and `comparison_basis` on a differentiator are required; everything else on
  those objects is optional.

## Implementation notes

### Amounts are integer minor units

UCP's `amount.json` requires integer minor units (cents, not decimal
strings). Any monetary value in a canonical example or fixture must be an
integer minor-unit value and validate against `amount.json`. Decimal strings
like `"10.00"` will fail validation.

## Future scope

The items below are deliberately out of the initial scope. They are deferred
to later versions or live in separate artefacts so the initial surface stays
small enough to ship and validate.

### Variant-level descriptors

UCP's product schema permits each variant to carry its own description. The
initial schema attaches descriptors only at the product level, on the
assumption that most enrichment use cases are model-level. Variant-level
extension is additive (a new `descriptors` field nested in each variant);
revisit in a future version if real client data shows the product-level
surface is too coarse.

### Category-specific extensions

The initial descriptors are category-agnostic. Category packs would add
structured fields where a category's buying decision needs them:

- **Apparel** — fit, fabric, care, sizing systems.
- **Electronics** — compatibility, specifications, port/standard support.
- **Beauty** — ingredients, skin/hair-type fit, claims substantiation.

Each would ship as its own additive layer, composing the same way the base
extension does — no breaking change to existing consumers.

### Quality-scoring methodology

The structural conformance the schema enforces — fields present, well-formed,
using documented vocabulary terms — is intentionally separate from content
quality (is a highlight well-written, is a use case coherent, are intent tags
accurately applied). A companion quality-scoring methodology is out of scope
for the schema itself.
