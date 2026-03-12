# API Design

## Interfaces

### API-001 Application Search
- method: GET
- path: /applications
- purpose: Return filtered application list
- request:
  - applicantName
  - status
- response:
  - applicationId
  - applicantName
