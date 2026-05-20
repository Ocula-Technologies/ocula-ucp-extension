# Roadmap

Where `tech.ocula.shopping.descriptors` goes after v0.1. This is direction, not commitment — shapes
and sequencing will shift with adoption and UCP working-group feedback.

## After v0.1

### Category-specific extensions

The v0.1 descriptors are category-agnostic. Category packs would add structured fields where a
category's buying decision needs them:

- **Apparel** — fit, fabric, care, sizing systems.
- **Electronics** — compatibility, specifications, port/standard support.
- **Beauty** — ingredients, skin/hair-type fit, claims substantiation.

Each would ship as its own additive layer, composing the same way the base extension does — no
breaking change to v0.1.

### Promotion to `dev.ucp.*`

`tech.ocula.shopping.descriptors` lives in Ocula's vendor namespace by design — a vendor extension
can ship and iterate without working-group consensus. If the descriptive layer gains adoption, the
path is promotion into the core `dev.ucp.*` namespace, following the precedent of
[Affirm's payment extension RFC (#384)](https://github.com/Universal-Commerce-Protocol/ucp/issues/384).

## Deferred from v0.1

*Populated as v0.1 firms up: what was considered and cut, and why.*
