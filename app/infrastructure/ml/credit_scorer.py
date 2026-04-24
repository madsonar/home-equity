import os
import pickle
from typing import Optional, List

import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score
from loguru import logger

from app.config import settings
from app.domain.credit.entities import CreditFeatures, CreditScore
from app.domain.credit.ports import ICreditScorer


MODEL_PATH = settings.credit_model_path
DEFAULT_TERM_MONTHS = 120

_text_vectorizer: Optional[TfidfVectorizer] = None
_use_transformers = False


def _try_load_transformers():
    global _use_transformers
    try:
        from sentence_transformers import SentenceTransformer
        _use_transformers = True
        return SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")
    except ImportError:
        return None


def _get_text_features(texts: list[str]) -> np.ndarray:
    global _text_vectorizer
    model = _try_load_transformers()
    if model is not None:
        return model.encode(texts)
    if _text_vectorizer is None:
        _text_vectorizer = TfidfVectorizer(max_features=100, ngram_range=(1, 2))
        _text_vectorizer.fit(texts)
    return _text_vectorizer.transform(texts).toarray()


def _compute_features(feat: CreditFeatures) -> np.ndarray:
    ltv = feat.requested_amount / feat.property_value if feat.property_value > 0 else 1.0
    dti = (feat.requested_amount / DEFAULT_TERM_MONTHS) / feat.monthly_income if feat.monthly_income > 0 else 1.0
    numeric = np.array([[
        feat.monthly_income, feat.property_value, feat.requested_amount,
        feat.employment_years, float(feat.age), float(feat.has_other_debts), ltv, dti,
    ]])
    text_input = f"{feat.profession} {feat.loan_purpose}".strip() or "profissional assalariado"
    return np.hstack([numeric, _get_text_features([text_input])])


def _generate_synthetic_data(n: int = 500):
    rng = np.random.default_rng(42)
    incomes = rng.uniform(3000, 50000, n)
    prop_values = rng.uniform(200_000, 2_000_000, n)
    amounts = prop_values * rng.uniform(0.1, 0.8, n)
    years = rng.uniform(0, 30, n)
    ages = rng.integers(21, 70, n)
    debts = rng.integers(0, 2, n)
    ltvs = amounts / prop_values
    dtis = (amounts / DEFAULT_TERM_MONTHS) / incomes
    approved = ((ltvs < 0.6) & (dtis < 0.3) & (incomes > 5000) & (years > 1)).astype(int)
    noise_idx = rng.choice(n, size=int(n * 0.1), replace=False)
    approved[noise_idx] = 1 - approved[noise_idx]
    texts = ["profissional assalariado refinanciamento"] * n
    text_feats = _get_text_features(texts)
    numeric = np.column_stack([incomes, prop_values, amounts, years, ages.astype(float),
                                debts.astype(float), ltvs, dtis])
    return np.hstack([numeric, text_feats]), approved


def _rows_to_arrays(rows: List) -> tuple[np.ndarray, np.ndarray]:
    """Converte linhas do Snowflake (monthly_income, ..., approved) em X, y."""
    feats, labels = [], []
    for row in rows:
        feat = CreditFeatures(
            monthly_income=float(row[0]), property_value=float(row[1]),
            requested_amount=float(row[2]), employment_years=float(row[3]),
            age=int(row[4]), has_other_debts=bool(row[5]),
            profession=str(row[6] or ""), loan_purpose=str(row[7] or ""),
        )
        feats.append(_compute_features(feat).flatten())
        labels.append(int(row[8]))
    return np.array(feats), np.array(labels)


class SklearnCreditScorer(ICreditScorer):
    def __init__(self):
        self._pipeline: Optional[Pipeline] = None

    def _load_or_train(self) -> Pipeline:
        global _text_vectorizer
        if self._pipeline is not None:
            return self._pipeline
        if os.path.exists(MODEL_PATH):
            with open(MODEL_PATH, "rb") as f:
                pipeline, vectorizer = pickle.load(f)
            if vectorizer is not None:
                _text_vectorizer = vectorizer
            self._pipeline = pipeline
            return pipeline
        self.train()
        return self._pipeline  # type: ignore

    def train(self, real_data: Optional[List] = None) -> float:
        logger.info("Treinando modelo de credit scoring...")
        if real_data:
            X, y = _rows_to_arrays(real_data)
            logger.info(f"Usando {len(y)} registros reais do Snowflake")
        else:
            X, y = _generate_synthetic_data(1000)

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        pipeline = Pipeline([
            ("scaler", StandardScaler()),
            ("clf", RandomForestClassifier(n_estimators=100, random_state=42, class_weight="balanced")),
        ])
        pipeline.fit(X_train, y_train)
        auc = roc_auc_score(y_test, pipeline.predict_proba(X_test)[:, 1])
        logger.info(f"Modelo treinado. AUC-ROC: {auc:.4f}")
        os.makedirs("./data", exist_ok=True)
        with open(MODEL_PATH, "wb") as f:
            pickle.dump((pipeline, _text_vectorizer), f)
        self._pipeline = pipeline
        return auc

    def predict(self, features: CreditFeatures) -> CreditScore:
        model = self._load_or_train()
        X = _compute_features(features)
        prob = float(model.predict_proba(X)[0][1])
        ltv = features.requested_amount / features.property_value if features.property_value > 0 else 1.0
        dti = (features.requested_amount / DEFAULT_TERM_MONTHS) / features.monthly_income if features.monthly_income > 0 else 1.0
        installment = features.requested_amount / DEFAULT_TERM_MONTHS
        risk_factors = []
        if ltv > 0.6:
            risk_factors.append(f"LTV elevado ({ltv:.0%} > 60%)")
        if dti > 0.3:
            risk_factors.append(f"Comprometimento de renda alto ({dti:.0%} > 30%)")
        if features.employment_years < 1:
            risk_factors.append("Menos de 1 ano de vínculo empregatício")
        if features.has_other_debts:
            risk_factors.append("Possui outras dívidas em aberto")
        approved = prob >= 0.6
        explanation = (
            f"Score de crédito: {prob:.0%}. LTV: {ltv:.0%}. "
            f"Comprometimento de renda: {dti:.0%}. "
            + (f"Fatores de risco: {'; '.join(risk_factors)}." if risk_factors else "Perfil dentro dos critérios.")
        )
        return CreditScore(
            score=round(prob, 4), approved=approved, ltv=round(ltv, 4),
            monthly_installment=round(installment, 2), risk_factors=risk_factors, explanation=explanation,
        )
