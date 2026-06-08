from datetime import datetime, timedelta, timezone
from typing import Any

from jose import JWTError, jwt
from passlib.context import CryptContext


from app.core.config import settings

# Password hashing ke liye shared context.
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """User ke plain password ko stored hash se compare karta hai."""
    print("PASSWORD:", plain_password)
    print("PASSWORD LENGTH:", len(plain_password))
    print("HASH:", hashed_password)
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Naya password secure hash me convert karta hai."""
    return pwd_context.hash(password)


def create_access_token(subject: str, expires_minutes: int | None = None) -> str:
    """
    JWT token create karta hai.
    `sub` field me user id string ke form me store hota hai.
    """
    expire_minutes = expires_minutes or settings.ACCESS_TOKEN_EXPIRE_MINUTES
    expire = datetime.now(timezone.utc) + timedelta(minutes=expire_minutes)
    payload: dict[str, Any] = {"sub": subject, "exp": expire}
    return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_access_token(token: str) -> dict[str, Any]:
    """JWT token decode karta hai aur invalid hone par error raise karta hai."""
    return jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])


class TokenDecodeError(Exception):
    """Custom exception taaki auth flow readable rahe."""


def extract_subject_from_token(token: str) -> str:
    """
    Token se user id nikalta hai.
    Yeh function auth dependency me use hoga.
    """
    try:
        payload = decode_access_token(token)
        subject = payload.get("sub")
        if not subject:
            raise TokenDecodeError("Token me subject missing hai")
        return subject
    except JWTError as exc:
        raise TokenDecodeError("Invalid token") from exc
