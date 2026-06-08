from fastapi import HTTPException, status

from app.core.security import get_password_hash
from app.model.user import User, UserRole
from app.repository.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate


class UserService:
    """User creation aur management logic yaha handle hota hai."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def create_user(self, payload: UserCreate) -> User:
        existing_user = self.user_repository.get_by_email(payload.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Is email se user already exist karta hai",
            )

        user = User(
            employee_id=payload.employee_id,
            name=payload.name,
            email=payload.email,
            phone=payload.phone,
            password_hash=get_password_hash(payload.password),
            role=payload.role.value,
            department=payload.department,
            designation=payload.designation,
            join_date=payload.join_date,
            is_active=payload.is_active,
        )
        return self.user_repository.create(user)

    def list_users(self) -> list[User]:
        return self.user_repository.get_all()

    def get_user(self, user_id: int) -> User:
        user = self.user_repository.get_by_id(user_id)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User nahi mila")
        return user

    def update_user(self, user_id: int, payload: UserUpdate) -> User:
        user = self.get_user(user_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            if isinstance(value, UserRole):
                value = value.value
            setattr(user, key, value)
        return self.user_repository.save(user)
