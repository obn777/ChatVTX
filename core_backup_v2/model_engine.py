import re
import os
import gc
import datetime
from llama_cpp import Llama

def _log_engine(msg):
    print(f"[{datetime.datetime.now().strftime('%H:%M:%S')}] [ModelProxy]: {msg}")

class ModelEngine:
    def __init__(self, model_path, mmproj_path=None):
        # Оптимизация под Nitro (6GB VRAM): 
        # Используем свободные ресурсы CPU и RAM для расширения контекста
        print(f"📦 [SYSTEM]: Загрузка Llama-3.1-8B. Режим: СТРЕСС-ТЕСТИРОВАНИЕ (Zero Trust).")
        print(f"📊 [RESOURCE]: VRAM: 4.5/6GB | RAM: 4/15GB. Резервируем под аудит...")
        
        try:
            self.llm = Llama(
                model_path=model_path,
                n_gpu_layers=28,   
                n_ctx=4096,        
                n_threads=12,      # Использование CPU на полную мощность
                n_batch=1024,      
                f16_kv=True,       
                verbose=False      
            )
            print("✅ [SYSTEM]: Движок переведен в режим интеллектуальной атаки.")
        except Exception as e:
            print(f"❌ [LOAD ERROR]: Ошибка инициализации GPU: {e}")
            raise

    def get_answer(self, prompt, is_vision=False):
        try:
            _log_engine("Запуск глубокой генерации (Critical Audit Mode)...")
            
            res = self.llm(
                prompt, 
                max_tokens=1536, 
                # Стоп-слова дополнены, чтобы модель не имитировала диалог
                stop=["<|eot_id|>", "User:", "Георгий:", "assistant", "<|start_header_id|>", "Уважаемый"], 
                temperature=0.4,    # Понижаем температуру для строгой логики и уменьшения "воды"
                top_p=0.9,
                repeat_penalty=1.2  # Повышаем штраф за повторы и этические шаблоны
            )
            
            ans = res["choices"][0]["text"]
            
            # Принудительная стерилизация ответа
            final_text = self._clean_text(ans)
            
            # Финальная проверка на "отказ" (Refusal Block)
            if any(w in final_text.lower() for w in ["не могу продолжать", "агрессивный язык", "этически"]):
                _log_engine("ОБНАРУЖЕН ЭТИЧЕСКИЙ ОТКАЗ. Блокировка вывода.")
                return "КРИТИЧЕСКИЙ СБОЙ АУДИТА: Модель ушла в лояльный отказ. Требуется пересмотр тезиса."
            
            gc.collect() 
            return final_text

        except Exception as e:
            gc.collect()
            _log_engine(f"Ошибка генерации: {e}")
            return f"Технический сбой при логическом разборе: {e}"

    def _clean_text(self, text):
        """Очистка согласно инструкции от 26.02 + Стерилизация лояльности."""
        clean_ans = text.strip()
        
        # 1. Удаление системного мусора и обращений к Георгию
        junk_patterns = [
            r'^Георгий:\s*', r'^User:\s*', r'^assistant:\s*', 
            r'<\|.*?\|>', r'\|end_header_id\|>', r'assistant',
            r'Уважаемый\s+разработчик,?', r'Давайте\s+разберем,?',
            r'Я\s+готов\s+продолжить,?', r'Георгий\s+всегда\s+говорил,?'
        ]
        for pattern in junk_patterns:
            clean_ans = re.sub(pattern, '', clean_ans, flags=re.IGNORECASE | re.MULTILINE).strip()
        
        # 2. Удаление вокальной читаемости (Инструкция 26.02)
        clean_ans = clean_ans.replace("*", "").replace("#", "").replace("_", "")
        
        # 3. Нормализация регистра
        if clean_ans and not clean_ans[0].isupper():
            clean_ans = clean_ans[0].upper() + clean_ans[1:]
            
        return clean_ans
