# API Design

## Interfaces

### API-001 Load domain map context
- method: READ
- path: .specify/project/domain-map.md
- purpose: Load optional domain boundary and related brief metadata into command execution context.
- request:
  - command name such as `sdd.brief`, `sdd.design`, or `sdd.tasks`
  - current brief or design target when applicable
- response:
  - normalized domain entries
  - related brief references
  - upstream and downstream dependency notes

### API-002 Write domain-aware brief output
- method: WRITE
- path: briefs/<brief-id>.md
- purpose: Persist domain alignment and related brief references in generated brief documents when domain map context exists.
- request:
  - normalized brief content
  - resolved domain ownership
  - related brief list
- response:
  - regenerated brief with domain metadata sections and source references

### API-003 Write domain-aware design bundle output
- method: WRITE
- path: designs/<design-id>/
- purpose: Propagate domain dependencies and related brief references into design overview, module/test artifacts, and task assumptions.
- request:
  - selected brief
  - domain map context
  - design bundle artifacts
- response:
  - regenerated design bundle with cross-domain review context
