from .base_mode import BaseMode


class AnalyticMode(BaseMode):
    """
    Режим строгого системного анализа.
    Предназначен для структурированного, логически выверенного ответа
    без эмоциональной окраски и без агрессивной деконструкции.
    """

    def __init__(self):
        super().__init__()
        self.mode_name = "ANALYTIC"

        self.instruction = (
            "ИНСТРУКЦИЯ РЕЖИМА [ANALYTIC]:\n"
            "1. Применяй декомпозицию: разбивай проблему на логические блоки.\n"
            "2. Выявляй причинно-следственные связи.\n"
            "3. Убирай лишние допущения (принцип бритвы Оккама).\n"
            "4. Формируй структурированный вывод.\n"
            "5. Если запрос краткий или неопределённый — уточни его, а не проводи аудит."
        )

    def modify_prompt(self, prompt: str) -> str:
        """
        Внедрение аналитического фрейма без агрессивной аудиторской логики.
        """

        clean_input = prompt.strip()

        analytic_frame = (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"CURRENT_MODE: {self.mode_name}\n"
            f"{self.instruction}\n"
            f"<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"REQUEST:\n{clean_input}\n"
            f"<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )

        return analytic_frame

    def get_description(self) -> str:
        return "Структурированный аналитический режим без агрессивной деконструкции."
