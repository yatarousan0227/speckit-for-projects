"""Minimal Markdown read/write helpers."""

from __future__ import annotations

from pathlib import Path

from speckit_for_projects.io.filesystem import read_text, write_text


def load_markdown(path: Path) -> str:
    """Load a Markdown file as plain text."""
    return read_text(path)


def dump_markdown(path: Path, content: str) -> None:
    """Persist Markdown content."""
    write_text(path, content)
