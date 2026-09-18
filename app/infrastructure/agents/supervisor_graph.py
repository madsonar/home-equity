"""
Supervisor LangGraph para análise de crédito com múltiplos agentes especialistas
e Human-in-the-loop para decisão final de aprovação.

Fluxo:
  supervisor → plan (lista de agentes) → fan-out paralelo dos especialistas
             → compose_answer → ask_human (interrupt) → apply_decision.

Estado é checkpointado (MemorySaver por default; configurável para Postgres).
"""
from __future__ import annotations

import json
from typing import Any, Literal, TypedDict

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, START, StateGraph
from langgraph.types import interrupt
from loguru import logger

from app.infrastructure.agents.experts import (
    credit_expert, rag_expert, regulation_expert, viability_expert,
    web_research_expert,
)
from app.infrastructure.llm.providers import get_langchain_llm


# ── Estado ────────────────────────────────────────────────────────────────────


class AnalysisState(TypedDict, total=False):
    # Input
    request_id: int
    session_id: str
    request_payload: dict[str, Any]
    score_snapshot: dict[str, Any] | None
    user_message: str                  # mensagem do analista
    # Planejamento
    plan: list[str]                    # agentes a chamar
    # Resultados parciais
    rag_findings: dict[str, Any]
    regulation_findings: dict[str, Any]
    credit_findings: dict[str, Any]
    viability_findings: dict[str, Any]
    web_findings: dict[str, Any]
    # Saída
    supervisor_answer: str
    sources: list[dict[str, Any]]
    # HITL
    pending_decision: bool
    decision: Literal["approved", "rejected"] | None
    rationale: str


AGENT_SET = {"rag", "regulation", "credit", "viability", "web"}


# ── Nó: supervisor (planejamento) ────────────────────────────────────────────


SUPERVISOR_PROMPT = """Você é o supervisor de uma equipe de análise de crédito Home Equity.

Dado o contexto da solicitação e a mensagem do analista, escolha quais especialistas
consultar. Opções:
- rag: busca base de conhecimento + anexos da sessão (FAISS efêmero).
- regulation: normas BACEN (Res. 4.676/2018, Lei 9.514/1997, LTV).
- credit: score ML, LTV, DTI, parcela.
- viability: análise consolidada de viabilidade financeira.
- web: pesquisa web sobre o perfil/profissão/notícias recentes.

Responda SOMENTE em JSON estrito:
{"plan": ["rag", "regulation", ...], "reasoning": "breve racional"}

Inclua somente os agentes necessários. Default sugerido: ["rag","regulation","credit"].
"""


def _supervisor_node(state: AnalysisState) -> dict[str, Any]:
    msg = state.get("user_message", "")
    payload = state.get("request_payload", {})
    snapshot = state.get("score_snapshot", {})
    ctx = (
        f"Solicitação: {json.dumps(payload, ensure_ascii=False)}\n"
        f"Score atual: {json.dumps(snapshot, ensure_ascii=False)}\n"
        f"Mensagem do analista: {msg}"
    )
    llm = get_langchain_llm()
    try:
        resp = llm.invoke([SystemMessage(content=SUPERVISOR_PROMPT), HumanMessage(content=ctx)])
        raw = resp.content if isinstance(resp.content, str) else "".join(
            p.get("text", "") if isinstance(p, dict) else str(p) for p in resp.content
        )
        start = raw.find("{"); end = raw.rfind("}")
        data = json.loads(raw[start:end + 1]) if start >= 0 and end > start else {}
        plan = [p for p in data.get("plan", []) if p in AGENT_SET]
    except Exception as e:
        logger.warning(f"supervisor planning falhou, usando default: {e}")
        plan = []
    if not plan:
        plan = ["rag", "regulation", "credit"]
    return {"plan": plan}


# ── Nós dos especialistas (wrapper do estado) ────────────────────────────────


def _run_rag(state: AnalysisState) -> dict[str, Any]:
    out = rag_expert.run(
        session_id=state.get("session_id", ""),
        query=state.get("user_message", ""),
        payload=state.get("request_payload", {}),
    )
    return {"rag_findings": out}


def _run_regulation(state: AnalysisState) -> dict[str, Any]:
    out = regulation_expert.run(query=state.get("user_message", ""))
    return {"regulation_findings": out}


def _run_credit(state: AnalysisState) -> dict[str, Any]:
    out = credit_expert.run(payload=state.get("request_payload", {}))
    return {"credit_findings": out}


def _run_viability(state: AnalysisState) -> dict[str, Any]:
    out = viability_expert.run(
        payload=state.get("request_payload", {}),
        score_snapshot=state.get("score_snapshot", {}),
    )
    return {"viability_findings": out}


def _run_web(state: AnalysisState) -> dict[str, Any]:
    out = web_research_expert.run(
        payload=state.get("request_payload", {}),
        query=state.get("user_message", ""),
    )
    return {"web_findings": out}


# ── Nó: compose_answer ───────────────────────────────────────────────────────


COMPOSE_PROMPT = """Você é o supervisor sênior do backoffice de análise de crédito.
Consolide os achados dos especialistas em uma resposta objetiva e útil para o analista
que está analisando a solicitação. Seja conciso (máximo ~250 palavras), estruturado
(use bullet points), cite fontes quando disponíveis. NÃO decida aprovação — apenas
apresente evidências e recomendação. Responda em português BR."""


