"""Project bootstrap flow."""

from __future__ import annotations

import subprocess
from pathlib import Path

import typer
from rich.console import Console

from speckit_for_projects.foundations.app import AGENT_CONFIGS
from speckit_for_projects.foundations.generation import render_to_path
from speckit_for_projects.foundations.scaffolding import ensure_directory
from speckit_for_projects.services.agent_skill_installer import AgentSkillInstaller
from speckit_for_projects.services.agent_template_installer import AgentTemplateInstaller

MANAGED_TEMPLATES = {
    Path(".specify/glossary.md"): "project/glossary.md.j2",
    Path(".specify/conventions/README.md"): "project/conventions-readme.md.j2",
    Path(".specify/project/tech-stack.md"): "project/tech-stack.md.j2",
    Path(".specify/project/domain-map.md"): "project/domain-map.md.j2",
    Path(".specify/project/coding-rules.md"): "project/coding-rules.md.j2",
    Path(".specify/project/architecture-principles.md"): (
        "project/architecture-principles.md.j2"
    ),
    Path(".specify/templates/commands/brief.md"): "commands/brief.md.j2",
    Path(".specify/templates/commands/analyze.md"): "commands/analyze.md.j2",
    Path(".specify/templates/commands/clarify.md"): "commands/clarify.md.j2",
    Path(".specify/templates/commands/common-design.md"): "commands/common-design.md.j2",
    Path(".specify/templates/commands/design.md"): "commands/design.md.j2",
    Path(".specify/templates/commands/debug.md"): "commands/debug.md.j2",
    Path(".specify/templates/commands/tasks.md"): "commands/tasks.md.j2",
    Path(".specify/templates/commands/implement.md"): "commands/implement.md.j2",
    Path(".specify/templates/commands/reflect.md"): "commands/reflect.md.j2",
    Path(".specify/templates/artifacts/brief.md"): "artifacts/brief.md.j2",
    Path(".specify/templates/artifacts/design/overview.md"): "artifacts/design/overview.md.j2",
    Path(".specify/templates/artifacts/design/ui-storybook/README.md"): (
        "artifacts/design/ui-storybook/README.md.j2"
    ),
    Path(".specify/templates/artifacts/design/ui-storybook/package.json"): (
        "artifacts/design/ui-storybook/package.json.j2"
    ),
    Path(".specify/templates/artifacts/design/ui-fields.yaml"): (
        "artifacts/design/ui-fields.yaml.j2"
    ),
    Path(".specify/templates/artifacts/design/ui-storybook/.storybook/main.ts"): (
        "artifacts/design/ui-storybook/.storybook/main.ts.j2"
    ),
    Path(".specify/templates/artifacts/design/ui-storybook/.storybook/preview.ts"): (
        "artifacts/design/ui-storybook/.storybook/preview.ts.j2"
    ),
    Path(
        ".specify/templates/artifacts/design/ui-storybook/.storybook/preview.css"
    ): ("artifacts/design/ui-storybook/.storybook/preview.css.j2"),
    Path(
        ".specify/templates/artifacts/design/ui-storybook/stories/"
        "SCR-001-example.stories.js"
    ): (
        "artifacts/design/ui-storybook/stories/SCR-001-example.stories.js.j2"
    ),
    Path(
        ".specify/templates/artifacts/design/ui-storybook/components/"
        "SCR-001-example.html"
    ): (
        "artifacts/design/ui-storybook/components/SCR-001-example.html.j2"
    ),
    Path(".specify/templates/artifacts/design/sequence-flows/core-flow.md"): (
        "artifacts/design/sequence-flows/core-flow.md.j2"
    ),
    Path(".specify/templates/artifacts/design/batch-design.md"): (
        "artifacts/design/batch-design.md.j2"
    ),
    Path(".specify/templates/artifacts/design/common-design-refs.yaml"): (
        "artifacts/design/common-design-refs.yaml.j2"
    ),
    Path(".specify/templates/artifacts/design/test-design.md"): (
        "artifacts/design/test-design.md.j2"
    ),
    Path(".specify/templates/artifacts/design/test-plan.md"): (
        "artifacts/design/test-plan.md.j2"
    ),
    Path(".specify/templates/artifacts/design/traceability.yaml"): (
        "artifacts/design/traceability.yaml.j2"
    ),
    Path(".specify/templates/artifacts/design/tasks.md"): (
        "artifacts/design/tasks.md.j2"
    ),
    Path(".specify/templates/artifacts/common_design/api.md"): (
        "artifacts/common_design/api.md.j2"
    ),
    Path(".specify/templates/artifacts/common_design/data.md"): (
        "artifacts/common_design/data.md.j2"
    ),
    Path(".specify/templates/artifacts/common_design/module.md"): (
        "artifacts/common_design/module.md.j2"
    ),
    Path(".specify/templates/artifacts/common_design/ui-screen-catalog.md"): (
        "artifacts/common_design/ui-screen-catalog.md.j2"
    ),
    Path(".specify/templates/artifacts/common_design/ui-navigation-rules.md"): (
        "artifacts/common_design/ui-navigation-rules.md.j2"
    ),
}

