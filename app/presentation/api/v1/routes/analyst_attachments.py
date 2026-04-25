"""Rota de upload de anexo para uma sessão de análise. Extrai texto e indexa
no FAISS efêmero da sessão."""
from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.infrastructure.auth.security import require_analyst
from app.infrastructure.db.models import AnalysisAttachment, AnalysisSession, User
from app.infrastructure.db.session import get_db
from app.infrastructure.ingestion.doc_parser import DoclingParser
from app.infrastructure.rag.ephemeral_faiss import get_ephemeral_manager


router = APIRouter(prefix="/analyst", tags=["analyst"])


class AttachmentOut(BaseModel):
    id: int
    filename: str
    chunks_indexed: int
    size_bytes: int


STORAGE_ROOT = Path("./data/analysis_attachments")


@router.post(
    "/sessions/{sess_id}/attachments",
    response_model=AttachmentOut, status_code=status.HTTP_201_CREATED,
)
def upload_attachment(
    sess_id: int,
    user: Annotated[User, Depends(require_analyst)],
    db: Annotated[Session, Depends(get_db)],
    file: Annotated[UploadFile, File(...)],
):
    sess = db.get(AnalysisSession, sess_id)
    if not sess:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    STORAGE_ROOT.mkdir(parents=True, exist_ok=True)
    safe_name = (file.filename or "anexo").replace("/", "_")
    path = STORAGE_ROOT / f"sess{sess_id}_{safe_name}"
    content = file.file.read()
    path.write_bytes(content)

    # Parse + index em FAISS efêmero
    try:
        chunks = DoclingParser().parse_bytes(content, safe_name)
    except Exception:
        chunks = []

    indexed = 0
    if chunks:
        # prefixa metadata com o filename para ficar claro nas citações
        for c in chunks:
            c.source = safe_name
        indexed = get_ephemeral_manager().add(sess.thread_id, chunks)

    att = AnalysisAttachment(
        session_id=sess_id, filename=safe_name,
        mime=file.content_type or "application/octet-stream",
        size_bytes=len(content), storage_path=str(path),
        chunks_indexed=indexed,
    )
    db.add(att); db.commit(); db.refresh(att)
    return AttachmentOut(
        id=att.id, filename=att.filename,
        chunks_indexed=att.chunks_indexed, size_bytes=att.size_bytes,
    )
