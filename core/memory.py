import json
import os
import difflib
import shutil
from datetime import datetime

class MemoryManager:
    def __init__(self, file_path="/root/NovBase/data/long_term_memory.json"):
        # Основные пути
        self.file_path = file_path
        self.knowledge_path = "/root/NovBase/data/knowledge.json"
        self.users_db_path = "/root/NovBase/data/users_db.json"
        
        # --- ЗАЩИЩЕННАЯ ЗОНА (Nitro-оптимизация) ---
        self.secure_dir = os.path.expanduser("~/.novbase_protected_memory")
        self.secure_knowledge = os.path.join(self.secure_dir, "knowledge_backup.json")
        self.secure_users = os.path.join(self.secure_dir, "users_backup.json")
        
        self._ensure_dirs()
        self._restore_from_secure_zone()

        # Инициализация пустых файлов, если их нет
        if not os.path.exists(self.users_db_path):
            self._save_json(self.users_db_path, {"users": {}})
        if not os.path.exists(self.knowledge_path):
            self._save_json(self.knowledge_path, {})
        if not os.path.exists(self.file_path):
            self._create_default_memory()

    def _ensure_dirs(self):
        """Создание необходимых директорий."""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
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
        """Сохранение JSON и синхронизация с защищенной зоной."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        
        # Резервное копирование знаний и базы пользователей
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

    # --- СЛОЙ: УПРАВЛЕНИЕ ПОЛЬЗОВАТЕЛЯМИ (IP & Gender) ---
    
    def identify_user(self, ip):
        """Поиск имени пользователя по списку IP."""
        db = self._load_json(self.users_db_path)
        for name, info in db.get("users", {}).items():
            if ip in info.get("ips", []):
                return name
        return None

    def register_user(self, name, ip, gender="unknown"):
        """Регистрация нового пользователя или обновление данных."""
        db = self._load_json(self.users_db_path)
        if "users" not in db: db["users"] = {}
        
        if name not in db["users"]:
            db["users"][name] = {"ips": [], "gender": gender, "created": str(datetime.now())}
        
        if ip not in db["users"][name]["ips"]:
            db["users"][name]["ips"].append(ip)
            db["users"][name]["ips"] = db["users"][name]["ips"][-10:] # Лимит прыжков
        
        if gender != "unknown":
            db["users"][name]["gender"] = gender
            
        self._save_json(self.users_db_path, db)
        return db["users"][name]

    def get_user_context(self, name):
        """Возвращает гендерную инструкцию для LLM."""
        db = self._load_json(self.users_db_path)
        user = db.get("users", {}).get(name, {})
        gender = user.get("gender", "unknown")
        
        if gender == "мужчина":
            return "Собеседник — МУЖЧИНА. Общайся прямо, без уменьшительно-ласкательных форм."
        elif gender == "женщина":
            return "Собеседник — ЖЕНЩИНА. Общайся мягко, эмоционально, как подруга."
        return "Веди диалог в нейтральном стиле."

    # --- СЛОЙ: ДИАЛОГОВАЯ ПАМЯТЬ ---
    
    def save_memory(self, user_query, ai_response):
        data = self._load_json(self.file_path)
        if not data: data = {"history": []}
        
        entry = {
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "q": user_query,
            "a": ai_response
        }
        data.setdefault("history", []).append(entry)
        data["history"] = data["history"][-15:] # Окно контекста
        self._save_json(self.file_path, data)

    def _create_default_memory(self):
        initial_data = {
            "system_start": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "history": []
        }
        self._save_json(self.file_path, initial_data)

    # --- СЛОЙ: БАЗА ЗНАНИЙ (Recall & Add) ---

    def recall_knowledge(self, query):
        """Тот самый метод, которого не хватало для ответа про Байкал."""
        kb = self._load_json(self.knowledge_path)
        if not kb: return ""
        
        keys = list(kb.keys())
        matches = difflib.get_close_matches(query.lower(), keys, n=1, cutoff=0.5)
        
        if matches:
            fact = kb[matches[0]]
            return f"\n[ФАКТ ИЗ ТВОИХ ЗНАНИЙ]: {fact['content']}\n"
        return ""

    def add_knowledge(self, topic, content):
        kb = self._load_json(self.knowledge_path)
        kb[topic.lower()] = {
            "content": content,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self._save_json(self.knowledge_path, kb)

    def get_med_guard(self):
        """Юридический предохранитель."""
        return "Запрещено давать медицинские советы. Ты не врач."
