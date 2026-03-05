import re


class IntentRouter:
    """
    Определяет намерение запроса до выбора режима.
    Минимизирует ложные срабатывания стратегических режимов.
    """

    def __init__(self):
        self.engineering_triggers = [
            "реализуй",
            "напиши",
            "спроектируй",
            "создай",
            "разработай"
        ]

        self.debate_triggers = [
            "докажи",
            "оспори",
            "опровергни",
            "разгроми",
            "почему это неверно"
        ]

        self.info_triggers = [
            "как",
            "что",
            "где",
            "когда",
            "зачем",
            "почему"
        ]

    # ----------------------------------

    def detect(self, text: str) -> str:
        if not text or len(text.strip()) < 3:
            return "clarification"

        lower = text.lower()

        # Debate — включаем строгий аудит
        if any(trigger in lower for trigger in self.debate_triggers):
            return "debate"

        # Engineering — приоритет над аналитикой
        if any(trigger in lower for trigger in self.engineering_triggers):
            return "engineering"

        # Информационный запрос
        if any(lower.startswith(trigger) for trigger in self.info_triggers):
            return "info"

        # Короткий ввод
        if len(lower.split()) <= 2:
            return "clarification"

        return "analysis"
