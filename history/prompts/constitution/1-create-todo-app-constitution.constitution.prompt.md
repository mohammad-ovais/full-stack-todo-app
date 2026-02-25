---
id: 1
title: Create Todo App Constitution
stage: constitution
date: 2026-01-30
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: [constitution,spec-driven-development,auth,jwt,nextjs,fastapi]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
---

## Prompt

```text
Project: Multi-user Todo Web App using Next.js, FastAPI, SQLModel, Neon DB, Better Auth, and Agentic Dev Stack
Goal: Spec → Plan → Tasks → Code (no manual coding)

Core Principles

Follow the Spec Architect's specification strictly.

Frontend, backend, DB, and auth responsibilities must stay separate.

All APIs, schemas, and auth rules must be consistent across services.

Every endpoint must be protected with JWT authentication.

No manual code edits—only agent-generated code allowed.

Development Standards
Auth

Better Auth must issue JWT tokens.

FastAPI must verify JWT using same BETTER_AUTH_SECRET.

All queries must filter data by authenticated user.

Database

SQLModel schema: Task table with user_id foreign key.

Neon PostgreSQL used for storage.

CRUD operations must always enforce user ownership.

API

Use strict RESTful endpoints:

GET/POST /api/{user_id}/tasks

GET/PUT/DELETE /api/{user_id}/tasks/{id}

PATCH /api/{user_id}/tasks/{id}/complete

Frontend

Next.js App Router

API client must attach JWT token to all requests.

UI must be responsive.

Constraints

Only stack-approved technologies allowed.

All tasks must include inputs, outputs, and acceptance criteria.

No feature beyond specification.

Success Criteria

JWT auth fully working (login → token → backend verify).

CRUD endpoints functional and secure.

Neon DB connected + schema consistent.

Frontend task UI working with real API.

Entire project generated through agent workflow only.
```

## Response snapshot

Created a comprehensive constitution for the Multi-user Todo Web App project that establishes core principles, technical standards, and development workflow requirements. The constitution enforces Spec-Driven Development, separation of concerns, security-first architecture, API contract consistency, data integrity, and test-first development practices. It also defines specific standards for authentication, database operations, API design, and frontend development aligned with the specified technology stack.

## Outcome

- ✅ Impact: Created foundational constitution document that will guide all development activities
- 🧪 Tests: N/A (documentation creation)
- 📁 Files: Updated .specify/memory/constitution.md with comprehensive project principles
- 🔁 Next prompts: Proceed with spec creation following the constitution guidelines
- 🧠 Reflection: Constitution establishes clear governance framework for the agentic development process

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create feature specification based on constitution