from functools import lru_cache

from app.providers.mock_dashboard_provider import MockDashboardProvider
from app.services.ai_service import AIService
from app.services.dashboard_service import DashboardService
from app.services.user_service import UserService


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
