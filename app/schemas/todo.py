from datetime import datetime, timezone
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class TodoBase(BaseModel):
    """Base schema for Todo containing common fields."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Title of the ToDo task",
        examples=["Acheter du pain"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Detailed description of the task",
        examples=["Passer à la boulangerie du coin avant 19h"]
    )
    is_completed: bool = Field(
        default=False,
        description="Status of completion of the task"
    )


class TodoCreate(TodoBase):
    """Schema used when creating a new Todo."""

    pass


class TodoUpdate(BaseModel):
    """Schema used when updating an existing Todo (all fields optional for partial update)."""

    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=200,
        description="Updated title of the ToDo task"
    )
    description: Optional[str] = Field(
        default=None,
        max_length=1000,
        description="Updated description of the task"
    )
    is_completed: Optional[bool] = Field(
        default=None,
        description="Updated completion status"
    )


class TodoResponse(TodoBase):
    """Schema returned in API responses."""

    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Unique identifier for the Todo"
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the Todo was created"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Timestamp when the Todo was last updated"
    )

    model_config = {
        "from_attributes": True
    }

