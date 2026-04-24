from app.domain.knowledge.entities import KnowledgeChunk
from app.domain.conversation.entities import ConversationSession, Message, MessageRole


def test_knowledge_chunk_defaults():
    chunk = KnowledgeChunk(content="Texto relevante", source="doc.pdf")
    assert chunk.score == 0.0
    assert chunk.metadata == {}


def test_knowledge_chunk_with_metadata():
    chunk = KnowledgeChunk(
        content="Conteúdo",
        source="url",
        metadata={"type": "web", "title": "CashMe"},
        score=0.92,
    )
    assert chunk.metadata["type"] == "web"
    assert chunk.score == 0.92


def test_conversation_session():
    session = ConversationSession(session_id="sess-123")
    assert session.messages == []

    session.messages.append(Message(role=MessageRole.USER, content="Olá"))
    assert len(session.messages) == 1
    assert session.messages[0].role == MessageRole.USER


def test_message_roles():
    assert MessageRole.USER == "user"
    assert MessageRole.ASSISTANT == "assistant"
    assert MessageRole.SYSTEM == "system"
