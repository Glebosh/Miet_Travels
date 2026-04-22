import uuid

from fastapi import FastAPI, HTTPException
from loguru import logger

from app.config import settings
from app.schemas import FeedbackRequest, FeedbackResponse
from app.telegram_client import TelegramClient

app = FastAPI(title="feedback-service")
telegram_client = TelegramClient(
    token=settings.telegram_bot_token,
    chat_id=settings.telegram_chat_id,
    timeout_sec=settings.request_timeout_sec,
)


@app.get("/health")
def health():
    return {"ok": True}


@app.post("/api/v1/feedback", response_model=FeedbackResponse, status_code=202)
def create_feedback(payload: FeedbackRequest):
    request_id = str(uuid.uuid4())

    try:
        telegram_client.send_feedback(
            name=payload.name,
            email=payload.email,
            message=payload.message,
        )
        logger.info("feedback sent: ", request_id)
    except Exception as exc:
        logger.error("feedback failed: ", request_id, str(exc))
        raise HTTPException(
            status_code=502,
            detail={"ok": False, "error": "telegram_unavailable", "request_id": request_id},
        ) from exc

    return FeedbackResponse(ok=True, status="accepted", request_id=request_id)
