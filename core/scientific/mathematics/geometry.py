import math
import re

def extract_numbers(text):
    """
    Ищет все числа в строке. 
    Поддерживает целые и дробные (через точку или запятую).
    """
    # Заменяем запятые на точки для корректного преобразования во float
    clean_text = text.replace(',', '.')
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", clean_text)
    return [float(n) for n in numbers]

def calculate_area(shape, params):
    """
    Ядро геометрических вычислений.
    """
    try:
        if shape == "circle":
            if len(params) < 1: return "нужен радиус"
            r = params[0]
            area = math.pi * (r**2)
            return f"площадь круга с радиусом {r} ≈ {round(area, 2)}"
        
        elif shape == "rectangle":
            if len(params) < 1: return "нужны стороны"
            # Если передано одно число, считаем это квадратом
            a = params[0]
            b = params[1] if len(params) >= 2 else a
            area = a * b
            shape_name = "квадрата" if a == b else "прямоугольника"
            return f"площадь {shape_name} ({a}x{b}) = {round(area, 2)}"
        
        elif shape == "triangle":
            if len(params) < 2: return "нужны основание и высота"
            a, h = params[0], params[1]
            area = 0.5 * a * h
            return f"площадь треугольника (осн. {a}, выс. {h}) = {round(area, 2)}"
            
        return None
    except Exception as e:
        return f"ошибка в формуле: {e}"

def solve(expression):
    """
    Главная точка входа. Парсит текст Георгия и выбирает действие.
    """
    text = expression.lower()
    nums = extract_numbers(text)
    
    if not nums:
        return "Георгий, я не нашел чисел в запросе. Укажите размеры фигуры."

    # Логика определения фигуры по ключевым словам
    if any(w in text for w in ["круг", "шар", "радиус", "диаметр"]):
        return calculate_area("circle", nums)
    
    if any(w in text for w in ["квадрат", "прямоугольник", "сторона", "длина"]):
        return calculate_area("rectangle", nums)
    
    if any(w in text for w in ["треугольник", "пирамид"]):
        return calculate_area("triangle", nums)

    return ("Я нашел числа " + str(nums) + ", но не понял, какую фигуру считать. "
            "Уточните: это круг, квадрат или треугольник?")
