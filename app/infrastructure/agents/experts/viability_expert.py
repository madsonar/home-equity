"""Especialista em viabilidade: análise financeira consolidada."""
from __future__ import annotations

from typing import Any

from langchain_core.messages import HumanMessage, SystemMessage
from loguru import logger

from app.infrastructure.llm.providers import get_langchain_llm


VIA_PROMPT = """Você é analista sênior de viabilidade financeira de crédito imobiliário.
Produza um parecer curto (máximo 8 linhas) avaliando: (a) comprometimento de renda (DTI),
(b) LTV vs limite, (c) capacidade de pagamento frente ao prazo, (d) riscos. Termine com
UMA recomendação: "recomendo aprovação", "recomendo aprovação com ressalvas",
"recomendo reprovação". Responda em português BR."""


def run(*, payload: dict[str, Any], score_snapshot: dict[str, Any]) -> dict[str, Any]:
    try:
        context = (
            f"Solicitação: renda R$ {payload.get('monthly_income', 0):,.0f}, "
            f"imóvel R$ {payload.get('property_value', 0):,.0f}, "
            f"valor R$ {payload.get('requested_amount', 0):,.0f}, "
            f"idade {payload.get('age', '-')}, "
            f"anos emprego {payload.get('employment_years', '-')}, "
            f"outras dívidas: {payload.get('has_other_debts', False)}, "
            f"profissão: {payload.get('profession', '-')}.\n"
            f"Score: {score_snapshot or {}}."
        )
        resp = get_langchain_llm().invoke([
            SystemMessage(content=VIA_PROMPT), HumanMessage(content=context),
        ])
        content = resp.content if isinstance(resp.content, str) else "".join(
            p.get("text", "") if isinstance(p, dict) else str(p) for p in resp.content
        )
        return {"summary": content, "sources": []}
    except Exception as e:
        logger.exception("viability_expert falhou")
        return {"summary": f"Falha na análise de viabilidade: {e}", "sources": []}
