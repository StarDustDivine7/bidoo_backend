from fastapi import HTTPException, status

from app.core.security import create_access_token, verify_password
from app.repository.user_repository import UserRepository
from app.schemas.auth_schemas import LoginRequest, TokenResponse


class AuthService:
    """Authentication ka business logic yaha rakha gaya hai."""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, payload: LoginRequest) -> TokenResponse:
        user = self.user_repository.get_by_email(payload.email)
        if not user or not verify_password(payload.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Email ya password galat hai",
            )

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User inactive hai, admin se contact karein",
            )

        token = create_access_token(subject=str(user.id))
        return TokenResponse(access_token=token)
