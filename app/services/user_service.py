import json
from pathlib import Path

from app.core.config import settings
from app.core.exceptions import UserNotFoundError
from app.schemas.user import CurrentUser


class UserService:
    def __init__(self) -> None:
        path = Path(__file__).resolve().parents[1] / "mock_data" / "users.json"
        self.users = [CurrentUser.model_validate(item) for item in json.loads(path.read_text(encoding="utf-8"))]

    def get_current_user(self) -> CurrentUser:
        for user in self.users:
            if user.id == settings.mock_user_id:
                return user
        raise UserNotFoundError(settings.mock_user_id)
