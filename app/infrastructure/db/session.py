"""Engine + sessionmaker síncrono (psycopg3). Usado pelo FastAPI via Depends."""
from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.config import settings


_engine: Engine | None = None
_SessionLocal: sessionmaker[Session] | None = None


def get_engine() -> Engine:
    global _engine
    if _engine is None:
        _engine = create_engine(
            settings.postgres_dsn,
            pool_pre_ping=True,
            pool_size=10,
            max_overflow=20,
            future=True,
        )
    return _engine


def get_sessionmaker() -> sessionmaker[Session]:
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(
            bind=get_engine(), autocommit=False, autoflush=False, expire_on_commit=False, future=True,
        )
    return _SessionLocal


def get_db() -> Iterator[Session]:
    """FastAPI Depends factory."""
    Session_ = get_sessionmaker()
    db = Session_()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def session_scope() -> Iterator[Session]:
    """Para scripts / seed / dentro do grafo LangGraph."""
    Session_ = get_sessionmaker()
    db = Session_()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Cria tabelas no startup (POC — Alembic opcional no futuro)."""
    from app.infrastructure.db import models  # noqa: F401 — importa para registrar no Base
    models.Base.metadata.create_all(bind=get_engine())
