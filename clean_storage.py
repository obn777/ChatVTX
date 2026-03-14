import json
import os

BASE_DIR = "/home/obn7/NovBase/storage"
FILES = ["keys.json", "limits.json", "users_vtx.json", "cache.json"]

def fix_storage():
    print("🧹 Начинаю зачистку старых хвостов...")
    
    # 1. Обнуляем лимиты (чтобы не выбрасывало в free по ошибке)
    limits_path = os.path.join(BASE_DIR, "limits.json")
    with open(limits_path, 'w') as f:
        json.dump({"admins": ["твой_ключ"], "global_limit": 99999}, f)
        print("✅ Лимиты сброшены.")

    # 2. Чистим кэш сессий (чтобы забыть "глючные" входы)
    cache_path = os.path.join(BASE_DIR, "cache.json")
    if os.path.exists(cache_path):
        with open(cache_path, 'w') as f:
            json.dump({}, f)
        print("✅ Кэш сессий очищен.")

    # 3. Проверка ключей
    keys_path = os.path.join(BASE_DIR, "keys.json")
    # Убедись, что твой ключ там первый и главный
    with open(keys_path, 'w') as f:
        json.dump({"твой_админ_ключ": "ultra", "guest": "free"}, f)
        print("✅ Ключи синхронизированы.")

if __name__ == "__main__":
    fix_storage()
