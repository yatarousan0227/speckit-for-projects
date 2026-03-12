# Application Portal Search

- brief_id: 001-screened-application-portal
- status: draft

## Background
The operations team currently reviews customer applications by email and spreadsheet.

## Goal
Provide a searchable web screen for application review.

## Scope In
- Application search
- Detail view transition

## Scope Out
- Payment processing

## Users And External Actors
- Operations staff

## Constraints
- Must reuse the existing customer master API

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
- CD-UI-001
- CD-UI-002

## Requirements
### REQ-001 Search applications from the main screen
- priority: must
- description: Operations staff can search applications by applicant name and status.
- rationale: Review throughput depends on quick filtering.

## Source References
- `.specify/project/tech-stack.md`
- `.specify/project/architecture-principles.md`
- `.specify/glossary.md`
