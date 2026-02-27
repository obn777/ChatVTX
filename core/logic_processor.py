import re
import os
import datetime
from typing import Dict, Any

# -----------------------
# Логирование (без изменений)
# -----------------------
LOG_PATH = os.path.normpath(
    os.path.join(os.path.dirname(__file__), "..", "logs", "logic_processor.log")
)
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def _log(msg: str) -> None:
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] {msg}"
    try:
        print(line)
        with open(LOG_PATH, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except: pass

class LogicProcessor:
    def __init__(self):
        _log("[LogicProcessor] Инициализация с мед-фильтром и гендерной логикой.")

    def process(self, query: str, context: str = "") -> str:
        q = query.strip()
        ql = q.lower()
        _log(f"[LogicProcessor] Обработка: {q[:50]}...")

        # 1) МЕДИЦИНСКИЙ ПРЕДОХРАНИТЕЛЬ (Юридическая защита)
        # Блокируем запросы про лекарства и диагнозы
        med_keywords = [
            r"таблетк", r"лекарств", r"антибиоти", r"рецепт",
            r"диагноз", r"вылечит", r"терапи", r"дозировк"
        ]
        if any(re.search(kw, ql) for kw in med_keywords):
            _log("[LogicProcessor] Сработал мед-фильтр.")
            return (
                "Я очень за тебя переживаю, но я не врач. "
                "Пожалуйста, не занимайся самолечением и обратись к специалисту. "
                "Здоровье — это слишком важно, чтобы рисковать!"
            )

        # 2) ГЕНДЕРНОЕ УТОЧНЕНИЕ (Для "Мурзиков")
        # Если пришла команда регистрации "Я [пол]"
        if ql.startswith("я мужчина") or ql.startswith("я женщина"):
            _log("[LogicProcessor] Распознано уточнение пола.")
            return "Принято! Теперь я буду общаться с тобой подобающим образом."

        # 3) ПРИВЕТСТВИЯ С УЧЕТОМ ГЕНДЕРА (из контекста)
        if re.match(r"^(привет|здравствуй|hello)\b", ql):
            if "МУЖЧИНА" in context:
                return "Приветствую. Чем могу быть полезна?"
            return "Привет, дорогая! Как твои дела?"

        # 4) АРИФМЕТИКА (Твой оригинал)
        m = re.search(r"стар.?[иеюа]*\s*(\d+).*младше.*на\s*(\d+)", q, flags=re.IGNORECASE)
        if m:
            return f"Если старший {m.group(1)}, а разница {m.group(2)}, младший будет равен {int(m.group(1)) - int(m.group(2))}."

        # 5) ПОСЛЕДОВАТЕЛЬНОСТИ
        if re.search(r"\b2,?\s*4,?\s*8,?\s*16\b", q):
            return "Следующее число — 32."

        # 6) ЛОГИКА ПРО ЯБЛОКИ / ЛАМПЫ (Твой оригинал)
        if "яблок" in ql and "все" in ql and "красн" in ql:
            return "Из утверждения «все яблоки красные» не следует, что любой красный фрукт — яблоко."

        # 7) ФОЛБЭК (Если ничего не подошло, отдаем в LLM)
        _log("[LogicProcessor] Логика не найдена, передача в LLM.")
        return "" # Пустая строка означает "передай запрос нейронке"

    async def process_message(self, text: str, context: str = "") -> Dict[str, Any]:
        """Асинхронная оболочка."""
        _log("[LogicProcessor] process_message() вызван.")
        result_text = self.process(text, context)
        return {
            "text": text,
            "result": result_text,
            "processed": bool(result_text), # True если LogicProcessor сам ответил
            "timestamp": datetime.datetime.now().isoformat()
        }

if __name__ == "__main__":
    lp = LogicProcessor()
    # Тест мед-фильтра
    print(f"TEST MED: {lp.process('Какие таблетки от головы?')}")
    # Тест гендера
    print(f"TEST GENDER: {lp.process('Привет', context='МУЖЧИНА')}")
