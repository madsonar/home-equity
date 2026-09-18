"""Script de teste de todos os módulos."""
import os
import sys
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.makedirs("./data", exist_ok=True)


def ok(msg):
    print(f"  ✓ {msg}")


def fail(msg, err):
    print(f"  ✗ {msg}: {err}")
    sys.exit(1)


print("=== Módulos principais ===")
try:
    from app.config import settings
    ok("config")
except Exception as e:
    fail("config", e)

try:
    from app.llm.providers import get_langchain_llm
    ok("llm/providers")
except Exception as e:
    fail("llm/providers", e)

try:
    from app.rag.chroma_store import get_chroma_vectorstore, search_chroma
    ok("rag/chroma_store")
except Exception as e:
    fail("rag/chroma_store", e)

try:
    from app.rag.faiss_store import build_faiss_index_from_vectors
    idx = build_faiss_index_from_vectors(np.random.rand(5, 64).astype("float32"))
    ok(f"rag/faiss_store — index com {idx.ntotal} vetores")
except Exception as e:
    fail("rag/faiss_store", e)

try:
    from app.rag.llama_rag import get_llama_index
    ok("rag/llama_rag")
except Exception as e:
    fail("rag/llama_rag", e)

try:
    from app.ingestion.scraper import scrape_url, scraped_to_documents
    ok("ingestion/scraper (lazy)")
except Exception as e:
    fail("ingestion/scraper", e)

try:
    from app.ingestion.doc_parser import parse_directory, markdown_to_documents
    docs = markdown_to_documents("# Teste\nConteúdo de crédito.", source="test")
    ok(f"ingestion/doc_parser — {len(docs)} chunks")
except Exception as e:
    fail("ingestion/doc_parser", e)

try:
    from app.memory.conversation import get_short_term_memory
    mem = get_short_term_memory("test")
    mem.save_context({"input": "oi"}, {"output": "olá"})
    ok(f"memory — {len(mem.chat_memory.messages)} mensagens")
except Exception as e:
    fail("memory", e)

try:
    from app.agents.langchain_agent import TOOLS, build_langchain_agent
    ok(f"agents/langchain — {len(TOOLS)} tools: {[t.name for t in TOOLS]}")
except Exception as e:
    fail("agents/langchain", e)

try:
    from app.agents.agno_agent import build_agno_agent
    ok("agents/agno")
except Exception as e:
    fail("agents/agno", e)

try:
    from app.api.routes import router
    ok(f"api/routes — {len(router.routes)} rotas")
except Exception as e:
    fail("api/routes", e)

try:
    from app.main import app
    ok(f"FastAPI app — '{app.title}'")
except Exception as e:
    fail("main", e)

print()
print("=== Credit scorer ===")
try:
    from app.ml.credit_scorer import CreditFeatures, predict_credit_score, train_model

    if not os.path.exists("./data/credit_model.pkl"):
        auc = train_model()
        print(f"  modelo treinado — AUC-ROC: {auc:.4f}")

    good = CreditFeatures(
        monthly_income=20000, property_value=800000, requested_amount=250000,
        employment_years=8, age=42, has_other_debts=False,
    )
    r = predict_credit_score(good)
    ok(f"perfil aprovado  — score={r.score:.0%}, approved={r.approved}, LTV={r.ltv:.0%}")
    assert r.approved, "Perfil bom deveria ser aprovado!"

    bad = CreditFeatures(
        monthly_income=3500, property_value=300000, requested_amount=270000,
        employment_years=0.3, age=20, has_other_debts=True,
    )
    r2 = predict_credit_score(bad)
    ok(f"perfil reprovado — score={r2.score:.0%}, approved={r2.approved}, risks={len(r2.risk_factors)}")
    assert not r2.approved, "Perfil ruim deveria ser reprovado!"

except Exception as e:
    fail("credit_scorer", e)

print()
print("=== parse_directory (knowledge_base) ===")
try:
    from app.ingestion.doc_parser import parse_directory
    docs_kb = parse_directory("./data/knowledge_base")
    ok(f"knowledge_base — {len(docs_kb)} chunks indexados")
except Exception as e:
    fail("parse_directory", e)

print()
print("Todos os testes passaram!")
