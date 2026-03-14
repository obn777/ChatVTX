import math
import re

class GeometryEngine:
    """
    Интеллектуальный геометрический модуль.
    Умеет отличать абстрактные фигуры от планетарных масштабов.
    """
    def __init__(self):
        self.num_pattern = re.compile(r"[-+]?\d*\.\d+|\d+")
        # Земля: экваториальный радиус в км
        self.EARTH_RADIUS_KM = 6378.1
        self.EARTH_CIRCUMFERENCE_KM = 40075.0

    def _extract_params(self, text):
        clean_text = text.replace(',', '.')
        return [float(n) for n in self.num_pattern.findall(clean_text)]

    def solve(self, expression: str):
        text = expression.lower()
        params = self._extract_params(text)

        # 0. Исключение ложных срабатываний (Скорость и Движение)
        # Если в запросе речь о времени в пути, геометрия не должна мешать физике
        if any(w in text for w in ["км/ч", "км.ч", "скорость", "за сколько", "быстро"]):
            return None

        header = "ГЕОМЕТРИЧЕСКИЙ СПРАВОЧНИК. "

        # 1. СПЕЦ-КЕЙС: ЗЕМЛЯ
        if "земл" in text and any(w in text for w in ["вокруг", "обойти", "длина", "окружность"]):
            return (f"{header}Длина экватора Земли составляет примерно {self.EARTH_CIRCUMFERENCE_KM} км. "
                    f"Средний радиус планеты — {self.EARTH_RADIUS_KM} км.")

        if not params:
            return None

        # 2. КРУГ / ШАР (улучшенный триггер)
        # Проверяем, что "круг" - это фигура, а не предлог "вокруг"
        is_geometry_circle = any(w in text for w in ["радиус", "диаметр", "площадь круга"])
        if is_geometry_circle or ( "круг" in text and "вокруг" not in text):
            r = params[0]
            area = math.pi * (r**2)
            length = 2 * math.pi * r
            return (f"{header}Для окружности с радиусом {r}: "
                    f"площадь S = {round(area, 2)}, "
                    f"длина L = {round(length, 2)}.")

        # 3. ПРЯМОУГОЛЬНИК / КВАДРАТ
        if any(w in text for w in ["квадрат", "прямоугольник", "периметр", "сторона"]):
            a = params[0]
            b = params[1] if len(params) >= 2 else a
            area = a * b
            perimeter = 2 * (a + b)
            shape = "квадрата" if a == b else "прямоугольника"
            return (f"{header}Для {shape} со сторонами {a} и {b}: "
                    f"площадь S = {round(area, 2)}, "
                    f"периметр P = {round(perimeter, 2)}.")

        # 4. ТРЕУГОЛЬНИК
        if any(w in text for w in ["треугольник", "пирамид"]):
            if len(params) >= 2:
                base, height = params[0], params[1]
                area = 0.5 * base * height
                return (f"{header}Площадь треугольника (0.5 * {base} * {height}) равна {round(area, 2)}.")
            return f"{header}Для расчета треугольника укажите основание и высоту."

        return None

geometry_tool = GeometryEngine()

def solve(expression):
    return geometry_tool.solve(expression)
