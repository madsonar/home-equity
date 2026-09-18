"""Especialista em pesquisa web: consulta Tavily/DuckDuckGo sobre o cliente/profissão."""
from __future__ import annotations

from typing import Any

from loguru import logger

from app.infrastructure.web.web_search import web_search


def run(*, payload: dict[str, Any], query: str) -> dict[str, Any]:
    profession = str(payload.get("profession", "") or "")
    q = query.strip() or f"empréstimo home equity {profession} mercado imobiliário Brasil"
    try:
        results = web_search(q, max_results=5)
    except Exception as e:
        logger.warning(f"web_search falhou: {e}")
        results = []

    if not results:
        return {
            "summary": "Pesquisa web indisponível (sem API key Tavily ou rede restrita).",
            "sources": [],
        }
    bullets = [f"- {r['title']}: {r['snippet'][:200]}" for r in results]
    sources = [{"source": r["url"], "title": r["title"]} for r in results]
    return {"summary": "Resultados web:\n" + "\n".join(bullets), "sources": sources}
