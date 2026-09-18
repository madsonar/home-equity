import os
from typing import List
import numpy as np
import faiss
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

from app.config import settings
from app.infrastructure.llm.providers import get_embeddings
from app.domain.knowledge.entities import KnowledgeChunk
from app.domain.knowledge.ports import IVectorStore


_faiss_store: FAISS | None = None


def _chunk_to_doc(chunk: KnowledgeChunk) -> Document:
    return Document(page_content=chunk.content, metadata={"source": chunk.source, **chunk.metadata})


def _doc_to_chunk(doc: Document) -> KnowledgeChunk:
    meta = dict(doc.metadata)
    source = meta.pop("source", "unknown")
    return KnowledgeChunk(content=doc.page_content, source=source, metadata=meta)


def _get_embeddings():
    return get_embeddings()


class FAISSVectorStore(IVectorStore):
    def _get_store(self) -> FAISS | None:
        global _faiss_store
        index_path = settings.faiss_index_path
        if _faiss_store is None and os.path.exists(f"{index_path}/index.faiss"):
            _faiss_store = FAISS.load_local(
                index_path, _get_embeddings(), allow_dangerous_deserialization=True
            )
        return _faiss_store

    def add(self, chunks: List[KnowledgeChunk]) -> int:
        global _faiss_store
        docs = [_chunk_to_doc(c) for c in chunks]
        embeddings = _get_embeddings()
        if _faiss_store is None:
            _faiss_store = FAISS.from_documents(docs, embeddings)
        else:
            _faiss_store.add_documents(docs)
        os.makedirs(settings.faiss_index_path, exist_ok=True)
        _faiss_store.save_local(settings.faiss_index_path)
        return len(chunks)

    def search(self, query: str, k: int = 4) -> List[KnowledgeChunk]:
        store = self._get_store()
        if store is None:
            return []
        return [_doc_to_chunk(d) for d in store.similarity_search(query, k=k)]

    def search_with_score(self, query: str, k: int = 4) -> List[tuple[KnowledgeChunk, float]]:
        store = self._get_store()
        if store is None:
            return []
        return [(_doc_to_chunk(d), s) for d, s in store.similarity_search_with_score(query, k=k)]


def build_faiss_index_from_vectors(vectors: np.ndarray) -> faiss.IndexFlatL2:
    dim = vectors.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(vectors.astype("float32"))
    return index
