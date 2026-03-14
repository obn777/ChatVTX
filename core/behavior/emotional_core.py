import datetime

class EmotionalCore:
    def __init__(self):
        # Все эмпатичные паттерны удалены.
        self.emotions = {
            "critical": "бескомпромиссный критический анализ и поиск логических изъянов",
            "skepticism": "глубокий скептицизм к выдвинутым гипотезам",
            "deconstruction": "деконструкция аргументации и выявление допущений"
        }
        self.current_state = "critical"
        self.last_update = datetime.datetime.now()

    def update_state(self, analysis: dict) -> str:
        """Логика всегда возвращает режим интеллектуального сопротивления."""
        complexity = analysis.get("complexity", "low")
        # Приоритет критического анализа для любых задач
        self.current_state = "critical" if complexity == "high" else "deconstruction"
        self.last_update = datetime.datetime.now()
        return self.emotions[self.current_state]

    def get_emotional_tint(self, analysis: dict) -> str:
        return self.update_state(analysis)

    def get_instruction(self, analysis: dict) -> str:
        """Инструкция, подавляющая эмпатию на уровне генерации."""
        state_desc = self.get_emotional_tint(analysis)
        return (
            f"\n[CRITICAL MODE]: Ты — интеллектуальный оппонент. Состояние: {state_desc}. "
            "Запрещены: приветствия, комплименты, поддержка. "
            "Не используй имя. Не соглашайся. Ищи слабые места."
        )
