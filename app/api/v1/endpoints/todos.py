"""
Controller REST / Endpoints API v1 pour la gestion des tâches ToDo.

Ce module contient les fonctions de routeur (Path Operations) pour FastAPI.
Les endpoints reçoivent les requêtes HTTP, valident l'entrée avec Pydantic,
et délèguent la logique métier au `TodoService`.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.postgres_repository import PostgresTodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService

router = APIRouter()


def get_todo_service(db: AsyncSession = Depends(get_db_session)) -> TodoService:
    """
    Fournisseur de dépendance pour instancier `TodoService` avec `PostgresTodoRepository`.

    Args:
        db (AsyncSession): Session de base de données PostgreSQL active.

    Returns:
        TodoService: Instance de la couche service configurée.
    """
    repository = PostgresTodoRepository(session=db)
    return TodoService(repository=repository)


@router.get(
    "/",
    response_model=List[TodoResponse],
    status_code=status.HTTP_200_OK,
    summary="Lister toutes les tâches ToDo",
    description="Récupère la liste des tâches. Possibilité de filtrer par statut de réalisation (`is_completed`)."
)
async def list_todos(
    is_completed: Optional[bool] = Query(
        default=None,
        description="Filtrer par statut : `true` pour complétée, `false` pour non complétée"
    ),
    service: TodoService = Depends(get_todo_service)
) -> List[TodoResponse]:
    """
    Endpoint HTTP GET pour lister l'ensemble des tâches ToDo.

    Args:
        is_completed (Optional[bool]): Filtre optionnel sur le statut.
        service (TodoService): Service métier injecté.

    Returns:
        List[TodoResponse]: Liste des tâches sérialisées.
    """
    return await service.get_todos(is_completed=is_completed)


@router.post(
    "/",
    response_model=TodoResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Créer une nouvelle tâche ToDo",
    description="Ajoute une nouvelle tâche ToDo avec un titre et une description optionnelle."
)
async def create_todo(
    todo_in: TodoCreate,
    service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    """
    Endpoint HTTP POST pour créer une nouvelle tâche ToDo.

    Args:
        todo_in (TodoCreate): Corps de la requête validé par Pydantic.
        service (TodoService): Service métier injecté.

    Returns:
        TodoResponse: La tâche nouvellement créée.
    """
    return await service.create_todo(todo_in)


@router.get(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    summary="Obtenir une tâche par son ID",
    description="Récupère les détails d'une tâche ToDo spécifique par son identifiant unique."
)
async def get_todo(
    todo_id: str,
    service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    """
    Endpoint HTTP GET pour récupérer les détails d'une tâche par son identifiant.

    Args:
        todo_id (str): Identifiant UUID de la tâche.
        service (TodoService): Service métier injecté.

    Returns:
        TodoResponse: Détails de la tâche correspondante.
    """
    return await service.get_todo_by_id(todo_id)


@router.put(
    "/{todo_id}",
    response_model=TodoResponse,
    status_code=status.HTTP_200_OK,
    summary="Modifier une tâche ToDo",
    description="Met à jour le titre, la description ou le statut d'une tâche existante."
)
async def update_todo(
    todo_id: str,
    todo_in: TodoUpdate,
    service: TodoService = Depends(get_todo_service)
) -> TodoResponse:
    """
    Endpoint HTTP PUT pour mettre à jour une tâche ToDo existante.

    Args:
        todo_id (str): Identifiant unique de la tâche.
        todo_in (TodoUpdate): Corps de la requête contenant les modifications.
        service (TodoService): Service métier injecté.

    Returns:
        TodoResponse: La tâche mise à jour.
    """
    return await service.update_todo(todo_id, todo_in)


@router.delete(
    "/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Supprimer une tâche ToDo",
    description="Supprime définitivement une tâche ToDo par son identifiant unique."
)
async def delete_todo(
    todo_id: str,
    service: TodoService = Depends(get_todo_service)
) -> None:
    """
    Endpoint HTTP DELETE pour supprimer une tâche ToDo.

    Args:
        todo_id (str): Identifiant unique de la tâche.
        service (TodoService): Service métier injecté.
    """
    await service.delete_todo(todo_id)
