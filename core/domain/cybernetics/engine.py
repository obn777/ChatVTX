import os
import sys
import subprocess

# --- СЛОВАРЬ ПРОГРАММАТИКИ ---
LANG_BASE = {
    "python": "Интерпретируемый. Использование: AI/ML, Backend. Особенности: GIL, динамическая типизация.",
    "c++": "Компилируемый. Использование: High-load, GameDev. Особенности: Управление памятью, RAII.",
    "rust": "Компилируемый. Использование: System safety. Особенности: Borrow Checker, Zero-cost abstractions.",
    "javascript": "Событийный. Использование: Fullstack. Особенности: V8 engine, асинхронность."
}

def analyze_syntax(code):
    """Кибернетический анализ фрагментов кода."""
    issues = []
    if "except:" in code and "pass" in code:
        issues.append("⚠️ Обнаружено подавление всех ошибок (bare except).")
    if "eval(" in code:
        issues.append("🚨 Критическая уязвимость: использование eval().")
    if "os.system" in code:
        issues.append("⚠️ Рекомендуется subprocess вместо os.system.")
    return " | ".join(issues) if issues else "Синтаксический анализ: Чисто."

def create_module(name, category="scientific"):
    """Генератор структуры нового модуля с автоматическим __init__."""
    path = f"/home/obn7/NovBase/core/{category}/{name}"
    try:
        os.makedirs(path, exist_ok=True)
        init_file = os.path.join(path, "__init__.py")
        main_file = os.path.join(path, f"{name}.py")
        
        # Шаблон кода с пробросом в init для устранения ошибок импорта
        code_template = f"""# Module: {name.upper()}
def solve(expression):
    text = expression.lower()
    return f"🤖 [{name.upper()} DATA]: Обработан запрос '{{text}}'"
"""
        with open(main_file, "w") as f:
            f.write(code_template)
        
        # Автоматический экспорт функции solve
        with open(init_file, "w") as f:
            f.write(f"from .{name} import solve")
            
        return f"✅ Модуль {name} создан и экспортирован в {path}"
    except Exception as e:
        return f"❌ Ошибка генерации: {e}"

def fix_paths():
    """Авто-исправление и синхронизация критических путей NovBase."""
    required = [
        "/home/obn7/NovBase",
        "/home/obn7/NovBase/core",
        "/home/obn7/NovBase/core/scientific",
        "/home/obn7/NovBase/storage"
    ]
    added = []
    for p in required:
        if p not in sys.path:
            sys.path.append(p)
            added.append(p)
    return f"Fixed: {len(added)} paths added" if added else "Paths: Valid"

def solve(expression):
    text = expression.lower()
    
    # 1. СЕКТОР ПРОГРАММАТИКИ (Языки)
    for lang, desc in LANG_BASE.items():
        if f"язык {lang}" in text or f"про {lang}" in text:
            return f"🤖 [CYBER-LANG]: {desc}"

    # 2. СЕКТОР ГЕНЕРАЦИИ (Создание модулей)
    if "создай модуль" in text or "новый модуль" in text:
        parts = text.split()
        name = parts[-1].strip()
        return f"🤖 [CYBER-GEN]: {create_module(name)}"

    # 3. СЕКТОР АНАЛИЗА (Проверка кода)
    if "проверь код" in text or "```" in text:
        return f"🤖 [CYBER-ANALYZE]: {analyze_syntax(expression)}"

    # 4. СЕКТОР СЕРВИСА (Пути и Статус)
    if "исправь пути" in text or "чекни пути" in text:
        return f"🤖 [CYBER-SYS]: {fix_paths()}"
    
    if "статус системы" in text:
        return f"🤖 [CYBER-SYS]: Путей в реестре: {len(sys.path)}. Модуль Кибернетики: Активен."

    return None
