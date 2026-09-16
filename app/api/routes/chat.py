from fastapi import APIRouter, Depends, Request

from app.api.dependencies import get_ai_service
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.ai_service import AIService

router = APIRouter(prefix="/api/v1", tags=["AI Integration"])


@router.post(
    "/chat",
    response_model=ChatResponse,
    summary="Send chat message",
    description="Integration boundary for the AI team's chatbot service. Runs in mock mode by default and can proxy to an external AI service via environment configuration.",
)
async def chat(
    payload: ChatRequest,
    request: Request,
    service: AIService = Depends(get_ai_service),
) -> ChatResponse:
    return await service.chat(payload, request.state.request_id)
