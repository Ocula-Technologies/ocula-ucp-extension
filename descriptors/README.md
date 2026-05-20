# Descriptors (`tech.ocula.shopping.descriptors`)

The descriptive layer of agentic commerce: a UCP `catalog` vendor extension that decorates each
product in a catalog response with structured **highlights**, **Q&A pairs**, **use cases**,
**intent tags**, and competitive **differentiators** — the structures an AI agent needs to judge
contextual fit and describe a product to a buyer.

## How a business advertises it

A business declares the capability in its `/.well-known/ucp` manifest, alongside the UCP catalog
capabilities it extends:

```json
"tech.ocula.shopping.descriptors": [
  {
    "version": "2026-05-18",
    "spec": "https://ocula.tech/ucp-extension/descriptors/",
    "schema": "https://ocula.tech/ucp-extension/descriptors/schemas/2026-05-18/descriptors.json",
    "extends": [
      "dev.ucp.shopping.catalog.search",
      "dev.ucp.shopping.catalog.lookup"
    ]
  }
]
```

Full manifest: [`examples/manifest.json`](examples/manifest.json).

## What it adds to a product

The extension decorates `products[].items` in a `catalog.search` / `catalog.lookup` response with a
`descriptors` object. Excerpt from a composed response:

```json
"descriptors": {
  "highlights": [
    {
      "statement": "Carbon plate returns energy through the gait cycle for less fatigue on long runs.",
      "category": "performance"
    }
  ],
  "qa_pairs": [
    {
      "question": "Do these run true to size?",
      "answer": "Yes — fits true to size for most runners; size down half a size for a narrow forefoot.",
      "intent": "sizing"
    }
  ],
  "use_cases": [
    {
      "scenario": "Weekend trail running in mixed weather",
      "persona": "Intermediate runner training for an ultramarathon",
      "context": "Rocky, muddy single-track, 20-40 km outings",
      "outcome": "Stable footing on technical terrain with energy return that holds through hour three."
    }
  ],
  "intent_tags": ["decision_phase:research", "user_type:enthusiast", "situational_fit:seasonal"],
  "differentiators": [
    {
      "claim": "40% lighter than the previous generation at the same drop and stack height.",
      "comparison_basis": "previous_generation"
    }
  ]
}
```

Full composed responses: [`examples/search_response.json`](examples/search_response.json),
[`examples/lookup_response.json`](examples/lookup_response.json).

## Reference

- **Capability schema:** [`schemas/2026-05-18/descriptors.json`](schemas/2026-05-18/descriptors.json);
  component types live under `schemas/2026-05-18/types/`.
- **Intent vocabulary:** [`../taxonomy/`](../taxonomy/README.md) — the shopping-intent taxonomy that
  `intent_tags` values draw from.
- **Design rationale:** `docs/design.md` — why each field exists, why its shape, and what was rejected.

`category`, `intent`, `comparison_basis`, and `intent_tags` are **open vocabularies**: clients MUST
tolerate and ignore unknown values.
