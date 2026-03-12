from __future__ import annotations

from pathlib import Path

import pytest

from speckit_for_projects.domain.exceptions import DesignBundleValidationError
from speckit_for_projects.services.consistency_checker import (
    ensure_valid_design_bundle,
    missing_shared_paths,
    validate_design_bundle,
)


def _create_specific_bundle_files(bundle_dir: Path) -> None:
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
        "tasks.md",
        "common-design-refs.yaml",
    ]:
        (bundle_dir / relative).write_text("placeholder\n", encoding="utf-8")


def _create_common_design(project_dir: Path) -> None:
    common_dir = project_dir / "designs" / "common_design" / "api"
    common_dir.mkdir(parents=True)
    (common_dir / "CD-API-001-shared-search.md").write_text("# Shared API\n", encoding="utf-8")
    ui_dir = project_dir / "designs" / "common_design" / "ui"
    ui_dir.mkdir(parents=True)
    (ui_dir / "CD-UI-001-screen-catalog.md").write_text("# Shared UI Screen Catalog\n", encoding="utf-8")


def test_validate_design_bundle_detects_missing_requirement(tmp_path: Path):
    bundle_dir = tmp_path / "designs" / "specific_design" / "001-sample"
    brief_path = tmp_path / "briefs" / "001-sample.md"
    _create_bundle_files(bundle_dir, tmp_path)
    (bundle_dir / "tasks.md").write_text(
        "# Tasks\n\n## Tasks\n### TASK-001 Example\n- requirement_ids:\n  - REQ-999\n"
        "- artifact_refs:\n  - overview.md\n- common_design_refs:\n  - CD-API-001\n",
        encoding="utf-8",
    )
    (bundle_dir / "traceability.yaml").write_text(
        "brief_id: 001-sample\ndesign_id: 001-sample\nrequirements:\n"
        "  - requirement_id: REQ-999\n    primary_artifact: overview.md\n"
        "    related_artifacts: []\n    common_design_refs:\n      - CD-API-001\n",
        encoding="utf-8",
    )
    brief_path.parent.mkdir(parents=True)
    brief_path.write_text(
        "# Sample\n\n## Common Design References\n- CD-API-001\n\n## Requirements\n"
        "### REQ-001 Example\n- priority: must\n",
        encoding="utf-8",
    )

    result = validate_design_bundle(bundle_dir=bundle_dir, brief_path=brief_path)

    assert "unmapped requirement: REQ-001" in result.missing_requirements
    assert "requirement missing from tasks: REQ-001" in result.uncovered_task_requirements


def test_validate_design_bundle_accepts_ui_common_design_reference(tmp_path: Path):
    bundle_dir = tmp_path / "designs" / "specific_design" / "001-sample"
    brief_path = tmp_path / "briefs" / "001-sample.md"
    _create_specific_bundle_files(bundle_dir)
    _create_common_design(tmp_path)
    (bundle_dir / "common-design-refs.yaml").write_text(
        "brief_id: 001-sample\ndesign_id: 001-sample\ncommon_design_refs:\n"
        "  - ref_id: CD-UI-001\n    kind: ui\n    usage: consume\n",
        encoding="utf-8",
    )
    (bundle_dir / "traceability.yaml").write_text(
        "brief_id: 001-sample\ndesign_id: 001-sample\nrequirements:\n"
        "  - requirement_id: REQ-001\n    primary_artifact: overview.md\n"
        "    related_artifacts: []\n    common_design_refs:\n      - CD-UI-001\n",
        encoding="utf-8",
    )
    (bundle_dir / "tasks.md").write_text(
        "# Tasks\n\n## Tasks\n### TASK-001 Example\n- requirement_ids:\n  - REQ-001\n"
        "- artifact_refs:\n  - overview.md\n- common_design_refs:\n  - CD-UI-001\n",
        encoding="utf-8",
    )
    brief_path.parent.mkdir(parents=True)
    brief_path.write_text(
        "# Sample\n\n## Common Design References\n- CD-UI-001\n\n## Requirements\n"
        "### REQ-001 Example\n- priority: must\n",
        encoding="utf-8",
    )

    result = validate_design_bundle(bundle_dir=bundle_dir, brief_path=brief_path)

    assert result.invalid_common_design_entries == []


def test_missing_shared_paths_allows_optional_common_design_ui_directory(tmp_path: Path):
    required_dirs = [
        "briefs",
        "designs/common_design",
        "designs/common_design/api",
        "designs/common_design/data",
        "designs/common_design/module",
        "designs/specific_design",
        ".specify/project",
        ".specify/templates/commands",
        ".specify/templates/artifacts/design/ui-storybook/.storybook",
        ".specify/templates/artifacts/design/ui-storybook/stories",
        ".specify/templates/artifacts/design/ui-storybook/components",
        ".specify/templates/artifacts/design/sequence-flows",
        ".specify/templates/artifacts/common_design",
    ]
    for relative in required_dirs:
        (tmp_path / relative).mkdir(parents=True, exist_ok=True)

    required_files = [
        ".specify/glossary.md",
        ".specify/project/tech-stack.md",
        ".specify/project/coding-rules.md",
        ".specify/project/architecture-principles.md",
        ".specify/project/domain-map.md",
        ".specify/templates/commands/brief.md",
        ".specify/templates/commands/common-design.md",
        ".specify/templates/commands/design.md",
        ".specify/templates/commands/tasks.md",
        ".specify/templates/commands/implement.md",
        ".specify/templates/artifacts/brief.md",
        ".specify/templates/artifacts/design/overview.md",
        ".specify/templates/artifacts/design/ui-storybook/README.md",
        ".specify/templates/artifacts/design/ui-storybook/package.json",
        ".specify/templates/artifacts/design/ui-fields.yaml",
        ".specify/templates/artifacts/design/ui-storybook/.storybook/main.ts",
        ".specify/templates/artifacts/design/ui-storybook/.storybook/preview.ts",
        ".specify/templates/artifacts/design/ui-storybook/.storybook/preview.css",
        ".specify/templates/artifacts/design/ui-storybook/stories/SCR-001-example.stories.js",
        ".specify/templates/artifacts/design/ui-storybook/components/SCR-001-example.html",
        ".specify/templates/artifacts/design/sequence-flows/core-flow.md",
        ".specify/templates/artifacts/design/batch-design.md",
        ".specify/templates/artifacts/design/common-design-refs.yaml",
        ".specify/templates/artifacts/design/test-design.md",
        ".specify/templates/artifacts/design/test-plan.md",
        ".specify/templates/artifacts/design/traceability.yaml",
        ".specify/templates/artifacts/design/tasks.md",
        ".specify/templates/artifacts/common_design/api.md",
        ".specify/templates/artifacts/common_design/data.md",
        ".specify/templates/artifacts/common_design/module.md",
        ".specify/templates/artifacts/common_design/ui-screen-catalog.md",
        ".specify/templates/artifacts/common_design/ui-navigation-rules.md",
    ]
    for relative in required_files:
        (tmp_path / relative).write_text("placeholder\n", encoding="utf-8")

    assert missing_shared_paths(tmp_path) == []


