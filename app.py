import os
import sys
import asyncio
import datetime
from flask import Flask, request, jsonify, render_template
from threading import Lock

# ===== Core Imports =====
from core.cognition.controller import CognitionController
from core.memory.memory_manager import MemoryManager
from core.engine.model_engine import ModelEngine
from core.logic_processor import LogicProcessor
from core.dispatcher import MemoryDispatcher
from core.memory.sanitizer import CacheSanitizer
from core.backup_manager import BackupManager
from core.action_executor import ActionExecutor
from core.behavior.mode_manager import ModeManager

# Voice engine (опционально)
try:
    from core.tts.voice_engine import voice
except Exception:
    voice = None


# ==========================================
# Flask Setup
# ==========================================

app = Flask(__name__)
model_lock = Lock()

BASE_DIR = "/home/obn7/NovBase"
MODEL_PATH = "/home/obn7/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
MM_PROJ_PATH = "/home/obn7/models/mmproj-model-f16.gguf"

if not os.path.exists(MODEL_PATH):
    print(f"❌ Модель не найдена: {MODEL_PATH}")
    sys.exit(1)


# ==========================================
# Async Loop
# ==========================================

def get_safe_loop():
    try:
        return asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop

loop = get_safe_loop()


# ==========================================
# Initialization
# ==========================================

print("🚀 Инициализация NovBase...")

bm = BackupManager()
bm.create_backup()

memory = MemoryManager()
logic = LogicProcessor()
sanitizer = CacheSanitizer()
executor = ActionExecutor()
mode_manager = ModeManager()

# ВАЖНО: синхронизируем mode_manager внутри logic
logic.mode_manager = mode_manager

dispatcher_path = os.path.join(BASE_DIR, "storage/cache.json")
dispatcher = MemoryDispatcher(cache_path=dispatcher_path)

engine = ModelEngine(
    model_path=MODEL_PATH,
    mmproj_path=MM_PROJ_PATH
)

# Фоновая очистка
loop.create_task(sanitizer.run_periodic_cleanup(interval_hours=24))


# ==========================================
# Headers
# ==========================================

@app.after_request
def add_header(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# ==========================================
# Routes
# ==========================================

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/status")
def status():
    return jsonify({
        "status": "online",
        "engine": "Llama-3.1-8B",
        "voice_active": getattr(voice, "current_mode", "disabled"),
        "mode": mode_manager.get_mode_name(),
        "time": datetime.datetime.now().isoformat()
    })


@app.route("/stop", methods=["POST"])
def stop_speech():
    if voice:
        voice.stop()
    return jsonify({"status": "stopped"})


@app.route("/chat", methods=["POST"])
def chat():

    data = request.json or {}
    text = data.get("text", "").strip()
    client_key = data.get("key", "")
    voice_enabled = data.get("voice_enabled", True)

    # Безопасность
    if client_key != "2056":
        return jsonify({"reply": "Доступ ограничен."})

    if not text:
        return jsonify({"reply": "Запрос пуст."})

    # Остановка речи при выключении
    if not voice_enabled and voice:
        voice.stop()

    # ==================================
    # Logic Layer
    # ==================================

    logic_res = loop.run_until_complete(
        logic.process_message(text)
    )

    if logic_res["processed"]:
        final_reply = logic.sanitize_output(logic_res["result"])

        if voice_enabled and voice:
            voice.speak(final_reply)

        return jsonify({"reply": final_reply})

    # ==================================
    # Cache Layer
    # ==================================

    cached_reply = dispatcher.get_valid_cache(text)
    if cached_reply:
        final_reply = logic.sanitize_output(cached_reply)

        if voice_enabled and voice:
            voice.speak(final_reply)

        return jsonify({"reply": final_reply, "status": "from_cache"})

    # ==================================
    # Mode Detection
    # ==================================

    mode_manager.auto_detect_mode(text)

    # ==================================
    # LLM Generation
    # ==================================

    formatted_history = ""

    with model_lock:
        hist_path = os.path.join(BASE_DIR, "storage/history.json")
        mem_data = memory._load_json(hist_path)

        history_list = mem_data.get("history", []) if isinstance(mem_data, dict) else []

        for entry in history_list[-3:]:
            if isinstance(entry, dict):
                q = entry.get("q", "")
                a = entry.get("a", "")
                formatted_history += f"<|user|>{q}<|end|><|assistant|>{a}<|end|>"

        base_prompt = logic.prompt_manager.format_prompt(
            text,
            history=formatted_history
        )

        full_reply = engine.get_answer(base_prompt)

    # ==================================
    # Post Processing
    # ==================================

    clean_reply = logic.sanitize_output(full_reply)

    saved_path = executor.execute(
        logic_res.get("cognition", {}),
        clean_reply
    )

    if saved_path:
        filename = os.path.basename(saved_path)
        clean_reply += f"\n\n[Файл сохранён: {filename}]"

    if hasattr(memory, "save_to_history"):
        memory.save_to_history(text, clean_reply)

    dispatcher.process_entry(text, clean_reply)

    if voice_enabled and voice:
        voice.speak(clean_reply)
    elif voice:
        voice.stop()

    return jsonify({
        "reply": clean_reply,
        "status": "success",
        "mode": mode_manager.get_mode_name()
    })


# ==========================================

if __name__ == "__main__":
    print("🚀 NovBase запущен на 8080.")
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=False,
        threaded=True
    )
