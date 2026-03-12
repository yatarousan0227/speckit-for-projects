# Batch Design

## Execution Snapshot

```mermaid
flowchart LR
    SCHEDULE["Nightly Schedule 02:00 JST"] --> JOB["Reconciliation Worker"]
    JOB --> FILE["Settlement File Import"]
    FILE --> REPORT["Reconciliation Report Output"]
```

## Batch And Async Responsibilities

- applicable: yes
- trigger: nightly schedule at 02:00 JST
- purpose: Import settlement file and reconcile transactions
- dependencies:
  - External settlement file delivery
