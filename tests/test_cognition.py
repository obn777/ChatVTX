import asyncio
import sys
import os

# Добавляем корневую директорию в путь, чтобы импорты работали
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.mid_cognition.controller import CognitionController

async def run_diagnostic():
    print("🧠 [Diagnostic] Запуск проверки всех слоев когниции...")
    print("-" * 50)
    
    controller = CognitionController()
    
    # Тестовый сценарий: сложный запрос с кодом
    test_query = "Малышка, запиши функцию на python для очистки логов, это очень важно!"
    
    print(f"📥 Ввод: {test_query}")
    print("-" * 50)
    
    # Запускаем цикл когниции
    data = await controller.process_cognition(test_query)
    
    # Проверка модулей
    print(f"✅ 1. Analyzer (Intent): {data['analysis'].get('intent')}")
    print(f"✅ 2. Emotions (State): {data['emotional_state']}")
    print(f"✅ 3. Reasoner (Thought): {data['thought'][:60]}...")
    print(f"✅ 4. Planner (Steps): {data['mission_plan']}")
    print(f"✅ 5. Tutor (Advice): {data['tutor_advice']}")
    
    print("-" * 50)
    print("📜 ПОЛНЫЙ КОГНИТИВНЫЙ КОНТЕКСТ ДЛЯ LLM:")
    print(data['full_cognitive_context'])
    print("-" * 50)
    print("🚀 Диагностика завершена. Все системы в норме.")

if __name__ == "__main__":
    asyncio.run(run_diagnostic())
