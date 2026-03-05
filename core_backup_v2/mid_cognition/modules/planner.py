from core.mid_cognition.interface.base_module import BaseAnalyzer

class MissionPlanner(BaseAnalyzer):
    """
    Модуль планирования: разбивает сложные интенты на последовательность действий.
    """
    def __init__(self):
        super().__init__()

    def analyze(self, query: str, **kwargs) -> dict:
        """
        Анализирует запрос на предмет необходимости выполнения системных операций.
        """
        analysis = kwargs.get('analysis', {})
        intent = analysis.get('intent', 'general')
        ql = query.lower()
        
        plan = []
        
        # 1. Логика работы с файловой системой и кодом
        if intent == "action" or any(w in ql for w in ["запиши", "файл", "сохрани", "заметка"]):
            if any(w in ql for w in ["код", "скрипт", "python"]):
                plan.append("step: code_formatting")
            plan.append("action: file_save")

        # 2. Логика долгосрочной памяти
        if any(w in ql for w in ["запомни", "важно", "в памяти"]):
            plan.append("action: memory_store")

        # 3. Логика синхронизации
        if any(w in ql for w in ["синхрон", "github", "отправь"]):
            plan.append("action: git_push")

        return {
            "plan": plan,
            "requires_action": len(plan) > 0,
            "priority": "high" if "action" in intent else "normal"
        }

    def plan_steps(self, query: str, analysis: dict) -> str:
        """
        Метод для интеграции с контроллером: возвращает план в виде строки для LLM.
        """
        res = self.analyze(query, analysis=analysis)
        if not res["requires_action"]:
            return "Специфических системных действий не требуется."
        
        steps = " -> ".join(res["plan"])
        return f"План действий: {steps}."

    def reset(self):
        """Сброс состояния планировщика."""
        pass

# Экземпляр для экспорта
mission_planner = MissionPlanner()
