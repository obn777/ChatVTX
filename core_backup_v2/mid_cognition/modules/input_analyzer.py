from core.mid_cognition.interface.base_module import BaseAnalyzer

class InputAnalyzer(BaseAnalyzer):
    def __init__(self):
        super().__init__()
    
    def analyze(self, text: str, **kwargs) -> dict:
        text_l = text.lower()
        
        # --- 1. ДЕТЕКЦИЯ НАМЕРЕНИЙ (INTENTS) ---
        intent = "unknown"
        
        # ПРИОРИТЕТ 1: Команды к действию (Action)
        # Добавил больше триггеров для записи файлов и работы с системой
        if any(w in text_l for w in ["запиши", "заметка", "файл", "создай", "в файл", "занеси"]):
            intent = "action"
        
        # ПРИОРИТЕТ 2: Работа с памятью (Memorize)
        elif any(w in text_l for w in ["запомни", "сохрани в памяти", "зафиксируй"]): 
            intent = "memorize"
            
        # ПРИОРИТЕТ 3: Запрос данных (Recall)
        elif any(w in text_l for w in ["как меня зовут", "кто я", "вспомни", "что ты видел", "кто перед тобой"]): 
            intent = "recall"
            
        # ПРИОРИТЕТ 4: Социальное взаимодействие (Greeting)
        elif any(w in text_l for w in ["привет", "здравствуй", "хай", "приветствую"]): 
            intent = "greeting"
        
        # --- 2. АНАЛИЗ ТОНАЛЬНОСТИ (SENTIMENT) ---
        sentiment = "neutral"
        if any(w in text_l for w in ["круто", "хорошо", "молодец", "спасибо", "отлично"]): 
            sentiment = "positive"
        elif any(w in text_l for w in ["тупишь", "плохо", "ошибка", "ужасно", "неправильно"]): 
            sentiment = "negative"

        # --- 3. СБОР РЕЗУЛЬТАТОВ ---
        return {
            "intent": intent,
            "sentiment": sentiment,
            "topic": "общее",  # Стандартная тема
            "has_question": "?" in text or any(w in text_l for w in ["как", "что", "почему", "зачем", "кто", "где"]),
            "language": "russian",
            "full_text": text
        }

    def reset(self):
        """Сброс состояния анализатора при необходимости"""
        pass

# Экземпляр для импорта в cognition.py
input_analyzer = InputAnalyzer()
