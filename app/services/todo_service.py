"""
Couche service (Business Logic Layer) pour l'entité Todo.

Ce module contient la classe `TodoService` qui encapsule la logique métier, 
la vérification d'existence, le nettoyage des données et les règles de gestion, 
en s'appuyant uniquement sur l'interface d'abstraction `BaseTodoRepository`.
"""

from typing import List, Optional

from fastapi import HTTPException, status
from app.repositories.base import BaseTodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class TodoService:
    """
    Classe de service gérant la logique métier relative aux tâches ToDo.

    Attributes:
        repository (BaseTodoRepository): Instance du dépôt de données injecté.
    """

    def __init__(self, repository: BaseTodoRepository):
        """
        Initialise le service avec une implémentation de repository.

        Args:
            repository (BaseTodoRepository): Dépôt de données (PostgreSQL, JSON, etc.).
        """
        self.repository = repository

    async def get_todos(self, is_completed: Optional[bool] = None) -> List[TodoResponse]:
        """
        Récupère la liste des tâches ToDo en appliquant un filtrage éventuel.

        Args:
            is_completed (Optional[bool]): Filtre facultatif sur l'état d'accomplissement.

        Returns:
            List[TodoResponse]: Liste des schémas de réponse Todo.
        """
        return await self.repository.get_all(is_completed=is_completed)

    async def get_todo_by_id(self, todo_id: str) -> TodoResponse:
        """
        Récupère une tâche par son identifiant unique ou lève une exception HTTP 404.

        Args:
            todo_id (str): Identifiant UUID de la tâche.

        Returns:
            TodoResponse: La tâche si elle existe.

        Raises:
            HTTPException: Code 404 NOT FOUND si la tâche n'existe pas.
        """
        todo = await self.repository.get_by_id(todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tâche avec l'ID '{todo_id}' introuvable."
            )
        return todo

    async def create_todo(self, todo_in: TodoCreate) -> TodoResponse:
        """
        Effectue la validation métier et crée une nouvelle tâche ToDo.

        Args:
            todo_in (TodoCreate): Données de création de la tâche.

        Returns:
            TodoResponse: La tâche créée et instanciée.
        """
        # Nettoyage des espaces superflus (Sanitization)
        todo_in.title = todo_in.title.strip()
        if todo_in.description:
            todo_in.description = todo_in.description.strip()
        return await self.repository.create(todo_in)

    async def update_todo(self, todo_id: str, todo_in: TodoUpdate) -> TodoResponse:
        """
        Valide l'existence de la tâche et applique les modifications.

        Args:
            todo_id (str): Identifiant unique de la tâche.
            todo_in (TodoUpdate): Modifications à appliquer.

        Returns:
            TodoResponse: La tâche mise à jour.

        Raises:
            HTTPException: Code 404 NOT FOUND si la tâche est introuvable.
        """
        # Vérification préalable d'existence (lève 404 si introuvable)
        await self.get_todo_by_id(todo_id)

        if todo_in.title is not None:
            todo_in.title = todo_in.title.strip()
        if todo_in.description is not None:
            todo_in.description = todo_in.description.strip()

        updated_todo = await self.repository.update(todo_id, todo_in)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"La tâche avec l'ID '{todo_id}' n'a pas pu être mise à jour."
            )
        return updated_todo

    async def delete_todo(self, todo_id: str) -> None:
        """
        Supprime la tâche spécifiée par son identifiant unique.

        Args:
            todo_id (str): Identifiant unique de la tâche.

        Raises:
            HTTPException: Code 404 NOT FOUND si la tâche est introuvable.
        """
        success = await self.repository.delete(todo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Tâche avec l'ID '{todo_id}' introuvable."
            )
