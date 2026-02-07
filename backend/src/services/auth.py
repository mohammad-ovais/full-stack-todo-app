from sqlmodel import Session, select
from passlib.context import CryptContext
from typing import Optional
from datetime import timedelta
from ..models.user import User, UserCreate
from ..utils.jwt import create_access_token
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """Hash a plaintext password."""
    # Truncate password to 72 bytes to comply with bcrypt limitations
    # Note: bcrypt has a 72-byte limit; truncating ensures compatibility
    if len(password.encode('utf-8')) > 72:
        password = password.encode('utf-8')[:72].decode('utf-8', errors='ignore')
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(session: Session, email: str, password: str) -> Optional[User]:
    """Authenticate a user by email and password."""
    statement = select(User).where(User.email == email)
    user = session.exec(statement).first()

    if not user or not verify_password(password, user.hashed_password):
        return None

    return user

def create_user(session: Session, user_create: UserCreate) -> User:
    """Create a new user with hashed password."""
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == user_create.email)).first()
    if existing_user:
        raise ValueError("User with this email already exists")

    # Hash the password
    hashed_password = hash_password(user_create.password)

    # Create the user
    db_user = User(
        email=user_create.email,
        name=user_create.name,
        hashed_password=hashed_password
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user

def create_access_token_for_user(user_id: int) -> str:
    """Create an access token for a user."""
    data = {"sub": str(user_id)}
    expires_delta = timedelta(minutes=30)  # Token expires in 30 minutes
    return create_access_token(data=data, expires_delta=expires_delta)