import re

# Таблица атомных масс основных элементов
PERIODIC_TABLE = {
    "H": 1.008, "He": 4.002, "Li": 6.941, "C": 12.011,
    "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
    "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085,
    "P": 30.974, "S": 32.06, "Cl": 35.45, "K": 39.098,
    "Ca": 40.078, "Fe": 55.845, "Cu": 63.546, "Zn": 65.38
}

def calculate_molar_mass(formula):
    """Парсит формулу типа H2O или H2SO4 и считает массу."""
    # Регулярка для поиска элемента и его количества
    tokens = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
    total_mass = 0.0
    
    for element, count in tokens:
        if element in PERIODIC_TABLE:
            c = int(count) if count else 1
            total_mass += PERIODIC_TABLE[element] * c
        else:
            return None # Неизвестный элемент
    return round(total_mass, 3)

def solve(expression):
    """Точка входа для химических запросов."""
    text = expression.strip()
    
    # Поиск формул в тексте (заглавные буквы, цифры)
    formula_match = re.search(r'\b[A-Z][A-Za-z0-9]*\b', text)
    if not formula_match:
        return None
        
    formula = formula_match.group()
    mass = calculate_molar_mass(formula)
    
    if mass:
        return f"🧪 [CHEMISTRY]: Молекула {formula} | Молярная масса: {mass} г/моль"
    
    # Реакции (базовая заглушка)
    if "кислот" in text.lower() and "щелоч" in text.lower():
        return "🧪 [CHEMISTRY]: Реакция нейтрализации: Кислота + Щелочь = Соль + Вода."
        
    return None
