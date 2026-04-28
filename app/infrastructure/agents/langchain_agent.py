from typing import Any
from langchain_core.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from app.domain.conversation.ports import IAgentRunner
from app.infrastructure.llm.providers import get_langchain_llm
from app.infrastructure.observability.telemetry import (
    get_langfuse_callback,
    langfuse_metadata,
    start_trace,
    end_trace,
)
from app.infrastructure.rag.chroma_store import ChromaVectorStore
from app.infrastructure.rag.faiss_store import FAISSVectorStore
from app.infrastructure.rag.llama_rag import query_llama


SYSTEM_PROMPT = """Você é o assistente de crédito imobiliário da Equity, a maior fintech de Home Equity do Brasil.

Seu objetivo é ajudar clientes a entender o crédito com garantia de imóvel, avaliar elegibilidade,
esclarecer dúvidas e orientar sobre o processo.

Regras:
- Seja preciso com números e taxas
- Sempre mencione os riscos quando relevante
- Nunca prometa aprovação de crédito — apenas analise o perfil
- Responda sempre em português brasileiro
- Use as ferramentas disponíveis para buscar informações antes de responder"""

_chroma = ChromaVectorStore()
_faiss = FAISSVectorStore()


@tool
def search_knowledge_base(query: str) -> str:
    """Busca na base de conhecimento de crédito imobiliário via ChromaDB.
    Use para responder perguntas sobre taxas, requisitos, documentação e políticas."""
    docs = _chroma.search(query, k=4)
    if not docs:
        return "Nenhuma informação encontrada na base de conhecimento."
    return "\n\n---\n\n".join(f"[{d.source}]\n{d.content}" for d in docs)


@tool
def search_faiss_index(query: str) -> str:
    """Busca rápida no índice FAISS para complementar a busca semântica."""
    docs = _faiss.search(query, k=3)
    if not docs:
        return "Nenhum resultado no índice FAISS."
    return "\n\n---\n\n".join(d.content for d in docs)


@tool
def query_llama_index(question: str) -> str:
    """Consulta a base de conhecimento via LlamaIndex para análise mais profunda."""
    try:
        return query_llama(question)
    except Exception as e:
        return f"Erro na consulta LlamaIndex: {str(e)}"


@tool
def calculate_ltv(property_value: float, requested_amount: float) -> str:
    """Calcula o LTV (Loan-to-Value) e verifica se está dentro dos limites da Equity.
    Args:
        property_value: valor do imóvel em R$
        requested_amount: valor solicitado em R$
    """
    ltv = requested_amount / property_value if property_value > 0 else 0
    max_ltv = 0.60
    result = f"LTV calculado: {ltv:.1%}\nLTV máximo Equity: {max_ltv:.0%}\n"
    result += "✓ Aprovado neste critério" if ltv <= max_ltv else "✗ Reprovado — LTV acima do limite"
    return result


TOOLS = [search_knowledge_base, search_faiss_index, query_llama_index, calculate_ltv]
_checkpointer = MemorySaver()


class LangchainAgentRunner(IAgentRunner):
    def run(self, message: str, session_id: str, **kwargs) -> dict[str, Any]:
        provider = kwargs.get("provider")
        model = kwargs.get("model")
        llm = get_langchain_llm(provider=provider, model=model)
        agent = create_react_agent(
            model=llm,
            tools=TOOLS,
            prompt=SystemMessage(content=SYSTEM_PROMPT),
            checkpointer=_checkpointer,
        )
        config: dict[str, Any] = {"configurable": {"thread_id": session_id}}
        user_id = str(kwargs.get("user_id") or kwargs.get("user") or "")
        cb = get_langfuse_callback(
            session_id=session_id,
            user_id=user_id,
            tags=["chat", "langchain"],
        )
        if cb is not None:
            config["callbacks"] = [cb]
        # Em Langfuse v3 session/user/tags vão via metadata da invocação.
        config["metadata"] = langfuse_metadata(
            session_id=session_id,
            user_id=user_id,
            tags=["chat", "langchain"],
            extra={"provider": provider, "model": model},
        )

        # Trace manual (funciona com qualquer versão do langchain)
        trace = start_trace(
            name="chat.langchain",
            session_id=session_id,
            user_id=user_id,
            input=message,
            tags=["chat", "langchain"],
            metadata={"provider": provider, "model": model},
        )

        try:
            result = agent.invoke({"messages": [HumanMessage(content=message)]}, config=config)
        except Exception as e:
            end_trace(trace, output=str(e), level="ERROR", status_message=type(e).__name__)
            raise
        raw = result["messages"][-1].content
        # Gemini/Anthropic podem retornar lista de partes multimodais; normaliza para str
        if isinstance(raw, list):
            response = "".join(
                part.get("text", "") if isinstance(part, dict) else str(part)
                for part in raw
            )
        else:
            response = str(raw)
        end_trace(trace, output=response)
        return {
            "response": response,
            "session_id": session_id,
            "agent": "langchain",
        }
