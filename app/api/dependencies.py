from functools import lru_cache

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from app.core.exceptions import UnauthorizedError
from app.core.security import decode_access_token
from app.providers.mock_dashboard_provider import MockDashboardProvider
from app.schemas.user import CurrentUser
from app.services.ai_service import AIService
from app.services.dashboard_service import DashboardService
from app.services.user_service import UserService

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


@lru_cache
def get_dashboard_provider() -> MockDashboardProvider:
    return MockDashboardProvider()


@lru_cache
def get_dashboard_service() -> DashboardService:
    return DashboardService(get_dashboard_provider())


@lru_cache
def get_user_service() -> UserService:
    return UserService()


@lru_cache
def get_ai_service() -> AIService:
    return AIService()


def get_current_user(
    token: str | None = Depends(oauth2_scheme),
    service: UserService = Depends(get_user_service),
) -> CurrentUser:
    if not token:
        raise UnauthorizedError("Authentication token is required.")

    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if not user_id:
        raise UnauthorizedError("Invalid token payload.")

    user = service.get_user_by_id(user_id)
    if not user:
        raise UnauthorizedError("User not found.")

    return user


