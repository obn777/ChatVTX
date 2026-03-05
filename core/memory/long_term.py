import json
import os
import asyncio
import datetime
from pathlib import Path

class LongTermCache:
    """
    Система долгосрочного кэширования NovBase.
    Обеспечивает выживание данных при переустановке проекта и авто-восстановление.
    """
    def __init__(self):
        # 1. Локальный путь (внутри проекта)
        self.local_path = "/home/obn7/NovBase/storage/cache.json"
        
        # 2. Защищенный путь (вне проекта)
        self.secure_backup_dir = "/home/obn7/.novbase_cache_secure"
        self.secure_path = os.path.join(self.secure_backup_dir, "master_cache.json")
        
        self.cache = {}
        self._lock = asyncio.Lock()

    async def init(self):
        """Инициализация: поиск и автоматическое восстановление кэша."""
        os.makedirs(os.path.dirname(self.local_path), exist_ok=True)
        os.makedirs(self.secure_backup_dir, exist_ok=True)
        
        await self._restore_from_secure_zone()
        return self

    async def _restore_from_secure_zone(self):
        """Логика выживания: восстанавливает кэш из защищенной зоны."""
        source = None
        
        if os.path.exists(self.secure_path):
            source = self.secure_path
            print("🛡️ [Cache] Найдена мастер-копия. Восстанавливаю память...")
        elif os.path.exists(self.local_path):
            source = self.local_path
            print("📁 [Cache] Используется локальный кэш.")

        if source:
            try:
                with open(source, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
                
                if source == self.secure_path and not os.path.exists(self.local_path):
                    await self.save_with_backup()
                    print("✅ [Cache] Локальный файл восстановлен из системы.")
            except Exception as e:
                print(f"❌ [Cache] Критическая ошибка чтения: {e}")
                self.cache = {}

    async def save_with_backup(self):
        """Двойное сохранение (Mirroring)."""
        async with self._lock:
            data_str = json.dumps(self.cache, ensure_ascii=False, indent=2)
            
            try:
                with open(self.local_path, "w", encoding="utf-8") as f:
                    f.write(data_str)
            except Exception as e:
                print(f"⚠️ [Cache] Ошибка локального сохранения: {e}")
            
            try:
                with open(self.secure_path, "w", encoding="utf-8") as f:
                    f.write(data_str)
            except Exception as e:
                print(f"⚠️ [Cache] Ошибка записи в защищенную зону: {e}")

    def _validate_quality(self, text: str) -> bool:
        """Интеллектуальный фильтр качества."""
        if not text or len(text) < 5: return False # Снизил порог для коротких важных ответов
        
        blacklist = ["error", "critical connection", "undefined", "{"]
        if any(item in text.lower() for item in blacklist): return False
        
        return True

    async def set_entry(self, query: str, response: str):
        """Запись в кэш."""
        if not self._validate_quality(response):
            return False

        clean_resp = response.strip().replace("&nbsp;", " ")
        
        # Сохраняем как объект для расширяемости
        self.cache[query.lower().strip()] = {
            "value": clean_resp,
            "timestamp": datetime.datetime.now().isoformat()
        }
        
        await self.save_with_backup()
        return True

    async def get_entry(self, query: str):
        """Мгновенный поиск."""
        query_fixed = query.lower().strip()
        entry = self.cache.get(query_fixed)
        
        if entry:
            # Возвращаем только строку значения
            return entry["value"] if isinstance(entry, dict) else entry
        return None

    async def get_context(self, limit=5):
        """
        НОВЫЙ МЕТОД: Возвращает последние N записей для истории диалога.
        Это именно то, что нужно для 'памяти' Малышки.
        """
        try:
            # Берем последние записи из текущего словаря кэша
            items = list(self.cache.items())[-limit:]
            context = []
            for q, data in items:
                # Извлекаем текст ответа в зависимости от формата хранения
                ans = data["value"] if isinstance(data, dict) else data
                context.append({"q": q, "a": ans})
            return context
        except Exception as e:
            print(f"⚠️ [Cache] Ошибка получения контекста: {e}")
            return []
