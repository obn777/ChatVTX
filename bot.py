import os
import time
import requests
import subprocess
import re
from requests.exceptions import RequestException

from core.logic_processor import LogicProcessor

# ===============================
# Конфигурация и Безопасность
# ===============================

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ADMIN_ID = 5173080765  
# Финальный ID твоего канала
CHANNEL_ID = -1003753510672 

if not TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN not set")

BASE_URL = f"https://api.telegram.org/bot{TOKEN}/"

# Точные пути на твоем Nitro
PIPER_EXE = "/home/obn7/NovBase/core/tts/piper/piper"
PIPER_MODEL = "/home/obn7/NovBase/core/tts/piper/ru_RU-irina-medium.onnx"
VOICE_OUTPUT = "/home/obn7/NovBase/temp_voice.ogg"

# ===============================
# Инициализация ядра
# ===============================

logic = LogicProcessor()
offset = None

print(f"🚀 NovBase: Цифровой клон активен на Nitro.")
print(f"🎙️ Голос Ирины: {PIPER_MODEL}")
print(f"📢 Связь с каналом: {CHANNEL_ID} установлена.")

# ===============================
# Функции синтеза и связи
# ===============================

def speak(text):
    """Синтез речи через Piper и сжатие FFmpeg"""
    if not os.path.exists(PIPER_MODEL):
        print(f"❌ Ошибка: Модель не найдена: {PIPER_MODEL}")
        return None

    try:
        # Очистка текста от лишних символов для диктора
        clean_text = text.replace('\n', ' ').strip()
        clean_text = re.sub(r'[^\w\s\.,!\?\-]', '', clean_text)
        
        # Конвейер: Piper -> FFmpeg (Opus OGG)
        cmd = (
            f'echo "{clean_text}" | '
            f'{PIPER_EXE} --model {PIPER_MODEL} --output_raw | '
            f'ffmpeg -y -f s16le -ar 22050 -ac 1 -i - '
            f'-c:a libopus -b:a 32k -vbr on -application voip '
            f'{VOICE_OUTPUT}'
        )
        
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return VOICE_OUTPUT
    except Exception as e:
        print(f"❌ Ошибка синтеза: {e}")
        return None

def send_msg(chat_id, text):
    """Универсальная отправка текста"""
    try:
        requests.post(BASE_URL + "sendMessage", data={"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}, timeout=15)
    except Exception as e:
        print(f"❌ Ошибка отправки текста: {e}")

def send_voice(chat_id, file_path):
    """Отправка голосового сообщения"""
    url = BASE_URL + "sendVoice"
    try:
        with open(file_path, 'rb') as voice:
            requests.post(url, data={'chat_id': chat_id}, files={'voice': voice}, timeout=25)
    except Exception as e:
        print(f"❌ Ошибка отправки аудио: {e}")

# ===============================
# Основной цикл
# ===============================

while True:
    try:
        response = requests.get(BASE_URL + "getUpdates", params={"offset": offset, "timeout": 30}, timeout=35)
        data = response.json()

        if data.get("ok"):
            for update in data.get("result", []):
                offset = update["update_id"] + 1
                message = update.get("message")
                if not message: continue

                user_id = message.get("from", {}).get("id")
                chat_id = message["chat"]["id"]
                text = message.get("text", "").strip()

                # Логирование входящих для контроля
                print(f"📩 Входящее от ID: {user_id} | Текст: {text}")

                # 1. ДЕТЕКТОР ID КАНАЛА (оставляем для новых каналов)
                if message.get("forward_from_chat"):
                    f_id = message["forward_from_chat"]["id"]
                    f_title = message["forward_from_chat"].get("title", "Канал")
                    send_msg(chat_id, f"🔍 ID канала *{f_title}*: `{f_id}`")
                    continue

                # ФИЛЬТР АДМИНА
                if user_id != ADMIN_ID:
                    print(f"🚫 Попытка доступа от стороннего ID: {user_id}")
                    continue

                if not text: continue

                # 2. КОМАНДА ПУБЛИКАЦИИ В КАНАЛ
                if text.lower().startswith("канал:"):
                    post_content = text[6:].strip()
                    # Текст в канал
                    send_msg(CHANNEL_ID, post_content)
                    # Голос в канал
                    v_file = speak(post_content)
                    if v_file and os.path.exists(v_file):
                        send_voice(CHANNEL_ID, v_file)
                        os.remove(v_file)
                    send_msg(chat_id, "✅ Опубликовано в канале vtx_clone")
                
                else:
                    # 3. ОБЫЧНЫЙ ОТВЕТ ТЕБЕ В ЛИЧКУ
                    reply = logic.process(text) or "Модули промолчали."
                    send_msg(chat_id, reply)
                    
                    voice_file = speak(reply)
                    if voice_file and os.path.exists(voice_file):
                        send_voice(chat_id, voice_file)
                        os.remove(voice_file)

    except RequestException as e:
        print("⚠ Сеть:", e)
        time.sleep(5)
    except Exception as e:
        print("❌ Критическая ошибка:", e)
        time.sleep(5)
