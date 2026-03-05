import os
from llama_cpp import Llama
from core.config import config

class ModelEngine:
    """
    Интерфейс взаимодействия с LLM (Llama-3.1-8B).
    Оптимизировано под Nitro-ANV15-41 (GPU Offloading).
    """
    def __init__(self, model_path=None, mmproj_path=None):
        # Если путь не передан, берем из конфига 2026 года
        self.model_path = model_path or config.get_model_path("main")
        self.mmproj_path = mmproj_path or config.get_model_path("vision")
        
        # Параметры для GPU Nitro (RTX 4050/3050 6GB)
        # n_gpu_layers=33 выносит всю модель 8B Q4_K_M в видеопамять
        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=4096,           # Контекстное окно
                n_gpu_layers=33,      # Полный оффлоад на GPU
                n_threads=12,         # Потоки твоего процессора
                verbose=False         # Убираем лишний мусор из консоли
            )
            print(f"🚀 [ModelEngine]: Модель загружена в VRAM ({self.model_path})")
        except Exception as e:
            print(f"❌ [ModelEngine ERROR]: Ошибка загрузки модели: {e}")
            self.llm = None

    def get_answer(self, prompt: str) -> str:
        """Генерация ответа с учетом инженерных ограничений."""
        if not self.llm:
            return "ОШИБКА: Движок модели не инициализирован. Проверьте путь к GGUF файлу."

        try:
            # Настройка параметров генерации для "Интеллектуала"
            output = self.llm(
                prompt,
                max_tokens=1024,
                temperature=0.2,      # Низкая температура для точности кода
                top_p=0.9,
                stop=["<|eot_id|>", "User:"],
                echo=False
            )
            
            response_text = output['choices'][0]['text'].strip()
            return response_text
            
        except Exception as e:
            return f"❌ [ModelEngine]: Сбой во время генерации: {e}"

    def get_token_count(self, text: str) -> int:
        """Позволяет системе MemoryManager оценивать нагрузку на контекст."""
        return len(self.llm.tokenize(text.encode('utf-8')))
