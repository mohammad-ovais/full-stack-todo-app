import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from src.main import app
from src.database.database import get_session
from src.models.user import User


# Create a test database
@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(bind=engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


def test_register_user(client: TestClient):
    """Test user registration endpoint."""
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword123"
    }

    response = client.post("/auth/register", json=user_data)

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data


def test_login_user(client: TestClient, session: Session):
    """Test user login endpoint."""
    # First register a user
    user_data = {
        "email": "test@example.com",
        "name": "Test User",
        "password": "securepassword123"
    }

    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 200

    # Then try to login
    login_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_invalid_credentials(client: TestClient):
    """Test login with invalid credentials."""
    login_data = {
        "email": "nonexistent@example.com",
        "password": "wrongpassword"
    }

    response = client.post("/auth/login", json=login_data)

    assert response.status_code == 401


def test_health_endpoint(client: TestClient):
    """Test health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"