PROJECT_DESIGN_SYSTEM_TEMPLATES = {
    Path(".specify/project/design-system.md"): "project/design-system.md.j2",
    Path(".specify/project/ui-storybook/README.md"): "project/ui-storybook/README.md.j2",
    Path(".specify/project/ui-storybook/package.json"): "project/ui-storybook/package.json.j2",
    Path(".specify/project/ui-storybook/.storybook/main.ts"): (
        "project/ui-storybook/.storybook/main.ts.j2"
    ),
    Path(".specify/project/ui-storybook/.storybook/preview.ts"): (
        "project/ui-storybook/.storybook/preview.ts.j2"
    ),
    Path(".specify/project/ui-storybook/.storybook/preview.css"): (
        "project/ui-storybook/.storybook/preview.css.j2"
    ),
    Path(".specify/project/ui-storybook/stories/atoms/Button.stories.js"): (
        "project/ui-storybook/stories/atoms/Button.stories.js.j2"
    ),
    Path(".specify/project/ui-storybook/stories/molecules/FieldWithHint.stories.js"): (
        "project/ui-storybook/stories/molecules/FieldWithHint.stories.js.j2"
    ),
    Path(".specify/project/ui-storybook/stories/organisms/TaskList.stories.js"): (
        "project/ui-storybook/stories/organisms/TaskList.stories.js.j2"
    ),
    Path(".specify/project/ui-storybook/stories/templates/TaskInboxTemplate.stories.js"): (
        "project/ui-storybook/stories/templates/TaskInboxTemplate.stories.js.j2"
    ),
    Path(".specify/project/ui-storybook/stories/pages/TaskInboxPage.stories.js"): (
        "project/ui-storybook/stories/pages/TaskInboxPage.stories.js.j2"
    ),
    Path(".specify/project/ui-storybook/components/atoms/Button.html"): (
        "project/ui-storybook/components/atoms/Button.html.j2"
    ),
    Path(".specify/project/ui-storybook/components/molecules/FieldWithHint.html"): (
        "project/ui-storybook/components/molecules/FieldWithHint.html.j2"
    ),
    Path(".specify/project/ui-storybook/components/organisms/TaskList.html"): (
        "project/ui-storybook/components/organisms/TaskList.html.j2"
    ),
    Path(".specify/project/ui-storybook/components/templates/TaskInboxTemplate.html"): (
        "project/ui-storybook/components/templates/TaskInboxTemplate.html.j2"
    ),
    Path(".specify/project/ui-storybook/components/pages/TaskInboxPage.html"): (
        "project/ui-storybook/components/pages/TaskInboxPage.html.j2"
    ),
}


def resolve_target_directory(current_dir: Path, project_name: str | None, here: bool) -> Path:
    """Resolve the init target directory from CLI input."""
    if here and project_name not in (None, "."):
        raise typer.BadParameter("cannot combine project_name with --here")
    if here or project_name in (None, "."):
        return current_dir
    assert project_name is not None
    return current_dir / project_name


