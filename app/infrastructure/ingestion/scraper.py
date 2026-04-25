import asyncio
from typing import List
from dataclasses import dataclass

import httpx
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


async def _scrape_with_crawl4ai(url: str, bypass_cache: bool) -> _ScrapedContent:
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
        logger.warning(f"crawl4ai falhou em {url}: {result.error_message}")
        return _ScrapedContent(url=url, title="", markdown="", success=False)
    return _ScrapedContent(url=url, title=result.metadata.get("title", url),
                           markdown=result.markdown or "", success=True)


async def _scrape_with_httpx(url: str) -> _ScrapedContent:
    """Fallback estático via httpx + BeautifulSoup quando crawl4ai/Chromium não está disponível."""
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        logger.error("beautifulsoup4 não instalado — fallback indisponível")
        return _ScrapedContent(url=url, title="", markdown="", success=False)

    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; CashMeBot/1.0; +https://cashme.com.br)",
        "Accept": "text/html,application/xhtml+xml",
    }
    try:
        async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, headers=headers) as client:
            r = await client.get(url)
            r.raise_for_status()
    except Exception as e:
        logger.warning(f"httpx fallback falhou em {url}: {e}")
        return _ScrapedContent(url=url, title="", markdown="", success=False)

    soup = BeautifulSoup(r.text, "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "aside", "noscript"]):
        tag.decompose()
    title = (soup.title.string if soup.title and soup.title.string else url).strip()
    text = "\n".join(line.strip() for line in soup.get_text("\n").splitlines() if line.strip())
    if len(text) < 200:
        logger.warning(f"httpx fallback: conteúdo muito curto em {url} ({len(text)} chars)")
        return _ScrapedContent(url=url, title=title, markdown=text, success=bool(text))
    return _ScrapedContent(url=url, title=title, markdown=text, success=True)


async def _scrape_url(url: str, bypass_cache: bool = False) -> _ScrapedContent:
    """Tenta crawl4ai (com JS); se falhar (Chromium ausente/erro), cai pro httpx estático."""
    try:
        result = await _scrape_with_crawl4ai(url, bypass_cache)
        if result.success and result.markdown:
            return result
        logger.info(f"crawl4ai sem conteúdo útil em {url}; usando fallback httpx")
    except ImportError:
        logger.info(f"crawl4ai indisponível; usando fallback httpx para {url}")
    except Exception as e:
        logger.warning(f"crawl4ai exception em {url}: {e}; usando fallback httpx")
    return await _scrape_with_httpx(url)


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
