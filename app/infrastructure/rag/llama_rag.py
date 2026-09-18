from typing import List
import chromadb
from chromadb.config import Settings as ChromaSettings

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings as LlamaSettings,
    Document as LlamaDocument,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
from app.config import settings


def _configure_llama():
    from app.infrastructure.llm.providers import get_langchain_llm, get_embeddings  # noqa: F401
    # LLM via provider configurado no .env
    if settings.default_llm_provider in ("google", "gemini"):
        from llama_index.llms.langchain import LangChainLLM
        LlamaSettings.llm = LangChainLLM(llm=get_langchain_llm())
    else:
        from llama_index.llms.openai import OpenAI as LlamaOpenAI
        LlamaSettings.llm = LlamaOpenAI(model=settings.default_llm_model, api_key=settings.openai_api_key)
    # Embeddings via provider configurado no .env
    if settings.embedding_provider in ("google", "gemini"):
        from llama_index.embeddings.langchain import LangchainEmbedding
        LlamaSettings.embed_model = LangchainEmbedding(get_embeddings())
    else:
        from llama_index.embeddings.openai import OpenAIEmbedding
        LlamaSettings.embed_model = OpenAIEmbedding(
            model=settings.embedding_model, api_key=settings.openai_api_key
        )


def _get_chroma_vector_store():
    client = chromadb.PersistentClient(
        path=settings.chroma_persist_path,
        settings=ChromaSettings(anonymized_telemetry=False),
    )
    collection = client.get_or_create_collection(settings.llama_collection)
    return ChromaVectorStore(chroma_collection=collection)


def build_llama_index(texts: List[str]) -> VectorStoreIndex:
    _configure_llama()
    documents = [LlamaDocument(text=t) for t in texts]
    vector_store = _get_chroma_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_documents(documents, storage_context=storage_context)


def get_llama_index() -> VectorStoreIndex:
    _configure_llama()
    vector_store = _get_chroma_vector_store()
    storage_context = StorageContext.from_defaults(vector_store=vector_store)
    return VectorStoreIndex.from_vector_store(vector_store, storage_context=storage_context)


def query_llama(question: str) -> str:
    index = get_llama_index()
    engine = index.as_query_engine(similarity_top_k=4)
    return str(engine.query(question))
