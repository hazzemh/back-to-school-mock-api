from fastapi import APIRouter, Depends

from app.api.dependencies import get_user_service
from app.schemas.user import CurrentUser
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["User"])


@router.get(
    "/me",
    response_model=CurrentUser,
    summary="Get current user",
    description="Returns the current mock user for chatbot greeting/personalization. Replace with token-derived identity when authentication is introduced.",
)
def get_me(service: UserService = Depends(get_user_service)) -> CurrentUser:
    return service.get_current_user()
