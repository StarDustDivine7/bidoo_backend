from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field

from app.model.task import TaskPriority, TaskStatus


class TaskCreate(BaseModel):
    """Admin ke task assignment payload ke liye schema."""

    title: str = Field(..., min_length=3, max_length=150)
    description: str | None = None
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: date | None = None
    assigned_to_user_id: int


class TaskStatusUpdate(BaseModel):
    """Employee apne assigned task ka status update kar sakta hai."""

    status: TaskStatus


class TaskResponse(BaseModel):
    """Task API response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    description: str | None = None
    priority: TaskPriority
    status: TaskStatus
    due_date: date | None = None
    assigned_to_user_id: int
    created_by_admin_id: int
    created_at: datetime
    updated_at: datetime
