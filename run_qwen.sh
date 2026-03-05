#!/bin/bash
cd /home/obn7/NovBase
source venv/bin/activate
export PYTHONPATH=$PYTHONPATH:/home/obn7/NovBase
echo "🚀 Запуск сервера с Qwen2.5-7B..."
echo "📊 Модель: 5.5GB, оптимизация для RTX 3050 6GB"
echo ""
python3 main_qwen.py
