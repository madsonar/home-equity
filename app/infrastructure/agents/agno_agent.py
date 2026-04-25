from typing import Any

from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.models.google import Gemini
from agno.tools import tool

from app.config import settings
from app.domain.conversation.ports import IAgentRunner
from app.domain.credit.entities import CreditFeatures
from app.infrastructure.ml.credit_scorer import SklearnCreditScorer
from app.infrastructure.observability.telemetry import start_trace, end_trace
from app.infrastructure.rag.chroma_store import ChromaVectorStore

_chroma = ChromaVectorStore()
_scorer = SklearnCreditScorer()


@tool
def buscar_base_conhecimento(query: str) -> str:
    """Busca na base de conhecimento de crédito imobiliário.

    Args:
        query: pergunta ou termo a buscar

    Returns:
        Trechos relevantes da base de conhecimento
    """
    docs = _chroma.search(query, k=4)
    if not docs:
        return "Nenhuma informação encontrada."
    return "\n\n".join(f"• {d.content}" for d in docs)


@tool
def avaliar_perfil_credito(
    renda_mensal: float,
    valor_imovel: float,
    valor_solicitado: float,
    anos_emprego: float,
    idade: int,
    tem_outras_dividas: bool,
) -> str:
    """Avalia o perfil de crédito do cliente e retorna score de aprovação.

    Args:
        renda_mensal: renda mensal em R$
        valor_imovel: valor do imóvel dado como garantia em R$
        valor_solicitado: valor do crédito solicitado em R$
        anos_emprego: anos de vínculo empregatício
        idade: idade do solicitante
        tem_outras_dividas: se possui outras dívidas

    Returns:
        Análise detalhada do perfil de crédito
    """
    features = CreditFeatures(
        monthly_income=renda_mensal, property_value=valor_imovel,
        requested_amount=valor_solicitado, employment_years=anos_emprego,
        age=idade, has_other_debts=tem_outras_dividas,
    )
    result = _scorer.predict(features)
    status = "APROVADO" if result.approved else "REPROVADO"
    return (
        f"Resultado: {status}\nScore: {result.score:.0%}\nLTV: {result.ltv:.0%}\n"
        f"Parcela estimada (120x): R$ {result.monthly_installment:,.2f}\n{result.explanation}"
    )


class AgnoAgentRunner(IAgentRunner):
    def run(self, message: str, session_id: str, **kwargs) -> dict[str, Any]:
        provider = kwargs.get("provider") or settings.default_llm_provider
        if provider in ("google", "gemini"):
            model = Gemini(id=settings.default_llm_model, api_key=settings.google_api_key)
        else:
            model = OpenAIChat(id=settings.default_llm_model, api_key=settings.openai_api_key)

        agent = Agent(
            model=model,
            tools=[buscar_base_conhecimento, avaliar_perfil_credito],
            description="Assistente especializado em crédito com garantia de imóvel da CashMe",
            instructions=[
                "Você é o assistente de crédito imobiliário da CashMe.",
                "Sempre use a base de conhecimento antes de responder perguntas sobre produtos.",
                "Para avaliações de crédito, use a ferramenta avaliar_perfil_credito.",
                "A aprovação final depende de análise completa — nunca prometa resultado.",
                "Responda sempre em português brasileiro.",
            ],
            markdown=True,
            show_tool_calls=True,
        )
        trace = start_trace(
            name="chat.agno",
            session_id=session_id,
            user_id=str(kwargs.get("user_id") or kwargs.get("user") or ""),
            input=message,
            tags=["chat", "agno"],
            metadata={"provider": provider, "model": settings.default_llm_model},
        )
        try:
            response = agent.run(message)
        except Exception as e:
            end_trace(trace, output=str(e), level="ERROR", status_message=type(e).__name__)
            raise
        end_trace(trace, output=response.content)
        return {"response": response.content, "session_id": session_id, "agent": "agno"}
