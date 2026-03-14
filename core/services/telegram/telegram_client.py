import asyncio
import os
from typing import Optional

from telegram import Bot
from telegram.error import TelegramError


class TelegramClient:
    """
    Низкоуровневый клиент Telegram API.
    Отвечает только за отправку сообщений.
    Совместим с python-telegram-bot v20+.
    """

    def __init__(self, token: Optional[str] = None):
        """
        Token можно передать явно или через переменную окружения TELEGRAM_TOKEN.
        """
        self.token = token or os.getenv("TELEGRAM_TOKEN")

        if not self.token:
            raise ValueError(
                "Telegram token is not provided. "
                "Set TELEGRAM_TOKEN environment variable."
            )

        self.bot = Bot(token=self.token)

    # -------------------------------------------------
    # Async API
    # -------------------------------------------------

    async def send_message(self, chat_id: str, text: str):
        """
        Асинхронная отправка сообщения.
        """
        try:
            await self.bot.send_message(
                chat_id=chat_id,
                text=text
            )
        except TelegramError as e:
            raise RuntimeError(f"Telegram send error: {e}")

    # -------------------------------------------------
    # Sync Wrapper (для Flask)
    # -------------------------------------------------

    def send_sync(self, chat_id: str, text: str):
        """
        Синхронная безопасная отправка.
        Подходит для использования внутри Flask.
        """

        try:
            loop = asyncio.get_running_loop()
            # Если loop уже активен — создаём задачу
            loop.create_task(self.send_message(chat_id, text))
        except RuntimeError:
            # Если event loop не запущен — используем asyncio.run
            asyncio.run(self.send_message(chat_id, text))
