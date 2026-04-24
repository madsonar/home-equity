"""
Métricas Prometheus customizadas da aplicação CashMe.
Importadas pelos route handlers para rastrear eventos de negócio.
"""
from prometheus_client import Counter, Histogram

credit_score_total = Counter(
    "cashme_credit_score_total",
    "Total de requisições de credit scoring",
    ["result"],  # "approved" | "rejected"
)

agent_requests_total = Counter(
    "cashme_agent_requests_total",
    "Total de requisições ao agente conversacional",
    ["agent_type"],  # "langchain" | "agno"
)

rag_queries_total = Counter(
    "cashme_rag_queries_total",
    "Total de buscas semânticas realizadas",
    ["store"],  # "chroma" | "faiss"
)

ingest_chunks_total = Counter(
    "cashme_ingest_chunks_total",
    "Total de chunks indexados na base vetorial",
    ["source_type"],  # "url" | "document"
)

model_prediction_seconds = Histogram(
    "cashme_model_prediction_seconds",
    "Duração da inferência do modelo de credit scoring",
    buckets=[0.001, 0.005, 0.01, 0.025, 0.05, 0.1, 0.25, 0.5, 1.0],
)
