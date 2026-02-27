import base64, io, gc, re, os
from llama_cpp import Llama
from PIL import Image

class ModelEngine:
    def __init__(self, model_path, mmproj_path):
        print(f"📦 [SYSTEM]: Загрузка Llama-3.2-Vision (11B)...")
        
        try:
            self.llm = Llama(
                model_path=model_path,
                chat_handler=None, 
                n_gpu_layers=10, # Осторожно: 11B модель тяжелая для 6GB VRAM
                n_ctx=2048,      
                n_threads=12,
                n_batch=512,
                verbose=False,
                logits_all=True
            )
            
            from llama_cpp.llama_chat_format import Llava15ChatHandler
            self.chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path)
            self.llm.chat_handler = self.chat_handler
            
            print("✅ [SYSTEM]: Движок проинициализирован успешно.")
        except Exception as e:
            print(f"❌ [LOAD ERROR]: {e}")
            raise

        self.last_photo_path = "/home/obn7/server/static/last_risk.png"

    def _get_image_b64(self):
        try:
            if not os.path.exists(self.last_photo_path): return None
            with Image.open(self.last_photo_path) as img:
                img = img.convert("RGB").resize((560, 560)) 
                buf = io.BytesIO()
                img.save(buf, format="JPEG", quality=90)
                return base64.b64encode(buf.getvalue()).decode('utf-8')
        except Exception as e:
            return None

    def get_answer(self, prompt, is_vision=False):
        if not is_vision:
            is_vision = any(w in prompt.lower() for w in ["фото", "видишь", "изображение", "картинка"])
        
        image_b64 = self._get_image_b64() if is_vision else None

        try:
            if is_vision and image_b64:
                # Извлекаем чистый вопрос пользователя
                user_match = re.search(r'<\|start_header_id\|>user<\|end_header_id\|>\n(.*?)(?=<\|eot_id\|>)', prompt, re.DOTALL)
                clean_query = user_match.group(1).strip() if user_match else prompt

                res = self.llm.create_chat_completion(
                    messages=[{
                        "role": "user", 
                        "content": [
                            {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"}},
                            {"type": "text", "text": f"Будь краток. {clean_query}"}
                        ]
                    }],
                    max_tokens=512,
                    temperature=0.1
                )
                ans = res["choices"][0]["message"]["content"]
            else:
                res = self.llm(prompt, max_tokens=512, stop=["<|eot_id|>"], temperature=0.7)
                ans = res["choices"][0]["text"]

            return self._clean_text(ans)
        except Exception as e:
            return f"Ошибка анализа: {e}"

    def _clean_text(self, text):
        clean_ans = text.strip()
        junk_patterns = [r'^Георгий:\s*', r'^User:\s*', r'^assistant:\s*', r'<\|.*?\|>', r'\|end_header_id\|>']
        for pattern in junk_patterns:
            clean_ans = re.sub(pattern, '', clean_ans, flags=re.IGNORECASE | re.MULTILINE).strip()
        return clean_ans.capitalize()
