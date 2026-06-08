from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import TokenDecodeError, extract_subject_from_token
from app.model.user import User, UserRole
from app.repository.user_repository import UserRepository

# Swagger UI me bearer token support dene ke liye.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> User:
    """
    Bearer token se current logged-in user nikalta hai.
    Yeh protected routes ka base dependency hai.
    """
    try:
        user_id = int(extract_subject_from_token(token))
    except (ValueError, TokenDecodeError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
        )

    user = UserRepository(db).get_by_id(user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User nahi mila")
    if not user.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User inactive hai")
    return user


def require_admin(current_user: User = Depends(get_current_user)) -> User:
    """Admin-only routes ke liye role guard."""
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Sirf admin allowed hai")
    return current_user
