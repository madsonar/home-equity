from abc import ABC, abstractmethod
from .entities import CreditFeatures, CreditScore


class ICreditScorer(ABC):
    @abstractmethod
    def predict(self, features: CreditFeatures) -> CreditScore: ...

    @abstractmethod
    def train(self) -> float: ...
