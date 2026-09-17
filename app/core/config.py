from __future__ import annotations

import os
from dataclasses import dataclass


def _as_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


@dataclass(frozen=True)
class Settings:
    app_name: str = os.getenv("APP_NAME", "Back to School Mock Integration API")
    app_env: str = os.getenv("APP_ENV", "development")
    app_host: str = os.getenv("APP_HOST", "0.0.0.0")
    app_port: int = int(os.getenv("APP_PORT", "8000"))
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    root_path: str = os.getenv("ROOT_PATH", "/b2s-mock-api")

    mock_data_refresh_seconds: int = max(1, int(os.getenv("MOCK_DATA_REFRESH_SECONDS", "60")))
    mock_scenario: str = os.getenv("MOCK_SCENARIO", "source").strip().lower()

    mock_user_id: str = os.getenv("MOCK_USER_ID", "USR-001")

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "b2s_mock_secret_key_change_in_production_12345")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expire_minutes: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "60"))

    mock_ai_enabled: bool = _as_bool(os.getenv("MOCK_AI_ENABLED"), True)
    ai_service_url: str | None = os.getenv("AI_SERVICE_URL") or None
    ai_chat_path: str = os.getenv("AI_CHAT_PATH", "/chat")
    ai_timeout_seconds: float = float(os.getenv("AI_TIMEOUT_SECONDS", "30"))

    cors_allowed_origins: tuple[str, ...] = tuple(
        origin.strip()
        for origin in os.getenv("CORS_ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:5173").split(",")
        if origin.strip()
    )


settings = Settings()
