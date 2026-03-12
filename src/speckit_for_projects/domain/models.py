"""Core domain models for speckit_for_projects."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class Requirement(BaseModel):
    """A requirement captured in a brief."""

    model_config = ConfigDict(extra="forbid")

    id: str
    summary: str
    description: str
    priority: Literal["must", "should", "could"] = "should"


class Brief(BaseModel):
    """The structured source document for design generation."""

    model_config = ConfigDict(extra="forbid")

    brief_id: str
    title: str
    background: str
    scope_in: list[str] = Field(default_factory=list)
    scope_out: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    common_design_refs: list[str] = Field(default_factory=list)
    requirements: list[Requirement] = Field(default_factory=list)


class ProjectStandards(BaseModel):
    """Shared project standards used by design generation."""

    model_config = ConfigDict(extra="forbid")

    tech_stack: str
    domain_map: str | None = None
    coding_rules: str
    architecture_principles: str


class DesignBundle(BaseModel):
    """A design bundle generated from one brief."""

    model_config = ConfigDict(extra="forbid")

    design_id: str
    brief_id: str
    artifacts: list[str] = Field(default_factory=list)


class TraceabilityEntry(BaseModel):
    """Maps one requirement to generated artifacts."""

    model_config = ConfigDict(extra="forbid")

    requirement_id: str
    primary_artifact: str
    related_artifacts: list[str] = Field(default_factory=list)
    common_design_refs: list[str] = Field(default_factory=list)
    project_standards: list[str] = Field(default_factory=list)
    status: Literal["draft", "mapped", "reviewed"] = "draft"


class TaskItem(BaseModel):
    """A planned implementation task."""

    model_config = ConfigDict(extra="forbid")

    task_id: str
    title: str
    requirement_ids: list[str] = Field(default_factory=list)
    artifact_refs: list[str] = Field(default_factory=list)
    common_design_refs: list[str] = Field(default_factory=list)
    depends_on: list[str] = Field(default_factory=list)
