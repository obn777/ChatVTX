import os, time, threading, datetime, requests, asyncio, re
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ==================================================
# Core & Domain Imports
# ==================================================
try:
    from core.logic_processor import LogicProcessor
    from core.auth_manager import AuthManager
    from core.domain.system_vtx import vtx_manager
    from core.domain.telegram.bot_connector import BotConnector
    from core.domain.telegram.telegram_router import TelegramRouter
    from core.domain.telegram.user_connector import UserConnector
except Exception as e:
    print(f"⚠️ [BOT_ERROR]: Ошибка импорта модулей: {e}")

# ==================================================
# Конфигурация
# ==================================================
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 5173080765
CHANNEL_ID = -1003753510672
BASE_DIR = "/home/obn7/NovBase/"

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
SMTP_USER = "vtxm777@gmail.com"
SMTP_PASSWORD = "taiwnzgkjvuamwrb"

SITE_TOP = "🚀 <b>VTX TERMINAL:</b> <a href='https://chatvtx.xyz'>ОТКРЫТЬ</a>\n"
SITE_BOT = "\n\n🌐 <a href='https://chatvtx.xyz'>chatvtx.xyz</a>"

# Глобальные переменные (инициализируются внутри run_bot)
logic = None
auth_mgr = None
bot = None
router = None
users = None

def send_email_notification(target_email, user_name, key):
    try:
        msg = MIMEMultipart()
        msg['From'] = f"VTX Core <{SMTP_USER}>"
        msg['To'] = target_email
        msg['Subject'] = "🔑 Ваш ключ доступа к VTX ULTRA CORE"
        body = f"Здравствуйте, {user_name}!\n\nВаш персональный ключ: {key}\nВход: https://chatvtx.xyz"
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as e:
        print(f"❌ SMTP Error: {e}")
        return False

async def get_ai_reply(text):
    """Безопасный вызов нейросети"""
    try:
        # Теперь здесь всегда будет использоваться GPU-версия,
        # переданная из app.py
        res = await logic.process_message(text, user_status="Free")
        return res.get("result", "Система активна.")
    except Exception as e:
        return f"⚠️ Ошибка ядра: {e}"

def run_bot(shared_logic=None):
    """
    Основная функция запуска бота.
    Принимает shared_logic, чтобы не плодить копии нейросети в RAM/VRAM.
    """
    global logic, auth_mgr, bot, router, users

    print("🤖 [BOT]: Инициализация систем бота...")

    # Приоритет отдается общему ядру (GPU)
    if shared_logic is not None:
        logic = shared_logic
        print("✅ [BOT]: Успешно подключено к единому GPU-ядру.")
    else:
        # Если бот запущен вручную как python3 bot.py
        print("⚠️ [BOT]: Общее ядро не найдено. Запуск локальной CPU-версии...")
        logic = LogicProcessor(force_cpu=True)

    auth_mgr = AuthManager(BASE_DIR)
    bot = BotConnector(TOKEN, BASE_DIR, SITE_TOP, SITE_BOT, vtx_manager)
    router = TelegramRouter(ADMIN_ID)
    users = UserConnector()

    offset = None

    # Создаем/получаем цикл событий для асинхронных ответов ИИ
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    print("烙 [BOT]: Система запущена и слушает обновления...")

    while True:
        try:
            # Получение обновлений
            r = requests.get(bot.base_url + "getUpdates", params={"offset": offset, "timeout": 10}, timeout=15)
            updates = r.json().get("result", [])

            for upd in updates:
                offset = upd["update_id"] + 1
                msg = upd.get("message")
                if not msg or "text" not in msg: continue

                uid = msg["from"]["id"]
                chat_id = msg["chat"]["id"]
                text = msg["text"].strip()

                state = users.get_state(uid)
                action = router.resolve_action(uid, text, state)

                if action == "START_REGISTRATION":
                    bot.send_msg(chat_id, "📥 Введите ваш <b>Email</b>:")
                    users.set_state(uid, "WAIT_DATA")
                elif action == "SUBMIT_DATA":
                    if "@" in text:
                        email = text.lower()
                        key = auth_mgr.approve_key(email)
                        threading.Thread(target=send_email_notification, args=(email, "User", key), daemon=True).start()
                        bot.send_msg(chat_id, f"✅ Ключ отправлен на {email}")
                        users.set_state(uid, "IDLE")
                    else:
                        bot.send_msg(chat_id, "⚠️ Укажите валидный Email.")
                else:
                    # Генерация ответа через единое ядро
                    reply = loop.run_until_complete(get_ai_reply(text))
                    bot.send_msg(chat_id, reply)

        except Exception as e:
            print(f"⚠️ [BOT_LOOP_ERROR]: {e}")
            time.sleep(5)

if __name__ == "__main__":
    # Для отладки только бота (запустится на CPU)
    run_bot()
