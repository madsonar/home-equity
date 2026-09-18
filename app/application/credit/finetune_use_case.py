from typing import Optional
from loguru import logger

from app.domain.credit.ports import ICreditScorer


class FinetuneScorerUseCase:
    """Retreina o modelo de crédito com dados reais do Snowflake (fallback: sintéticos)."""

    def __init__(self, scorer: ICreditScorer, snowflake_repo=None):
        self._scorer = scorer
        self._snowflake = snowflake_repo

    def execute(self) -> dict:
        if self._snowflake is not None:
            try:
                rows = self._snowflake.fetch_credit_data()
                logger.info(f"Dados reais obtidos do Snowflake: {len(rows)} registros")
                auc = self._scorer.train(real_data=rows)
            except Exception as exc:
                logger.warning(f"Falha ao buscar dados do Snowflake ({exc}). Usando dados sintéticos.")
                auc = self._scorer.train()
        else:
            logger.info("Snowflake não configurado — treinando com dados sintéticos.")
            auc = self._scorer.train()

        return {"auc_roc": round(auc, 4), "status": "ok"}
