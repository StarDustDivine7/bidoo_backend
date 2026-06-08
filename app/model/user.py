from datetime import date, datetime
from enum import Enum

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    EMPLOYEE = "employee"


class User(Base):
    """ERP ke users table me admin aur employee dono store honge."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(String, unique=True, nullable=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    phone = Column(String, nullable=True)
    password_hash = Column(String, nullable=False)
    role = Column(String, nullable=False, default=UserRole.EMPLOYEE.value)
    department = Column(String, nullable=True)
    designation = Column(String, nullable=True)
    join_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    assigned_tasks = relationship(
        "Task",
        foreign_keys="Task.assigned_to_user_id",
        back_populates="assignee",
        cascade="all, delete-orphan",
    )
    created_tasks = relationship(
        "Task",
        foreign_keys="Task.created_by_admin_id",
        back_populates="created_by",
    )
    attendance_records = relationship(
        "Attendance",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    work_logs = relationship(
        "WorkLog",
        back_populates="user",
        cascade="all, delete-orphan",
    )
