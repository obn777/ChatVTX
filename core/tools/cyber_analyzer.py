import os
import sys
import subprocess
import re

class CyberAnalyzer:
    """
    Модуль кибернетического анализа и авто-генерации структуры NovBase.
    Позволяет системе саморасширяться и проводить аудит кода.
    """
    def __init__(self):
        # База знаний по языкам программирования
        self.lang_base = {
            "python": "Интерпретируемый язык. Идеален для искусственного интеллекта и бэкенда. Особенности: глобальная блокировка интерпретатора и динамическая типизация.",
            "c++": "Компилируемый язык высокого уровня. Применяется в высоконагруженных системах. Особенности: прямое управление памятью.",
            "rust": "Компилируемый системный язык. Особенности: строгая проверка владения памятью и безопасность без потерь производительности.",
            "javascript": "Событийный язык для веб-разработки. Особенности: движок V8 и высокая асимхронность."
        }

    def analyze_syntax(self, code: str) -> str:
        """Аудит безопасности и чистоты кода."""
        issues = []
        # Поиск опасных или неэффективных конструкций
        if re.search(r"except:\s*pass", code):
            issues.append("обнаружено подавление ошибок через пустой блок эксепт.")
        if "eval(" in code:
            issues.append("найдена критическая уязвимость использования функции эвал.")
        if "os.system(" in code:
            issues.append("рекомендуется заменить системные вызовы ос систем на сабпроцесс.")
        
        return "Внимание: " + " ".join(issues) if issues else "Анализ завершен. Код чист."

    def create_module(self, name: str, category: str = "scientific") -> str:
        """Генератор структуры нового модуля с авто-экспортом."""
        # Очистка имени модуля от мусора
        name = re.sub(r'[^a-zA-Z0-9_]', '', name)
        path = f"/home/obn7/NovBase/core/{category}/{name}"
        try:
            os.makedirs(path, exist_ok=True)
            init_file = os.path.join(path, "__init__.py")
            main_file = os.path.join(path, f"{name}.py")
            
            code_template = (
                f"# Module: {name.upper()}\n"
                f"def solve(expression):\n"
                f"    return f'🤖 [{name.upper()}]: Обработан запрос {{expression}}'\n"
            )
            
            with open(main_file, "w") as f: f.write(code_template)
            with open(init_file, "w") as f: f.write(f"from .{name} import solve")
                
            return f"Модуль {name} успешно развернут по адресу {path}."
        except Exception as e:
            return f"Произошла ошибка при создании модуля: {str(e)}."

    def fix_paths(self) -> str:
        """Синхронизация путей для устранения ошибок импорта."""
        required = [
            "/home/obn7/NovBase",
            "/home/obn7/NovBase/core",
            "/home/obn7/NovBase/core/scientific"
        ]
        added = [p for p in required if p not in sys.path]
        for p in added: 
            sys.path.append(p)
        
        if added:
            return f"Пути синхронизированы. Добавлено объектов: {len(added)}."
        return "Все системные пути валидны."

    def analyze(self, text: str):
        """Точка входа для LogicProcessor."""
        ql = text.lower()
        
        # 1. Справочник языков
        for lang, desc in self.lang_base.items():
            if f"язык {lang}" in ql: 
                return f"КИБЕР-СПРАВКА. {desc}"

        # 2. Создание модулей (Детекция команды)
        if any(w in ql for w in ["создай модуль", "новый модуль"]):
            # Берем последнее слово как имя модуля
            parts = ql.split()
            if len(parts) > 2:
                name = parts[-1].strip()
                return f"ГЕНЕРАЦИЯ СИСТЕМЫ. {self.create_module(name)}"

        # 3. Аудит кода
        if "проверь код" in ql or "```" in ql:
            return f"АУДИТ БЕЗОПАСНОСТИ. {self.analyze_syntax(text)}"

        # 4. Системный сервис
        if "исправь пути" in ql: 
            return f"СИСТЕМНЫЙ СЕРВИС. {self.fix_paths()}"
            
        if "статус системы" in ql:
            return f"СИСТЕМНЫЙ СЕРВИС. Реестр путей содержит {len(sys.path)} записей. Модуль кибернетики активен."

        return None

# Экземпляр для LogicProcessor
cyber_tool = CyberAnalyzer()
