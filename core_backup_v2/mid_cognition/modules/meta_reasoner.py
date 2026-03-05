from core.mid_cognition.interface.base_module import BaseAnalyzer

class MetaReasoner(BaseAnalyzer):
    """
    Модуль мета-анализа: формирует стратегию ответа и внутреннюю логику действий.
    """
    def __init__(self):
        super().__init__()
        self.current_task = None

    def analyze(self, query: str, **kwargs) -> dict:
        """
        Основной метод анализа когнитивного состояния.
        """
        # Безопасно извлекаем данные из kwargs
        analysis = kwargs.get('analysis', {})
        last_obj = kwargs.get('last_obj', 'контекст пуст')
        
        # 1. Оцениваем сложность (добавил проверку на длину запроса и ключевые слова кода)
        query_lower = query.lower()
        is_complex = (
            analysis.get('complexity') == 'high' or 
            analysis.get('intent') in ['deep_analysis', 'action'] or
            len(query.split()) > 15 or # Длинные запросы требуют больше внимания
            any(w in query_lower for w in ["код", "скрипт", "функци", "ошибк"])
        )
        
        # 2. Формируем цепочку рассуждений (Chain of Thought)
        thought_process = []
        if is_complex:
            thought_process.append(f"Георгий поставил сложную задачу")
            thought_process.append(f"Фокус: {last_obj}")
            thought_process.append("Активация режима High-Capacity для Llama-3.1-8B")
        else:
            thought_process.append("Стандартный диалог")
        
        return {
            "thought_chain": thought_process,
            "is_complex": is_complex,
            "recommended_action": "respond" if not is_complex else "solve_task"
        }

    def think(self, text: str, state: str) -> str:
        """
        Формирует текстовый внутренний монолог для системного промпта.
        """
        # Передаем состояние в analyze через именованные аргументы
        cog_analysis = self.analyze(text)
        chain = " -> ".join(cog_analysis["thought_chain"])
        
        # Убираем лишние символы для вокальной чистоты (инструкция от 26.02)
        return (
            f"Внутренний план: {chain}. "
            f"Учитываю эмоциональный фон: {state}. "
            f"Рекомендованное действие: {cog_analysis['recommended_action']}."
        )

    def reset(self):
        self.current_task = None

# Экземпляр для экспорта
meta_reasoner = MetaReasoner()
