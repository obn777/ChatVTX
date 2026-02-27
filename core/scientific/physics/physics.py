import re

def extract_numbers(text):
    """Извлекает числа из текста (целые и дробные)."""
    clean_text = text.replace(',', '.')
    numbers = re.findall(r"[-+]?\d*\.\d+|\d+", clean_text)
    return [float(n) for n in numbers]

def solve(expression):
    """
    Главная точка входа для физических расчетов и конвертации.
    """
    text = expression.lower()
    nums = extract_numbers(text)
    
    if not nums:
        return "Георгий, укажите значение для перевода (например: 100 км/ч)."

    val = nums[0]

    # --- БЛОК 1: СКОРОСТЬ ---
    if "км/ч" in text and "м/с" in text:
        res = round(val / 3.6, 2)
        return f"{val} км/ч = {res} м/с"
    
    if "м/с" in text and "км/ч" in text:
        res = round(val * 3.6, 2)
        return f"{val} м/с = {res} км/ч"

    # --- БЛОК 2: ТЕМПЕРАТУРА ---
    if "цельс" in text and "фаренгейт" in text:
        res = round((val * 9/5) + 32, 2)
        return f"{val}°C = {res}°F"
    
    if "фаренгейт" in text and "цельс" in text:
        res = round((val - 32) * 5/9, 2)
        return f"{val}°F = {res}°C"

    # --- БЛОК 3: ДАВЛЕНИЕ (Для инженерии) ---
    if "бар" in text and "паскаль" in text:
        res = val * 100000
        return f"{val} бар = {res} Па"

    # --- БЛОК 4: КИНЕМАТИКА (S = V * T) ---
    if "скорость" in text and "время" in text:
        if len(nums) >= 2:
            res = round(nums[0] * nums[1], 2)
            return f"Путь при V={nums[0]} и T={nums[1]} составит {res} ед."

    return (f"Я вижу число {val}, но не понял, какую физическую величину перевести. "
            "Я умею: км/ч в м/с, Цельсий в Фаренгейт и расчет пути.")
