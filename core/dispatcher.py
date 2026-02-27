import json
import os
from datetime import datetime

class MemoryDispatcher:
    def __init__(self, cache_path):
        self.path = cache_path
        # 0. СТОП-ТРИГГЕРЫ (Запросы, которые нельзя кешировать)
        self.vision_triggers = ["фото", "изображение", "видишь", "картинка", "photo", "image", "на этом"]
        self.ensure_storage()

    def ensure_storage(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as f: 
                json.dump({}, f)

    def process_entry(self, query, response, intent):
        # 1. ЗАПРЕТ СОХРАНЕНИЯ ВИЗУАЛЬНЫХ ДАННЫХ
        # Нам не нужно сохранять ответ на "Что на фото?", так как фото всегда меняется
        low_query = query.lower()
        if any(w in low_query for w in self.vision_triggers):
            return "skipped_vision"

        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}

        # 2. ОПРЕДЕЛЕНИЕ ПРИОРИТЕТА
        priority = 1
        if any(w in low_query for w in ["год", "время", "дата", "кто я", "зовут", "час"]):
            priority = 10
        elif intent in ["memorize", "skill_use", "cybernetic"]:
            priority = 7

        # 3. ДРОБЛЕНИЕ ПО ТЕМАМ
        topic = "general"
        if any(w in low_query for w in ["время", "год", "час", "минут", "секунд"]): 
            topic = "time_sync"
        elif any(w in low_query for w in ["гео", "где", "координат", "город"]):
            topic = "location"
        
        # 4. АВТО-ЗАМЕНА (Очистка старых данных темы)
        if topic in ["time_sync", "location"]:
            data = {k: v for k, v in data.items() if v.get("topic") != topic}

        # 5. ЗАПИСЬ НОВОЙ РЕВИЗИИ
        old_rev = 0
        if query in data and isinstance(data[query], dict):
            old_rev = data[query].get("rev", 0)
        
        data[query] = {
            "value": response,
            "timestamp": datetime.now().isoformat(),
            "priority": priority,
            "topic": topic,
            "rev": old_rev + 1
        }

        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return f"v{data[query]['rev']}"

    def get_valid_cache(self, query):
        low_query = query.lower()
        
        # 6. ПРОВЕРКА НА ВИЗУАЛЬНЫЙ ЗАПРОС (Обход кеша)
        if any(w in low_query for w in self.vision_triggers):
            print(f"📸 [DISPATCHER]: Визуальный запрос. Кеш принудительно пропущен.")
            return None

        try:
            if not os.path.exists(self.path): return None
            
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            entry = data.get(query)
            if not entry or not isinstance(entry, dict):
                return None

            topic = entry.get('topic', 'general')
            timestamp = entry.get('timestamp')
            value = entry.get('value')

            # 7. ПРОВЕРКА АКТУАЛЬНОСТИ
            if topic == "time_sync" and timestamp:
                dt = datetime.fromisoformat(timestamp)
                if (datetime.now() - dt).total_seconds() > 10:
                    print(f"🔄 [Dispatcher] Кэш времени устарел")
                    return None
            
            return value
        except Exception as e:
            print(f"⚠️ Ошибка Диспетчера: {e}")
            return None
