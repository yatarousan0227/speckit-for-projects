"""`sdd analyze` command."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from speckit_for_projects.services.consistency_checker import (
    BundleValidationResult,
    list_design_bundle_paths,
    resolve_brief_path_for_bundle,
    resolve_design_bundle_path,
    validate_design_bundle,
)

ISSUE_CATEGORIES: tuple[tuple[str, str], ...] = (
    ("missing_files", "missing_files"),
    ("missing_requirements", "missing_requirements"),
    ("uncovered_task_requirements", "uncovered_task_requirements"),
    ("invalid_traceability_entries", "invalid_traceability_entries"),
    ("invalid_common_design_entries", "invalid_common_design_entries"),
    ("invalid_structure_entries", "invalid_structure_entries"),
)


@dataclass(frozen=True)
class FormattedIssueCategory:
    """CLI-ready issue category view."""

    key: str
    label: str
    count: int
    messages: tuple[str, ...]


@dataclass(frozen=True)
class BundleAnalysis:
    """Analyze result with bundle metadata."""

    bundle_dir: Path
    brief_path: Path | None
    result: BundleValidationResult

    @property
    def status(self) -> str:
        return "success" if self.result.is_valid else "failure"


@dataclass(frozen=True)
class FormattedBundleAnalysis:
    """CLI-ready bundle analysis view."""

    bundle_path: str
    brief_path: str | None
    status: str
    total_issues: int
    categories: tuple[FormattedIssueCategory, ...]


def register_analyze_command(app: typer.Typer) -> None:
    """Register the analyze command on the Typer app."""

    @app.command("analyze")
    def analyze_command(
        target: str | None = typer.Argument(
            None,
            help="Design ID or path to a specific design bundle.",
        ),
        analyze_all: bool = typer.Option(
            False,
            "--all",
            help="Analyze every bundle under designs/specific_design/.",
        ),
        debug: bool = typer.Option(False, "--debug", help="Show extra debug output."),
    ) -> None:
        _validate_analyze_options(target=target, analyze_all=analyze_all)

        project_dir = Path.cwd()
        console = Console()
        bundle_dirs = _resolve_bundle_targets(
            project_dir=project_dir,
            target=target,
            analyze_all=analyze_all,
        )
        analyses: list[BundleAnalysis] = []
        for bundle_dir in bundle_dirs:
            brief_path = resolve_brief_path_for_bundle(
                bundle_dir=bundle_dir,
                project_dir=project_dir,
            )
            analyses.append(
                BundleAnalysis(
                    bundle_dir=bundle_dir,
                    brief_path=brief_path,
                    result=validate_design_bundle(bundle_dir=bundle_dir, brief_path=brief_path),
                )
            )

        _print_analysis_results(
            console=console,
            analyses=analyses,
            project_dir=project_dir,
            debug=debug,
        )
        raise typer.Exit(code=2 if any(not item.result.is_valid for item in analyses) else 0)


def _validate_analyze_options(target: str | None, analyze_all: bool) -> None:
    """Validate option combinations for `sdd analyze`."""
    if target and analyze_all:
        raise typer.BadParameter("target and --all cannot be used together")
    if not target and not analyze_all:
        raise typer.BadParameter("target is required unless --all is used")


def _resolve_bundle_targets(project_dir: Path, target: str | None, analyze_all: bool) -> list[Path]:
    """Resolve the analyze target to one or more bundle directories."""
    try:
        if analyze_all:
            return list_design_bundle_paths(project_dir)
        if target is None:
            raise typer.BadParameter("target is required unless --all is used")
        return [resolve_design_bundle_path(project_dir, target)]
    except FileNotFoundError as exc:
        raise typer.BadParameter(str(exc)) from exc


def _print_analysis_results(
    console: Console, analyses: list[BundleAnalysis], project_dir: Path, debug: bool
) -> None:
    """Render analyze results to the terminal."""
    formatted_analyses = [
        _format_bundle_analysis(analysis=analysis, project_dir=project_dir) for analysis in analyses
    ]

    table = Table(title="SpecKit for Projects analyze")
    table.add_column("Bundle")
    table.add_column("Status")
    table.add_column("Issues", justify="right")

    for formatted in formatted_analyses:
        table.add_row(
            formatted.bundle_path,
            formatted.status,
            str(formatted.total_issues),
        )

    console.print(table)

    _print_summary(
        console=console,
        formatted_analyses=formatted_analyses,
        multiple_bundles=len(formatted_analyses) > 1,
    )

    for formatted in formatted_analyses:
        if formatted.status == "success" and not debug:
            continue
        _print_bundle_details(console=console, formatted=formatted, debug=debug)


def _format_bundle_analysis(analysis: BundleAnalysis, project_dir: Path) -> FormattedBundleAnalysis:
    """Convert a raw bundle analysis into CLI display data."""
    categories = []
    for key, label in ISSUE_CATEGORIES:
        messages = tuple(getattr(analysis.result, key))
        categories.append(
            FormattedIssueCategory(
                key=key,
                label=label,
                count=len(messages),
                messages=messages,
            )
        )
    return FormattedBundleAnalysis(
        bundle_path=_display_path(analysis.bundle_dir, project_dir),
        brief_path=(
            _display_path(analysis.brief_path, project_dir)
            if analysis.brief_path is not None
            else None
        ),
        status=analysis.status,
        total_issues=len(analysis.result.issues),
        categories=tuple(categories),
    )


def _print_summary(
    console: Console, formatted_analyses: list[FormattedBundleAnalysis], multiple_bundles: bool
) -> None:
    """Print overall analyze summary."""
    success_count = sum(1 for analysis in formatted_analyses if analysis.status == "success")
    failure_count = len(formatted_analyses) - success_count
    console.print(
        "summary: "
        f"inspected {len(formatted_analyses)} bundle(s), "
        f"success {success_count}, "
        f"failure {failure_count}"
    )

    if not multiple_bundles or failure_count == 0:
        return

    failure_paths = [
        analysis.bundle_path
        for analysis in formatted_analyses
        if analysis.status == "failure"
    ]
    console.print("failure bundles:")
    for failure_path in failure_paths:
        console.print(f"  - {failure_path}")


def _print_bundle_details(
    console: Console, formatted: FormattedBundleAnalysis, debug: bool
) -> None:
    """Print per-bundle detail sections."""
    console.print(f"bundle detail: {formatted.bundle_path}")
    console.print(f"status: {formatted.status}")

    if debug and formatted.brief_path is not None:
        console.print(f"brief: {formatted.brief_path}")

    issue_categories = []
    for category in formatted.categories:
        if category.count == 0:
            continue
        issue_categories.append(category)

    if issue_categories:
        console.print("issue counts:")
        for category in issue_categories:
            console.print(f"  - {category.label}: {category.count}")

    if formatted.status == "success":
        console.print("no issues found")
        return

    for category in issue_categories:
        console.print(f"{category.label} ({category.count})")
        for message in category.messages:
            console.print(f"  - {message}")


def _display_path(path: Path, project_dir: Path) -> str:
    """Render a path relative to the project when possible."""
    try:
        return str(path.relative_to(project_dir))
    except ValueError:
        return str(path)
