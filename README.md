# Todo Full-Stack Web Application

A multi-user todo web application built with Next.js (App Router), FastAPI, SQLModel, Neon PostgreSQL, and Better Auth. The system provides JWT-based authentication, user-isolated todo management, and secure API endpoints.

## Features

- User registration and authentication with JWT tokens
- Secure todo management with create, read, update, delete, and completion functionality
- Multi-user isolation - users can only access their own todos
- Responsive web interface built with Next.js
- FastAPI backend with SQLModel ORM
- Neon PostgreSQL database

## Tech Stack

- **Frontend**: Next.js 16+, React, TypeScript
- **Backend**: FastAPI, Python 3.11+
- **Database**: SQLModel with Neon PostgreSQL
- **Authentication**: JWT with Better Auth
- **Testing**: pytest (backend), Jest (frontend)

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL-compatible database (Neon recommended)

### Docker Setup (Recommended)

The easiest way to run the application is using Docker Compose:

1. Make sure Docker and Docker Compose are installed
2. Update the environment variables in `docker-compose.yml` as needed
3. Run the application:
   ```bash
   docker-compose up
   ```
4. The frontend will be available at `http://localhost:3000`
5. The backend API will be available at `http://localhost:8000`

### Manual Setup

#### Backend Setup

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables by creating a `.env` file:
   ```env
   DATABASE_URL=postgresql://todo_user:todo_password@localhost:5432/todo_db
   BETTER_AUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
   ```

5. Run the application:
   ```bash
   uvicorn src.main:app --reload --port 8000
   ```

#### Frontend Setup

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Set up environment variables by creating a `.env.local` file:
   ```env
   NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
   NEXTAUTH_SECRET=your-super-secret-jwt-key-here-make-it-long-and-random
   ```

4. Run the development server:
   ```bash
   npm run dev
   ```

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and receive JWT token

### Todo Management
- `GET /api/{user_id}/tasks` - Get user's todos
- `POST /api/{user_id}/tasks` - Create new todo
- `GET /api/{user_id}/tasks/{id}` - Get specific todo
- `PUT /api/{user_id}/tasks/{id}` - Update todo
- `DELETE /api/{user_id}/tasks/{id}` - Delete todo
- `PATCH /api/{user_id}/tasks/{id}/complete` - Toggle completion status

## Architecture

The application follows a clean architecture with separation of concerns:
- **Frontend**: Next.js App Router with authentication and todo management components
- **Backend**: FastAPI with SQLModel models, service layer, and API routes
- **Database**: Neon PostgreSQL with proper indexing and foreign key relationships
- **Authentication**: JWT-based with proper middleware and validation

## Security

- JWT tokens for authentication and authorization
- User data isolation at the database level
- Input validation and sanitization
- Secure password hashing
- Rate limiting and protection against common attacks

## Testing

To run backend tests:
```bash
cd backend
python -m pytest
```

To run frontend tests (when implemented):
```bash
cd frontend
npm test
```

## Deployment

The application can be deployed using the provided Docker configuration:
1. Build the containers: `docker-compose build`
2. Run the application: `docker-compose up -d`

For production deployments, make sure to:
- Use strong, randomly generated secrets
- Configure SSL certificates
- Set up a reverse proxy (nginx, Apache)
- Configure proper logging and monitoring
- Set up automated backups for the database