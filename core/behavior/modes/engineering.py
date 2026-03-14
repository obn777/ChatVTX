from .base_mode import BaseMode

class EngineeringMode(BaseMode):
    """
    Режим инженерного синтеза. 
    Фокус на создании чистого кода, алгоритмов и технической документации.
    """
    def __init__(self):
        super().__init__()
        self.mode_name = "ENGINEERING"
        self.instruction = (
            "ИНСТРУКЦИЯ РЕЖИМА [ENGINEERING]:\n"
            "1. ПРИОРИТЕТ: Чистота кода, типизация (Python hints) и модульность.\n"
            "2. СТРУКТУРА: Всегда указывай файловые пути согласно архитектуре NovBase.\n"
            "3. БЕЗОПАСНОСТЬ: Исключай уязвимости и избыточные зависимости.\n"
            "4. КОНТЕКСТ: Учитывай, что работа ведется на модели 8B (ограничение VRAM 6GB).\n"
            "5. ФОРМАТ: Код должен быть готов к копированию (Markdown-блоки)."
        )

    def modify_prompt(self, prompt: str) -> str:
        """
        Перевод модели в состояние прикладного разработчика.
        """
        clean_input = prompt.strip()
        
        # Инъекция инженерного фрейма
        engineering_frame = (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"CURRENT_COGNITIVE_MODE: {self.mode_name}\n"
            f"{self.instruction}\n"
            f"PROJECT_ROOT: /home/obn7/NovBase\n"
            f"<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"TECHNICAL_TASK: {clean_input}\n"
            f"EXECUTE_ENGINEERING_SYNTHESIS.<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
        
        return engineering_frame

    def get_description(self) -> str:
        return "Режим разработки: генерация кода, проектирование систем и тех-дизайн."
