from __future__ import annotations

import os
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def _run_sdd(tmp_path: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", "--project", str(ROOT), "sdd", *args],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        check=False,
    )


def _tool_env(base_dir: Path) -> dict[str, str]:
    env = os.environ.copy()
    env["XDG_DATA_HOME"] = str(base_dir / "data")
    env["XDG_BIN_HOME"] = str(base_dir / "bin")
    env["XDG_CACHE_HOME"] = str(base_dir / "cache")
    return env


def _create_valid_bundle(project_dir: Path, design_id: str) -> Path:
    bundle_dir = project_dir / "designs" / "specific_design" / design_id
    (bundle_dir / "ui-storybook" / ".storybook").mkdir(parents=True)
    (bundle_dir / "ui-storybook" / "stories").mkdir(parents=True)
    (bundle_dir / "ui-storybook" / "components").mkdir(parents=True)
    (bundle_dir / "sequence-flows").mkdir(parents=True)

    for relative in [
        "overview.md",
        "ui-storybook/README.md",
        "ui-storybook/package.json",
        "ui-fields.yaml",
        "ui-storybook/.storybook/main.ts",
        "ui-storybook/.storybook/preview.ts",
        "ui-storybook/.storybook/preview.css",
        "ui-storybook/stories/SCR-001-example.stories.js",
        "ui-storybook/components/SCR-001-example.html",
        "sequence-flows/core-flow.md",
        "batch-design.md",
        "test-design.md",
        "test-plan.md",
    ]:
        (bundle_dir / relative).write_text("placeholder\n", encoding="utf-8")

    (project_dir / "designs" / "common_design" / "api").mkdir(parents=True, exist_ok=True)
    (project_dir / "designs" / "common_design" / "api" / "CD-API-001-shared-search.md").write_text(
        "# Shared API\n",
        encoding="utf-8",
    )
    (project_dir / "briefs").mkdir(parents=True, exist_ok=True)
    (project_dir / "briefs" / f"{design_id}.md").write_text(
        "# Sample\n\n## Common Design References\n- CD-API-001\n\n## Requirements\n"
        "### REQ-001 Example\n- priority: must\n",
        encoding="utf-8",
    )
    (bundle_dir / "tasks.md").write_text(
        "# Tasks\n\n## Tasks\n### TASK-001 Example\n- requirement_ids:\n  - REQ-001\n"
        "- artifact_refs:\n  - overview.md\n- common_design_refs:\n  - CD-API-001\n",
        encoding="utf-8",
    )
    (bundle_dir / "common-design-refs.yaml").write_text(
        "brief_id: sample\ndesign_id: sample\ncommon_design_refs:\n"
        "  - ref_id: CD-API-001\n    kind: api\n    usage: consume\n",
        encoding="utf-8",
    )
    (bundle_dir / "traceability.yaml").write_text(
        "brief_id: sample\ndesign_id: sample\nrequirements:\n"
        "  - requirement_id: REQ-001\n    primary_artifact: overview.md\n"
        "    related_artifacts: []\n    common_design_refs:\n      - CD-API-001\n",
        encoding="utf-8",
    )
    return bundle_dir


def test_e2e_init_and_check_with_generic_agent(tmp_path: Path) -> None:
    init_result = _run_sdd(
        tmp_path,
        "init",
        "--here",
        "--ai",
        "generic",
        "--ai-commands-dir",
        ".myagent/commands",
        "--no-git",
    )
    assert init_result.returncode == 0, init_result.stdout + init_result.stderr

    check_result = _run_sdd(
        tmp_path,
        "check",
        "--ai",
        "generic",
        "--ai-commands-dir",
        ".myagent/commands",
    )
    assert check_result.returncode == 0, check_result.stdout + check_result.stderr

    assert (tmp_path / ".specify" / "templates" / "commands" / "brief.md").exists()
    assert (tmp_path / ".specify" / "templates" / "commands" / "analyze.md").exists()
    assert (tmp_path / ".specify" / "templates" / "commands" / "common-design.md").exists()
    assert (
        tmp_path / ".specify" / "templates" / "artifacts" / "design" / "traceability.yaml"
    ).exists()
    assert (
        tmp_path
        / ".specify"
        / "templates"
        / "artifacts"
        / "design"
        / "common-design-refs.yaml"
    ).exists()
    assert (
        tmp_path
        / ".specify"
        / "templates"
        / "artifacts"
        / "common_design"
        / "ui-screen-catalog.md"
    ).exists()
    assert (tmp_path / ".myagent" / "commands" / "sdd.analyze.md").exists()
    assert (tmp_path / ".myagent" / "commands" / "sdd.common-design.md").exists()
    assert (tmp_path / ".myagent" / "commands" / "sdd.design.md").exists()
    assert (tmp_path / ".myagent" / "commands" / "sdd.implement.md").exists()
    assert (tmp_path / "briefs").is_dir()
    assert (tmp_path / "designs").is_dir()
    assert (tmp_path / "designs" / "common_design" / "api").is_dir()
    assert (tmp_path / "designs" / "common_design" / "ui").is_dir()
    assert (tmp_path / "designs" / "specific_design").is_dir()


