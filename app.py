import os
import sys
import asyncio
import datetime
import json
import threading
import re
import time
from flask import Flask, request, jsonify, render_template, send_from_directory
from threading import Lock

# ==================================================
# Core & Auth Imports
# ==================================================
try:
    from core.logic_processor import LogicProcessor
    from core.auth_manager import AuthManager
    from core.mailer import send_vtx_key
    from core.personal_hub.manager import PersonalHubManager
    from bot import run_bot
except Exception as e:
    print(f"⚠️ Core modules error: {e}")

# ==================================================
# Flask Setup
# ==================================================
app = Flask(__name__)
app.secret_key = "vtx_core_secure_session_key"

# Мощный Lock для предотвращения коллизий в видеопамяти RTX 3050
model_lock = Lock()

BASE_DIR = "/home/obn7/NovBase"

# Глобальные объекты (инициализируются в блоке __main__)
logic = None
auth = None
hub = None
loop = None

# Глобальный список доверенных ID
ADMIN_DEVICES = ["f64705573428989a"]

# ==================================================
# INTERNAL BOT THREAD
# ==================================================
def start_vtx_bot():
    """Запуск Telegram-бота с передачей GPU-ядра"""
    try:
        # ПЕРЕДАЕМ объект logic, чтобы бот не запускал свою CPU-версию
        run_bot(shared_logic=logic)
    except Exception as e:
        print(f"⚠️ [SYSTEM]: Ошибка в работе бота: {e}")

# ==================================================
# PUBLIC API ROUTES
# ==================================================

@app.route("/")
def index():
    """Главная страница (Лендинг)"""
    return render_template("landing.html")

@app.route("/terminal")
def terminal():
    """Интерфейс чата в браузере"""
    return render_template("index.html")

@app.route("/chat", methods=["GET", "POST"])
def chat():
    if request.method == "GET":
        return "Система VTX активна. Ожидаю POST-запросы.", 200

    try:
        data = request.get_json()
        if not data: return jsonify({"reply": "Пустой запрос."}), 400

        raw_text = data.get("text", "")
        u_name = data.get("name", "User")
        u_key = data.get("key", "").strip()
        u_uid = data.get("uid", "").strip()
        u_ip = request.remote_addr

        print(f"\n[REQ] {u_name} | UID: {u_uid} | Key: {u_key}")

        # Проверка админа
        is_admin = (u_uid in ADMIN_DEVICES) or (u_key == "7777")

        if is_admin:
            allowed, status = True, "Admin"
        else:
            allowed, status = auth.check_access(u_ip, u_name, u_key)

        if not allowed:
            return jsonify({"reply": "Доступ ограничен. Введите ключ активации.", "mode": "Free"})

        # Контекст и персонализация
        current_id = "admin_georgiy" if is_admin else (u_key if u_key else u_ip)
        dynamic_prompt = hub.get_dynamic_prompt(current_id) if hub else ""

        # Генерация через ЕДИНОЕ ядро с защитой Lock
        with model_lock:
            res = loop.run_until_complete(logic.process_message(
                text=raw_text, user_status=status, history=dynamic_prompt
            ))
            reply = res.get("result", "...")
            if hub and current_id:
                hub.update_client_data(current_id, raw_text, reply)

        return jsonify({"reply": reply, "mode": status, "personalized": True})

    except Exception as e:
        print(f"🚨 Chat Error: {e}")
        return jsonify({"reply": "Ошибка ядра VTX."}), 500

# ==================================================
# UTILS & ADMIN
# ==================================================

@app.route("/api/admin/stats")
def admin_stats():
    return jsonify(auth.users)

@app.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json()
        email = data.get("email", "").strip()
        if not email: return jsonify({"success": False}), 400
        new_key = auth.approve_key(email)
        # Отправка письма в отдельном потоке
        threading.Thread(target=send_vtx_key, args=(email, "User", new_key), daemon=True).start()
        return jsonify({"success": True})
    except: return jsonify({"success": False}), 500

@app.route("/static/<path:filename>")
def serve_static(filename):
    return send_from_directory(os.path.join(BASE_DIR, "static"), filename)

# ==================================================
# MAIN EXECUTION
# ==================================================
if __name__ == "__main__":
    # 1. Подготовка асинхронного цикла
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    # 2. Инициализация ядра (СТРОГО ОДИН РАЗ)
    logic = LogicProcessor() # Здесь захватывается GPU
    auth = AuthManager(BASE_DIR)
    hub = PersonalHubManager(BASE_DIR)

    print("✅ Системы VTX синхронизированы (Single Core Mode)")

    # 3. Запуск Telegram-бота (теперь он использует 'logic' на GPU)
    bot_thread = threading.Thread(target=start_vtx_bot, daemon=True)
    bot_thread.start()

    print("🤖 [SYSTEM]: Telegram Bot инициирован с общим ядром.")
    print("🚀 Малышка VTX готова. Слушаю порт 8080...")

    # 4. Запуск веб-сервера (без релоадера, чтобы не плодить процессы)
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False,
        use_reloader=False,
        threaded=True
    )
