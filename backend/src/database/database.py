from sqlmodel import create_engine, Session
from sqlalchemy import event
from sqlalchemy.pool import QueuePool
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Create the engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=300,
)

def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get a database session
    """
    with Session(engine) as session:
        yield session