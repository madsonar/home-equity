from typing import List
from langchain_classic.memory import ConversationBufferWindowMemory, VectorStoreRetrieverMemory
from langchain_core.messages import BaseMessage
from langchain_chroma import Chroma

from app.config import settings
from app.infrastructure.llm.providers import get_embeddings
from app.domain.conversation.entities import ConversationSession, Message, MessageRole
from app.domain.conversation.ports import IMemoryStore


def get_short_term_memory(session_id: str) -> ConversationBufferWindowMemory:
    return ConversationBufferWindowMemory(
        k=settings.short_term_memory_window, memory_key="chat_history", return_messages=True,
        input_key="input", output_key="output",
    )


def get_long_term_memory(session_id: str) -> VectorStoreRetrieverMemory:
    vectorstore = Chroma(
        collection_name=f"{settings.memory_collection_prefix}{session_id}",
        embedding_function=get_embeddings(),
        persist_directory=settings.chroma_persist_path,
    )
    return VectorStoreRetrieverMemory(
        retriever=vectorstore.as_retriever(search_kwargs={"k": 3}),
        memory_key="relevant_history",
        input_key="input",
    )


class ConversationManager(IMemoryStore):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.short_term = get_short_term_memory(session_id)
        self.long_term = get_long_term_memory(session_id)

    def save(self, session_id: str, user_input: str, ai_output: str) -> None:
        self.short_term.save_context({"input": user_input}, {"output": ai_output})
        self.long_term.save_context({"input": user_input}, {"output": ai_output})

    def get_session(self, session_id: str) -> ConversationSession:
        messages = []
        for msg in self.short_term.chat_memory.messages:
            role = MessageRole.USER if msg.type == "human" else MessageRole.ASSISTANT
            messages.append(Message(role=role, content=msg.content))
        return ConversationSession(session_id=session_id, messages=messages)

    def clear(self) -> None:
        self.short_term.clear()
