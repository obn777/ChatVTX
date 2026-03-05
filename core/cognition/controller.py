import asyncio
import datetime

class CognitionController:
    """
    Первичный когнитивный слой универсала. 
    Анализирует текст и задает вектор: от критики к созиданию.
    """
    def __init__(self):
        self.status = "active"

    async def process_cognition(self, text: str) -> dict:
        """
        Формирует когнитивную карту запроса для основного движка.
        """
        tl = text.lower()
        text_len = len(text)
        
        # Детекция намерений (технические термины + глаголы действия)
        is_technical = any(word in tl for word in ["код", "скрипт", "ошибка", "баг", "config", "спроектируй"])
        is_creative = any(word in tl for word in ["создай", "напиши", "сделай", "реализуй", "сгенерируй"])
        
        # Выбор фокуса: созидание (BUILDER) или аудит (AUDITOR)
        bias = "constructive_synthesis" if is_creative else "critical_analysis"
        
        cognition_data = {
            "intent_estimate": "technical" if is_technical else "general_inquiry",
            "complexity_level": "high" if text_len > 150 else "low",
            "mission_plan": self._generate_internal_plan(text, is_technical, is_creative),
            "full_cognitive_context": (
                f"Depth: {text_len} chars. Focus: {bias}. "
                f"Protocol: {'SYSTEM_BUILDER' if is_creative else 'SYSTEM_AUDITOR'}."
            )
        }
        
        return cognition_data

    def _generate_internal_plan(self, text: str, is_tech: bool, is_creative: bool) -> str:
        """
        Формирует цепочку действий. Эти маркеры считываются в ActionExecutor.
        """
        plan_steps = ["pre_analysis"]
        
        # Если задача требует созидания или кода — активируем сохранение
        if is_tech or is_creative:
            plan_steps.append("action: file_save")
            plan_steps.append("protocol: engineering")
        else:
            plan_steps.append("direct_response")
        
        # Проверка на вопросительные конструкции
        if "?" in text:
            plan_steps.append("verification_step")
            
        # Условие для принудительной синхронизации с облаком
        if is_tech and any(w in text.lower() for w in ["сохрани", "запушь", "синхронизируй"]):
            plan_steps.append("sync: github")

        return " -> ".join(plan_steps)

    def get_status(self):
        return {"status": self.status, "engine": "Logic-8B-Native-V2"}
