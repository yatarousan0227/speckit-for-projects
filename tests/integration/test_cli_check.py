from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from speckit_for_projects.cli import app

runner = CliRunner()


def test_check_fails_when_shared_scaffold_is_missing():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["check"])

        assert result.exit_code == 2
        assert "failure" in result.stdout


def test_check_succeeds_when_shared_scaffold_exists():
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init", "--here", "--no-git"])
        assert init_result.exit_code == 0, init_result.stdout

        result = runner.invoke(app, ["check"])

        assert result.exit_code == 0, result.stdout
        assert "success" in result.stdout


def test_check_fails_when_new_common_design_command_file_is_missing():
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init", "--here", "--no-git"])
        assert init_result.exit_code == 0, init_result.stdout

        Path(".specify/templates/commands/common-design.md").unlink()

        result = runner.invoke(app, ["check"])

        assert result.exit_code == 2, result.stdout


def test_check_warns_when_agent_runtime_is_missing(monkeypatch):
    monkeypatch.setattr("speckit_for_projects.services.agent_runtime.shutil.which", lambda _: None)
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init", "--here", "--ai", "codex", "--no-git"])
        assert init_result.exit_code == 0, init_result.stdout

        result = runner.invoke(app, ["check", "--ai", "codex"])

        assert result.exit_code == 1, result.stdout
        assert "runtime not found: codex" in result.stdout


def test_check_prints_codex_usage_note():
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init", "--here", "--ai", "codex", "--no-git"])
        assert init_result.exit_code == 0, init_result.stdout

        result = runner.invoke(app, ["check", "--ai", "codex"])

        assert result.exit_code in {0, 1}, result.stdout
        assert "saved prompts" in result.stdout
        assert "Codex-discoverable skills" in result.stdout


def test_check_accepts_kiro_alias(monkeypatch):
    monkeypatch.setattr(
        "speckit_for_projects.services.agent_runtime.shutil.which",
        lambda command: "/usr/bin/kiro" if command == "kiro" else None,
    )
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init", "--here", "--ai", "kiro", "--no-git"])
        assert init_result.exit_code == 0, init_result.stdout

        result = runner.invoke(app, ["check", "--ai", "kiro"])

        assert result.exit_code == 0, result.stdout


def test_check_uses_claude_local_runtime_fallback(monkeypatch, tmp_path):
    local_claude = tmp_path / "claude"
    local_claude.write_text("", encoding="utf-8")
    monkeypatch.setattr("speckit_for_projects.services.agent_runtime.CLAUDE_LOCAL_PATH", local_claude)
    monkeypatch.setattr("speckit_for_projects.services.agent_runtime.shutil.which", lambda _: None)
    with runner.isolated_filesystem():
        init_result = runner.invoke(app, ["init", "--here", "--ai", "claude", "--no-git"])
        assert init_result.exit_code == 0, init_result.stdout

        result = runner.invoke(app, ["check", "--ai", "claude"])

        assert result.exit_code == 0, result.stdout


def test_check_generic_requires_commands_dir():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["check", "--ai", "generic"])

        assert result.exit_code == 2


def test_check_generic_detects_missing_command_file():
    with runner.isolated_filesystem():
        init_result = runner.invoke(
            app,
            [
                "init",
                "--here",
                "--ai",
                "generic",
                "--ai-commands-dir",
                ".myagent/commands",
                "--no-git",
            ],
        )
        assert init_result.exit_code == 0, init_result.stdout

        Path(".myagent/commands/sdd.common-design.md").unlink()

        result = runner.invoke(
            app,
            ["check", "--ai", "generic", "--ai-commands-dir", ".myagent/commands"],
        )

        assert result.exit_code == 2, result.stdout
        assert ".myagent/commands/sdd.common-design.md" in result.stdout
