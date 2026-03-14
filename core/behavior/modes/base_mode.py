from abc import ABC, abstractmethod

class BaseMode(ABC):
    """
    Абстрактный базовый класс для всех интеллектуальных режимов NovBase.
    Обеспечивает единство структуры и стандарты вывода.
    """
    def __init__(self):
        self.mode_name = "BASE"
        # Общие ограничения для всех режимов, чтобы модель не "плыла"
        self.base_constraints = (
            "ОБЩИЕ ПРАВИЛА:\n"
            "- Никаких приветствий и этикетных пауз.\n"
            "- Запрещено использовать имя Георгий (обращайся 'Объект' или 'Система').\n"
            "- Ответ должен быть максимально плотным, без водянистых вступлений.\n"
            "- Используй только фактологический стиль."
        )

    @abstractmethod
    def modify_prompt(self, prompt: str) -> str:
        """
        Метод трансформации входящего запроса под специфику режима.
        Должен быть переопределен в каждом дочернем классе.
        """
        pass

    def get_description(self) -> str:
        """Возвращает краткое описание возможностей режима."""
        return "Базовый когнитивный слой системы."

    def _apply_base_wrap(self, core_instruction: str, user_input: str) -> str:
        """
        Вспомогательный метод для единообразного форматирования 
        системного промпта (внутренний хелпер).
        """
        return (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"{self.base_constraints}\n"
            f"{core_instruction}\n"
            f"<|eot_id|>\n"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_input}\n"
            f"<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
