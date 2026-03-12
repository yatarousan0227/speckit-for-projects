"""CLI entrypoint for speckit_for_projects."""

from speckit_for_projects.commands.check import register_check_command
from speckit_for_projects.commands.init import register_init_command
from speckit_for_projects.foundations.app import create_app

app = create_app()
register_init_command(app)
register_check_command(app)


def main() -> None:
    """Run the CLI application."""
    app()
