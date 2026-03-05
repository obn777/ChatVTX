#!/bin/bash

# Переходим в директорию проекта
cd /home/obn7/NovBase || exit

# 1. Проверка и инициализация Git
if [ ! -d ".git" ]; then
    echo "⚙️ [Sync]: Инициализация нового репозитория..."
    git init
    git remote add origin https://github.com/obn777/ChatVTX.git
    git branch -M main
fi

# 2. Интеллектуальный фильтр (Игнорируем venv и лишний кэш)
if [ ! -f ".gitignore" ]; then
    echo "venv/" > .gitignore
    echo "__pycache__/" >> .gitignore
    echo "*.pyc" >> .gitignore
    echo ".env" >> .gitignore
    echo "📁 [Sync]: Создан базовый .gitignore"
fi

# 3. Синхронизация данных
echo "🔄 [Sync]: Индексация изменений в NovBase..."
git add .

# Проверяем, есть ли что коммитить, чтобы не плодить пустые логи
if git diff-index --quiet HEAD --; then
    echo "💤 [Sync]: Изменений не обнаружено. Пропуск."
else
    # Создаем коммит с временной меткой 2026 года
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    echo "📦 [Sync]: Создание слепка системы ($timestamp)..."
    git commit -m "NovBase Sync: $timestamp [Core & Memory Update]"

    # 4. Отправка на GitHub
    echo "🚀 [Sync]: Передача данных в репозиторий ChatVTX..."

    # Пытаемся запушить. Если не настроен SSH, потребуется Personal Access Token
    if git push -u origin main; then
        echo "✅ [Sync]: Данные успешно доставлены в ChatVTX!"
    else
        echo "❌ [Sync]: Ошибка синхронизации. Проверь сетевое соединение или права доступа (PAT)."
    fi
fi

# Возврат прав на выполнение (на всякий случай)
chmod +x "$0"
