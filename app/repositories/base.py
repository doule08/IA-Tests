from abc import ABC, abstractmethod
from typing import List, Optional
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class BaseTodoRepository(ABC):
    """Abstract interface for Todo repository to allow easy DB switching in the future."""

    @abstractmethod
    async def get_all(self, is_completed: Optional[bool] = None) -> List[TodoResponse]:
        """Retrieve all todo items, optionally filtered by completion status."""
        pass

    @abstractmethod
    async def get_by_id(self, todo_id: str) -> Optional[TodoResponse]:
        """Retrieve a specific todo item by ID."""
        pass

    @abstractmethod
    async def create(self, todo_in: TodoCreate) -> TodoResponse:
        """Create a new todo item."""
        pass

    @abstractmethod
    async def update(self, todo_id: str, todo_in: TodoUpdate) -> Optional[TodoResponse]:
        """Update an existing todo item."""
        pass

    @abstractmethod
    async def delete(self, todo_id: str) -> bool:
        """Delete a todo item by ID."""
        pass
