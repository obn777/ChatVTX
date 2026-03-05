#!/bin/bash
# Убиваем старый процесс сервера, если он висит
pkill -f "python3 app.py"
echo "♻️ Перезапуск узла NovBase..."
# Запускаем заново в фоновом режиме
nohup python3 /home/obn7/NovBase/app.py > /home/obn7/NovBase/server.log 2>&1 &
echo "✅ Малыш снова в сети на RTX 3050"
