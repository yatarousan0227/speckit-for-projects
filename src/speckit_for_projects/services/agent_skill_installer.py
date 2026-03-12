"""Install agent skills derived from shared command templates."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from speckit_for_projects.foundations.app import (
    AGENT_CONFIGS,
    AGENT_SKILLS_DIR_OVERRIDES,
    DEFAULT_SKILLS_DIR,
    AgentConfig,
)
from speckit_for_projects.foundations.generation import render_template
from speckit_for_projects.foundations.scaffolding import ensure_directory
from speckit_for_projects.services.agent_template_installer import COMMAND_SPECS


@dataclass(frozen=True)
class InstalledSkillFile:
    """One installed agent skill file."""

    skill_name: str
    path: Path
    changed: bool


def resolve_skills_directory(project_dir: Path, config: AgentConfig) -> Path:
    """Resolve the skills directory for an agent."""
    override = AGENT_SKILLS_DIR_OVERRIDES.get(config.key)
    if override is not None:
        return project_dir / override
    if config.folder is not None:
        return project_dir / config.folder.rstrip("/") / "skills"
    return project_dir / DEFAULT_SKILLS_DIR


class AgentSkillInstaller:
    """Install SKILL.md files for command templates without mutating commands."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def install(self, ai_assistant: str, *, overwrite: bool = False) -> list[InstalledSkillFile]:
        config = self._resolve_agent(ai_assistant)
        skills_dir = resolve_skills_directory(self.project_dir, config)
        ensure_directory(skills_dir)

        source_dir = self.project_dir / ".specify" / "templates" / "commands"
        results: list[InstalledSkillFile] = []
        for spec in COMMAND_SPECS:
            source_file = source_dir / spec.source_name
            if source_file.exists():
                body = source_file.read_text(encoding="utf-8").rstrip()
            else:
                body = render_template(spec.template_name).rstrip()

            skill_dir = skills_dir / spec.skill_name
            ensure_directory(skill_dir)
            destination = skill_dir / "SKILL.md"
            content = render_template(
                "agent-files/skill-wrapper.md.j2",
                skill_name=spec.skill_name,
                description=spec.description,
                command_name=spec.command_name,
                source_path=f".specify/templates/commands/{spec.source_name}",
                body=body,
            )

            changed = True
            if destination.exists() and not overwrite:
                changed = False
            else:
                destination.write_text(content, encoding="utf-8")

            results.append(InstalledSkillFile(spec.skill_name, destination, changed))

        return results

    @staticmethod
    def _resolve_agent(ai_assistant: str) -> AgentConfig:
        if ai_assistant not in AGENT_CONFIGS:
            raise ValueError(f"unsupported ai assistant: {ai_assistant}")
        return AGENT_CONFIGS[ai_assistant]
