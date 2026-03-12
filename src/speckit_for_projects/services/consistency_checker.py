"""Scaffold consistency checks."""

from __future__ import annotations

import re
from collections.abc import Mapping
from dataclasses import dataclass, field
from pathlib import Path

from ruamel.yaml.error import YAMLError

from speckit_for_projects.domain.exceptions import DesignBundleValidationError
from speckit_for_projects.io.yaml_loader import load_yaml

REQUIRED_SHARED_PATHS = [
    Path(".specify/glossary.md"),
    Path(".specify/project/tech-stack.md"),
    Path(".specify/project/coding-rules.md"),
    Path(".specify/project/architecture-principles.md"),
    Path(".specify/project/domain-map.md"),
    Path(".specify/templates/commands/brief.md"),
    Path(".specify/templates/commands/common-design.md"),
    Path(".specify/templates/commands/design.md"),
    Path(".specify/templates/commands/tasks.md"),
    Path(".specify/templates/commands/implement.md"),
    Path(".specify/templates/artifacts/brief.md"),
    Path(".specify/templates/artifacts/design/overview.md"),
    Path(".specify/templates/artifacts/design/ui-storybook/README.md"),
    Path(".specify/templates/artifacts/design/ui-storybook/package.json"),
    Path(".specify/templates/artifacts/design/ui-fields.yaml"),
    Path(".specify/templates/artifacts/design/ui-storybook/.storybook/main.ts"),
    Path(".specify/templates/artifacts/design/ui-storybook/.storybook/preview.ts"),
    Path(".specify/templates/artifacts/design/ui-storybook/.storybook/preview.css"),
    Path(".specify/templates/artifacts/design/ui-storybook/stories/SCR-001-example.stories.js"),
    Path(".specify/templates/artifacts/design/ui-storybook/components/SCR-001-example.html"),
    Path(".specify/templates/artifacts/design/sequence-flows/core-flow.md"),
    Path(".specify/templates/artifacts/design/batch-design.md"),
    Path(".specify/templates/artifacts/design/common-design-refs.yaml"),
    Path(".specify/templates/artifacts/design/test-design.md"),
    Path(".specify/templates/artifacts/design/test-plan.md"),
    Path(".specify/templates/artifacts/design/traceability.yaml"),
    Path(".specify/templates/artifacts/design/tasks.md"),
    Path(".specify/templates/artifacts/common_design/api.md"),
    Path(".specify/templates/artifacts/common_design/data.md"),
    Path(".specify/templates/artifacts/common_design/module.md"),
    Path(".specify/templates/artifacts/common_design/ui-screen-catalog.md"),
    Path(".specify/templates/artifacts/common_design/ui-navigation-rules.md"),
    Path("briefs"),
    Path("designs/common_design"),
    Path("designs/common_design/api"),
    Path("designs/common_design/data"),
    Path("designs/common_design/module"),
    Path("designs/specific_design"),
]
SPECIFIC_DESIGNS_PATH = Path("designs/specific_design")
BRIEFS_PATH = Path("briefs")

REQUIRED_BUNDLE_PATHS = [
    Path("overview.md"),
    Path("ui-storybook/README.md"),
    Path("ui-storybook/package.json"),
    Path("ui-fields.yaml"),
    Path("ui-storybook/.storybook/main.ts"),
    Path("ui-storybook/.storybook/preview.ts"),
    Path("ui-storybook/.storybook/preview.css"),
    Path("sequence-flows/core-flow.md"),
    Path("batch-design.md"),
    Path("common-design-refs.yaml"),
    Path("test-design.md"),
    Path("test-plan.md"),
    Path("traceability.yaml"),
    Path("tasks.md"),
]

REQUIREMENT_HEADING_PATTERN = re.compile(r"^###\s+(REQ-\d{3})\b", re.MULTILINE)
TASK_REQUIREMENT_PATTERN = re.compile(r"\bREQ-\d{3}\b")
COMMON_DESIGN_REF_PATTERN = re.compile(r"\bCD-(?:API|DATA|MOD|UI)-\d{3}\b")
STORYBOOK_STORY_GLOB = "ui-storybook/stories/SCR-*.stories.js"
STORYBOOK_COMPONENT_GLOB = "ui-storybook/components/SCR-*.html"
OLD_SPECIFIC_DESIGN_FILES = [
    Path("api-design.md"),
    Path("data-design.md"),
    Path("module-design.md"),
]
SPECIFIC_ARTIFACT_TOKENS = (
    "overview.md",
    "ui-fields.yaml",
    "common-design-refs.yaml",
    "batch-design.md",
    "test-design.md",
    "test-plan.md",
    "traceability.yaml",
    "ui-storybook/",
    "sequence-flows/",
)


