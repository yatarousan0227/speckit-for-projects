# Nightly Reconciliation

- brief_id: 001-nightly-reconciliation
- status: draft

## Background
Daily transaction totals are manually reconciled against an external settlement file.

## Goal
Automate nightly reconciliation and exception reporting.

## Scope In
- Nightly batch import
- Reconciliation result report

## Scope Out
- Real-time settlement

## Users And External Actors
- Back-office operations
- External settlement system

## Constraints
- External file is delivered once per night

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
### REQ-001 Reconcile settlement totals each night
- priority: must
- description: The system imports the nightly settlement file and reports mismatches by the next business day.
- rationale: Manual reconciliation delays morning operations.

## Source References
- `.specify/project/tech-stack.md`
- `.specify/project/architecture-principles.md`
- `.specify/glossary.md`
