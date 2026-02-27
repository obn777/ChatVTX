import os
import subprocess
from flask import Flask, render_template, send_from_directory

app = Flask(__name__, template_folder='templates')

# Основные пути
BASE_DIR = os.path.abspath(os.path.expanduser("~/NovBase"))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "static/downloads")
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.route('/')
def index():
    """Главная страница сайта (Зеленый интерфейс)"""
    return render_template('index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Раздача картинок (включая ai_avatar.png)"""
    return send_from_directory(STATIC_DIR, filename)

@app.route('/download/chatvtx.zip')
def download():
    """Раздача твоего основного архива проекта"""
    file_path = os.path.join(DOWNLOADS_DIR, "chatvtx.zip")
    
    if not os.path.exists(file_path):
        return "Файл еще загружается или не найден на сервере. Подождите завершения SCP.", 404
        
    # Проверяем размер для красоты (опционально)
    size_mb = os.path.getsize(file_path) / (1024 * 1024)
    print(f"Отдача файла chatvtx.zip, размер: {size_mb:.2f} MB")
    
    return send_from_directory(DOWNLOADS_DIR, "chatvtx.zip", as_attachment=True)

if __name__ == '__main__':
    # Автоматическая очистка порта 8000 перед стартом
    try:
        subprocess.run(["fuser", "-k", "8000/tcp"], check=False)
        print("Порт 8000 очищен.")
    except Exception as e:
        print(f"Запуск без очистки порта: {e}")

    print(f"Сайт запущен! Проверь его по адресу http://127.0.0.1:8000")
    # Запуск на всех интерфейсах внутри контейнера
    app.run(host='0.0.0.0', port=8000, debug=False)
