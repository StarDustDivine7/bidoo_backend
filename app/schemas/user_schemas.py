from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.model.user import UserRole


class UserBase(BaseModel):
    """Shared user fields jo response aur request dono me kaam aate hain."""

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str | None = None
    department: str | None = None
    designation: str | None = None
    join_date: date | None = None
    role: UserRole = UserRole.EMPLOYEE
    is_active: bool = True


class UserCreate(UserBase):
    """Admin jab naya user banayega tab ye schema use hoga."""

    employee_id: str | None = None
    password: str = Field(..., min_length=6, max_length=100)


class UserUpdate(BaseModel):
    """Admin selected fields update kar sake iske liye partial schema."""

    name: str | None = Field(default=None, min_length=2, max_length=100)
    phone: str | None = None
    department: str | None = None
    designation: str | None = None
    join_date: date | None = None
    role: UserRole | None = None
    is_active: bool | None = None


class UserResponse(UserBase):
    """API response me password nahi bhejna chahiye, isliye safe schema."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    employee_id: str | None = None
    created_at: datetime
    updated_at: datetime