def _compose_node(state: AnalysisState) -> dict[str, Any]:
    parts: list[str] = []
    sources: list[dict[str, Any]] = []

    for name, key in [
        ("RAG (base + anexos)", "rag_findings"),
        ("Regulação BACEN", "regulation_findings"),
        ("Crédito/ML", "credit_findings"),
        ("Viabilidade", "viability_findings"),
        ("Pesquisa Web", "web_findings"),
    ]:
        d: dict[str, Any] = state.get(key) or {}  # type: ignore[assignment]
        if d:
            parts.append(f"[{name}]\n{d.get('summary', '')}")
            for s in d.get("sources", []) or []:
                sources.append(s)

    llm = get_langchain_llm()
    user = (
        f"Mensagem do analista:\n{state.get('user_message', '')}\n\n"
        f"Solicitação:\n{json.dumps(state.get('request_payload', {}), ensure_ascii=False)}\n\n"
        f"Achados:\n" + "\n\n".join(parts)
    )
    try:
        resp = llm.invoke([SystemMessage(content=COMPOSE_PROMPT), HumanMessage(content=user)])
        raw = resp.content if isinstance(resp.content, str) else "".join(
            p.get("text", "") if isinstance(p, dict) else str(p) for p in resp.content
        )
    except Exception as e:
        logger.exception("compose falhou")
        raw = f"Falha ao compor resposta: {e}\n\nAchados crus:\n" + "\n\n".join(parts)
    return {"supervisor_answer": raw, "sources": sources, "pending_decision": True}


# ── Nó: ask_human (HITL) ─────────────────────────────────────────────────────


def _ask_human_node(state: AnalysisState) -> dict[str, Any]:
    """Pausa o grafo até o analista responder. O runner externo (WS) deve chamar
    `graph.invoke(Command(resume={"decision":..., "rationale":...}), config=cfg)`."""
    payload = interrupt({
        "question": "Aprovar ou reprovar esta solicitação?",
        "answer": state.get("supervisor_answer", ""),
    })
    # Ao resumir, `payload` traz a decisão
    return {
        "decision": payload.get("decision"),
        "rationale": payload.get("rationale", ""),
        "pending_decision": False,
    }


# ── Nó: apply_decision — grava em Postgres + notifica cliente ────────────────


def _apply_decision_node(state: AnalysisState) -> dict[str, Any]:
    from datetime import datetime, timezone
    from app.infrastructure.db.models import (
        AnalysisSession, ClientNotification, DecisionRecord, Decision,
        SimulationRequest, SimulationStatus,
    )
    from app.infrastructure.db.session import session_scope

    decision = state.get("decision")
    rationale = state.get("rationale", "")
    req_id = state.get("request_id")
    if not decision or not req_id:
        return {}
    decision_enum = Decision.approved if decision == "approved" else Decision.rejected
    status_enum = SimulationStatus.approved if decision == "approved" else SimulationStatus.rejected

    with session_scope() as db:
        sess = db.query(AnalysisSession).filter(
            AnalysisSession.request_id == req_id,
        ).first()
        analyst_id = sess.analyst_id if sess else None
        sim = db.get(SimulationRequest, req_id)
        if sim is not None:
            sim.status = status_enum
            sim.decided_at = datetime.now(timezone.utc)
            sim.public_message = rationale
        if sess is not None and not sess.closed_at:
            sess.closed_at = datetime.now(timezone.utc)
        if analyst_id:
            db.add(DecisionRecord(
                request_id=req_id, analyst_id=analyst_id,
                decision=decision_enum, rationale=rationale,
            ))
        if sim is not None:
            title = "Sua solicitação foi aprovada" if decision == "approved" else "Sua solicitação não foi aprovada"
            db.add(ClientNotification(
                client_id=sim.client_id, request_id=req_id,
                title=title, body=rationale,
            ))
    return {"supervisor_answer": f"Decisão registrada: {decision.upper()}. {rationale}"}


# ── Roteamento condicional ───────────────────────────────────────────────────


def _from_supervisor(state: AnalysisState) -> list[str]:
    plan = state.get("plan", [])
    return [
        {"rag": "rag_expert", "regulation": "regulation_expert",
         "credit": "credit_expert", "viability": "viability_expert",
         "web": "web_research_expert"}[p]
        for p in plan if p in AGENT_SET
    ] or ["compose_answer"]


# ── Compilação ───────────────────────────────────────────────────────────────


_graph = None
_checkpointer = None


def _build_graph():
    global _graph, _checkpointer
    if _graph is not None:
        return _graph

    g = StateGraph(AnalysisState)
    g.add_node("supervisor", _supervisor_node)
    g.add_node("rag_expert", _run_rag)
    g.add_node("regulation_expert", _run_regulation)
    g.add_node("credit_expert", _run_credit)
    g.add_node("viability_expert", _run_viability)
    g.add_node("web_research_expert", _run_web)
    g.add_node("compose_answer", _compose_node)
    g.add_node("ask_human", _ask_human_node)
    g.add_node("apply_decision", _apply_decision_node)

    g.add_edge(START, "supervisor")
    g.add_conditional_edges("supervisor", _from_supervisor,
                            ["rag_expert", "regulation_expert", "credit_expert",
                             "viability_expert", "web_research_expert", "compose_answer"])
    for n in ("rag_expert", "regulation_expert", "credit_expert",
              "viability_expert", "web_research_expert"):
        g.add_edge(n, "compose_answer")
    g.add_edge("compose_answer", "ask_human")
    g.add_edge("ask_human", "apply_decision")
    g.add_edge("apply_decision", END)

    _checkpointer = MemorySaver()
    _graph = g.compile(checkpointer=_checkpointer)
    return _graph


def get_supervisor_graph():
    return _build_graph()
