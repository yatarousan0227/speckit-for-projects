# Test Design

## Requirement Coverage

### REQ-001
- normal_cases:
  - Search by applicant name returns matching applications
- error_cases:
  - API error shows retry guidance
- boundary_cases:
  - Empty search condition returns the default list
- references:
  - overview.md
  - common-design-refs.yaml
