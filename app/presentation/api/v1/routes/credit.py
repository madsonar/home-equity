import time
from typing import List
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.container import get_score_use_case, get_finetune_use_case
from app.application.credit.score_use_case import ScoreCreditUseCase
from app.application.credit.finetune_use_case import FinetuneScorerUseCase
from app.domain.credit.entities import CreditFeatures
from app.infrastructure.observability.metrics import credit_score_total, model_prediction_seconds

router = APIRouter(prefix="/score", tags=["credit"])


class ScoreRequest(BaseModel):
    monthly_income: float = Field(..., gt=0, description="Renda mensal em R$")
    property_value: float = Field(..., gt=0, description="Valor do imóvel em R$")
    requested_amount: float = Field(..., gt=0, description="Valor solicitado em R$")
    employment_years: float = Field(default=2.0, ge=0)
    age: int = Field(default=35, ge=18, le=80)
    has_other_debts: bool = Field(default=False)
    profession: str = Field(default="")
    loan_purpose: str = Field(default="")


class ScoreResponse(BaseModel):
    score: float
    approved: bool
    ltv: float
    monthly_installment: float
    risk_factors: List[str]
    explanation: str


@router.post("", response_model=ScoreResponse)
async def credit_score(req: ScoreRequest, use_case: ScoreCreditUseCase = Depends(get_score_use_case)):
    features = CreditFeatures(
        monthly_income=req.monthly_income,
        property_value=req.property_value,
        requested_amount=req.requested_amount,
        employment_years=req.employment_years,
        age=req.age,
        has_other_debts=req.has_other_debts,
        profession=req.profession,
        loan_purpose=req.loan_purpose,
    )
    try:
        t0 = time.perf_counter()
        result = use_case.execute(features)
        model_prediction_seconds.observe(time.perf_counter() - t0)
        credit_score_total.labels(result="approved" if result.approved else "rejected").inc()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro no modelo: {str(e)}")
    return ScoreResponse(
        score=result.score, approved=result.approved, ltv=result.ltv,
        monthly_installment=result.monthly_installment,
        risk_factors=result.risk_factors, explanation=result.explanation,
    )


@router.post("/retrain")
async def retrain_model(use_case: FinetuneScorerUseCase = Depends(get_finetune_use_case)):
    """Retreina o modelo de credit scoring (Snowflake se configurado, senão sintético)."""
    try:
        return use_case.execute()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
