from __future__ import annotations

from pathlib import Path

from speckit_for_projects.services.consistency_checker import validate_design_bundle

ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = [
    (
        ROOT / "examples" / "screen-centric",
        "briefs/001-screened-application-portal.md",
        "designs/specific_design/001-screened-application-portal",
    ),
    (
        ROOT / "examples" / "api-centric",
        "briefs/001-customer-api-modernization.md",
        "designs/specific_design/001-customer-api-modernization",
    ),
    (
        ROOT / "examples" / "batch-centric",
        "briefs/001-nightly-reconciliation.md",
        "designs/specific_design/001-nightly-reconciliation",
    ),
]


def test_example_projects_have_valid_design_bundles():
    for example_root, brief_relative, bundle_relative in EXAMPLES:
        result = validate_design_bundle(
            bundle_dir=example_root / bundle_relative,
            brief_path=example_root / brief_relative,
        )
        assert result.is_valid, f"{example_root.name} has issues: {result.issues}"


def test_project_standards_examples_include_design_system_samples():
    example_roots = [
        ROOT / "examples" / "project-standards" / "todo-app",
        ROOT / "examples" / "project-standards" / "todo-app-ja",
    ]

    for example_root in example_roots:
        assert (example_root / ".specify" / "project" / "domain-map.md").exists()
        assert (example_root / ".specify" / "project" / "tech-stack.md").exists()
        assert (example_root / ".specify" / "project" / "coding-rules.md").exists()
        assert (example_root / ".specify" / "project" / "architecture-principles.md").exists()
