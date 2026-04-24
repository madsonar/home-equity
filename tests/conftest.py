"""Fixtures compartilhadas entre todos os testes."""
import pytest
from unittest.mock import MagicMock

from app.domain.credit.entities import CreditFeatures, CreditScore
from app.domain.knowledge.entities import KnowledgeChunk


@pytest.fixture
def sample_features() -> CreditFeatures:
    return CreditFeatures(
        monthly_income=15000.0,
        property_value=800_000.0,
        requested_amount=300_000.0,
        employment_years=5.0,
        age=38,
        has_other_debts=False,
        profession="Engenheiro",
        loan_purpose="Reforma",
    )


@pytest.fixture
def approved_score() -> CreditScore:
    return CreditScore(
        score=0.82,
        approved=True,
        ltv=0.375,
        monthly_installment=2500.0,
        risk_factors=[],
        explanation="Perfil dentro dos critérios.",
    )


@pytest.fixture
def sample_chunks():
    return [
        KnowledgeChunk(content="Home Equity permite usar imóvel como garantia.", source="kb/intro.md"),
        KnowledgeChunk(content="LTV máximo da CashMe é 60%.", source="kb/politica.md"),
    ]
