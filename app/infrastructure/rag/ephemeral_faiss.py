"""FAISS efêmero por sessão de análise. Anexos do analista vivem só na sessão.

Mantemos um `FAISS` em memória por `session_id` com TTL configurável. Não
persiste em disco para não poluir a knowledge base global.
"""
from __future__ import annotations

import threading
import time
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config import settings
from app.domain.knowledge.entities import KnowledgeChunk
from app.infrastructure.llm.providers import get_embeddings


def _chunk_to_doc(c: KnowledgeChunk) -> Document:
    return Document(page_content=c.content, metadata={"source": c.source, **c.metadata})


def _doc_to_chunk(d: Document) -> KnowledgeChunk:
    meta = dict(d.metadata)
    source = meta.pop("source", "anexo")
    return KnowledgeChunk(content=d.page_content, source=source, metadata=meta)


class _Entry:
    __slots__ = ("store", "touched")

    def __init__(self, store: FAISS):
        self.store: FAISS = store
        self.touched: float = time.time()


class EphemeralFAISSManager:
    """Singleton thread-safe que hospeda um FAISS por session_id."""

    def __init__(self) -> None:
        self._stores: dict[str, _Entry] = {}
        self._lock = threading.Lock()
        self._emb = None

    def _embeddings(self):
        if self._emb is None:
            self._emb = get_embeddings()
        return self._emb

    def _expire(self) -> None:
        ttl = settings.ephemeral_index_ttl_seconds
        now = time.time()
        with self._lock:
            for k in [k for k, v in self._stores.items() if now - v.touched > ttl]:
                self._stores.pop(k, None)

    def add(self, session_id: str, chunks: List[KnowledgeChunk]) -> int:
        if not chunks:
            return 0
        self._expire()
        docs = [_chunk_to_doc(c) for c in chunks]
        with self._lock:
            entry = self._stores.get(session_id)
            if entry is None:
                entry = _Entry(FAISS.from_documents(docs, self._embeddings()))
                self._stores[session_id] = entry
            else:
                entry.store.add_documents(docs)
            entry.touched = time.time()
        return len(chunks)

    def search(self, session_id: str, query: str, k: int = 4) -> list[tuple[KnowledgeChunk, float]]:
        self._expire()
        entry = self._stores.get(session_id)
        if entry is None:
            return []
        entry.touched = time.time()
        try:
            pairs = entry.store.similarity_search_with_score(query, k=k)
            return [(_doc_to_chunk(d), float(s)) for d, s in pairs]
        except Exception:
            return []

    def has(self, session_id: str) -> bool:
        return session_id in self._stores

    def drop(self, session_id: str) -> None:
        with self._lock:
            self._stores.pop(session_id, None)


_manager: EphemeralFAISSManager | None = None


def get_ephemeral_manager() -> EphemeralFAISSManager:
    global _manager
    if _manager is None:
        _manager = EphemeralFAISSManager()
    return _manager
