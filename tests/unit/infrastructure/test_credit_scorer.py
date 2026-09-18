"""
Testes do SklearnCreditScorer — não requerem APIs externas.
"""
import os
import pytest

from app.domain.credit.entities import CreditFeatures
from app.infrastructure.ml.credit_scorer import SklearnCreditScorer


@pytest.fixture
def scorer(tmp_path, monkeypatch):
    monkeypatch.setattr(
        "app.infrastructure.ml.credit_scorer.MODEL_PATH",
        str(tmp_path / "test_model.pkl"),
    )
    return SklearnCreditScorer()


def test_train_returns_valid_auc(scorer):
    auc = scorer.train()
    assert 0.5 <= auc <= 1.0


def test_predict_approved_profile(scorer):
    scorer.train()
    features = CreditFeatures(
        monthly_income=20_000.0,
        property_value=1_000_000.0,
        requested_amount=300_000.0,
        employment_years=8.0,
        age=40,
        has_other_debts=False,
    )
    result = scorer.predict(features)
    assert 0.0 <= result.score <= 1.0
    assert isinstance(result.approved, bool)
    assert result.ltv == pytest.approx(0.3, abs=0.001)
    assert result.monthly_installment == pytest.approx(2500.0, abs=0.01)


def test_predict_high_ltv_adds_risk_factor(scorer):
    scorer.train()
    features = CreditFeatures(
        monthly_income=5_000.0,
        property_value=300_000.0,
        requested_amount=250_000.0,  # LTV ~83%
        employment_years=2.0,
        age=30,
        has_other_debts=False,
    )
    result = scorer.predict(features)
    assert any("LTV" in rf for rf in result.risk_factors)


def test_predict_with_debts_adds_risk_factor(scorer):
    scorer.train()
    features = CreditFeatures(
        monthly_income=8_000.0,
        property_value=600_000.0,
        requested_amount=200_000.0,
        employment_years=3.0,
        age=35,
        has_other_debts=True,
    )
    result = scorer.predict(features)
    assert any("dívidas" in rf for rf in result.risk_factors)


def test_predict_ltv_calculation(scorer):
    scorer.train()
    features = CreditFeatures(
        monthly_income=15_000.0,
        property_value=800_000.0,
        requested_amount=400_000.0,
        employment_years=5.0,
        age=38,
        has_other_debts=False,
    )
    result = scorer.predict(features)
    assert result.ltv == pytest.approx(0.5, abs=0.001)
