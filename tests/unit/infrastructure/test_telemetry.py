from app.infrastructure.observability.telemetry import get_langfuse, get_tracer


def test_get_langfuse_returns_none_when_not_configured():
    # Sem chaves configuradas, deve retornar None sem levantar exceção
    result = get_langfuse()
    assert result is None


def test_get_tracer_returns_none_or_tracer():
    # Sem opentelemetry instalado, retorna None; com ele, retorna tracer
    result = get_tracer("cashme.test")
    # Aceita tanto None (otel não instalado) quanto objeto tracer
    assert result is None or hasattr(result, "start_as_current_span")
