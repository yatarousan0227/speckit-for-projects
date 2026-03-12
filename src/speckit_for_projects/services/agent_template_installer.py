"""Install agent-specific command files."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from speckit_for_projects.foundations.app import AGENT_CONFIGS, AgentConfig
from speckit_for_projects.foundations.generation import render_template
from speckit_for_projects.foundations.scaffolding import ensure_directory


@dataclass(frozen=True)
class CommandSpec:
    """Shared metadata for each installed command and derived skill."""

    command_name: str
    template_name: str
    source_name: str
    description: str
    skill_name: str


COMMAND_SPECS = (
    CommandSpec(
        "sdd.analyze",
        "commands/analyze.md.j2",
        "analyze.md",
        "Inspect design bundles and report consistency issues without rewriting artifacts.",
        "speckit-for-projects-analyze",
    ),
    CommandSpec(
        "sdd.brief",
        "commands/brief.md.j2",
        "brief.md",
        "Create a brief under briefs/<brief-id>.md using 001-kebab-slug naming.",
        "speckit-for-projects-brief",
    ),
    CommandSpec(
        "sdd.common-design",
        "commands/common-design.md.j2",
        "common-design.md",
        "Create or update one shared design artifact under designs/common_design/.",
        "speckit-for-projects-common-design",
    ),
    CommandSpec(
        "sdd.design",
        "commands/design.md.j2",
        "design.md",
        "Create or overwrite one specific design bundle and review changes with git diff.",
        "speckit-for-projects-design",
    ),
    CommandSpec(
        "sdd.tasks",
        "commands/tasks.md.j2",
        "tasks.md",
        "Create or update tasks.md as a regenerable implementation ledger.",
        "speckit-for-projects-tasks",
    ),
    CommandSpec(
        "sdd.implement",
        "commands/implement.md.j2",
        "implement.md",
        "Implement selected TASK-xxx items and update execution state in tasks.md.",
        "speckit-for-projects-implement",
    ),
)

COMMAND_SPECS_BY_NAME = {spec.command_name: spec for spec in COMMAND_SPECS}
COMMAND_TEMPLATES = {spec.command_name: spec.template_name for spec in COMMAND_SPECS}


@dataclass(frozen=True)
class InstalledCommandFile:
    """One installed agent-specific command file."""

    command_name: str
    path: Path
    changed: bool


class AgentTemplateInstaller:
    """Install agent-specific command wrappers."""

    def __init__(self, project_dir: Path):
        self.project_dir = project_dir

    def install(
        self,
        ai_assistant: str,
        ai_commands_dir: str | None,
        *,
        overwrite: bool,
    ) -> list[InstalledCommandFile]:
        config = self._resolve_agent(ai_assistant)
        resolved_dir = Path(config.command_directory(str(self.project_dir), ai_commands_dir))
        output_dir = resolved_dir if resolved_dir.is_absolute() else self.project_dir / resolved_dir
        ensure_directory(output_dir)
        results: list[InstalledCommandFile] = []
        for spec in COMMAND_SPECS:
            destination = output_dir / f"{spec.command_name}.md"
            body = render_template(spec.template_name)
            wrapper_template = self._wrapper_template_name(config)
            content = render_template(
                wrapper_template,
                agent_name=config.name,
                command_name=spec.command_name,
                description=spec.description,
                skill_name=spec.skill_name,
                body=body.rstrip(),
            )
            changed = True
            if destination.exists() and not overwrite:
                changed = False
            else:
                destination.write_text(content, encoding="utf-8")
            results.append(
                InstalledCommandFile(
                    command_name=spec.command_name,
                    path=destination,
                    changed=changed,
                )
            )
        return results

    def _resolve_agent(self, ai_assistant: str) -> AgentConfig:
        if ai_assistant not in AGENT_CONFIGS:
            raise ValueError(f"unsupported ai assistant: {ai_assistant}")
        return AGENT_CONFIGS[ai_assistant]

    @staticmethod
    def _wrapper_template_name(config: AgentConfig) -> str:
        if config.key == "codex":
            return "agent-files/codex-prompt-wrapper.md.j2"
        if config.wrapper_style == "frontmatter":
            return "agent-files/frontmatter-wrapper.md.j2"
        return "agent-files/command-wrapper.md.j2"
