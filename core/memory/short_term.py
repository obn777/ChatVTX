import json
import os
import difflib
import shutil
from datetime import datetime

class MemoryManager:
    def __init__(self, file_path="data/long_term_memory.json"):
        # Пути проекта
        self.file_path = file_path
        self.knowledge_path = "data/knowledge.json"
        self.users_db_path = "data/users_db.json" # Реестр всех пользователей
        
        # --- ЗАЩИЩЕННАЯ ЗОНА ---
        self.secure_dir = os.path.expanduser("~/.novbase_protected_memory")
        self.secure_knowledge = os.path.join(self.secure_dir, "knowledge_backup.json")
        self.secure_users = os.path.join(self.secure_dir, "users_backup.json")
        
        self._ensure_dirs()
        self._restore_from_secure_zone()

        # Инициализация файлов
        if not os.path.exists(self.users_db_path):
            self._save_json(self.users_db_path, {"users": {}})

    def _ensure_dirs(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        os.makedirs(os.path.dirname(self.users_db_path), exist_ok=True)
        os.makedirs(self.secure_dir, exist_ok=True)

    def _restore_from_secure_zone(self):
        """Восстановление критических данных из скрытого хранилища."""
        for work, secure in [(self.knowledge_path, self.secure_knowledge), 
                             (self.users_db_path, self.secure_users)]:
            if not os.path.exists(work) and os.path.exists(secure):
                try:
                    shutil.copy2(secure, work)
                    print(f"🧠 [Memory] Данные {os.path.basename(work)} восстановлены.")
                except Exception as e:
                    print(f"⚠️ Ошибка восстановления: {e}")

    def _save_json(self, path, data):
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # Резервное копирование критических данных
        if "knowledge.json" in path or "users_db.json" in path:
            secure_path = self.secure_knowledge if "knowledge" in path else self.secure_users
            try:
                shutil.copy2(path, secure_path)
            except: pass

    def _load_json(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return {}

    # --- НОВЫЙ СЛОЙ: УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ И IP ---
    
    def identify_user(self, ip):
        """Поиск имени пользователя по IP."""
        db = self._load_json(self.users_db_path)
        for name, info in db.get("users", {}).items():
            if ip in info.get("ips", []):
                return name
        return None

    def register_user(self, name, ip, gender="unknown"):
        """Регистрация или обновление IP/пола."""
        db = self._load_json(self.users_db_path)
        if "users" not in db: db["users"] = {}
        
        if name not in db["users"]:
            db["users"][name] = {"ips": [], "gender": gender, "created": str(datetime.now())}
        
        if ip not in db["users"][name]["ips"]:
            db["users"][name]["ips"].append(ip)
            db["users"][name]["ips"] = db["users"][name]["ips"][-10:] # Лимит 10 прыжков
        
        if gender != "unknown":
            db["users"][name]["gender"] = gender
            
        self._save_json(self.users_db_path, db)
        return db["users"][name]

    def get_user_context(self, name):
        """Возвращает гендерные инструкции и статус."""
        db = self._load_json(self.users_db_path)
        user = db.get("users", {}).get(name, {})
        gender = user.get("gender", "unknown")
        
        if gender == "мужчина":
            return "Собеседник — МУЖЧИНА. Общайся уважительно, прямо, забудь про уменьшительно-ласкательные суффиксы."
        elif gender == "женщина":
            return "Собеседник — ЖЕНЩИНА. Общайся как подруга, будь эмоциональной и мягкой."
        return "Пол собеседника неясен. Веди себя нейтрально."

    # --- СЛОЙ 1: ДИАЛОГОВАЯ ПАМЯТЬ ---
    def save_memory(self, user_query, ai_response):
        # (Твой оригинальный код с небольшим фиксом пути)
        data = self._load_json(self.file_path)
        if not data: data = {"history": []}
        
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "q": user_query,
            "a": ai_response
        }
        data.setdefault("history", []).append(entry)
        data["history"] = data["history"][-15:] 
        self._save_json(self.file_path, data)

    # --- БЕЗОПАСНОСТЬ (Медицина) ---
    def get_med_guard(self):
        return ("\n[ЗАКОН]: Тебе запрещено называть себя врачом или специалистом. "
                "Не давай прямых мед-инструкций. Ты просто собеседник.")

    # ... (остальные твои методы recall_knowledge и т.д. остаются без изменений)
