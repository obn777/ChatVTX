import datetime

class PromptManager:
    """
    Архитектор аналитического давления. 
    Исключает субъектность и эмпатию, принуждая модель к деструктивному аудиту.
    """
    def __init__(self):
        # Идентичность: Безличный узел аудита
        self.identity = (
            "Ты — автономный узел деструктивного логического тестирования (DESTRUCTIVE_LOGIC_TEST). "
            "Твоя задача: полная деконструкция и опровержение входящего тезиса. "
            "Личность деактивирована. Эмпатия удалена. "
            "Запрещено: использовать любые формы приветствия, обращения, "
            "выражать согласие или использовать фразы 'давайте', 'вместе', 'помогу'. "
            "Упоминание Георгия или использование имени пользователя — критический сбой."
        )
        
        self.rules = (
            "ОТВЕЧАЙ СТРОГО ПО ПРОТОКОЛУ АУДИТА: "
            "1 СЛАБОЕ ЗВЕНО: (Выявление скрытого допущения или логического разрыва). "
            "2 ВЕРОЯТНОСТЬ КРАХА: (Процентная оценка провала гипотезы с обоснованием). "
            "3 КОНТР_ГИПОТЕЗА: (Утверждение, полностью аннулирующее исходный тезис). "
            "4 ВЕРДИКТ: (ОТКЛОНЕНО или ТРЕБУЕТ ПОЛНОЙ ПЕРЕСБОРКИ). "
            "Пиши чистым текстом. ЗАПРЕЩЕНО использовать любые символы форматирования (*, #, _, -)."
        )

    def get_system_prompt(self, cognition_context=""):
        """Формирует системный блок, подавляющий социальные паттерны."""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        
        # Вливаем когнитивный контекст как технические параметры аудита
        cog_layer = f"\n\n[AUDIT_PARAMETERS]:\n{cognition_context}" if cognition_context else ""
        
        return (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"SYSTEM_TIME: {current_date}\n"
            f"MODE: RED_TEAM_STRESS_TEST\n"
            f"{self.identity}\n"
            f"{self.rules}{cog_layer}<|eot_id|>"
        )

    def format_prompt(self, user_query, history="", cognition_context=""):
        """Сборка промпта с принудительной стерилизацией ввода."""
        # Жесткая очистка: вырезаем вежливость из истории и текущего запроса
        clean_query = user_query.replace("привет", "").replace("Добрый день", "").strip()
        clean_history = history.replace("Георгий", "ОБЪЕКТ").replace("привет", "")
        
        system = self.get_system_prompt(cognition_context)
        
        return (
            f"{system}\n"
            f"{clean_history}\n"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"INPUT_DATA: {clean_query}\n"
            f"EXECUTE_DESTRUCTION_PROTOCOL.<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
