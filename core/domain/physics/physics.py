import re

class PhysicsEngine:
    """
    Модуль физических расчетов и конвертации величин.
    Адаптирован для вокальной озвучки Ириной и инженерных задач NovBase.
    """
    def __init__(self):
        # Паттерн для поиска чисел (целых и дробных)
        self.num_pattern = re.compile(r"[-+]?\d*\.\d+|\d+")

    def _extract_numbers(self, text):
        """Извлекает числа, поддерживая точку и запятую."""
        clean_text = text.replace(',', '.')
        numbers = self.num_pattern.findall(clean_text)
        return [float(n) for n in numbers]

    def solve(self, expression: str):
        """
        Точка входа для физических расчетов.
        """
        text = expression.lower()
        nums = self._extract_numbers(text)
        
        if not nums:
            return None

        val = nums[0]
        header = "ФИЗИЧЕСКИЙ РАСЧЕТ. "

        # --- БЛОК 1: ПЛОТНОСТЬ (Исправление приоритета) ---
        if "плотность" in text or "плотности" in text:
            if len(nums) >= 2:
                m, v = nums[0], nums[1]
                if v != 0:
                    res = round(m / v, 2)
                    return f"{header}При массе {m} и объеме {v} плотность объекта составит {res} единиц на кубический метр."
                return f"{header}Ошибка: объем не может быть равен нулю."

        # --- БЛОК 2: СКОРОСТЬ (Вокальная адаптация) ---
        if "км/ч" in text or "километров в час" in text:
            if "м/с" in text or "метров в секунду" in text:
                res = round(val / 3.6, 2)
                return f"{header}{val} километров в час это примерно {res} метров в секунду."
        
        if "м/с" in text or "метров в секунду" in text:
            if "км/ч" in text or "километров в час" in text:
                res = round(val * 3.6, 2)
                return f"{header}{val} метров в секунду это {res} километров в час."

        # --- БЛОК 3: ТЕМПЕРАТУРА ---
        if "цельс" in text and ("фаренгейт" in text or " f " in text):
            res = round((val * 9/5) + 32, 2)
            return f"{header}{val} градусов Цельсия равно {res} градусов Фаренгейта."
        
        if "фаренгейт" in text and "цельс" in text:
            res = round((val - 32) * 5/9, 2)
            return f"{header}{val} градусов Фаренгейта равно {res} градусов Цельсия."

        # --- БЛОК 4: КИНЕМАТИКА (Путь S = V * T) ---
        # Добавлена проверка, чтобы не путать с датами
        if ("скорость" in text) and ("время" in text):
            if len(nums) >= 2:
                v, t = nums[0], nums[1]
                res = round(v * t, 2)
                return f"{header}При скорости {v} и времени {t} пройденный путь составит {res} единиц."

        # Если есть числа, но формула не распознана — не возвращаем ничего, 
        # чтобы дать шанс другим модулям или LLM.
        return None

# Инициализация для импорта
physics_tool = PhysicsEngine()

def solve(expression):
    return physics_tool.solve(expression)