def test_e2e_init_with_codex_skills(tmp_path: Path) -> None:
    init_result = _run_sdd(tmp_path, "init", "--here", "--ai", "codex", "--ai-skills", "--no-git")
    assert init_result.returncode == 0, init_result.stdout + init_result.stderr

    check_result = _run_sdd(tmp_path, "check", "--ai", "codex")
    assert check_result.returncode in {0, 1}, check_result.stdout + check_result.stderr

    assert (tmp_path / ".codex" / "prompts" / "sdd.analyze.md").exists()
    assert (tmp_path / ".codex" / "prompts" / "sdd.common-design.md").exists()
    assert (tmp_path / ".codex" / "prompts" / "sdd.design.md").exists()
    assert (
        tmp_path / ".agents" / "skills" / "speckit-for-projects-analyze" / "SKILL.md"
    ).exists()
    assert (tmp_path / ".agents" / "skills" / "speckit-for-projects-brief" / "SKILL.md").exists()
    assert (
        tmp_path / ".agents" / "skills" / "speckit-for-projects-common-design" / "SKILL.md"
    ).exists()
    assert (tmp_path / ".agents" / "skills" / "speckit-for-projects-design" / "SKILL.md").exists()
    assert (tmp_path / ".agents" / "skills" / "speckit-for-projects-tasks" / "SKILL.md").exists()
    assert (
        tmp_path / ".agents" / "skills" / "speckit-for-projects-implement" / "SKILL.md"
    ).exists()


def test_e2e_init_with_kiro_alias_skills(tmp_path: Path) -> None:
    init_result = _run_sdd(tmp_path, "init", "--here", "--ai", "kiro", "--ai-skills", "--no-git")
    assert init_result.returncode == 0, init_result.stdout + init_result.stderr

    check_result = _run_sdd(tmp_path, "check", "--ai", "kiro")
    assert check_result.returncode in {0, 1}, check_result.stdout + check_result.stderr

    assert (tmp_path / ".kiro" / "prompts" / "sdd.analyze.md").exists()
    assert (tmp_path / ".kiro" / "prompts" / "sdd.common-design.md").exists()
    assert (tmp_path / ".kiro" / "prompts" / "sdd.design.md").exists()
    assert (tmp_path / ".kiro" / "skills" / "speckit-for-projects-analyze" / "SKILL.md").exists()
    assert (tmp_path / ".kiro" / "skills" / "speckit-for-projects-brief" / "SKILL.md").exists()
    assert (
        tmp_path / ".kiro" / "skills" / "speckit-for-projects-common-design" / "SKILL.md"
    ).exists()
    assert (tmp_path / ".kiro" / "skills" / "speckit-for-projects-design" / "SKILL.md").exists()
    assert (tmp_path / ".kiro" / "skills" / "speckit-for-projects-tasks" / "SKILL.md").exists()
    assert (tmp_path / ".kiro" / "skills" / "speckit-for-projects-implement" / "SKILL.md").exists()


def test_e2e_force_rerun_overwrites_managed_files(tmp_path: Path) -> None:
    first = _run_sdd(tmp_path, "init", "--here", "--ai", "codex", "--ai-skills", "--no-git")
    assert first.returncode == 0, first.stdout + first.stderr

    tech_stack = tmp_path / ".specify" / "project" / "tech-stack.md"
    skill_file = tmp_path / ".agents" / "skills" / "speckit-for-projects-brief" / "SKILL.md"
    tech_stack.write_text("custom content\n", encoding="utf-8")
    skill_file.write_text("custom skill\n", encoding="utf-8")

    second = _run_sdd(tmp_path, "init", "--here", "--ai", "codex", "--ai-skills", "--no-git")
    assert second.returncode == 0, second.stdout + second.stderr
    assert tech_stack.read_text(encoding="utf-8") == "custom content\n"
    assert skill_file.read_text(encoding="utf-8") == "custom skill\n"

    third = _run_sdd(
        tmp_path,
        "init",
        "--here",
        "--ai",
        "codex",
        "--ai-skills",
        "--no-git",
        "--force",
    )
    assert third.returncode == 0, third.stdout + third.stderr
    assert "Document the canonical runtime" in tech_stack.read_text(encoding="utf-8")
    assert skill_file.read_text(encoding="utf-8") != "custom skill\n"


def test_e2e_analyze_valid_bundle(tmp_path: Path) -> None:
    init_result = _run_sdd(tmp_path, "init", "--here", "--no-git")
    assert init_result.returncode == 0, init_result.stdout + init_result.stderr

    _create_valid_bundle(tmp_path, "001-sample")

    analyze_result = _run_sdd(tmp_path, "analyze", "001-sample")

    assert analyze_result.returncode == 0, analyze_result.stdout + analyze_result.stderr
    assert "SpecKit for Projects analyze" in analyze_result.stdout
    assert "summary: inspected 1 bundle(s), success 1, failure 0" in analyze_result.stdout


def test_e2e_uv_tool_install_editable_exposes_sdd_command(tmp_path: Path) -> None:
    tool_home = tmp_path / "uv-tool-home"
    tool_home.mkdir()
    env = _tool_env(tool_home)

    install_result = subprocess.run(
        ["uv", "tool", "install", "--editable", str(ROOT)],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert install_result.returncode == 0, install_result.stdout + install_result.stderr

    list_result = subprocess.run(
        ["uv", "tool", "list"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert list_result.returncode == 0, list_result.stdout + list_result.stderr
    assert "speckit-for-projects v0.1.0" in list_result.stdout
    assert "- sdd" in list_result.stdout

    sdd_path = tool_home / "bin" / "sdd"
    help_result = subprocess.run(
        [str(sdd_path), "--help"],
        cwd=tmp_path,
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert help_result.returncode == 0, help_result.stdout + help_result.stderr
    assert "SpecKit for Projects scaffold setup and environment checks." in help_result.stdout
