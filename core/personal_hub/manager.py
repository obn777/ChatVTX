import os
import json
import shutil
import hashlib
import datetime

class PersonalHubManager:
    def __init__(self, base_path):
        self.base_path = base_path
        self.hub_path = os.path.join(base_path, "core/personal_hub/clients")
        os.makedirs(self.hub_path, exist_ok=True)

    def _get_user_dir(self, email_or_id):
        """Генерирует уникальный путь к папке клиента на основе хэша email или ключа"""
        user_hash = hashlib.md5(email_or_id.lower().strip().encode()).hexdigest()
        return os.path.join(self.hub_path, user_hash)

    def get_client_room(self, email_or_id):
        """Инициализирует личное пространство (ячейку) клиента"""
        user_dir = self._get_user_dir(email_or_id)

        if not os.path.exists(user_dir):
            os.makedirs(user_dir, exist_ok=True)
            os.makedirs(os.path.join(user_dir, "cache"), exist_ok=True)
            os.makedirs(os.path.join(user_dir, "exports"), exist_ok=True)

            # Профиль эволюции (DNA пользователя) с секцией безопасности
            profile = {
                "user_identifier": email_or_id,
                "created_at": str(datetime.datetime.now()),
                "ai_settings": {
                    "tone": "дружелюбный, но профессиональный",
                    "persona_traits": ["аналитика", "внимательность"],
                    "interaction_style": "стандартный"
                },
                "security": {
                    "hardware_id": None,
                    "activation_date": None
                },
                "learned_facts": [],
                "total_messages": 0,
                "compressed_sessions": 0,
                "last_update": str(datetime.datetime.now())
            }

            self._save_profile(user_dir, profile)

            with open(os.path.join(user_dir, "history.json"), "w", encoding="utf-8") as f:
                json.dump([], f)

            # Генерируем ПЕРВЫЙ динамический промпт сразу при создании
            self._write_local_prompt(user_dir, profile)
            print(f"✅ [HUB] Ячейка создана для: {email_or_id}")

        return user_dir

    def _save_profile(self, user_dir, profile):
        """Технический метод сохранения профиля в profile.json"""
        path = os.path.join(user_dir, "profile.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(profile, f, indent=4, ensure_ascii=False)

    def verify_device_access(self, email_or_id, incoming_device_id):
        """
        ПРОВЕРКА ЖЕЛЕЗА: Реализует логику 'Один ключ — одно устройство'.
        """
        user_dir = self._get_user_dir(email_or_id)
        profile_path = os.path.join(user_dir, "profile.json")

        if not os.path.exists(profile_path):
            return False, "Ключ не найден в системе."

        with open(profile_path, "r", encoding="utf-8") as f:
            profile = json.load(f)

        if "security" not in profile:
            profile["security"] = {"hardware_id": None}

        assigned_hwid = profile["security"].get("hardware_id")

        # Кейс 1: Первая активация ключа
        if not assigned_hwid:
            profile["security"]["hardware_id"] = incoming_device_id
            profile["security"]["activation_date"] = str(datetime.datetime.now())
            self._save_profile(user_dir, profile)
            print(f"🔒 [SECURITY] Ключ {email_or_id} привязан к устройству {incoming_device_id}")
            return True, "Устройство успешно привязано."

        # Кейс 2: Проверка соответствия при повторных входах
        if assigned_hwid == incoming_device_id:
            return True, "Доступ разрешен."

        # Кейс 3: Попытка зайти с другого железа
        print(f"🚫 [SECURITY ALERT] Попытка шеринга ключа {email_or_id}!")
        return False, "Этот ключ уже привязан к другому устройству."

    def _write_local_prompt(self, user_dir, profile):
        """ФОРМИРОВАТЕЛЬ ЛОКАЛЬНОГО ПРОМПТА."""
        s = profile["ai_settings"]
        facts_list = profile.get("learned_facts", [])
        facts = "\n- ".join(facts_list[-10:]) if facts_list else "данные уточняются"

        prompt_content = (
            f"ТЫ — МАЛЫШКА VTX. Твой DNA адаптирован под клиента.\n"
            f"ИДЕНТИФИКАТОР: {profile['user_identifier']}\n"
            f"СТИЛЬ: {s['tone']}. ПОДАЧА: {s['interaction_style']}.\n"
            f"БАЗА ЗНАНИЙ О ВЛАДЕЛЬЦЕ:\n- {facts}\n\n"
            f"ИНСТРУКЦИЯ: Используй эти знания для персонализации."
        )

        try:
            for filename in ["dna_prompt.txt", "system_prompt.txt"]:
                path = os.path.join(user_dir, filename)
                with open(path, "w", encoding="utf-8") as f:
                    f.write(prompt_content)
            return True
        except Exception as e:
            print(f"⚠️ [HUB ERROR] Сбой записи промпта: {e}")
            return False

    def get_local_prompt(self, email_or_id):
        """Метод для быстрого чтения готового промпта из файла комнаты"""
        user_dir = self._get_user_dir(email_or_id)
        prompt_path = os.path.join(user_dir, "dna_prompt.txt")

        if os.path.exists(prompt_path):
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read()
        return "Ты — Малышка VTX, персональный ассистент."

    def get_dynamic_prompt(self, email_or_id):
        """Алиас для совместимости"""
        return self.get_local_prompt(email_or_id)

    def update_client_data(self, email_or_id, user_text, ai_response):
        """Обновление истории и DNA."""
        user_dir = self.get_client_room(email_or_id)
        history_path = os.path.join(user_dir, "history.json")
        profile_path = os.path.join(user_dir, "profile.json")

        try:
            # 1. История
            with open(history_path, "r", encoding="utf-8") as f:
                history = json.load(f)
            history.append({
                "timestamp": str(datetime.datetime.now()),
                "user": user_text,
                "ai": ai_response
            })
            history = self._compress_experience(user_dir, history)
            with open(history_path, "w", encoding="utf-8") as f:
                json.dump(history, f, indent=4, ensure_ascii=False)

            # 2. Профиль
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
            profile["total_messages"] += 1
            updated_profile = self._supervisor_evolution(profile, user_text, ai_response)
            self._save_profile(user_dir, updated_profile)

            # 3. Промпт
            self._write_local_prompt(user_dir, updated_profile)

        except Exception as e:
            print(f"⚠️ [HUB ERROR] Сбой обновления ячейки {email_or_id}: {e}")

    def _supervisor_evolution(self, profile, user_text, ai_response):
        """Интеллектуальный анализ интересов пользователя."""
        triggers = ["работаю над", "мой проект", "меня зовут", "люблю", "ненавижу", "цель", "занимаюсь"]
        user_lower = user_text.lower()

        for trigger in triggers:
            if trigger in user_lower and 10 < len(user_text) < 200:
                date_tag = datetime.datetime.now().strftime("%d.%m.%y")
                fact = f"[{date_tag}] {user_text.strip()}"
                if fact not in profile["learned_facts"]:
                    profile["learned_facts"].append(fact)
                    if len(profile["learned_facts"]) > 15:
                        profile["learned_facts"].pop(0)

        if len(user_text) > 400:
            profile["ai_settings"]["interaction_style"] = "развернутый технический анализ"
        elif any(word in user_lower for word in ["коротко", "лаконично", "кратко"]):
            profile["ai_settings"]["interaction_style"] = "максимально краткий"
            profile["ai_settings"]["tone"] = "деловой, холодный"

        profile["last_update"] = str(datetime.datetime.now())
        return profile

    def _compress_experience(self, user_dir, history):
        """Архивация старых сообщений."""
        if len(history) <= 50:
            return history

        profile_path = os.path.join(user_dir, "profile.json")
        try:
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)
            profile["compressed_sessions"] += 1
            archive_stamp = f"Архив сессии {profile['compressed_sessions']}: беседа от {history[0]['timestamp'][:10]}"
            if archive_stamp not in profile["learned_facts"]:
                profile["learned_facts"].insert(0, archive_stamp)
            self._save_profile(user_dir, profile)
        except Exception as e:
            print(f"⚠️ [CLEANER ERROR] {e}")

        return history[20:]

    def purge_client(self, email_or_id):
        """Удаление данных клиента."""
        user_dir = self._get_user_dir(email_or_id)
        if os.path.exists(user_dir):
            shutil.rmtree(user_dir)
            return True
        return False

    def create_digital_clone(self, email_or_id):
        """Создание ZIP-архива DNA."""
        user_dir = self._get_user_dir(email_or_id)
        if not os.path.exists(user_dir): return None
        archive_name = f"vtx_dna_{hashlib.md5(email_or_id.encode()).hexdigest()[:8]}"
        archive_base = os.path.join(user_dir, "exports", archive_name)
        shutil.make_archive(archive_base, 'zip', user_dir)
        return archive_base + ".zip"
