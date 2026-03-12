"""Template loading and rendering."""

from __future__ import annotations

from importlib.resources import files

from jinja2 import Environment, FileSystemLoader, StrictUndefined


def build_environment() -> Environment:
    """Build the Jinja environment for package templates."""
    template_root = files("speckit_for_projects").joinpath("templates")
    loader = FileSystemLoader(str(template_root))
    return Environment(loader=loader, autoescape=False, undefined=StrictUndefined, trim_blocks=True)
