# Shopping Intents — Human-Readable Spec

**Vocabulary:** `tech.ocula.shopping.intents`
**Version:** `2026-05-18`
**Machine-readable source:** [`shopping_intents.json`](./shopping_intents.json)
**Methodology:** [`docs/methodology.md`](./docs/methodology.md)

This document is the human-readable companion to the machine-readable taxonomy. Each value below
has a definition, positive and negative examples, and its wire format.

---

## Encoding convention

Values are wired as `<dimension>:<value>`. The dimension prefix is mandatory in wire format even
though values are unique across dimensions — the prefix is what makes a tag self-describing in a
mixed list.

| Form | Example |
|------|---------|
| Wire | `decision_phase:research` |
| JSON value | `"decision_phase:research"` |

These tags appear in:

- `descriptors.intent_tags[]` — applied to a whole product.
- `descriptors.qa_pairs[].intent` — applied to a single Q&A pair.

Both fields are **open vocabularies**: implementations MAY use values outside the taxonomy, and
consumers MUST tolerate unknown values. Growth is additive — values are never renamed or removed
once published.

## The four dimensions

| Dimension | What it captures | Example |
|-----------|------------------|---------|
| `purchase_context` | Why the shopper is buying — the motivating circumstance. | `purchase_context:gift` |
| `decision_phase` | Where the shopper sits in the decision funnel. | `decision_phase:research` |
| `user_type` | The shopper's relationship to the product category — expertise, engagement. | `user_type:beginner` |
| `situational_fit` | The situation the product is being chosen for — where, when, in what setting it will be used. | `situational_fit:travel` |

The four dimensions are designed to be orthogonal: a product can carry one (or more) value from
each dimension without the dimensions implying or excluding one another. The orthogonality claim
is defended in [`docs/methodology.md`](./docs/methodology.md).

## Worked example

A home cook upgrading from an entry-level coffee maker to a higher-end espresso machine for
everyday use at home. They have decided which model to buy and are ready to check out.

```json
{
  "descriptors": {
    "intent_tags": [
      "purchase_context:upgrade",
      "decision_phase:ready_to_buy",
      "user_type:enthusiast",
      "situational_fit:daily_use",
      "situational_fit:home_use"
    ]
  }
}
```

Multiple values from the same dimension are permitted — here, both `daily_use` and `home_use`
apply because the product is used both frequently and at home.

---

## `purchase_context`

Why the shopper is buying.

### `purchase_context:gift`

The shopper is buying for someone else, not themselves. The recipient is the end user; the
shopper makes the purchase decision but typically doesn't have direct expertise in the product
category.

**Apply when:** the product is being purchased for another person — birthdays, holidays,
weddings, congratulatory gifts, "treat someone" purchases. Helpful for surfacing gift packaging,
return policies, and "what would they like?" content.

**Do not apply when:** the shopper is buying for themselves, even if the framing is celebratory
(`special_occasion` belongs on `situational_fit`, not here).

**Wire:** `purchase_context:gift`

### `purchase_context:replacement`

The shopper already owns (or owned) a comparable item and is buying another to take its place
because the previous one is broken, worn, lost, or expired. Preserves existing capability rather
than expanding it.

**Apply when:** the prior item is being substituted — replacing a lost charger, a worn-out pair
of shoes, a broken kettle. Helpful for surfacing compatibility-with-prior-purchase content.

**Do not apply when:** the new item is meaningfully better than the old one (use `upgrade`), or
when the shopper is buying a second one for use *alongside* the first (use `repeat_purchase`).

**Wire:** `purchase_context:replacement`

### `purchase_context:upgrade`

The shopper already owns a comparable item and is replacing it with something better — more
features, higher quality, newer generation. Increases capability rather than preserving it.

**Apply when:** the new item is a deliberate step up — upgrading a phone, swapping a basic
blender for a high-end one, moving from entry-level to enthusiast tier. Helpful for surfacing
differentiators-vs-previous-generation content.

**Do not apply when:** the new item is roughly equivalent to the old one — that's `replacement`.
And not when the shopper is new to the category — that's `first_purchase`.

**Wire:** `purchase_context:upgrade`

### `purchase_context:first_purchase`

The shopper has not bought anything in this product category before. They lack a baseline for
comparison and often benefit from foundational content.

**Apply when:** the shopper is new to the category — first DSLR camera, first running shoes,
first set of kitchen knives. Often co-occurs with `user_type:beginner` but is distinct: a
professional photographer buying their first medium-format camera is `first_purchase` but not
`user_type:beginner`.

**Do not apply when:** the shopper has bought in this category before, regardless of whether
this specific model is new to them.

**Wire:** `purchase_context:first_purchase`

### `purchase_context:repeat_purchase`

The shopper has bought this same or equivalent item before and is buying another — not as a
substitute, but in addition (or to maintain a recurring supply). Distinct from `replacement`
(which is substitution) and `bulk_order` (which is multiple units in one transaction).

