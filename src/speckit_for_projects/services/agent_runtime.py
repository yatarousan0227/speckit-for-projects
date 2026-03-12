"""Agent runtime detection helpers."""

from __future__ import annotations

import shutil
from pathlib import Path

from speckit_for_projects.foundations.app import AgentConfig

CLAUDE_LOCAL_PATH = Path.home() / ".claude" / "local" / "claude"


def runtime_available(config: AgentConfig) -> bool:
    """Return whether the configured runtime is available locally."""
    if not config.requires_cli or config.cli_command is None:
        return True
    if config.key == "claude" and CLAUDE_LOCAL_PATH.is_file():
        return True
    if config.key == "kiro-cli":
        return shutil.which("kiro-cli") is not None or shutil.which("kiro") is not None
    return shutil.which(config.cli_command) is not None


def missing_runtime_message(config: AgentConfig) -> str:
    """Build a user-facing warning for a missing runtime."""
    if config.key == "kiro-cli":
        runtime_name = "kiro-cli or kiro"
    elif config.cli_command is not None:
        runtime_name = config.cli_command
    else:
        runtime_name = config.name

    message = f"runtime not found: {runtime_name}"
    if config.install_url is not None:
        return f"{message} (install: {config.install_url})"
    return message
