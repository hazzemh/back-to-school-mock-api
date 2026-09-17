from fastapi import APIRouter, Depends

from app.api.dependencies import get_current_user
from app.schemas.user import CurrentUser

router = APIRouter(prefix="/api/v1/users", tags=["User"])


@router.get(
    "/me",
    response_model=CurrentUser,
    summary="Get current user",
    description="Returns the authenticated user for chatbot greeting and personalization derived from the Bearer access token.",
)
def get_me(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
    return current_user

