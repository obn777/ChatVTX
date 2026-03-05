import json
import os
import shutil
from datetime import datetime

class MemoryManager:
    def __init__(self):
        self.base_dir = "/home/obn7/NovBase/storage"
        self.history_path = os.path.join(self.base_dir, "cache.json")
        self.knowledge_path = os.path.join(self.base_dir, "knowledge.json")
        self.users_db_path = os.path.join(self.base_dir, "users_db.json")
        
        # ЗАЩИЩЕННАЯ ЗОНА (Nitro/Termux)
        self.secure_dir = os.path.expanduser("~/.novbase_protected_memory")
        self.secure_backups = {
            "knowledge": os.path.join(self.secure_dir, "knowledge_backup.json"),
            "users": os.path.join(self.secure_dir, "users_backup.json")
        }
        
        self._ensure_dirs()
        self._restore_from_secure_zone()

    def _ensure_dirs(self):
        os.makedirs(self.base_dir, exist_ok=True)
        os.makedirs(self.secure_dir, exist_ok=True)

    def _restore_from_secure_zone(self):
        """Восстановление критических данных при переустановке."""
        for key, work_path in [("knowledge", self.knowledge_path), ("users", self.users_db_path)]:
            secure_path = self.secure_backups[key]
            if not os.path.exists(work_path) and os.path.exists(secure_path):
                shutil.copy2(secure_path, work_path)
                print(f"🧠 [Memory] {key} восстановлен из защиты.")

    def _save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # Бекапим только важные файлы (историю диалогов бекапить не обязательно)
        for key, work_path in [("knowledge", self.knowledge_path), ("users", self.users_db_path)]:
            if path == work_path:
                shutil.copy2(path, self.secure_backups[key])

    def _load_json(self, path):
        if not os.path.exists(path): return {}
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}

    # --- РАБОТА С ФАКТАМИ (Длинная память) ---
    def store_fact(self, user_query, info):
        """Запоминает конкретные факты (числа, имена)."""
        db = self._load_json(self.knowledge_path)
        # Чистим запрос от "запомни", "запиши"
        key = user_query.lower().replace("запомни", "").replace("число", "").strip()
        db[key] = {
            "value": info,
            "date": str(datetime.now()),
            "type": "fact"
        }
        self._save_json(self.knowledge_path, db)

    def recall_fact(self, query):
        """Ищет факт в базе знаний."""
        db = self._load_json(self.knowledge_path)
        query = query.lower()
        for key, data in db.items():
            if key in query or query in key:
                return data["value"]
        return None

    # --- РАБОТА С КОНТЕКСТОМ (Короткая память) ---
    def save_to_history(self, q, a):
        history = self._load_json(self.history_path)
        if not isinstance(history, list): history = []
        
        entry = {
            "t": datetime.now().strftime("%H:%M"),
            "q": q,
            "a": a
        }
        history.append(entry)
        self._save_json(self.history_path, history[-10:]) # Храним последние 10 фраз

    def get_formatted_history(self):
        history = self._load_json(self.history_path)
        if not history: return ""
        lines = []
        for e in history:
            lines.append(f"User: {e['q']}\nAssistant: {e['a']}")
        return "\n".join(lines)

    # --- ПОЛЬЗОВАТЕЛИ ---
    def get_user_gender_prompt(self, ip):
        db = self._load_json(self.users_db_path)
        # Поиск по IP
        for name, info in db.get("users", {}).items():
            if ip in info.get("ips", []):
                g = info.get("gender", "unknown")
                if g == "мужчина": return "Собеседник: МУЖЧИНА. Общайся прямо."
                if g == "женщина": return "Собеседник: ЖЕНЩИНА. Общайся мягко."
        return ""
