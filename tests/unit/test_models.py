from __future__ import annotations

from speckit_for_projects.domain.models import Brief, ProjectStandards, Requirement, TraceabilityEntry


def test_brief_round_trip():
    brief = Brief(
        brief_id="001-customer-portal",
        title="Customer Portal",
        background="Replace manual email workflows.",
        scope_in=["Registration", "Profile update"],
        scope_out=["Billing"],
        constraints=["Must reuse SSO"],
        common_design_refs=["CD-API-001"],
        requirements=[
            Requirement(
                id="REQ-001",
                summary="Users can sign up",
                description="The system supports self-service sign-up.",
                priority="must",
            )
        ],
    )

    restored = Brief.model_validate(brief.model_dump())

    assert restored == brief


def test_traceability_round_trip():
    entry = TraceabilityEntry(
        requirement_id="REQ-001",
        primary_artifact="overview.md",
        related_artifacts=["common-design-refs.yaml", "traceability.yaml"],
        common_design_refs=["CD-API-001"],
        project_standards=["tech-stack.md"],
        status="mapped",
    )

    restored = TraceabilityEntry.model_validate(entry.model_dump())

    assert restored == entry


def test_project_standards_round_trip():
    standards = ProjectStandards(
        tech_stack="python",
        domain_map=".specify/project/domain-map.md",
        coding_rules="strict",
        architecture_principles="layered",
    )

    restored = ProjectStandards.model_validate(standards.model_dump())

    assert restored == standards