@dataclass
class BundleValidationResult:
    """Validation result for one design bundle."""

    missing_files: list[str] = field(default_factory=list)
    missing_requirements: list[str] = field(default_factory=list)
    uncovered_task_requirements: list[str] = field(default_factory=list)
    invalid_traceability_entries: list[str] = field(default_factory=list)
    invalid_common_design_entries: list[str] = field(default_factory=list)
    invalid_structure_entries: list[str] = field(default_factory=list)

    @property
    def is_valid(self) -> bool:
        return not (
            self.missing_files
            or self.missing_requirements
            or self.uncovered_task_requirements
            or self.invalid_traceability_entries
            or self.invalid_common_design_entries
            or self.invalid_structure_entries
        )

    @property
    def issues(self) -> list[str]:
        return (
            self.missing_files
            + self.missing_requirements
            + self.uncovered_task_requirements
            + self.invalid_traceability_entries
            + self.invalid_common_design_entries
            + self.invalid_structure_entries
        )


def missing_shared_paths(project_dir: Path) -> list[Path]:
    """Return missing shared scaffold paths."""
    return [relative for relative in REQUIRED_SHARED_PATHS if not (project_dir / relative).exists()]


def resolve_design_bundle_path(project_dir: Path, target: str | Path) -> Path:
    """Resolve a design bundle from a design ID or explicit path."""
    candidate = Path(target)
    direct_path = candidate if candidate.is_absolute() else project_dir / candidate
    if direct_path.exists():
        if not direct_path.is_dir():
            raise FileNotFoundError(f"design bundle is not a directory: {target}")
        return direct_path

    bundle_path = project_dir / SPECIFIC_DESIGNS_PATH / str(target)
    if bundle_path.is_dir():
        return bundle_path

    raise FileNotFoundError(f"design bundle not found: {target}")


def list_design_bundle_paths(project_dir: Path) -> list[Path]:
    """List all specific design bundle directories under the project."""
    designs_dir = project_dir / SPECIFIC_DESIGNS_PATH
    if not designs_dir.is_dir():
        raise FileNotFoundError(f"specific design directory not found: {designs_dir}")
    return sorted(path for path in designs_dir.iterdir() if path.is_dir())


def resolve_brief_path_for_bundle(
    bundle_dir: Path, project_dir: Path | None = None
) -> Path | None:
    """Resolve the matching brief path for a design bundle when it exists."""
    resolved_project_dir = project_dir or _discover_project_dir(
        bundle_dir=bundle_dir,
        brief_path=None,
    )
    if resolved_project_dir is None:
        return None
    brief_path = resolved_project_dir / BRIEFS_PATH / f"{bundle_dir.name}.md"
    if brief_path.exists():
        return brief_path
    return None


