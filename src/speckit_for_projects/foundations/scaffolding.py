"""Filesystem scaffolding helpers."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class WriteResult:
    """Result of writing one scaffold file."""

    path: Path
    changed: bool


def ensure_directory(path: Path) -> None:
    """Create a directory when it does not exist."""
    path.mkdir(parents=True, exist_ok=True)
