import os
import datetime
import subprocess
from core.config import config

class ActionExecutor:
    """
    Класс реализации физических действий. 
    Отвечает за сохранение отчетов и запуск внешней синхронизации.
    """
    def __init__(self):
        self.base_path = config.get("base_paths", "novbase")
        self.docs_path = os.path.join(self.base_path, "storage/docs")
        self.sync_script = os.path.join(self.base_path, "sync.sh")
        
        # Гарантируем наличие папки для документов
        os.makedirs(self.docs_path, exist_ok=True)

    def execute(self, cognition_data: dict, last_reply: str):
        """
        Анализирует миссию и выполняет запись отчета или синхронизацию.
        """
        # Если в когнитивном плане нет прямых указаний на действия, выходим
        if not cognition_data:
            return None

        plan = cognition_data.get("mission_plan", "").lower()
        
        # Команда на сохранение отчета
        if "action: file_save" in plan or "сохранить отчет" in plan:
            saved_path = self._save_to_file(last_reply)
            
            # Если файл сохранен и есть флаг синхронизации
            if saved_path and ("sync" in plan or "github" in plan):
                self._sync_to_github()
            
            return saved_path
        
        return None

    def _save_to_file(self, content: str):
        """Техническое сохранение MD-файла в storage/docs."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"audit_report_{timestamp}.md"
        file_path = os.path.join(self.docs_path, filename)
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"# ОТЧЕТ ДЕСТРУКТИВНОГО ТЕСТИРОВАНИЯ\n")
                f.write(f"ID системы: Nitro-ANV15-41\n")
                f.write(f"Дата создания: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n")
                f.write(f"---\n\n")
                f.write(content)
                f.write(f"\n\n---\n*Конец зашифрованного отчета NovBase*")
            
            print(f"💾 [ActionExecutor]: Файл успешно зафиксирован: {file_path}")
            return file_path
        except Exception as e:
            print(f"❌ [ActionExecutor]: Критическая ошибка записи на диск: {e}")
            return None

    def _sync_to_github(self):
        """
        Тихая фоновая синхронизация через внешний bash-скрипт.
        Не блокирует основной поток генерации.
        """
        if os.path.exists(self.sync_script):
            try:
                # Запуск через subprocess.DEVNULL гарантирует отсутствие блокировок
                subprocess.Popen(
                    ["bash", self.sync_script], 
                    stdout=subprocess.DEVNULL, 
                    stderr=subprocess.DEVNULL,
                    start_new_session=True  # Отвязываем процесс от текущей сессии
                )
                print(f"🚀 [ActionExecutor]: Запущен протокол внешней синхронизации (Sync ID: {os.getpid()})")
            except Exception as e:
                print(f"❌ [ActionExecutor]: Сбой запуска синхронизатора: {e}")
        else:
            print(f"⚠️ [ActionExecutor]: Скрипт синхронизации {self.sync_script} не обнаружен.")
