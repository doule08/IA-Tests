"""
Implémentation basée sur un fichier JSON du dépôt de données (Repository) Todo.

Ce module implémente `BaseTodoRepository` pour la persistance locale dans un 
fichier JSON, sécurisée en concurrence d'accès asynchrone à l'aide d'un `asyncio.Lock`.
"""

import asyncio
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional
from uuid import uuid4

from app.core.config import settings
from app.repositories.base import BaseTodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class JSONTodoRepository(BaseTodoRepository):
    """
    Implémentation concrète du dictionnaire ToDo enregistrant les données dans un fichier JSON.

    Attributes:
        file_path (Path): Chemin d'accès au fichier JSON de stockage.
    """

    def __init__(self, file_path: Optional[Path] = None):
        """
        Initialise le dépôt JSON.

        Args:
            file_path (Optional[Path]): Chemin personnalisé optionnel vers le fichier JSON.
        """
        self.file_path = file_path if file_path is not None else settings.todos_file_path
        self._lock = asyncio.Lock()
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        """
        Vérifie l'existence du fichier et crée les répertoires ou le tableau JSON initial `[]` si nécessaire.
        """
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    async def _read_file(self) -> List[dict]:
        """
        Lit et décode de manière sécurisée le contenu brut du fichier JSON.

        Returns:
            List[dict]: Liste des dictionnaires représentants les todos.
        """
        if not self.file_path.exists():
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    async def _write_file(self, data: List[dict]) -> None:
        """
        Écrit la liste des dictionnaires de todos dans le fichier JSON.

        Args:
            data (List[dict]): Données sérialisées à écrire.
        """
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    async def get_all(self, is_completed: Optional[bool] = None) -> List[TodoResponse]:
        """
        Récupère toutes les tâches ToDo du fichier JSON.

        Args:
            is_completed (Optional[bool]): Filtre facultatif sur l'état d'accomplissement.

        Returns:
            List[TodoResponse]: Liste des tâches sous forme de schémas Pydantic.
        """
        async with self._lock:
            raw_data = await self._read_file()
            todos = [TodoResponse.model_validate(item) for item in raw_data]

            if is_completed is not None:
                todos = [t for t in todos if t.is_completed == is_completed]

            return todos

    async def get_by_id(self, todo_id: str) -> Optional[TodoResponse]:
        """
        Recherche une tâche par son identifiant unique dans le fichier JSON.

        Args:
            todo_id (str): Identifiant UUID de la tâche.

        Returns:
            Optional[TodoResponse]: Tâche correspondante ou None.
        """
        async with self._lock:
            raw_data = await self._read_file()
            for item in raw_data:
                if item.get("id") == todo_id:
                    return TodoResponse.model_validate(item)
            return None

    async def create(self, todo_in: TodoCreate) -> TodoResponse:
        """
        Ajoute une nouvelle tâche au fichier JSON.

        Args:
            todo_in (TodoCreate): Schéma de création.

        Returns:
            TodoResponse: Schéma de la tâche instanciée.
        """
        async with self._lock:
            raw_data = await self._read_file()
            now = datetime.now(timezone.utc)

            new_todo = TodoResponse(
                id=str(uuid4()),
                title=todo_in.title,
                description=todo_in.description,
                is_completed=todo_in.is_completed,
                created_at=now,
                updated_at=now
            )

            todo_dict = json.loads(new_todo.model_dump_json())
            raw_data.append(todo_dict)
            await self._write_file(raw_data)

            return new_todo

    async def update(self, todo_id: str, todo_in: TodoUpdate) -> Optional[TodoResponse]:
        """
        Modifie une tâche existante dans le fichier JSON.

        Args:
            todo_id (str): Identifiant unique de la tâche.
            todo_in (TodoUpdate): Données de modification.

        Returns:
            Optional[TodoResponse]: Tâche mise à jour ou None si non trouvée.
        """
        async with self._lock:
            raw_data = await self._read_file()
            for index, item in enumerate(raw_data):
                if item.get("id") == todo_id:
                    existing_todo = TodoResponse.model_validate(item)

                    update_data = todo_in.model_dump(exclude_unset=True)
                    updated_fields = existing_todo.model_copy(update=update_data)
                    updated_fields.updated_at = datetime.now(timezone.utc)

                    updated_dict = json.loads(updated_fields.model_dump_json())
                    raw_data[index] = updated_dict
                    await self._write_file(raw_data)

                    return updated_fields
            return None

    async def delete(self, todo_id: str) -> bool:
        """
        Supprime une tâche du fichier JSON.

        Args:
            todo_id (str): Identifiant unique de la tâche.

        Returns:
            bool: True si supprimée, False si absente du fichier.
        """
        async with self._lock:
            raw_data = await self._read_file()
            initial_length = len(raw_data)
            raw_data = [item for item in raw_data if item.get("id") != todo_id]

            if len(raw_data) < initial_length:
                await self._write_file(raw_data)
                return True
            return False
