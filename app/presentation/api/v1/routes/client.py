from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy import desc
from sqlalchemy.orm import Session

from app.config import settings
from app.container import get_score_use_case
from app.application.credit.score_use_case import ScoreCreditUseCase
from app.domain.credit.entities import CreditFeatures
from app.infrastructure.auth.security import require_client
from app.infrastructure.db.models import (
    ClientNotification, SimulationRequest, SimulationStatus, User,
)
from app.infrastructure.db.session import get_db


router = APIRouter(prefix="/client", tags=["client"])


class SimulationSubmit(BaseModel):
    monthly_income: float = Field(..., gt=0)
    property_value: float = Field(..., gt=0)
    requested_amount: float = Field(..., gt=0)
    employment_years: float = 2.0
    age: int = 35
    has_other_debts: bool = False
    profession: str = ""
    loan_purpose: str = ""


class SimulationResponse(BaseModel):
    id: int
    status: str
    amount_requested: float
    score_snapshot: dict[str, Any] | None = None
    public_message: str | None = None
    created_at: str
    decided_at: str | None = None


class NotificationResponse(BaseModel):
    id: int
    title: str
    body: str
    request_id: int | None
    read: bool
    created_at: str


def _to_sim_response(s: SimulationRequest) -> SimulationResponse:
    return SimulationResponse(
        id=s.id, status=s.status.value, amount_requested=s.amount_requested,
        score_snapshot=s.score_snapshot, public_message=s.public_message,
        created_at=s.created_at.isoformat(),
        decided_at=s.decided_at.isoformat() if s.decided_at else None,
    )


@router.post("/simulations", response_model=SimulationResponse, status_code=status.HTTP_201_CREATED)
def create_simulation(
    payload: SimulationSubmit,
    user: Annotated[User, Depends(require_client)],
    db: Annotated[Session, Depends(get_db)],
    use_case: Annotated[ScoreCreditUseCase, Depends(get_score_use_case)],
):
    features = CreditFeatures(**payload.model_dump())
    score = use_case.execute(features)
    snapshot = {
        "score": score.score, "approved": score.approved, "ltv": score.ltv,
        "monthly_installment": score.monthly_installment,
        "risk_factors": score.risk_factors, "explanation": score.explanation,
    }
    requires_analyst = payload.requested_amount >= settings.simulation_analyst_threshold
    status_val = SimulationStatus.pending_analyst if requires_analyst else SimulationStatus.auto_approved

    sim = SimulationRequest(
        client_id=user.id,
        payload=payload.model_dump(),
        score_snapshot=snapshot,
        amount_requested=payload.requested_amount,
        requires_analyst=requires_analyst,
        status=status_val,
        public_message=(None if requires_analyst else score.explanation),
    )
    db.add(sim)
    db.commit()
    db.refresh(sim)

    if requires_analyst:
        db.add(ClientNotification(
            client_id=user.id, request_id=sim.id,
            title="Simulação em análise",
            body=f"Sua solicitação de R$ {payload.requested_amount:,.2f} está sendo analisada por nossa equipe de backoffice.",
        ))
        db.commit()
    return _to_sim_response(sim)


@router.get("/simulations", response_model=list[SimulationResponse])
def list_simulations(
    user: Annotated[User, Depends(require_client)],
    db: Annotated[Session, Depends(get_db)],
):
    rows = db.query(SimulationRequest).filter(SimulationRequest.client_id == user.id)\
        .order_by(desc(SimulationRequest.created_at)).all()
    return [_to_sim_response(s) for s in rows]


@router.get("/simulations/{sim_id}", response_model=SimulationResponse)
def get_simulation(
    sim_id: int,
    user: Annotated[User, Depends(require_client)],
    db: Annotated[Session, Depends(get_db)],
):
    sim = db.get(SimulationRequest, sim_id)
    if not sim or sim.client_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Simulação não encontrada")
    return _to_sim_response(sim)


@router.get("/notifications", response_model=list[NotificationResponse])
def list_notifications(
    user: Annotated[User, Depends(require_client)],
    db: Annotated[Session, Depends(get_db)],
):
    rows = db.query(ClientNotification).filter(ClientNotification.client_id == user.id)\
        .order_by(desc(ClientNotification.created_at)).all()
    return [NotificationResponse(
        id=n.id, title=n.title, body=n.body, request_id=n.request_id,
        read=n.read_at is not None, created_at=n.created_at.isoformat(),
    ) for n in rows]


@router.post("/notifications/{nid}/read")
def mark_read(
    nid: int,
    user: Annotated[User, Depends(require_client)],
    db: Annotated[Session, Depends(get_db)],
):
    from datetime import datetime, timezone
    n = db.get(ClientNotification, nid)
    if not n or n.client_id != user.id:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    n.read_at = datetime.now(timezone.utc)
    db.commit()
    return {"status": "ok"}
