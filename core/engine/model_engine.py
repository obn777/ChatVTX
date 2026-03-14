import os
from llama_cpp import Llama
# Пытаемся импортировать конфиг, если он есть
try:
    from core.config import config
except ImportError:
    config = None

class ModelEngine:
    """
    Интерфейс взаимодействия с LLM (Llama-3.1-8B).
    Оптимизировано под Nitro-ANV15-41 (RTX 3050 6GB).
    """
    def __init__(self, model_path=None, use_gpu=True):
        # Приоритет путей: Явный -> Внешний /home/obn7/models/ -> Конфиг
        default_external_path = "/home/obn7/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"

        if model_path:
            self.model_path = model_path
        elif os.path.exists(default_external_path):
            self.model_path = default_external_path
        elif config:
            self.model_path = config.get_model_path("main")
        else:
            self.model_path = default_external_path

        if not os.path.exists(self.model_path):
            print(f"❌ [ModelEngine FATAL]: Файл не найден по пути: {self.model_path}")
            self.llm = None
            return

        # --- НАСТРОЙКИ ОПТИМИЗАЦИИ ДЛЯ RTX 3050 6GB ---
        # 24 слоя на GPU + 2048 контекст для стабильности под Ubuntu GUI
        gpu_layers = 24 if use_gpu else 0
        context_size = 2048 if use_gpu else 4096
        mode_text = "Turbo-Hybrid (GPU/CPU)" if use_gpu else "Safe (CPU)"

        try:
            self.llm = Llama(
                model_path=self.model_path,
                n_ctx=context_size,
                n_gpu_layers=gpu_layers,
                n_threads=8,
                n_batch=512,
                verbose=False
            )
            if self.llm:
                print(f"✅ [ModelEngine]: Успешно инициализировано ({mode_text}).")
        except Exception as e:
            print(f"❌ [ModelEngine ERROR]: Сбой при создании контекста (VRAM): {e}")
            self.llm = None

    def get_answer(self, prompt: str, max_tokens: int = 1024) -> str:
        """
        Генерация ответа через VTX Core.
        :param max_tokens: Динамический лимит (150 для Lite, 1024 для Ultra).
        """
        if not self.llm:
            return "ОШИБКА: Движок не активен. Проверьте параметры VRAM."

        try:
            output = self.llm(
                prompt,
                max_tokens=max_tokens, # Теперь лимит управляется из LogicProcessor
                temperature=0.3,
                top_p=0.9,
                repeat_penalty=1.1,
                stop=["<|eot_id|>", "<|end_of_text|>", "User:", "Assistant:"],
                echo=False
            )
            return output['choices'][0]['text'].strip()
        except Exception as e:
            return f"❌ [ModelEngine]: Ошибка генерации: {e}"

    def get_token_count(self, text: str) -> int:
        """Подсчет токенов для MemoryManager."""
        if not self.llm: return 0
        return len(self.llm.tokenize(text.encode('utf-8')))
