def _generate_local_prompt(self, user_dir, profile):
        """
        ФОРМИРОВАТЕЛЬ ЛОКАЛЬНОГО ПРОМПТА.
        Создает физический файл инструкции внутри комнаты клиента.
        """
        s = profile["ai_settings"]
        facts = "\n- ".join(profile["learned_facts"][-10:]) or "Личные данные не установлены."

        # Собираем кастомную личность
        local_instruction = (
            f"ТЫ — МАЛЫШКА VTX (Локальный узел: {profile['user_identifier'][:5]}).\n"
            f"ТВОЙ СТИЛЬ: {s['tone']}.\n"
            f"ТВОЙ ФОРМАТ ОТВЕТОВ: {s['interaction_style']}.\n"
            f"ЗНАНИЯ О СОБЕСЕДНИКЕ:\n- {facts}\n\n"
            f"ДИРЕКТИВА: Ты эволюционируешь вместе с пользователем. Твоя задача — быть полезным "
            f"соратником, учитывая его интерес к социологии и технологиям."
        )

        prompt_path = os.path.join(user_dir, "system_prompt.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(local_instruction)

        return prompt_path

    def update_client_data(self, email_or_id, user_text, ai_response):
        """Обновляем профиль И пересобираем локальный файл промпта."""
        user_dir = self.get_client_room(email_or_id)
        profile_path = os.path.join(user_dir, "profile.json")

        try:
            # (Твой код загрузки профиля...)
            with open(profile_path, "r", encoding="utf-8") as f:
                profile = json.load(f)

            # 1. Эволюционируем профиль через Supervisor
            updated_profile = self._supervisor_evolution(profile, user_text, ai_response)

            # 2. Сохраняем профиль
            with open(profile_path, "w", encoding="utf-8") as f:
                json.dump(updated_profile, f, indent=4, ensure_ascii=False)

            # 3. КЛЮЧЕВОЙ МОМЕНТ: Обновляем локальный файл инструкции
            self._generate_local_prompt(user_dir, updated_profile)

        except Exception as e:
            print(f"⚠️ [HUB ERROR] Сбой обновления локального промпта: {e}")
