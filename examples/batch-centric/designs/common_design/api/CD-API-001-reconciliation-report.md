# API Design

## Interfaces

### API-001 Reconciliation Report Retrieval
- method: GET
- path: /reconciliation/reports/latest
- purpose: Retrieve the most recent reconciliation report
- request:
  - none
- response:
  - mismatchCount
  - reportGeneratedAt
