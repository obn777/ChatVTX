import math
import re

def solve(expression):
    """
    Математический сопроцессор: корни, степени, геометрия.
    Адаптирован для вокальной озвучки Ириной.
    """
    # Подготовка текста: замена запятых на точки для float и очистка
    text = expression.lower().replace(',', '.')
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    nums = [float(n) for n in nums]

    if not nums:
        return None

    results = []

    # 1. Квадратный корень
    if "корень" in text or "sqrt" in text:
        val = nums[0]
        if val < 0:
            results.append(f"извлечение корня из отрицательного числа {val} невозможно в действительных числах")
        else:
            res = math.sqrt(val)
            results.append(f"квадратный корень из {val} равен {round(res, 4)}")

    # 2. Степень
    if "степен" in text or "^" in text or "**" in text:
        if len(nums) >= 2:
            base, exp = nums[0], nums[1]
            try:
                res = math.pow(base, exp)
                results.append(f"{base} в степени {exp} равно {res}")
            except OverflowError:
                results.append("результат возведения в степень слишком велик для вычисления")

    # 3. Геометрия: Площадь круга
    if "площадь" in text and "круг" in text:
        r = nums[0]
        s = math.pi * (r ** 2)
        results.append(f"площадь круга с радиусом {r} составляет {round(s, 2)}")

    # 4. Геометрия: Гипотенуза (Теорема Пифагора)
    if "гипотенуз" in text or "пифагор" in text:
        if len(nums) >= 2:
            a, b = nums[0], nums[1]
            res = math.hypot(a, b)
            results.append(f"гипотенуза треугольника с катетами {a} и {b} равна {round(res, 2)}")

    if results:
        # Формируем чистый текст без спецсимволов для корректной работы aplay/piper
        return "МАТЕМАТИЧЕСКИЙ РАСЧЕТ. " + ". ".join(results)
    
    return None
