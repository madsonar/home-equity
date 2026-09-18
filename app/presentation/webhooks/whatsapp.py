"""
Webhook WhatsApp — recebe mensagens via Twilio e responde com o agente.
Endpoint: POST /webhooks/whatsapp
"""
from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import PlainTextResponse
from loguru import logger

from app.infrastructure.messaging.whatsapp import parse_twilio_webhook, send_whatsapp_message

webhook_router = APIRouter(prefix="/webhooks", tags=["webhooks"])


@webhook_router.post("/whatsapp", response_class=PlainTextResponse)
async def whatsapp_webhook(request: Request):
    """Recebe mensagem do WhatsApp via Twilio e responde com o agente."""
    try:
        form_data = dict(await request.form())
        parsed = parse_twilio_webhook(form_data)
        from_number = parsed["from"]
        message_body = parsed["body"]
        logger.info(f"WhatsApp recebido de {from_number}: {message_body[:80]}")

        from app.container import get_chat_use_case
        use_case = get_chat_use_case()
        result = use_case.execute(
            message=message_body,
            session_id=f"wa_{from_number}",
            agent="langchain",
        )
        response_text = result["response"]

        try:
            send_whatsapp_message(from_number, response_text)
        except Exception as e:
            logger.warning(f"Falha ao enviar resposta WhatsApp: {e}")

        # Twilio espera TwiML ou 200 vazio
        return ""
    except Exception as e:
        logger.error(f"Erro no webhook WhatsApp: {e}")
        raise HTTPException(status_code=500, detail=str(e))
