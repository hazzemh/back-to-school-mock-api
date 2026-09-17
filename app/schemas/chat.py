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


class ChatMessage(BaseModel):
    message_id: str
    role: str = Field(..., description="Role of the sender: 'user' or 'assistant'")
    content: str
    timestamp: datetime


class ChatHistoryResponse(BaseModel):
    conversation_id: str
    messages: list[ChatMessage]


class WelcomeRequest(BaseModel):
    conversation_id: str | None = Field(None, description="Optional existing conversation identifier")


class WelcomeResponse(BaseModel):
    conversation_id: str
    message_id: str
    welcome_message: str
    suggested_prompts: list[str] = Field(default_factory=list, description="Recommended starter prompts")
    generated_at: datetime
    provider: str


