from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo import TodoModel
from app.repositories.base import BaseTodoRepository
from app.schemas.todo import TodoCreate, TodoResponse, TodoUpdate


class PostgresTodoRepository(BaseTodoRepository):
    """PostgreSQL implementation of the Todo repository using SQLAlchemy AsyncSession."""

    def __init__(self, session: AsyncSession):
        self.session = session

    def _to_response_schema(self, model: TodoModel) -> TodoResponse:
        """Convert SQLAlchemy TodoModel instance to Pydantic TodoResponse schema."""
        return TodoResponse(
            id=model.id,
            title=model.title,
            description=model.description,
            is_completed=model.is_completed,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    async def get_all(self, is_completed: Optional[bool] = None) -> List[TodoResponse]:
        """Retrieve all todos from PostgreSQL, with optional completed filter."""
        query = select(TodoModel)
        if is_completed is not None:
            query = query.where(TodoModel.is_completed == is_completed)
            
        result = await self.session.execute(query)
        models = result.scalars().all()
        return [self._to_response_schema(model) for model in models]

    async def get_by_id(self, todo_id: str) -> Optional[TodoResponse]:
        """Retrieve a todo item by ID from PostgreSQL."""
        query = select(TodoModel).where(TodoModel.id == todo_id)
        result = await self.session.execute(query)
        model = result.scalar_one_or_none()
        if model:
            return self._to_response_schema(model)
        return None

    async def create(self, todo_in: TodoCreate) -> TodoResponse:
        """Create a new todo in PostgreSQL."""
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
        """Update an existing todo in PostgreSQL."""
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
        """Delete a todo from PostgreSQL by ID."""
        query = select(TodoModel).where(TodoModel.id == todo_id)
        result = await self.session.execute(query)
        todo_model = result.scalar_one_or_none()
        
        if not todo_model:
            return False

        await self.session.delete(todo_model)
        await self.session.commit()
        return True
