from typing import Literal, Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field

from app.container import get_chat_use_case
from app.application.chat.chat_use_case import ChatUseCase
from app.infrastructure.guardrails.nemo_guardrails import apply_guardrails
from app.infrastructure.observability.metrics import agent_requests_total

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000)
    session_id: str = Field(default="default")
    agent: Literal["langchain", "agno"] = Field(default="langchain")
    provider: Optional[str] = Field(default=None, description="openai | gemini | deepseek")
    model: Optional[str] = Field(default=None)
    use_guardrails: bool = Field(default=False)


class ChatResponse(BaseModel):
    response: str
    session_id: str
    agent: str


@router.post("", response_model=ChatResponse)
async def chat(req: ChatRequest, use_case: ChatUseCase = Depends(get_chat_use_case)):
    try:
        result = use_case.execute(
            message=req.message,
            session_id=req.session_id,
            agent=req.agent,
            provider=req.provider,
            model=req.model,
        )
        agent_requests_total.labels(agent_type=req.agent).inc()
        if req.use_guardrails:
            result["response"] = await apply_guardrails(req.message, result["response"])
        return ChatResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
