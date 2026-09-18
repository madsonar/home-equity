from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from pydantic import BaseModel

from app.container import get_ingest_url_use_case, get_ingest_doc_use_case
from app.application.ingestion.ingest_url_use_case import IngestURLUseCase
from app.application.ingestion.ingest_doc_use_case import IngestDocUseCase
from app.infrastructure.observability.metrics import ingest_chunks_total

router = APIRouter(prefix="/ingest", tags=["ingestion"])


class IngestURLRequest(BaseModel):
    url: str
    bypass_cache: bool = False


class IngestResponse(BaseModel):
    chunks_added: int
    source: str
    message: str


@router.post("/url", response_model=IngestResponse)
async def ingest_url(
    req: IngestURLRequest,
    use_case: IngestURLUseCase = Depends(get_ingest_url_use_case),
):
    try:
        count = await use_case.execute(req.url, bypass_cache=req.bypass_cache)
    except ImportError as e:
        raise HTTPException(status_code=503, detail=str(e))
    if count == 0:
        raise HTTPException(status_code=422, detail=f"Nenhum conteúdo extraído de {req.url}")
    ingest_chunks_total.labels(source_type="url").inc(count)
    return IngestResponse(chunks_added=count, source=req.url,
                          message=f"{count} chunks indexados com sucesso")


@router.post("/doc", response_model=IngestResponse)
async def ingest_document(
    file: UploadFile = File(...),
    use_case: IngestDocUseCase = Depends(get_ingest_doc_use_case),
):
    if not file.filename:
        raise HTTPException(status_code=400, detail="Arquivo sem nome")
    content = await file.read()
    try:
        count = use_case.execute(content, file.filename)
    except ImportError as e:
        raise HTTPException(status_code=503, detail=str(e))
    if count == 0:
        raise HTTPException(status_code=422, detail="Nenhum conteúdo extraído do documento")
    ingest_chunks_total.labels(source_type="document").inc(count)
    return IngestResponse(chunks_added=count, source=file.filename,
                          message=f"{count} chunks indexados de '{file.filename}'")
