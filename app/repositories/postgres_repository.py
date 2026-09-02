"""
Implémentation PostgreSQL du dépôt de données (Repository) Todo.

Ce module implémente `BaseTodoRepository` à l'aide de SQLAlchemy AsyncSession
pour interagir avec une base de données PostgreSQL de manière totalement asynchrone.
"""

from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import TodoModel
from app.repositories.base import BaseTodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class PostgresTodoRepository(BaseTodoRepository):
    """
    Implémentation concrète du repository Todo utilisant SQLAlchemy et PostgreSQL.

    Attributes:
        session (AsyncSession): Session asynchrone SQLAlchemy active.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialise le repository PostgreSQL avec la session injectée.

        Args:
            session (AsyncSession): Session asynchrone de base de données.
        """
        self.session = session

    def _to_response_schema(self, model: TodoModel) -> TodoResponse:
        """
        Convertit une instance d'un modèle ORM `TodoModel` en schéma Pydantic `TodoResponse`.

        Args:
            model (TodoModel): Instance du modèle ORM SQLAlchemy.

        Returns:
            TodoResponse: Schéma Pydantic prêt pour la sérialisation API.
        """
        return TodoResponse(
            id=model.id,
            title=model.title,
            description=model.description,
            is_completed=model.is_completed,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_all(self, is_completed: Optional[bool] = None) -> List[TodoResponse]:
        """
        Récupère toutes les tâches enregistrées dans PostgreSQL avec filtrage optionnel.

        Args:
            is_completed (Optional[bool]): Filtre facultatif sur le statut.

        Returns:
            List[TodoResponse]: Liste des schémas TodoResponse.
        """
        query = select(TodoModel)
        if is_completed is not None:
            query = query.where(TodoModel.is_completed == is_completed)

        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_response_schema(model) for model in models]

    async def get_by_id(self, todo_id: str) -> Optional[TodoResponse]:
        """
        Recherche une tâche par son identifiant unique UUID dans PostgreSQL.

        Args:
            todo_id (str): Identifiant UUID de la tâche.

        Returns:
            Optional[TodoResponse]: Schéma TodoResponse ou None si introuvable.
        """
        query = select(TodoModel).where(TodoModel.id == todo_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model:
            return self._to_response_schema(model)
        return None

    async def create(self, todo_in: TodoCreate) -> TodoResponse:
        """
        Insère une nouvelle tâche ToDo dans la base de données PostgreSQL.

        Args:
            todo_in (TodoCreate): Données de création de la tâche.

        Returns:
            TodoResponse: Instance créée sérialisée.
        """
        now = datetime.now(timezone.utc)
        todo_model = TodoModel(
            id=str(uuid4()),
            title=todo_in.title,
            description=todo_in.description,
            is_completed=todo_in.is_completed,
            created_at=now,
            updated_at=now
        )
        self.session.add(todo_model)
        await self.session.commit()
        await self.session.refresh(todo_model)
        return self._to_response_schema(todo_model)

    async def update(self, todo_id: str, todo_in: TodoUpdate) -> Optional[TodoResponse]:
        """
        Met à jour les champs d'une tâche existante dans PostgreSQL.

        Args:
            todo_id (str): Identifiant unique de la tâche.
            todo_in (TodoUpdate): Valeurs à mettre à jour.

        Returns:
            Optional[TodoResponse]: Tâche mise à jour ou None si introuvable.
        """
        query = select(TodoModel).where(TodoModel.id == todo_id)
        result = await self.session.execute(query)
        todo_model = result.scalar_one_or_none()

        if not todo_model:
            return None

        update_data = todo_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(todo_model, field, value)

        todo_model.updated_at = datetime.now(timezone.utc)

        await self.session.commit()
        await self.session.refresh(todo_model)
        return self._to_response_schema(todo_model)

    async def delete(self, todo_id: str) -> bool:
        """
        Supprime définitivement une tâche de la base de données PostgreSQL.

        Args:
            todo_id (str): Identifiant unique de la tâche.

        Returns:
            bool: True si la suppression a été effectuée, False si absente.
        """
        query = select(TodoModel).where(TodoModel.id == todo_id)
        result = await self.session.execute(query)
        todo_model = result.scalar_one_or_none()

        if not todo_model:
            return False

        await self.session.delete(todo_model)
        await self.session.commit()
        return True
