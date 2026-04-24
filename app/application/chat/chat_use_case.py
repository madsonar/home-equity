from typing import Any
from app.domain.conversation.ports import IAgentRunner


class ChatUseCase:
    def __init__(self, langchain_runner: IAgentRunner, agno_runner: IAgentRunner):
        self._runners: dict[str, IAgentRunner] = {
            "langchain": langchain_runner,
            "agno": agno_runner,
        }

    def execute(
        self,
        message: str,
        session_id: str,
        agent: str = "langchain",
        **kwargs,
    ) -> dict[str, Any]:
        runner = self._runners.get(agent, self._runners["langchain"])
        return runner.run(message, session_id, **kwargs)
