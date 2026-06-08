from datetime import date, datetime
from enum import Enum

from sqlalchemy import Column, Date, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from app.core.database import Base


class TaskPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    BLOCKED = "blocked"


class Task(Base):
    """Admin ke assign kiye hue tasks ko store karta hai."""

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    priority = Column(String, nullable=False, default=TaskPriority.MEDIUM.value)
    status = Column(String, nullable=False, default=TaskStatus.PENDING.value)
    due_date = Column(Date, nullable=True)
    assigned_to_user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_by_admin_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assignee = relationship("User", foreign_keys=[assigned_to_user_id], back_populates="assigned_tasks")
    created_by = relationship("User", foreign_keys=[created_by_admin_id], back_populates="created_tasks")
