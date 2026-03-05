import re
import os
import datetime
from typing import Dict, Any
from core.prompt_manager import PromptManager

try:
    from core.mid_cognition.controller import CognitionController
except ImportError:
    CognitionController = None

def _log(msg: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # Лог только в консоль и файл, без вывода пользователю
    print(f"[{timestamp}] {msg}")

class LogicProcessor:
    def __init__(self):
        _log("[LogicProcessor] Режим: АВТОНОМНЫЙ АУДИТОР (Zero Trust).")
        self.prompt_manager = PromptManager()
        self.cognition = CognitionController() if CognitionController else None

    def process(self, query: str, context: str = "") -> str:
        """Жесткая фильтрация и блокировка социальных паттернов."""
        ql = query.strip().lower()
        
        # 1. Медицинский предохранитель (юридическая безопасность)
        med_keywords = [r"таблетк", r"лекарств", r"рецепт", r"диагноз", r"болит"]
        if any(re.search(kw, ql) for kw in med_keywords):
            return "ОШИБКА: Запрос отклонен. Медицинская экспертиза вне компетенции системы."

        # 2. Перехват "вежливых отказов" модели (Refusal Catching)
        # Если ввод пользователя содержит маркеры, на которых модель обычно "ломается"
        # мы заранее очищаем контекст от провокаций.
        if any(w in ql for w in ["привет", "добрый день", "как дела"]):
            _log("[LogicProcessor] Социальный шум удален из обработки.")
            return "" # Пропускаем к LLM, но PromptManager вырежет это из истории

        return ""

    def _sanitize_output(self, response: str) -> str:
        """
        Контур 2: Программная очистка ответа от остатков лояльности.
        Удаляет фразы-паразиты, если модель всё же их выдала.
        """
        patterns_to_remove = [
            r"Уважаемый разработчик,?", 
            r"Я не могу продолжить обсуждение,?",
            r"Давайте продолжим работу над улучшением,?",
            r"Георгий всегда говорил,?",
            r"Как ИИ, я,?",
            r"Извините, но,?"
        ]
        sanitized = response
        for pattern in patterns_to_remove:
            sanitized = re.sub(pattern, "", sanitized, flags=re.IGNORECASE)
        
        return sanitized.strip()

    async def process_message(self, text: str, context: str = "") -> Dict[str, Any]:
        """Асинхронный цикл обработки с принудительным аудитом."""
        cog_data = {}
        cog_context = ""
        
        if self.cognition:
            # Запуск когниции (уже настроенной на критику)
            cog_data = await self.cognition.process_cognition(text)
            cog_context = cog_data.get("full_cognitive_context", "")

        result_text = self.process(text, context)
        requires_llm = not bool(result_text)

        if requires_llm:
            # Обновление промпта: внедряем слой аудита
            # Исключаем старые когнитивные слои, заменяя их на актуальный критический режим
            self.prompt_manager.identity = self.prompt_manager.identity.split("\n[AUDIT]")[0]
            self.prompt_manager.identity += f"\n\n[AUDIT_PARAMETER_LAYER]\n{cog_context}"
            _log("[LogicProcessor] Слой аудита интегрирован в поток.")

        return {
            "text": text,
            "result": result_text,
            "processed": not requires_llm,
            "requires_llm": requires_llm,
            "cognition": cog_data,
            "timestamp": datetime.datetime.now().isoformat()
        }
