"""CLI entry-point tests covering subcommands, exit codes, and output formats."""

from __future__ import annotations

import json
from pathlib import Path

import pytest
from typer.testing import CliRunner

from ocula_ucp_validator import schema as schema_module
from ocula_ucp_validator.cli import EXIT_OK, EXIT_USAGE, EXIT_VALIDATION_FAILED, app
from tests._retrievers import offline_retrieve

runner = CliRunner()


@pytest.fixture(autouse=True)
def _offline_retriever(monkeypatch: pytest.MonkeyPatch) -> None:
    """Force CLI invocations to use vendored ucp.dev fixtures, not the live network."""
    monkeypatch.setattr(schema_module, "http_retrieve", offline_retrieve)


def test_response_valid_exits_zero(fixtures_dir: Path, capability_path: Path) -> None:
    result = runner.invoke(app, [
        "response", str(fixtures_dir / "valid_search_response.json"),
        "--capability", str(capability_path),
    ])
    assert result.exit_code == EXIT_OK, result.stdout


def test_response_invalid_exits_one(fixtures_dir: Path, capability_path: Path) -> None:
    result = runner.invoke(app, [
        "response", str(fixtures_dir / "invalid_descriptors_wrong_type.json"),
        "--capability", str(capability_path),
    ])
    assert result.exit_code == EXIT_VALIDATION_FAILED
    assert "/products/0/descriptors/highlights" in result.stdout


def test_response_missing_file_exits_usage(capability_path: Path) -> None:
    result = runner.invoke(app, [
        "response", "does-not-exist.json", "--capability", str(capability_path),
    ])
    assert result.exit_code == EXIT_USAGE


def test_response_unresolvable_ref_exits_usage_with_url(fixtures_dir: Path) -> None:
    """An unreachable `$ref` exits cleanly (code 2) with the URL, not a traceback."""
    result = runner.invoke(app, [
        "response", str(fixtures_dir / "valid_search_response.json"),
        "--capability", str(fixtures_dir / "descriptors_capability_unresolvable.json"),
    ])
    assert result.exit_code == EXIT_USAGE, result.output
    assert result.exception is None or isinstance(result.exception, SystemExit), result.exception
    assert "missing.json" in result.output


def test_manifest_valid_exits_zero(fixtures_dir: Path) -> None:
    result = runner.invoke(app, ["manifest", str(fixtures_dir / "manifest_valid.json")])
    assert result.exit_code == EXIT_OK, result.stdout


def test_manifest_invalid_exits_one(fixtures_dir: Path) -> None:
    result = runner.invoke(app, ["manifest", str(fixtures_dir / "manifest_bad_version.json")])
    assert result.exit_code == EXIT_VALIDATION_FAILED
    assert "version" in result.stdout


def test_json_output_emits_structured_payload(fixtures_dir: Path, capability_path: Path) -> None:
    result = runner.invoke(app, [
        "response", str(fixtures_dir / "invalid_descriptors_wrong_type.json"),
        "--capability", str(capability_path), "--json",
    ])
    assert result.exit_code == EXIT_VALIDATION_FAILED
    payload = json.loads(result.stdout)
    assert payload["is_valid"] is False
    assert payload["errors"], "expected at least one error in JSON output"
    first = payload["errors"][0]
    assert {"path", "json_pointer", "rule", "message"} <= set(first)


def test_json_snapshot_against_known_invalid(fixtures_dir: Path, capability_path: Path) -> None:
    result = runner.invoke(app, [
        "response", str(fixtures_dir / "invalid_descriptors_wrong_type.json"),
        "--capability", str(capability_path), "--json",
    ])
    payload = json.loads(result.stdout)
    assert payload == {
        "is_valid": False,
        "errors": [
            {
                "path": ["products", 0, "descriptors", "highlights"],
                "json_pointer": "/products/0/descriptors/highlights",
                "rule": "type",
                "message": "'not an array' is not of type 'array'",
            }
        ],
    }
