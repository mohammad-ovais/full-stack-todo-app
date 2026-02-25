# Implementation Plan: Todo Full-Stack Web Application

**Branch**: `001-todo-web-app` | **Date**: 2026-01-30 | **Spec**: specs/001-todo-web-app/spec.md
**Input**: Feature specification from `/specs/[###-feature-name]/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Implementation of a multi-user todo web application using Next.js (App Router), FastAPI, SQLModel, Neon PostgreSQL, and Better Auth. The system will provide JWT-based authentication, user-isolated todo management, and secure API endpoints following the agentic dev stack approach.

## Technical Context

**Language/Version**: Python 3.11 (FastAPI), JavaScript/TypeScript (Next.js 16+)
**Primary Dependencies**: FastAPI, SQLModel, Neon PostgreSQL, Better Auth, Next.js App Router
**Storage**: Neon PostgreSQL with SQLModel ORM
**Testing**: pytest (backend), Jest/Vitest (frontend)
**Target Platform**: Web application (Linux server deployment)
**Project Type**: Web (frontend + backend + auth)
**Performance Goals**: <2 seconds for CRUD operations, 1000 concurrent users
**Constraints**: <200ms p95 response time, JWT authentication on all endpoints, multi-user data isolation
**Scale/Scope**: Multi-user support with individual data isolation

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ Spec-Driven Development: Following Plan → Tasks → Code workflow
- ✅ Separation of Concerns: Frontend, backend, database, and auth responsibilities separate
- ✅ Security-First Architecture: JWT authentication on all endpoints
- ✅ API Contract Consistency: Consistent schemas across services
- ✅ Data Integrity and Ownership: SQLModel schema with user_id foreign key
- ✅ Test-First Development: Testing strategy defined for all layers

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-web-app/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── todo.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── todo_service.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── auth_routes.py
│   │   └── todo_routes.py
│   ├── middleware/
│   │   └── auth_middleware.py
│   ├── database/
│   │   └── database.py
│   └── main.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── requirements.txt

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   ├── register/
│   │   └── dashboard/
│   ├── components/
│   │   ├── TodoList.tsx
│   │   ├── TodoForm.tsx
│   │   └── ProtectedRoute.tsx
│   ├── services/
│   │   ├── api.ts
│   │   └── auth.ts
│   ├── types/
│   │   └── index.ts
│   └── utils/
│       └── jwt.ts
├── tests/
├── public/
└── package.json

shared/
├── types/
│   └── api.ts
└── constants/
    └── index.ts
```

**Structure Decision**: Selected web application structure with separate backend and frontend directories to maintain clear separation of concerns between server-side logic and client-side presentation. Includes shared types for API contract consistency.

## Major Technical Decisions

| Decision | Options Considered | Chosen Option | Rationale |
|----------|-------------------|---------------|-----------|
| Authentication Method | JWT vs Session-based | JWT with Better Auth | Aligns with specification requirement, enables stateless API, compatible with multi-user isolation |
| Database Schema | Direct SQL vs ORM vs SQLModel | SQLModel with Neon PostgreSQL | Matches specification requirements, provides type safety, integrates well with FastAPI |
| Frontend API Client | Raw fetch vs Axios vs Custom | Custom API client with JWT attachment | Ensures JWT tokens are attached to all requests as required by spec |
| API Route Design | REST vs GraphQL | REST with user_id segmentation | Matches specification requirement for REST endpoints: /api/{user_id}/tasks |
| Task Ownership Enforcement | Backend only vs Frontend + Backend | Backend enforcement with frontend validation | Critical security requirement - backend must enforce ownership regardless of frontend |
| Connection Handling | Connection pooling vs Single connection | Connection pooling with Neon | Ensures scalability and proper resource management for multi-user application |

## Development Phases

### Foundation Phase
- Set up project structure with backend and frontend directories
- Configure environment variables and secrets management
- Initialize dependency management (pip for backend, npm for frontend)
- Set up basic configuration files and shared types

### Backend Layer
- Implement SQLModel database schema with user and todo models
- Create JWT authentication with Better Auth integration
- Build FastAPI routes for user registration/login and protected todo endpoints
- Implement auth middleware for JWT verification
- Create service layer for business logic

### Frontend Layer
- Set up Next.js App Router with protected routes
- Implement authentication UI (login/register)
- Create todo management UI components
- Build API client that attaches JWT tokens to requests
- Implement user dashboard for todo management

### Integration Phase
- Connect frontend to backend API
- Configure CORS and environment-specific settings
- Implement error handling and user feedback mechanisms
- Set up proper deployment configurations

### Validation Phase
- Implement comprehensive testing suite
- Verify JWT authentication and authorization
- Test multi-user data isolation
- Validate all API contracts and success criteria

## Testing Strategy

- **Unit Tests**: Individual function and component testing
- **Integration Tests**: API endpoint validation and auth flow verification
- **Contract Tests**: API schema consistency between frontend and backend
- **Security Tests**: JWT verification, authorization failures, data isolation
- **End-to-End Tests**: Full user journey validation from registration to todo management

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Multiple project structure | Web application requires separate frontend/backend | Monolithic approach would violate separation of concerns principle |