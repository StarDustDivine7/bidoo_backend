from sqlalchemy import func
from sqlalchemy.orm import Session

from app.model.user import User, UserRole


class UserRepository:
    """User table ke basic DB operations ko isolate karta hai."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(func.lower(User.email) == email.lower()).first()

    def get_all(self) -> list[User]:
        return self.db.query(User).order_by(User.created_at.desc()).all()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def save(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def count_all(self) -> int:
        return self.db.query(User).count()

    def count_by_role(self, role: UserRole) -> int:
        return self.db.query(User).filter(User.role == role.value).count()

    def count_active(self) -> int:
        return self.db.query(User).filter(User.is_active.is_(True)).count()
