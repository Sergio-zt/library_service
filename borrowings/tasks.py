import os
import requests
from celery import shared_task


@shared_task
def send_telegram_notification(message):
    bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")

    if not bot_token or not chat_id:
        print("Telegram credentials are not set in .env")
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": message,
    }

    try:
        response = requests.post(url, json=payload)
        # Проверяем, успешен ли запрос (код 200)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send message to Telegram: {e}")
