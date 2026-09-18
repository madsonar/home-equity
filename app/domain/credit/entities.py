from dataclasses import dataclass, field
from typing import List


@dataclass
class CreditFeatures:
    monthly_income: float
    property_value: float
    requested_amount: float
    employment_years: float
    age: int
    has_other_debts: bool
    profession: str = ""
    loan_purpose: str = ""


@dataclass
class CreditScore:
    score: float
    approved: bool
    ltv: float
    monthly_installment: float
    risk_factors: List[str] = field(default_factory=list)
    explanation: str = ""
