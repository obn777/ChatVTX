#!/bin/bash
while true; do
  if ! pgrep -f "app.py" > /dev/null
  then
    echo "Малыш упал! Запускаю оповещение о профилактике..."
    # Этот микро-код будет отвечать вместо Малыша, пока тот лежит
    python3 -c "
from flask import Flask, jsonify
app = Flask(__name__)
@app.route('/chat', methods=['POST'])
def sorry():
    return jsonify({'reply': 'извините идет профилактика, пожалуйста подключитесь позже, следите за индикатором. как только станет зеленым то вы снова с нами.'})
@app.route('/')
def health():
    return 'MAINTENANCE', 503
app.run(host='0.0.0.0', port=8080)
" &
    sleep 60 # Даем тебе время починить основу или отдохнуть
  fi
  sleep 10
done
