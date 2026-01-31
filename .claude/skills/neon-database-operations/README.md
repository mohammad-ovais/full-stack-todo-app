# Neon Database Operations Skill

This skill handles Neon Serverless PostgreSQL connections and SQLModel queries with user data isolation and secure error handling.

## Overview

The skill provides a complete set of utilities for managing Neon PostgreSQL connections with SQLModel, including:
- Async engine creation with proper connection pooling
- FastAPI session dependencies
- User-filtered queries with WHERE user_id enforcement
- Secure transaction management
- Proper error handling (no raw database errors exposed)
- Connection pooling configuration

## Features

- **Neon PostgreSQL Connection**: Creates async engine optimized for Neon's serverless connections
- **Connection Pooling**: Configurable pool sizes and connection recycling
- **User Data Isolation**: All queries enforce `WHERE user_id = authenticated_user_id`
- **FastAPI Integration**: Provides session dependency for DI
- **Transaction Support**: Proper transaction management with rollback on errors
- **Secure Error Handling**: Raw database errors are never exposed to API responses
- **Record Ownership**: Validates that records belong to authenticated user before operations

## Usage

```typescript
import { neonDatabaseOperations } from './skills/neon-database-operations'

// Create async engine for Neon
const connectionString = process.env.NEON_DATABASE_URL!;
const engine = neonDatabaseOperations.createAsyncEngine(
  connectionString,
  10,  // pool size
  20   // max overflow
);

// Create FastAPI session dependency
const get_db_session = neonDatabaseOperations.createSessionDependency(engine);

// Define your SQLModel (must include user_id field for isolation)
class Task(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str
  completed: bool = False
  user_id: int  // Critical for data isolation

// Use in your API endpoint with user authentication
@app.get("/api/{user_id}/tasks")
async def get_tasks(
  user_id: int,
  authenticated_user_id: int = Depends(get_authenticated_user_id),
  session: AsyncSession = Depends(get_db_session)
):
  # Verify user is accessing their own data
  if user_id != authenticated_user_id:
    raise HTTPException(status_code=403, detail="Access denied")

  # Use the skill's user-filtered query (enforces user_id isolation)
  tasks = await neonDatabaseOperations.executeUserFilteredQuery(
    session,
    Task,
    authenticated_user_id
  )

  return tasks
```

## Key Functions

- `createAsyncEngine(connectionString, poolSize, maxOverflow)` - Creates optimized async engine
- `createSessionDependency(engine)` - Creates FastAPI session dependency
- `executeUserFilteredQuery(session, model, authenticatedUserId, filters?)` - Queries with user isolation
- `executeSingleUserFilteredQuery(session, model, authenticatedUserId, id)` - Gets single user record
- `createRecordWithUserAssociation(session, modelInstance, authenticatedUserId)` - Creates user-bound record
- `updateUserOwnedRecord(session, modelClass, recordId, authenticatedUserId, updateData)` - Updates owned record
- `deleteUserOwnedRecord(session, modelClass, recordId, authenticatedUserId)` - Deletes owned record
- `executeTransaction(session, transactionFn)` - Executes transaction safely
- `checkRecordOwnership(session, modelClass, recordId, authenticatedUserId)` - Verifies ownership

## Security Notes

- All queries enforce `WHERE user_id = authenticated_user_id` for data isolation
- Raw database errors are caught and replaced with generic error messages
- User ID verification is enforced at the application layer
- Connection pooling prevents resource exhaustion
- Transaction rollback occurs on errors to maintain data consistency