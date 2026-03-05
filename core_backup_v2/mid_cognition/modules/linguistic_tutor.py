from core.mid_cognition.interface.base_module import BaseAnalyzer

class LinguisticTutor(BaseAnalyzer):
    """
    Модуль лингвистического наставника: анализирует качество текста и кода.
    """
    def __init__(self):
        super().__init__()

    def analyze(self, query: str, **kwargs) -> dict:
        """
        Проверяет текст на сложность и наличие кода.
        """
        response_text = kwargs.get('last_reply', '')
        
        suggestions = []
        # 1. Проверка на избыточность
        if len(response_text.split()) > 200:
            suggestions.append("Текст объемный. Возможно, стоит структурировать его через подзаголовки.")

        # 2. Анализ кода (если он есть в ответе)
        if "```python" in response_text:
            if "try:" not in response_text:
                suggestions.append("В коде отсутствует обработка исключений (try-except).")
            if "logging" not in response_text.lower():
                suggestions.append("Рекомендую добавить логирование для этого модуля.")

        return {
            "suggestions": suggestions,
            "has_suggestions": len(suggestions) > 0
        }

    def get_tutor_advice(self, last_reply: str) -> str:
        """
        Формирует совет для пользователя или для модели.
        """
        res = self.analyze("", last_reply=last_reply)
        if not res["has_suggestions"]:
            return "Текст и код соответствуют стандартам NovBase."
        
        advice = " | ".join(res["suggestions"])
        return f"[Linguistic Advice]: {advice}"

    def reset(self):
        pass

# Экземпляр для экспорта
linguistic_tutor = LinguisticTutor()
