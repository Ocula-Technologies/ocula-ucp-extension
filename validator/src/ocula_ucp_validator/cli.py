"""`ocula-ucp-validate` command-line entry point."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Annotated

import typer
from referencing.exceptions import Unretrievable

from ocula_ucp_validator.report import ValidationResult, render_human
from ocula_ucp_validator.schema import local_first_retrieve
from ocula_ucp_validator.validate import DEFAULT_VARIANT, validate_manifest, validate_response

EXIT_OK = 0
EXIT_VALIDATION_FAILED = 1
EXIT_USAGE = 2

app = typer.Typer(
    help="Validate UCP feed responses and manifest entries for tech.ocula.shopping.descriptors.",
    no_args_is_help=True,
    add_completion=False,
)


@app.command()
def response(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    capability: Annotated[
        Path,
        typer.Option(
            "--capability",
            help="Path to the descriptors capability schema JSON.",
            exists=True,
            dir_okay=False,
            readable=True,
        ),
    ],
    variant: Annotated[
        str, typer.Option(help="Capability `$defs` variant to validate against.")
    ] = DEFAULT_VARIANT,
    json_out: Annotated[
        bool, typer.Option("--json", help="Emit machine-readable JSON instead of grouped text.")
    ] = False,
    schema_root: Annotated[
        Path | None,
        typer.Option(
            "--schema-root",
            help="Resolve ocula.tech/ucp-extension/* $refs from this dir, not the network.",
            exists=True,
            file_okay=False,
        ),
    ] = None,
) -> None:
    """Validate a feed response against a capability schema variant."""
    payload = json.loads(file.read_text())
    retrieve = local_first_retrieve(schema_root) if schema_root else None
    try:
        result = validate_response(payload, capability, variant=variant, retrieve=retrieve)
    except Unretrievable as exc:
        detail = exc.__cause__ or f"could not retrieve {exc.ref!r}"
        typer.echo(f"error: {detail}", err=True)
        raise typer.Exit(code=EXIT_USAGE) from exc
    _emit(result, json_out)


@app.command()
def manifest(
    file: Annotated[Path, typer.Argument(exists=True, dir_okay=False, readable=True)],
    json_out: Annotated[
        bool, typer.Option("--json", help="Emit machine-readable JSON instead of grouped text.")
    ] = False,
) -> None:
    """Validate a `/.well-known/ucp` manifest entry."""
    payload = json.loads(file.read_text())
    result = validate_manifest(payload)
    _emit(result, json_out)


def _emit(result: ValidationResult, json_out: bool) -> None:
    if json_out:
        typer.echo(json.dumps(result.to_dict(), indent=2))
    else:
        typer.echo(render_human(result))
    if not result.is_valid:
        raise typer.Exit(code=EXIT_VALIDATION_FAILED)


def main() -> None:
    try:
        app()
    except typer.Exit:
        raise
    except json.JSONDecodeError as exc:
        typer.echo(f"error: {exc}", err=True)
        sys.exit(EXIT_USAGE)


if __name__ == "__main__":
    main()
