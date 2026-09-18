from dataclasses import dataclass, field
from typing import List
from enum import Enum


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    role: MessageRole
    content: str


@dataclass
class ConversationSession:
    session_id: str
    messages: List[Message] = field(default_factory=list)
