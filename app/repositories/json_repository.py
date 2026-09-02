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
    """JSON file implementation of the Todo repository."""

    def __init__(self, file_path: Optional[Path] = None):
        self.file_path = file_path if file_path is not None else settings.todos_file_path
        self._lock = asyncio.Lock()
        self._ensure_file_exists()


    def _ensure_file_exists(self) -> None:
        """Create the directory and initial empty JSON file if they don't exist."""
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self.file_path.exists() or self.file_path.stat().st_size == 0:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump([], f, indent=2)

    async def _read_file(self) -> List[dict]:
        """Read raw json data from file."""
        if not self.file_path.exists():
            return []
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    async def _write_file(self, data: List[dict]) -> None:
        """Write raw json data to file."""
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    async def get_all(self, is_completed: Optional[bool] = None) -> List[TodoResponse]:
        """Retrieve all todos with optional status filtering."""
        async with self._lock:
            raw_data = await self._read_file()
            todos = [TodoResponse.model_validate(item) for item in raw_data]
            
            if is_completed is not None:
                todos = [t for t in todos if t.is_completed == is_completed]
                
            return todos

    async def get_by_id(self, todo_id: str) -> Optional[TodoResponse]:
        """Retrieve a single todo by its ID."""
        async with self._lock:
            raw_data = await self._read_file()
            for item in raw_data:
                if item.get("id") == todo_id:
                    return TodoResponse.model_validate(item)
            return None

    async def create(self, todo_in: TodoCreate) -> TodoResponse:
        """Create and store a new todo."""
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
            
            # Serialize for JSON storage
            todo_dict = json.loads(new_todo.model_dump_json())
            raw_data.append(todo_dict)
            await self._write_file(raw_data)
            
            return new_todo

    async def update(self, todo_id: str, todo_in: TodoUpdate) -> Optional[TodoResponse]:
        """Update an existing todo."""
        async with self._lock:
            raw_data = await self._read_file()
            for index, item in enumerate(raw_data):
                if item.get("id") == todo_id:
                    existing_todo = TodoResponse.model_validate(item)
                    
                    # Update fields if provided
                    update_data = todo_in.model_dump(exclude_unset=True)
                    updated_fields = existing_todo.model_copy(update=update_data)
                    updated_fields.updated_at = datetime.now(timezone.utc)
                    
                    updated_dict = json.loads(updated_fields.model_dump_json())
                    raw_data[index] = updated_dict
                    await self._write_file(raw_data)
                    
                    return updated_fields
            return None


    async def delete(self, todo_id: str) -> bool:
        """Delete a todo by ID."""
        async with self._lock:
            raw_data = await self._read_file()
            initial_length = len(raw_data)
            raw_data = [item for item in raw_data if item.get("id") != todo_id]
            
            if len(raw_data) < initial_length:
                await self._write_file(raw_data)
                return True
            return False
