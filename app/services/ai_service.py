from __future__ import annotations

import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

import httpx

from app.core.config import settings
from app.core.exceptions import AIServiceError
from app.schemas.chat import ChatRequest, ChatResponse
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
