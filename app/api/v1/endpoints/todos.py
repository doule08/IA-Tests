from typing import List, Optional

from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db_session
from app.repositories.postgres_repository import PostgresTodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate
from app.services.todo_service import TodoService

router = APIRouter()


def get_todo_service(db: AsyncSession = Depends(get_db_session)) -> TodoService:
    """Dependency provider for TodoService using PostgreSQL repository."""
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
    """Endpoint to retrieve list of todos."""
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
    """Endpoint to create a new todo."""
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
    """Endpoint to get a todo by ID."""
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
    """Endpoint to update an existing todo."""
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
    """Endpoint to delete a todo."""
    await service.delete_todo(todo_id)
