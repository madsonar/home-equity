"""
OpenTelemetry + Langfuse — tracing de agentes e LLM calls.

Langfuse v3 adota OTEL por baixo dos panos. A integração LangChain/LangGraph
emite spans hierárquicos automaticamente: cada nó do StateGraph vira um span
filho e o Langfuse exibe o grafo conceitual no "Agent Graph view" do trace.

Imports são lazy: o módulo carrega sem os pacotes instalados.
"""
from __future__ import annotations
import contextlib
from typing import Any, Optional, TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from langfuse import Langfuse
    from opentelemetry.sdk.trace import TracerProvider

_langfuse: Optional["Langfuse"] = None
_tracer_provider: Optional["TracerProvider"] = None
_langfuse_v3: bool = False  # True quando langfuse>=3.x está em uso


def setup_telemetry(fastapi_app=None) -> Optional["Langfuse"]:
    global _langfuse, _tracer_provider, _langfuse_v3

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
        from langfuse import Langfuse  # type: ignore
        if settings.langfuse_public_key and settings.langfuse_secret_key:
            # v3 + v2 compartilham a mesma assinatura de construtor para
            # public_key/secret_key/host. Em v3 a instância é singleton e
            # acessível depois via `get_client()`.
            _langfuse = Langfuse(
                public_key=settings.langfuse_public_key,
                secret_key=settings.langfuse_secret_key,
                host=settings.langfuse_host,
            )
            try:
                from importlib.metadata import version as _pkg_version
                _v = _pkg_version("langfuse")
                _langfuse_v3 = int(_v.split(".")[0]) >= 3
            except Exception:
                _langfuse_v3 = False
            logger.info(
                f"Langfuse {'v3' if _langfuse_v3 else 'v2'} ativo — host: {settings.langfuse_host}"
            )
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


def get_langfuse_callback(session_id: str = "", user_id: str = "",
                           tags: Optional[list[str]] = None):
    """Retorna um CallbackHandler do Langfuse para LangChain/LangGraph.

    Em v3 o handler não aceita session/user/tags no construtor — eles devem
    ser passados via `metadata` na invocação do grafo. Use também
    `langfuse_metadata()` para montar o dict pronto.
    """
    if get_langfuse() is None:
        return None

    if _langfuse_v3:
        try:
            from langfuse.langchain import CallbackHandler  # type: ignore
            return CallbackHandler()
        except Exception as e:
            logger.debug(f"Langfuse v3 callback indisponível: {e}")
            return None

    # v2 (legacy) — aceita kwargs no construtor
    try:
        from langfuse.callback import CallbackHandler  # type: ignore
        return CallbackHandler(
            session_id=session_id or None,
            user_id=user_id or None,
            tags=tags or None,
        )
    except Exception as e:
        logger.debug(f"Langfuse v2 callback indisponível: {e}")
        return None


def langfuse_metadata(session_id: str = "", user_id: str = "",
                      tags: Optional[list[str]] = None,
                      extra: Optional[dict] = None) -> dict:
    """Monta o dict de `metadata` esperado pelo Langfuse v3 ao invocar
    LangChain/LangGraph. Em v2 esses campos são ignorados pelo handler
    (que recebe os mesmos via construtor)."""
    md: dict[str, Any] = {}
    if session_id:
        md["langfuse_session_id"] = session_id
    if user_id:
        md["langfuse_user_id"] = user_id
    if tags:
        md["langfuse_tags"] = list(tags)
    if extra:
        md.update(extra)
    return md


@contextlib.contextmanager
def langfuse_span(name: str, *, session_id: str = "", user_id: str = "",
                  tags: Optional[list[str]] = None,
                  input: Any = None, metadata: Optional[dict] = None):
    """Context manager que cria um span raiz no Langfuse v3, agrupando
    todo o trabalho dentro dele (incluindo o grafo LangGraph cujos nós
    se aninham automaticamente). Faz no-op se Langfuse não estiver ativo
    ou em v2.
    """
    lf = get_langfuse()
    if lf is None or not _langfuse_v3:
        yield None
        return
    try:
        # v3 API: start_as_current_observation(as_type="span", ...)
        cm = lf.start_as_current_observation(
            as_type="span",
            name=name,
            input=input,
            metadata=metadata or None,
        )
    except Exception as e:
        logger.debug(f"langfuse_span fallback: {e}")
        yield None
        return

    with cm as span:
        # Propaga session/user/tags para o trace todo
        try:
            from langfuse import propagate_attributes  # type: ignore
            with propagate_attributes(
                session_id=session_id or None,
                user_id=user_id or None,
                tags=tags or None,
            ):
                yield span
        except Exception:
            yield span


def start_trace(name: str, *, session_id: str = "", user_id: str = "",
                input: Any = None, tags: Optional[list[str]] = None,
                metadata: Optional[dict] = None):
    """Cria um trace manual. Em v3 retorna um span raiz já iniciado
    (o caller deve chamar `end_trace` para fechar/atualizar). Em v2 retorna
    o objeto trace clássico. Retorna None se Langfuse não estiver ativo.
    """
    lf = get_langfuse()
    if lf is None:
        return None

    if _langfuse_v3:
        try:
            span = lf.start_span(name=name, input=input, metadata=metadata or None)
            # Propagar session/user/tags via update_trace
            try:
                span.update_trace(
                    session_id=session_id or None,
                    user_id=user_id or None,
                    tags=tags or None,
                    input=input,
                    metadata=metadata or None,
                )
            except Exception:
                pass
            return span
        except Exception as e:
            logger.debug(f"Langfuse v3 start_span falhou: {e}")
            return None

    try:
        return lf.trace(
            name=name,
            session_id=session_id or None,
            user_id=user_id or None,
            input=input,
            tags=tags or None,
            metadata=metadata or None,
        )
    except Exception as e:
        logger.debug(f"Langfuse start_trace falhou: {e}")
        return None


def end_trace(trace, *, output: Any = None, level: str = "DEFAULT",
              status_message: str = "") -> None:
    if trace is None:
        return
    try:
        if _langfuse_v3:
            # v3 — encerra o span e atualiza o trace I/O
            try:
                trace.update(output=output)
            except Exception:
                pass
            try:
                trace.update_trace(output=output)
            except Exception:
                pass
            try:
                trace.end()
            except Exception:
                pass
            return

        # v2
        trace.update(output=output)
        try:
            trace.generation(
                name="llm",
                input=None,
                output=output,
                level=level if level != "DEFAULT" else None,
                status_message=status_message or None,
            )
        except Exception:
            pass
    except Exception as e:
        logger.debug(f"Langfuse end_trace falhou: {e}")


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
        if _langfuse_v3:
            with lf.start_as_current_observation(
                as_type="generation",
                name=trace_name,
                model=model or None,
                input=input_text,
            ) as gen:
                gen.update(output=output_text)
                try:
                    gen.update_trace(
                        session_id=session_id or None,
                        user_id=user_id or None,
                    )
                except Exception:
                    pass
            return
        t = lf.trace(name=trace_name, session_id=session_id or None, user_id=user_id or None)
        t.generation(
            name="llm-generation",
            model=model,
            input=input_text,
            output=output_text,
        )
    except Exception as e:
        logger.debug(f"Langfuse trace falhou: {e}")
