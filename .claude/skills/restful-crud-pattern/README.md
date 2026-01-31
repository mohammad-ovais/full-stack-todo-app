# RESTful CRUD Pattern Skill

This skill provides a consistent pattern for implementing RESTful API endpoints for todo tasks with JWT authentication and user ownership validation.

## Overview

The skill implements the standard 6 endpoint structure:
- `GET /api/{user_id}/tasks` - List all tasks for user
- `POST /api/{user_id}/tasks` - Create new task for user
- `GET /api/{user_id}/tasks/{id}` - Get specific task for user
- `PUT /api/{user_id}/tasks/{id}` - Update specific task for user
- `DELETE /api/{user_id}/tasks/{id}` - Delete specific task for user
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle task completion

## Features

- **JWT Authentication**: All endpoints validate JWT tokens
- **User Ownership**: Validates that resources belong to authenticated user
- **Proper HTTP Status Codes**: Follows REST conventions
- **Error Handling**: Comprehensive error responses
- **Input Validation**: Optional schema validation
- **Security**: Prevents unauthorized access between users

## Usage

```typescript
import { restfulCrudPattern } from './skills/restful-crud-pattern'

const taskController = restfulCrudPattern.createController({
  modelName: 'task',
  tableName: 'tasks',
  jwtService: yourJwtService,
  dbService: yourDbService,
  validationSchema: yourValidationSchema // optional
})

// Register routes
app.get('/api/:user_id/tasks', taskController.list)
app.post('/api/:user_id/tasks', taskController.create)
app.get('/api/:user_id/tasks/:id', taskController.getOne)
app.put('/api/:user_id/tasks/:id', taskController.update)
app.delete('/api/:user_id/tasks/:id', taskController.delete)
app.patch('/api/:user_id/tasks/:id/complete', taskController.toggleComplete)
```

## Response Format

All endpoints return consistent JSON responses:

Success:
```json
{
  "success": true,
  "data": { /* resource data */ }
}
```

Error:
```json
{
  "error": "Error message",
  "details": "Additional details"
}
```

## Security Notes

- User ID in URL path must match JWT token user ID
- Resources are filtered by authenticated user ID
- 404 responses for non-existent or unauthorized resources
- 403 responses for authorization mismatches