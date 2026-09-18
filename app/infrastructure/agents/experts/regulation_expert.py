"""Especialista em regulação BACEN: retrieval focado em termos regulatórios."""
from __future__ import annotations

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger

from app.infrastructure.agents.experts.rag_expert import _store
from app.infrastructure.llm.providers import get_langchain_llm


REG_PROMPT = """Você é especialista em regulação financeira brasileira (BACEN, CMN).
Dado os trechos regulatórios abaixo e a pergunta do analista, produza um parecer
curto (máximo 6 linhas) em bullet points citando Resolução/Lei/artigo. Em português BR."""


def run(*, query: str) -> dict[str, Any]:
    reg_query = f"BACEN regulação Home Equity alienação fiduciária LTV {query or ''}"
    evidence: list[str] = []
    sources: list[dict[str, Any]] = []
    try:
        hits = _store().search_with_score(reg_query, k=6)
        for chunk, score in hits:
            src = chunk.source or ""
            if any(k in src.lower() for k in ("regula", "bacen", "home_equity", "resolu")):
                evidence.append(chunk.content[:500])
                sources.append({"source": src, "score": round(float(score), 4)})
        if not evidence:
            # fallback: topo 3 mesmo sem filtro
            for chunk, score in hits[:3]:
                evidence.append(chunk.content[:500])
                sources.append({"source": chunk.source, "score": round(float(score), 4)})
    except Exception as e:
        logger.warning(f"regulation retrieval falhou: {e}")

    context = "\n---\n".join(evidence) if evidence else "(sem evidências regulatórias encontradas)"
    try:
        resp = get_langchain_llm().invoke([
            SystemMessage(content=REG_PROMPT),
            HumanMessage(content=f"Pergunta do analista: {query}\n\nTrechos:\n{context}"),
        ])
        content = resp.content if isinstance(resp.content, str) else "".join(
            p.get("text", "") if isinstance(p, dict) else str(p) for p in resp.content
        )
    except Exception as e:
        content = f"Falha no LLM regulatório: {e}"
    return {"summary": content, "sources": sources}