**Apply when:** the shopper is buying another of the same — restocking consumables, adding a
second matching mug to a set, buying the same shoe again because the previous pair worked out.
Helpful for surfacing reorder shortcuts and "you bought this before" content.

**Do not apply when:** the previous item is being substituted (`replacement`), or when the
shopper is buying multiple units in this transaction (`bulk_order`).

**Wire:** `purchase_context:repeat_purchase`

### `purchase_context:bulk_order`

The shopper is buying multiple units of the same item in a single transaction, typically for
inventory, group consumption, or volume-discount reasons.

**Apply when:** the order quantity is meaningfully greater than a typical single-shopper
purchase — cases of wine for an event, twelve identical T-shirts for a team, office supplies in
volume. Often co-occurs with `user_type:professional` but does not require it.

**Do not apply when:** the shopper is making repeated transactions of one unit over time
(`repeat_purchase`), or when ordering several different items together (just normal shopping —
no tag).

**Wire:** `purchase_context:bulk_order`

### `purchase_context:urgent_need`

The shopper is operating under time pressure — they need the product soon and decision speed
matters. Captures the circumstance, not the funnel state: an urgent shopper may still be in
research or comparison if they're forced to choose quickly.

**Apply when:** delivery speed, in-stock availability, and clear recommendation matter more than
exhaustive comparison — replacing a broken essential, last-minute travel gear, a same-day-need
purchase. Helpful for surfacing expedited shipping and "best fast pick" content.

**Do not apply when:** the shopper is simply in `decision_phase:ready_to_buy`. Ready-to-buy
describes funnel position; `urgent_need` describes a timing constraint that may apply at any
funnel position.

**Wire:** `purchase_context:urgent_need`

---

## `decision_phase`

Where the shopper sits in the decision funnel.

### `decision_phase:research`

The shopper is exploring the category broadly — learning what exists, what matters, and how to
evaluate options. They have not narrowed to a shortlist.

**Apply when:** the shopper is asking "what should I look for?", "what's available?",
"how does this category work?". Helpful for surfacing educational content, category overviews,
and broad highlights.

**Do not apply when:** the shopper has identified two or three specific options they're choosing
between (`comparison`), or has decided what to buy and is checking out (`ready_to_buy`).

**Wire:** `decision_phase:research`

### `decision_phase:comparison`

The shopper has narrowed to a shortlist (typically 2–4 specific options) and is evaluating them
against one another. They know the category and roughly what they want; the question is which
specific product wins.

**Apply when:** the shopper is asking "X vs Y", "which of these is best for…", "what's the
difference between…". Helpful for surfacing competitive differentiators and side-by-side spec
content.

**Do not apply when:** the shopper is still exploring without a shortlist (`research`), or has
chosen a specific item and is finalising purchase (`ready_to_buy`).

**Wire:** `decision_phase:comparison`

### `decision_phase:ready_to_buy`

The shopper has decided what they want and is finalising the purchase — adding to cart,
checking variants, confirming availability, completing checkout.

**Apply when:** the shopper is asking "is this in stock?", "what's shipping?", "which size?",
"can I get it by X?". Helpful for surfacing fulfilment, sizing, and finalisation content.

**Do not apply when:** the shopper is still evaluating alternatives, even if they're close to
deciding (`comparison`).

**Wire:** `decision_phase:ready_to_buy`

### `decision_phase:post_purchase_support`

The shopper has already bought the item and is back with questions, problems, or follow-on
needs — care, accessories, troubleshooting, warranty claims, replacements.

**Apply when:** the question is about an item already owned — "how do I clean this?", "is this
under warranty?", "what accessories work with it?". Helpful for surfacing care, accessory, and
support content.

**Do not apply when:** the shopper is buying a *new* replacement or upgrade — that's a new
purchase event with its own `purchase_context` and a fresh funnel position, not
`post_purchase_support`.

**Wire:** `decision_phase:post_purchase_support`

---

## `user_type`

The shopper's relationship to the product category — expertise, engagement, and frequency of use.
Reflects their relationship with the *category*, not their relationship with this specific
product (which is captured by `purchase_context:first_purchase` / `repeat_purchase`).

### `user_type:beginner`

The shopper is new to the product category and lacks the vocabulary, baseline expectations, and
self-knowledge to evaluate options confidently. They benefit from foundational content and
sensible defaults.

**Apply when:** the shopper is starting out — first running shoes, first chef's knife, first
DSLR. Helpful for surfacing "what to look for" content and recommended-for-beginners highlights.

**Do not apply when:** the shopper has experience in the category but uses it only occasionally
(`occasional_user`), or when they buy professionally but happen to be new to a specific
sub-category (case-by-case — a chef trying their first sous vide is still
`user_type:professional` for cooking generally).

**Wire:** `user_type:beginner`

### `user_type:enthusiast`

The shopper has substantial category knowledge driven by personal interest or hobby. They have
strong preferences, will pay for quality, and engage with the category beyond its utility — they
read reviews, follow brands, optimise their setup.

