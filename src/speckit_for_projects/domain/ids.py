"""ID generation rules."""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

SEQUENCED_SLUG_PATTERN = re.compile(r"^(?P<number>\d{3})-(?P<slug>[a-z0-9-]+)$")


def slugify(value: str) -> str:
    """Convert free text into a kebab-case slug."""
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    lowered = normalized.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", lowered).strip("-")
    return slug or "item"


def next_sequenced_slug(parent: Path, label: str) -> str:
    """Generate the next repo-local sequenced slug under a directory."""
    slug = slugify(label)
    parent.mkdir(parents=True, exist_ok=True)
    max_number = 0
    for child in parent.iterdir():
        name = child.stem if child.is_file() else child.name
        match = SEQUENCED_SLUG_PATTERN.match(name)
        if match:
            max_number = max(max_number, int(match.group("number")))
    return f"{max_number + 1:03d}-{slug}"
