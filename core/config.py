import os
import json
import sys

class Config:
    """
    Единый центр управления путями и параметрами NovBase.
    Синхронизировано с архитектурой Nitro-ANV15-41.
    Защищено от ошибок NoneType при инициализации.
    """
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _get_default_config(self):
        """Возвращает базовую карту путей, если внешний файл недоступен или поврежден."""
        base_dir = "/home/obn7/NovBase"
        return {
            "base_paths": {
                "novbase": base_dir,
                "models": "/home/obn7/models",
                "storage": os.path.join(base_dir, "storage"),
                "logs": os.path.join(base_dir, "logs")
            },
            "model_paths": {
                "main": "/home/obn7/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf",
                "vision": "/home/obn7/models/mmproj-model-f16.gguf"
            },
            "storage_paths": {
                "history": os.path.join(base_dir, "storage/history.json"),
                "cache": os.path.join(base_dir, "storage/cache.json"),
                "long_term_memory": os.path.join(base_dir, "storage/memory/master_cache.json")
            },
            "system": {
                "device": "Nitro-ANV15-41",
                "vram_limit_gb": 6,
                "threads": 12
            }
        }
    
    def _load_config(self):
        """Загружает конфигурацию слиянием дефолтных значений и внешнего JSON."""
        # 1. Сначала ставим дефолты
        self._config = self._get_default_config()
        
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "configs", "paths.json"
        )
        
        # 2. Пробуем обновить из файла
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r', encoding='utf-8') as f:
                    user_data = json.load(f)
                    if isinstance(user_data, dict):
                        # Глубокое обновление (merge) разделов
                        for section in ["base_paths", "model_paths", "storage_paths", "system"]:
                            if section in user_data and isinstance(user_data[section], dict):
                                self._config[section].update(user_data[section])
                print(f"✅ [CONFIG]: Интегрированы данные из {config_path}")
            except Exception as e:
                print(f"❌ [CONFIG ERROR]: Ошибка парсинга {config_path}: {e}")

    def get(self, *keys, default=None):
        """Безопасное извлечение параметров по цепочке ключей."""
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def get_model_path(self, model_type="main"):
        return self.get("model_paths", model_type)
    
    def get_storage_path(self, key):
        return self.get("storage_paths", key)

    def ensure_dirs(self):
        """Безопасное создание структуры папок."""
        # Собираем список папок для проверки
        raw_dirs = [
            self.get("base_paths", "storage"),
            self.get("base_paths", "logs"),
            os.path.join(self.get("base_paths", "novbase"), "configs")
        ]
        
        # Добавляем папки, в которых лежат файлы памяти
        for path_key in ["history", "cache", "long_term_memory"]:
            file_path = self.get_storage_path(path_key)
            if file_path:
                raw_dirs.append(os.path.dirname(file_path))

        # Очищаем от None и дублей, создаем
        for d in sorted(list(set(filter(None, raw_dirs)))):
            if not os.path.exists(d):
                try:
                    os.makedirs(d, exist_ok=True)
                    print(f"📁 [SYSTEM]: Создана директория {d}")
                except Exception as e:
                    print(f"❌ [SYSTEM ERROR]: Не удалось создать {d}: {e}")
        
        print("✅ [SYSTEM]: Инфраструктура подтверждена.")

# Инициализация
config = Config()
config.ensure_dirs()
