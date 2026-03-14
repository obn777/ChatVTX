# core/services/telegram/telegram_gateway.py

import asyncio
from core.logic_processor import LogicProcessor
from .telegram_service import TelegramService


class TelegramGateway:

    def __init__(self, token: str):
        self.logic = LogicProcessor()
        self.service = TelegramService(token=token)

    async def handle_message(self, chat_id: str, text: str):
        result = await self.logic.process_message(text)

        if result["result"]:
            await self.service.send(chat_id, result["result"])

    def start(self):
        # здесь будет polling или webhook
        pass
