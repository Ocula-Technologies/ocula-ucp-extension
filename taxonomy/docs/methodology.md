# Taxonomy Construction Methodology

This document defends the construction of `tech.ocula.shopping.intents` v0.1: what informed it,
why the dimensions are what they are, why we rejected the alternatives we considered, the
orthogonality claim, and what we deliberately deferred. The vocabulary itself is in
[`../shopping_intents.json`](../shopping_intents.json); per-value definitions are in
[`../shopping_intents.md`](../shopping_intents.md).

It is intended to read as methodology, not marketing. If a claim below cannot be defended in
review, it should be revised or removed.

## Source material

The taxonomy is grounded in catalogue exposure from Ocula's enrichment work across enterprise
retailers. Across that work, shoppers' decision-shaping context falls into a small number of
recurring axes: why they're buying, where they are in the funnel, what their relationship with
the category is, and what situation the product will serve. These four axes are the dimensions
of the v0.1 taxonomy.

The vocabulary itself is drafted from these observations and is subject to review against the
underlying catalogues for coverage, naming consistency, and orthogonality between dimensions
before publication.

No prior published taxonomy maps shopping intents along these dimensions in a way AI agents can
use as a stable reference. Existing work in the space is either merchant-specific or buried
inside proprietary recommendation engines, so the taxonomy is not inherited from a third-party
framework.

## Scope of this document

The four dimensions and their values are drawn from Ocula's catalogue work. The remaining
sections of this document — rejected alternatives, known tensions, and deferred-to-v0.2
candidates — are design-time reasoning at draft stage, intended to give reviewers something
concrete to push back against. They are not a record of historical deliberation. Reviewers
should amend or replace any item that does not reflect Ocula's actual position.

## Why these four dimensions

The v0.1 taxonomy uses four dimensions because four questions repeatedly explain a shopper's
context:

| Dimension | Question it answers |
|-----------|---------------------|
| `purchase_context` | Why are they buying? |
| `decision_phase` | Where are they in the funnel? |
| `user_type` | Who are they, in relation to the category? |
| `situational_fit` | Where, when, or in what setting will the product be used? |

Each is necessary: pairs of products at the same category, price, and feature set diverge in
their suitability for a shopper depending on one (or more) of these dimensions. None is
sufficient on its own.

### Rejected alternatives

Each of the following was considered and rejected for v0.1.

**Price tier** (`luxury`, `mid_range`, `budget`). Rejected because it describes the product, not
the shopper's context. UCP already carries price information directly; intent should be
orthogonal to product attributes.

**Demographics** (`age_band`, `gender`, `region`). Rejected for three reasons: (a) privacy
implications would compromise adoption, (b) demographic membership is a weak predictor of intent
relative to the four dimensions chosen, (c) the buyer's demographic often differs from the end
user's (gifts especially).

**Category-of-product**. Rejected: UCP carries product taxonomy / category natively. The intent
taxonomy is deliberately orthogonal to category so that the same intent (e.g.
`decision_phase:research`) is meaningful regardless of what the shopper is researching.

**Channel** (`web`, `mobile`, `voice`, `in_store`). Rejected: channel is a property of how the
interaction is happening, not of the shopper's intent. A shopper in `decision_phase:research`
behaves comparably across channels; surfacing channel-specific content is a job for the
front-end, not the taxonomy.

**Emotional driver** (`status`, `comfort`, `identity`, `belonging`). Rejected as a primary
dimension because it cannot be reliably applied at the catalogue level — emotional drivers are
expressive of an underlying decision, not the decision itself. Their observable consequences
(luxury for status, daily-driver for comfort, gift for belonging) are already captured in the
four chosen dimensions.

**Price sensitivity** (`price_sensitive`, `price_flexible`). Rejected: every shopper has *some*
budget, so the tag over-applies; and the more useful signal — the actual budget range — is
either inferrable from price-filter behaviour or out of scope for a public extension.

**Brand loyalty** (`brand_loyal`, `brand_open`). Rejected for v0.1: implementations vary widely
in how brand affinity is modelled, and there isn't enough cross-implementation signal to
standardise a vocabulary yet. Revisit when more partners are using the v0.1 taxonomy.

**Single-dimension flat list** (e.g. `gift_research_beginner_travel` as one token). Rejected:
flat compound tokens defeat compositionality. The whole value of the taxonomy comes from being
able to assert one dimension's value without committing to the others, and from being able to
intersect tags across products to surface matches.

**A fifth `frequency_of_use` dimension** (`rare`, `occasional`, `daily`, `constant`). Rejected:
the common case (everyday use) is already captured by `situational_fit:daily_use`, and the
remaining frequency points are either rare enough to defer (`constant` for industrial use cases)
or fold cleanly into other dimensions (`rare` ≈ `special_occasion` or `seasonal`). A full
frequency dimension is a candidate for v0.2 if patterns recur.

## Orthogonality argument

