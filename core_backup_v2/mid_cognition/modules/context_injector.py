import collections
import datetime

class ContextInjector:
    """
    Модуль 'Эмоционального эха'. 
    Накапливает историю состояний и подмешивает её в текущий промпт.
    """
    def __init__(self, memory_limit=5):
        # Очередь с фиксированной длиной для хранения последних состояний
        self.state_history = collections.deque(maxlen=memory_limit)
        self.last_sync = datetime.datetime.now()

    def inject(self, current_analysis: dict, current_state: str) -> str:
        """
        Принимает текущую эмоцию и возвращает 'сглаженный' контекст 
        с учетом предыдущих состояний.
        """
        self.state_history.append({
            "state": current_state,
            "sentiment": current_analysis.get("sentiment", "neutral"),
            "time": datetime.datetime.now()
        })

        # Анализируем доминирующее настроение в истории
        sentiments = [s["sentiment"] for s in self.state_history]
        
        # Если в истории много негатива, усиливаем поддержку
        if sentiments.count("negative") >= 2:
            echo_msg = "В воздухе всё еще чувствуется напряжение от прошлых проблем. Будь особенно внимательна и надежна."
        elif sentiments.count("positive") >= 3:
            echo_msg = "Георгий в отличном настроении, поддерживай этот драйв и легкую ироничность."
        else:
            echo_msg = "Соблюдай преемственность текущего диалога."

        return f"[EMOTIONAL ECHO]: {echo_msg}"

    def reset(self):
        """Очистка эмоциональной памяти."""
        self.state_history.clear()

# Экземпляр для интеграции
context_injector = ContextInjector()
