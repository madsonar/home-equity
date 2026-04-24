from app.domain.credit.entities import CreditFeatures, CreditScore
from app.domain.credit.ports import ICreditScorer


class ScoreCreditUseCase:
    def __init__(self, scorer: ICreditScorer):
        self._scorer = scorer

    def execute(self, features: CreditFeatures) -> CreditScore:
        return self._scorer.predict(features)
