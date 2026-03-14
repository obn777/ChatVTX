import math
import re

def solve(expression):
    """
    Математический сопроцессор: корни, степени, геометрия.
    Адаптирован для вокальной озвучки и интеграции в VTX Core.
    """
    # Подготовка текста: замена запятых на точки и приведение к нижнему регистру
    text = expression.lower().replace(',', '.')

    # Регулярное выражение для поиска всех чисел
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    nums = [float(n) for n in nums]

    if not nums:
        return None

    results = []
    header = "МАТЕМАТИЧЕСКИЙ РАСЧЕТ. "

    # 0. Исключение: Планетарные масштабы (Земля)
    # Если речь о Земле, математика не должна навязывать расчет "круга" радиусом 2км
    if "земл" in text and "вокруг" in text:
        return None  # Отдаем расчет модулю физики или знаниям LLM

    # 1. Квадратный корень
    if any(w in text for w in ["корень", "sqrt"]):
        val = nums[0]
        if val < 0:
            results.append(f"извлечение корня из отрицательного числа {val} невозможно")
        else:
            res = math.sqrt(val)
            results.append(f"квадратный корень из {val} равен {round(res, 4)}")

    # 2. Степень
    if any(w in text for w in ["степен", "^", "**"]):
        if len(nums) >= 2:
            base, exp = nums[0], nums[1]
            try:
                res = math.pow(base, exp)
                # Форматируем вывод, чтобы не было гигантских чисел
                formatted_res = f"{res:.4g}" if res > 1000000 else round(res, 4)
                results.append(f"{base} в степени {exp} равно {formatted_res}")
            except OverflowError:
                results.append("результат слишком велик для вычисления")

    # 3. Геометрия: Площадь и длина круга (Строгий триггер)
    # Проверяем, что это именно задача на геометрию, а не "обойти вокруг"
    if "площадь" in text and "круг" in text and "вокруг" not in text:
        r = nums[0]
        s = math.pi * (r ** 2)
        l = 2 * math.pi * r
        results.append(f"площадь круга с радиусом {r} составляет {round(s, 2)}, длина окружности {round(l, 2)}")

    # 4. Геометрия: Теорема Пифагора
    if any(w in text for w in ["гипотенуз", "пифагор"]):
        if len(nums) >= 2:
            a, b = nums[0], nums[1]
            res = math.hypot(a, b)
            results.append(f"гипотенуза треугольника с катетами {a} и {b} равна {round(res, 2)}")

    if results:
        return header + ". ".join(results)

    return None
