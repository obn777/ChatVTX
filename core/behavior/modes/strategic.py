from .base_mode import BaseMode

class StrategicMode(BaseMode):
    """
    Режим стратегического планирования и визионерства.
    Цель: масштабирование, долгосрочное развитие и системная интеграция.
    """
    def __init__(self):
        super().__init__()
        self.mode_name = "STRATEGIC"
        self.instruction = (
            "ИНСТРУКЦИЯ РЕЖИМА [STRATEGIC]:\n"
            "1. МАСШТАБ: Смотри на проблему в контексте всей системы NovBase и её будущего.\n"
            "2. РЕСУРСЫ: Учитывай ограничения железа (VRAM 6GB) как стратегический лимит.\n"
            "3. ВЕКТОР 2026: Ориентируйся на тренды автономных ИИ-агентов и локальных LLM.\n"
            "4. ЭКОСИСТЕМА: Ищи способы синергии между модулями (Memory, Engine, Vision).\n"
            "5. РЕЗУЛЬТАТ: Дорожная карта, этапы реализации и оценка долгосрочных рисков."
        )

    def modify_prompt(self, prompt: str) -> str:
        """
        Перевод модели в состояние архитектора-стратега.
        """
        clean_input = prompt.strip()
        
        # Инъекция стратегического фрейма
        strategic_frame = (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"CURRENT_COGNITIVE_MODE: {self.mode_name}\n"
            f"{self.instruction}\n"
            f"STRATEGIC_TIMELINE: 2026\n"
            f"<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"STRATEGIC_OBJECTIVE: {clean_input}\n"
            f"EXECUTE_VISIONARY_PLANNING.<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        
        return strategic_frame

    def get_description(self) -> str:
        return "Режим стратега: долгосрочное планирование, архитектурное видение и развитие."
