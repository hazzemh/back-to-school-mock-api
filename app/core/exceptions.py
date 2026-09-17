from dataclasses import dataclass


@dataclass
class AppError(Exception):
    code: str
    message: str
    status_code: int = 500


class DashboardNotFoundError(AppError):
    def __init__(self, dashboard: str):
        super().__init__("DASHBOARD_NOT_FOUND", f"Unknown dashboard: {dashboard}", 404)


class UserNotFoundError(AppError):
    def __init__(self, user_id: str):
        super().__init__("USER_NOT_FOUND", f"Mock user not found: {user_id}", 404)


class AIServiceError(AppError):
    def __init__(self, message: str = "The AI service is temporarily unavailable.", status_code: int = 502):
        super().__init__("AI_SERVICE_UNAVAILABLE", message, status_code)


class InvalidCredentialsError(AppError):
    def __init__(self, message: str = "Invalid username/email or password"):
        super().__init__("INVALID_CREDENTIALS", message, 401)


class UnauthorizedError(AppError):
    def __init__(self, message: str = "Could not validate credentials"):
        super().__init__("UNAUTHORIZED", message, 401)

