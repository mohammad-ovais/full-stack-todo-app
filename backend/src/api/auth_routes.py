from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import Dict
from ..database.database import get_session
from ..models.user import UserCreate, User as UserModel
from ..services.auth import create_user, authenticate_user, create_access_token_for_user
from ..models.user import UserRead
from ..utils.validation import validate_password_strength

router = APIRouter()

@router.post("/register", response_model=UserRead)
def register(user: UserCreate, session: Session = Depends(get_session)):
    """Register a new user."""
    # Validate password strength before creating user
    is_valid, error_msg = validate_password_strength(user.password)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    try:
        db_user = create_user(session, user)
        return db_user
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred during registration"
        )


@router.post("/login")
def login(user_data: Dict[str, str], session: Session = Depends(get_session)):
    """Authenticate a user and return an access token."""
    email = user_data.get("email")
    password = user_data.get("password")

    if not email or not password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email and password are required"
        )

    user = authenticate_user(session, email, password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token_for_user(user.id)

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }