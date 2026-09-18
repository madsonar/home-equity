from app.domain.credit.entities import CreditFeatures, CreditScore


def test_credit_features_defaults():
    f = CreditFeatures(
        monthly_income=10_000.0,
        property_value=500_000.0,
        requested_amount=200_000.0,
        employment_years=3.0,
        age=35,
        has_other_debts=False,
    )
    assert f.profession == ""
    assert f.loan_purpose == ""
    assert f.has_other_debts is False


def test_credit_features_custom():
    f = CreditFeatures(
        monthly_income=25_000.0,
        property_value=1_000_000.0,
        requested_amount=400_000.0,
        employment_years=10.0,
        age=45,
        has_other_debts=True,
        profession="Médico",
        loan_purpose="Investimento",
    )
    assert f.profession == "Médico"
    assert f.has_other_debts is True


def test_credit_score_approved():
    s = CreditScore(score=0.75, approved=True, ltv=0.4, monthly_installment=3333.0)
    assert s.approved is True
    assert s.risk_factors == []
    assert s.explanation == ""


def test_credit_score_rejected():
    s = CreditScore(
        score=0.3,
        approved=False,
        ltv=0.75,
        monthly_installment=5000.0,
        risk_factors=["LTV elevado (75% > 60%)"],
        explanation="Reprovado por LTV.",
    )
    assert s.approved is False
    assert len(s.risk_factors) == 1