def validate_design_bundle(
    bundle_dir: Path, brief_path: Path | None = None
) -> BundleValidationResult:
    """Validate one generated specific design bundle."""
    result = BundleValidationResult()
    project_dir = _discover_project_dir(bundle_dir=bundle_dir, brief_path=brief_path)

    for relative_path in REQUIRED_BUNDLE_PATHS:
        if not (bundle_dir / relative_path).exists():
            result.missing_files.append(f"missing file: {bundle_dir / relative_path}")

    if not any(bundle_dir.glob(STORYBOOK_STORY_GLOB)):
        result.missing_files.append(
            f"missing file matching: {bundle_dir / STORYBOOK_STORY_GLOB}"
        )
    if not any(bundle_dir.glob(STORYBOOK_COMPONENT_GLOB)):
        result.missing_files.append(
            f"missing file matching: {bundle_dir / STORYBOOK_COMPONENT_GLOB}"
        )
    for relative_path in OLD_SPECIFIC_DESIGN_FILES:
        if (bundle_dir / relative_path).exists():
            result.invalid_structure_entries.append(
                f"legacy specific design artifact is not allowed: {bundle_dir / relative_path}"
            )

    traceability_path = bundle_dir / "traceability.yaml"
    common_design_refs_path = bundle_dir / "common-design-refs.yaml"
    tasks_path = bundle_dir / "tasks.md"
    mapped_ids: set[str] = set()
    bundle_common_refs = set()
    if traceability_path.exists():
        traceability_common_refs = (
            _collect_common_design_refs(common_design_refs_path, result)
            if common_design_refs_path.exists()
            else set()
        )
        mapped_ids.update(
            _collect_traceability_ids(
                traceability_path=traceability_path,
                result=result,
                bundle_common_refs=traceability_common_refs,
            )
        )
    else:
        result.invalid_traceability_entries.append(
            f"missing traceability file: {traceability_path}"
        )
    if common_design_refs_path.exists():
        bundle_common_refs = _collect_common_design_refs(common_design_refs_path, result)
    else:
        result.invalid_common_design_entries.append(
            f"missing common design refs file: {common_design_refs_path}"
        )

    if brief_path is not None and brief_path.exists():
        requirement_ids = set(
            REQUIREMENT_HEADING_PATTERN.findall(brief_path.read_text(encoding="utf-8"))
        )
        brief_common_refs = _extract_brief_common_design_refs(brief_path, result)
        result.missing_requirements.extend(
            f"unmapped requirement: {requirement_id}"
            for requirement_id in sorted(requirement_ids - mapped_ids)
        )
        task_ids = extract_task_requirement_ids(tasks_path) if tasks_path.exists() else set()
        result.uncovered_task_requirements.extend(
            f"requirement missing from tasks: {requirement_id}"
            for requirement_id in sorted(requirement_ids - task_ids)
        )
        result.invalid_common_design_entries.extend(
            f"brief common design ref missing from specific bundle: {ref_id}"
            for ref_id in sorted(brief_common_refs - bundle_common_refs)
        )

    if project_dir is not None:
        for ref_id in sorted(bundle_common_refs):
            if _resolve_common_design_path(project_dir, ref_id) is None:
                result.invalid_common_design_entries.append(
                    f"common design ref cannot be resolved: {ref_id}"
                )

    if tasks_path.exists():
        task_content = tasks_path.read_text(encoding="utf-8")
        has_specific_artifact_ref = any(token in task_content for token in SPECIFIC_ARTIFACT_TOKENS)
        has_common_design_ref = bool(COMMON_DESIGN_REF_PATTERN.search(task_content))
        if not has_specific_artifact_ref and not has_common_design_ref:
            result.invalid_structure_entries.append(
                "tasks must reference at least one specific artifact or common design ref: "
                f"{tasks_path}"
            )

    return result


def extract_task_requirement_ids(tasks_path: Path) -> set[str]:
    """Extract all requirement IDs referenced in tasks.md."""
    if not tasks_path.exists():
        return set()
    content = tasks_path.read_text(encoding="utf-8")
    return set(TASK_REQUIREMENT_PATTERN.findall(content))


def _collect_traceability_ids(
    traceability_path: Path,
    result: BundleValidationResult,
    bundle_common_refs: set[str],
) -> set[str]:
    """Collect mapped requirement IDs from traceability.yaml without crashing on bad shapes."""
    try:
        data = load_yaml(traceability_path)
    except YAMLError as exc:
        result.invalid_traceability_entries.append(
            f"invalid traceability yaml: {traceability_path} ({exc.__class__.__name__})"
        )
        return set()

    if data is None:
        return set()
    if not isinstance(data, Mapping):
        result.invalid_traceability_entries.append(
            f"traceability file must contain a mapping: {traceability_path}"
        )
        return set()

    requirements = data.get("requirements", [])
    if not isinstance(requirements, list):
        result.invalid_traceability_entries.append(
            f"traceability requirements must be a list: {traceability_path}"
        )
        return set()

    mapped_ids: set[str] = set()
    for index, entry in enumerate(requirements, start=1):
        if not isinstance(entry, Mapping):
            result.invalid_traceability_entries.append(
                f"traceability entry must be a mapping at index {index}: {traceability_path}"
            )
            continue

        requirement_id = entry.get("requirement_id") or entry.get("id")
        if not requirement_id:
            result.invalid_traceability_entries.append(
                f"traceability entry missing requirement_id: {traceability_path}"
            )
            continue

        mapped_ids.add(str(requirement_id))
        if not entry.get("primary_artifact"):
            result.invalid_traceability_entries.append(
                f"traceability entry missing primary_artifact for {requirement_id}"
            )
        primary_artifact = entry.get("primary_artifact")
        if primary_artifact and str(primary_artifact).startswith("common_design/"):
            result.invalid_traceability_entries.append(
                f"traceability primary_artifact must stay in specific design for {requirement_id}"
            )
        if not isinstance(entry.get("related_artifacts", []), list):
            result.invalid_traceability_entries.append(
                f"traceability related_artifacts must be a list for {requirement_id}"
            )
        common_design_refs = entry.get("common_design_refs")
        if common_design_refs is None:
            result.invalid_traceability_entries.append(
                f"traceability entry missing common_design_refs for {requirement_id}"
            )
            common_design_refs = []
        if not isinstance(common_design_refs, list):
            result.invalid_traceability_entries.append(
                f"traceability common_design_refs must be a list for {requirement_id}"
            )
            continue
        for ref in common_design_refs:
            if str(ref) not in bundle_common_refs:
                result.invalid_traceability_entries.append(
                    f"traceability references unknown common design ref {ref} for {requirement_id}"
                )

    return mapped_ids


