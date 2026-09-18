from abc import ABC, abstractmethod
from typing import Any
from .entities import ConversationSession


class IAgentRunner(ABC):
    @abstractmethod
    def run(self, message: str, session_id: str, **kwargs) -> dict[str, Any]: ...


class IMemoryStore(ABC):
    @abstractmethod
    def save(self, session_id: str, user_input: str, ai_output: str) -> None: ...

    @abstractmethod
    def get_session(self, session_id: str) -> ConversationSession: ...
