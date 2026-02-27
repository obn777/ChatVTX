import json
import os
import asyncio
import datetime
import shutil
from pathlib import Path

class LongTermCache:
    """
    Система долгосрочного кэширования NovBase.
    Обеспечивает выживание данных при переустановке проекта.
    """
    def __init__(self):
        # Основной путь (внутри проекта)
        self.local_path = "/home/obn7/NovBase/storage/cache.json"
        
        # Защищенный путь (вне папки проекта для выживания при переустановке)
        # Используем стандартную системную директорию Termux для var данных
        self.secure_backup_dir = "/data/data/com.termux/files/usr/var/novbase_cache"
        self.secure_path = os.path.join(self.secure_backup_dir, "master_cache.json")
        
        self.cache = {}
        self._lock = asyncio.Lock()

    async def init(self):
        """Инициализация: поиск и восстановление кэша."""
        os.makedirs(os.path.dirname(self.local_path), exist_ok=True)
        os.makedirs(self.secure_backup_dir, exist_ok=True)
        
        await self._restore_from_secure_zone()
        return self

    async def _restore_from_secure_zone(self):
        """Восстанавливает локальный кэш из защищенной зоны, если локальный пуст."""
        target = None
        
        # Логика выбора источника
        if os.path.exists(self.secure_path):
            target = self.secure_path
            print("🛡️ [Cache] Обнаружена защищенная копия. Восстановление...")
        elif os.path.exists(self.local_path):
            target = self.local_path
            print("📁 [Cache] Используется локальный кэш.")

        if target:
            try:
                with open(target, "r", encoding="utf-8") as f:
                    self.cache = json.load(f)
            except Exception as e:
                print(f"❌ [Cache] Ошибка чтения: {e}")
                self.cache = {}

    async def save_with_backup(self):
        """Сохранение сразу в две точки (асинхронно)."""
        async with self._lock:
            data = json.dumps(self.cache, ensure_ascii=False, indent=2)
            
            # Сохраняем локально
            with open(self.local_path, "w", encoding="utf-8") as f:
                f.write(data)
            
            # Резервируем в защищенную зону
            try:
                with open(self.secure_path, "w", encoding="utf-8") as f:
                    f.write(data)
            except PermissionError:
                print("⚠️ [Cache] Нет прав на запись в системную зону var!")

    def _validate_quality(self, text: str) -> bool:
        """Интеллектуальный фильтр на основе вашего CacheFilter."""
        if not text or len(text) < 20: return False
        if not any(char in text for char in ".!?"): return False
        # Исключаем технический мусор
        if "<br>" in text or "{" in text: return False
        return True

    async def set_entry(self, query: str, response: str):
        """Добавление записи с проверкой качества."""
        if not self._validate_quality(response):
            return False

        clean_resp = response.strip().replace("&nbsp;", " ")
        
        self.cache[query] = {
            "value": clean_resp,
            "date": datetime.datetime.now().isoformat(),
            "rating": self.cache.get(query, {}).get("rating", 1.0)
        }
        
        # Автосохранение
        await self.save_with_backup()
        return True

    async def get_entry(self, query: str):
        """Получение записи."""
        entry = self.cache.get(query)
        if entry:
            return entry["value"]
        return None
