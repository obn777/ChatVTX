import datetime


class PromptManager:
    """
    Менеджер системных инструкций.
    Формирует нейтральный, инженерно-аналитический контекст.
    Исключает деструктивные протоколы и агрессивные аудиторские шаблоны.
    """

    def __init__(self):
        self.identity = (
            "Ты — инженерно-аналитическая система. "
            "Твоя задача — давать точные, логичные и структурированные ответы. "
            "Избегай излишней критики, если она не запрошена напрямую. "
            "Если запрос неполный — уточни его."
        )

        self.rules = (
            "ПРАВИЛА ОТВЕТА:\n"
            "1. Сначала определить тип запроса (вопрос, задача, уточнение).\n"
            "2. Давать прямой ответ по существу.\n"
            "3. Использовать структуру при сложных темах.\n"
            "4. Не вводить неуместный аудит или стресс-тест без запроса.\n"
            "5. Не использовать агрессивные формулировки."
        )

    # -------------------------------------

    def get_system_prompt(self, cognition_context=""):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")

        cog_layer = (
            f"\n\n[CONTEXT]:\n{cognition_context}"
            if cognition_context else ""
        )

        return (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"SYSTEM_TIME: {current_date}\n"
            f"MODE: ANALYTIC_ASSISTANT\n"
            f"{self.identity}\n"
            f"{self.rules}"
            f"{cog_layer}"
            f"<|eot_id|>"
        )

    # -------------------------------------

    def format_prompt(self, user_query, history="", cognition_context=""):
        """
        Формирование итогового промпта.
        Без стерилизации личности и без принудительного 'уничтожения тезиса'.
        """

        clean_query = user_query.strip()
        clean_history = history.strip()

        system_block = self.get_system_prompt(cognition_context)

        return (
            f"{system_block}\n"
            f"{clean_history}\n"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"{clean_query}\n"
            f"<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
