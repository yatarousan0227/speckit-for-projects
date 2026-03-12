from __future__ import annotations

from pathlib import Path

from typer.testing import CliRunner

from speckit_for_projects.cli import app

runner = CliRunner()


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


def test_analyze_succeeds_for_design_id():
    with runner.isolated_filesystem():
        bundle_dir = _create_valid_bundle(Path.cwd(), "001-sample")

        result = runner.invoke(app, ["analyze", bundle_dir.name])

        assert result.exit_code == 0, result.stdout
        assert "success" in result.stdout
        assert "001-sample" in result.stdout


def test_analyze_accepts_bundle_path():
    with runner.isolated_filesystem():
        bundle_dir = _create_valid_bundle(Path.cwd(), "001-sample")

        result = runner.invoke(app, ["analyze", str(bundle_dir)])

        assert result.exit_code == 0, result.stdout
        assert "success" in result.stdout
        assert "designs/specific_design/001-sample" in result.stdout


def test_analyze_all_targets_every_bundle():
    with runner.isolated_filesystem():
        _create_valid_bundle(Path.cwd(), "001-sample")
        _create_valid_bundle(Path.cwd(), "002-sample")

        result = runner.invoke(app, ["analyze", "--all"])

        assert result.exit_code == 0, result.stdout
        assert "001-sample" in result.stdout
        assert "002-sample" in result.stdout
        assert "inspected 2 bundle(s)" in result.stdout


def test_analyze_reports_bundle_failures():
    with runner.isolated_filesystem():
        bundle_dir = _create_valid_bundle(Path.cwd(), "001-invalid")
        (bundle_dir / "tasks.md").unlink()
        (bundle_dir / "traceability.yaml").unlink()

        result = runner.invoke(app, ["analyze", bundle_dir.name])

        assert result.exit_code == 2, result.stdout
        assert "failure" in result.stdout
        assert "issue counts:" in result.stdout
        assert "missing_files: 2" in result.stdout
        assert "missing_requirements: 1" in result.stdout
        assert "uncovered_task_requirements: 1" in result.stdout
        assert "invalid_traceability_entries: 1" in result.stdout
        assert "missing_files (2)" in result.stdout
        assert "missing_requirements (1)" in result.stdout
        assert "uncovered_task_requirements (1)" in result.stdout
        assert "invalid_traceability_entries (1)" in result.stdout
        assert "tasks.md" in result.stdout
        assert "missing traceability file" in result.stdout


def test_analyze_all_lists_failure_bundles():
    with runner.isolated_filesystem():
        _create_valid_bundle(Path.cwd(), "001-valid")
        invalid_bundle = _create_valid_bundle(Path.cwd(), "002-invalid")
        (invalid_bundle / "common-design-refs.yaml").unlink()

        result = runner.invoke(app, ["analyze", "--all"])

        assert result.exit_code == 2, result.stdout
        assert "summary: inspected 2 bundle(s), success 1, failure 1" in result.stdout
        assert "failure bundles:" in result.stdout
        assert "designs/specific_design/002-invalid" in result.stdout


def test_analyze_rejects_target_and_all_together():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["analyze", "001-sample", "--all"])

        assert result.exit_code == 2


def test_analyze_requires_target_or_all():
    with runner.isolated_filesystem():
        result = runner.invoke(app, ["analyze"])

        assert result.exit_code == 2
