import os
import json
import sys

class Config:
    """Единый класс конфигурации для всего проекта"""
    
    _instance = None
    _config = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance
    
    def _load_config(self):
        """Загружает конфигурацию из файла"""
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), 
            "configs", "paths.json"
        )
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self._config = json.load(f)
            print(f"✅ Конфигурация загружена из {config_path}")
        except FileNotFoundError:
            print(f"⚠️ Файл конфигурации не найден: {config_path}")
            self._config = self._get_default_config()
        except Exception as e:
            print(f"❌ Ошибка загрузки конфигурации: {e}")
            self._config = self._get_default_config()
    
    def _get_default_config(self):
        """Возвращает конфигурацию по умолчанию"""
        return {
            "base_paths": {
                "novbase": "/home/obn7/NovBase",
                "models": "/home/obn7/models"
            },
            "model_paths": {
                "llama3_8b_text": "/home/obn7/models/llava-llama-3-8b-v1_1.Q4_K_M.gguf"
            },
            "storage_paths": {
                "memory_cache": "/home/obn7/NovBase/storage/memory/master_cache.json"
            },
            "log_paths": {}
        }
    
    def get(self, *keys, default=None):
        """Получает значение из конфигурации по цепочке ключей"""
        value = self._config
        for key in keys:
            if isinstance(value, dict):
                value = value.get(key)
                if value is None:
                    return default
            else:
                return default
        return value
    
    def get_model_path(self, model_name):
        """Получает путь к модели по имени"""
        return self.get("model_paths", model_name)
    
    def get_storage_path(self, path_name):
        """Получает путь к хранилищу"""
        return self.get("storage_paths", path_name)
    
    def ensure_dirs(self):
        """Создает все необходимые директории"""
        paths = []
        
        if "storage_paths" in self._config:
            paths.extend(self._config["storage_paths"].values())
        if "log_paths" in self._config:
            paths.extend(self._config["log_paths"].values())
        
        for path in paths:
            if path and isinstance(path, str):
                dirname = os.path.dirname(path)
                if dirname:
                    os.makedirs(dirname, exist_ok=True)
        
        print("✅ Все директории созданы")

# Создаем глобальный экземпляр
config = Config()
