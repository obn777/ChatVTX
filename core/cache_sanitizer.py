import asyncio
import json
import os
import datetime
from pathlib import Path

class CacheSanitizer:
    """
    Автономный сервис очистки и оптимизации долгосрочного кэша.
    """
    def __init__(self, cache_path: str = "/home/obn7/NovBase/storage/cache.json"):
        self.cache_path = cache_path
        self.secure_path = "/data/data/com.termux/files/usr/var/novbase_cache/master_cache.json"

    async def run_periodic_cleanup(self, interval_hours: int = 24):
        """Запуск цикла очистки раз в сутки."""
        while True:
            print(f"🧹 [Sanitizer] Плановая очистка кэша: {datetime.datetime.now()}")
            await self.perform_cleanup()
            await asyncio.sleep(interval_hours * 3600)

    async def perform_cleanup(self):
        """Основная логика фильтрации и сжатия."""
        if not os.path.exists(self.cache_path):
            return

        try:
            with open(self.cache_path, "r", encoding="utf-8") as f:
                cache = json.load(f)

            original_count = len(cache)
            now = datetime.datetime.now()
            to_delete = []

            for query, data in cache.items():
                # 1. Проверка на "протухание" (старше 60 дней)
                last_used = data.get("date")
                if last_used:
                    dt = datetime.datetime.fromisoformat(last_used)
                    if (now - dt).days > 60:
                        # Если рейтинг низкий — удаляем, если высокий — просто снижаем
                        if data.get("rating", 1.0) < 1.5:
                            to_delete.append(query)
                            continue
                        else:
                            data["rating"] = round(data["rating"] * 0.7, 2)

                # 2. Удаление технического мусора (если просочился)
                val = str(data.get("value", ""))
                if len(val) < 10 or "{" in val or "<br>" in val:
                    to_delete.append(query)

            # Удаление
            for q in to_delete:
                del cache[q]

            # Сохранение очищенных данных в обе зоны
            clean_data = json.dumps(cache, ensure_ascii=False, indent=2)
            for path in [self.cache_path, self.secure_path]:
                os.makedirs(os.path.dirname(path), exist_ok=True)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(clean_data)

            diff = original_count - len(cache)
            if diff > 0:
                print(f"✅ [Sanitizer] Удалено {diff} неактуальных записей.")
            
        except Exception as e:
            print(f"❌ [Sanitizer] Ошибка при очистке: {e}")

# Запуск как отдельного демона (если нужно протестировать отдельно)
if __name__ == "__main__":
    sanitizer = CacheSanitizer()
    asyncio.run(sanitizer.perform_cleanup())
