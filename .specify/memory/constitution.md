<!-- SYNC IMPACT REPORT:
Version change: N/A -> 1.0.0
Modified principles: N/A (new constitution)
Added sections: All sections
Removed sections: None
Templates requiring updates:
- .specify/templates/plan-template.md ✅ updated
- .specify/templates/spec-template.md ✅ updated
- .specify/templates/tasks-template.md ✅ updated
- .specify/templates/commands/*.md ✅ reviewed
Follow-up TODOs: None
-->
# Multi-user Todo Web App Constitution

## Core Principles

### I. Spec-Driven Development
All development follows the Spec → Plan → Tasks → Code workflow. No manual code edits are allowed - only agent-generated code. Every feature must have clear specifications before implementation begins.

### II. Separation of Concerns
Frontend, backend, database, and authentication responsibilities must remain separate. Clear boundaries between services prevent tight coupling and enable independent development and scaling.

### III. Security-First Architecture
All APIs must be protected with JWT authentication. Every endpoint must verify user identity and enforce data ownership. No unauthorized access to user data is permitted.

### IV. API Contract Consistency
All API schemas, authentication rules, and data contracts must be consistent across services. Changes to shared schemas require coordinated updates across all affected components.

### V. Data Integrity and Ownership
All database operations must enforce user ownership. CRUD operations must filter data by authenticated user. The Task table must include user_id foreign key for proper data isolation.

### VI. Test-First Development (NON-NEGOTIABLE)
All features must have tests written before implementation. Endpoints must be tested for authentication, authorization, and functionality. Both positive and negative test cases are required.

## Technical Standards

### Authentication Requirements
Better Auth must issue JWT tokens. FastAPI must verify JWT using the same BETTER_AUTH_SECRET. All API requests must include valid authentication headers.

### Database Standards
SQLModel schema must be used consistently. Neon PostgreSQL is the designated database. All queries must filter by authenticated user to prevent unauthorized data access.

### API Design Standards
Strict RESTful endpoints must be implemented: GET/POST /api/{user_id}/tasks, GET/PUT/DELETE /api/{user_id}/tasks/{id}, PATCH /api/{user_id}/tasks/{id}/complete. All endpoints must enforce user ownership validation.

### Frontend Standards
Next.js App Router must be used. API client must attach JWT token to all requests. UI must be responsive and handle authentication state properly.

## Development Workflow

### Technology Stack Compliance
Only stack-approved technologies are allowed: Next.js, FastAPI, SQLModel, Neon DB, Better Auth. No additional frameworks or libraries without explicit approval.

### Task Requirements
All tasks must include clear inputs, outputs, and acceptance criteria. Tasks must be testable and verifiable. Each task must contribute to one of the success criteria.

### Code Quality Standards
Smallest viable changes only. No refactoring of unrelated code. Code must follow established patterns. Proper error handling and validation required for all user inputs.

## Governance

This constitution supersedes all other development practices. All pull requests and reviews must verify compliance with these principles. Amendments require documentation, approval, and migration plan. All team members must acknowledge and follow these principles.

**Version**: 1.0.0 | **Ratified**: 2026-01-30 | **Last Amended**: 2026-01-30