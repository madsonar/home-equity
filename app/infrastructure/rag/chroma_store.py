from typing import List
import chromadb
from chromadb.config import Settings as ChromaSettings
from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.config import settings
from app.infrastructure.llm.providers import get_embeddings
from app.domain.knowledge.entities import KnowledgeChunk
from app.domain.knowledge.ports import IVectorStore


def _chunk_to_doc(chunk: KnowledgeChunk) -> Document:
    return Document(page_content=chunk.content, metadata={"source": chunk.source, **chunk.metadata})


def _doc_to_chunk(doc: Document, score: float = 0.0) -> KnowledgeChunk:
    meta = dict(doc.metadata)
    source = meta.pop("source", "unknown")
    return KnowledgeChunk(content=doc.page_content, source=source, metadata=meta, score=score)


def _get_embeddings():
    return get_embeddings()


def _get_client() -> chromadb.ClientAPI:
    if settings.app_env == "production":
        return chromadb.HttpClient(
            host=settings.chroma_host,
            port=settings.chroma_port,
            settings=ChromaSettings(anonymized_telemetry=False),
        )
    return chromadb.PersistentClient(
        path=settings.chroma_persist_path,
        settings=ChromaSettings(anonymized_telemetry=False),
    )


class ChromaVectorStore(IVectorStore):
    def _store(self) -> Chroma:
        return Chroma(
            client=_get_client(),
            collection_name=settings.chroma_collection,
            embedding_function=_get_embeddings(),
        )

    def add(self, chunks: List[KnowledgeChunk]) -> int:
        self._store().add_documents([_chunk_to_doc(c) for c in chunks])
        return len(chunks)

    def search(self, query: str, k: int = 4) -> List[KnowledgeChunk]:
        return [_doc_to_chunk(d) for d in self._store().similarity_search(query, k=k)]

    def search_with_score(self, query: str, k: int = 4) -> List[tuple[KnowledgeChunk, float]]:
        return [(_doc_to_chunk(d), s) for d, s in self._store().similarity_search_with_score(query, k=k)]
