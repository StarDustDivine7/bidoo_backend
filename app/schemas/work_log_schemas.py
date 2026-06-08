from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class WorkLogCreate(BaseModel):
    """Daily work update create karne ke liye schema."""

    summary: str = Field(..., min_length=5)
    blockers: str | None = None
    hours_spent: Decimal | None = None
    work_date: date | None = None


class WorkLogResponse(BaseModel):
    """Work log API response schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    work_date: date
    summary: str
    blockers: str | None = None
    hours_spent: Decimal | None = None
    created_at: datetime
    updated_at: datetime
