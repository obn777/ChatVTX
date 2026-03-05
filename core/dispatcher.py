import json
import os
import re
from datetime import datetime


class MemoryDispatcher:
    """
    Интеллектуальный диспетчер памяти NovBase.
    Управляет кэшем, режимами и приоритетами обработки.
    Поддерживает гибридный формат данных (list/dict).
    """

    def __init__(self, cache_path="/home/obn7/NovBase/storage/cache.json"):
        self.path = cache_path

        # Триггеры визуального режима
        self.vision_triggers = [
            "фото", "изображение", "видишь", "картинка", "photo",
            "image", "на этом", "смотри", "взгляни"
        ]

        self.ensure_storage()

    # -------------------------------------------------
    # STORAGE
    # -------------------------------------------------

    def ensure_storage(self):
        os.makedirs(os.path.dirname(self.path), exist_ok=True)
        if not os.path.exists(self.path):
            with open(self.path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False)

    def _load_safe(self):
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    # -------------------------------------------------
    # UTILITIES
    # -------------------------------------------------

    def _sanitize_query(self, query):
        q = query.lower().strip()
        q = re.sub(r'[^\w\s]', '', q)
        return " ".join(q.split())

    # -------------------------------------------------
    # MODE SYSTEM
    # -------------------------------------------------

    def extract_mode_command(self, text: str):
        """
        Проверяет явную команду вида:
        /mode opponent
        """
        text = text.strip().lower()

        if text.startswith("/mode"):
            parts = text.split()
            if len(parts) >= 2:
                return parts[1]

        return None

    def auto_detect_mode(self, text: str) -> str:
        """
        Простая эвристика определения режима.
        """
        t = text.lower()

        if "анализ" in t or "ошибк" in t:
            return "opponent"

        if "план" in t or "стратег" in t:
            return "strategic"

        if "шаг" in t or "инструкц" in t:
            return "engineering"

        return "analytic"

    # -------------------------------------------------
    # CACHE WRITE
    # -------------------------------------------------

    def process_entry(self, query, response, intent="general"):
        low_query = self._sanitize_query(query)
        if not low_query:
            return "empty_query"

        if any(w in low_query for w in self.vision_triggers):
            return "skipped_vision"

        data = self._load_safe()

        if isinstance(data, list):
            data.append({
                "q": query,
                "a": response,
                "timestamp": datetime.now().isoformat(),
                "intent": intent
            })
            if len(data) > 200:
                data = data[-100:]
        else:
            if not isinstance(data, dict):
                data = {}

            priority = 1
            if any(w in low_query for w in ["год", "время", "дата", "час"]):
                priority = 10

            topic = "general"
            if any(w in low_query for w in ["время", "час"]):
                topic = "time_sync"

            if topic in ["time_sync"]:
                data = {
                    k: v for k, v in data.items()
                    if isinstance(v, dict) and v.get("topic") != topic
                }

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

    # -------------------------------------------------
    # CACHE READ
    # -------------------------------------------------

    def get_valid_cache(self, query):
        low_query = self._sanitize_query(query)
        if not low_query:
            return None

        if any(w in low_query for w in self.vision_triggers):
            return None

        data = self._load_safe()

        if isinstance(data, list):
            for entry in reversed(data):
                if isinstance(entry, dict) and \
                   self._sanitize_query(entry.get("q", "")) == low_query:
                    return entry.get("a")
            return None

        entry = data.get(low_query)
        if not entry or not isinstance(entry, dict):
            return None

        topic = entry.get('topic', 'general')
        timestamp = entry.get('timestamp')

        if topic == "time_sync" and timestamp:
            try:
                dt = datetime.fromisoformat(timestamp)
                if (datetime.now() - dt).total_seconds() > 30:
                    return None
            except:
                return None

        return entry.get('value')
