from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from speckit_for_projects.cli import app

runner = CliRunner()
EXPECTED_ROOT = Path(__file__).resolve().parent / "expected"


def _assert_matches(actual: Path, expected: Path) -> None:
    assert actual.read_text(encoding="utf-8") == expected.read_text(encoding="utf-8")


def test_project_templates_match_golden_files():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--here", "--no-git"])
        assert result.exit_code == 0, result.stdout

        _assert_matches(
            Path(".specify/project/tech-stack.md"),
            EXPECTED_ROOT / "shared" / "project" / "tech-stack.md",
        )
        _assert_matches(
            Path(".specify/project/domain-map.md"),
            EXPECTED_ROOT / "shared" / "project" / "domain-map.md",
        )
        _assert_matches(
            Path(".specify/project/coding-rules.md"),
            EXPECTED_ROOT / "shared" / "project" / "coding-rules.md",
        )
        _assert_matches(
            Path(".specify/project/architecture-principles.md"),
            EXPECTED_ROOT / "shared" / "project" / "architecture-principles.md",
        )


def test_project_design_system_templates_match_golden_files():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--here", "--project-design-system", "--no-git"])
        assert result.exit_code == 0, result.stdout

        _assert_matches(
            Path(".specify/project/design-system.md"),
            EXPECTED_ROOT / "shared" / "project" / "design-system.md",
        )
        _assert_matches(
            Path(".specify/project/ui-storybook/README.md"),
            EXPECTED_ROOT / "shared" / "project" / "ui-storybook" / "README.md",
        )


def test_command_templates_match_golden_files():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--here", "--no-git"])
        assert result.exit_code == 0, result.stdout

        _assert_matches(
            Path(".specify/templates/commands/analyze.md"),
            EXPECTED_ROOT / "shared" / "commands" / "analyze.md",
        )
        _assert_matches(
            Path(".specify/templates/commands/brief.md"),
            EXPECTED_ROOT / "shared" / "commands" / "brief.md",
        )
        _assert_matches(
            Path(".specify/templates/commands/clarify.md"),
            EXPECTED_ROOT / "shared" / "commands" / "clarify.md",
        )
        _assert_matches(
            Path(".specify/templates/commands/common-design.md"),
            EXPECTED_ROOT / "shared" / "commands" / "common-design.md",
        )
        _assert_matches(
            Path(".specify/templates/commands/design.md"),
            EXPECTED_ROOT / "shared" / "commands" / "design.md",
        )
        _assert_matches(
            Path(".specify/templates/commands/tasks.md"),
            EXPECTED_ROOT / "shared" / "commands" / "tasks.md",
        )
        _assert_matches(
            Path(".specify/templates/commands/implement.md"),
            EXPECTED_ROOT / "shared" / "commands" / "implement.md",
        )


def test_codex_agent_files_match_golden_files():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--here", "--ai", "codex", "--no-git"])
        assert result.exit_code == 0, result.stdout

        _assert_matches(
            Path(".codex/prompts/sdd.analyze.md"),
            EXPECTED_ROOT / "agents" / "codex" / "sdd.analyze.md",
        )
        _assert_matches(
            Path(".codex/prompts/sdd.brief.md"),
            EXPECTED_ROOT / "agents" / "codex" / "sdd.brief.md",
        )
        _assert_matches(
            Path(".codex/prompts/sdd.clarify.md"),
            EXPECTED_ROOT / "agents" / "codex" / "sdd.clarify.md",
        )
        _assert_matches(
            Path(".codex/prompts/sdd.common-design.md"),
            EXPECTED_ROOT / "agents" / "codex" / "sdd.common-design.md",
        )
        _assert_matches(
            Path(".codex/prompts/sdd.design.md"),
            EXPECTED_ROOT / "agents" / "codex" / "sdd.design.md",
        )
        _assert_matches(
            Path(".codex/prompts/sdd.tasks.md"),
            EXPECTED_ROOT / "agents" / "codex" / "sdd.tasks.md",
        )
        _assert_matches(
            Path(".codex/prompts/sdd.implement.md"),
            EXPECTED_ROOT / "agents" / "codex" / "sdd.implement.md",
        )


