# Add Project Domain Map Support

- brief_id: 001-project-domain-map-support
- status: draft

## Background
Large programs need multiple briefs so that scope, ownership, and review boundaries stay manageable. The current scaffold preserves requirement traceability inside each brief and design bundle, but it does not provide a first-class source for domain boundaries or cross-brief relationships. That makes it hard to explain why briefs are split, which briefs are related, and what upstream domains must be reviewed together.

## Goal
Introduce a shared `domain-map.md` project standard and reflect it in generated briefs, design bundles, and tasks so that multi-brief programs stay reviewable without collapsing back into one oversized brief.

## Scope In
- Add `.specify/project/domain-map.md` as a managed project standard
- Define how brief generation reads domain relationships when the file exists
- Define how design generation propagates related brief and dependency context
- Define backward-compatible behavior for repositories that do not adopt the file yet
- Define validation and example coverage for the new standard

## Scope Out
- Automatic graph layout or visualization tooling
- Cross-repository dependency discovery
- Runtime service dependency management outside the design documents
- A new database or metadata service for storing relationships

## Users And External Actors
- Design leads working across multiple briefs
- Reviewers who need to understand upstream and downstream impact
- Engineers implementing tasks derived from related briefs
- AI agents generating briefs, design bundles, and tasks

## Constraints
- Existing repositories must keep working when `domain-map.md` is absent
- The solution must stay text-file based and fit the current small CLI design
- Shared project standards remain the canonical source of cross-cutting guidance
- The added workflow should improve clarity without requiring portfolio-scale orchestration logic

## Domain Alignment
- primary_domain: DOM-001
- related_briefs:
  - none
- upstream_domains:
  - none
- downstream_domains:
  - none

## Common Design References
- CD-API-001
- CD-DATA-001
- CD-MOD-001

## Requirements
### REQ-001 Add shared domain map standard
- priority: must
- description: The scaffold must support `.specify/project/domain-map.md` as a shared project standard for domain boundaries, dependencies, and related brief references.
- rationale: Multi-brief programs need one canonical source that explains why briefs are separated and how they connect.

### REQ-002 Reflect domain context in briefs
- priority: must
- description: When `domain-map.md` exists, brief generation must read it and write explicit domain alignment and related brief references into the generated brief.
- rationale: Brief readers need immediate visibility into whether a feature extends an existing domain and what other briefs must be reviewed with it.

### REQ-003 Reflect domain context in design bundles
- priority: must
- description: Design generation must propagate domain dependencies and related brief context into the generated design bundle so that module boundaries, test scope, and review assumptions account for upstream and downstream impact.
- rationale: Design artifacts are where cross-domain effects become concrete, so the relationship data must survive beyond the brief.

### REQ-004 Preserve backward-compatible command behavior
- priority: must
- description: `sdd.brief`, `sdd.design`, and `sdd.tasks` must continue to work when `domain-map.md` is absent, while using the additional context when the file is present.
- rationale: Existing repositories should adopt the feature incrementally instead of blocking on a full migration.

### REQ-005 Validate and document the new standard
- priority: should
- description: The repository must provide checks, examples, and documentation that explain how to use the domain map standard and verify that generated outputs stay consistent with it.
- rationale: The feature will be ignored or misused unless it is visible in the scaffold, examples, and regression coverage.

## Source References
- `.specify/project/tech-stack.md`
- `.specify/project/architecture-principles.md`
- `.specify/project/domain-map.md`
- `.specify/glossary.md`
