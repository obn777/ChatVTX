# Путь к файлу: /root/NovBase/app.py

import os
import json
import subprocess
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string
from llama_cpp import Llama
from threading import Lock

app = Flask(__name__)
model_lock = Lock()

# --- ПУТИ И КОНФИГУРАЦИЯ ---
BASE_DIR = os.path.expanduser("~/NovBase")
DB_FILE = os.path.join(BASE_DIR, "users_db.json")
MAX_USERS = 100

# Параметры модели 8B
model_path = "/root/NovBase/models/Meta-Llama-3-8B-Instruct-Q6_K.gguf"
llm = Llama(model_path=model_path, n_ctx=4096, n_gpu_layers=-1, verbose=False)

chat_history = {} 
last_activity = {}

# --- ЛОГИКА БАЗЫ ДАННЫХ ---
def load_db():
    # Стандартная структура с поддержкой ключей доступа
    default_db = {
        "access_keys": {"2056": "Георгий (Admin)"}, 
        "names": {}, 
        "mail": {}
    }
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # Проверка на корректность структуры
                if not isinstance(data, dict) or "names" not in data:
                    return default_db
                if "access_keys" not in data:
                    data["access_keys"] = default_db["access_keys"]
                return data
        except:
            return default_db
    return default_db

def save_db(db_data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db_data, f, ensure_ascii=False, indent=4)

def get_local_geo(ip):
    if ip == "127.0.0.1": return "Localhost"
    try:
        res = subprocess.check_output(f"geoiplookup {ip}", shell=True).decode()
        return res.split(':')[-1].strip()
    except: return "Unknown"

# --- ДИЗАЙН АДМИНКИ ---
ADMIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Hub Monitor</title>
    <style>
        body { background: #0a0a0a; color: #00ff41; font-family: monospace; padding: 20px; }
        .panel { border: 1px solid #00ff41; padding: 20px; box-shadow: 0 0 15px #00ff41; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { border: 1px solid #00441a; padding: 10px; text-align: left; }
        th { background: #00220d; }
    </style>
</head>
<body>
    <div class="panel">
        <h1>[ NETWORK HUB: ACTIVE ]</h1>
        <p>Всего пользователей: {{ db_size }} | Активных ключей: {{ keys_count }}</p>
        <table>
            <tr><th>ИМЯ (ВЛАДЕЛЕЦ КЛЮЧА)</th><th>РЕГИОН</th><th>ПОСЛЕДНЕЕ</th><th>ВРЕМЯ</th></tr>
            {% for uid, info in activity.items() %}
            <tr>
                <td><strong>{{ info.name }}</strong></td>
                <td>{{ info.geo }}</td>
                <td>{{ info.msg }}</td>
                <td>{{ info.time }}</td>
            </tr>
            {% endfor %}
        </table>
    </div>
</body>
</html>
"""

@app.route('/')
def health(): return "SYSTEM ONLINE", 200

@app.route('/admin')
def admin():
    current_db = load_db()
    return render_template_string(
        ADMIN_HTML, 
        db_size=len(current_db.get("names", {})), 
        keys_count=len(current_db.get("access_keys", {})),
        activity=last_activity
    )

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    # Получаем реальный IP
    user_id = request.headers.get('X-Forwarded-For', request.remote_addr)
    text = data.get("text", "").strip()
    
    current_db = load_db()
    allowed_keys = current_db.get("access_keys", {})

    # 1. ПРОВЕРКА КЛЮЧА АРЕНДЫ
    client_key = request.headers.get('X-API-Key') or data.get('key')
    if client_key not in allowed_keys:
        return jsonify({
            "reply": "Доступ ограничен. Неверный ключ аренды.",
            "status": "unauthorized"
        })

    key_owner = allowed_keys[client_key]

    # 2. РЕГИСТРАЦИЯ ИМЕНИ
    if text.lower().startswith("я "):
        new_name = text[2:].strip()
        current_db["names"][user_id] = new_name
        save_db(current_db)
        return jsonify({"reply": f"Принято! {new_name}, ты используешь доступ: {key_owner}.", "status": "success"})

    current_name = current_db["names"].get(user_id)
    if not current_name:
        return jsonify({"reply": f"Привет! Я Малышка. (Доступ: {key_owner}). Представься: 'Я [Имя]'"})

    # ОБНОВЛЕНИЕ МОНИТОРИНГА
    last_activity[user_id] = {
        "name": f"{current_name} ({key_owner})",
        "geo": get_local_geo(user_id),
        "msg": text[:50],
        "time": datetime.now().strftime("%H:%M:%S")
    }

    # 3. ГЕНЕРАЦИЯ (Llama-3 8B)
    with model_lock:
        if user_id not in chat_history:
            chat_history[user_id] = []
        
        chat_history[user_id].append({"role": "user", "content": text})
        chat_history[user_id] = chat_history[user_id][-8:]

        prompt = "<|begin_of_text|>"
        for msg in chat_history[user_id]:
            prompt += f"<|start_header_id|>{msg['role']}<|end_header_id|>\n\n{msg['content']}<|eot_id|>"
        prompt += "<|start_header_id|>assistant<|end_header_id|>\n\n"

        output = llm(prompt, max_tokens=450, stop=["<|eot_id|>"], stream=False)
        full_reply = output['choices'][0]['text'].strip()
        
        chat_history[user_id].append({"role": "assistant", "content": full_reply})

        return jsonify({
            "reply": full_reply,
            "status": "success"
        })

if __name__ == '__main__':
    if not os.path.exists(BASE_DIR): os.makedirs(BASE_DIR)
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
