# Quickstart Guide: Todo Full-Stack Web Application

**Feature**: Todo Full-Stack Web Application
**Date**: 2026-01-30
**Branch**: 001-todo-web-app

## Overview

This guide provides step-by-step instructions to set up and run the multi-user todo web application locally. The application consists of a Next.js frontend, FastAPI backend, and Neon PostgreSQL database with Better Auth for JWT authentication.

## Prerequisites

- Node.js 18+ (for frontend development)
- Python 3.11+ (for backend development)
- PostgreSQL-compatible database (Neon recommended)
- Git
- Package managers: pip and npm/yarn

## Environment Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup

#### Navigate to backend directory
```bash
cd backend
```

#### Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### Install dependencies
```bash
pip install -r requirements.txt
# If requirements.txt doesn't exist yet, install core dependencies:
pip install fastapi uvicorn sqlmodel python-multipart better-exceptions python-jose[cryptography] passlib[bcrypt] python-dotenv psycopg2-binary
```

#### Set up environment variables
Create a `.env` file in the backend directory:
```env
DATABASE_URL=postgresql://username:password@localhost:5432/todo_app
BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
BETTER_AUTH_DATABASE_URL=${DATABASE_URL}
```

### 3. Frontend Setup

#### Navigate to frontend directory
```bash
cd frontend  # or cd ../frontend if you're in the backend directory
```

#### Install dependencies
```bash
npm install
# or yarn install
```

#### Set up environment variables
Create a `.env.local` file in the frontend directory:
```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
NEXTAUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:8000/auth
```

## Database Setup

### 1. Set up Neon PostgreSQL Database
1. Create a Neon account at https://neon.tech/
2. Create a new project
3. Copy the connection string and update your backend `.env` file

### 2. Run Database Migrations
From the backend directory:
```bash
# Create and run migrations (you'll need to implement this based on your SQLModel setup)
python -c "
from sqlmodel import SQLModel
from backend.database.database import engine
from backend.models.user import User
from backend.models.todo import Todo

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

if __name__ == '__main__':
    create_db_and_tables()
"
```

## Running the Application

### 1. Start the Backend Server

From the backend directory:
```bash
uvicorn src.main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### 2. Start the Frontend Development Server

From the frontend directory:
```bash
npm run dev
# or yarn dev
```

The frontend will be available at `http://localhost:3000`

## API Endpoints

Once running, the backend provides these authenticated endpoints:

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token
- `POST /auth/logout` - Logout (optional)

### Todo Management
- `GET /api/{user_id}/tasks` - Get user's todos
- `POST /api/{user_id}/tasks` - Create new todo
- `GET /api/{user_id}/tasks/{id}` - Get specific todo
- `PUT /api/{user_id}/tasks/{id}` - Update todo
- `DELETE /api/{user_id}/tasks/{id}` - Delete todo
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Testing the Application

### Backend Tests
From the backend directory:
```bash
pytest
```

### Frontend Tests
From the frontend directory:
```bash
npm test
# or yarn test
```

## Development Workflow

### Backend Development
1. Make changes to Python files in `src/`
2. The server will automatically reload due to `--reload` flag
3. Update tests in `tests/` as needed

### Frontend Development
1. Make changes to React components in `src/app/` or `src/components/`
2. The development server will hot-reload changes
3. Update tests in `tests/` as needed

## Configuration Notes

### Environment Variables Explained

**Backend (.env)**:
- `DATABASE_URL`: Connection string for PostgreSQL database
- `BETTER_AUTH_SECRET`: Secret key for JWT signing/verification
- `BETTER_AUTH_DATABASE_URL`: Database connection for authentication

**Frontend (.env.local)**:
- `NEXT_PUBLIC_API_BASE_URL`: Base URL for API calls
- `NEXTAUTH_SECRET`: Must match the backend secret for JWT validation
- `NEXT_PUBLIC_BETTER_AUTH_URL`: Authentication endpoint URL

### Security Notes
- Never commit `.env` files to version control
- Use strong, random secrets for JWT signing
- Ensure HTTPS in production environments
- Validate all user inputs and sanitize outputs

## Troubleshooting

### Common Issues

**Database Connection Errors**:
- Verify your database URL is correct
- Check that your database service is running
- Ensure firewall rules allow connections

**Authentication Failing**:
- Confirm that JWT secrets match between frontend and backend
- Verify that authentication endpoints are accessible

**CORS Issues**:
- Check that your frontend domain is allowed in backend CORS settings
- Verify that authentication headers are properly forwarded

### Debugging Tips
- Enable debug logging in your `.env` files
- Use browser developer tools to inspect network requests
- Check server logs for error messages
- Verify JWT token format and validity

## Next Steps

1. Customize the UI components in the frontend directory
2. Extend the data models with additional fields as needed
3. Implement additional API endpoints
4. Add more comprehensive tests
5. Set up CI/CD pipelines
6. Prepare for production deployment