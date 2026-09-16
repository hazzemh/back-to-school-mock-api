from datetime import datetime
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    conversation_id: str | None = None


class ChatResponse(BaseModel):
    conversation_id: str
    message_id: str
    answer: str
    generated_at: datetime
    provider: str
