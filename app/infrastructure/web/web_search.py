"""Pesquisa web simples. Tenta Tavily (se key), depois DuckDuckGo, senão noop."""
from __future__ import annotations

from typing import Any

from loguru import logger

from app.config import settings


def _tavily(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    if not settings.tavily_api_key:
        return []
    try:
        from tavily import TavilyClient  # type: ignore
        client = TavilyClient(api_key=settings.tavily_api_key)
        res = client.search(query=query, max_results=max_results, include_answer=False)
        return [
            {"title": r.get("title", ""), "url": r.get("url", ""), "snippet": r.get("content", "")}
            for r in res.get("results", [])
        ]
    except Exception as e:
        logger.warning(f"Tavily falhou: {e}")
        return []


def _duckduckgo(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    try:
        from duckduckgo_search import DDGS  # type: ignore
        with DDGS() as ddg:
            results = list(ddg.text(query, max_results=max_results, safesearch="moderate"))
        return [
            {"title": r.get("title", ""), "url": r.get("href", ""), "snippet": r.get("body", "")}
            for r in results
        ]
    except Exception as e:
        logger.warning(f"DuckDuckGo falhou: {e}")
        return []


def web_search(query: str, max_results: int = 5) -> list[dict[str, Any]]:
    out = _tavily(query, max_results)
    if out:
        return out
    return _duckduckgo(query, max_results)
