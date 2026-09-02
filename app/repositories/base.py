"""
Interface abstraite pour les dépôts de données (Repositories) de l'entité Todo.

Ce module définit le contrat d'interface (Repository Pattern) que toute 
implémentation de persistance (JSON, PostgreSQL, SQLite, In-Memory, etc.) 
doit respecter.
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class BaseTodoRepository(ABC):
    """
    Classe de base abstraite définissant l'interface du dictionnaire / repository des Todos.
    """

    @abstractmethod
    async def get_all(self, is_completed: Optional[bool] = None) -> List[TodoResponse]:
        """
        Récupère l'ensemble des tâches ToDo, avec possibilité de filtrage.

        Args:
            is_completed (Optional[bool]): Filtrer par statut si renseigné.

        Returns:
            List[TodoResponse]: Liste des schémas de réponse Todo.
        """
        pass

    @abstractmethod
    async def get_by_id(self, todo_id: str) -> Optional[TodoResponse]:
        """
        Récupère une tâche ToDo par son identifiant unique.

        Args:
            todo_id (str): Identifiant UUID de la tâche.

        Returns:
            Optional[TodoResponse]: Le schéma de la tâche si trouvée, sinon None.
        """
        pass

    @abstractmethod
    async def create(self, todo_in: TodoCreate) -> TodoResponse:
        """
        Persiste et crée une nouvelle tâche ToDo.

        Args:
            todo_in (TodoCreate): Données de création de la tâche.

        Returns:
            TodoResponse: La tâche créée et instanciée.
        """
        pass

    @abstractmethod
    async def update(self, todo_id: str, todo_in: TodoUpdate) -> Optional[TodoResponse]:
        """
        Met à jour une tâche ToDo existante.

        Args:
            todo_id (str): Identifiant unique de la tâche.
            todo_in (TodoUpdate): Modifications à appliquer.

        Returns:
            Optional[TodoResponse]: La tâche mise à jour ou None si introuvable.
        """
        pass

    @abstractmethod
    async def delete(self, todo_id: str) -> bool:
        """
        Supprime définitivement une tâche ToDo.

        Args:
            todo_id (str): Identifiant unique de la tâche.

        Returns:
            bool: True si la suppression a réussi, False si la tâche n'existait pas.
        """
        pass
