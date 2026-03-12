# Module Design

## Dependency Snapshot

```mermaid
flowchart LR
    MOD001["MOD-001 ReconciliationJob"] --> IMPORTER["SettlementImporter"]
    MOD001 --> REPOSITORY["ReconciliationRepository"]
```

## Module Boundaries

### MOD-001 ReconciliationJob
- responsibility: Orchestrate file import and reconciliation
- inputs:
  - settlement_file
- outputs:
  - reconciliation_report
- collaborators:
  - SettlementImporter
  - ReconciliationRepository
