"""WebSocket para chat de análise com supervisor LangGraph.

Protocolo:
  C→S: {type:"user_message", content, thread_id?}
       {type:"human_decision", decision:"approved"|"rejected", rationale}
  S→C: agent_started, agent_delta, agent_result, supervisor_answer,
       awaiting_human_decision, decision_applied, error, analyst_message,
       history (enviado no connect).
"""
from __future__ import annotations

import json
from typing import Any

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, status
from loguru import logger
from sqlalchemy.orm import Session

from app.application.analysis.graph_runner import run_analyst_turn, resume_with_decision
from app.infrastructure.auth.security import decode_token
from app.infrastructure.db.models import (
    AnalysisMessage, AnalysisSession, Role, SimulationRequest, User,
)
from app.infrastructure.db.session import get_sessionmaker


router = APIRouter()


async def _send(ws: WebSocket, evt: dict[str, Any]) -> None:
    try:
        await ws.send_text(json.dumps(evt, ensure_ascii=False, default=str))
    except Exception as e:
        logger.warning(f"WS send failed: {e}")


def _load_session(db: Session, sess_id: int) -> tuple[AnalysisSession, SimulationRequest]:
    sess = db.get(AnalysisSession, sess_id)
    if not sess:
        raise ValueError("Sessão não encontrada")
    sim = db.get(SimulationRequest, sess.request_id)
    if not sim:
        raise ValueError("Solicitação não encontrada")
    return sess, sim


@router.websocket("/ws/analyst/sessions/{sess_id}")
async def analyst_session_ws(websocket: WebSocket, sess_id: int):
    # Auth via query string ?token=
    token = websocket.query_params.get("token")
    if not token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        payload = decode_token(token)
    except Exception:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    Session_ = get_sessionmaker()
    db: Session = Session_()
    try:
        user = db.get(User, int(payload["sub"]))
        if not user or user.role not in (Role.analista, Role.admin):
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            return
        try:
            sess, sim = _load_session(db, sess_id)
        except ValueError:
            await websocket.close(code=status.WS_1011_INTERNAL_ERROR)
            return

        await websocket.accept()

        # Envia histórico na conexão
        msgs = db.query(AnalysisMessage).filter(AnalysisMessage.session_id == sess_id)\
            .order_by(AnalysisMessage.created_at).all()
        await _send(websocket, {
            "type": "history",
            "messages": [{
                "role": m.role, "agent_name": m.agent_name,
                "content": m.content, "event_type": m.event_type,
                "metadata": m.msg_metadata or {},
                "created_at": m.created_at.isoformat(),
            } for m in msgs],
        })

        emit = lambda evt: _send(websocket, evt)

        while True:
            try:
                raw = await websocket.receive_text()
            except WebSocketDisconnect:
                return
            try:
                data = json.loads(raw)
            except Exception:
                await _send(websocket, {"type": "error", "message": "JSON inválido"})
                continue
            msg_type = data.get("type")

            if msg_type == "user_message":
                content = (data.get("content") or data.get("message") or "").strip()
                if not content:
                    await _send(websocket, {"type": "error", "message": "mensagem vazia"})
                    continue
                # Recarrega sim/sess (evita cache)
                db.expire_all()
                sess = db.get(AnalysisSession, sess_id)
                sim = db.get(SimulationRequest, sess.request_id)
                async for _ in run_analyst_turn(
                    db_session_id=sess_id, thread_id=sess.thread_id,
                    user_message=content,
                    request_payload=sim.payload or {},
                    request_id=sim.id,
                    score_snapshot=sim.score_snapshot,
                    emit=emit,
                ):
                    pass

            elif msg_type == "human_decision":
                decision = data.get("decision")
                rationale = (data.get("rationale") or "").strip()
                if decision not in ("approved", "rejected"):
                    await _send(websocket, {"type": "error", "message": "decision inválida"})
                    continue
                if not rationale:
                    rationale = f"Decisão manual do analista: {decision}."
                db.expire_all()
                sess = db.get(AnalysisSession, sess_id)
                await resume_with_decision(
                    db_session_id=sess_id, thread_id=sess.thread_id,
                    decision=decision, rationale=rationale, emit=emit,
                )

            else:
                await _send(websocket, {"type": "error", "message": f"type desconhecido: {msg_type}"})
    finally:
        db.close()
