"""Custom exceptions for speckit_for_projects."""

from __future__ import annotations

from dataclasses import dataclass, field


class GeneralSddError(Exception):
    """Base exception for speckit_for_projects."""


class InvalidIdentifierError(GeneralSddError):
    """Raised when a brief-id or design-id is invalid."""


class FilesystemValidationError(GeneralSddError):
    """Raised when a required file or directory is missing."""


@dataclass
class DesignBundleValidationError(GeneralSddError):
    """Raised when a design bundle fails consistency checks."""

    issues: list[str] = field(default_factory=list)

    def __str__(self) -> str:
        return "\n".join(self.issues) if self.issues else "design bundle validation failed"
