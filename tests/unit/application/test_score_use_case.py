import pytest
from unittest.mock import MagicMock

from app.domain.credit.entities import CreditFeatures, CreditScore
from app.domain.credit.ports import ICreditScorer
from app.application.credit.score_use_case import ScoreCreditUseCase


def test_score_use_case_delegates_to_scorer(sample_features, approved_score):
    mock_scorer = MagicMock(spec=ICreditScorer)
    mock_scorer.predict.return_value = approved_score

    use_case = ScoreCreditUseCase(scorer=mock_scorer)
    result = use_case.execute(sample_features)

    assert result == approved_score
    mock_scorer.predict.assert_called_once_with(sample_features)


def test_score_use_case_returns_rejected(sample_features):
    rejected = CreditScore(
        score=0.25, approved=False, ltv=0.8, monthly_installment=5000.0,
        risk_factors=["LTV elevado (80% > 60%)"], explanation="Reprovado.",
    )
    mock_scorer = MagicMock(spec=ICreditScorer)
    mock_scorer.predict.return_value = rejected

    use_case = ScoreCreditUseCase(scorer=mock_scorer)
    result = use_case.execute(sample_features)

    assert result.approved is False
    assert "LTV" in result.risk_factors[0]


def test_score_use_case_propagates_exception(sample_features):
    mock_scorer = MagicMock(spec=ICreditScorer)
    mock_scorer.predict.side_effect = RuntimeError("Modelo não carregado")

    use_case = ScoreCreditUseCase(scorer=mock_scorer)
    with pytest.raises(RuntimeError, match="Modelo não carregado"):
        use_case.execute(sample_features)
