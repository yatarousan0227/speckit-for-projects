# Customer API Modernization

- brief_id: 001-customer-api-modernization
- status: draft

## Background
Partner systems currently rely on a legacy export format with poor filtering.

## Goal
Expose a query API for customer profile lookup.

## Scope In
- Profile lookup API
- Response contract standardization

## Scope Out
- Frontend portal

## Users And External Actors
- Partner integration system

## Constraints
- Must preserve the existing customer identifier

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
### REQ-001 Return customer profiles by external identifier
- priority: must
- description: Partner systems can retrieve a normalized customer profile by external identifier.
- rationale: Downstream workflows require stable API access.

## Source References
- `.specify/project/tech-stack.md`
- `.specify/project/architecture-principles.md`
- `.specify/glossary.md`
