import uuid
from typing import Annotated, Any
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import asc, desc, or_
from sqlalchemy.orm import Session

from app.infrastructure.auth.security import require_analyst
from app.infrastructure.db.models import (
    AnalysisSession, AnalysisMessage, AnalysisAttachment,
    SimulationRequest, SimulationStatus, User,
)
from app.infrastructure.db.session import get_db


router = APIRouter(prefix="/analyst", tags=["analyst"])


class QueueItem(BaseModel):
    id: int
    amount_requested: float
    status: str
    client_name: str
    client_email: str
    score_snapshot: dict[str, Any] | None
    created_at: str
    assigned_analyst_id: int | None


class SessionInfo(BaseModel):
    id: int
    request_id: int
    thread_id: str
    analyst_id: int
    opened_at: str
    closed_at: str | None


class SessionDetail(BaseModel):
    session: SessionInfo
    request: dict[str, Any]
    client: dict[str, Any]
    messages: list[dict[str, Any]]
    attachments: list[dict[str, Any]]


@router.get("/queue", response_model=list[QueueItem])
def list_queue(
    user: Annotated[User, Depends(require_analyst)],
    db: Annotated[Session, Depends(get_db)],
    status_filter: str = "pending_analyst",
):
    q = db.query(SimulationRequest)
    if status_filter == "pending_analyst":
        q = q.filter(SimulationRequest.status == SimulationStatus.pending_analyst)
    elif status_filter == "mine":
        q = q.filter(
            SimulationRequest.assigned_analyst_id == user.id,
            SimulationRequest.status == SimulationStatus.in_analysis,
        )
    elif status_filter == "all_open":
        q = q.filter(or_(
            SimulationRequest.status == SimulationStatus.pending_analyst,
            SimulationRequest.status == SimulationStatus.in_analysis,
        ))
    rows = q.order_by(asc(SimulationRequest.created_at)).all()
    out: list[QueueItem] = []
    for s in rows:
        c = db.get(User, s.client_id)
        out.append(QueueItem(
            id=s.id, amount_requested=s.amount_requested, status=s.status.value,
            client_name=(c.full_name if c else ""), client_email=(c.email if c else ""),
            score_snapshot=s.score_snapshot, created_at=s.created_at.isoformat(),
            assigned_analyst_id=s.assigned_analyst_id,
        ))
    return out


@router.post("/queue/{req_id}/claim", response_model=SessionInfo)
def claim(
    req_id: int,
    user: Annotated[User, Depends(require_analyst)],
    db: Annotated[Session, Depends(get_db)],
):
    """Atribui a simulação ao analista e abre a sessão de análise (ou retorna existente)."""
    sim = db.get(SimulationRequest, req_id)
    if not sim:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Solicitação não encontrada")
    if sim.status not in (SimulationStatus.pending_analyst, SimulationStatus.in_analysis):
        raise HTTPException(status.HTTP_409_CONFLICT, f"Status inválido: {sim.status.value}")
    if sim.assigned_analyst_id and sim.assigned_analyst_id != user.id:
        raise HTTPException(status.HTTP_409_CONFLICT, "Já atribuída a outro analista")

    sim.assigned_analyst_id = user.id
    sim.status = SimulationStatus.in_analysis

    sess = db.query(AnalysisSession).filter(AnalysisSession.request_id == req_id).first()
    if not sess:
        sess = AnalysisSession(
            request_id=req_id, analyst_id=user.id,
            thread_id=f"req-{req_id}-{uuid.uuid4().hex[:8]}",
        )
        db.add(sess)
    db.commit()
    db.refresh(sess)
    return SessionInfo(
        id=sess.id, request_id=sess.request_id, thread_id=sess.thread_id,
        analyst_id=sess.analyst_id, opened_at=sess.opened_at.isoformat(),
        closed_at=sess.closed_at.isoformat() if sess.closed_at else None,
    )


@router.get("/sessions/{sess_id}", response_model=SessionDetail)
def get_session(
    sess_id: int,
    user: Annotated[User, Depends(require_analyst)],
    db: Annotated[Session, Depends(get_db)],
):
    sess = db.get(AnalysisSession, sess_id)
    if not sess:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    sim = db.get(SimulationRequest, sess.request_id)
    client = db.get(User, sim.client_id) if sim else None
    msgs = db.query(AnalysisMessage).filter(AnalysisMessage.session_id == sess_id)\
        .order_by(asc(AnalysisMessage.created_at)).all()
    atts = db.query(AnalysisAttachment).filter(AnalysisAttachment.session_id == sess_id)\
        .order_by(asc(AnalysisAttachment.created_at)).all()
    return SessionDetail(
        session=SessionInfo(
            id=sess.id, request_id=sess.request_id, thread_id=sess.thread_id,
            analyst_id=sess.analyst_id, opened_at=sess.opened_at.isoformat(),
            closed_at=sess.closed_at.isoformat() if sess.closed_at else None,
        ),
        request={
            "id": sim.id, "status": sim.status.value,
            "amount_requested": sim.amount_requested,
            "payload": sim.payload, "score_snapshot": sim.score_snapshot,
            "created_at": sim.created_at.isoformat(),
        } if sim else {},
        client={
            "id": client.id, "name": client.full_name, "email": client.email,
        } if client else {},
        messages=[{
            "id": m.id, "role": m.role, "agent_name": m.agent_name,
            "content": m.content, "event_type": m.event_type,
            "metadata": m.msg_metadata or {}, "created_at": m.created_at.isoformat(),
        } for m in msgs],
        attachments=[{
            "id": a.id, "filename": a.filename, "mime": a.mime,
            "size_bytes": a.size_bytes, "chunks_indexed": a.chunks_indexed,
            "created_at": a.created_at.isoformat(),
        } for a in atts],
    )
