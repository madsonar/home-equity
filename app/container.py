"""
Dependency injection container — wiring entre application e infrastructure.
Toda escolha de provider/backend vem da factory
(`app.infrastructure.llm.providers`), que por sua vez lê do `.env`.
"""
from functools import lru_cache

from app.infrastructure.llm.providers import (
    get_agent_runner,
    get_vector_store,
)
from app.infrastructure.rag.chroma_store import ChromaVectorStore
from app.infrastructure.rag.faiss_store import FAISSVectorStore
from app.infrastructure.ml.credit_scorer import SklearnCreditScorer
from app.infrastructure.ingestion.scraper import Crawl4AIWebScraper
from app.infrastructure.ingestion.doc_parser import DoclingParser
from app.application.credit.score_use_case import ScoreCreditUseCase
from app.application.credit.finetune_use_case import FinetuneScorerUseCase
from app.application.chat.chat_use_case import ChatUseCase
from app.application.ingestion.ingest_url_use_case import IngestURLUseCase
from app.application.ingestion.ingest_doc_use_case import IngestDocUseCase
from app.application.search.search_use_case import SearchUseCase


# ── Singletons ──────────────────────────────────────────────────────────────
@lru_cache(maxsize=1)
def _chroma() -> ChromaVectorStore:
    return ChromaVectorStore()


@lru_cache(maxsize=1)
def _faiss() -> FAISSVectorStore:
    return FAISSVectorStore()


@lru_cache(maxsize=1)
def _scorer() -> SklearnCreditScorer:
    return SklearnCreditScorer()


# ── FastAPI Depends factories ───────────────────────────────────────────────

def get_score_use_case() -> ScoreCreditUseCase:
    return ScoreCreditUseCase(scorer=_scorer())


def get_finetune_use_case() -> FinetuneScorerUseCase:
    from app.infrastructure.data.snowflake import get_snowflake_repo
    return FinetuneScorerUseCase(scorer=_scorer(), snowflake_repo=get_snowflake_repo())


def get_chat_use_case() -> ChatUseCase:
    # Ambos runners disponíveis; escolha default vem de settings.default_agent
    return ChatUseCase(
        langchain_runner=get_agent_runner("langchain"),
        agno_runner=get_agent_runner("agno"),
    )


def get_ingest_url_use_case() -> IngestURLUseCase:
    return IngestURLUseCase(Crawl4AIWebScraper(), _chroma(), _faiss())


def get_ingest_doc_use_case() -> IngestDocUseCase:
    return IngestDocUseCase(DoclingParser(), _chroma(), _faiss())


def get_search_use_case() -> SearchUseCase:
    # Vector store ativo vem do .env (VECTOR_STORE_BACKEND)
    return SearchUseCase(get_vector_store())
