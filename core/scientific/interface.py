import importlib
import os
import re

class ScientificInterface:
    def __init__(self):
        self.base_path = "core.scientific"
        # Расширенная карта ключевых слов для автоматической маршрутизации
        self.routes = {
            "math": ["+", "-", "*", "/", "^", "корень", "сумма", "разность"],
            "geometry": ["площадь", "периметр", "круг", "треугольник", "квадрат", "радиус"],
            "physics": ["км/ч", "м/с", "скорость", "переведи", "масса", "давление", "цельсий", "фаренгейт"],
            "bio": ["днк", "рнк", "ген", "нуклеотид", "последовательность", "атгц", "atgc"]
        }

    def route_query(self, query):
        """
        Интеллектуальный маршрутизатор: 
        Анализирует запрос Георгия и выбирает специализированный научный модуль.
        """
        q = query.lower()
        
        # 1. Проверка на биоинформатику (высокий приоритет из-за специфических букв)
        if any(word in q for word in self.routes["bio"]):
            return self.call("bioinformatics", "bioinformatics", "solve", expression=query)

        # 2. Проверка на геометрию
        if any(word in q for word in self.routes["geometry"]):
            return self.call("math", "geometry", "solve", expression=query)
        
        # 3. Проверка на физику/конвертацию
        if any(word in q for word in self.routes["physics"]):
            return self.call("physics", "physics", "solve", expression=query)
            
        # 4. По умолчанию (или если есть только цифры/знаки) — арифметика
        if any(char.isdigit() for char in q) or any(op in q for op in self.routes["math"]):
            return self.call("math", "arithmetic", "solve", expression=query)
            
        return None

    def call(self, domain, module_name, function_name, **kwargs):
        """
        Динамический загрузчик модулей.
        """
        try:
            # Маппинг доменов на папки
            if domain == "math":
                folder = "mathematics"
            elif domain == "bioinformatics":
                folder = "bioinformatics"
            else:
                folder = domain

            module_path = f"{self.base_path}.{folder}.{module_name}"
            
            # Динамический импорт модуля
            module = importlib.import_module(module_path)
            
            # Получение и вызов функции
            func = getattr(module, function_name)
            return func(**kwargs)
            
        except ModuleNotFoundError:
            print(f"⚠️ [Science] Модуль {module_name} не найден в {module_path}")
            return None
        except Exception as e:
            print(f"⚠️ [Science Interface Error] Ошибка в {domain}.{module_name}: {e}")
            return None
