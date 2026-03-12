from __future__ import annotations

from speckit_for_projects.services.task_ledger import merge_task_execution_history


def test_merge_task_execution_history_preserves_mutable_sections():
    existing = """# Tasks For 001-sample

- brief_id: 001-sample
- design_id: 001-sample

## Execution Assumptions
- existing assumption

## Tasks
### TASK-001 Build API
- requirement_ids:
  - REQ-001
- artifact_refs:
  - api-design.md
- depends_on:
  - none
- implementation_notes:
  - old note

#### Execution Status
- status: in_progress
- owner: dev
- last_updated: 2026-03-11

#### Checklist
- [x] implement code
- [ ] add or update tests
- [ ] run local verification
- [ ] review diff

#### Implementation Log
- 2026-03-11 Started implementation

#### Changed Files
- src/app.py

#### Verification Results
- status: failed
- commands:
  - pytest
- notes:
  - one test still failing

## Dependency Order
- TASK-001

## Test References
- REQ-001 -> test-design.md / test-plan.md
"""
    regenerated = """# Tasks For 001-sample

- brief_id: 001-sample
- design_id: 001-sample

## Execution Assumptions
- regenerated assumption

## Tasks
### TASK-001 Build API
- requirement_ids:
  - REQ-001
- artifact_refs:
  - module-design.md
- depends_on:
  - none
- implementation_notes:
  - new note

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
"""

    merged = merge_task_execution_history(regenerated, existing)

    assert "- artifact_refs:\n  - module-design.md" in merged
    assert "- status: in_progress" in merged
    assert "- 2026-03-11 Started implementation" in merged
    assert "- src/app.py" in merged
    assert "- status: failed" in merged


def test_merge_task_execution_history_archives_removed_tasks():
    existing = """# Tasks For 001-sample

- brief_id: 001-sample
- design_id: 001-sample

## Execution Assumptions
- assumption

## Tasks
### TASK-001 Build API
- requirement_ids:
  - REQ-001
- artifact_refs:
  - api-design.md
- depends_on:
  - none
- implementation_notes:
  - old note

#### Execution Status
- status: done
- owner:
- last_updated: 2026-03-11

#### Checklist
- [x] implement code
- [x] add or update tests
- [x] run local verification
- [x] review diff

#### Implementation Log
- 2026-03-11 Finished

#### Changed Files
- src/app.py

#### Verification Results
- status: passed
- commands:
  - pytest
- notes:
  - all green

## Dependency Order
- TASK-001

## Test References
- REQ-001 -> test-design.md / test-plan.md
"""
    regenerated = """# Tasks For 001-sample

- brief_id: 001-sample
- design_id: 001-sample

## Execution Assumptions
- assumption

## Tasks
### TASK-002 Build UI
- requirement_ids:
  - REQ-002
- artifact_refs:
  - overview.md
- depends_on:
  - none
- implementation_notes:
  - new task

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
- TASK-002

## Test References
- REQ-002 -> test-design.md / test-plan.md
"""

    merged = merge_task_execution_history(regenerated, existing)

    assert "## Archived Execution History" in merged
    assert "### TASK-001 Build API" in merged
    assert "- 2026-03-11 Finished" in merged
    assert "### TASK-002 Build UI" in merged
