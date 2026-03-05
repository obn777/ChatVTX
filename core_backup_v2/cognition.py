# Путь к файлу: /home/obn7/NovBase/core/cognition.py

import time
import re
import os
import json
import asyncio
import datetime
import subprocess
from typing import Dict, Any, Optional

# Импорт модуля синхронизации (Бекап-система)
try:
    from .sync_guard import SyncGuard
except ImportError:
    SyncGuard = None

# Импорт модулей когнитивного слоя (NovBase Standard)
try:
    from .mid_cognition.modules.input_analyzer import input_analyzer
    from .mid_cognition.modules.meta_reasoner import meta_reasoner
    from .mid_cognition.modules.planner import mission_planner
    
    # Репетитор (Форма)
    from .mid_cognition.modules.linguistic_tutor import LinguisticTutor
    linguistic_tutor = LinguisticTutor()
    
    # Эмоции (Характер)
    from .mid_cognition.modules.emotional_core import EmotionalCore
    emotional_core = EmotionalCore()
    
    # Синтаксис (Голосовой ввод)
    from .mid_cognition.modules.syntactic_restorer import SyntacticRestorer
    syntax_restorer = SyntacticRestorer()
    
except ImportError:
    input_analyzer = meta_reasoner = mission_planner = None
    linguistic_tutor = emotional_core = syntax_restorer = None

# --- КЛАСС "ТРИ АПОСТОЛА" (ЦЕНТРАЛИЗОВАННЫЙ ОРКЕСТРАТОР) ---
class TriApostles:
    def __init__(self, engine):
        self.engine = engine
        self.facts_path = os.path.join(engine.cache_secure_dir, "apostles_facts.json")
        self.actions_cfg_path = os.path.join(engine.base_path, "configs/actions.json")
        self.user_facts = self._load_facts()

    def _load_facts(self):
        if os.path.exists(self.facts_path):
            try:
                with open(self.facts_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except: return {}
        return {}

    def _save_facts(self):
        try:
            with open(self.facts_path, "w", encoding="utf-8") as f:
                json.dump(self.user_facts, f, ensure_ascii=False, indent=2)
            # Синхронизация бекапа после записи
            if self.engine.guard:
                self.engine.guard.synchronize()
        except Exception as e:
            print(f"⚠️ [Apostles Save Error]: {e}")

    def process(self, text: str) -> Optional[str]:
        """Оркестрация: Действие -> Извлечение -> Запись."""
        t_lower = text.lower().strip()
        
        # 1. АПОСТОЛ ДЕЙСТВИЯ (Action): Перехват системных команд
        action_triggers = ["выполни", "сделай", "перезагрузи", "очисти", "запусти", "бекап", "синхронизируй"]
        if any(trigger in t_lower for trigger in action_triggers):
            action_res = self._handle_action(t_lower)
            if action_res: return action_res

        # 2. АПОСТОЛ ПУТИ (Recall): Проверка триггеров извлечения памяти
        recall_triggers = ["что ты запомнил", "повтори", "напомни", "какой", "какое", "назови", "расскажи что запомнил"]
        if any(phrase in t_lower for phrase in recall_triggers):
            return self._handle_recall(t_lower)

        # 3. АПОСТОЛ ВХОДА (Store): Проверка триггера записи в память
        if "запомни" in t_lower:
            return self._handle_store(text, t_lower)
            
        return None

    def _handle_action(self, t_lower: str) -> Optional[str]:
        """Логика выполнения системных команд через белый список."""
        if not os.path.exists(self.actions_cfg_path):
            return None 

        try:
            with open(self.actions_cfg_path, 'r') as f:
                whitelist = json.load(f)
        except: return "⚠️ [Апостол Действия]: Ошибка чтения configs/actions.json"

        cmd_key = None
        if "перезагрузи" in t_lower or "рестарт" in t_lower: cmd_key = "reboot_node"
        elif "бекап" in t_lower or "синхронизируй" in t_lower: cmd_key = "sync_memory"
        elif "очисти логи" in t_lower: cmd_key = "clean_logs"
        elif "deploy" in t_lower or "деплой" in t_lower: cmd_key = "deploy_fix"

        if cmd_key and cmd_key in whitelist:
            command = whitelist[cmd_key]
            try:
                subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"⚙️ [Апостол Действия]: Задача **{cmd_key}** запущена."
            except Exception as e:
                return f"❌ [Апостол Действия]: Сбой выполнения: {e}"
        return None

    def _handle_store(self, text: str, t_lower: str) -> str:
        cat, val = "note", ""
        if "число" in t_lower or "цифр" in t_lower:
            nums = re.findall(r"\d+", text)
            cat, val = "number", nums[0] if nums else ""
        elif "имя" in t_lower:
            parts = text.split("имя", 1)
            val = parts[1].strip().split()[0] if len(parts) > 1 else ""
            cat = "name"
        else:
            parts = text.split("запомни", 1)
            val = parts[1].strip().lstrip(": ") if len(parts) > 1 else ""
            cat = "note"

        if val:
            self.user_facts[cat] = val
            self._save_facts()
            return f"✅ [Апостол Выхода]: Запомнил {cat}: **{val}**."
        return "⚠️ [Апостол Входа]: Нечего сохранять."

    def _handle_recall(self, t_lower: str) -> str:
        cat = "note"
        if "число" in t_lower: cat = "number"
        elif "имя" in t_lower: cat = "name"
        
        val = self.user_facts.get(cat)
        if val:
            return f"📢 [Апостол Выхода]: В памяти по категории {cat}: **{val}**."
        
        if self.user_facts.get("note"):
            return f"В '{cat}' пусто, но есть заметка: **{self.user_facts.get('note')}**."
        return f"Память пуста по запросу: {cat}."

# --- ОСНОВНОЙ ДВИЖОК ---
class MidCognitionEngine:
    def __init__(self):
        self.base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.cache_local = os.path.join(self.base_path, "storage/cache.json")
        self.cache_secure_dir = os.path.expanduser("~/.novbase_protected_memory")
        self.cache_secure = os.path.join(self.cache_secure_dir, "master_cache.json")
        
        os.makedirs(os.path.dirname(self.cache_local), exist_ok=True)
        os.makedirs(self.cache_secure_dir, exist_ok=True)

        self.apostles = TriApostles(self)

        if SyncGuard:
            self.guard = SyncGuard(
                primary_paths=[self.cache_secure, self.cache_local, self.apostles.facts_path],
                backup_dir=os.path.join(self.cache_secure_dir, "shadow_vault")
            )
            self.guard.restore_integrity()
        else:
            self.guard = None

        self.cache_data = self._load_secured_cache()
        self._cache_lock = asyncio.Lock()
        
        print(f"✅ Когнитивный центр 10.6 запущен. Все системы активны.")

    def _load_secured_cache(self) -> Dict[str, Any]:
        for path in [self.cache_secure, self.cache_local]:
            if os.path.exists(path):
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        return json.load(f)
                except Exception: continue
        return {}

    async def force_sync_cache(self):
        async with self._cache_lock:
            try:
                data_str = json.dumps(self.cache_data, ensure_ascii=False, indent=2)
                with open(self.cache_local, "w", encoding="utf-8") as f: f.write(data_str)
                with open(self.cache_secure, "w", encoding="utf-8") as f: f.write(data_str)
                if self.guard: self.guard.synchronize()
            except Exception as e: print(f"⚠️ [Cache Sync Error] {e}")

    def analyze_input(self, text: str, **kwargs) -> Dict[str, Any]:
        processed_text = syntax_restorer.preprocess_voice_flow(text) if syntax_restorer else text

        apostle_response = self.apostles.process(processed_text)
        if apostle_response:
            return {"intent": "command_intercept", "semantic_block": apostle_response}

        if processed_text in self.cache_data:
            return {"intent": "cache_hit", "response": self.cache_data[processed_text]["value"]}

        if input_analyzer:
            analysis = input_analyzer.analyze(processed_text)
        else:
            analysis = {"intent": "unknown", "sentiment": "neutral"}
        
        analysis["raw_text"] = processed_text 
        analysis["semantic_block"] = self._priority_semantic_check(processed_text)
        
        if meta_reasoner:
            analysis["reasoning"] = meta_reasoner.analyze(processed_text, analysis=analysis, last_obj=kwargs.get('last_obj', 'ничего'))
        
        return analysis

    def _priority_semantic_check(self, text: str) -> str:
        t = text.lower()
        if any(cmd in t for cmd in ["сохрани", "запиши"]) and "/root" in t:
            return "Доступ к системным путям ограничен для твоей безопасности."
        return None

    def create_system_prompt(self, analysis: Dict[str, Any]) -> str:
        if analysis.get("intent") == "command_intercept":
            return analysis["semantic_block"]

        tutor_logic = linguistic_tutor.get_instruction() if linguistic_tutor else ""
        emotion_logic = emotional_core.get_instruction(analysis) if emotional_core else ""
        
        return (
            "Ты — Малыш, прагматичный инженерный модуль NovBase.\n"
            f"{tutor_logic}\n{emotion_logic}\n"
            "СТИЛЬ: Кратко, инженерный подход. Обращайся к пользователю только на 'ты'."
        )
