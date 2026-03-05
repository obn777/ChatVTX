# Путь к файлу: /home/obn7/NovBase/core/sync_guard.py

import os
import shutil
import json

class SyncGuard:
    def __init__(self, primary_paths: list, backup_dir: str):
        self.primary_paths = primary_paths
        self.backup_dir = backup_dir
        os.makedirs(self.backup_dir, exist_ok=True)

    def synchronize(self):
        """Зеркалирование основных файлов конфигурации в защищенное хранилище."""
        for path in self.primary_paths:
            if os.path.exists(path):
                filename = os.path.basename(path)
                backup_path = os.path.join(self.backup_dir, f"shadow_{filename}")
                
                try:
                    # Простая проверка: если размер или время изменения отличаются — копируем
                    if not os.path.exists(backup_path) or \
                       os.path.getmtime(path) > os.path.getmtime(backup_path):
                        shutil.copy2(path, backup_path)
                        # print(f"✅ [SyncGuard]: {filename} захеширован.")
                except Exception as e:
                    print(f"⚠️ [SyncGuard Error]: {e}")

    def restore_integrity(self):
        """Восстановление поврежденных или отсутствующих файлов из тени."""
        for path in self.primary_paths:
            if not os.path.exists(path):
                filename = os.path.basename(path)
                backup_path = os.path.join(self.backup_dir, f"shadow_{filename}")
                if os.path.exists(backup_path):
                    shutil.copy2(backup_path, path)
                    print(f"🛠 [SyncGuard]: Восстановлен {filename} из тени.")
