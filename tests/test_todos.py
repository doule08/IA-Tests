import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.core.config import settings

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Bienvenue sur l'API ToDo List!" in response.json()["message"]


def test_crud_todo_workflow(tmp_path):
    # Override settings file path for testing
    test_json_file = tmp_path / "test_todos.json"
    settings.todos_file_path = test_json_file

    # 1. Create a Todo
    create_payload = {
        "title": "Acheter du lait",
        "description": "2 bouteilles de lait demi-écrémé"
    }
    response = client.post("/api/v1/todos/", json=create_payload)
    assert response.status_code == 201
    created_todo = response.json()
    assert created_todo["title"] == "Acheter du lait"
    assert created_todo["is_completed"] is False
    todo_id = created_todo["id"]

    # 2. Get Todo by ID
    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id

    # 3. List Todos
    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    todos_list = response.json()
    assert len(todos_list) == 1

    # 4. Update Todo
    update_payload = {"is_completed": True}
    response = client.put(f"/api/v1/todos/{todo_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["is_completed"] is True

    # 5. Filter Completed Todos
    response = client.get("/api/v1/todos/?is_completed=true")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # 6. Delete Todo
    response = client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 204

    # 7. Verify Deleted
    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 404
