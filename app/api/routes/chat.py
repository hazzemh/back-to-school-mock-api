from fastapi import APIRouter, Depends, Request

from app.api.dependencies import get_ai_service, get_current_user
from app.schemas.chat import ChatRequest, ChatResponse
from app.schemas.user import CurrentUser
from app.services.ai_service import AIService

router = APIRouter(prefix="/api/v1", tags=["AI Integration"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send chat message",
    description="Integration boundary for the AI team's chatbot service. Requires Bearer token authentication.",
)
async def chat(
    payload: ChatRequest,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    service: AIService = Depends(get_ai_service),
) -> ChatResponse:
    return await service.chat(payload, request.state.request_id, current_user)

