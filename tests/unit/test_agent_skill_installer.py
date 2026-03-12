from __future__ import annotations

from pathlib import Path

from speckit_for_projects.foundations.app import AGENT_CONFIGS
from speckit_for_projects.services.agent_skill_installer import (
    AgentSkillInstaller,
    resolve_skills_directory,
)


def test_resolve_skills_directory_for_codex(tmp_path: Path):
    directory = resolve_skills_directory(tmp_path, AGENT_CONFIGS["codex"])

    assert directory == tmp_path / ".agents" / "skills"


def test_resolve_skills_directory_for_generic(tmp_path: Path):
    directory = resolve_skills_directory(tmp_path, AGENT_CONFIGS["generic"])

    assert directory == tmp_path / ".agents" / "skills"


def test_resolve_skills_directory_for_named_agent(tmp_path: Path):
    directory = resolve_skills_directory(tmp_path, AGENT_CONFIGS["claude"])

    assert directory == tmp_path / ".claude" / "skills"


def test_skill_installer_keeps_existing_skill_file(tmp_path: Path):
    source_dir = tmp_path / ".specify" / "templates" / "commands"
    source_dir.mkdir(parents=True)
    for name in (
        "analyze.md",
        "brief.md",
        "common-design.md",
        "design.md",
        "tasks.md",
        "implement.md",
    ):
        (source_dir / name).write_text(f"# {name}\n", encoding="utf-8")

    existing_skill = tmp_path / ".agents" / "skills" / "speckit-for-projects-brief" / "SKILL.md"
    existing_skill.parent.mkdir(parents=True)
    existing_skill.write_text("custom\n", encoding="utf-8")

    results = AgentSkillInstaller(project_dir=tmp_path).install("codex")

    assert existing_skill.read_text(encoding="utf-8") == "custom\n"
    assert any(
        result.skill_name == "speckit-for-projects-brief" and not result.changed
        for result in results
    )


def test_skill_installer_overwrites_existing_skill_file_with_force(tmp_path: Path):
    source_dir = tmp_path / ".specify" / "templates" / "commands"
    source_dir.mkdir(parents=True)
    for name in (
        "analyze.md",
        "brief.md",
        "common-design.md",
        "design.md",
        "tasks.md",
        "implement.md",
    ):
        (source_dir / name).write_text(f"# {name}\n", encoding="utf-8")

    existing_skill = tmp_path / ".agents" / "skills" / "speckit-for-projects-brief" / "SKILL.md"
    existing_skill.parent.mkdir(parents=True)
    existing_skill.write_text("custom\n", encoding="utf-8")

    results = AgentSkillInstaller(project_dir=tmp_path).install("codex", overwrite=True)

    assert existing_skill.read_text(encoding="utf-8") != "custom\n"
    assert any(
        result.skill_name == "speckit-for-projects-brief" and result.changed for result in results
    )


def test_skill_installer_includes_analyze_skill(tmp_path: Path):
    source_dir = tmp_path / ".specify" / "templates" / "commands"
    source_dir.mkdir(parents=True)
    for name in (
        "analyze.md",
        "brief.md",
        "common-design.md",
        "design.md",
        "tasks.md",
        "implement.md",
    ):
        (source_dir / name).write_text(f"# {name}\n", encoding="utf-8")

    results = AgentSkillInstaller(project_dir=tmp_path).install("codex", overwrite=True)

    analyze_skill = tmp_path / ".agents" / "skills" / "speckit-for-projects-analyze" / "SKILL.md"
    assert analyze_skill.exists()
    assert any(
        result.skill_name == "speckit-for-projects-analyze" and result.changed
        for result in results
    )
