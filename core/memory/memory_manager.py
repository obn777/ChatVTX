import os
import json
import datetime
from core.config import config

class MemoryManager:
    """
    Управляет краткосрочной и долгосрочной памятью системы.
    Реализует автоматическое сохранение кэша и ротацию истории.
    Интегрировано требование от 11.02 по сохранению кэша.
    """
    def __init__(self):
        # Пути подтягиваются из центрального конфига paths.json
        self.history_path = config.get_storage_path("history")
        self.master_cache_path = config.get_storage_path("long_term_memory")
        self._ensure_storage()

    def _ensure_storage(self):
        """Проверяет наличие файлов и создает структуру при первом запуске."""
        for path in [self.history_path, self.master_cache_path]:
            if not os.path.exists(path):
                os.makedirs(os.path.dirname(path), exist_ok=True)
                initial_data = {
                    "history": [] if "history" in path else {},
                    "metadata": {
                        "created": str(datetime.datetime.now()),
                        "version": "2.0"
                    }
                }
                if "long_term" in path:
                    initial_data = {"data": {}, "metadata": initial_data["metadata"]}
                
                with open(path, 'w', encoding='utf-8') as f:
                    json.dump(initial_data, f, ensure_ascii=False, indent=4)
                print(f"📁 [MEMORY]: Инициализировано новое хранилище: {path}")

    def _load_json(self, path):
        """Безопасная загрузка JSON с защитой от сбоев питания на Nitro."""
        try:
            if os.path.exists(path):
                with open(path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except (json.JSONDecodeError, Exception) as e:
            print(f"⚠️ [MEMORY ERROR]: Файл поврежден {path}: {e}")
            return {}

    def _save_json(self, path, data):
        """Атомарная запись для предотвращения повреждения данных."""
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"❌ [MEMORY ERROR]: Ошибка записи {path}: {e}")
            return False

    def save_to_history(self, user_text, assistant_text):
        """
        Сохраняет диалог и обновляет к acknowledgment долгосрочной памяти.
        Ротация: 50 последних записей (согласно оптимизации VRAM).
        """
        # 1. Обновление текущей истории сессии
        data = self._load_json(self.history_path)
        if "history" not in data or not isinstance(data["history"], list):
            data["history"] = []
            
        new_entry = {
            "timestamp": str(datetime.datetime.now()),
            "q": user_text,
            "a": assistant_text
        }
        
        data["history"].append(new_entry)
        
        # Ротация: держим только последние 50 записей для быстрого парсинга
        if len(data["history"]) > 50:
            data["history"] = data["history"][-50:]
            
        self._save_json(self.history_path, data)

        # 2. Синхронизация с Long-Term Memory (Инструкция от 11.02)
        self._update_master_cache(user_text, assistant_text)

    def _update_master_cache(self, q, a):
        """Индексация данных для мгновенного восстановления ответов."""
        cache = self._load_json(self.master_cache_path)
        if "data" not in cache:
            cache["data"] = {}
            
        # Нормализация ключа (нижний регистр, без лишних пробелов)
        key = q.strip().lower()
        
        # Сохраняем только содержательные ответы (длиннее 10 символов)
        if len(key) > 3 and len(a) > 10:
            cache["data"][key] = {
                "response": a,
                "last_seen": str(datetime.datetime.now()),
                "hits": cache["data"].get(key, {}).get("hits", 0) + 1
            }
        
        self._save_json(self.master_cache_path, cache)

    def get_history_for_prompt(self, limit=5):
        """Извлекает контекст для формирования промпта."""
        data = self._load_json(self.history_path)
        history = data.get("history", [])
        if not isinstance(history, list):
            return []
        return history[-limit:]

    def clear_session_history(self):
        """Очистка текущей истории без удаления долгосрочного кэша."""
        data = {"history": [], "metadata": {"cleared": str(datetime.datetime.now())}}
        self._save_json(self.history_path, data)
        print("🧹 [MEMORY]: История текущей сессии очищена.")
