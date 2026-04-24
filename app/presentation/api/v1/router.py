from fastapi import APIRouter
from .routes.health import router as health_router
from .routes.chat import router as chat_router
from .routes.credit import router as credit_router
from .routes.ingestion import router as ingestion_router
from .routes.search import router as search_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(chat_router)
api_router.include_router(credit_router)
api_router.include_router(ingestion_router)
api_router.include_router(search_router)
