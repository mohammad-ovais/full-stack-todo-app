# Data Model: Todo Full-Stack Web Application

**Feature**: Todo Full-Stack Web Application
**Date**: 2026-01-30
**Branch**: 001-todo-web-app
**Model Version**: 1.0

## Overview

This document defines the database schema for the multi-user todo web application using SQLModel. The data model ensures user data isolation and supports all required functionality as specified in the feature requirements.

## Entity Relationship Diagram (Conceptual)

```
┌─────────┐    ┌──────────────┐
│  User   │    │     Todo     │
├─────────┤    ├──────────────┤
│ id (PK) │◄───┤ user_id (FK) │
│ email   │    │ id (PK)      │
│ name    │    │ title        │
│ created │    │ description  │
└─────────┘    │ completed    │
               │ created_at   │
               │ updated_at   │
               └──────────────┘
```

## Detailed Entity Definitions

### User Entity

**Purpose**: Represents an authenticated user of the application

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID / Integer | PRIMARY KEY, NOT NULL, AUTO_INCREMENT | Unique identifier for the user |
| email | String(255) | UNIQUE, NOT NULL | User's email address for authentication |
| name | String(255) | NOT NULL | User's display name |
| hashed_password | String(255) | NOT NULL | BCrypt hashed password |
| created_at | DateTime | NOT NULL, DEFAULT NOW() | Timestamp of user creation |
| updated_at | DateTime | NOT NULL, DEFAULT NOW() | Timestamp of last update |

**Indexes**:
- PRIMARY KEY (id)
- UNIQUE INDEX (email)

**Relationships**:
- One-to-Many: User → Todos (via user_id foreign key)

### Todo Entity

**Purpose**: Represents a task item owned by a specific user

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| id | UUID / Integer | PRIMARY KEY, NOT NULL, AUTO_INCREMENT | Unique identifier for the todo |
| user_id | UUID / Integer | FOREIGN KEY, NOT NULL | Reference to the owning user |
| title | String(255) | NOT NULL | Title/description of the task |
| description | Text | NULL | Optional detailed description of the task |
| completed | Boolean | NOT NULL, DEFAULT FALSE | Completion status of the task |
| created_at | DateTime | NOT NULL, DEFAULT NOW() | Timestamp of todo creation |
| updated_at | DateTime | NOT NULL, DEFAULT NOW() | Timestamp of last update |

**Indexes**:
- PRIMARY KEY (id)
- INDEX (user_id) - For efficient user-based queries
- INDEX (completed) - For efficient filtering by completion status

**Relationships**:
- Many-to-One: Todo → User (via user_id foreign key)

## SQL Schema Definition

```sql
-- Users table
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Todos table
CREATE TABLE todos (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Indexes for performance
CREATE INDEX idx_todos_user_id ON todos(user_id);
CREATE INDEX idx_todos_completed ON todos(completed);
```

## SQLModel Class Definitions

### User Model

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, nullable=False)
    name: str = Field(nullable=False)

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to todos
    todos: list["Todo"] = Relationship(back_populates="user")

class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UserCreate(UserBase):
    password: str  # Plain text password for hashing

class UserUpdate(SQLModel):
    email: Optional[str] = None
    name: Optional[str] = None
```

### Todo Model

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

class TodoBase(SQLModel):
    title: str = Field(nullable=False)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)

class Todo(TodoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: "User" = Relationship(back_populates="todos")

class TodoRead(TodoBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

class TodoCreate(TodoBase):
    pass

class TodoUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
```

## Data Integrity Constraints

### Foreign Key Constraints
- `todos.user_id` references `users.id` with CASCADE delete
- Ensures referential integrity between users and their todos

### Unique Constraints
- `users.email` is unique to prevent duplicate accounts

### Not Null Constraints
- Critical fields are enforced as NOT NULL to maintain data integrity
- `user_id` in todos ensures every todo is associated with a user

## Query Patterns

### Common Queries

**Retrieve user's todos**:
```sql
SELECT * FROM todos WHERE user_id = $1 ORDER BY created_at DESC;
```

**Check todo ownership**:
```sql
SELECT COUNT(*) FROM todos WHERE id = $1 AND user_id = $2;
```

**Update todo status**:
```sql
UPDATE todos SET completed = $1, updated_at = NOW()
WHERE id = $2 AND user_id = $3;
```

### Security Validation
All queries must validate user ownership to enforce multi-user isolation.

## Migration Strategy

### Initial Schema Migration
1. Create users table
2. Create todos table
3. Create indexes
4. Verify constraints

### Future Extension Points
- Additional user profile fields
- Category/tags for todos
- Due dates and reminders
- Priority levels

## Security Considerations

### Data Isolation
- Every query must filter by `user_id` to prevent cross-user data access
- Foreign key constraints prevent orphaned records
- CASCADE delete ensures data cleanup when users are removed

### Access Control
- Backend services must validate JWT and extract user ID
- All database operations must use the validated user ID
- Direct database access should be restricted

## Performance Optimizations

### Indexing Strategy
- Primary keys indexed automatically
- Foreign key columns indexed for join performance
- Frequently queried boolean fields indexed

### Query Optimization
- Use prepared statements to prevent SQL injection
- Implement pagination for large result sets
- Cache frequently accessed user metadata

## Validation Rules

### Business Logic Constraints
- Users cannot modify/delete other users' todos
- Todo titles must not be empty
- User emails must follow standard email format

### Data Format Validation
- Email fields validated against standard email format
- Timestamps stored in UTC timezone
- Boolean fields restricted to true/false values