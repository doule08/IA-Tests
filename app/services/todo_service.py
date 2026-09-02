from typing import List, Optional

from fastapi import HTTPException, status
from app.repositories.base import BaseTodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class TodoService:
    """Service layer containing business logic for Todo management."""

    def __init__(self, repository: BaseTodoRepository):
        self.repository = repository

    async def get_todos(self, is_completed: Optional[bool] = None) -> List[TodoResponse]:
        """Fetch list of todos with optional filtering."""
        return await self.repository.get_all(is_completed=is_completed)

    async def get_todo_by_id(self, todo_id: str) -> TodoResponse:
        """Fetch a single todo or raise 404 HTTP Exception if not found."""
        todo = await self.repository.get_by_id(todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' not found."
            )
        return todo

    async def create_todo(self, todo_in: TodoCreate) -> TodoResponse:
        """Business logic for creating a new todo item."""
        # Sanitize title whitespace
        todo_in.title = todo_in.title.strip()
        if todo_in.description:
            todo_in.description = todo_in.description.strip()
        return await self.repository.create(todo_in)

    async def update_todo(self, todo_id: str, todo_in: TodoUpdate) -> TodoResponse:
        """Business logic for updating an existing todo item."""
        # Ensure item exists
        await self.get_todo_by_id(todo_id)
        
        if todo_in.title is not None:
            todo_in.title = todo_in.title.strip()
        if todo_in.description is not None:
            todo_in.description = todo_in.description.strip()
            
        updated_todo = await self.repository.update(todo_id, todo_in)
        if not updated_todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' could not be updated."
            )
        return updated_todo

    async def delete_todo(self, todo_id: str) -> None:
        """Business logic for deleting a todo item."""
        success = await self.repository.delete(todo_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Todo item with ID '{todo_id}' not found."
            )
