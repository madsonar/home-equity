"""
Testes de integração da API — usa TestClient sem chamadas reais a LLMs/VectorDB.
Mocks injetados via dependency_overrides do FastAPI.
"""
import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

from app.domain.credit.entities import CreditScore
from app.domain.knowledge.entities import KnowledgeChunk


@pytest.fixture
def client():
    from app.main import app
    from app import container

    # Mock credit scorer
    mock_scorer = MagicMock()
    mock_scorer.predict.return_value = CreditScore(
        score=0.78, approved=True, ltv=0.375, monthly_installment=2500.0,
        risk_factors=[], explanation="Perfil aprovado.",
    )
    mock_scorer.train.return_value = 0.85

    # Mock vector store
    mock_store = MagicMock()
    mock_store.search_with_score.return_value = [
        (KnowledgeChunk(content="Home Equity é crédito com garantia.", source="kb.md"), 0.92),
    ]

    # Override DI
    from app.application.credit.score_use_case import ScoreCreditUseCase
    from app.application.search.search_use_case import SearchUseCase

    app.dependency_overrides[container.get_score_use_case] = lambda: ScoreCreditUseCase(mock_scorer)
    app.dependency_overrides[container.get_search_use_case] = lambda: SearchUseCase(mock_store)

    with TestClient(app, raise_server_exceptions=False) as c:
        yield c

    app.dependency_overrides.clear()


def test_health(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "version" in data
    assert data["version"] == "2.0.0"


def test_score_approved(client):
    payload = {
        "monthly_income": 15000.0,
        "property_value": 800000.0,
        "requested_amount": 300000.0,
        "employment_years": 5.0,
        "age": 38,
        "has_other_debts": False,
    }
    response = client.post("/api/v1/score", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["approved"] is True
    assert 0.0 <= data["score"] <= 1.0
    assert "ltv" in data
    assert "explanation" in data


def test_score_validation_rejects_zero_income(client):
    payload = {
        "monthly_income": 0.0,  # inválido: gt=0
        "property_value": 800000.0,
        "requested_amount": 300000.0,
    }
    response = client.post("/api/v1/score", json=payload)
    assert response.status_code == 422


def test_score_validation_rejects_underage(client):
    payload = {
        "monthly_income": 10000.0,
        "property_value": 500000.0,
        "requested_amount": 200000.0,
        "age": 17,  # inválido: ge=18
    }
    response = client.post("/api/v1/score", json=payload)
    assert response.status_code == 422


def test_search_returns_results(client):
    response = client.get("/api/v1/search?q=home+equity&k=2")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    assert "content" in data[0]
    assert "score" in data[0]


def test_search_requires_query(client):
    response = client.get("/api/v1/search?q=")
    assert response.status_code == 400
