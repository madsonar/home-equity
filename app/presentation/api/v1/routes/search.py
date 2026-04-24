from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel

from app.container import get_search_use_case
from app.application.search.search_use_case import SearchUseCase
from app.infrastructure.observability.metrics import rag_queries_total

router = APIRouter(prefix="/search", tags=["search"])


class SearchResult(BaseModel):
    content: str
    source: str
    score: float


@router.get("", response_model=List[SearchResult])
async def search(q: str, k: int = 4, use_case: SearchUseCase = Depends(get_search_use_case)):
    if not q:
        raise HTTPException(status_code=400, detail="Parâmetro 'q' é obrigatório")
    rag_queries_total.labels(store="chroma").inc()
    results = use_case.execute(q, k=k)
    return [
        SearchResult(content=chunk.content, source=chunk.source, score=round(float(score), 4))
        for chunk, score in results
    ]
