from typing import Annotated
from datetime import datetime, timezone, timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger
from pydantic import BaseModel
from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from app.infrastructure.auth.security import hash_password, require_admin
from app.infrastructure.db.models import AnalysisSession, Role, SimulationRequest, User
from app.infrastructure.db.session import get_db


router = APIRouter(prefix="/admin", tags=["admin"])


class UserIn(BaseModel):
    email: str
    password: str
    full_name: str
    role: Role


class UserOut(BaseModel):
    id: int
    email: str
    full_name: str
    role: str
    created_at: str


@router.get("/users", response_model=list[UserOut])
def list_users(
    _: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    rows = db.query(User).order_by(desc(User.created_at)).all()
    return [UserOut(
        id=u.id, email=u.email, full_name=u.full_name,
        role=u.role.value, created_at=u.created_at.isoformat(),
    ) for u in rows]


@router.post("/users", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(
    data: UserIn,
    _: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    if db.query(User).filter(User.email == data.email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "E-mail já cadastrado")
    u = User(
        email=data.email, password_hash=hash_password(data.password),
        full_name=data.full_name, role=data.role,
    )
    db.add(u); db.commit(); db.refresh(u)
    return UserOut(
        id=u.id, email=u.email, full_name=u.full_name,
        role=u.role.value, created_at=u.created_at.isoformat(),
    )


@router.delete("/users/{uid}")
def delete_user(
    uid: int,
    me: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    if uid == me.id:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Não pode apagar a si mesmo")
    u = db.get(User, uid)
    if not u:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    db.delete(u); db.commit()
    return {"status": "ok"}


class MetricsOut(BaseModel):
    chunks_indexed: int | None = None
    avg_score_today: float | None = None
    active_sessions: int | None = None
    pending_simulations: int | None = None
    total_simulations: int | None = None


def _count_chunks() -> int | None:
    """Conta documentos no Chroma; retorna None se indisponível."""
    try:
        from app.config import settings
        import chromadb
        client = chromadb.HttpClient(host=settings.chroma_host, port=int(settings.chroma_port))
        total = 0
        for col in client.list_collections():
            try:
                total += col.count()
            except Exception:
                pass
        return total
    except Exception as e:
        logger.warning(f"chroma chunks count falhou: {e}")
        return None


def _count_active_sessions(db: Session) -> int:
    return db.query(func.count(AnalysisSession.id)).filter(AnalysisSession.closed_at.is_(None)).scalar() or 0


def _avg_score_today(db: Session) -> float | None:
    today = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
    rows = (db.query(SimulationRequest.score_snapshot)
              .filter(SimulationRequest.created_at >= today)
              .filter(SimulationRequest.score_snapshot.isnot(None))
              .all())
    scores: list[float] = []
    for (snap,) in rows:
        if isinstance(snap, dict) and isinstance(snap.get("score"), (int, float)):
            scores.append(float(snap["score"]))
    if not scores:
        return None
    return round(sum(scores) / len(scores), 3)


@router.get("/metrics", response_model=MetricsOut)
def admin_metrics(
    _: Annotated[User, Depends(require_admin)],
    db: Annotated[Session, Depends(get_db)],
):
    total = db.query(func.count(SimulationRequest.id)).scalar() or 0
    pending = db.query(func.count(SimulationRequest.id)).filter(
        SimulationRequest.status == "pending_analyst"
    ).scalar() or 0
    return MetricsOut(
        chunks_indexed=_count_chunks(),
        avg_score_today=_avg_score_today(db),
        active_sessions=_count_active_sessions(db),
        pending_simulations=pending,
        total_simulations=total,
    )
