"""Orquestra o supervisor LangGraph emitindo eventos para o WebSocket e
persistindo em Postgres. Thread_id do checkpoint = `analysis_sessions.thread_id`.
"""
from __future__ import annotations

import asyncio
import json
from typing import Any, AsyncIterator, Awaitable, Callable

from langgraph.types import Command
from loguru import logger

from app.infrastructure.agents.supervisor_graph import get_supervisor_graph
from app.infrastructure.db.models import AnalysisMessage, AnalysisSession, SimulationRequest
from app.infrastructure.db.session import session_scope
from app.infrastructure.observability.telemetry import (
    end_trace,
    get_langfuse_callback,
    start_trace,
)


AGENT_NODES = {
    "rag_expert", "regulation_expert", "credit_expert",
    "viability_expert", "web_research_expert", "supervisor",
    "compose_answer", "ask_human", "apply_decision",
}


def _persist(session_id: int, role: str, content: str, *,
             agent_name: str | None = None, event_type: str | None = None,
             metadata: dict | None = None) -> None:
    with session_scope() as db:
        db.add(AnalysisMessage(
            session_id=session_id, role=role, agent_name=agent_name,
            content=content, event_type=event_type, msg_metadata=metadata,
        ))


async def run_analyst_turn(
    *, db_session_id: int, thread_id: str, user_message: str,
    request_payload: dict[str, Any], request_id: int,
    score_snapshot: dict[str, Any] | None,
    emit: Callable[[dict[str, Any]], Awaitable[Any]],
) -> AsyncIterator[dict[str, Any]]:
    """Executa um turno do grafo (até `ask_human` ou END) em streaming.

    Chama `emit(event)` para enviar cada evento ao WebSocket. Também persiste
    em `analysis_messages`. Yielda o mesmo evento para o consumer.
    """
    graph = get_supervisor_graph()
    config: dict[str, Any] = {"configurable": {"thread_id": thread_id}}
    cb = get_langfuse_callback(session_id=thread_id, tags=["analyst", "supervisor-graph"])
    if cb is not None:
        config["callbacks"] = [cb]

    # Trace manual (independente da versão do langchain)
    lf_trace = start_trace(
        name="analyst.turn",
        session_id=thread_id,
        input={"message": user_message, "request_id": request_id},
        tags=["analyst", "supervisor-graph"],
        metadata={"request_payload": request_payload, "score": score_snapshot},
    )

    # Persiste a mensagem do analista
    _persist(db_session_id, role="analyst", content=user_message, event_type="user_message")
    await emit({"type": "analyst_message", "content": user_message})

    initial: dict[str, Any] = {
        "request_id": request_id,
        "session_id": thread_id,
        "request_payload": request_payload,
        "score_snapshot": score_snapshot,
        "user_message": user_message,
    }

    started_nodes: set[str] = set()
    try:
        async for event in graph.astream_events(initial, config=config, version="v2"):
            kind = event.get("event", "")
            name = event.get("name", "")

            if kind == "on_chain_start" and name in AGENT_NODES and name not in started_nodes:
                started_nodes.add(name)
                msg = {"type": "agent_started", "agent": name}
                await emit(msg)
                _persist(db_session_id, role="agent", agent_name=name,
                         content="", event_type="agent_started", metadata=msg)

            elif kind == "on_chat_model_stream":
                # Delta de LLM — identificamos o agente via tags/metadata
                metadata = event.get("metadata", {}) or {}
                agent = metadata.get("langgraph_node") or ""
                chunk = event.get("data", {}).get("chunk")
                if chunk is None:
                    continue
                text = getattr(chunk, "content", "")
                if isinstance(text, list):
                    text = "".join(
                        p.get("text", "") if isinstance(p, dict) else str(p) for p in text
                    )
                if text:
                    await emit({"type": "agent_delta", "agent": agent, "token": text})

            elif kind == "on_chain_end" and name in AGENT_NODES:
                data = event.get("data", {}).get("output") or {}
                # Captura o findings do nó
                for key, label in [
                    ("rag_findings", "rag_expert"),
                    ("regulation_findings", "regulation_expert"),
                    ("credit_findings", "credit_expert"),
                    ("viability_findings", "viability_expert"),
                    ("web_findings", "web_research_expert"),
                ]:
                    if key in data and name == label:
                        findings = data[key] or {}
                        msg = {
                            "type": "agent_result",
                            "agent": label,
                            "summary": findings.get("summary", ""),
                            "sources": findings.get("sources", []),
                        }
                        await emit(msg)
                        _persist(db_session_id, role="agent", agent_name=label,
                                 content=findings.get("summary", ""),
                                 event_type="agent_result",
                                 metadata={"sources": findings.get("sources", [])})

                if name == "compose_answer" and "supervisor_answer" in data:
                    answer = data.get("supervisor_answer", "") or ""
                    sources = data.get("sources", []) or []
                    msg = {"type": "supervisor_answer", "content": answer, "sources": sources}
                    await emit(msg)
                    _persist(db_session_id, role="supervisor", content=answer,
                             event_type="supervisor_answer", metadata={"sources": sources})
                    end_trace(lf_trace, output={"answer": answer, "sources": sources})

            yield event
    except Exception as e:
        logger.exception("Erro no grafo")
        msg = {"type": "error", "message": str(e)}
        await emit(msg)
        _persist(db_session_id, role="system", content=str(e), event_type="error")
        end_trace(lf_trace, output=str(e), level="ERROR", status_message=type(e).__name__)
        return

    # Checa se o grafo parou em `ask_human` (interrupt)
    state = graph.get_state(config)
    if state and state.next and "ask_human" in state.next:
        msg = {
            "type": "awaiting_human_decision",
            "question": "Aprovar ou reprovar esta solicitação?",
        }
        await emit(msg)
        _persist(db_session_id, role="system", content=msg["question"],
                 event_type="awaiting_human_decision")


async def resume_with_decision(
    *, db_session_id: int, thread_id: str, decision: str, rationale: str,
    emit: Callable[[dict[str, Any]], Awaitable[Any]],
) -> None:
    """Retoma o grafo com a decisão do analista (HITL)."""
    graph = get_supervisor_graph()
    config: dict[str, Any] = {"configurable": {"thread_id": thread_id}}
    cb = get_langfuse_callback(session_id=thread_id, tags=["analyst", "resume-decision"])
    if cb is not None:
        config["callbacks"] = [cb]
    _persist(db_session_id, role="human_decision",
             content=f"{decision}: {rationale}", event_type="human_decision",
             metadata={"decision": decision, "rationale": rationale})
    try:
        async for event in graph.astream_events(
            Command(resume={"decision": decision, "rationale": rationale}),
            config=config, version="v2",
        ):
            kind = event.get("event", "")
            name = event.get("name", "")
            if kind == "on_chain_end" and name == "apply_decision":
                await emit({
                    "type": "decision_applied",
                    "decision": decision,
                    "rationale": rationale,
                })
                _persist(db_session_id, role="system",
                         content=f"Decisão aplicada: {decision}",
                         event_type="decision_applied",
                         metadata={"decision": decision, "rationale": rationale})
    except Exception as e:
        logger.exception("resume falhou")
        await emit({"type": "error", "message": str(e)})
