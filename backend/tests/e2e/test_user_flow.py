import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from src.main import app
from src.database.database import get_session
from src.models.user import User
from src.models.todo import Todo


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


def test_full_user_todo_flow(client: TestClient, session: Session):
    """
    End-to-end test covering the complete user flow:
    1. Register a new user
    2. Login to get JWT token
    3. Create a todo
    4. Retrieve the todo
    5. Update the todo
    6. Mark the todo as complete
    7. Delete the todo
    """

    # Step 1: Register a new user
    user_data = {
        "email": "e2e_test@example.com",
        "name": "E2E Test User",
        "password": "SecurePassword123!"
    }

    register_response = client.post("/auth/register", json=user_data)
    assert register_response.status_code == 200

    register_data = register_response.json()
    assert register_data["email"] == "e2e_test@example.com"
    assert register_data["name"] == "E2E Test User"
    assert "id" in register_data

    user_id = register_data["id"]
    assert user_id is not None

    # Step 2: Login to get JWT token
    login_data = {
        "email": "e2e_test@example.com",
        "password": "SecurePassword123!"
    }

    login_response = client.post("/auth/login", json=login_data)
    assert login_response.status_code == 200

    login_result = login_response.json()
    assert "access_token" in login_result
    assert login_result["token_type"] == "bearer"

    token = login_result["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # Step 3: Create a todo
    todo_data = {
        "title": "Test todo for E2E flow",
        "description": "This is a test todo created during E2E testing",
        "completed": False
    }

    create_todo_response = client.post(f"/api/{user_id}/tasks", json=todo_data, headers=headers)
    assert create_todo_response.status_code == 200

    created_todo = create_todo_response.json()
    assert created_todo["title"] == "Test todo for E2E flow"
    assert created_todo["description"] == "This is a test todo created during E2E testing"
    assert created_todo["completed"] is False
    assert created_todo["user_id"] == user_id

    todo_id = created_todo["id"]
    assert todo_id is not None

    # Step 4: Retrieve the todo
    get_todo_response = client.get(f"/api/{user_id}/tasks/{todo_id}", headers=headers)
    assert get_todo_response.status_code == 200

    retrieved_todo = get_todo_response.json()
    assert retrieved_todo["id"] == todo_id
    assert retrieved_todo["title"] == "Test todo for E2E flow"
    assert retrieved_todo["user_id"] == user_id

    # Step 5: Update the todo
    update_data = {
        "title": "Updated test todo",
        "description": "This is an updated test todo",
        "completed": True
    }

    update_response = client.put(f"/api/{user_id}/tasks/{todo_id}", json=update_data, headers=headers)
    assert update_response.status_code == 200

    updated_todo = update_response.json()
    assert updated_todo["id"] == todo_id
    assert updated_todo["title"] == "Updated test todo"
    assert updated_todo["description"] == "This is an updated test todo"
    assert updated_todo["completed"] is True

    # Step 6: Mark the todo as complete (toggle)
    toggle_response = client.patch(f"/api/{user_id}/tasks/{todo_id}/complete",
                                  json={"completed": False}, headers=headers)
    assert toggle_response.status_code == 200

    toggled_todo = toggle_response.json()
    assert toggled_todo["id"] == todo_id
    assert toggled_todo["completed"] is False  # Changed back to False

    # Step 7: Delete the todo
    delete_response = client.delete(f"/api/{user_id}/tasks/{todo_id}", headers=headers)
    assert delete_response.status_code == 200

    delete_result = delete_response.json()
    assert delete_result["message"] == "Todo deleted successfully"

    # Verify the todo is gone
    get_deleted_response = client.get(f"/api/{user_id}/tasks/{todo_id}", headers=headers)
    assert get_deleted_response.status_code == 404


def test_multi_user_isolation(client: TestClient, session: Session):
    """
    Test that users cannot access other users' todos
    """

    # Create first user
    user1_data = {
        "email": "user1@example.com",
        "name": "User 1",
        "password": "SecurePassword123!"
    }

    register_response1 = client.post("/auth/register", json=user1_data)
    assert register_response1.status_code == 200
    user1_id = register_response1.json()["id"]

    # Create second user
    user2_data = {
        "email": "user2@example.com",
        "name": "User 2",
        "password": "SecurePassword123!"
    }

    register_response2 = client.post("/auth/register", json=user2_data)
    assert register_response2.status_code == 200
    user2_id = register_response2.json()["id"]

    # Login as user 1
    login_data1 = {
        "email": "user1@example.com",
        "password": "SecurePassword123!"
    }

    login_response1 = client.post("/auth/login", json=login_data1)
    assert login_response1.status_code == 200
    token1 = login_response1.json()["access_token"]
    headers1 = {"Authorization": f"Bearer {token1}"}

    # Login as user 2
    login_data2 = {
        "email": "user2@example.com",
        "password": "SecurePassword123!"
    }

    login_response2 = client.post("/auth/login", json=login_data2)
    assert login_response2.status_code == 200
    token2 = login_response2.json()["access_token"]
    headers2 = {"Authorization": f"Bearer {token2}"}

    # User 1 creates a todo
    todo_data = {
        "title": "User 1's private todo",
        "description": "This should only be accessible to user 1",
        "completed": False
    }

    create_todo_response = client.post(f"/api/{user1_id}/tasks", json=todo_data, headers=headers1)
    assert create_todo_response.status_code == 200
    todo_id = create_todo_response.json()["id"]

    # User 2 tries to access user 1's todo (should fail)
    attempt_response = client.get(f"/api/{user1_id}/tasks/{todo_id}", headers=headers2)
    assert attempt_response.status_code == 403  # Forbidden access

    # User 1 can access their own todo
    own_access_response = client.get(f"/api/{user1_id}/tasks/{todo_id}", headers=headers1)
    assert own_access_response.status_code == 200

    # User 2 can access their own (empty) list
    user2_todos_response = client.get(f"/api/{user2_id}/tasks", headers=headers2)
    assert user2_todos_response.status_code == 200
    assert user2_todos_response.json() == []