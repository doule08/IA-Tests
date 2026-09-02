"""
Suite de tests unitaires et d'intégration pour l'API ToDo List.

Ce module valide l'ensemble du cycle de vie CRUD des tâches ToDo à l'aide de
FastAPI TestClient et d'une base de données SQLite en mémoire (`sqlite+aiosqlite:///:memory:`).
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.main import app
from app.db.session import Base, get_db_session

# URL de la base de données SQLite en mémoire pour l'isolation des tests
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
    """
    Surcharge de dépendance pour rediriger les requêtes de tests vers la base SQLite en mémoire.
    """
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with TestingSessionLocal() as session:
        yield session


# Surcharge de la dépendance FastAPI
app.dependency_overrides[get_db_session] = override_get_db_session

# Client de test HTTP FastAPI
client = TestClient(app)


def test_root_endpoint():
    """
    Teste le bon fonctionnement de l'endpoint racine `/` (Healthcheck).
    """
    response = client.get("/")
    assert response.status_code == 200
    assert "Bienvenue sur l'API ToDo List!" in response.json()["message"]


def test_crud_todo_workflow():
    """
    Teste le workflow complet CRUD (Création, Lecture, Modification, Filtrage, Suppression).
    """
    # 1. Création d'une tâche
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

    # 2. Récupération par ID
    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 200
    assert response.json()["id"] == todo_id

    # 3. Liste globale des tâches
    response = client.get("/api/v1/todos/")
    assert response.status_code == 200
    todos_list = response.json()
    assert len(todos_list) == 1

    # 4. Modification de la tâche
    update_payload = {"is_completed": True}
    response = client.put(f"/api/v1/todos/{todo_id}", json=update_payload)
    assert response.status_code == 200
    assert response.json()["is_completed"] is True

    # 5. Filtrage des tâches terminées
    response = client.get("/api/v1/todos/?is_completed=true")
    assert response.status_code == 200
    assert len(response.json()) == 1

    # 6. Suppression de la tâche
    response = client.delete(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 204

    # 7. Vérification de la suppression
    response = client.get(f"/api/v1/todos/{todo_id}")
    assert response.status_code == 404
