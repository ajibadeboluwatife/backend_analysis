"""Backend Oracle API Chat Models Module."""

from pydantic import BaseModel


class Message(BaseModel):
    """A single message in a chat conversation."""

    role: str
    content: str


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""

    messages: list[Message]


class ChatChunk(BaseModel):
    """A chunk of streamed chat response."""

    content: str
    done: bool | None = False
