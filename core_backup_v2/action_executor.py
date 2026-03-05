import os
import datetime
import subprocess

class ActionExecutor:
    def __init__(self, base_path="/home/obn7/NovBase"):
        self.base_path = base_path
        self.docs_path = os.path.join(base_path, "storage/docs")
        self.sync_script = os.path.join(base_path, "sync.sh")
        os.makedirs(self.docs_path, exist_ok=True)

    def execute(self, cognition_data: dict, last_reply: str):
        """
        Проверяет план и выполняет физические действия + синхронизацию.
        """
        plan = cognition_data.get("mission_plan", "")
        
        if "action: file_save" in plan:
            saved_path = self._save_to_file(last_reply)
            if saved_path:
                # После сохранения вызываем GitHub Sync
                self._sync_to_github()
            return saved_path
        
        return None

    def _save_to_file(self, content: str):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"mission_report_{timestamp}.md"
        file_path = os.path.join(self.docs_path, filename)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# Отчет системы NovBase\n")
                f.write(f"Дата: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
                f.write(content)
            print(f"💾 [ActionExecutor] Файл сохранен: {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ [ActionExecutor] Ошибка записи: {e}")
            return None

    def _sync_to_github(self):
        """
        Запускает bash-скрипт синхронизации.
        """
        if os.path.exists(self.sync_script):
            try:
                # Запускаем sync.sh в фоновом режиме, чтобы не тормозить ответ пользователю
                subprocess.Popen(["bash", self.sync_script], 
                                 stdout=subprocess.DEVNULL, 
                                 stderr=subprocess.DEVNULL)
                print(f"🚀 [ActionExecutor] Запущена синхронизация с ChatVTX...")
            except Exception as e:
                print(f"❌ [ActionExecutor] Ошибка запуска синхронизации: {e}")
