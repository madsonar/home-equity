"""Especialista em crédito: chama ML scorer e interpreta LTV/DTI."""
from __future__ import annotations

from typing import Any

from loguru import logger

from app.container import get_score_use_case
from app.domain.credit.entities import CreditFeatures


def run(*, payload: dict[str, Any]) -> dict[str, Any]:
    try:
        features = CreditFeatures(
            monthly_income=float(payload.get("monthly_income", 0) or 0),
            property_value=float(payload.get("property_value", 0) or 0),
            requested_amount=float(payload.get("requested_amount", 0) or 0),
            employment_years=float(payload.get("employment_years", 2) or 2),
            age=int(payload.get("age", 35) or 35),
            has_other_debts=bool(payload.get("has_other_debts", False)),
            profession=str(payload.get("profession", "") or ""),
            loan_purpose=str(payload.get("loan_purpose", "") or ""),
        )
        score = get_score_use_case().execute(features)
        lines = [
            f"Score ML: {score.score:.0%} — {'APROVADO' if score.approved else 'REPROVADO'} pelo modelo.",
            f"LTV: {score.ltv:.0%} (limite BACEN HE puro: 60%).",
            f"Parcela estimada (120m): R$ {score.monthly_installment:,.2f}.",
        ]
        if score.risk_factors:
            lines.append("Fatores de risco: " + "; ".join(score.risk_factors) + ".")
        return {"summary": "\n".join(lines), "sources": [{"source": "ml_credit_model"}]}
    except Exception as e:
        logger.exception("credit_expert falhou")
        return {"summary": f"Falha ao calcular score: {e}", "sources": []}
