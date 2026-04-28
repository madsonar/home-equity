"""
Equity Credit Intelligence Agent — FastAPI entrypoint (Clean Architecture v2).
"""
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger

from app.config import settings
from app.presentation.api.v1.router import api_router
from app.presentation.webhooks.whatsapp import webhook_router
from app.presentation.middleware.tracing import TracingMiddleware
from app.presentation.ws.analyst_ws import router as analyst_ws_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando Equity Credit Intelligence Agent v2...")

    for path in [settings.knowledge_base_path, settings.chroma_persist_path,
                 settings.faiss_index_path, "./data"]:
        os.makedirs(path, exist_ok=True)

    # Inicializa schema relacional (Postgres) — tabelas usadas pela
    # área do cliente/analista/admin.
    try:
        from app.infrastructure.db.session import init_db
        init_db()
        logger.info("Schema relacional (Postgres) pronto.")
    except Exception as e:
        logger.warning(f"Erro ao inicializar Postgres: {e}")

    # Treina modelo se não existir
    if not os.path.exists(settings.credit_model_path):
        from app.container import _scorer
        scorer = _scorer()
        auc = scorer.train()
        logger.info(f"Modelo treinado. AUC-ROC: {auc:.4f}")

    # Indexa knowledge base
    kb_path = settings.knowledge_base_path
    if os.path.exists(kb_path) and os.listdir(kb_path):
        from app.infrastructure.ingestion.doc_parser import DoclingParser
        from app.container import _chroma
        try:
            chunks = DoclingParser().parse_directory(kb_path)
            if chunks:
                _chroma().add(chunks)
                logger.info(f"Knowledge base indexada: {len(chunks)} chunks")
        except Exception as e:
            logger.warning(f"Erro ao indexar knowledge base: {e}")

    logger.info("Aplicação pronta. Acesse /docs para a documentação interativa.")
    yield
    logger.info("Encerrando aplicação...")
    try:
        from app.infrastructure.observability.telemetry import flush_langfuse
        flush_langfuse()
    except Exception:
        pass


app = FastAPI(
    title="Equity Credit Intelligence Agent",
    description=(
        "Agente conversacional de análise de crédito imobiliário (Home Equity). "
        "Combina RAG, múltiplos LLMs, web scraping, ML e Clean Architecture."
    ),
    version="2.0.0",
    lifespan=lifespan,
)

# ── Prometheus metrics endpoint (/metrics) ──────────────────────────────────
try:
    from prometheus_fastapi_instrumentator import Instrumentator
    Instrumentator(
        should_group_status_codes=True,
        should_ignore_untemplated=True,
        should_instrument_requests_inprogress=True,
        excluded_handlers=["/metrics", "/docs", "/redoc", "/openapi.json", "/favicon.ico"],
    ).instrument(app).expose(app, include_in_schema=False, tags=["monitoring"])
    logger.info("Prometheus metrics expostos em /metrics")
except ImportError:
    logger.info("prometheus-fastapi-instrumentator não instalado — /metrics indisponível")

# ── Telemetry (lazy — não quebra se pacotes opcionais não instalados) ────────
from app.infrastructure.observability.telemetry import setup_telemetry
setup_telemetry(app)

# ── Middleware ───────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(TracingMiddleware)

# ── Routes ───────────────────────────────────────────────────────────────────
app.include_router(api_router, prefix="/api/v1")
app.include_router(webhook_router)
app.include_router(analyst_ws_router)


@app.get("/", include_in_schema=False)
async def root():
    return {
        "name": "Equity Credit Intelligence Agent",
        "version": "2.0.0",
        "docs": "/docs",
        "ui": "/ui",
        "metrics": "/metrics",
        "health": "/api/v1/health",
        "endpoints": {
            "chat": "POST /api/v1/chat",
            "score": "POST /api/v1/score",
            "retrain": "POST /api/v1/score/retrain",
            "ingest_url": "POST /api/v1/ingest/url",
            "ingest_doc": "POST /api/v1/ingest/doc",
            "search": "GET /api/v1/search?q=...",
            "whatsapp": "POST /webhooks/whatsapp",
        },
    }


# ── SPA (React) ──────────────────────────────────────────────────────────────
# Montado por último para que /api/* e /docs tenham prioridade.
_web_dist = Path(__file__).parent / "presentation" / "web" / "dist"
if _web_dist.exists():
    from fastapi.responses import FileResponse

    # Assets versionados (JS/CSS/imagens) ficam abaixo de /ui/assets
    _assets_dir = _web_dist / "assets"
    if _assets_dir.exists():
        app.mount(
            "/ui/assets",
            StaticFiles(directory=_assets_dir),
            name="web-assets",
        )

    # Qualquer outro caminho dentro de /ui devolve um arquivo estático se existir,
    # senão devolve o index.html para que o React Router controle a rota.
    @app.get("/ui", include_in_schema=False)
    @app.get("/ui/", include_in_schema=False)
    @app.get("/ui/{full_path:path}", include_in_schema=False)
    async def spa_handler(full_path: str = ""):  # noqa: D401
        target = (_web_dist / full_path).resolve() if full_path else _web_dist / "index.html"
        # Bloqueia traversal para fora do dist
        try:
            target.relative_to(_web_dist.resolve())
        except ValueError:
            target = _web_dist / "index.html"
        if target.is_file():
            return FileResponse(target)
        return FileResponse(_web_dist / "index.html")

    logger.info(f"SPA montada em /ui a partir de {_web_dist}")
else:
    logger.warning(f"SPA não encontrada em {_web_dist} (rode `make web-build`)")
