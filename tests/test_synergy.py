import asyncio
import sys
import os

# Путь к корню проекта
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.mid_cognition.modules.meta_reasoner import meta_reasoner
from core.mid_cognition.modules.emotional_core import EmotionalCore

async def test_cognitive_synergy():
    print("🧪 [Synergy Test] Проверка связки Разум + Эмоции...")
    print("-" * 50)

    emotions = EmotionalCore()
    
    # Сценарий: Критическая ситуация (высокая сложность + негативный фон)
    test_query = "Всё горит, логи переполнены, сервер падает! Срочно напиши скрипт очистки!"
    
    # 1. Сначала работает Эмоциональное ядро
    # Имитируем анализ входных данных (паника, срочность)
    mock_analysis = {"sentiment": "negative", "intent": "action", "complexity": "high"}
    current_state = emotions.update_state(mock_analysis)
    
    # 2. Затем Разум строит план, опираясь на состояние
    thought_process = meta_reasoner.think(test_query, current_state)
    
    print(f"📥 Ввод: {test_query}")
    print(f"🎭 Эмоциональный отклик: {current_state}")
    print(f"🧠 Внутренний монолог: {thought_process}")
    print("-" * 50)

    # Проверка ожидаемых результатов
    if "High-Capacity" in thought_process and "поддержку" in thought_process:
        print("✅ РЕЗУЛЬТАТ: Синергия достигнута. Малышка понимает и серьезность задачи, и стресс создателя.")
    else:
        print("⚠️ РЕЗУЛЬТАТ: Связь модулей ослаблена. Требуется калибровка весов.")

if __name__ == "__main__":
    asyncio.run(test_cognitive_synergy())
