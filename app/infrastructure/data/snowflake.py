"""
Conector Snowflake para dados reais de crédito.
Import lazy: o módulo carrega sem snowflake-connector-python instalado.
"""
from __future__ import annotations
from typing import List, Optional
from loguru import logger


def _get_connector():
    try:
        import snowflake.connector
        from app.config import settings
        return snowflake.connector, settings
    except ImportError as e:
        raise ImportError(
            "snowflake-connector-python não instalado. Execute: pip install snowflake-connector-python"
        ) from e


class SnowflakeRepository:
    """Repositório de dados reais de crédito no Snowflake."""

    def __init__(self):
        self._conn = None

    def _get_connection(self):
        sf, settings = _get_connector()
        if self._conn is None or self._conn.is_closed():
            self._conn = sf.connect(
                account=settings.snowflake_account,
                user=settings.snowflake_user,
                password=settings.snowflake_password,
                warehouse=settings.snowflake_warehouse,
                database=settings.snowflake_database,
                schema=settings.snowflake_schema,
            )
            logger.info("Conectado ao Snowflake")
        return self._conn

    def fetch_credit_data(self, limit: int = 10_000) -> List[tuple]:
        """
        Retorna linhas de CREDIT_APPLICATIONS.
        Colunas esperadas:
          monthly_income, property_value, requested_amount, employment_years,
          age, has_other_debts, profession, loan_purpose, approved
        """
        conn = self._get_connection()
        cursor = conn.cursor()
        cursor.execute(
            """
            SELECT
                monthly_income, property_value, requested_amount,
                employment_years, age, has_other_debts,
                profession, loan_purpose, approved
            FROM CREDIT_APPLICATIONS
            LIMIT %(limit)s
            """,
            {"limit": limit},
        )
        rows = cursor.fetchall()
        logger.info(f"Snowflake: {len(rows)} registros obtidos")
        return rows

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None


def get_snowflake_repo() -> Optional[SnowflakeRepository]:
    """Retorna instância ou None se credenciais não configuradas."""
    try:
        from app.config import settings
        if not (settings.snowflake_account and settings.snowflake_user):
            return None
        return SnowflakeRepository()
    except Exception:
        return None
