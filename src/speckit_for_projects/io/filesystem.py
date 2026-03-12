"""Filesystem access helpers."""

from __future__ import annotations

from pathlib import Path


def read_text(path: Path) -> str:
    """Read text using UTF-8."""
    return path.read_text(encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    """Write text using UTF-8."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
