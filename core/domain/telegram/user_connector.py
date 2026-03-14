import json
import os

class UserConnector:
    def __init__(self, storage_path="/home/obn7/NovBase/storage/user_states.json"):
        self.storage_path = storage_path
        self.states = self._load_states()

    def _load_states(self):
        """Загрузка состояний из файла при старте."""
        if os.path.exists(self.storage_path):
            try:
                with open(self.storage_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def _save_states(self):
        """Сохранение состояний в файл."""
        try:
            with open(self.storage_path, 'w', encoding='utf-8') as f:
                json.dump(self.states, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Ошибка сохранения состояний: {e}")

    def set_state(self, user_id, state):
        """Установка статуса (например, WAIT_DATA)"""
        self.states[str(user_id)] = state
        self._save_states()

    def get_state(self, user_id):
        """Получение текущего статуса пользователя."""
        return self.states.get(str(user_id), "IDLE")

    def clear_state(self, user_id):
        """Сброс статуса после завершения действия."""
        if str(user_id) in self.states:
            del self.states[str(user_id)]
            self._save_states()
