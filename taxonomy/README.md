# Shopping Intent Taxonomy

A controlled vocabulary of shopping intents across four orthogonal dimensions, shipped both
machine-readable and human-readable.

| File | Audience |
|------|----------|
| [`shopping_intents.json`](./shopping_intents.json) | Machines — ingestion, indexing, tag validation. |
| [`shopping_intents.md`](./shopping_intents.md) | Humans — per-intent definitions, positive and negative examples, wire format. |
| [`docs/methodology.md`](./docs/methodology.md) | Reviewers — why these dimensions, what was rejected, orthogonality argument, deferred-to-v0.2. |

## What this is

`tech.ocula.shopping.intents` is a vocabulary of shopping intent values organised across four
dimensions: `purchase_context` (why are they buying), `decision_phase` (where in the funnel),
`user_type` (what kind of shopper), and `situational_fit` (in what setting will it be used).

It is the companion vocabulary to the `tech.ocula.shopping.descriptors` capability extension —
values from this taxonomy appear in `descriptors.intent_tags[]` and `descriptors.qa_pairs[].intent`
on product responses. But the taxonomy stands on its own and can be ingested by any system that
needs a stable, shared vocabulary of shopping intent.

The vocabulary is **open**: consumers MUST tolerate unknown values, and growth is additive.
Existing values are never renamed or removed once published.

## Why it's useful beyond UCP

The taxonomy was built for UCP product responses, but it isn't UCP-specific. A controlled,
orthogonal intent vocabulary is independently useful for:

- **Search relevance.** Intent tags let a search system re-rank results by contextual fit, not
  just keyword match. A `decision_phase:research` shopper benefits from broad-coverage results;
  a `decision_phase:ready_to_buy` shopper benefits from narrow, decision-supporting results.

- **Recommendation systems.** Intent dimensions are stable features for collaborative filtering
  and content-based recommendation. Shoppers in similar `purchase_context` × `user_type`
  cells tend to convert on similar products, and the cells are interpretable to merchandisers
  in ways latent embeddings aren't.

- **Merchandising and content surfacing.** Editorial and merchandising decisions are easier to
  reason about against an explicit taxonomy than against ad-hoc tags. "What do we show shoppers
  in `purchase_context:gift` + `decision_phase:research`?" is a tractable question; "what do we
  show shoppers tagged with `gift-research-stuff`?" isn't.

## How to use it

**Machines:** ingest `shopping_intents.json`. The file is shaped as a single JSON object with
a `dimensions` map. Each dimension has a `values` array of strings. The encoding for tags is
`<dimension>:<value>` (e.g. `decision_phase:research`). Tolerate unknown values.

**Humans:** read `shopping_intents.md`. Every value has a definition, positive examples, negative
examples (the boundary cases that distinguish it from neighbours), and its wire format.

**Reviewers:** read `docs/methodology.md`. Defends the choice of four dimensions, lists what was
rejected and why, makes the orthogonality argument, and lists what was deferred to v0.2.

## Versioning

The current version is `2026-05-18`. See `docs/methodology.md` for the versioning policy: open
vocabulary, additive growth, no renames or removals once published.

## License

Apache 2.0 — see the [repository LICENSE](../LICENSE).
