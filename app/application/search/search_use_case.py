from typing import List
from app.domain.knowledge.entities import KnowledgeChunk
from app.domain.knowledge.ports import IVectorStore


class SearchUseCase:
    def __init__(self, store: IVectorStore):
        self._store = store

    def execute(self, query: str, k: int = 4) -> List[tuple[KnowledgeChunk, float]]:
        return self._store.search_with_score(query, k=k)
