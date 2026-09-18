"""
NeMo Guardrails — compliance e segurança para respostas do agente.
Import lazy: o módulo carrega sem nemoguardrails instalado.
Guarda config em guardrails/ na raiz do projeto.
"""
from __future__ import annotations
import os
from typing import Optional, TYPE_CHECKING
from loguru import logger

if TYPE_CHECKING:
    from nemoguardrails import LLMRails

_rails: Optional["LLMRails"] = None
_GUARDRAILS_PATH = os.path.join(os.path.dirname(__file__), "../../../guardrails")


def _get_rails() -> Optional["LLMRails"]:
    global _rails
    if _rails is not None:
        return _rails
    try:
        from nemoguardrails import RailsConfig, LLMRails
        config_path = os.path.abspath(_GUARDRAILS_PATH)
        if not os.path.exists(config_path):
            logger.info("Pasta guardrails/ não encontrada — guardrails desativados")
            return None
        config = RailsConfig.from_path(config_path)
        _rails = LLMRails(config)
        logger.info("NeMo Guardrails configurado com sucesso")
        return _rails
    except ImportError:
        logger.info("nemoguardrails não instalado — guardrails desativados")
        return None
    except Exception as e:
        logger.warning(f"Erro ao carregar NeMo Guardrails: {e}")
        return None


async def apply_guardrails(user_message: str, bot_response: str) -> str:
    """
    Aplica guardrails na resposta do agente.
    Retorna a resposta original se guardrails não disponíveis.
    """
    rails = _get_rails()
    if rails is None:
        return bot_response
    try:
        messages = [
            {"role": "user", "content": user_message},
            {"role": "assistant", "content": bot_response},
        ]
        result = await rails.generate_async(messages=messages)
        return result.get("content", bot_response)
    except Exception as e:
        logger.warning(f"Guardrails falhou ({e}) — usando resposta original")
        return bot_response
