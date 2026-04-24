"""Factory central de componentes configuráveis pelo `.env`.

Todo o código que precise de LLM, embeddings, vector store, agente ou
cliente de LLM provider passa por aqui — nunca instancia classes
concretas diretamente.

Fluxo: Settings (.env) → factory.get_X() → instância pronta para uso.

Para trocar provider/modelo/backend, edite apenas o `.env`.
"""
from __future__ import annotations

from functools import lru_cache
from typing import Any

from langchain_core.embeddings import Embeddings
from langchain_core.language_models import BaseChatModel

from app.config import settings


# ═══════════════════════════════════════════════════════════════════════════
#  LLM (chat / score)
# ═══════════════════════════════════════════════════════════════════════════
def get_langchain_llm(
    provider: str | None = None,
    model: str | None = None,
    temperature: float | None = None,
) -> BaseChatModel:
    """Retorna um LangChain ChatModel do provider/modelo configurado."""
    provider = (provider or settings.default_llm_provider).lower()
    model = model or settings.default_llm_model
    temperature = settings.default_llm_temperature if temperature is None else temperature

    if provider == "openai":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(model=model, temperature=temperature, api_key=settings.openai_api_key)

    if provider in ("google", "gemini"):
        from langchain_google_genai import ChatGoogleGenerativeAI
        return ChatGoogleGenerativeAI(
            model=model, temperature=temperature, google_api_key=settings.google_api_key,
        )

    if provider == "deepseek":
        from langchain_openai import ChatOpenAI
        return ChatOpenAI(
            model=model, temperature=temperature,
            api_key=settings.deepseek_api_key, base_url="https://api.deepseek.com",
        )

    if provider == "cohere":
        from langchain_cohere import ChatCohere
        return ChatCohere(model=model, cohere_api_key=settings.cohere_api_key, temperature=temperature)

    raise ValueError(
        f"Provider LLM não suportado: {provider!r}. "
        "Use: openai | google | deepseek | cohere (env DEFAULT_LLM_PROVIDER)."
    )


# Alias curto
get_llm = get_langchain_llm


# ═══════════════════════════════════════════════════════════════════════════
#  Embeddings
# ═══════════════════════════════════════════════════════════════════════════
@lru_cache(maxsize=4)
def get_embeddings(provider: str | None = None, model: str | None = None) -> Embeddings:
    """Retorna Embeddings do provider configurado (cacheado)."""
    provider = (provider or settings.embedding_provider).lower()
    model = model or settings.embedding_model

    if provider in ("google", "gemini"):
        from langchain_google_genai import GoogleGenerativeAIEmbeddings
        return GoogleGenerativeAIEmbeddings(model=model, google_api_key=settings.google_api_key)

    if provider == "openai":
        from langchain_openai import OpenAIEmbeddings
        return OpenAIEmbeddings(model=model, api_key=settings.openai_api_key)

    if provider == "cohere":
        from langchain_cohere import CohereEmbeddings
        return CohereEmbeddings(model=model, cohere_api_key=settings.cohere_api_key)

    if provider in ("local", "huggingface", "sentence-transformers"):
        from langchain_community.embeddings import HuggingFaceEmbeddings
        return HuggingFaceEmbeddings(model_name=settings.local_embedding_model)

    raise ValueError(
        f"Provider de embeddings não suportado: {provider!r}. "
        "Use: google | openai | cohere | local (env EMBEDDING_PROVIDER)."
    )


# ═══════════════════════════════════════════════════════════════════════════
#  LlamaIndex — LLM + embedding globais
# ═══════════════════════════════════════════════════════════════════════════
def configure_llamaindex() -> None:
    from llama_index.core import Settings as LlamaSettings
    from llama_index.llms.langchain import LangChainLLM
    from llama_index.embeddings.langchain import LangchainEmbedding

    LlamaSettings.llm = LangChainLLM(llm=get_langchain_llm())
    LlamaSettings.embed_model = LangchainEmbedding(get_embeddings())


# ═══════════════════════════════════════════════════════════════════════════
#  Agno — modelo nativo
# ═══════════════════════════════════════════════════════════════════════════
def get_agno_model(provider: str | None = None, model: str | None = None) -> Any:
    provider = (provider or settings.default_llm_provider).lower()
    model = model or settings.default_llm_model

    if provider in ("google", "gemini"):
        from agno.models.google import Gemini
        return Gemini(id=model, api_key=settings.google_api_key)

    if provider == "openai":
        from agno.models.openai import OpenAIChat
        return OpenAIChat(id=model, api_key=settings.openai_api_key)

    if provider == "deepseek":
        from agno.models.deepseek import DeepSeek
        return DeepSeek(id=model, api_key=settings.deepseek_api_key)

    raise ValueError(f"Agno ainda não suporta provider {provider!r}.")


# ═══════════════════════════════════════════════════════════════════════════
#  Vector store (backend = settings.vector_store_backend)
# ═══════════════════════════════════════════════════════════════════════════
def get_vector_store():
    backend = settings.vector_store_backend.lower()
    if backend == "chroma":
        from app.infrastructure.rag.chroma_store import ChromaVectorStore
        return ChromaVectorStore()
    if backend == "faiss":
        from app.infrastructure.rag.faiss_store import FAISSVectorStore
        return FAISSVectorStore()
    raise ValueError(f"VECTOR_STORE_BACKEND inválido: {backend!r}. Use: chroma | faiss.")


# ═══════════════════════════════════════════════════════════════════════════
#  Agente (chat)
# ═══════════════════════════════════════════════════════════════════════════
def get_agent_runner(name: str | None = None):
    name = (name or settings.default_agent).lower()
    if name == "langchain":
        from app.infrastructure.agents.langchain_agent import LangchainAgentRunner
        return LangchainAgentRunner()
    if name == "agno":
        from app.infrastructure.agents.agno_agent import AgnoAgentRunner
        return AgnoAgentRunner()
    raise ValueError(f"Agente desconhecido: {name!r}. Use: langchain | agno.")


# ═══════════════════════════════════════════════════════════════════════════
#  Clientes utilitários
# ═══════════════════════════════════════════════════════════════════════════
def get_openai_client():
    from openai import OpenAI
    return OpenAI(api_key=settings.openai_api_key)
