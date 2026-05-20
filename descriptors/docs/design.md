# Descriptors — design rationale

> **DRAFT — partial document.** The full launch version is tracked under a
> future launch-docs ticket. This stub captures the field-shape rationale that
> the schemas in `descriptors/schemas/2026-05-18/` are predicated on. The
> remaining sections are placeholders.

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

## Future scope

The items below are deliberately out of the initial scope. They are deferred to
later versions or live in separate artefacts so the initial surface stays small
enough to ship and validate.

### Variant-level descriptors

UCP's product schema permits each variant to carry its own description. The
initial schema attaches descriptors only at the product level, on the
assumption that most enrichment use cases are model-level. Variant-level
extension is additive (a new `descriptors` field nested in each variant);
revisit in a future version if real client data shows the product-level
surface is too coarse.

## Why a descriptive layer at all

*TODO — filled in by the launch-docs ticket.*

## Why a vendor extension rather than a metadata blob

*TODO — filled in by the launch-docs ticket.*

## Composition mechanism

*TODO — filled in by the launch-docs ticket.*

## Why response-level composition rather than Product-type extension

*TODO — filled in by the launch-docs ticket.*
