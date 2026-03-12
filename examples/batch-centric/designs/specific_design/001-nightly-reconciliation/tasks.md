# Tasks For 001-nightly-reconciliation

- brief_id: 001-nightly-reconciliation
- design_id: 001-nightly-reconciliation

## Execution Assumptions
- Nightly upstream exports arrive before the reconciliation batch starts.

## Tasks
### TASK-001 Build nightly reconciliation batch
- requirement_ids:
  - REQ-001
- artifact_refs:
  - batch-design.md
  - common-design-refs.yaml
- common_design_refs:
  - CD-API-001
  - CD-DATA-001
  - CD-MOD-001
- depends_on:
  - none
- implementation_notes:
  - Execute the nightly batch through the shared reconciliation service and publish the shared report contract.

#### Execution Status
- status: pending
- owner:
- last_updated:

#### Checklist
- [ ] implement code
- [ ] add or update tests
- [ ] run local verification
- [ ] review diff

#### Implementation Log
- <timestamped note>

#### Changed Files
- <repo-relative path>

#### Verification Results
- status: not_run
- commands:
  - <verification command>
- notes:
  - <result summary>

## Dependency Order
- TASK-001

## Test References
- REQ-001 -> test-design.md / test-plan.md

## Archived Execution History
### TASK-000 <archived task title>
...
