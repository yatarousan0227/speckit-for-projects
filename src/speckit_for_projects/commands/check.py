"""`sdd check` command."""

from __future__ import annotations

from pathlib import Path

import typer
from rich.console import Console

from speckit_for_projects.foundations.app import AI_ASSISTANT_HELP, resolve_ai_assistant
from speckit_for_projects.services.environment_checker import EnvironmentChecker


def register_check_command(app: typer.Typer) -> None:
    """Register the check command on the Typer app."""

    @app.command("check")
    def check_command(
        ai_assistant: str | None = typer.Option(None, "--ai", help=AI_ASSISTANT_HELP),
        ai_commands_dir: str | None = typer.Option(
            None,
            "--ai-commands-dir",
            help="Directory for agent command files. Required with --ai generic.",
        ),
        debug: bool = typer.Option(False, "--debug", help="Show extra debug output."),
    ) -> None:
        resolved_ai = resolve_ai_assistant(ai_assistant)
        _validate_check_options(resolved_ai, ai_commands_dir)
        console = Console()
        checker = EnvironmentChecker(console=console, debug=debug)
        exit_code = checker.run(
            project_dir=Path.cwd(),
            ai_assistant=resolved_ai,
            ai_commands_dir=ai_commands_dir,
        )
        raise typer.Exit(code=exit_code)


def _validate_check_options(ai_assistant: str | None, ai_commands_dir: str | None) -> None:
    """Validate option combinations for `sdd check`."""
    if ai_assistant is None:
        if ai_commands_dir is not None:
            raise typer.BadParameter("--ai-commands-dir requires --ai generic")
        return
    if ai_assistant == "generic" and ai_commands_dir is None:
        raise typer.BadParameter("--ai-commands-dir is required for --ai generic")
    if ai_assistant != "generic" and ai_commands_dir is not None:
        raise typer.BadParameter("--ai-commands-dir can only be used with --ai generic")
