from fastapi import APIRouter, Depends, Request

from app.api.dependencies import get_ai_service, get_current_user
from app.schemas.chat import (
    ChatHistoryResponse,
    ChatRequest,
    ChatResponse,
    WelcomeRequest,
    WelcomeResponse,
)
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


@router.get(
    "/chat/history/{conversation_id}",
    response_model=ChatHistoryResponse,
    summary="Get conversation history",
    description="Retrieves message history for a specific conversation ID. Requires Bearer token authentication.",
)
async def get_chat_history(
    conversation_id: str,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    service: AIService = Depends(get_ai_service),
) -> ChatHistoryResponse:
    return await service.get_conversation_history(conversation_id, request.state.request_id, current_user)


@router.post(
    "/chat/welcome",
    response_model=WelcomeResponse,
    summary="Get initial welcome message and prompts",
    description="Fetches an initial personalized welcome greeting and starter prompts for a new or existing chatbot session. Requires Bearer token authentication.",
)
async def welcome(
    payload: WelcomeRequest,
    request: Request,
    current_user: CurrentUser = Depends(get_current_user),
    service: AIService = Depends(get_ai_service),
) -> WelcomeResponse:
    return await service.get_welcome_message(payload, request.state.request_id, current_user)



