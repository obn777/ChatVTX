import math
import re

class GeometryEngine:
    """
    Специализированный модуль для расчета параметров геометрических фигур.
    Адаптирован под вокальное чтение и быструю обработку.
    """
    def __init__(self):
        # Паттерны для поиска чисел (поддержка точек и запятых)
        self.num_pattern = re.compile(r"[-+]?\d*\.\d+|\d+")

    def _extract_params(self, text):
        clean_text = text.replace(',', '.')
        return [float(n) for n in self.num_pattern.findall(clean_text)]

    def solve(self, expression: str):
        text = expression.lower()
        params = self._extract_params(text)
        
        if not params:
            return None

        header = "ГЕОМЕТРИЧЕСКИЙ РАСЧЕТ. "

        # 1. КРУГ / ШАР
        if any(w in text for w in ["круг", "шар", "радиус", "диаметр"]):
            r = params[0]
            area = math.pi * (r**2)
            length = 2 * math.pi * r
            return (f"{header}Для круга с радиусом {r}: "
                    f"площадь составляет {round(area, 2)}, "
                    f"длина окружности равна {round(length, 2)}.")

        # 2. ПРЯМОУГОЛЬНИК / КВАДРАТ
        if any(w in text for w in ["квадрат", "прямоугольник", "периметр", "сторона"]):
            a = params[0]
            b = params[1] if len(params) >= 2 else a
            area = a * b
            perimeter = 2 * (a + b)
            shape = "квадрата" if a == b else "прямоугольника"
            return (f"{header}Для {shape} со сторонами {a} и {b}: "
                    f"площадь равна {round(area, 2)}, "
                    f"периметр составляет {round(perimeter, 2)}.")

        # 3. ТРЕУГОЛЬНИК
        if any(w in text for w in ["треугольник", "пирамид"]):
            if len(params) >= 2:
                base, height = params[0], params[1]
                area = 0.5 * base * height
                return (f"{header}Площадь треугольника с основанием {base} "
                        f"и высотой {height} равна {round(area, 2)}.")
            return f"{header}Для треугольника мне нужны два числа: основание и высота."

        return None

# Экземпляр модуля
geometry_tool = GeometryEngine()

def solve(expression):
    return geometry_tool.solve(expression)
