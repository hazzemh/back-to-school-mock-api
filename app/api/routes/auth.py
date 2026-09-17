from fastapi import APIRouter, Depends

from app.api.dependencies import get_user_service
from app.core.config import settings
from app.core.exceptions import InvalidCredentialsError
from app.core.security import create_access_token
from app.schemas.auth import LoginRequest, TokenResponse
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User Login",
    description="Authenticates user credentials and returns a JWT Bearer access token.",
)
def login(
    payload: LoginRequest,
    service: UserService = Depends(get_user_service),
) -> TokenResponse:
    user = service.authenticate_user(payload.username_or_email, payload.password)
    if not user:
        raise InvalidCredentialsError("Invalid username/email or password.")

    access_token = create_access_token(data={"sub": user.id})
    expires_in = settings.jwt_access_token_expire_minutes * 60
    return TokenResponse(access_token=access_token, token_type="bearer", expires_in=expires_in)
