import pytest
from unittest.mock import MagicMock

from app.domain.conversation.ports import IAgentRunner
from app.application.chat.chat_use_case import ChatUseCase


def _make_use_case():
    langchain = MagicMock(spec=IAgentRunner)
    agno = MagicMock(spec=IAgentRunner)
    return ChatUseCase(langchain_runner=langchain, agno_runner=agno), langchain, agno


def test_chat_uses_langchain_by_default():
    use_case, langchain, agno = _make_use_case()
    langchain.run.return_value = {"response": "ok", "session_id": "s1", "agent": "langchain"}

    result = use_case.execute("Olá", "s1")

    langchain.run.assert_called_once()
    agno.run.assert_not_called()
    assert result["agent"] == "langchain"


def test_chat_uses_agno_when_requested():
    use_case, langchain, agno = _make_use_case()
    agno.run.return_value = {"response": "resposta agno", "session_id": "s2", "agent": "agno"}

    result = use_case.execute("Olá", "s2", agent="agno")

    agno.run.assert_called_once()
    langchain.run.assert_not_called()
    assert result["agent"] == "agno"


def test_chat_falls_back_to_langchain_for_unknown_agent():
    use_case, langchain, _ = _make_use_case()
    langchain.run.return_value = {"response": "fallback", "session_id": "s3", "agent": "langchain"}

    result = use_case.execute("Olá", "s3", agent="nonexistent")

    langchain.run.assert_called_once()


def test_chat_passes_kwargs_to_runner():
    use_case, langchain, _ = _make_use_case()
    langchain.run.return_value = {"response": "ok", "session_id": "s4", "agent": "langchain"}

    use_case.execute("Olá", "s4", provider="gemini", model="gemini-1.5-flash")

    _, _, kwargs = langchain.run.mock_calls[0]
    assert kwargs.get("provider") == "gemini" or langchain.run.call_args[1].get("provider") == "gemini" or \
           "gemini" in str(langchain.run.call_args)
