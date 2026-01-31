"""
Basic performance test to validate that CRUD operations complete in under 2 seconds
"""
import time
import requests
import threading
from concurrent.futures import ThreadPoolExecutor
import json

# Configuration
BASE_URL = "http://localhost:8000"
NUM_CONCURRENT_USERS = 10
OPERATIONS_PER_USER = 5

def register_and_login_user(user_num):
    """Register and login a user, return the JWT token"""
    email = f"perf_test_user_{user_num}@example.com"
    password = "SecurePassword123!"

    # Register user
    register_data = {
        "email": email,
        "name": f"Perf Test User {user_num}",
        "password": password
    }

    register_resp = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    assert register_resp.status_code == 200, f"Registration failed for user {user_num}"
    user_id = register_resp.json()["id"]

    # Login user
    login_data = {
        "email": email,
        "password": password
    }

    login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    assert login_resp.status_code == 200, f"Login failed for user {user_num}"

    token = login_resp.json()["access_token"]
    return user_id, token

def measure_operation_time(operation_func, *args, **kwargs):
    """Measure the time taken for an operation"""
    start_time = time.time()
    result = operation_func(*args, **kwargs)
    end_time = time.time()
    elapsed = end_time - start_time
    return elapsed, result

def create_todo(user_id, token):
    """Create a todo for a user"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    todo_data = {
        "title": f"Performance test todo {time.time()}",
        "description": "Created during performance test",
        "completed": False
    }

    response = requests.post(f"{BASE_URL}/api/{user_id}/tasks", json=todo_data, headers=headers)
    return response

def get_todos(user_id, token):
    """Get all todos for a user"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(f"{BASE_URL}/api/{user_id}/tasks", headers=headers)
    return response

def update_todo(user_id, todo_id, token):
    """Update a todo for a user"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    update_data = {
        "title": f"Updated performance test todo {time.time()}",
        "description": "Updated during performance test",
        "completed": True
    }

    response = requests.put(f"{BASE_URL}/api/{user_id}/tasks/{todo_id}", json=update_data, headers=headers)
    return response

def delete_todo(user_id, todo_id, token):
    """Delete a todo for a user"""
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.delete(f"{BASE_URL}/api/{user_id}/tasks/{todo_id}", headers=headers)
    return response

def run_performance_test():
    """Run the performance test with multiple concurrent users"""
    print(f"Starting performance test with {NUM_CONCURRENT_USERS} concurrent users...")
    print(f"Each user will perform {OPERATIONS_PER_USER} operations")

    # Register and login all users first
    user_tokens = []
    print("Setting up users...")
    for i in range(NUM_CONCURRENT_USERS):
        user_id, token = register_and_login_user(i)
        user_tokens.append((user_id, token))
        print(f"User {i} set up with ID {user_id}")

    # Track operation times
    operation_times = {
        "create": [],
        "read": [],
        "update": [],
        "delete": []
    }

    def run_user_operations(user_data):
        """Run operations for a single user"""
        user_id, token = user_data

        for op_num in range(OPERATIONS_PER_USER):
            # Create a todo
            elapsed, response = measure_operation_time(create_todo, user_id, token)
            operation_times["create"].append(elapsed)
            assert response.status_code == 200, f"Create failed: {response.text}"
            todo_id = response.json()["id"]

            # Read the todo
            elapsed, response = measure_operation_time(get_todos, user_id, token)
            operation_times["read"].append(elapsed)
            assert response.status_code == 200

            # Update the todo
            elapsed, response = measure_operation_time(update_todo, user_id, todo_id, token)
            operation_times["update"].append(elapsed)
            assert response.status_code == 200

            # Delete the todo
            elapsed, response = measure_operation_time(delete_todo, user_id, todo_id, token)
            operation_times["delete"].append(elapsed)
            assert response.status_code == 200

    print("Running concurrent operations...")
    start_total = time.time()

    # Run operations concurrently
    with ThreadPoolExecutor(max_workers=NUM_CONCURRENT_USERS) as executor:
        futures = [executor.submit(run_user_operations, user_data) for user_data in user_tokens]

        # Wait for all to complete
        for future in futures:
            future.result()

    end_total = time.time()
    total_time = end_total - start_total

    # Calculate statistics
    avg_times = {}
    max_times = {}
    for op_type, times in operation_times.items():
        if times:
            avg_times[op_type] = sum(times) / len(times)
            max_times[op_type] = max(times)
        else:
            avg_times[op_type] = 0
            max_times[op_type] = 0

    # Print results
    print("\n=== PERFORMANCE TEST RESULTS ===")
    print(f"Total test time: {total_time:.2f} seconds")
    print(f"Total operations: {sum(len(times) for times in operation_times.values())}")

    print("\nOperation timing:")
    for op_type in ["create", "read", "update", "delete"]:
        print(f"  {op_type.upper()}:")
        print(f"    Average time: {avg_times[op_type]:.3f}s")
        print(f"    Max time: {max_times[op_type]:.3f}s")
        print(f"    All times under 2s: {'YES' if max_times[op_type] < 2.0 else 'NO'}")

    # Evaluate success criteria
    print("\n=== EVALUATION ===")
    all_under_2s = all(max_time < 2.0 for max_time in max_times.values())
    print(f"All operations completed in under 2 seconds: {'PASS' if all_under_2s else 'FAIL'}")

    if all_under_2s:
        print("✅ Performance requirements met!")
    else:
        print("❌ Performance requirements not met!")
        for op_type, max_time in max_times.items():
            if max_time >= 2.0:
                print(f"  - {op_type} operations took {max_time:.3f}s (exceeds 2s limit)")

    return all_under_2s

if __name__ == "__main__":
    # Make sure the API is running
    try:
        resp = requests.get(f"{BASE_URL}/health")
        if resp.status_code != 200:
            print(f"❌ API not responding properly. Health check returned {resp.status_code}")
            exit(1)
        print(f"✅ API is running at {BASE_URL}")
    except requests.ConnectionError:
        print(f"❌ Cannot connect to API at {BASE_URL}")
        print("Please start the backend server before running this test")
        exit(1)

    run_performance_test()