def test_validate_design_bundle_reports_non_mapping_traceability_file(tmp_path: Path):
    bundle_dir = tmp_path / "designs" / "specific_design" / "001-sample"
    _create_bundle_files(bundle_dir, tmp_path)
    (bundle_dir / "traceability.yaml").write_text("- bad\n", encoding="utf-8")

    result = validate_design_bundle(bundle_dir=bundle_dir)

    assert result.invalid_traceability_entries == [
        f"traceability file must contain a mapping: {bundle_dir / 'traceability.yaml'}"
    ]


def test_validate_design_bundle_reports_missing_common_design_reference(tmp_path: Path):
    bundle_dir = tmp_path / "designs" / "specific_design" / "001-sample"
    brief_path = tmp_path / "briefs" / "001-sample.md"
    _create_specific_bundle_files(bundle_dir)
    (bundle_dir / "traceability.yaml").write_text(
        "brief_id: 001-sample\ndesign_id: 001-sample\nrequirements:\n"
        "  - requirement_id: REQ-001\n    primary_artifact: overview.md\n"
        "    related_artifacts: []\n    common_design_refs:\n      - CD-API-999\n",
        encoding="utf-8",
    )
    (bundle_dir / "common-design-refs.yaml").write_text(
        "brief_id: 001-sample\ndesign_id: 001-sample\ncommon_design_refs:\n"
        "  - ref_id: CD-API-999\n    kind: api\n    usage: consume\n",
        encoding="utf-8",
    )
    (bundle_dir / "tasks.md").write_text(
        "# Tasks\n\n## Tasks\n### TASK-001 Example\n- requirement_ids:\n  - REQ-001\n"
        "- artifact_refs:\n  - overview.md\n- common_design_refs:\n  - CD-API-999\n",
        encoding="utf-8",
    )
    brief_path.parent.mkdir(parents=True)
    brief_path.write_text(
        "# Sample\n\n## Common Design References\n- CD-API-999\n\n## Requirements\n"
        "### REQ-001 Example\n- priority: must\n",
        encoding="utf-8",
    )

    result = validate_design_bundle(bundle_dir=bundle_dir, brief_path=brief_path)

    assert "common design ref cannot be resolved: CD-API-999" in result.invalid_common_design_entries


def test_validate_design_bundle_rejects_legacy_specific_artifacts(tmp_path: Path):
    bundle_dir = tmp_path / "designs" / "specific_design" / "001-sample"
    _create_bundle_files(bundle_dir, tmp_path)
    (bundle_dir / "api-design.md").write_text("legacy\n", encoding="utf-8")

    result = validate_design_bundle(bundle_dir=bundle_dir)

    assert result.invalid_structure_entries == [
        f"legacy specific design artifact is not allowed: {bundle_dir / 'api-design.md'}"
    ]


def test_ensure_valid_design_bundle_raises_for_invalid_bundle(tmp_path: Path):
    bundle_dir = tmp_path / "designs" / "specific_design" / "001-invalid"
    bundle_dir.mkdir(parents=True)

    with pytest.raises(DesignBundleValidationError):
        ensure_valid_design_bundle(bundle_dir)


def _create_bundle_files(bundle_dir: Path, project_dir: Path) -> None:
    _create_specific_bundle_files(bundle_dir)
    _create_common_design(project_dir)
    (bundle_dir / "tasks.md").write_text(
        "# Tasks\n\n## Tasks\n### TASK-001 Example\n- requirement_ids:\n  - REQ-001\n"
        "- artifact_refs:\n  - overview.md\n- common_design_refs:\n  - CD-API-001\n",
        encoding="utf-8",
    )
    (bundle_dir / "common-design-refs.yaml").write_text(
        "brief_id: 001-sample\ndesign_id: 001-sample\ncommon_design_refs:\n"
        "  - ref_id: CD-API-001\n    kind: api\n    usage: consume\n",
        encoding="utf-8",
    )
    (bundle_dir / "traceability.yaml").write_text(
        "brief_id: 001-sample\ndesign_id: 001-sample\nrequirements:\n"
        "  - requirement_id: REQ-001\n    primary_artifact: overview.md\n"
        "    related_artifacts: []\n    common_design_refs:\n      - CD-API-001\n",
        encoding="utf-8",
    )
