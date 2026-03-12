# Test Design

## Requirement Coverage

### REQ-001
- normal_cases:
  - Valid identifier returns one normalized profile
- error_cases:
  - Unknown identifier returns not found
- boundary_cases:
  - Identifier with minimum length is accepted
- references:
  - common-design-refs.yaml
  - overview.md
