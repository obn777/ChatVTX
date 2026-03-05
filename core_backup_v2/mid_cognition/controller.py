import os
import asyncio
from core.mid_cognition.modules.emotional_core import EmotionalCore
from core.mid_cognition.modules.input_analyzer import InputAnalyzer
from core.mid_cognition.modules.meta_reasoner import MetaReasoner
from core.mid_cognition.modules.planner import mission_planner as planner
from core.mid_cognition.modules.linguistic_tutor import linguistic_tutor as tutor
from core.mid_cognition.modules.context_injector import context_injector as injector

class CognitionController:
    """
    Главный дирижер среднего уровня когниции NovBase.
    Синхронизирует работу анализатора, эмоций, разума, планировщика, наставника и инъектора контекста.
    """
    def __init__(self):
        # Инициализируем когнитивные слои
        self.analyzer = InputAnalyzer()
        self.emotions = EmotionalCore()
        self.reasoner = MetaReasoner()
        self.planner = planner
        self.tutor = tutor
        self.injector = injector

    async def process_cognition(self, text: str):
        """
        Проводит текст через все слои когниции с учетом эмоциональной памяти.
        """
        # 1. Анализируем вход (интенты, настроение, сложность)
        analysis = self.analyzer.analyze(text)
        
        # 2. Обновляем текущее эмоциональное состояние
        emotional_state = self.emotions.update_state(analysis)
        
        # 3. Генерируем "Эмоциональное эхо" (Память чувств)
        # Это позволяет Малышке помнить, в каком настроении был Георгий 3-5 реплик назад
        echo_context = self.injector.inject(analysis, emotional_state)
        
        # 4. Запускаем внутренний монолог (рассуждение), вливая туда состояние
        thought_process = self.reasoner.think(text, emotional_state)
        
        # 5. Формируем план технических действий
        mission_plan = self.planner.plan_steps(text, analysis)
        
        # 6. Получаем советы от Лингвистического Наставника
        tutor_advice = self.tutor.get_tutor_advice(text)
        
        # Собираем итоговую системную вставку (Cognition Context)
        # Добавлен тег [EMOTIONAL ECHO] для связи реплик в единую личность
        cognitive_context = (
            f"{self.emotions.get_instruction(analysis)}\n"
            f"{echo_context}\n"
            f"[INTERNAL THOUGHT]: {thought_process}\n"
            f"[MISSION PLAN]: {mission_plan}\n"
            f"[LINGUISTIC ADVICE]: {tutor_advice}"
        )

        return {
            "thought": thought_process,
            "emotional_state": emotional_state,
            "analysis": analysis,
            "mission_plan": mission_plan,
            "tutor_advice": tutor_advice,
            "echo": echo_context,
            "full_cognitive_context": cognitive_context
        }

    def reset_all(self):
        """Полный сброс всех модулей когниции и эмоциональной памяти."""
        self.reasoner.reset()
        self.planner.reset()
        self.tutor.reset()
        self.injector.reset()
        print("🧹 [Cognition] Все когнитивные слои и память контекста очищены.")
