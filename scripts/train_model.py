"""Treina e salva o modelo de credit scoring."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

os.makedirs("./data", exist_ok=True)

from app.ml.credit_scorer import train_model

auc = train_model()
print(f"Modelo salvo em ./data/credit_model.pkl  (AUC-ROC: {auc:.4f})")
