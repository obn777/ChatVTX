# Путь к файлу: /home/obn7/NovBase/model_loader.py

import os
import sys
import glob
import json

# --- СИЛОВОЕ ОГРАНИЧЕНИЕ ПОТОКОВ (УЛЬТИМАТИВНОЕ) ---
# Устанавливаем 4 потока, чтобы гарантированно уйти от цифр 1200-1600%
os.environ["OMP_NUM_THREADS"] = "4"
os.environ["MKL_NUM_THREADS"] = "4"
os.environ["OPENBLAS_NUM_THREADS"] = "4"
os.environ["VECLIB_MAXIMUM_THREADS"] = "4"
os.environ["NUMEXPR_NUM_THREADS"] = "4"

# ОТКЛЮЧАЕМ ГРАФЫ CUDA для стабильности на RTX 3050 (минимизация VRAM spikes)
os.environ["GGML_CUDA_NO_GRAPHS"] = "1"

print(f"--- [NovBase Loader]: Запуск Python из: {sys.executable} ---")

try:
    from llama_cpp import Llama
    from llama_cpp.llama_chat_format import Llava15ChatHandler
    print("--- [Loader]: Библиотека llama_cpp загружена (Лимит: 4 потока) ---")
except ImportError as e:
    print(f"--- [Loader] Ошибка импорта: {e} ---")
    sys.exit(1)

def get_base_path():
    """Динамическое определение корневой папки проекта для переносимости."""
    return os.path.dirname(os.path.abspath(__file__))

def get_latest_mobile_photo():
    """Находит последнее фото в папке Camera на Air1 Ultra через GVFS MTP"""
    try:
        gvfs_path = f"/run/user/{os.getuid()}/gvfs/"
        if not os.path.exists(gvfs_path):
            return None
        
        mtp_folders = [d for d in os.listdir(gvfs_path) if "Air1_Ultra" in d]
        if not mtp_folders:
            return None
        
        # Путь к папке камеры на Air1 Ultra
        camera_dir = os.path.join(
            gvfs_path, 
            mtp_folders[0], 
            "Внутренний общий накопитель/DCIM/Camera"
        )
        
        if not os.path.exists(camera_dir):
            return None

        files = glob.glob(os.path.join(camera_dir, "*.[jJ][pP][gG]"))
        if not files:
            return None
            
        latest_file = max(files, key=os.path.getmtime)
        return latest_file
    except Exception as e:
        print(f"⚠️ [MTP Error]: {e}")
        return None

def load_multimodal_model():
    """Загрузка LLaVA с автоматической подстройкой путей."""
    base_dir = get_base_path()
    
    # Пытаемся найти модель в локальной папке сервера или в общей папке моделей
    # Если ты переносишь базу, эти пути будут проверяться первыми
    potential_paths = [
        os.path.join(base_dir, "models/llava-llama-3-8b-v1_1.Q4_K_M.gguf"),
        "/home/obn7/server/llava-llama-3-8b-v1_1.Q4_K_M.gguf"
    ]
    
    potential_mmproj = [
        os.path.join(base_dir, "models/llava-llama-3-8b-v1_1-mmproj-f16.gguf"),
        "/home/obn7/server/llava-llama-3-8b-v1_1-mmproj-f16.gguf"
    ]

    model_path = next((p for p in potential_paths if os.path.exists(p)), None)
    mmproj_path = next((p for p in potential_mmproj if os.path.exists(p)), None)

    if not model_path or not mmproj_path:
        print(f"❌ [Loader]: Файлы модели не найдены! Проверено: {base_dir}/models/")
        return None

    try:
        print(f"--- [Loader]: Инициализация Видения (Проектор: {os.path.basename(mmproj_path)}) ---")
        chat_handler = Llava15ChatHandler(clip_model_path=mmproj_path, verbose=False)

        print(f"--- [Loader]: Загрузка LLM ({os.path.basename(model_path)}) ---")
        
        # Настройки оптимизированы под RTX 3050 (4GB/6GB VRAM)
        # n_gpu_layers=28: Почти вся модель в VRAM
        # n_threads=4: Чтобы CPU не закипал
        llm = Llama(
            model_path=model_path,
            chat_handler=chat_handler,
            n_ctx=2048,           
            n_gpu_layers=28,      
            n_threads=4,          
            n_threads_batch=4,    
            n_batch=512,          
            offload_kqv=True,     
            f16_kv=True,          
            use_mlock=False,      
            verbose=False         
        )
        return llm
    except Exception as e:
        print(f"❌ [Loader Error]: Ошибка инициализации Llama: {e}")
        return None

if __name__ == "__main__":
    print("--- [Loader]: Тестовый запуск с лимитом потоков ---")
    model = load_multimodal_model()
    if model:
        print("✅ [Loader]: ГОТОВО. Модель готова к работе в составе NovBase.")
    else:
        print("❌ [Loader]: ОШИБКА загрузки.")
