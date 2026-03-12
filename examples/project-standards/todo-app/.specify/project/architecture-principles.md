# Architecture Principles

This file is the shared source of architectural truth for all ToDo application design bundles.

## Required Principles

- Responsibility boundaries:
  - presentation concerns belong in React components
  - application orchestration belongs in server actions or route handlers
  - domain rules belong in feature services
  - persistence concerns belong in repositories
- Dependency direction:
  - UI may depend on feature application interfaces, but not on repository implementations
  - feature services may depend on repositories and shared infrastructure
  - repositories must not depend on UI or request-specific rendering code
- Server-first rule:
  - task reads should prefer server rendering when it improves consistency and simplifies state management
  - client components should only be used for interaction-heavy UI behavior
- API ownership:
  - task lifecycle behavior is owned by the `tasks` feature
  - authentication behavior is owned by the auth layer
  - reminder delivery, if introduced, is owned by a separate notification module and must not leak into task repositories
- Data consistency:
  - the database is the source of truth for task state
  - completion status must be derived from persisted fields such as `status` and `completedAt`
  - filtering and sorting rules must be deterministic and documented in the feature design
- Security and isolation:
  - every task query and mutation must be scoped to the authenticated user
  - authorization checks must run on the server, never only in the client
- Change strategy:
  - optimize for clear feature boundaries over premature reuse
  - extract shared modules only after at least two concrete use cases exist
- Operational simplicity:
  - prefer one deployable application and one primary database
  - add queues, workers, or event-driven patterns only when measurable operational need appears

## Integration Principles

- External email delivery must be wrapped behind an internal notification interface.
- Monitoring and logging tools must remain replaceable through infrastructure adapters.
- Third-party SDK usage must stay out of core domain logic.

## Design Review Heuristics

- A design is invalid if it allows client-side bypass of ownership checks.
- A design is invalid if business rules are distributed across route handlers, components, and repositories without a clear source of truth.
- A design is invalid if it creates separate persistence models for the same task state without a reconciliation strategy.
