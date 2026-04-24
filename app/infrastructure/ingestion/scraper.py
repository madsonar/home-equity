import asyncio
from typing import List
from dataclasses import dataclass

from langchain_text_splitters import RecursiveCharacterTextSplitter
from loguru import logger

from app.domain.knowledge.entities import KnowledgeChunk
from app.domain.knowledge.ports import IWebScraper


@dataclass
class _ScrapedContent:
    url: str
    title: str
    markdown: str
    success: bool


def _get_crawler_classes():
    try:
        from crawl4ai import AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
        return AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode
    except ImportError as e:
        raise ImportError("crawl4ai não instalado. Execute: pip install crawl4ai && crawl4ai-setup") from e


async def _scrape_url(url: str, bypass_cache: bool = False) -> _ScrapedContent:
    AsyncWebCrawler, BrowserConfig, CrawlerRunConfig, CacheMode = _get_crawler_classes()
    browser_config = BrowserConfig(headless=True, verbose=False)
    run_config = CrawlerRunConfig(
        cache_mode=CacheMode.BYPASS if bypass_cache else CacheMode.ENABLED,
        word_count_threshold=50,
        excluded_tags=["nav", "footer", "aside"],
        remove_overlay_elements=True,
    )
    async with AsyncWebCrawler(config=browser_config) as crawler:
        result = await crawler.arun(url=url, config=run_config)
    if not result.success:
        logger.warning(f"Falha ao scraping de {url}: {result.error_message}")
        return _ScrapedContent(url=url, title="", markdown="", success=False)
    return _ScrapedContent(url=url, title=result.metadata.get("title", url),
                           markdown=result.markdown or "", success=True)


def _to_chunks(scraped: _ScrapedContent, chunk_size: int = 1000, chunk_overlap: int = 200) -> List[KnowledgeChunk]:
    if not scraped.success or not scraped.markdown:
        return []
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return [
        KnowledgeChunk(content=chunk, source=scraped.url,
                       metadata={"title": scraped.title, "type": "web"})
        for chunk in splitter.split_text(scraped.markdown)
    ]


class Crawl4AIWebScraper(IWebScraper):
    async def scrape(self, url: str, bypass_cache: bool = False) -> List[KnowledgeChunk]:
        scraped = await _scrape_url(url, bypass_cache=bypass_cache)
        return _to_chunks(scraped)
