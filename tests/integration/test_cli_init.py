from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from speckit_for_projects.cli import app

runner = CliRunner()


def test_init_codex_creates_scaffold():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--here", "--ai", "codex", "--ai-skills", "--no-git"])

        assert result.exit_code == 0, result.stdout
        assert "Codex does not register custom /sdd.* slash commands" in result.stdout
        assert "speckit-for-projects-analyze" in result.stdout
        assert Path(".specify/project/tech-stack.md").exists()
        assert Path(".specify/project/domain-map.md").exists()
        assert Path(".specify/templates/commands/analyze.md").exists()
        assert Path(".specify/templates/commands/common-design.md").exists()
        assert Path(".specify/templates/commands/design.md").exists()
        assert Path(".specify/templates/artifacts/design/traceability.yaml").exists()
        assert Path(".specify/templates/artifacts/design/common-design-refs.yaml").exists()
        assert Path(".specify/templates/artifacts/common_design/api.md").exists()
        assert Path(".specify/templates/artifacts/common_design/ui-screen-catalog.md").exists()
        assert Path(".specify/templates/artifacts/common_design/ui-navigation-rules.md").exists()
        assert Path(
            ".specify/templates/artifacts/design/ui-storybook/.storybook/main.ts"
        ).exists()
        assert Path(
            ".specify/templates/artifacts/design/ui-storybook/.storybook/preview.ts"
        ).exists()
        assert Path(
            ".specify/templates/artifacts/design/ui-storybook/package.json"
        ).exists()
        assert Path(".codex/prompts/sdd.analyze.md").exists()
        assert Path(".codex/prompts/sdd.design.md").exists()
        assert Path(".codex/prompts/sdd.common-design.md").exists()
        assert Path(".codex/prompts/sdd.implement.md").exists()
        assert Path(".agents/skills/speckit-for-projects-analyze/SKILL.md").exists()
        assert Path(".agents/skills/speckit-for-projects-brief/SKILL.md").exists()
        assert Path(".agents/skills/speckit-for-projects-common-design/SKILL.md").exists()
        assert Path(".agents/skills/speckit-for-projects-design/SKILL.md").exists()
        assert Path(".agents/skills/speckit-for-projects-tasks/SKILL.md").exists()
        assert Path(".agents/skills/speckit-for-projects-implement/SKILL.md").exists()
        assert Path("briefs").is_dir()
        assert Path("designs").is_dir()
        assert Path("designs/common_design/api").is_dir()
        assert Path("designs/common_design/ui").is_dir()
        assert Path("designs/specific_design").is_dir()


def test_init_generic_writes_to_custom_commands_dir():
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
        assert Path(".myagent/commands/sdd.analyze.md").exists()
        assert Path(".myagent/commands/sdd.brief.md").exists()
        assert Path(".myagent/commands/sdd.common-design.md").exists()
        assert Path(".myagent/commands/sdd.design.md").exists()
        assert Path(".myagent/commands/sdd.tasks.md").exists()
        assert Path(".myagent/commands/sdd.implement.md").exists()


def test_init_rerun_keeps_then_overwrites_managed_files():
    with runner.isolated_filesystem():
        first = runner.invoke(app, ["init", "--here", "--ai", "codex", "--ai-skills", "--no-git"])
        assert first.exit_code == 0, first.stdout

        tech_stack = Path(".specify/project/tech-stack.md")
        skill_file = Path(".agents/skills/speckit-for-projects-brief/SKILL.md")
        tech_stack.write_text("custom content\n", encoding="utf-8")
        skill_file.write_text("custom skill\n", encoding="utf-8")

        second = runner.invoke(app, ["init", "--here", "--ai", "codex", "--ai-skills", "--no-git"])
        assert second.exit_code == 0, second.stdout
        assert tech_stack.read_text(encoding="utf-8") == "custom content\n"
        assert skill_file.read_text(encoding="utf-8") == "custom skill\n"

        third = runner.invoke(
            app,
            ["init", "--here", "--ai", "codex", "--ai-skills", "--no-git", "--force"],
        )
        assert third.exit_code == 0, third.stdout
        assert "Document the canonical runtime" in tech_stack.read_text(encoding="utf-8")
        assert "custom skill\n" != skill_file.read_text(encoding="utf-8")


def test_init_kiro_alias_creates_prompts_and_skills():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["init", "--here", "--ai", "kiro", "--ai-skills", "--no-git"])

        assert result.exit_code == 0, result.stdout
        assert Path(".kiro/prompts/sdd.analyze.md").exists()
        assert Path(".kiro/prompts/sdd.brief.md").exists()
        assert Path(".kiro/prompts/sdd.common-design.md").exists()
        assert Path(".kiro/prompts/sdd.design.md").exists()
        assert Path(".kiro/prompts/sdd.tasks.md").exists()
        assert Path(".kiro/prompts/sdd.implement.md").exists()
        assert Path(".kiro/skills/speckit-for-projects-analyze/SKILL.md").exists()
        assert Path(".kiro/skills/speckit-for-projects-brief/SKILL.md").exists()
        assert Path(".kiro/skills/speckit-for-projects-common-design/SKILL.md").exists()
        assert Path(".kiro/skills/speckit-for-projects-design/SKILL.md").exists()
        assert Path(".kiro/skills/speckit-for-projects-tasks/SKILL.md").exists()
        assert Path(".kiro/skills/speckit-for-projects-implement/SKILL.md").exists()
