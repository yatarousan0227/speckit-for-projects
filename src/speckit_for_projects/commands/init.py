"""`sdd init` command."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from speckit_for_projects.foundations.app import AI_ASSISTANT_HELP, resolve_ai_assistant
from speckit_for_projects.services.project_initializer import ProjectInitializer, resolve_target_directory


def register_init_command(app: typer.Typer) -> None:
    """Register the init command on the Typer app."""

    @app.command("init")
    def init_command(
        project_name: str | None = typer.Argument(
            None,
            help="Project directory name. Omit when using --here or '.' for current directory.",
        ),
        ai_assistant: str | None = typer.Option(None, "--ai", help=AI_ASSISTANT_HELP),
        ai_commands_dir: str | None = typer.Option(
            None,
            "--ai-commands-dir",
            help="Directory for agent command files. Required with --ai generic.",
        ),
        ai_skills: bool = typer.Option(
            False,
            "--ai-skills",
            help="Install command templates as SKILL.md files for the selected agent.",
        ),
        no_git: bool = typer.Option(False, "--no-git", help="Skip git repository initialization."),
        here: bool = typer.Option(False, "--here", help="Initialize the current directory."),
        force: bool = typer.Option(
            False,
            "--force",
            help="Overwrite managed scaffold files on re-run.",
        ),
        debug: bool = typer.Option(False, "--debug", help="Show extra debug output."),
    ) -> None:
        console = Console()
        target = resolve_target_directory(Path.cwd(), project_name, here)
        initializer = ProjectInitializer(console=console, debug=debug)
        initializer.initialize(
            target_dir=target,
            ai_assistant=resolve_ai_assistant(ai_assistant),
            ai_commands_dir=ai_commands_dir,
            ai_skills=ai_skills,
            no_git=no_git,
            force=force,
        )
