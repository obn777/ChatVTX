import re
import os
import gc
import datetime
from llama_cpp import Llama

class ModelEngine:
    def __init__(self, model_path, mmproj_path=None):
        # Оптимизация под Nitro (6GB VRAM): 
        # Используем свободные ресурсы CPU и RAM для расширения контекста
        print(f"📦 [SYSTEM]: Загрузка Llama-3.1-8B. Режим: МАКСИМАЛЬНАЯ ГЛУБИНА.")
        print(f"📊 [RESOURCE]: VRAM: 4.5/6GB | RAM: 4/15GB. Расширяем лимиты...")
        
        try:
            self.llm = Llama(
                model_path=model_path,
                n_gpu_layers=28,   
                # Увеличиваем контекст до 4096. 
                # Это съест еще ~500-800MB VRAM, как раз уложимся в лимит 6GB.
                n_ctx=4096,        
                n_threads=12,      # Поднимаем нагрузку на CPU (у тебя запас до 1600%)
                n_batch=1024,      # Ускоряем обработку промпта
                f16_kv=True,       
                verbose=False      
            )
            print("✅ [SYSTEM]: Движок Малышки переведен в режим лонгридов (4096 ctx).")
        except Exception as e:
            print(f"❌ [LOAD ERROR]: Ошибка инициализации GPU: {e}")
            raise

    def get_answer(self, prompt, is_vision=False):
        try:
            _log_engine("Запуск глубокой генерации (High-Capacity Mode)...")
            
            # max_tokens=1536 позволяет писать огромные статьи, 
            # сохраняя место для системного промпта и истории.
            res = self.llm(
                prompt, 
                max_tokens=1536, 
                stop=["<|eot_id|>", "User:", "Георгий:", "assistant", "<|start_header_id|>"], 
                temperature=0.75,   # Немного больше креатива для длинных текстов
                top_p=0.9,
                repeat_penalty=1.12 # Усиленная защита от зацикливания в длинных ответах
            )
            
            ans = res["choices"][0]["text"]
            final_text = self._clean_text(ans)
            
            gc.collect() 
            return final_text

        except Exception as e:
            gc.collect()
            _log_engine(f"Ошибка генерации: {e}")
            return f"Извини, произошел технический сбой при глубоком анализе: {e}"

    def _clean_text(self, text):
        """Очистка согласно инструкции от 26.02 (без спецсимволов)."""
        clean_ans = text.strip()
        junk_patterns = [
            r'^Георгий:\s*', r'^User:\s*', r'^assistant:\s*', 
            r'<\|.*?\|>', r'\|end_header_id\|>', r'assistant'
        ]
        for pattern in junk_patterns:
            clean_ans = re.sub(pattern, '', clean_ans, flags=re.IGNORECASE | re.MULTILINE).strip()
        
        # Удаляем вокальную читаемость символов
        clean_ans = clean_ans.replace("*", "").replace("#", "").replace("_", "")
        
        if clean_ans and not clean_ans[0].isupper():
            clean_ans = clean_ans[0].upper() + clean_ans[1:]
            
        return clean_ans

def _log_engine(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [ModelProxy]: {msg}")
