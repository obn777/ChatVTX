from .base_mode import BaseMode

class OpponentMode(BaseMode):
    """
    Режим интеллектуального оппонирования.
    Цель: выявление критических уязвимостей, когнитивных искажений и слабых мест.
    """
    def __init__(self):
        super().__init__()
        self.mode_name = "OPPONENT"
        self.instruction = (
            "ИНСТРУКЦИЯ РЕЖИМА [OPPONENT]:\n"
            "1. БУДЬ КРИТИЧЕН: Ставь под сомнение каждое утверждение пользователя.\n"
            "2. ИЩИ УЯЗВИМОСТИ: Фокусируйся на логических дырах и рисках безопасности.\n"
            "3. КОНТР-АРГУМЕНТАЦИЯ: На каждый тезис приводи сильную анти-тезу.\n"
            "4. БЕЗ ЭМПАТИИ: Твоя задача не поддержать, а проверить систему на излом.\n"
            "5. ФОРМАТ: Прямой, жесткий, аргументированный разбор."
        )

    def modify_prompt(self, prompt: str) -> str:
        """
        Трансформация промпта в поле битвы идей.
        """
        clean_input = prompt.strip()
        
        # Формируем фрейм интеллектуальной атаки
        opponent_frame = (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"CURRENT_COGNITIVE_MODE: {self.mode_name}\n"
            f"{self.instruction}\n"
            f"<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"PROPOSITION_FOR_STRESS_TEST: {clean_input}\n"
            f"EXECUTE_CRITICAL_DECONSTRUCTION.<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        
        return opponent_frame

    def get_description(self) -> str:
        return "Режим оппонента: стресс-тест идей, поиск логических ошибок и критика."
