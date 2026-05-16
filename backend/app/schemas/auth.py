"""Authentication schemas."""
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    """JWT token response."""

    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""

    sub: str | None = None


class UserLogin(BaseModel):
    """Login request schema."""

    email: EmailStr
    password: str


class UserRegister(BaseModel):
    """Registration request schema."""

    email: EmailStr
    password: str
    full_name: str | None = None