def test_generic_agent_files_match_golden_files():
    with runner.isolated_filesystem():
        result = runner.invoke(
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
        assert result.exit_code == 0, result.stdout

        _assert_matches(
            Path(".myagent/commands/sdd.analyze.md"),
            EXPECTED_ROOT / "agents" / "generic" / "sdd.analyze.md",
        )
        _assert_matches(
            Path(".myagent/commands/sdd.brief.md"),
            EXPECTED_ROOT / "agents" / "generic" / "sdd.brief.md",
        )
        _assert_matches(
            Path(".myagent/commands/sdd.clarify.md"),
            EXPECTED_ROOT / "agents" / "generic" / "sdd.clarify.md",
        )
        _assert_matches(
            Path(".myagent/commands/sdd.common-design.md"),
            EXPECTED_ROOT / "agents" / "generic" / "sdd.common-design.md",
        )
        _assert_matches(
            Path(".myagent/commands/sdd.design.md"),
            EXPECTED_ROOT / "agents" / "generic" / "sdd.design.md",
        )
        _assert_matches(
            Path(".myagent/commands/sdd.tasks.md"),
            EXPECTED_ROOT / "agents" / "generic" / "sdd.tasks.md",
        )
        _assert_matches(
            Path(".myagent/commands/sdd.implement.md"),
            EXPECTED_ROOT / "agents" / "generic" / "sdd.implement.md",
        )


def test_claude_agent_files_use_frontmatter_wrapper():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--here", "--ai", "claude", "--no-git"])
        assert result.exit_code == 0, result.stdout

        _assert_matches(
            Path(".claude/commands/sdd.analyze.md"),
            EXPECTED_ROOT / "agents" / "claude" / "sdd.analyze.md",
        )
        _assert_matches(
            Path(".claude/commands/sdd.brief.md"),
            EXPECTED_ROOT / "agents" / "claude" / "sdd.brief.md",
        )
        _assert_matches(
            Path(".claude/commands/sdd.clarify.md"),
            EXPECTED_ROOT / "agents" / "claude" / "sdd.clarify.md",
        )


def test_codex_skill_files_match_golden_files():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--here", "--ai", "codex", "--ai-skills", "--no-git"])
        assert result.exit_code == 0, result.stdout

        _assert_matches(
            Path(".agents/skills/speckit-for-projects-analyze/SKILL.md"),
            EXPECTED_ROOT / "skills" / "speckit-for-projects-analyze" / "SKILL.md",
        )
        _assert_matches(
            Path(".agents/skills/speckit-for-projects-brief/SKILL.md"),
            EXPECTED_ROOT / "skills" / "speckit-for-projects-brief" / "SKILL.md",
        )
        _assert_matches(
            Path(".agents/skills/speckit-for-projects-clarify/SKILL.md"),
            EXPECTED_ROOT / "skills" / "speckit-for-projects-clarify" / "SKILL.md",
        )
        _assert_matches(
            Path(".agents/skills/speckit-for-projects-common-design/SKILL.md"),
            EXPECTED_ROOT / "skills" / "speckit-for-projects-common-design" / "SKILL.md",
        )
        _assert_matches(
            Path(".agents/skills/speckit-for-projects-design/SKILL.md"),
            EXPECTED_ROOT / "skills" / "speckit-for-projects-design" / "SKILL.md",
        )
        _assert_matches(
            Path(".agents/skills/speckit-for-projects-tasks/SKILL.md"),
            EXPECTED_ROOT / "skills" / "speckit-for-projects-tasks" / "SKILL.md",
        )
        _assert_matches(
            Path(".agents/skills/speckit-for-projects-implement/SKILL.md"),
            EXPECTED_ROOT / "skills" / "speckit-for-projects-implement" / "SKILL.md",
        )
