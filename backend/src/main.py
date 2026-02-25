from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .database.database import engine
from sqlmodel import SQLModel
from .models.user import User
from .models.todo import Todo


# Import routers
from .api.auth_routes import router as auth_router
from .api.todo_routes import router as todo_router

# Import logging and security configuration
from .config.logging_config import logger
from .config.security import setup_security_headers, setup_rate_limiting

# Create the FastAPI app
app = FastAPI(title="Todo API", version="1.0.0")

# Set up security configurations
setup_security_headers(app)
setup_rate_limiting(app)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,  # Using Bearer tokens, not cookies
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(todo_router, prefix="/api", tags=["todos"])

@app.on_event("startup")
async def startup_event():
    """Create database tables on startup"""
    SQLModel.metadata.create_all(engine)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Todo API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}