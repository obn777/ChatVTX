import json
import os
from datetime import datetime

class ClientManager:
    def __init__(self, file_path="/root/NovBase/data/client_tasks.json"):
        self.file_path = file_path
        # Список уроков для английского языка
        self.english_lessons = [
            "Урок 1: Основы произношения и алфавит. Давай начнем с произношения гласных.",
            "Урок 2: Приветствия и знакомство. Как правильно представить себя на английском.",
            "Урок 3: Базовые глаголы быть и иметь. Строим первые простые предложения.",
            "Урок 4: Числительные и время. Учимся называть время и считать.",
            "Урок 5: Повседневные фразы. Общение в магазине и кафе."
        ]
        if not os.path.exists(self.file_path):
            self._save_json({"clients": {}})

    def _load_json(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"clients": {}}

    def _save_json(self, data):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def manage_task(self, client_name, text):
        text_l = text.lower()
        
        # Если клиент просит начать курс или дать следующий урок
        if "курс" in text_l or "обучение" in text_l or "следующий урок" in text_l:
            if "английск" in text_l or "english" in text_l:
                return self._process_english_course(client_name)
        
        return None

    def _process_english_course(self, client_name):
        db = self._load_json()
        
        if client_name not in db["clients"]:
            db["clients"][client_name] = {"english_step": 0}
            
        current_step = db["clients"][client_name].get("english_step", 0)
        
        if current_step < len(self.english_lessons):
            lesson_text = self.english_lessons[current_step]
            db["clients"][client_name]["english_step"] += 1
            self._save_json(db)
            return f"Василий, твой текущий прогресс сохранен. {lesson_text} Когда будешь готов к следующему шагу, просто скажи мне."
        else:
            return "Василий, ты успешно завершил базовый курс английского языка. Поздравляю. Могу предложить повторение или перейти к новой теме."

    def get_client_info(self, client_name):
        db = self._load_json()
        return db["clients"].get(client_name, None)
