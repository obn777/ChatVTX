import math
import re

def solve(expression):
    """
    Математический сопроцессор: корни, степени, площади.
    """
    text = expression.lower().replace(',', '.')
    nums = re.findall(r"[-+]?\d*\.\d+|\d+", text)
    nums = [float(n) for n in nums]

    if not nums:
        return None

    results = []

    # 1. Квадратный корень
    if "корень" in text or "sqrt" in text:
        res = math.sqrt(nums[0])
        results.append(f"√{nums[0]} = {round(res, 4)}")

    # 2. Степень
    if "степен" in text or "^" in text:
        if len(nums) >= 2:
            res = math.pow(nums[0], nums[1])
            results.append(f"{nums[0]}^{nums[1]} = {res}")

    # 3. Геометрия: Площадь круга
    if "площадь" in text and "круг" in text:
        r = nums[0]
        s = math.pi * (r ** 2)
        results.append(f"S круга (r={r}) = {round(s, 2)}")

    # 4. Геометрия: Гипотенуза (Пифагор)
    if "гипотенуз" in text or "пифагор" in text:
        if len(nums) >= 2:
            res = math.hypot(nums[0], nums[1])
            results.append(f"Гипотенуза (a={nums[0]}, b={nums[1]}) = {round(res, 2)}")

    return "📐 [MATH]: " + " | ".join(results) if results else None
