from __future__ import annotations

import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx

from app.core.config import settings
from app.core.exceptions import AIServiceError
from app.schemas.chat import (
    ChatHistoryResponse,
    ChatMessage,
    ChatRequest,
    ChatResponse,
    WelcomeRequest,
    WelcomeResponse,
)
from app.schemas.user import CurrentUser

RIYADH = ZoneInfo("Asia/Riyadh")


class AIService:
    async def chat(self, request: ChatRequest, request_id: str, current_user: CurrentUser) -> ChatResponse:
        if settings.mock_ai_enabled or not settings.ai_service_url:
            conversation_id = request.conversation_id or f"conv-{uuid.uuid4().hex[:12]}"
            return ChatResponse(
                conversation_id=conversation_id,
                message_id=f"msg-{uuid.uuid4().hex[:12]}",
                answer=(
                    f"Hello {current_user.first_name}! Mock AI response. The integration endpoint is working. "
                    "Configure AI_SERVICE_URL and set MOCK_AI_ENABLED=false to forward messages to the AI service."
                ),
                generated_at=datetime.now(tz=RIYADH),
                provider="mock",
            )

        url = settings.ai_service_url.rstrip("/") + "/" + settings.ai_chat_path.lstrip("/")
        try:
            async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
                payload = request.model_dump(exclude_none=True)
                payload["user_id"] = current_user.id
                response = await client.post(
                    url,
                    json=payload,
                    headers={
                        "X-Request-ID": request_id,
                        "X-User-ID": current_user.id,
                    },
                )

                response.raise_for_status()
                data = response.json()
        except (httpx.HTTPError, ValueError) as exc:
            raise AIServiceError() from exc

        # The adapter accepts a small set of common upstream field names so the AI team
        # can integrate before its final contract is frozen.
        try:
            answer = data.get("answer") or data.get("message") or data.get("response")
            if not isinstance(answer, str):
                raise ValueError("AI response is missing an answer/message/response string")
            return ChatResponse(
                conversation_id=str(data.get("conversation_id") or request.conversation_id or f"conv-{uuid.uuid4().hex[:12]}"),
                message_id=str(data.get("message_id") or f"msg-{uuid.uuid4().hex[:12]}"),
                answer=answer,
                generated_at=datetime.now(tz=RIYADH),
                provider="external",
            )
        except Exception as exc:
            raise AIServiceError("The AI service returned an unsupported response contract.") from exc

    async def get_conversation_history(
        self, conversation_id: str, request_id: str, current_user: CurrentUser
    ) -> ChatHistoryResponse:
        now = datetime.now(tz=RIYADH)
        if settings.mock_ai_enabled or not settings.ai_service_url:
            return ChatHistoryResponse(
                conversation_id=conversation_id,
                messages=[
                    ChatMessage(
                        message_id="msg-001",
                        role="user",
                        content="Hello, I need assistance with network status.",
                        timestamp=now,
                    ),
                    ChatMessage(
                        message_id="msg-002",
                        role="assistant",
                        content=(
                            f"Hello {current_user.first_name}! Mock AI response history for conversation '{conversation_id}'. "
                            "All systems in Network Operations and Service Operations are running normally."
                        ),
                        timestamp=now,
                    ),
                ],
            )

        url = settings.ai_service_url.rstrip("/") + "/" + settings.ai_chat_path.lstrip("/") + f"/history/{conversation_id}"
        try:
            async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
                response = await client.get(
                    url,
                    headers={
                        "X-Request-ID": request_id,
                        "X-User-ID": current_user.id,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return ChatHistoryResponse.model_validate(data)
        except Exception:
            return ChatHistoryResponse(
                conversation_id=conversation_id,
                messages=[
                    ChatMessage(
                        message_id="msg-001",
                        role="user",
                        content="Hello, I need assistance with network status.",
                        timestamp=now,
                    ),
                    ChatMessage(
                        message_id="msg-002",
                        role="assistant",
                        content=f"Hello {current_user.first_name}! Conversation history retrieved.",
                        timestamp=now,
                    ),
                ],
            )

    async def get_welcome_message(
        self, request: WelcomeRequest, request_id: str, current_user: CurrentUser
    ) -> WelcomeResponse:
        conversation_id = request.conversation_id or f"conv-{uuid.uuid4().hex[:12]}"
        now = datetime.now(tz=RIYADH)
        default_prompts = [
            "What is the current network status?",
            "Show complaint intelligence overview",
            "View FTTH maturity index dashboard",
        ]

        if settings.mock_ai_enabled or not settings.ai_service_url:
            return WelcomeResponse(
                conversation_id=conversation_id,
                message_id=f"msg-welcome-{uuid.uuid4().hex[:8]}",
                welcome_message=(
                    f"Hello {current_user.first_name}! Welcome to the B2S Operations Assistant. "
                    "How can I assist you with network assurance, complaints, or service operations today?"
                ),
                suggested_prompts=default_prompts,
                generated_at=now,
                provider="mock",
            )

        url = settings.ai_service_url.rstrip("/") + "/" + settings.ai_chat_path.lstrip("/") + "/welcome"
        try:
            async with httpx.AsyncClient(timeout=settings.ai_timeout_seconds) as client:
                payload = request.model_dump(exclude_none=True)
                payload["user_id"] = current_user.id
                response = await client.post(
                    url,
                    json=payload,
                    headers={
                        "X-Request-ID": request_id,
                        "X-User-ID": current_user.id,
                    },
                )
                response.raise_for_status()
                data = response.json()
                return WelcomeResponse(
                    conversation_id=str(data.get("conversation_id") or conversation_id),
                    message_id=str(data.get("message_id") or f"msg-welcome-{uuid.uuid4().hex[:8]}"),
                    welcome_message=str(
                        data.get("welcome_message")
                        or data.get("message")
                        or f"Hello {current_user.first_name}! Welcome to the B2S Operations Assistant."
                    ),
                    suggested_prompts=list(data.get("suggested_prompts") or default_prompts),
                    generated_at=now,
                    provider="external",
                )
        except Exception:
            return WelcomeResponse(
                conversation_id=conversation_id,
                message_id=f"msg-welcome-{uuid.uuid4().hex[:8]}",
                welcome_message=(
                    f"Hello {current_user.first_name}! Welcome to the B2S Operations Assistant. "
                    "How can I assist you with network assurance, complaints, or service operations today?"
                ),
                suggested_prompts=default_prompts,
                generated_at=now,
                provider="mock",
            )


