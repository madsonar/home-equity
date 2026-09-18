import time
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from loguru import logger

from app.infrastructure.observability.telemetry import get_tracer


class TracingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        tracer = get_tracer("cashme.http")
        span_name = f"{request.method} {request.url.path}"
        start = time.perf_counter()

        if tracer:
            with tracer.start_as_current_span(span_name) as span:
                span.set_attribute("http.method", request.method)
                span.set_attribute("http.url", str(request.url))
                response = await call_next(request)
                elapsed = (time.perf_counter() - start) * 1000
                span.set_attribute("http.status_code", response.status_code)
                span.set_attribute("http.duration_ms", round(elapsed, 2))
        else:
            response = await call_next(request)
            elapsed = (time.perf_counter() - start) * 1000

        logger.debug(f"{request.method} {request.url.path} → {response.status_code} ({elapsed:.1f}ms)")
        return response
