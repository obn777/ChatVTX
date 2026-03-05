import os
import asyncio
import logging
from typing import Optional

from .telegram_client import TelegramClient


logger = logging.getLogger("TelegramService")


class TelegramService:
    """
    Высокоуровневый сервис Telegram для NovBase.

    Отвечает за:
    - управление клиентом
    - контроль состояния
    - унифицированную отправку сообщений
    - безопасную работу в Flask + asyncio
    """

    def __init__(self, client: Optional[TelegramClient] = None):
        token = os.getenv("TELEGRAM_BOT_TOKEN")

        if client:
            self.client = client
        else:
            if not token:
                raise ValueError(
                    "Переменная окружения TELEGRAM_BOT_TOKEN не задана."
                )
            self.client = TelegramClient(token)

        self._running = False

    # =====================================================
    # Lifecycle
    # =====================================================

    def start(self):
        """
        Запуск сервиса.
        Сейчас TelegramClient не требует фонового процесса.
        Метод оставлен для будущего расширения (polling/webhook).
        """
        if self._running:
            return

        self._running = True
        logger.info("TelegramService запущен.")

    def stop(self):
        """
        Остановка сервиса.
        """
        if not self._running:
            return

        self._running = False
        logger.info("TelegramService остановлен.")

    def is_running(self) -> bool:
        """
        Проверка состояния сервиса.
        """
        return self._running

    # =====================================================
    # Messaging API
    # =====================================================

    def send(self, chat_id: str, message: str):
        """
        Унифицированная отправка сообщения.

        Работает:
        - в async окружении (Flask + event loop)
        - в синхронном режиме
        """

        if not self._running:
            self.start()

        try:
            # Если уже существует активный event loop
            loop = asyncio.get_running_loop()
            return loop.create_task(
                self.client.send_message(chat_id, message)
            )

        except RuntimeError:
            # Если loop отсутствует — выполняем синхронно
            return self.client.send_sync(chat_id, message)

    # =====================================================
    # Convenience Method
    # =====================================================

    async def send_async(self, chat_id: str, message: str):
        """
        Явный асинхронный метод.
        Используется внутри async-сервисов.
        """
        if not self._running:
            self.start()

        await self.client.send_message(chat_id, message)
