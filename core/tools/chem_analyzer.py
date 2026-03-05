import re

class ChemAnalyzer:
    """
    Модуль химического анализа системы NovBase.
    Расчет молярных масс и распознавание типов реакций.
    """
    def __init__(self):
        # Таблица атомных масс (IUPAC стандарт)
        self.periodic_table = {
            "H": 1.008, "He": 4.002, "Li": 6.941, "Be": 9.012, "B": 10.81,
            "C": 12.011, "N": 14.007, "O": 15.999, "F": 18.998, "Ne": 20.180,
            "Na": 22.990, "Mg": 24.305, "Al": 26.982, "Si": 28.085, "P": 30.974,
            "S": 32.06, "Cl": 35.45, "Ar": 39.948, "K": 39.098, "Ca": 40.078,
            "Cr": 51.996, "Mn": 54.938, "Fe": 55.845, "Ni": 58.693, "Cu": 63.546,
            "Zn": 65.38, "Ag": 107.868, "Au": 196.967, "Hg": 200.59, "Pb": 207.2
        }

    def calculate_molar_mass(self, formula: str):
        """Парсит химическую формулу и вычисляет молярную массу."""
        # Регулярка для поиска элементов и их индексов
        tokens = re.findall(r'([A-Z][a-z]*)(\d*)', formula)
        total_mass = 0.0
        
        for element, count in tokens:
            if element in self.periodic_table:
                c = int(count) if count else 1
                total_mass += self.periodic_table[element] * c
            else:
                # Если найден неизвестный элемент, прерываем расчет
                return None
        return round(total_mass, 2)

    def analyze(self, text: str):
        """Анализирует запрос на наличие химических данных."""
        # Поиск потенциальных формул (Заглавная буква + буквы/цифры)
        formulas = re.findall(r'\b[A-Z][A-Za-z0-9]*\b', text)
        
        results = []
        for f in formulas:
            # Исключаем короткие слова и ложные срабатывания (например, названия модулей)
            if not any(char.isdigit() for char in f) and f not in self.periodic_table:
                if len(f) < 2: continue
            
            mass = self.calculate_molar_mass(f)
            if mass:
                # Адаптируем вывод для Ирины (грамм на моль вместо г/моль)
                results.append(f"{f}, масса которого {mass} грамм на моль")

        if results:
            report_parts = ["ХИМИЧЕСКИЙ АНАЛИЗ."]
            report_parts.extend(results)
            
            low_text = text.lower()
            # Детекция типов реакций
            if "кислот" in low_text and "щелоч" in low_text:
                report_parts.append("Обнаружены признаки реакции нейтрализации. Результат: соль и вода.")
            elif "горен" in low_text or "+ o2" in low_text:
                report_parts.append("Тип процесса: окисление или горение.")
                
            return " ".join(report_parts)
            
        return None

# Экземпляр для интеграции в LogicProcessor
chem_tool = ChemAnalyzer()
