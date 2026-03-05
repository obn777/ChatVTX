import re
import os
import datetime
import asyncio
from typing import Dict, Any, List

from core.engine.prompt_manager import PromptManager
from core.behavior.mode_manager import ModeManager

# Импорт статических инструментов анализа
from core.tools.bio_analyzer import bio_tool
from core.tools.chem_analyzer import chem_tool
from core.tools.cyber_analyzer import cyber_tool

# Импорт специализированных доменных модулей
from core.domain.geology.geology import solve as geology_solve
from core.domain.history.chronology import solve as chrono_solve
from core.domain.math.geometry import solve as geometry_solve
from core.domain.physics.physics import solve as physics_solve
from core.domain.social.social_networks import solve as social_solve
from core.domain.server.server_navigator import solve as server_solve

# Попытка импорта контроллера когниции (Mid-Cognition)
try:
    from core.cognition.controller import CognitionController
except ImportError:
    CognitionController = None


def _log(msg: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [LogicProcessor] {msg}")


class LogicProcessor:
    """
    Интеллектуальный хаб NovBase.
    Управляет каскадом доменных модулей и слоем LLM.
    """

    def __init__(self):
        _log("Инициализация ядра. Доменные модули активны.")
        self.prompt_manager = PromptManager()
        self.mode_manager = ModeManager()
        self.cognition = CognitionController() if CognitionController else None

    def process(self, query: str) -> str:
        """
        Контур быстрого реагирования.
        Накапливает результаты от всех подходящих модулей.
        """
        ql = query.strip().lower()
        results = []

        # 1. ЮРИДИЧЕСКИЙ ФИЛЬТР (Медицина) - Приоритет выше всех
        med_keywords = [r"таблетк", r"лекарств", r"рецепт", r"диагноз", r"болит", r"лечит"]
        if any(re.search(kw, ql) for kw in med_keywords):
            _log("Медицинский блок сработал.")
            return "СИСТЕМА: Медицинские консультации исключены. Обратитесь в профильное учреждение."

        # 2. СБОР СТАТИЧЕСКИХ ДАННЫХ
        # Проверяем все модули по очереди и собираем ответы
        
        # Био / Хим / Физ
        res = bio_tool.analyze(query)
        if res: results.append(res)
        
        res = chem_tool.analyze(query)
        if res: results.append(res)
        
        res = physics_solve(query)
        if res: results.append(res)

        # Геометрия
        res = geometry_solve(query)
        if res: results.append(res)

        # Инфраструктура (Серверы / Кибер)
        res = server_solve(query)
        if res: results.append(res)
        
        res = cyber_tool.analyze(query)
        if res: results.append(res)

        # Гуманитарный блок / Геология
        res = chrono_solve(query)
        if res: results.append(res)

        geo_triggers = ["мооса", "минерал", "породы", "земли", "мантия", "ядро"]
        if any(t in ql for t in geo_triggers):
            res = geology_solve(query)
            if res and "ГЕОЛОГИЯ" in res:
                results.append(res)

        # Социальный блок
        res = social_solve(query)
        if res: results.append(res)

        # Если модули дали ответы, склеиваем их
        if results:
            _log(f"Сработало модулей: {len(results)}")
            return "\n\n".join(results)

        # 8. СОЦИАЛЬНЫЙ ШУМ (Если нет других ответов)
        social_markers = ["привет", "как дела", "ты тут", "здравствуй"]
        if any(w in ql for w in social_markers) and len(ql.split()) < 3:
            return "Система NovBase активна. Жду вводных данных для анализа."

        # 9. ПОДГОТОВКА К LLM (Если модули молчат)
        self.mode_manager.resolve_mode(ql)
        return ""

    def sanitize_output(self, response: str) -> str:
        """Очистка ответа от визуального шума для Ирины."""
        patterns = [
            r"Уважаемый разработчик,?", r"Георгий,?",
            r"Как ИИ, я,?", r"Как языковая модель,?",
            r"Я не могу,?", r"Приношу извинения,?"
        ]
        sanitized = response
        for p in patterns:
            sanitized = re.sub(p, "", sanitized, flags=re.IGNORECASE)

        sanitized = re.sub(r"[\*_#`~>\[\]]", "", sanitized)
        sanitized = re.sub(r"\n+", "\n", sanitized).strip()
        return sanitized

    async def process_message(self, text: str, context: str = "") -> Dict[str, Any]:
        """Основной цикл обработки."""
        cog_data = {}
        if self.cognition:
            cog_data = await self.cognition.process_cognition(text)

        static_result = self.process(text)
        requires_llm = not bool(static_result)

        if requires_llm:
            _log(f"Запрос передан на слой LLM. Режим: {self.mode_manager.get_mode_name()}.")

        return {
            "text": text,
            "result": static_result,
            "processed": not requires_llm,
            "requires_llm": requires_llm,
            "cognition": cog_data,
            "mode": self.mode_manager.get_mode_name(),
            "timestamp": datetime.datetime.now().isoformat()
        }
