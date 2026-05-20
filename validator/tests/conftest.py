"""Shared fixtures: paths to vendored test schemas + an offline retriever."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from tests._retrievers import offline_retrieve

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES


@pytest.fixture
def capability_path(fixtures_dir: Path) -> Path:
    return fixtures_dir / "descriptors_capability.json"


@pytest.fixture
def offline() -> Callable[[str], object]:
    return offline_retrieve
