import os
import tarfile
import datetime
import shutil

class BackupManager:
    """
    Автоматизированная система резервного копирования NovBase.
    Защищает код, кэш и документы, исключая тяжелые веса (модели/venv).
    """
    def __init__(self, project_path="/home/obn7/NovBase", backup_dir="/home/obn7/NovBase_backups"):
        self.project_path = project_path
        self.backup_dir = backup_dir
        # Что НЕ включаем в архив:
        # venv и models — слишком тяжелые (десятки ГБ)
        # .git и __pycache__ — лишний мусор для бэкапа логики
        self.exclude = ["venv", "models", "__pycache__", ".git", "NovBase_backups"]

    def create_backup(self):
        """Создает сжатый .tar.gz архив текущего состояния проекта."""
        if not os.path.exists(self.backup_dir):
            os.makedirs(self.backup_dir)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"novbase_backup_{timestamp}.tar.gz"
        backup_path = os.path.join(self.backup_dir, backup_name)

        print(f"📦 [Backup] Инициализация архивации: {backup_name}")

        def filter_function(tarinfo):
            # Проверка: не входит ли имя файла или папки в список исключений
            if any(exc in tarinfo.name for exc in self.exclude):
                return None
            return tarinfo

        try:
            with tarfile.open(backup_path, "w:gz") as tar:
                # Рекурсивно добавляем все файлы проекта с применением фильтра
                tar.add(self.project_path, arcname="NovBase", filter=filter_function)
            
            # Получаем размер архива для логов
            file_size = os.path.getsize(backup_path) / (1024 * 1024)
            print(f"✅ [Backup] Успех! Размер: {file_size:.2f} MB")
            print(f"📍 Путь: {backup_path}")
            
            self._rotate_backups() # Очистка старых копий
            return backup_path
        except Exception as e:
            print(f"❌ [Backup] Критическая ошибка при создании бэкапа: {e}")
            return None

    def _rotate_backups(self):
        """Поддерживает ротацию: храним только 5 последних версий."""
        try:
            backups = sorted(
                [os.path.join(self.backup_dir, f) for f in os.listdir(self.backup_dir) if f.endswith(".tar.gz")],
                key=os.path.getmtime
            )
            
            if len(backups) > 5:
                to_remove = backups[:-5]
                for old_backup in to_remove:
                    os.remove(old_backup)
                    print(f"🧹 [Backup] Старая копия удалена: {os.path.basename(old_backup)}")
        except Exception as e:
            print(f"⚠️ [Backup] Не удалось провести ротацию: {e}")

if __name__ == "__main__":
    # Тестовый запуск
    bm = BackupManager()
    bm.create_backup()
