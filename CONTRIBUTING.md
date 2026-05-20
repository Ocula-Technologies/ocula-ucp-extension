# Contributing

Thanks for your interest in `tech.ocula.shopping.descriptors` and its companion shopping-intent
taxonomy. This is a UCP vendor extension under active development; contributions to the schemas,
taxonomy, examples, and docs are welcome.

## Ground rules

- **Be respectful.** This project follows the [Contributor Covenant](./CODE_OF_CONDUCT.md).
- **License.** Contributions are accepted under the repository's [Apache 2.0 license](./LICENSE).
  By opening a pull request you agree your contribution is licensed under those same terms. No CLA
  is required.
- **Scope.** The extension defines *structure* — whether descriptors are present, well-formed, and
  use documented vocabulary. Content-quality judgements are deliberately out of scope (see the
  README), so proposals to add quality scoring to the open schema won't be merged.

## How to propose a change

- **Schema, taxonomy, or vocabulary changes:** open an issue first. These ripple into manifests
  and downstream consumers, so it's worth agreeing the shape and compatibility story before you
  invest in a PR.
- **Docs, examples, typos, and obvious fixes:** open a pull request directly.
- **New intent values or dimensions:** the vocabularies are *open*, so additions are welcome — via
  issue or PR — provided they follow the compatibility rules below.

## Compatibility rules

Enforced in review, and partly in CI. Changes that break them won't be merged.

- **Schemas are versioned by date** (`descriptors/schemas/<YYYY-MM-DD>/`) and target
  **JSON Schema Draft 2020-12**. Once a dated version is published and referenced by external
  manifests, treat it as frozen — ship changes as a *new* dated directory, not edits to a released
  one.
- **Growth is additive.** New values and optional fields are fine. Never rename or remove a
  published vocabulary value — mark it deprecated in the human-readable spec instead. Because the
  vocabularies are open (consumers MUST tolerate unknown values), additions never force a change on
  existing consumers.
- **Breaking structural changes** (renaming a key, restructuring arrays) require a **new versioned
  namespace** — e.g. `tech.ocula.shopping.intents.v2` — rather than an edit to the existing one.
- **Taxonomy invariants** (checked by CI): every dimension name and value is `snake_case`, and each
  value belongs to exactly one dimension, so a value alone identifies its dimension.

## Running the checks locally

Two workflows run on every PR — `schema-lint` and `link-check`. You can run the same schema checks
before pushing:

```bash
pip install check-jsonschema referencing

# 1. Schemas validate against the JSON Schema 2020-12 metaschema
check-jsonschema --check-metaschema descriptors/schemas/**/*.json

# 2. Every $ref resolves (local schemas + upstream UCP URLs)
python .github/scripts/resolve_refs.py descriptors/schemas

# 3. Taxonomy invariants (snake_case, values unique across dimensions)
python .github/scripts/lint_taxonomy.py taxonomy/shopping_intents.json
```

Markdown links are checked by [lychee](https://github.com/lycheeverse/lychee) — keep links live.

## Commit and PR conventions

- Use [Conventional Commits](https://www.conventionalcommits.org/) (`feat(descriptors): …`,
  `docs: …`, `ci: …`).
- Keep each PR to one logical change.
- When you change a schema, update the affected examples under `descriptors/examples/` and the
  relevant docs in the same PR.
- A maintainer reviews every PR; `CODEOWNERS` routes the request automatically.

## Don't commit client data

`private/` and `client-feeds/` are gitignored and must stay that way — never commit real customer
catalogue data. Use the synthetic payloads under `descriptors/examples/` for fixtures.

## Reporting a security issue

Email **support@ocula.tech** rather than opening a public issue.
