import asyncio
from core.services.telegram.telegram_client import TelegramClient

async def main():
    client = TelegramClient()
    await client.send_message(
        chat_id="ВАШ_CHAT_ID",
        text="NovBase Telegram test OK 🚀"
    )

if __name__ == "__main__":
    asyncio.run(main())
