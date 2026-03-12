from __future__ import annotations

from pathlib import Path

from speckit_for_projects.services.context_assembler import ContextAssembler


def test_context_assembler_includes_domain_map_path(tmp_path: Path):
    context = ContextAssembler().build(tmp_path)

    assert context["domain_map"] == str(tmp_path / ".specify" / "project" / "domain-map.md")
