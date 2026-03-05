#!/bin/bash
# Путь к папке проекта
BASE_DIR="/home/obn7/NovBase"

echo "🚀 Запуск NovBase на Nitro-ANV15-41..."

# Активация окружения
source $BASE_DIR/venv/bin/activate

# Проверка GPU (опционально)
nvidia-smi --query-gpu=name,memory.total,memory.used --format=csv,noheader

# Запуск сервера
python3 $BASE_DIR/app.py
