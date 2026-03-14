import re

class PhysicsEngine:
    """
    Модуль физических расчетов NovBase.
    Ориентирован на кинематику, термодинамику и планетарные масштабы.
    """
    def __init__(self):
        self.num_pattern = re.compile(r"[-+]?\d*\.\d+|\d+")
        # Константы для точности
        self.EARTH_CIRCUMFERENCE = 40075.0

    def _extract_numbers(self, text):
        clean_text = text.replace(',', '.')
        numbers = self.num_pattern.findall(clean_text)
        return [float(n) for n in numbers]

    def solve(self, expression: str):
        text = expression.lower()
        nums = self._extract_numbers(text)
        header = "ФИЗИЧЕСКИЙ РАСЧЕТ. "

        # --- СПЕЦ-КЕЙС: ДВИЖЕНИЕ ВОКРУГ ЗЕМЛИ ---
        if "земл" in text and ("обойти" in text or "объехать" in text or "кругосвет" in text):
            if nums:
                v = nums[0]
                if v > 0:
                    time_hours = round(self.EARTH_CIRCUMFERENCE / v, 2)
                    days = round(time_hours / 24, 1)
                    return (f"{header}Для обхода Земли (40075 км) со скоростью {v} км/ч "
                            f"потребуется {time_hours} ч. (примерно {days} сут. непрерывного хода).")

        if not nums:
            return None

        val = nums[0]

        # --- БЛОК 1: ПЛОТНОСТЬ ---
        if "плотность" in text or "плотности" in text:
            if len(nums) >= 2:
                m, v = nums[0], nums[1]
                if v != 0:
                    res = round(m / v, 2)
                    return f"{header}При массе {m} и объеме {v} плотность составит {res} ед/м³."
                return f"{header}Ошибка: деление на ноль (объем)."

        # --- БЛОК 2: КОНВЕРТАЦИЯ СКОРОСТИ ---
        if "км/ч" in text and ("м/с" in text or "метров в секунду" in text):
            return f"{header}{val} км/ч = {round(val / 3.6, 2)} м/с."

        if "м/с" in text and ("км/ч" in text or "километров в час" in text):
            return f"{header}{val} м/с = {round(val * 3.6, 2)} км/ч."

        # --- БЛОК 3: ТЕМПЕРАТУРА ---
        if "цельс" in text and ("фаренгейт" in text or " f " in text):
            res = round((val * 9/5) + 32, 2)
            return f"{header}{val}°C = {res}°F."

        if "фаренгейт" in text and "цельс" in text:
            res = round((val - 32) * 5/9, 2)
            return f"{header}{val}°F = {res}°C."

        # --- БЛОК 4: КИНЕМАТИКА (S, V, T) ---
        # Расчет времени: t = S / v
        if "за сколько" in text or "время" in text:
            if "расстояние" in text or "путь" in text or "дистанция" in text:
                if len(nums) >= 2:
                    s, v = nums[0], nums[1]
                    if v > 0:
                        return f"{header}Время в пути при S={s} и v={v} составит {round(s/v, 2)} ч."

        # Расчет пути: S = v * t
        if "путь" in text or "расстояние" in text:
            if "скорость" in text and "время" in text:
                if len(nums) >= 2:
                    v, t = nums[0], nums[1]
                    return f"{header}Пройденный путь (v*t) при v={v} и t={t} составит {round(v*t, 2)} ед."

        return None

physics_tool = PhysicsEngine()

def solve(expression):
    return physics_tool.solve(expression)
