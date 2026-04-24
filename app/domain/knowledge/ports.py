from abc import ABC, abstractmethod
from typing import List
from .entities import KnowledgeChunk


class IVectorStore(ABC):
    @abstractmethod
    def add(self, chunks: List[KnowledgeChunk]) -> int: ...

    @abstractmethod
    def search(self, query: str, k: int = 4) -> List[KnowledgeChunk]: ...

    @abstractmethod
    def search_with_score(self, query: str, k: int = 4) -> List[tuple[KnowledgeChunk, float]]: ...


class IDocumentParser(ABC):
    @abstractmethod
    def parse_bytes(self, content: bytes, filename: str) -> List[KnowledgeChunk]: ...

    @abstractmethod
    def parse_directory(self, path: str) -> List[KnowledgeChunk]: ...


class IWebScraper(ABC):
    @abstractmethod
    async def scrape(self, url: str, bypass_cache: bool = False) -> List[KnowledgeChunk]: ...
