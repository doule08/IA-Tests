import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db.session import Base, get_db_session

TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestingSessionLocal = async_sessionmaker(
    bind=test_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False
)


async def override_get_db_session():
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db_session] = override_get_db_session

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert "Bienvenue sur l'API ToDo List!" in response.json()["message"]


def test_crud_todo_workflow():
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
