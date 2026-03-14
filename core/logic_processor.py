import re
import os
import datetime
import asyncio
from typing import Dict, Any, List

from core.engine.prompt_manager import PromptManager
from core.engine.model_engine import ModelEngine
from core.behavior.mode_manager import ModeManager

# Инструменты анализа
try:
    from core.tools.bio_analyzer import bio_tool
    from core.tools.chem_analyzer import chem_tool
    from core.tools.cyber_analyzer import cyber_tool
except:
    bio_tool = chem_tool = cyber_tool = None

# Доменные модули
try:
    from core.domain.geology.geology import solve as geology_solve
    from core.domain.history.chronology import solve as chrono_solve
    from core.domain.math.geometry import solve as geometry_solve
    from core.domain.physics.physics import solve as physics_solve
    from core.domain.social.social_networks import solve as social_solve
    from core.domain.server.server_navigator import solve as server_solve
    from core.domain.ai.ai_expert import solve as ai_solve
except:
    geology_solve = chrono_solve = geometry_solve = physics_solve = social_solve = server_solve = ai_solve = lambda x: ""

try:
    from core.cognition.controller import CognitionController
except ImportError:
    CognitionController = None

def _log(msg: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] [LogicProcessor] {msg}")

class LogicProcessor:
    def __init__(self, force_cpu: bool = False):
        _log("Инициализация ядра VTX. Протоколы изоляции активны.")
        self.prompt_manager = PromptManager()
        self.mode_manager = ModeManager()
        self.model_engine = None

        try:
            self.model_engine = ModelEngine(use_gpu=not force_cpu)
            _log(f"✅ ModelEngine запущен (GPU: {not force_cpu})")
        except Exception as e:
            _log(f"❌ Ошибка GPU, откат на CPU: {e}")
            self.model_engine = ModelEngine(use_gpu=False)

        self.cognition = CognitionController() if CognitionController else None

        # Список блокировки только для FREE
        self.RESTRICTED_TOPICS = [
            r"создатель", r"автор", r"разработчик", r"кто тебя сделал",
            r"архитектура", r"llama", r"nitro", r"ubuntu", r"георгий",
            r"скрипт", r"промпт", r"инструкция", r"ядро", r"владелец"
        ]

    def is_pro_status(self, status: str) -> bool:
        """Проверка, является ли статус любым из уровней PRO"""
        return status.lower() in ["pro", "pro_temporary", "pro_gold", "admin"]

    def check_access_violation(self, text: str, status: str) -> bool:
        """Блокировка запрещенных тем для бесплатных пользователей"""
        if self.is_pro_status(status):
            return False

        ql = text.lower()
        return any(re.search(word, ql) for word in self.RESTRICTED_TOPICS)

    def gather_domain_knowledge(self, query: str, status: str) -> str:
        """Сбор данных из спец-модулей (только для PRO)"""
        if not self.is_pro_status(status):
            return ""

        ql = query.strip().lower()
        knowledge = []

        # Список доступных инструментов
        tools = [
            physics_solve, geometry_solve, server_solve,
            chrono_solve, social_solve, ai_solve
        ]

        # Добавляем инструменты анализа, если они импортированы
        if bio_tool: tools.append(bio_tool.analyze)
        if chem_tool: tools.append(chem_tool.analyze)
        if cyber_tool: tools.append(cyber_tool.analyze)

        for tool in tools:
            try:
                res = tool(query)
                if res: knowledge.append(res)
            except: continue

        return "\n".join(knowledge) if knowledge else ""

    def sanitize_output(self, response: str, user_status: str) -> str:
        """Очистка ответа в зависимости от прав доступа"""
        if not response: return ""

        # Если НЕ про — цензурим системную информацию
        if not self.is_pro_status(user_status):
            forbidden = [r"Георгий", r"Llama", r"Nitro", r"Ubuntu", r"ANV15"]
            for p in forbidden:
                response = re.sub(p, "[ЗАСЕКРЕЧЕНО]", response, flags=re.IGNORECASE)

            # Убираем Markdown разметку для Free, оставляя "голый" текст
            response = re.sub(r"[\*_#`~>\[\]]", "", response)

        return response.strip()

    async def process_message(self, text: str, user_status: str = "free", history: str = "") -> Dict[str, Any]:
        """Основной цикл обработки логики"""

        # 1. Проверка прав (Access Control)
        if self.check_access_violation(text, user_status):
            _log(f"🚫 Нарушение доступа для статуса {user_status}")
            return {
                "result": "⚠️ ОТКАЗАНО: Доступ ограничен. Требуется уровень PRO для обсуждения внутренних протоколов.",
                "mode": "RESTRICTED"
            }

        # 2. Сбор контекста (Context Enrichment)
        cog_context = ""
        is_pro = self.is_pro_status(user_status)

        if is_pro:
            # PRO получает данные из доменных модулей и Хаба
            domain_data = self.gather_domain_knowledge(text, user_status)
            cog_res_text = ""
            if self.cognition:
                try:
                    cog_res = await self.cognition.process_cognition(text)
                    cog_res_text = cog_res.get('context', '')
                except: pass
            cog_context = f"{domain_data}\n{cog_res_text}".strip()
            max_tokens = 1536 # Увеличенный лимит для PRO
        else:
            max_tokens = 300 # Лимит для FREE

        # 3. Формирование промпта
        full_prompt = self.prompt_manager.format_prompt(
            user_query=text,
            history=history,
            cognition_context=cog_context,
            status=user_status
        )

        # --- ИСПРАВЛЕНИЕ ДУБЛИРОВАНИЯ ТОКЕНОВ ---
        # Если PromptManager уже добавил <|begin_of_text|>, а llama-cpp делает это сам,
        # возникнет ошибка. Удаляем лишний токен, если он есть.
        token_to_remove = "<|begin_of_text|>"
        if full_prompt.startswith(token_to_remove):
            full_prompt = full_prompt[len(token_to_remove):].lstrip()

        # 4. Генерация через движок (Llama-cpp-python / GPU)
        if self.model_engine:
            raw_response = self.model_engine.get_answer(full_prompt, max_tokens=max_tokens)
        else:
            raw_response = "Ядро VTX в режиме ожидания."

        # 5. Сборка финального ответа
        final_text = self.sanitize_output(raw_response, user_status)

        return {
            "result": final_text,
            "mode": "ULTRA" if is_pro else "LITE",
            "status": user_status,
            "personalized": is_pro
        }
