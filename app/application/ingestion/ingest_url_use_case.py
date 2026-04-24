from typing import Sequence
from app.domain.knowledge.ports import IWebScraper, IVectorStore


class IngestURLUseCase:
    def __init__(self, scraper: IWebScraper, *stores: IVectorStore):
        self._scraper = scraper
        self._stores: Sequence[IVectorStore] = stores

    async def execute(self, url: str, bypass_cache: bool = False) -> int:
        chunks = await self._scraper.scrape(url, bypass_cache=bypass_cache)
        if not chunks:
            return 0
        for store in self._stores:
            store.add(chunks)
        return len(chunks)
