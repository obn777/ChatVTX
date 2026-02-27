from abc import ABC, abstractmethod

class BaseAnalyzer(ABC):
    """
    Базовый интерфейс для всех модулей когнитивного слоя NovBase.
    Гарантирует, что каждый модуль (InputAnalyzer, ContextTracker и т.д.)
    имеет стандартизированные методы управления.
    """
    def __init__(self):
        self.name = self.__class__.__name__

    @abstractmethod
    def analyze(self, text: str, **kwargs) -> dict:
        """
        Основной метод анализа. Принимает текст и дополнительные аргументы 
        (например, визуальный контекст от проектора).
        """
        pass

    @abstractmethod
    def reset(self):
        """
        Сбрасывает внутреннее состояние модуля (историю, накопленные флаги).
        """
        pass
