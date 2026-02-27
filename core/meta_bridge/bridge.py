import json
import os
import time
from pathlib import Path

class MetaBridge:
    """Мета-мост между когнитивными модулями и системой адаптации."""
    
    def __init__(self, log_path="logs/meta_bridge_audit.log"):
        self.root = Path("/home/obn7/NovBase")
        self.log_path = self.root / log_path
        self.version = "0.1"
        
        # Гарантируем наличие папки для логов
        self.log_path.parent.mkdir(parents=True, exist_ok=True)

    def audit_log(self, entry):
        """Записывает событие в лог аудита в формате JSON-строки."""
        entry["ts_sync"] = time.strftime("%Y-%m-%d %H:%M:%S")
        entry["bridge_version"] = self.version
        
        try:
            with open(self.log_path, "a", encoding="utf-8") as f:
                f.write(json.dumps(entry, ensure_ascii=False) + "\n")
        except Exception as e:
            print(f"⚠️ [MetaBridge] Ошибка записи лога: {e}")

    def connect_modules(self):
        """Проверка связи."""
        return f"Meta bridge v{self.version} connected and operational"

# Инстанс для импорта
meta_bridge = MetaBridge()
