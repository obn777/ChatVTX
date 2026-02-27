from core.mid_cognition.interface.base_module import BaseAnalyzer

class MissionPlanner(BaseAnalyzer):
    def __init__(self):
        super().__init__()

    def analyze(self, query: str, **kwargs) -> dict:
        analysis = kwargs.get('analysis', {})
        intent = analysis.get('intent')
        
        plan = []
        # Если анализатор пометил запрос как команду (action)
        if intent == "action":
            # Ищем конкретную задачу: запись
            if any(w in query.lower() for w in ["запиши", "файл", "заметка"]):
                plan.append("action: file_save")
        
        return {
            "plan": plan,
            "requires_action": len(plan) > 0
        }

    def reset(self):
        pass

mission_planner = MissionPlanner()
