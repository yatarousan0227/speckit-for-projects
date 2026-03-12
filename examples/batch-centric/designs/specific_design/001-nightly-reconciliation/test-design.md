# Test Design

## Requirement Coverage

### REQ-001
- normal_cases:
  - Nightly job imports settlement file and produces a report
- error_cases:
  - Missing file raises an operational alert
- boundary_cases:
  - Empty file still generates a zero-mismatch report
- references:
  - batch-design.md
  - common-design-refs.yaml
