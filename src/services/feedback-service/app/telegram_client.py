import requests


class TelegramClient:
    def __init__(self, token: str, chat_id: str, timeout_sec: int = 5):
        self.token = token
        self.chat_id = chat_id
        self.timeout_sec = timeout_sec

    def send_feedback(self, name: str, email: str, message: str) -> None:
        if not self.token or not self.chat_id:
            raise Exception("Can't make response due lack of token and chat_id")

        payload = {
            "chat_id": self.chat_id,
            "text": f"Сообщение от {name}:\n\n{message}\n\nПочта пользователя: {email}",
        }
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        try:
            response = requests.post(url, json=payload, timeout=self.timeout_sec)

        except requests.RequestException as e:
            raise ConnectionError("telegram request failed") from e

        if response.status_code not in (200, 201):
            raise RuntimeError("telegram returned non-success response")
