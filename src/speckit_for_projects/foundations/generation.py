"""Template generation helpers."""

from __future__ import annotations

from pathlib import Path

from speckit_for_projects.foundations.scaffolding import WriteResult, ensure_directory
from speckit_for_projects.foundations.templating import build_environment


def render_template(template_name: str, **context: object) -> str:
    """Render a package template by name."""
    environment = build_environment()
    return environment.get_template(template_name).render(**context).rstrip() + "\n"


def render_to_path(
    destination: Path, template_name: str, *, overwrite: bool, **context: object
) -> WriteResult:
    """Render a template to a path, optionally overwriting existing files."""
    ensure_directory(destination.parent)
    content = render_template(template_name, **context)
    if destination.exists() and not overwrite:
        return WriteResult(path=destination, changed=False)
    destination.write_text(content, encoding="utf-8")
    return WriteResult(path=destination, changed=True)
