"""
Integração WhatsApp via Twilio.
Import lazy: o módulo carrega sem twilio instalado.
"""
from __future__ import annotations
from loguru import logger


def _get_client():
    try:
        from twilio.rest import Client
        from app.config import settings
        return Client(settings.twilio_account_sid, settings.twilio_auth_token), settings
    except ImportError as e:
        raise ImportError("twilio não instalado. Execute: pip install twilio") from e


def send_whatsapp_message(to: str, body: str) -> str:
    """Envia mensagem via WhatsApp (Twilio). Retorna o SID da mensagem."""
    client, settings = _get_client()
    message = client.messages.create(
        body=body,
        from_=f"whatsapp:{settings.twilio_whatsapp_from}",
        to=f"whatsapp:{to}",
    )
    logger.info(f"WhatsApp enviado para {to}: {message.sid}")
    return message.sid


def parse_twilio_webhook(form_data: dict) -> dict:
    """Extrai campos relevantes de um webhook Twilio."""
    return {
        "from": form_data.get("From", "").replace("whatsapp:", ""),
        "body": form_data.get("Body", ""),
        "message_sid": form_data.get("MessageSid", ""),
        "profile_name": form_data.get("ProfileName", ""),
    }
