import json
import os
import re
from datetime import datetime

class MemoryDispatcher:
    """
    Интеллектуальный диспетчер памяти NovBase.
    Управляет приоритетами кеширования и поддерживает гибридный формат данных (list/dict).
    """
    def __init__(self, cache_path="/home/obn7/NovBase/storage/cache.json"):
        self.path = cache_path
        # Триггеры визуального режима (обработка картинками идет мимо текстового кэша)
        self.vision_triggers = [
            "фото", "изображение", "видишь", "картинка", "photo", 
            "image", "на этом", "смотри", "взгляни"
        ]
        self.ensure_storage()

    def ensure_storage(self):
        """Гарантирует наличие директории и файла кэша."""
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as f: 
                json.dump({}, f, ensure_ascii=False)

    def _load_safe(self):
        """Безопасная загрузка данных любого типа."""
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _sanitize_query(self, query):
        """Очистка запроса для более точного поиска в кэше."""
        # Убираем знаки препинания и лишние пробелы для 'мягкого' совпадения
        q = query.lower().strip()
        q = re.sub(r'[^\w\s]', '', q)
        return " ".join(q.split())

    def process_entry(self, query, response, intent="general"):
        """Запись новой информации с определением её 'веса'."""
        low_query = self._sanitize_query(query)
        if not low_query: return "empty_query"
        
        if any(w in low_query for w in self.vision_triggers):
            return "skipped_vision"

        data = self._load_safe()

        # Если данные — список (формат истории)
        if isinstance(data, list):
            data.append({
                "q": query,
                "a": response,
                "timestamp": datetime.now().isoformat(),
                "intent": intent
            })
            if len(data) > 200: data = data[-100:]
        else:
            # Если данные — словарь (структурированный кэш)
            if not isinstance(data, dict): data = {}
            
            # Определяем приоритет (важные факты хранятся дольше)
            priority = 1
            if any(w in low_query for w in ["год", "время", "дата", "кто я", "зовут", "час"]):
                priority = 10
            
            # Тематическая группировка
            topic = "general"
            if any(w in low_query for w in ["время", "год", "час"]): 
                topic = "time_sync"
            elif any(w in low_query for w in ["гео", "где", "город"]):
                topic = "location"
            
            # Очистка старых данных по той же теме (например, старое время)
            if topic in ["time_sync", "location"]:
                data = {k: v for k, v in data.items() if isinstance(v, dict) and v.get("topic") != topic}

            old_rev = 0
            if low_query in data and isinstance(data[low_query], dict):
                old_rev = data[low_query].get("rev", 0)
            
            data[low_query] = {
                "value": response,
                "timestamp": datetime.now().isoformat(),
                "priority": priority,
                "topic": topic,
                "rev": old_rev + 1
            }

        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return "saved"

    def get_valid_cache(self, query):
        """Поиск актуального ответа с поддержкой обоих форматов данных."""
        low_query = self._sanitize_query(query)
        if not low_query: return None
        
        if any(w in low_query for w in self.vision_triggers):
            return None

        data = self._load_safe()

        # ОБРАБОТКА СПИСКА
        if isinstance(data, list):
            for entry in reversed(data):
                if isinstance(entry, dict) and self._sanitize_query(entry.get("q", "")) == low_query:
                    return entry.get("a")
            return None

        # ОБРАБОТКА СЛОВАРЯ
        entry = data.get(low_query)
        if not entry or not isinstance(entry, dict):
            return None

        topic = entry.get('topic', 'general')
        timestamp = entry.get('timestamp')
        
        # Проверка актуальности для динамических данных (время устаревает за 30 сек)
        if topic == "time_sync" and timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                if (datetime.now() - dt).total_seconds() > 30:
                    return None
            except: return None
        
        return entry.get('value')