class ProjectInitializer:
    """Create shared scaffold and optional agent command files."""

    def __init__(self, console: Console, debug: bool) -> None:
        self.console = console
        self.debug = debug

    def initialize(
        self,
        *,
        target_dir: Path,
        ai_assistant: str | None,
        ai_commands_dir: str | None,
        ai_skills: bool,
        project_design_system: bool,
        no_git: bool,
        force: bool,
    ) -> None:
        self._validate_ai_options(ai_assistant, ai_commands_dir, ai_skills)
        ensure_directory(target_dir)
        ensure_directory(target_dir / "briefs")
        ensure_directory(target_dir / "designs")
        ensure_directory(target_dir / "designs" / "common_design" / "api")
        ensure_directory(target_dir / "designs" / "common_design" / "data")
        ensure_directory(target_dir / "designs" / "common_design" / "module")
        ensure_directory(target_dir / "designs" / "common_design" / "ui")
        ensure_directory(target_dir / "designs" / "specific_design")

        managed_templates = dict(MANAGED_TEMPLATES)
        if project_design_system:
            managed_templates.update(PROJECT_DESIGN_SYSTEM_TEMPLATES)

        changes = []
        for relative_path, template_name in managed_templates.items():
            write_result = render_to_path(
                target_dir / relative_path,
                template_name,
                overwrite=force,
            )
            changes.append(write_result)

        if ai_assistant is not None:
            installer = AgentTemplateInstaller(project_dir=target_dir)
            installer_results = installer.install(
                ai_assistant=ai_assistant,
                ai_commands_dir=ai_commands_dir,
                overwrite=force,
            )
            for installed_file in installer_results:
                state = "updated" if installed_file.changed else "kept"
                self.console.print(f"{state}: {installed_file.path.relative_to(target_dir)}")
            if ai_skills:
                skill_installer = AgentSkillInstaller(project_dir=target_dir)
                skill_results = skill_installer.install(ai_assistant=ai_assistant, overwrite=force)
                for installed_skill in skill_results:
                    state = "updated" if installed_skill.changed else "kept"
                    self.console.print(f"{state}: {installed_skill.path.relative_to(target_dir)}")
            if ai_assistant == "codex":
                self.console.print(_codex_usage_note(ai_skills))

        if not no_git:
            self._init_git(target_dir)

        changed_count = sum(1 for item in changes if item.changed)
        kept_count = len(changes) - changed_count
        self.console.print(
            f"Initialized {target_dir} with {changed_count} managed files written "
            f"and {kept_count} kept."
        )

    def _validate_ai_options(
        self, ai_assistant: str | None, ai_commands_dir: str | None, ai_skills: bool
    ) -> None:
        if ai_assistant is None:
            if ai_commands_dir is not None:
                raise typer.BadParameter("--ai-commands-dir requires --ai generic")
            if ai_skills:
                raise typer.BadParameter("--ai-skills requires --ai")
            return
        if ai_assistant not in AGENT_CONFIGS:
            raise typer.BadParameter(f"unsupported ai assistant: {ai_assistant}")
        if ai_assistant == "generic" and ai_commands_dir is None:
            raise typer.BadParameter("--ai-commands-dir is required for --ai generic")
        if ai_assistant != "generic" and ai_commands_dir is not None:
            raise typer.BadParameter("--ai-commands-dir can only be used with --ai generic")

    def _init_git(self, target_dir: Path) -> None:
        if (target_dir / ".git").exists():
            return
        try:
            result = subprocess.run(
                ["git", "init"],
                cwd=target_dir,
                capture_output=True,
                text=True,
                check=False,
            )
        except FileNotFoundError:
            if self.debug:
                self.console.print(
                    "[yellow]Debug:[/yellow] git executable not found; skipping init."
                )
            return
        if result.returncode != 0 and self.debug:
            self.console.print(f"[yellow]Debug:[/yellow] git init skipped: {result.stderr.strip()}")


def _codex_usage_note(ai_skills: bool) -> str:
    """Explain how generated prompts are used in Codex CLI."""
    if ai_skills:
        return (
            "note: Codex does not register custom /sdd.* slash commands. "
            "Use `.codex/prompts/*.md` as saved prompts, or restart Codex and ask it to use "
            "`speckit-for-projects-analyze`, `speckit-for-projects-brief`, "
            "`speckit-for-projects-clarify`, "
            "`speckit-for-projects-common-design`, "
            "`speckit-for-projects-design`, `speckit-for-projects-debug`, "
            "`speckit-for-projects-tasks`, `speckit-for-projects-implement`, "
            "or `speckit-for-projects-reflect`."
        )
    return (
        "note: Codex does not register custom /sdd.* slash commands. "
        "Use `.codex/prompts/*.md` as saved prompts, or re-run `sdd init --ai codex --ai-skills` "
        "to install Codex-discoverable skills."
    )
