# Путь к файлу: /home/obn7/NovBase/deploy_fix.py

import os
import sys
import json
import subprocess

def fix_deployment():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"🚀 [DeployFix]: Начинаю адаптацию NovBase в {base_dir}")

    # 1. Исправление путей в системных файлах
    config_path = os.path.join(base_dir, "configs/server_config.json")
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            cfg = json.load(f)
        
        cfg["base_path"] = base_dir
        cfg["storage_path"] = os.path.join(base_dir, "storage")
        
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(cfg, f, indent=4, ensure_ascii=False)
        print("✅ Пути в server_config.json обновлены.")

    # 2. Проверка Venv
    if not os.path.exists(os.path.join(base_dir, "venv")):
        print("⚠️ [ВНИМАНИЕ]: Виртуальное окружение 'venv' не найдено.")
        print("💡 Рекомендуется запустить: python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt")

    # 3. Поиск модели
    model_dir = os.path.join(base_dir, "models")
    models = [d for d in os.listdir(model_dir) if os.path.isdir(os.path.join(model_dir, d))]
    
    if models:
        print(f"🔎 Найдены модели: {', '.join(models)}")
        # Можно автоматически прописать первую найденную в загрузчик
    else:
        print("❌ Модели в папке /models не обнаружены.")

    # 4. Адаптация прав доступа
    print("🔐 Настройка прав на исполнение скриптов...")
    scripts = ["run_qwen.sh", "reboot_node.sh"]
    for s in scripts:
        s_path = os.path.join(base_dir, s)
        if os.path.exists(s_path):
            subprocess.run(["chmod", "+x", s_path])

    print("\n✅ [DeployFix]: Базовая настройка завершена.")
    print("🔗 Теперь проверь пути к модели в 'model_loader.py' и запускай 'app.py'.")

if __name__ == "__main__":
    fix_deployment()
