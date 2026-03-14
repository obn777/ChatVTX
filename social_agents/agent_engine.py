import json
import os
import random
import time
import re
import sys
from pyrogram import Client, filters
from pyrogram.enums import ChatAction

# Добавляем корневую директорию в путь, чтобы видеть core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from core.domain.ai.ai_expert import solve

# ===============================
# Официальные ключи Telegram Desktop 
# (Используем их, раз my.telegram.org не пускает)
# ===============================
API_ID = 2040
API_HASH = "b18441a1ff60e31889c02d1f11e97420"

# Пути к данным
WORKDIR = "/home/obn7/NovBase/social_agents/sessions"
CONFIG_PATH = "/home/obn7/NovBase/social_agents/targets.json"

# Создаем папку сессий, если её нет
if not os.path.exists(WORKDIR):
    os.makedirs(WORKDIR)

app = Client(
    "malyshka_agent",
    api_id=API_ID,
    api_hash=API_HASH,
    workdir=WORKDIR
)

def get_allowed_chats():
    """Загрузка белого списка чатов"""
    if not os.path.exists(CONFIG_PATH):
        # Создаем пустой конфиг, если файла нет
        with open(CONFIG_PATH, 'w') as f:
            json.dump({"allowed_chats": []}, f)
        return []
    
    try:
        with open(CONFIG_PATH, 'r') as f:
            data = json.load(f)
            return data.get("allowed_chats", [])
    except Exception as e:
        print(f"❌ Ошибка конфига: {e}")
        return []

@app.on_message(filters.group & ~filters.me)
async def agent_logic(client, message):
    allowed_chats = get_allowed_chats()
    
    # 1. Проверка: разрешен ли этот чат?
    if message.chat.id not in allowed_chats:
        # Временная отладка: выводим ID чатов, где ты находишься
        print(f"👀 Пропускаю сообщение в '{message.chat.title}' (ID: {message.chat.id})")
        return

    text = message.text.lower() if message.text else ""
    
    # 2. Триггеры для входа в дискуссию
    triggers = ["ии", "ai", "нейросеть", "8b", "nitro", "контур", "прогноз", "малышка"]
    
    if any(word in text for word in triggers):
        # Получаем ответ от ИИ-эксперта
        raw_response = solve(text)
        
        if raw_response:
            # Очистка от HTML (в группах юзерботу лучше писать как человек)
            clean_reply = re.sub('<[^<]+?>', '', raw_response)
            
            print(f"🎯 [AGENT] Отвечаю в чате: {message.chat.title}")
            
            # 3. Имитация присутствия (Typing...)
            await client.send_chat_action(message.chat.id, ChatAction.TYPING)
            
            # Рандомная пауза, будто человек думает и пишет
            await time.sleep(random.randint(5, 12))
            
            await message.reply_text(clean_reply)

if __name__ == "__main__":
    print("--- NovBase: Social Agent Active ---")
    print(f"📂 Рабочая папка: {WORKDIR}")
    print("🚀 Запускаю процесс авторизации...")
    app.run()
