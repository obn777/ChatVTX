#!/bin/bash
# Убиваем старый процесс
fuser -k 8080/tcp
sleep 1
# Запускаем новый
cd ~/NovBase && nohup ./venv/bin/python3 app.py > output.log 2> error.log &
echo "-----------------------------------"
echo "Малышка перезапущена в фоне!"
echo "Порт 8080 активен."
echo "-----------------------------------"