def _collect_common_design_refs(
    common_design_refs_path: Path, result: BundleValidationResult
) -> set[str]:
    try:
        data = load_yaml(common_design_refs_path)
    except YAMLError as exc:
        result.invalid_common_design_entries.append(
            f"invalid common design refs yaml: {common_design_refs_path} ({exc.__class__.__name__})"
        )
        return set()

    if data is None:
        return set()
    if not isinstance(data, Mapping):
        result.invalid_common_design_entries.append(
            f"common design refs file must contain a mapping: {common_design_refs_path}"
        )
        return set()

    refs = data.get("common_design_refs", [])
    if not isinstance(refs, list):
        result.invalid_common_design_entries.append(
            f"common_design_refs must be a list: {common_design_refs_path}"
        )
        return set()

    resolved_refs: set[str] = set()
    for index, entry in enumerate(refs, start=1):
        if not isinstance(entry, Mapping):
            result.invalid_common_design_entries.append(
                "common design ref entry must be a mapping at index "
                f"{index}: {common_design_refs_path}"
            )
            continue
        ref_id = entry.get("ref_id")
        if not ref_id:
            result.invalid_common_design_entries.append(
                f"common design ref entry missing ref_id: {common_design_refs_path}"
            )
            continue
        if not COMMON_DESIGN_REF_PATTERN.fullmatch(str(ref_id)):
            result.invalid_common_design_entries.append(
                f"invalid common design ref id {ref_id}: {common_design_refs_path}"
            )
            continue
        resolved_refs.add(str(ref_id))
    return resolved_refs


def _extract_brief_common_design_refs(
    brief_path: Path, result: BundleValidationResult
) -> set[str]:
    content = brief_path.read_text(encoding="utf-8")
    match = re.search(
        r"^## Common Design References\s*\n(?P<body>.*?)(?=^##\s|\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if match is None:
        result.invalid_common_design_entries.append(
            f"brief missing Common Design References section: {brief_path}"
        )
        return set()

    refs = set(COMMON_DESIGN_REF_PATTERN.findall(match.group("body")))
    if "- none" in match.group("body"):
        return set()
    return refs


def _resolve_common_design_path(project_dir: Path, ref_id: str) -> Path | None:
    matches = list((project_dir / "designs" / "common_design").glob(f"*/{ref_id}-*.md"))
    if len(matches) != 1:
        return None
    return matches[0]


def _discover_project_dir(bundle_dir: Path, brief_path: Path | None) -> Path | None:
    if brief_path is not None:
        return brief_path.parent.parent
    for candidate in [bundle_dir, *bundle_dir.parents]:
        if (candidate / "briefs").exists() and (candidate / "designs").exists():
            return candidate
    return None


def ensure_valid_design_bundle(bundle_dir: Path, brief_path: Path | None = None) -> None:
    """Raise when a design bundle is inconsistent."""
    result = validate_design_bundle(bundle_dir=bundle_dir, brief_path=brief_path)
    if not result.is_valid:
        raise DesignBundleValidationError(result.issues)
