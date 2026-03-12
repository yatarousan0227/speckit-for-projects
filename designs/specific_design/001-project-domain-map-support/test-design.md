# Test Design

## Requirement Coverage

### REQ-001
- normal_cases:
  - `sdd init` installs `.specify/project/domain-map.md` alongside the existing shared project standards.
  - Generated scaffold documentation mentions the new file as the place for cross-brief domain relationships.
- error_cases:
  - Installer omits the file from one agent/scaffold path while other shared project files are present.
- boundary_cases:
  - Repository re-runs initialization with `--force` and the managed template is overwritten cleanly.
- references:
  - overview.md
  - module-design.md

### REQ-002
- normal_cases:
  - Brief generation reads `domain-map.md` and writes domain alignment plus related brief references for a feature that matches one known domain.
  - Brief generation includes the domain map in source references when it is used.
- error_cases:
  - The domain map contains an unknown related brief ID and the workflow reports the ambiguity instead of inventing relationships.
- boundary_cases:
  - A project without `domain-map.md` still generates a valid brief without extra relationship sections.
- references:
  - overview.md
  - api-design.md

### REQ-003
- normal_cases:
  - Design generation carries the brief's domain alignment into overview, module boundaries, and task assumptions.
  - Related brief references appear in the design bundle wherever cross-domain review is needed.
- error_cases:
  - The design workflow drops dependency context from one artifact and creates inconsistent review scope across the bundle.
- boundary_cases:
  - A design bundle for an isolated domain writes an explicit `none` relationship state instead of leaving the section ambiguous.
- references:
  - overview.md
  - module-design.md

### REQ-004
- normal_cases:
  - Brief, design, and tasks workflows succeed unchanged when `domain-map.md` is absent.
  - A repository can adopt the file later without changing old brief IDs or design IDs.
- error_cases:
  - Optional domain map support becomes a hard requirement and blocks existing repositories.
- boundary_cases:
  - The file exists but contains only one domain with no relationships and workflows still complete.
- references:
  - overview.md
  - module-design.md

### REQ-005
- normal_cases:
  - Regression fixtures and README guidance show how to populate and use the domain map.
  - Consistency or scaffold checks point maintainers to the right file when domain-aware generation is enabled.
- error_cases:
  - Golden tests pass without covering any domain map-aware output changes.
- boundary_cases:
  - Documentation describes the feature as mandatory even though the implementation remains optional.
- references:
  - overview.md
  - test-plan.md
