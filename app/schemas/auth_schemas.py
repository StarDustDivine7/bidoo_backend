from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """User login ke liye email aur password bhejega."""

    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)


class TokenResponse(BaseModel):
    """Successful login ke baad JWT token response."""

    access_token: str
    token_type: str = "bearer"
