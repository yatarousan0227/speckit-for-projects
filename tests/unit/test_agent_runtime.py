from __future__ import annotations

from pathlib import Path

from speckit_for_projects.foundations.app import AGENT_CONFIGS
from speckit_for_projects.services import agent_runtime


def test_claude_runtime_uses_local_fallback(monkeypatch, tmp_path: Path):
    local_claude = tmp_path / "claude"
    local_claude.write_text("", encoding="utf-8")
    monkeypatch.setattr(agent_runtime, "CLAUDE_LOCAL_PATH", local_claude)
    monkeypatch.setattr(agent_runtime.shutil, "which", lambda _: None)

    assert agent_runtime.runtime_available(AGENT_CONFIGS["claude"]) is True


def test_kiro_runtime_accepts_kiro_binary(monkeypatch):
    monkeypatch.setattr(
        agent_runtime.shutil,
        "which",
        lambda command: "/usr/bin/kiro" if command == "kiro" else None,
    )

    assert agent_runtime.runtime_available(AGENT_CONFIGS["kiro-cli"]) is True


def test_missing_runtime_message_includes_install_url():
    message = agent_runtime.missing_runtime_message(AGENT_CONFIGS["codex"])

    assert "runtime not found: codex" in message
    assert "https://github.com/openai/codex" in message
