from llama_cpp import Llama
import os

model_path = "/home/obn7/models/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf"
print(f"Checking {model_path}...")
try:
    llm = Llama(model_path=model_path, verbose=True)
    print("✅ SUCCESS: Model loaded!")
except Exception as e:
    print(f"❌ FAIL: {e}")
