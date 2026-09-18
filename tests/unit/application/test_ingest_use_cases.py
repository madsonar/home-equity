import pytest
from unittest.mock import MagicMock, AsyncMock

from app.domain.knowledge.ports import IWebScraper, IDocumentParser, IVectorStore
from app.domain.knowledge.entities import KnowledgeChunk
from app.application.ingestion.ingest_url_use_case import IngestURLUseCase
from app.application.ingestion.ingest_doc_use_case import IngestDocUseCase


@pytest.mark.asyncio
async def test_ingest_url_adds_to_all_stores(sample_chunks):
    scraper = MagicMock(spec=IWebScraper)
    scraper.scrape = AsyncMock(return_value=sample_chunks)
    store1 = MagicMock(spec=IVectorStore)
    store2 = MagicMock(spec=IVectorStore)

    use_case = IngestURLUseCase(scraper, store1, store2)
    count = await use_case.execute("https://example.com")

    assert count == len(sample_chunks)
    store1.add.assert_called_once_with(sample_chunks)
    store2.add.assert_called_once_with(sample_chunks)


@pytest.mark.asyncio
async def test_ingest_url_returns_zero_on_empty(sample_chunks):
    scraper = MagicMock(spec=IWebScraper)
    scraper.scrape = AsyncMock(return_value=[])
    store = MagicMock(spec=IVectorStore)

    use_case = IngestURLUseCase(scraper, store)
    count = await use_case.execute("https://empty.com")

    assert count == 0
    store.add.assert_not_called()


def test_ingest_doc_adds_to_all_stores(sample_chunks):
    parser = MagicMock(spec=IDocumentParser)
    parser.parse_bytes.return_value = sample_chunks
    store1 = MagicMock(spec=IVectorStore)
    store2 = MagicMock(spec=IVectorStore)

    use_case = IngestDocUseCase(parser, store1, store2)
    count = use_case.execute(b"conteudo", "doc.pdf")

    assert count == len(sample_chunks)
    store1.add.assert_called_once()
    store2.add.assert_called_once()


def test_ingest_doc_returns_zero_on_empty():
    parser = MagicMock(spec=IDocumentParser)
    parser.parse_bytes.return_value = []
    store = MagicMock(spec=IVectorStore)

    use_case = IngestDocUseCase(parser, store)
    count = use_case.execute(b"", "empty.pdf")

    assert count == 0
    store.add.assert_not_called()
