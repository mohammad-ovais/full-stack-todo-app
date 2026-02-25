# API Contracts: Todo Full-Stack Web Application

**Feature**: Todo Full-Stack Web Application
**Date**: 2026-01-30
**Branch**: 001-todo-web-app
**Version**: 1.0

## Overview

This document defines the API contracts between the frontend and backend services. These contracts ensure consistent communication and data exchange while maintaining the required authentication and user isolation.

## Authentication Contract

### JWT Token Format
- Algorithm: HS256
- Secret: Shared via `BETTER_AUTH_SECRET` environment variable
- Claims: `sub` (subject/user ID), `exp` (expiration), `iat` (issued at)

### Authorization Header
All protected endpoints require: `Authorization: Bearer {jwt_token}`

## REST API Endpoints

### Authentication Endpoints

#### POST /auth/register
**Description**: Register a new user account
**Authentication**: None

**Request Body**:
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2023-01-01T00:00:00Z"
}
```

**Response (400 Bad Request)**:
```json
{
  "detail": "User already exists or invalid input"
}
```

#### POST /auth/login
**Description**: Authenticate user and return JWT token
**Authentication**: None

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK)**:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

**Response (401 Unauthorized)**:
```json
{
  "detail": "Incorrect email or password"
}
```

### Todo Management Endpoints

#### GET /api/{user_id}/tasks
**Description**: Retrieve all todos for the specified user
**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): ID of the user whose tasks to retrieve

**Query Parameters**:
- `completed` (boolean, optional): Filter by completion status
- `limit` (integer, optional): Maximum number of results
- `offset` (integer, optional): Offset for pagination

**Response (200 OK)**:
```json
[
  {
    "id": 1,
    "user_id": 123,
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  },
  {
    "id": 2,
    "user_id": 123,
    "title": "Walk the dog",
    "description": null,
    "completed": true,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```

**Response (401 Unauthorized)**: Invalid or missing JWT token
**Response (403 Forbidden)**: User ID in token doesn't match path parameter
**Response (404 Not Found)**: User ID doesn't exist

#### POST /api/{user_id}/tasks
**Description**: Create a new todo for the specified user
**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): ID of the user creating the task

**Request Body**:
```json
{
  "title": "New task title",
  "description": "Task description (optional)",
  "completed": false
}
```

**Response (201 Created)**:
```json
{
  "id": 3,
  "user_id": 123,
  "title": "New task title",
  "description": "Task description (optional)",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (400 Bad Request)**: Invalid input data
**Response (401 Unauthorized)**: Invalid or missing JWT token
**Response (403 Forbidden)**: User ID in token doesn't match path parameter

#### GET /api/{user_id}/tasks/{id}
**Description**: Retrieve a specific todo by ID
**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): ID of the user who owns the task
- `id` (integer): ID of the task to retrieve

**Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-01T00:00:00Z"
}
```

**Response (401 Unauthorized)**: Invalid or missing JWT token
**Response (403 Forbidden)**: User ID in token doesn't match path parameter
**Response (404 Not Found)**: Task doesn't exist or doesn't belong to user

#### PUT /api/{user_id}/tasks/{id}
**Description**: Update an existing todo
**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): ID of the user who owns the task
- `id` (integer): ID of the task to update

**Request Body**:
```json
{
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Updated task title",
  "description": "Updated description",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

**Response (400 Bad Request)**: Invalid input data
**Response (401 Unauthorized)**: Invalid or missing JWT token
**Response (403 Forbidden)**: User ID in token doesn't match path parameter
**Response (404 Not Found)**: Task doesn't exist or doesn't belong to user

#### DELETE /api/{user_id}/tasks/{id}
**Description**: Delete a specific todo
**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): ID of the user who owns the task
- `id` (integer): ID of the task to delete

**Response (204 No Content)**: Task successfully deleted

**Response (401 Unauthorized)**: Invalid or missing JWT token
**Response (403 Forbidden)**: User ID in token doesn't match path parameter
**Response (404 Not Found)**: Task doesn't exist or doesn't belong to user

#### PATCH /api/{user_id}/tasks/{id}/complete
**Description**: Toggle the completion status of a specific todo
**Authentication**: Required

**Path Parameters**:
- `user_id` (integer): ID of the user who owns the task
- `id` (integer): ID of the task to update

**Request Body**:
```json
{
  "completed": true
}
```

**Response (200 OK)**:
```json
{
  "id": 1,
  "user_id": 123,
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2023-01-01T00:00:00Z",
  "updated_at": "2023-01-02T00:00:00Z"
}
```

**Response (400 Bad Request)**: Invalid input data
**Response (401 Unauthorized)**: Invalid or missing JWT token
**Response (403 Forbidden)**: User ID in token doesn't match path parameter
**Response (404 Not Found)**: Task doesn't exist or doesn't belong to user

## Error Response Format

All error responses follow this format:

```json
{
  "detail": "Human-readable error message"
}
```

## Security Contract

### Authentication Validation
- All protected endpoints validate JWT token format
- Token expiration is checked
- User ID in token must match the user_id path parameter for all operations
- Invalid tokens return 401 Unauthorized

### Data Isolation
- All operations filter data by the authenticated user's ID
- Users cannot access data belonging to other users
- Backend services must validate user ownership for each request

### Input Validation
- All user inputs are validated for type and format
- SQL injection prevention through parameterized queries
- Cross-site scripting (XSS) prevention through output sanitization

## Frontend API Client Contract

### Expected Response Types

**Successful Responses**:
- Use appropriate HTTP status codes (200, 201, 204)
- Return JSON objects with predictable field names
- Include timestamps in ISO 8601 format

**Error Responses**:
- Return 4xx/5xx HTTP status codes appropriately
- Include descriptive error messages in `detail` field
- Never expose sensitive internal error details

### Client Responsibilities
- Attach JWT token to all authenticated requests
- Handle 401 responses by redirecting to login
- Handle 403 responses by showing appropriate user feedback
- Parse timestamps correctly using JavaScript Date constructor