import json
import os
import datetime
import uuid
import threading

class AuthManager:
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.storage_dir = os.path.join(base_dir, "storage")
        self.users_path = os.path.join(self.storage_dir, "users_vtx.json")
        self.keys_path = os.path.join(self.storage_dir, "keys.json")
        self.ADMIN_PASSWORD = "2056"  # Твой мастер-код
        self.users = {}
        self.key_data = {"applications": [], "active_keys": {}}
        self.load_data()

    def load_data(self):
        """Загрузка базы данных с защитой от поврежденных файлов"""
        os.makedirs(self.storage_dir, exist_ok=True)

        # Загрузка базы пользователей
        if os.path.exists(self.users_path):
            with open(self.users_path, "r", encoding="utf-8") as f:
                try:
                    content = f.read().strip()
                    self.users = json.loads(content) if content else {}
                except:
                    self.users = {}

        # Загрузка базы ключей
        if os.path.exists(self.keys_path):
            with open(self.keys_path, "r", encoding="utf-8") as f:
                try:
                    content = f.read().strip()
                    self.key_data = json.loads(content) if content else {"applications": [], "active_keys": {}}
                    if "active_keys" not in self.key_data:
                        self.key_data["active_keys"] = {}
                except:
                    self.key_data = {"applications": [], "active_keys": {}}
        else:
            self.key_data = {"applications": [], "active_keys": {}}

    def save_all(self):
        """Синхронное сохранение данных"""
        try:
            with open(self.users_path, "w", encoding="utf-8") as f:
                json.dump(self.users, f, ensure_ascii=False, indent=4)
            with open(self.keys_path, "w", encoding="utf-8") as f:
                json.dump(self.key_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"❌ [AUTH ERROR] Не удалось сохранить базу: {e}")

    def verify_admin(self, password):
        return str(password) == self.ADMIN_PASSWORD

    def approve_key(self, user_id_or_note="Web Registration"):
        """Генерирует ключ и возвращает его"""
        return self.generate_pro_key(note=f"ID: {user_id_or_note}", target_status="Pro_Temporary")

    def generate_pro_key(self, note="Admin Generated", target_status="Pro_Temporary"):
        """Создать новый уникальный ключ в системе"""
        new_key = f"VTX-{uuid.uuid4().hex[:8].upper()}"
        self.key_data["active_keys"][new_key] = {
            "created_at": str(datetime.datetime.now()),
            "note": note,
            "is_used": False,
            "used_by_ip": None,
            "target_status": target_status
        }
        self.save_all()
        print(f"🔑 [AUTH] Сгенерирован ключ {new_key} для {note}")
        return new_key

    def ensure_pro_access(self, email, name, current_status):
        """
        Проверяет наличие ключа по Email и отправляет, если его нет.
        """
        if not email or "@" not in email:
            return None

        email_clean = email.lower().strip()
        existing_key = None

        # Ищем ключ в базе по email в заметке (note)
        for k, info in self.key_data.get("active_keys", {}).items():
            if email_clean in info.get("note", "").lower():
                existing_key = k
                break

        if not existing_key:
            existing_key = self.approve_key(email_clean)
            try:
                from core.mailer import send_vtx_key
                threading.Thread(target=send_vtx_key, args=(email_clean, name, existing_key)).start()
            except Exception as e:
                print(f"⚠️ [AUTH] Ошибка авто-отправки: {e}")

        return existing_key

    def check_access(self, ip, name="Гость", key=None, email=None):
        """
        ГЛАВНЫЙ УЗЕЛ: Проверка доступа с логикой авто-подхвата статуса.
        """
        # 1. Инициализация пользователя, если новый IP
        if ip not in self.users:
            self.users[ip] = {
                "name": name,
                "status": "Free",
                "email": email,
                "last_seen": str(datetime.datetime.now()),
                "activated_at": None,
                "key_used": None
            }

        user = self.users[ip]
        user["last_seen"] = str(datetime.datetime.now())
        if name != "Гость": user["name"] = name
        if email: user["email"] = email.lower().strip()

        # 2. АВТО-АВТОРИЗАЦИЯ (Если пришел Email, ищем ключ в базе)
        if user["status"] == "Free" and user.get("email"):
            for k, info in self.key_data.get("active_keys", {}).items():
                if user["email"] in info.get("note", "").lower():
                    # Нашли ключ для этой почты! Привязываем IP мгновенно
                    user["status"] = info.get("target_status", "Pro_Temporary")
                    user["key_used"] = k
                    user["activated_at"] = info.get("created_at")
                    print(f"✨ [AUTH] IP {ip} автоматически авторизован через Email: {user['email']}")
                    self.save_all()
                    break

        # 3. РУЧНАЯ АКТИВАЦИЯ ПО КЛЮЧУ (Если ввели в поле)
        if key and key.strip() in self.key_data.get("active_keys", {}):
            k_strip = key.strip()
            k_info = self.key_data["active_keys"][k_strip]

            # Если ключ еще не привязан к этому IP
            if user["key_used"] != k_strip:
                user["status"] = k_info.get("target_status", "Pro_Temporary")
                user["key_used"] = k_strip
                user["activated_at"] = str(datetime.datetime.now())
                k_info["is_used"] = True
                k_info["used_by_ip"] = ip
                self.save_all()
                print(f"🚀 [AUTH] {name} активировал ключ {k_strip}")

        # 4. КОНТРОЛЬ ЖИЗНЕННОГО ЦИКЛА (Pro_Temporary = 10 дней)
        if user["status"] == "Pro_Temporary" and user["activated_at"]:
            try:
                start_date = datetime.datetime.fromisoformat(user["activated_at"])
                days_passed = (datetime.datetime.now() - start_date).days
                if days_passed >= 10:
                    user["status"] = "Free"
                    self.save_all()
                if days_passed >= 30:
                    return True, "Expired_Data"
            except:
                pass

        return True, user["status"]
