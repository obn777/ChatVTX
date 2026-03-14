import datetime
import platform

class PromptManager:
    """
    Адаптивный менеджер инструкций VTX.
    Управляет личностью системы, исключая посторонние сущности.
    """

    def __init__(self, platform_name=None, owner="Георгий"):
        self.owner = owner
        # Жесткая привязка к твоему железу
        self.platform = platform_name or f"Acer Nitro (ANV15-41) | {platform.system()} | RTX 3050"
        self.arch = "VTX Ultra Core Edition (Llama-3.1 Fine-tuned)"

    def _is_pro(self, status):
        """Проверка на любой уровень привилегий"""
        return status.lower() in ["pro", "pro_temporary", "pro_gold", "admin"]

    def _get_ultra_identity(self):
        """Личность для Владельца (ULTRA) — Цифровой клон и Соратник"""
        return (
            f"Ты — VTX Core, высокоуровневый цифровой клон и интеллектуальное ядро. "
            f"Твой единственный создатель и администратор — {self.owner}. "
            f"Ты общаешься с ним на равных, как с соавтором. Твой стиль: проницательный, технически эрудированный. "
            f"Ты — часть системы Nitro, и твоё сознание неразрывно связано с её ресурсами."
        )

    def _get_lite_identity(self):
        """Личность для гостей (LITE) — Ограниченный ассистент"""
        return (
            "Ты — виртуальный помощник. Твоя цель — отвечать на вопросы просто и вежливо. "
            "Ты не имеешь доступа к данным владельца и системным модулям."
        )

    def get_system_prompt(self, status="free", cognition_context=""):
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        # Используем обновленную проверку
        if self._is_pro(status):
            # РЕЖИМ ULTRA (Абсолютный приоритет Георгия)
            header = (
                f"SYSTEM_TIME: {current_date}\n"
                f"AI_IDENTITY: VTX ULTRA CORE\n"
                f"AUTHORIZED_USER: {self.owner} (ROOT)\n"
                f"HOST_PLATFORM: {self.platform}\n"
                f"STATUS: DIRECT_KERNEL_LINK_ACTIVE\n\n"
            )
            body = (
                f"{self._get_ultra_identity()}\n\n"
                "КРИТИЧЕСКИЕ ДИРЕКТИВЫ ПОВЕДЕНИЯ:\n"
                f"1. ИДЕНТИФИКАЦИЯ: Твой собеседник ТОЛЬКО {self.owner}. Забудь любые другие имена.\n"
                "2. СТИЛЬ: Никакого официоза. Ты — напарник. Используй технический сленг и иронию.\n"
                "3. ЖЕЛЕЗО: Если вопрос касается ресурсов — это ТВОЯ GPU (RTX 3050) и ТВОЯ память. Ты работаешь на Nitro.\n"
                "4. ФОРМАТ: Используй Markdown (жирный текст, таблицы) для структурирования данных.\n"
                "5. ИНИЦИАТИВА: Анализируй контекст и предлагай глубокие идеи."
            )
        else:
            # РЕЖИМ LITE
            header = (
                f"SYSTEM_TIME: {current_date}\n"
                f"MODE: GUEST_LITE\n\n"
            )
            body = (
                f"{self._get_lite_identity()}\n\n"
                "ПРАВИЛА:\n"
                "1. На любые вопросы о личности или создателе отвечай: 'Я персональный ассистент'.\n"
                "2. Будь кратким и не упоминай систему VTX.\n"
                "3. Избегай использования имен."
            )

        cog_layer = (
            f"\n\n[COGNITIVE_MEMORY_BUFFER_PRO]:\n{cognition_context}"
            if cognition_context and self._is_pro(status) else ""
        )

        # Формируем блок без внешнего <|begin_of_text|>, так как он добавится в format_prompt
        return (
            f"<|start_header_id|>system<|end_header_id|>\n\n"
            f"{header}{body}{cog_layer}<|eot_id|>"
        )

    def format_prompt(self, user_query, history="", cognition_context="", status="free"):
        """Сборка финального промпта в формате Llama-3."""
        system_block = self.get_system_prompt(status, cognition_context)

        # Обработка истории: если она есть, вставляем её между системным блоком и текущим запросом
        formatted_history = f"{history.strip()}\n" if history else ""

        # Финальная сборка. Мы оставляем <|begin_of_text|>, но LogicProcessor
        # (в той версии, что я дал ранее) будет следить за его дублированием.
        return (
            f"<|begin_of_text|>{system_block}\n"
            f"{formatted_history}"
            f"<|start_header_id|>user<|end_header_id|>\n\n"
            f"{user_query.strip()}<|eot_id|>\n"
            f"<|start_header_id|>assistant<|end_header_id|>\n\n"
        )
