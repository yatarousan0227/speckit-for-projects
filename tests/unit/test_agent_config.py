from __future__ import annotations

import pytest

from speckit_for_projects.foundations.app import AGENT_CONFIGS, resolve_ai_assistant


def test_codex_command_directory_resolution():
    directory = AGENT_CONFIGS["codex"].command_directory("/repo")
    assert directory == "/repo/.codex/prompts"


def test_generic_requires_commands_dir():
    with pytest.raises(ValueError):
        AGENT_CONFIGS["generic"].command_directory("/repo")


def test_generic_command_directory_resolution():
    directory = AGENT_CONFIGS["generic"].command_directory("/repo", ".myagent/commands")
    assert directory == ".myagent/commands"


def test_vibe_command_directory_resolution():
    directory = AGENT_CONFIGS["vibe"].command_directory("/repo")
    assert directory == "/repo/.vibe/prompts"


def test_kiro_alias_resolution():
    assert resolve_ai_assistant("kiro") == "kiro-cli"
    assert resolve_ai_assistant("kiro-cli") == "kiro-cli"
