import pytest
from unittest.mock import Mock, patch
from sqlmodel import Session
from src.models.user import UserCreate
from src.services.auth import create_user, authenticate_user, hash_password, verify_password

def test_hash_password():
    """Test that password hashing works correctly."""
    password = "test_password"
    hashed = hash_password(password)

    assert hashed != password  # Hashed password should not equal original
    assert verify_password(password, hashed)  # Should verify successfully

def test_verify_password_invalid():
    """Test that invalid passwords are rejected."""
    password = "test_password"
    wrong_password = "wrong_password"
    hashed = hash_password(password)

    assert not verify_password(wrong_password, hashed)  # Wrong password should fail

def test_create_user_success():
    """Test creating a new user."""
    session_mock = Mock(spec=Session)
    user_create = UserCreate(email="test@example.com", name="Test User", password="password123")

    # Mock the query result to return None (user doesn't exist)
    session_mock.exec.return_value.first.return_value = None

    with patch('src.services.auth.pwd_context') as mock_pwd_context:
        mock_pwd_context.hash.return_value = "hashed_password"

        # Mock the User model
        with patch('src.services.auth.User') as mock_user_class:
            mock_user_instance = Mock()
            mock_user_instance.id = 1
            mock_user_instance.email = "test@example.com"
            mock_user_class.return_value = mock_user_instance

            # Call the function
            result = create_user(session_mock, user_create)

            # Assertions
            session_mock.add.assert_called_once()
            session_mock.commit.assert_called_once()
            assert result is not None

def test_authenticate_user_success():
    """Test successful user authentication."""
    session_mock = Mock(spec=Session)
    user_mock = Mock()
    user_mock.id = 1
    user_mock.email = "test@example.com"
    user_mock.hashed_password = "hashed_password"

    # Mock the query result
    session_mock.exec.return_value.first.return_value = user_mock

    with patch('src.services.auth.verify_password') as mock_verify:
        mock_verify.return_value = True

        result = authenticate_user(session_mock, "test@example.com", "password123")

        assert result == user_mock

def test_authenticate_user_wrong_password():
    """Test authentication with wrong password."""
    session_mock = Mock(spec=Session)
    user_mock = Mock()
    user_mock.id = 1
    user_mock.email = "test@example.com"
    user_mock.hashed_password = "hashed_password"

    # Mock the query result
    session_mock.exec.return_value.first.return_value = user_mock

    with patch('src.services.auth.verify_password') as mock_verify:
        mock_verify.return_value = False  # Password verification fails

        result = authenticate_user(session_mock, "test@example.com", "wrong_password")

        assert result is None

def test_authenticate_user_not_found():
    """Test authentication with non-existent user."""
    session_mock = Mock(spec=Session)

    # Mock the query result to return None (user not found)
    session_mock.exec.return_value.first.return_value = None

    result = authenticate_user(session_mock, "nonexistent@example.com", "password123")

    assert result is None