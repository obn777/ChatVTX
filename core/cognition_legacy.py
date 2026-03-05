import os
import json
import asyncio
import re
from typing import Dict, Any, Optional

# ===============================
# Optional Sync Layer
# ===============================

try:
    from .sync_guard import SyncGuard
except ImportError:
    SyncGuard = None


# ===============================
# TriApostles Orchestrator
# ===============================

class TriApostles:
    """
    Центральный оркестратор команд, памяти и системных действий.
    """

    def __init__(self, engine):
        self.engine = engine
        self.base_path = engine.base_path
        self.facts_path = os.path.join(
            engine.cache_secure_dir,
            "apostles_facts.json"
        )
        self.user_facts = self._load_facts()

    # ------------------------------

    def _load_facts(self):
        if os.path.exists(self.facts_path):
            try:
                with open(self.facts_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return {}
        return {}

    # ------------------------------

    def _save_facts(self):
        try:
            with open(self.facts_path, "w", encoding="utf-8") as f:
                json.dump(self.user_facts, f, ensure_ascii=False, indent=2)

            if getattr(self.engine, "guard", None):
                self.engine.guard.synchronize()

        except Exception as e:
            print(f"⚠ [Apostles Save Error]: {e}")

    # ------------------------------

    def process(self, text: str) -> Optional[str]:
        """
        Минимальная обработка команд.
        """

        t = text.lower().strip()

        if "запомни" in t:
            return self._store(text)

        if any(word in t for word in ["что ты запомнил", "напомни"]):
            return self._recall()

        return None

    # ------------------------------

    def _store(self, text: str) -> str:
        parts = text.split("запомни", 1)
        value = parts[1].strip() if len(parts) > 1 else ""

        if value:
            self.user_facts["note"] = value
            self._save_facts()
            return f"✅ Запомнил: {value}"

        return "⚠ Нечего сохранять."

    # ------------------------------

    def _recall(self) -> str:
        value = self.user_facts.get("note")
        if value:
            return f"📌 В памяти: {value}"
        return "Память пуста."


# ===============================
# Mid Cognition Engine (Simplified)
# ===============================

class MidCognitionEngine:
    """
    Упрощённый когнитивный слой,
    совместимый с новой архитектурой.
    """

    def __init__(self):
        self.base_path = os.path.dirname(
            os.path.dirname(os.path.abspath(__file__))
        )

        self.cache_local = os.path.join(
            self.base_path, "storage/cache.json"
        )

        self.cache_secure_dir = os.path.expanduser(
            "~/.novbase_protected_memory"
        )

        self.cache_secure = os.path.join(
            self.cache_secure_dir, "master_cache.json"
        )

        os.makedirs(self.cache_secure_dir, exist_ok=True)

        self.apostles = TriApostles(self)

        self.guard = None
        if SyncGuard:
            try:
                self.guard = SyncGuard(
                    primary_paths=[
                        self.cache_secure,
                        self.cache_local,
                        self.apostles.facts_path
                    ],
                    backup_dir=os.path.join(
                        self.cache_secure_dir,
                        "shadow_vault"
                    )
                )
                self.guard.restore_integrity()
            except Exception:
                self.guard = None

        self.cache_data = self._load_cache()
        self._cache_lock = asyncio.Lock()

        print("✅ Cognition layer initialized (clean mode).")

    # ------------------------------

    def _load_cache(self) -> Dict[str, Any]:
        for path in [self.cache_secure, self.cache_local]:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception:
                    continue
        return {}

    # ------------------------------

    async def force_sync_cache(self):
        async with self._cache_lock:
            try:
                data = json.dumps(
                    self.cache_data,
                    ensure_ascii=False,
                    indent=2
                )

                with open(self.cache_local, "w", encoding="utf-8") as f:
                    f.write(data)

                with open(self.cache_secure, "w", encoding="utf-8") as f:
                    f.write(data)

                if self.guard:
                    self.guard.synchronize()

            except Exception as e:
                print(f"⚠ Cache Sync Error: {e}")

    # ------------------------------

    def analyze_input(self, text: str) -> Dict[str, Any]:
        """
        Базовый анализ без старых mid_cognition зависимостей.
        """

        apostle_response = self.apostles.process(text)
        if apostle_response:
            return {
                "intent": "command_intercept",
                "semantic_block": apostle_response
            }

        if text in self.cache_data:
            return {
                "intent": "cache_hit",
                "response": self.cache_data[text].get("value")
            }

        # Минимальный универсальный анализ
        return {
            "intent": "general",
            "raw_text": text,
            "sentiment": "neutral"
        }

    # ------------------------------

    def create_system_prompt(self, analysis: Dict[str, Any]) -> str:
        """
        Генерация системного промпта.
        """

        if analysis.get("intent") == "command_intercept":
            return analysis["semantic_block"]

        return (
            "Ты — инженерный модуль NovBase.\n"
            "Отвечай кратко, структурировано и по делу.\n"
            "Обращайся к пользователю на 'ты'."
        )
