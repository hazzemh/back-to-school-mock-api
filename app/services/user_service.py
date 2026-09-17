from __future__ import annotations

import json
from pathlib import Path

from app.core.config import settings
from app.core.exceptions import UserNotFoundError
from app.core.security import verify_password
from app.schemas.user import CurrentUser, UserInDB


class UserService:
    def __init__(self) -> None:
        path = Path(__file__).resolve().parents[1] / "mock_data" / "users.json"
        self.db_users = [UserInDB.model_validate(item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def get_user_by_id(self, user_id: str) -> CurrentUser | None:
        for user in self.db_users:
            if user.id == user_id:
                return CurrentUser.model_validate(user.model_dump())
        return None

    def get_user_by_username_or_email(self, identifier: str) -> UserInDB | None:
        clean_id = identifier.strip().lower()
        for user in self.db_users:
            if user.username.lower() == clean_id or user.email.lower() == clean_id:
                return user
        return None

    def authenticate_user(self, username_or_email: str, password: str) -> CurrentUser | None:
        user = self.get_user_by_username_or_email(username_or_email)
        if not user:
            return None
        if not verify_password(password, user.password_hash):
            return None
        return CurrentUser.model_validate(user.model_dump())

    def get_current_user(self, user_id: str | None = None) -> CurrentUser:
        target_id = user_id or settings.mock_user_id
        user = self.get_user_by_id(target_id)
        if user:
            return user
        raise UserNotFoundError(target_id)