The four dimensions are designed so that knowing a value on one dimension tells you nothing
about which value applies on the others. A `decision_phase:research` shopper can be a beginner
or a professional, buying as a gift or for themselves, for any situation.

Pairwise:

| Pair | Independence |
|------|--------------|
| `purchase_context` × `decision_phase` | A gift can be in any funnel position. An upgrade can be in research, comparison, or ready-to-buy. |
| `purchase_context` × `user_type` | Any user type can be making any kind of purchase (gift, replacement, upgrade, etc.). |
| `purchase_context` × `situational_fit` | A gift can be for any situation (travel, daily use, seasonal, etc.). |
| `decision_phase` × `user_type` | Any user type can be in any funnel position. Beginners can be ready-to-buy; professionals can be researching. |
| `decision_phase` × `situational_fit` | A research-phase shopper can be choosing for any situation. |
| `user_type` × `situational_fit` | A beginner can be choosing for any situation. A professional can be choosing for personal home use. |

### Known tensions

Three places where the orthogonality is imperfect, called out so reviewers can judge whether the
tradeoff is acceptable:

1. **`urgent_need` lives in `purchase_context`** even though urgency is more naturally a
   property of timing pressure than of motivation. It is placed here because the urgency is a
   circumstance of *why-now*, not a funnel position — an urgent shopper can still be in research
   if (say) their dishwasher just broke and they don't know what to buy. We accepted the slight
   axis stretch over creating a fifth dimension just to host urgency.

2. **`bulk_order` and `user_type:professional` correlate strongly** in practice. They remain
   conceptually independent (homeowners buying cases of wine for a wedding is a non-professional
   bulk order), but the correlation is real. We accept this as a practical fact, not a modelling
   failure — orthogonality is a design principle, not a statistical claim about empirical
   independence.

3. **`situational_fit:daily_use` is about frequency, not setting**, while the rest of
   `situational_fit` is about location/setting. Daily-use can co-occur with `home_use` or
   `professional_setting` (the dimension allows multiple values), so the issue is one of
   semantic uniformity within the dimension rather than orthogonality across dimensions. The
   alternative — promoting frequency to its own dimension — has been deferred to v0.2 because
   `daily_use` covers the dominant case and the cost of a fifth dimension didn't justify the
   precision gain.

These tensions are documented rather than resolved. v0.2 should revisit them with feedback from
real client data.

## Versioning policy

The vocabulary is **open** per UCP convention: consumers MUST tolerate unknown values rather
than rejecting them as invalid. This is what makes additive growth possible.

The vocabulary grows **additively**:

- New values MAY be added at any version bump and require no consumer changes.
- New dimensions MAY be added at minor version bumps; consumers that ignore unknown dimensions
  continue to function.
- Existing values MUST NOT be renamed or removed. If a value was a mistake, mark it deprecated
  in the human-readable spec and discourage its use; do not delete it.
- Structural changes (renaming the `dimensions` key, restructuring `values` arrays) would
  require a new versioned namespace, e.g. `tech.ocula.shopping.intents.v2`.

The `version` field in `shopping_intents.json` is the date the version was published. Consumers
SHOULD check the version they have ingested against the published one periodically; new values
will only be visible after a refresh.

## Deferred to v0.2

The following candidates were considered for v0.1 and explicitly deferred.

- **`subscription_intent`** (one-time vs. subscription). Deferred because the wire format would
  interact with `decision_phase:ready_to_buy` in ways we want to see real client signal on
  before standardising. Likely v0.2 if subscription commerce continues to grow inside UCP.

- **`accessibility_needs`**. Deferred because the right modelling is genuinely unclear: shopper-
  asserted preference vs. requirement, opt-in vs. inferred, granularity (motor / visual /
  cognitive / sensory). Also has privacy implications that warrant a dedicated design pass.

- **`frequency_of_use`** as its own dimension (`rare`, `occasional`, `daily`, `constant`).
  Deferred because `daily_use` already captures the dominant case, but real catalogue data may
  show a need for finer-grained frequency, especially in B2B / industrial contexts.

- **`sustainability_preference`** (`eco_conscious`, `circular_economy`). Deferred because the
  meaningful signal differs by category — recycled materials in apparel, energy ratings in
  appliances, fair-trade certification in food — and the cross-category abstraction isn't
  obvious yet. Likely better modelled as a separate vocabulary, not a dimension here.

- **`price_sensitivity`**. Deferred (and possibly rejected outright). See "rejected alternatives"
  above. Revisit only if real demand emerges from clients.

- **`promotional_pickup`** (purchase driven by a sale / coupon) as a value in
  `purchase_context`. Deferred because consumers can infer this from UCP's existing price /
  promo fields, and there's no clear use case yet that needs the explicit tag.

- **A `relationship_to_recipient`** sub-axis for gifts (`romantic`, `family`, `professional`,
  `acquaintance`). Deferred because the privacy implications are real and the lift in
  recommendation quality from this signal is unclear.

When v0.2 is drafted, each of these gets revisited with whatever client validation data v0.1
produces.
