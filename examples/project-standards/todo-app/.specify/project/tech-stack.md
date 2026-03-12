# Tech Stack

This document defines the canonical runtime, frameworks, infrastructure, and external services for the ToDo application.

## Runtime

- Language: TypeScript 5.x for application code
- Runtime: Node.js 22 LTS
- Package manager: pnpm 10
- Hosting model: single Next.js web application deployed on Vercel
- Database: PostgreSQL 16
- ORM and schema management: Prisma
- Authentication: NextAuth.js with email/password or OAuth provider support

## Frontend

- Framework: Next.js 15 App Router
- UI library: React 19
- Styling: Tailwind CSS 4
- Form handling: React Hook Form
- Input validation: Zod
- State strategy:
  - server state is fetched through server components or route handlers
  - local UI state stays inside client components
  - cross-screen client state should be minimized

## Backend

- API style: Next.js Route Handlers and Server Actions
- Business logic location: `src/features/<feature>/server/`
- Database access location: Prisma repositories under `src/server/repositories/`
- Background work: cron-based reminder or cleanup jobs are optional and isolated from request handling

## Quality And Operations

- Unit tests: Vitest
- UI and integration tests: React Testing Library
- End-to-end tests: Playwright
- Linting: ESLint
- Formatting: Prettier
- Error tracking: Sentry
- Structured logging: Pino-compatible JSON logs
- CI:
  - typecheck
  - lint
  - unit and integration tests
  - Prisma migration validation
  - Playwright smoke test on main flows

## External Services

- Email delivery provider for password reset and reminder notifications
- Sentry for exception and performance monitoring
- Vercel-managed deployment platform

## Constraints

- The application must remain operable as a single service until scale or domain complexity justifies service separation.
- Browser support targets the latest stable Chrome, Safari, Edge, and Firefox.
- Core task operations must work without introducing real-time infrastructure.
