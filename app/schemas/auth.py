from __future__ import annotations

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username_or_email: str = Field(..., description="Username or email address")
    password: str = Field(..., description="User password")


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(..., description="Access token expiration in seconds")


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None
    iat: int | None = None
