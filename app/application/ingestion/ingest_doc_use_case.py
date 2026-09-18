from typing import Sequence
from app.domain.knowledge.ports import IDocumentParser, IVectorStore


class IngestDocUseCase:
    def __init__(self, parser: IDocumentParser, *stores: IVectorStore):
        self._parser = parser
        self._stores: Sequence[IVectorStore] = stores

    def execute(self, content: bytes, filename: str) -> int:
        chunks = self._parser.parse_bytes(content, filename)
        if not chunks:
            return 0
        for store in self._stores:
            store.add(chunks)
        return len(chunks)
