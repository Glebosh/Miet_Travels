import os


class Settings:
    telegram_bot_token: str = os.environ.get("FEEDBACK_TELEGRAM_BOT_TOKEN", "")
    telegram_chat_id: str = os.environ.get("FEEDBACK_TELEGRAM_CHAT_ID", "")
    request_timeout_sec: int = int(os.environ.get("FEEDBACK_REQUEST_TIMEOUT_SEC", "5"))
    log_level: str = os.environ.get("FEEDBACK_LOG_LEVEL", "INFO")


settings = Settings()
