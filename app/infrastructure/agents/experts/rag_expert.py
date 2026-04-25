"""RAG: consulta anexos da sessão (FAISS efêmero) + KB global (Chroma)."""
from __future__ import annotations

from typing import Any

from loguru import logger

from app.config import settings
from app.infrastructure.rag.chroma_store import ChromaVectorStore
from app.infrastructure.rag.ephemeral_faiss import get_ephemeral_manager


_chroma: ChromaVectorStore | None = None


def _store() -> ChromaVectorStore:
    global _chroma
    if _chroma is None:
        _chroma = ChromaVectorStore()
    return _chroma


def run(*, session_id: str, query: str, payload: dict[str, Any]) -> dict[str, Any]:
    if not query:
        query = f"análise de crédito valor {payload.get('requested_amount', 0)} imóvel {payload.get('property_value', 0)}"

    sources: list[dict[str, Any]] = []
    bullets: list[str] = []

    # 1) Anexos da sessão primeiro (prioridade)
    mgr = get_ephemeral_manager()
    if session_id and mgr.has(session_id):
        for chunk, score in mgr.search(session_id, query, k=3):
            bullets.append(f"(anexo) {chunk.content[:320]}")
            sources.append({"source": f"anexo:{chunk.source}", "score": round(float(score), 4)})

    # 2) KB global
    try:
        for chunk, score in _store().search_with_score(query, k=settings.rag_top_k):
            bullets.append(f"(kb) {chunk.content[:320]}")
            sources.append({"source": chunk.source, "score": round(float(score), 4)})
    except Exception as e:
        logger.warning(f"RAG Chroma falhou: {e}")

    summary = "Evidências recuperadas:\n" + "\n---\n".join(bullets) if bullets else "Nenhuma evidência relevante."
    return {"summary": summary, "sources": sources}
