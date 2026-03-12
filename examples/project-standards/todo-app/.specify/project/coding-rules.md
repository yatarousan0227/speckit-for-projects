# Coding Rules

This document defines the implementation rules that all generated tasks and design artifacts must follow for the ToDo application.

## Required Rules

- Naming conventions:
  - use `PascalCase` for React components and types
  - use `camelCase` for variables, functions, and object properties
  - use `kebab-case` for route segments and non-code file names where applicable
  - use domain names consistently: `task`, `taskList`, `dueDate`, `completedAt`
- Module boundaries:
  - UI components must not call Prisma directly
  - route handlers and server actions must delegate business rules to feature-level server modules
  - repositories must not contain presentation logic
- Validation:
  - all external input must be validated with Zod before business logic runs
  - form validation rules must be defined once and reused across client and server when possible
- Error handling:
  - expected business errors must return user-safe messages and stable error codes
  - unexpected errors must be logged with request context and surfaced as generic user messages
  - do not swallow exceptions without structured logging
- Data updates:
  - every create, update, complete, reopen, and delete operation must verify the authenticated user owns the target task
  - write operations must be idempotent where retries are realistic
- Logging and monitoring:
  - logs must be structured JSON in server execution paths
  - each error log must include feature name, action name, user ID when available, and task ID when available
  - sensitive values such as access tokens, passwords, and raw session cookies must never be logged
- Review expectations:
  - pull requests must include tests or a clear rationale when tests are intentionally omitted
  - generated files must be reviewed with `git diff` before merge
- Testing expectations:
  - domain rules need unit tests
  - route handlers and server actions need integration tests for success and failure paths
  - end-to-end coverage must include task creation, completion toggle, edit, filtering, and delete flows

## Preferred File Organization

- `src/app/` for route entry points and layout wiring
- `src/features/tasks/` for task-specific UI and server logic
- `src/server/` for shared server-only infrastructure
- `src/lib/` for small cross-feature utilities with low domain coupling

## Prohibited Shortcuts

- Do not embed SQL in UI components.
- Do not duplicate validation schemas between client and server without a strong technical reason.
- Do not make client components the source of truth for task persistence state.
- Do not introduce background jobs for behavior that can be handled synchronously in the request path.
