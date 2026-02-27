from core.mid_cognition.interface.base_module import BaseAnalyzer

class MetaReasoner(BaseAnalyzer):
    def __init__(self):
        super().__init__()
        self.current_task = None

    def analyze(self, query: str, **kwargs) -> dict:
        analysis = kwargs.get('analysis', {})
        last_obj = kwargs.get('last_obj', 'ничего')
        
        # Логика "внутреннего монолога"
        # 1. Оцениваем сложность
        is_complex = analysis.get('has_question') or analysis.get('intent') == 'action'
        
        # 2. Формируем цепочку рассуждений (Chain of Thought)
        thought_process = []
        if is_complex:
            thought_process.append(f"Георгий спрашивает: {query}")
            thought_process.append(f"Я вижу перед собой: {last_obj}")
            thought_process.append("Нужно сопоставить эти данные.")
        
        return {
            "thought_chain": thought_process,
            "is_complex": is_complex,
            "recommended_action": "respond" if not is_complex else "solve_task"
        }

    def reset(self):
        self.current_task = None

meta_reasoner = MetaReasoner()
