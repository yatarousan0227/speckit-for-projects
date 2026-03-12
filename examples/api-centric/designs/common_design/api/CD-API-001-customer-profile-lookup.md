# API Design

## Interfaces

### API-001 Customer Profile Lookup
- method: GET
- path: /customers/{externalCustomerId}
- purpose: Return a normalized customer profile
- request:
  - externalCustomerId
- response:
  - customerId
  - profile
