"""Environment and scaffold checks."""

from __future__ import annotations

from pathlib import Path

from rich.console import Console
from rich.table import Table

from speckit_for_projects.foundations.app import AGENT_CONFIGS
from speckit_for_projects.services.agent_runtime import missing_runtime_message, runtime_available
from speckit_for_projects.services.agent_skill_installer import resolve_skills_directory
from speckit_for_projects.services.agent_template_installer import COMMAND_TEMPLATES
from speckit_for_projects.services.consistency_checker import missing_shared_paths


class EnvironmentChecker:
    """Check the shared scaffold and optional agent setup."""

    def __init__(self, console: Console, debug: bool) -> None:
        self.console = console
        self.debug = debug

    def run(
        self, project_dir: Path, ai_assistant: str | None, ai_commands_dir: str | None = None
    ) -> int:
        notes: list[str] = []
        warnings: list[str] = []
        failures: list[str] = []

        missing = missing_shared_paths(project_dir)
        failures.extend(str(item) for item in missing)

        if ai_assistant is not None:
            if ai_assistant not in AGENT_CONFIGS:
                failures.append(f"unsupported ai assistant: {ai_assistant}")
            else:
                config = AGENT_CONFIGS[ai_assistant]
                if config.requires_cli and not runtime_available(config):
                    warnings.append(missing_runtime_message(config))
                try:
                    resolved_dir = Path(config.command_directory(str(project_dir), ai_commands_dir))
                    if resolved_dir.is_absolute():
                        command_dir = resolved_dir
                    else:
                        command_dir = project_dir / resolved_dir
                except ValueError as exc:
                    failures.append(str(exc))
                    command_dir = None
                if command_dir is not None:
                    for command_name in COMMAND_TEMPLATES:
                        expected = command_dir / f"{command_name}.md"
                        if not expected.exists():
                            failures.append(_display_path(expected, project_dir))
                if ai_assistant == "codex":
                    notes.append(self._codex_note(project_dir))

        self._print_results(warnings, failures, notes)
        if failures:
            return 2
        if warnings:
            return 1
        return 0

    def _print_results(self, warnings: list[str], failures: list[str], notes: list[str]) -> None:
        table = Table(title="SpecKit for Projects check")
        table.add_column("Severity")
        table.add_column("Message")
        if not warnings and not failures:
            table.add_row("success", "shared scaffold and requested agent configuration look valid")
        for warning in warnings:
            table.add_row("warning", warning)
        for failure in failures:
            table.add_row("failure", failure)
        self.console.print(table)
        for note in notes:
            self.console.print(note)
        if self.debug and warnings:
            self.console.print("[yellow]Debug:[/yellow] warnings do not block scaffold usage.")

    def _codex_note(self, project_dir: Path) -> str:
        """Describe how Codex should use generated assets."""
        skills_dir = resolve_skills_directory(project_dir, AGENT_CONFIGS["codex"])
        skill_names = [
            "speckit-for-projects-analyze",
            "speckit-for-projects-brief",
            "speckit-for-projects-common-design",
            "speckit-for-projects-design",
            "speckit-for-projects-tasks",
            "speckit-for-projects-implement",
        ]
        if all((skills_dir / skill_name / "SKILL.md").exists() for skill_name in skill_names):
            return (
                "note: Codex treats `.codex/prompts/*.md` as saved prompts, not custom slash "
                "commands. Ask Codex to use `speckit-for-projects-analyze`, "
                "`speckit-for-projects-brief`, "
                "`speckit-for-projects-common-design`, `speckit-for-projects-design`, "
                "`speckit-for-projects-tasks`, or `speckit-for-projects-implement`, "
                "or open the saved prompt files directly."
            )
        return (
            "note: Codex treats `.codex/prompts/*.md` as saved prompts, not custom slash "
            "commands. Re-run `sdd init --ai codex --ai-skills` if you want Codex-discoverable "
            "skills in addition to the saved prompt files."
        )


def _display_path(path: Path, project_dir: Path) -> str:
    """Render a path relative to the project when possible."""
    try:
        return str(path.relative_to(project_dir))
    except ValueError:
        return str(path)
