"""Build shared context for later AI command usage."""

from __future__ import annotations

from pathlib import Path


class ContextAssembler:
    """Collect shared scaffold paths for AI command prompts."""

    def build(self, project_dir: Path) -> dict[str, str]:
        base = project_dir / ".specify"
        return {
            "project_dir": str(project_dir),
            "glossary": str(base / "glossary.md"),
            "tech_stack": str(base / "project" / "tech-stack.md"),
            "domain_map": str(base / "project" / "domain-map.md"),
            "coding_rules": str(base / "project" / "coding-rules.md"),
            "architecture_principles": str(base / "project" / "architecture-principles.md"),
        }
