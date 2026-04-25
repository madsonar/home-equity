"""
OpenTelemetry + Langfuse — tracing de agentes e LLM calls.
Imports são lazy: o módulo carrega sem os pacotes instalados.
"""
from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from langfuse import Langfuse
    from opentelemetry.sdk.trace import TracerProvider

_langfuse: Optional["Langfuse"] = None
_tracer_provider: Optional["TracerProvider"] = None


def setup_telemetry(fastapi_app=None) -> Optional["Langfuse"]:
    global _langfuse, _tracer_provider

    try:
        from opentelemetry import trace
        from opentelemetry.sdk.trace import TracerProvider
        from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter

        _tracer_provider = TracerProvider()

        try:
            from app.config import settings
            if settings.otlp_endpoint:
                from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
                exporter = OTLPSpanExporter(endpoint=settings.otlp_endpoint)
            else:
                exporter = ConsoleSpanExporter()
        except Exception:
            exporter = ConsoleSpanExporter()

        _tracer_provider.add_span_processor(BatchSpanProcessor(exporter))
        trace.set_tracer_provider(_tracer_provider)

        if fastapi_app is not None:
            try:
                from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
                FastAPIInstrumentor.instrument_app(fastapi_app)
            except ImportError:
                pass
        logger.info("OpenTelemetry configurado")
    except ImportError:
        logger.info("opentelemetry-sdk não instalado — tracing OTEL desativado")

    try:
        from app.config import settings
        from langfuse import Langfuse
        if settings.langfuse_public_key and settings.langfuse_secret_key:
            _langfuse = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host,
            )
            logger.info(f"Langfuse tracing ativo — host: {settings.langfuse_host}")
    except (ImportError, Exception) as e:
        logger.info(f"Langfuse não configurado ({e})")

    return _langfuse


def get_tracer(name: str = "cashme"):
    try:
        from opentelemetry import trace
        return trace.get_tracer(name)
    except ImportError:
        return None


def get_langfuse() -> Optional["Langfuse"]:
    return _langfuse


def get_langfuse_callback(session_id: str = "", user_id: str = "", tags: Optional[list[str]] = None):
    """Retorna um CallbackHandler do Langfuse para LangChain/LangGraph.
    None se Langfuse não estiver configurado.

    Use:
        cb = get_langfuse_callback(session_id="abc", user_id="cliente1@cashme.local")
        cfg = {"callbacks": [cb]} if cb else {}
        agent.invoke({...}, config=cfg)
    """
    if get_langfuse() is None:
        return None
    try:
        from langfuse.callback import CallbackHandler
        return CallbackHandler(
            session_id=session_id or None,
            user_id=user_id or None,
            tags=tags or None,
        )
    except Exception as e:
        logger.debug(f"Langfuse callback indisponível: {e}")
        return None


def flush_langfuse() -> None:
    lf = get_langfuse()
    if lf is None:
        return
    try:
        lf.flush()
    except Exception:
        pass


def trace_llm_call(trace_name: str, input_text: str, output_text: str, model: str = "",
                   session_id: str = "", user_id: str = ""):
    lf = get_langfuse()
    if lf is None:
        return
    try:
        t = lf.trace(name=trace_name, session_id=session_id or None, user_id=user_id or None)
        t.generation(
            name="llm-generation",
            model=model,
            input=input_text,
            output=output_text,
        )
    except Exception as e:
        logger.debug(f"Langfuse trace falhou: {e}")
