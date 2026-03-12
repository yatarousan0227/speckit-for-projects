"""Domain validation helpers."""

from __future__ import annotations

from pathlib import Path

from speckit_for_projects.domain.exceptions import FilesystemValidationError, InvalidIdentifierError
from speckit_for_projects.domain.ids import SEQUENCED_SLUG_PATTERN


def validate_sequenced_slug(value: str) -> None:
    """Raise InvalidIdentifierError when a sequenced slug is invalid."""
    if not SEQUENCED_SLUG_PATTERN.match(value):
        raise InvalidIdentifierError(f"invalid sequenced slug: {value}")


def validate_existing_directory(path: Path) -> None:
    """Raise FilesystemValidationError when a directory does not exist."""
    if not path.exists() or not path.is_dir():
        raise FilesystemValidationError(f"missing directory: {path}")
