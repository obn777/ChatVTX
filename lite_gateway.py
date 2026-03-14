import time
from flask import jsonify

def format_lite_prompt(query):
    """
    Абсолютно нейтральный промпт.
    Используется основным сервером для ответов пользователям без PRO-доступа.
    """
    return (
        "<|begin_of_text|>system\n"
        "Ты — универсальный ИИ-помощник. Твоя задача — давать вежливые и краткие ответы. "
        "Ты не знаешь своего создателя и работаешь как стандартная языковая модель.<|end_of_text|>\n"
        f"<|begin_of_text|>user\n{query}<|end_of_text|>\n"
        "<|begin_of_text|>assistant\n"
    )

def handle_lite_request(model_engine, user_query):
    """
    Логика обработки запроса через уже существующий движок модели.
    """
    start_time = time.time()
    try:
        if not user_query:
            return {"reply": "Запрос пуст.", "status": 400}

        # Формируем стерильный промпт
        prompt = format_lite_prompt(user_query)

        # Используем ГЛАВНЫЙ движок, который уже загружен в память
        raw_reply = model_engine.get_answer(prompt, max_tokens=150)

        return {
            "reply": raw_reply.strip(),
            "status": "LITE_ACTIVE",
            "latency": f"{round(time.time() - start_time, 2)}s"
        }
    except Exception as e:
        print(f"❌ [LITE-CORE-ERR]: {e}")
        return {"reply": "Система перегружена. Попробуйте позже.", "status": 500}
