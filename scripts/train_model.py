"""Treina e salva o modelo de credit scoring (com tracking MLflow opcional)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.makedirs("./data", exist_ok=True)

from app.infrastructure.ml.credit_scorer import SklearnCreditScorer

scorer = SklearnCreditScorer()
auc = scorer.train()
print(f"Modelo salvo em ./data/credit_model.pkl  (AUC-ROC: {auc:.4f})")
