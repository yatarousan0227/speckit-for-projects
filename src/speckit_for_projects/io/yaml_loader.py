"""YAML helpers with order preservation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from ruamel.yaml import YAML


def build_yaml() -> YAML:
    """Create a configured YAML instance."""
    yaml = YAML()
    yaml.preserve_quotes = True
    yaml.default_flow_style = False
    return yaml


def load_yaml(path: Path) -> Any:
    """Load a YAML document from disk."""
    yaml = build_yaml()
    with path.open("r", encoding="utf-8") as handle:
        return yaml.load(handle)


def dump_yaml(path: Path, data: Any) -> None:
    """Dump a YAML document to disk."""
    yaml = build_yaml()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        yaml.dump(data, handle)