**Apply when:** the shopper is a hobbyist, collector, or passionate user — home barista, amateur
cyclist, audiophile. Helpful for surfacing technical differentiators, niche features, and
upgrade-vs-current-gear content.

**Do not apply when:** the shopper uses the category for livelihood (`professional`), or uses it
casually without category engagement (`occasional_user`).

**Wire:** `user_type:enthusiast`

### `user_type:professional`

The shopper uses the product category in their work or livelihood. Reliability, durability, and
fit-for-purpose-under-load matter more than novelty or experimentation.

**Apply when:** the shopper is buying for professional use — a contractor's tools, a chef's
knives, a working photographer's lenses. Helpful for surfacing duty-cycle, durability, and
warranty-for-professional-use content.

**Do not apply when:** the shopper is passionate about the category but doesn't earn from it
(`enthusiast`), or when they buy for occasional personal use (`occasional_user`).

**Wire:** `user_type:professional`

### `user_type:occasional_user`

The shopper has some familiarity with the category but uses it rarely — perhaps once a year,
once a season, or for specific events. They prioritise good-enough fit over depth of features
and don't want to over-invest.

**Apply when:** the shopper uses the category infrequently — annual ski trip, occasional dinner
parties, the once-a-year home repair. Helpful for surfacing entry-level recommendations and
"value for the use you'll get" content.

**Do not apply when:** the shopper is new to the category (`beginner`) or engages deeply
(`enthusiast`, `professional`).

**Wire:** `user_type:occasional_user`

---

## `situational_fit`

The situation the product is being chosen for. Multiple values are common — a daily-use mug for
home use is both `situational_fit:daily_use` and `situational_fit:home_use`.

### `situational_fit:travel`

The product will be used away from home — on trips, in transit, while staying somewhere else.
Portability, durability in transit, and conformance to travel rules (airline limits, voltage)
matter.

**Apply when:** the product is being chosen for trip use — carry-on luggage, travel-sized
toiletries, a packable rain jacket. Helpful for surfacing weight, size, and compatibility
content.

**Do not apply when:** the product happens to be portable but is being chosen for at-home use
(`daily_use` / `home_use`), or when the situation is a specific event (`special_occasion`).

**Wire:** `situational_fit:travel`

### `situational_fit:daily_use`

The product will be used routinely — everyday or near-everyday. Reliability under heavy
duty-cycle and longevity matter more than novelty or specialness.

**Apply when:** the product is for routine use — daily-driver shoes, an everyday handbag, a
regular kitchen knife. Helpful for surfacing comfort, durability, and ease-of-care content.

**Do not apply when:** the product is for rare or special situations (`special_occasion`,
`seasonal`).

**Wire:** `situational_fit:daily_use`

### `situational_fit:special_occasion`

The product will be used for a specific, non-routine event — a wedding, an anniversary dinner,
a formal interview, a milestone celebration.

**Apply when:** the use case is a discrete event — a formal dress, an engagement ring, a
champagne for a 50th anniversary. Helpful for surfacing presentation, formality, and
once-and-done quality content.

**Do not apply when:** the event recurs predictably with the seasons (`seasonal`), or when the
use is routine (`daily_use`).

**Wire:** `situational_fit:special_occasion`

### `situational_fit:seasonal`

The product will be used during a recurring time-of-year period — summer-only, winter-only,
holiday-season, back-to-school. Distinct from `special_occasion` (which is a discrete event)
because seasonal use recurs predictably.

**Apply when:** the product is tied to a season or recurring period — a ski jacket, a
Christmas-tree stand, summer sandals, hayfever tablets. Helpful for surfacing
in-season-availability and storage content.

**Do not apply when:** the use is for a one-off event (`special_occasion`), or is genuinely
year-round (`daily_use`).

**Wire:** `situational_fit:seasonal`

### `situational_fit:professional_setting`

The product will be used in a workplace, office, studio, or other professional environment. The
setting (not the user) is what matters — a `user_type:occasional_user` may still buy something
for use in their office.

**Apply when:** the product is being chosen for a work context — office attire, a desk lamp for
a home office, a kitchen tool for a restaurant. Helpful for surfacing dress-code, durability-
under-work-conditions, and noise/aesthetic-fit content.

**Do not apply when:** the product is for personal life at home (`home_use`), even if the
shopper happens to be a professional in their day job. The `user_type` dimension carries
profession; this dimension carries setting.

**Wire:** `situational_fit:professional_setting`

### `situational_fit:home_use`

The product will be used in a domestic / residential setting — a kitchen, a living room, a
bedroom, a garden. Captures location; combines naturally with `daily_use` (everyday at home) or
`special_occasion` (occasional at home).

**Apply when:** the product is for use at home — a sofa, a coffee maker, a garden hose.
Helpful for surfacing fit-with-home-environment and aesthetic-with-domestic-decor content.

**Do not apply when:** the product is portable and being chosen for use elsewhere (`travel`,
`professional_setting`).

**Wire:** `situational_fit:home_use`
