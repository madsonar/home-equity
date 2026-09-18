"""Modelos SQLAlchemy 2.x para área de analista/cliente/admin."""
from __future__ import annotations

import enum
from datetime import datetime
from typing import Any

from sqlalchemy import (
    JSON, Boolean, DateTime, Enum, Float, ForeignKey, Integer, String, Text,
    func, Index,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Role(str, enum.Enum):
    cliente = "cliente"
    analista = "analista"
    admin = "admin"


class SimulationStatus(str, enum.Enum):
    auto_approved = "auto_approved"
    pending_analyst = "pending_analyst"
    in_analysis = "in_analysis"
    approved = "approved"
    rejected = "rejected"


class Decision(str, enum.Enum):
    approved = "approved"
    rejected = "rejected"


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[Role] = mapped_column(Enum(Role, name="role_enum"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class SimulationRequest(Base):
    __tablename__ = "simulation_requests"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    payload: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    score_snapshot: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    amount_requested: Mapped[float] = mapped_column(Float, nullable=False)
    requires_analyst: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    status: Mapped[SimulationStatus] = mapped_column(
        Enum(SimulationStatus, name="simulation_status_enum"),
        default=SimulationStatus.auto_approved, nullable=False, index=True,
    )
    assigned_analyst_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    decided_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    public_message: Mapped[str | None] = mapped_column(Text, nullable=True)

    client = relationship("User", foreign_keys=[client_id])
    analyst = relationship("User", foreign_keys=[assigned_analyst_id])
    sessions = relationship("AnalysisSession", back_populates="request", cascade="all, delete-orphan")


class AnalysisSession(Base):
    __tablename__ = "analysis_sessions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("simulation_requests.id"), nullable=False, index=True)
    analyst_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    thread_id: Mapped[str] = mapped_column(String(64), unique=True, nullable=False)
    opened_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    closed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    request = relationship("SimulationRequest", back_populates="sessions")
    messages = relationship("AnalysisMessage", back_populates="session", cascade="all, delete-orphan")
    attachments = relationship("AnalysisAttachment", back_populates="session", cascade="all, delete-orphan")


class AnalysisMessage(Base):
    __tablename__ = "analysis_messages"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("analysis_sessions.id"), nullable=False, index=True)
    role: Mapped[str] = mapped_column(String(32), nullable=False)  # analyst|supervisor|agent|system|human_decision
    agent_name: Mapped[str | None] = mapped_column(String(64), nullable=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    event_type: Mapped[str | None] = mapped_column(String(64), nullable=True)  # agent_started|agent_result|...
    msg_metadata: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)

    session = relationship("AnalysisSession", back_populates="messages")


class AnalysisAttachment(Base):
    __tablename__ = "analysis_attachments"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    session_id: Mapped[int] = mapped_column(ForeignKey("analysis_sessions.id"), nullable=False, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    mime: Mapped[str] = mapped_column(String(128), nullable=False)
    size_bytes: Mapped[int] = mapped_column(Integer, nullable=False)
    storage_path: Mapped[str] = mapped_column(String(512), nullable=False)
    chunks_indexed: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    session = relationship("AnalysisSession", back_populates="attachments")


class DecisionRecord(Base):
    __tablename__ = "decisions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    request_id: Mapped[int] = mapped_column(ForeignKey("simulation_requests.id"), nullable=False, index=True)
    analyst_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    decision: Mapped[Decision] = mapped_column(Enum(Decision, name="decision_enum"), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class ClientNotification(Base):
    __tablename__ = "client_notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    client_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    request_id: Mapped[int | None] = mapped_column(ForeignKey("simulation_requests.id"), nullable=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    read_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), index=True)


Index("ix_simreq_status_created", SimulationRequest.status, SimulationRequest.created_at)
