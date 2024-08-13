from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field


class MessageIntent(str, Enum):
    question = "question"
    private = "private"

class Role(str, Enum):
    user = "user"
    system_manager = "system_manager"
    analysis_assistant = "analysis_assistant"
    streaming_assistant = "streaming_assistant"
    visual_assistant = "visual_assistant"
    progress_assistant = "progress_assistant"
    context_assistant = "context_assistant"

class Author(BaseModel):
    role: Optional[Role] = Field(default=Role.user.value)
    tool: Optional[str] = Field(default="")
    metadata: Optional[str] = Field(default="")

class Content(BaseModel):
    type: Optional[str] = Field(default="text")
    message: str
    metadata: Optional[str] = Field(default="")

class UserMessage(BaseModel):
    author: Author
    content: Content
    metadata: Optional[str] = Field(default="")

class SendMessageInput(BaseModel):
    chat_id: str
    focus: Optional[str] = Field(default="")
    is_new_chat: Optional[bool] = Field(default=True)
    sources: Optional[List[str]] = Field(default=[])
    user_message: UserMessage
    message_intent: Optional[MessageIntent]
    question_id: Optional[str] = Field(default="")
    message_id: Optional[str] = Field(default="")