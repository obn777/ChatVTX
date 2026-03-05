import asyncio
import json
import os
import datetime
from pathlib import Path

class CacheSanitizer:
    """
    Автономный сервис очистки и оптимизации долгосрочного кэша NovBase.
    Универсален: работает и со словарями кэша, и со списками истории.
    """
    def __init__(self, cache_path: str = "/home/obn7/NovBase/storage/cache.json"):
        self.cache_path = cache_path
        # Путь к мастер-копии в защищенной зоне
        self.secure_path = "/home/obn7/.novbase_cache_secure/master_cache.json"

    async def run_periodic_cleanup(self, interval_hours: int = 24):
        """Запуск цикла очистки раз в сутки."""
        while True:
            await asyncio.sleep(interval_hours * 3600)
            print(f"🧹 [Sanitizer] Плановая очистка: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            await self.perform_cleanup()

    async def perform_cleanup(self):
        """Основная логика фильтрации и сжатия."""
        if not os.path.exists(self.cache_path):
            print("⚠️ [Sanitizer] Файл не найден, чистить нечего.")
            return

        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            original_count = len(data)
            now = datetime.datetime.now()

            # СЛУЧАЙ 1: Данные в формате СЛОВАРЯ (Кэш быстрых ответов)
            if isinstance(data, dict):
                to_delete = []
                for query, content in data.items():
                    # Проверка по времени (если есть timestamp)
                    last_used = content.get("timestamp") if isinstance(content, dict) else None
                    if last_used:
                        try:
                            dt = datetime.datetime.fromisoformat(last_used)
                            if (now - dt).days > 60 and content.get("rating", 1.0) < 1.5:
                                to_delete.append(query)
                                continue
                        except: pass

                    # Удаление мусора
                    val = str(content.get("value", "")) if isinstance(content, dict) else str(content)
                    if len(val) < 5 or "{" in val or "undefined" in val.lower():
                        to_delete.append(query)

                for q in to_delete:
                    del data[q]

            # СЛУЧАЙ 2: Данные в формате СПИСКА (История диалогов)
            elif isinstance(data, list):
                # Оставляем только последние 100 записей, фильтруем пустые
                data = [
                    entry for entry in data 
                    if isinstance(entry, dict) and len(str(entry.get("a", ""))) > 5
                ]
                if len(data) > 100:
                    data = data[-100:]

            # Сохранение очищенных данных (Mirroring)
            clean_json = json.dumps(data, ensure_ascii=False, indent=2)
            for path in [self.cache_path, self.secure_path]:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(clean_json)

            diff = original_count - len(data)
            print(f"✅ [Sanitizer] Готово. Удалено объектов: {diff}")
            
        except Exception as e:
            print(f"❌ [Sanitizer] Критическая ошибка при очистке: {e}")

if __name__ == "__main__":
    sanitizer = CacheSanitizer()
    asyncio.run(sanitizer.perform_cleanup())
